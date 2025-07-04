from streamlit.runtime.scriptrunner import RerunException, RerunData
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from frontendv2.servicios.cache import inicializar_snapshot_datos, limpiar_cache_y_snapshot
from frontendv2.ui.utils import boton_actualizar_datos
from frontendv2.servicios.api import calcular_ruta, calcular_rutas_todos
import logging


def mostrar():
    st.header("Explorar Red")
    st.info("Visualiza la red logística y calcula rutas entre almacenes y clientes considerando recarga por batería.")
    # Botón para forzar actualización de todos los datos
    boton_actualizar_datos(key_suffix="_red")

    # Verificar estado de simulación y snapshot único
    if 'datos_red' not in st.session_state:
        st.warning("No hay datos disponibles. Inicia la simulación primero.")
        return
    datos = st.session_state['datos_red']
    # Recuperar ruta resaltada solo si se acaba de calcular
    just_calc = st.session_state.pop('just_calc', False)
    highlighted_edges = st.session_state.get('highlighted_edges') if just_calc else None
    highlight_color = st.session_state.get('highlight_color', 'red')
    vertices = datos.get('vertices', [])
    aristas = datos.get('aristas', [])
    pedidos = datos.get('pedidos', [])
    clientes = datos.get('clientes', [])
    almacenamientos = datos.get('almacenamientos', [])
    recargas = datos.get('recargas', [])


    if not vertices or not aristas:
        st.warning("No hay datos de red disponibles. Inicializa la simulación primero.")
        return

    # Construir grafo coherente con backend
    G = nx.Graph()
    for v in vertices:
        G.add_node(v['id'], tipo=v.get('tipo', ''), nombre=v.get('nombre', ''))
    for a in aristas:
        G.add_edge(a['origen'], a['destino'], peso=a.get('peso', 1.0))

    # Visualización del grafo principal
    st.subheader("Red logística completa")
    pos = nx.spring_layout(G, seed=42, k=0.7, iterations=100)
    colores = {"cliente": "skyblue", "almacenamiento": "orange", "recarga": "green"}
    node_colors = [colores.get(G.nodes[n].get("tipo", ""), "gray") for n in G.nodes]
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700, ax=ax)
    
    # Dibujar aristas base
    nx.draw_networkx_edges(G, pos, edge_color="#888", width=1, ax=ax, alpha=0.6)
    
    # Si hay aristas resaltadas de cálculos previos, mostrarlas
    if highlighted_edges:
        # Verificar que las aristas resaltadas existen en el grafo actual
        valid_highlighted_edges = [edge for edge in highlighted_edges if G.has_edge(edge[0], edge[1])]
        if valid_highlighted_edges:
            nx.draw_networkx_edges(G, pos, edgelist=valid_highlighted_edges, 
                                 edge_color=highlight_color, width=4, ax=ax, alpha=0.8)
            st.info(f"Mostrando {len(valid_highlighted_edges)} aristas de la última ruta calculada")
    
    # Dibujar etiquetas de nodos
    nx.draw_networkx_labels(G, pos, labels={n: G.nodes[n].get('nombre', n) for n in G.nodes}, 
                          font_size=10, ax=ax)
    
    # Dibujar etiquetas de pesos en las aristas
    edge_labels = nx.get_edge_attributes(G, 'peso')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', ax=ax, font_size=8)
    
    # Agregar leyenda de tipos de vértices
    legend_labels = [plt.Line2D([0], [0], marker='o', color='w', label=tipo.capitalize(),
                                markerfacecolor=color, markersize=10) for tipo, color in colores.items()]
    ax.legend(handles=legend_labels, loc='upper right', title="Tipo de vértice")
    
    # Si hay ruta resaltada, agregar información
    if highlighted_edges:
        ax.set_title(f"Red Logística - Última ruta calculada resaltada ({len(highlighted_edges)} aristas)", 
                    fontsize=14, fontweight='bold')
    else:
        ax.set_title("Red Logística Completa", fontsize=14, fontweight='bold')
    
    ax.axis('off')
    st.pyplot(fig)

    # Si hay ruta resaltada, mostrar botón para limpiar
    if highlighted_edges:
        if st.button("🗑️ Limpiar ruta resaltada", key="limpiar_ruta_resaltada"):
            st.session_state.pop('highlighted_edges', None)
            st.session_state.pop('highlight_color', None)
            st.session_state.pop('just_calc', None)
            st.rerun()

    def limpiar_cliente_y_pedido():
        st.session_state.pop("cliente_id", None)
        st.session_state.pop("pedido_id", None)

    def limpiar_pedido():
        st.session_state.pop("pedido_id", None)

    # --- Selectores dependientes del snapshot global ---
    almacenes_opciones = {a["nombre"]: a["id"] for a in almacenamientos}
    almacen_id = st.selectbox(
        "Selecciona un almacén de origen",
        options=list(almacenes_opciones.values()),
        format_func=lambda x: [k for k, v in almacenes_opciones.items() if v == x][0],
        key="almacen_id",
        on_change=limpiar_cliente_y_pedido
    )

    pedidos_almacen = [p for p in pedidos if (p.get("origen") or p.get("origen_id") or p.get("origen", {}).get("id")) == almacen_id]

    clientes_ids = set(
        (p.get("destino") or p.get("destino_id") or p.get("destino", {}).get("id"))
        for p in pedidos_almacen
    )
    clientes_filtrados = [c for c in clientes if c["id"] in clientes_ids]
    clientes_opciones = {c["nombre"]: c["id"] for c in clientes_filtrados}

    cliente_id = st.selectbox(
        "Selecciona un cliente destino",
        options=list(clientes_opciones.values()),
        format_func=lambda x: [k for k, v in clientes_opciones.items() if v == x][0],
        key=f"cliente_id_{almacen_id}",
        on_change=limpiar_pedido
    )

    # 4. Filtrar pedidos por almacén y cliente
    pedidos_filtrados = [
        p for p in pedidos_almacen
        if (p.get("destino") or p.get("destino_id") or p.get("destino", {}).get("id")) == cliente_id
    ]
    pedido_opciones = [p["id_pedido"] for p in pedidos_filtrados if "id_pedido" in p and p["id_pedido"] is not None]

    if not pedido_opciones:
        st.info("No hay pedidos disponibles para este cliente y almacén.")
        pedido_id = None
    else:
        pedido_id = st.selectbox(
            "Selecciona un pedido",
            options=pedido_opciones,
            format_func=str,
            key=f"pedido_id_{almacen_id}_{cliente_id}"
        )

    # --- Selección de algoritmo de ruta ---
    algoritmos = [
        ("BFS", "bfs"),
        ("DFS", "dfs"),
        ("Dijkstra", "dijkstra"),
        ("Floyd-Warshall", "floydwarshall"),
        ("Topological Sort", "topologicalsort"),
        ("Todos", "todos")
    ]
    algoritmo_opciones = [a[0] for a in algoritmos]
    algoritmo_seleccionado = st.radio(
        "Selecciona el algoritmo de cálculo de ruta",
        options=algoritmo_opciones,
        key=f"algoritmo_ruta_{almacen_id}_{cliente_id}"
    )
    algoritmo_key = dict(algoritmos)[algoritmo_seleccionado]

    # Botón para calcular ruta del pedido seleccionado
    if st.button("Calcular ruta", key="calcular_ruta"):
        if not pedido_id:
            st.warning("Selecciona un pedido válido.")
        else:
            resultados = {}
            # Llamada real a la API
            if algoritmo_key != "todos":
                try:
                    res = calcular_ruta(pedido_id, algoritmo_key)
                    resultados[algoritmo_key] = res
                except Exception as e:
                    resultados[algoritmo_key] = {"error": str(e)}
            else:
                try:
                    rutas = calcular_rutas_todos(pedido_id)
                    # se asume que retorna dict con algoritmos como claves
                    resultados = rutas.get('rutas', rutas)
                except Exception as e:
                    resultados = {"todos": {"error": str(e)}}
            
            # Mostrar comparativa de resultados
            datos_tabla = []
            for alg, res in resultados.items():
                if 'error' in res:
                    st.error(f"Algoritmo {alg.upper()}: {res['error']}")
                else:
                    datos_tabla.append({
                        'Algoritmo': alg.upper(),
                        'ID Ruta': res.get('id_ruta'),
                        'Peso': res.get('peso_total'),
                        'Recarga': 'Sí' if res.get('requiere_recarga') else 'No'
                    })
            if datos_tabla:
                st.subheader("Comparativa de rutas")
                st.table(datos_tabla)
            
            # Resaltar caminos en el grafo
            st.subheader("Visualización de rutas calculadas")
            fig2, ax2 = plt.subplots(figsize=(12, 8))
            
            # Dibujar el grafo base
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700, ax=ax2)
            nx.draw_networkx_edges(G, pos, edge_color="#cccccc", width=1, ax=ax2, alpha=0.5)
            nx.draw_networkx_labels(G, pos, labels={n: G.nodes[n].get('nombre', n) for n in G.nodes}, 
                                  font_size=10, ax=ax2)
            
            # Agregar etiquetas de peso de todas las aristas
            edge_labels = nx.get_edge_attributes(G, 'peso')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='gray', 
                                       font_size=8, ax=ax2)
            
            # Colores por algoritmo
            color_map = {'bfs':'blue','dfs':'purple','dijkstra':'red','floydwarshall':'green','topologicalsort':'orange'}
            legend_elements = []
            aristas_resaltadas_totales = 0
            
            # Procesar cada resultado para resaltar las aristas del camino
            for alg, res in resultados.items():
                if 'error' in res:
                    continue
                
                # Priorizar el campo 'camino' si está disponible
                camino = res.get('camino', [])
                edges_camino = []
                
                if camino and len(camino) >= 2:
                    # Usar la secuencia de vértices del camino
                    edges_camino = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
                    st.info(f"🎯 {alg.upper()}: Usando camino de vértices ({len(camino)} vértices)")
                else:
                    # Respaldo: usar aristas_ids
                    aristas_ids = res.get('aristas_ids', [])
                    if aristas_ids:
                        for arista_id in aristas_ids:
                            try:
                                origen_id, destino_id = map(int, arista_id.split('-'))
                                edges_camino.append((origen_id, destino_id))
                            except (ValueError, IndexError):
                                continue
                        st.info(f"📋 {alg.upper()}: Usando aristas_ids ({len(aristas_ids)} aristas)")
                    else:
                        st.warning(f"⚠️ {alg.upper()}: No hay camino ni aristas disponibles")
                        continue
                
                # Dibujar las aristas resaltadas del camino
                if edges_camino:
                    color = color_map.get(alg, 'cyan')
                    # Verificar que las aristas existen en el grafo
                    edges_validas = [edge for edge in edges_camino if G.has_edge(edge[0], edge[1])]
                    
                    if edges_validas:
                        nx.draw_networkx_edges(G, pos, edgelist=edges_validas, width=4,
                                             edge_color=color, ax=ax2, alpha=0.8)
                        aristas_resaltadas_totales += len(edges_validas)
                        
                        # Agregar a la leyenda
                        legend_elements.append(plt.Line2D([0], [0], color=color, lw=4, 
                                                        label=f'{alg.upper()} ({len(edges_validas)} aristas)'))
                        
                        st.success(f"✅ {alg.upper()}: {len(edges_validas)} aristas resaltadas correctamente")
                    else:
                        st.error(f"❌ {alg.upper()}: Las aristas del camino no existen en el grafo")
                        # Debug: mostrar qué aristas se intentaron dibujar
                        st.write(f"Aristas intentadas: {edges_camino[:5]}...")  # Mostrar solo las primeras 5
                else:
                    st.warning(f"⚠️ {alg.upper()}: No se pudieron extraer aristas del resultado")
            
            # Agregar leyenda de algoritmos si hay resultados válidos
            if legend_elements:
                ax2.legend(handles=legend_elements, loc='upper left', title="Rutas calculadas", 
                         bbox_to_anchor=(0, 1), fontsize=9)
            
            # Agregar leyenda de tipos de vértices
            vertex_legend = [plt.Line2D([0], [0], marker='o', color='w', label=tipo.capitalize(),
                                       markerfacecolor=color, markersize=10) 
                           for tipo, color in {"cliente": "skyblue", "almacenamiento": "orange", "recarga": "green"}.items()]
            ax2.legend(handles=vertex_legend, loc='upper right', title="Tipo de vértice", 
                     bbox_to_anchor=(1, 1), fontsize=9)
            
            ax2.set_title(f"Rutas calculadas - {aristas_resaltadas_totales} aristas resaltadas", 
                        fontsize=14, fontweight='bold')
            ax2.axis('off')
            
            st.pyplot(fig2)
            
            # Almacenar información para resaltado persistente (tomar el primer resultado válido)
            for alg_key, res in resultados.items():
                if 'error' not in res:
                    # Priorizar el campo 'camino'
                    camino = res.get('camino', [])
                    if camino and len(camino) >= 2:
                        edges = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
                        st.session_state['highlighted_edges'] = edges
                        st.session_state['highlight_color'] = color_map.get(alg_key, 'cyan')
                        st.session_state['just_calc'] = True
                        break
                    elif res.get('aristas_ids'):
                        # Respaldo: usar aristas_ids
                        try:
                            edges = [tuple(map(int, s.split('-'))) for s in res['aristas_ids']]
                            st.session_state['highlighted_edges'] = edges
                            st.session_state['highlight_color'] = color_map.get(alg_key, 'cyan')
                            st.session_state['just_calc'] = True
                            break
                        except (ValueError, IndexError):
                            continue
            
            st.success("✅ Ruta(s) calculada(s) y visualizada(s) correctamente.")

    st.caption("Selecciona un almacén, un cliente y un pedido para calcular la ruta. El grafo muestra los pesos de las aristas y la leyenda de vértices.")

    # --- Sección del Árbol de Expansión Mínima (Kruskal) ---
    st.divider()
    st.subheader("Árbol de Expansión Mínima (Kruskal)")
    st.info("Calcula y visualiza el árbol de expansión mínima de toda la red usando el algoritmo de Kruskal.")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("Calcular Árbol Mínimo (Kruskal)", key="calcular_mst_kruskal"):
            try:
                from frontendv2.servicios.api import calcular_mst_kruskal
                
                with st.spinner("Calculando árbol de expansión mínima..."):
                    mst_data = calcular_mst_kruskal()
                
                # Debug: mostrar estructura de datos recibidos
                st.write("**Debug - Datos recibidos del MST:**")
                st.json(mst_data)
                
                # Debug: mostrar vértices disponibles en el snapshot
                st.write("**Debug - Vértices en el snapshot:**")
                vertices_info = [{"id": v["id"], "nombre": v.get("nombre", ""), "tipo": v.get("tipo", "")} for v in vertices[:10]]  # Mostrar solo los primeros 10
                st.json(vertices_info)
                
                # Almacenar el resultado en session_state para persistencia
                st.session_state['mst_kruskal_data'] = mst_data
                st.success(f"Árbol mínimo calculado. Peso total: {mst_data.get('peso_total', 'N/A')}")
                
            except Exception as e:
                st.error(f"Error al calcular el árbol mínimo: {str(e)}")
    
    with col2:
        # Mostrar información del MST si está disponible
        if 'mst_kruskal_data' in st.session_state:
            mst_data = st.session_state['mst_kruskal_data']
            st.write(f"**Peso total del MST:** {mst_data.get('peso_total', 'N/A')}")
            st.write(f"**Número de aristas:** {len(mst_data.get('aristas', []))}")
    
    # Visualización permanente del MST si está disponible
    if 'mst_kruskal_data' in st.session_state:
        mst_data = st.session_state['mst_kruskal_data']
        aristas_mst = mst_data.get('aristas', [])
        vertices_en_mst = set(mst_data.get('vertices_en_mst', []))
        
        if aristas_mst:
            st.subheader("Visualización del Árbol Mínimo")
            
            # Usar el grafo original como base y resaltar las aristas del MST
            # En lugar de crear un nuevo grafo, usar el mismo layout y datos
            fig_mst, ax_mst = plt.subplots(figsize=(12, 8))
            
            # Dibujar todos los nodos del grafo original
            nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                                 node_size=700, ax=ax_mst, alpha=0.7)
            
            # Dibujar todas las aristas originales en gris claro
            nx.draw_networkx_edges(G, pos, edge_color='lightgray', width=1, ax=ax_mst, alpha=0.3)
            
            # Crear lista de aristas del MST para resaltar
            aristas_mst_tuples = []
            for arista in aristas_mst:
                origen = arista.get('origen')
                destino = arista.get('destino')
                # Verificar que los vértices existen en el grafo
                if origen in G.nodes and destino in G.nodes:
                    aristas_mst_tuples.append((origen, destino))
            
            # Dibujar aristas del MST en color destacado
            if aristas_mst_tuples:
                nx.draw_networkx_edges(G, pos, edgelist=aristas_mst_tuples, 
                                     edge_color='red', width=4, ax=ax_mst)
            
            # Dibujar etiquetas de nodos
            nx.draw_networkx_labels(G, pos, 
                                  labels={n: G.nodes[n].get('nombre', n) for n in G.nodes},
                                  font_size=10, ax=ax_mst)
            
            # Dibujar etiquetas de pesos solo en las aristas del MST
            edge_labels_mst = {}
            for arista in aristas_mst:
                origen = arista.get('origen')
                destino = arista.get('destino')
                peso = arista.get('peso')
                if origen in G.nodes and destino in G.nodes:
                    # Usar la arista en cualquier dirección
                    if G.has_edge(origen, destino):
                        edge_labels_mst[(origen, destino)] = peso
                    elif G.has_edge(destino, origen):
                        edge_labels_mst[(destino, origen)] = peso
            
            if edge_labels_mst:
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels_mst, 
                                           font_color='darkred', font_size=10, ax=ax_mst)
            
            # Agregar leyenda
            legend_labels = [plt.Line2D([0], [0], marker='o', color='w', label=tipo.capitalize(),
                                       markerfacecolor=color, markersize=12) 
                           for tipo, color in colores.items()]
            # Agregar línea para MST
            legend_labels.append(plt.Line2D([0], [0], color='red', linewidth=4, label='Aristas MST'))
            ax_mst.legend(handles=legend_labels, loc='upper right', title="Elementos")
            
            ax_mst.set_title(f"Árbol de Expansión Mínima (Kruskal)\nPeso Total: {mst_data.get('peso_total', 'N/A')}", 
                           fontsize=14, fontweight='bold')
            ax_mst.axis('off')
            
            st.pyplot(fig_mst)
            
            # Mostrar tabla con las aristas del MST
            st.subheader("Aristas del Árbol Mínimo")
            tabla_mst = []
            for arista in aristas_mst:
                origen_id = arista.get('origen')
                destino_id = arista.get('destino')
                
                # Buscar los nombres de los vértices en los datos del snapshot
                origen_nombre = f"ID:{origen_id}"
                destino_nombre = f"ID:{destino_id}"
                
                # Buscar en vértices para obtener nombres
                for v in vertices:
                    if v['id'] == origen_id:
                        origen_nombre = v.get('nombre', f"ID:{origen_id}")
                    if v['id'] == destino_id:
                        destino_nombre = v.get('nombre', f"ID:{destino_id}")
                
                tabla_mst.append({
                    'Origen': origen_nombre,
                    'Destino': destino_nombre,
                    'Peso': arista.get('peso', 'N/A')
                })
            
            if tabla_mst:
                st.table(tabla_mst)
            else:
                st.warning("No se encontraron aristas válidas en el MST.")
    
    # Botón para limpiar el MST
    if 'mst_kruskal_data' in st.session_state:
        if st.button("Limpiar Árbol Mínimo", key="limpiar_mst"):
            del st.session_state['mst_kruskal_data']
            st.rerun()