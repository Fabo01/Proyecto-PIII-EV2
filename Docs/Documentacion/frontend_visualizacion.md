# Documentación del Frontend y Visualización

## Descripción General
El frontend del sistema está desarrollado con Streamlit y proporciona una interfaz web interactiva para gestionar y visualizar todos los aspectos del sistema logístico de drones. Está organizado en múltiples pestañas funcionales que permiten ejecutar simulaciones, explorar la red, gestionar pedidos, analizar rutas y visualizar estadísticas.

## Ubicación en la Arquitectura
- **Capa de Presentación**: `frontend/` y `frontendv2/`
- **Tecnología**: Streamlit, Matplotlib, NetworkX, Plotly
- **Responsabilidad**: Interfaz de usuario y visualización de datos

## Estructura del Frontend

### Organización de Archivos
```
frontend/
├── main.py                    # Aplicación principal Streamlit
├── servicios/                 # Servicios para comunicación con API
│   ├── api.py                # Cliente API REST
│   └── cache.py              # Cache del frontend
├── ui/                       # Componentes de interfaz de usuario
│   ├── clientes.py           # Gestión de clientes
│   ├── estadisticas.py       # Visualización de estadísticas
│   ├── hashmaps.py          # Visualización de estructuras TDA
│   ├── listas.py            # Gestión de listas
│   ├── red.py               # Visualización de red principal
│   ├── red_interactiva.py   # Red interactiva avanzada
│   ├── rutas.py             # Gestión y visualización de rutas
│   └── simulacion.py        # Control de simulación
├── utils/                    # Utilidades y validadores
│   ├── errores.py           # Manejo de errores
│   └── validadores.py       # Validaciones de entrada
└── visualizacion/           # Componentes de visualización
    ├── avl.py              # Visualización de árbol AVL
    ├── charts.py           # Gráficos estadísticos
    └── grafo.py            # Visualización de grafos
```

## 1. Aplicación Principal

### Configuración y Layout Principal
```python
# frontend/main.py

import streamlit as st
import sys
import os

# Configuración de la página
st.set_page_config(
    page_title="Sistema Logístico Drones - Correos Chile",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para mejorar la apariencia
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #3b82f6;
    }
    
    .success-alert {
        background: #d1fae5;
        border: 1px solid #10b981;
        color: #065f46;
        padding: 0.75rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .warning-alert {
        background: #fef3c7;
        border: 1px solid #f59e0b;
        color: #92400e;
        padding: 0.75rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Función principal de la aplicación"""
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>🚁 Sistema Logístico de Drones</h1>
        <h3>Correos Chile - Simulación y Gestión de Entregas</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar conexión con API
    if not verificar_conexion_api():
        st.error("❌ No se puede conectar con el backend. Verifique que el servidor esté ejecutándose.")
        st.info("💡 Ejecute: `uvicorn Backend.API.main:app --reload` en la terminal")
        return
    
    # Sidebar con información del sistema
    mostrar_sidebar_sistema()
    
    # Menú principal de pestañas
    tabs = st.tabs([
        "🎮 Simulación",
        "🌐 Explorar Red", 
        "👥 Clientes y Pedidos",
        "📊 Análisis de Rutas",
        "📈 Estadísticas",
        "🔧 Estructuras TDA"
    ])
    
    with tabs[0]:
        from ui.simulacion import mostrar_pestaña_simulacion
        mostrar_pestaña_simulacion()
    
    with tabs[1]:
        from ui.red import mostrar_pestaña_red
        mostrar_pestaña_red()
    
    with tabs[2]:
        from ui.clientes import mostrar_pestaña_clientes
        mostrar_pestaña_clientes()
    
    with tabs[3]:
        from ui.rutas import mostrar_pestaña_rutas
        mostrar_pestaña_rutas()
    
    with tabs[4]:
        from ui.estadisticas import mostrar_pestaña_estadisticas
        mostrar_pestaña_estadisticas()
    
    with tabs[5]:
        from ui.hashmaps import mostrar_pestaña_tda
        mostrar_pestaña_tda()

def verificar_conexion_api():
    """Verifica conectividad con el backend"""
    try:
        from servicios.api import ClienteAPI
        cliente = ClienteAPI()
        respuesta = cliente.obtener_estado_simulacion()
        return respuesta is not None
    except Exception:
        return False

def mostrar_sidebar_sistema():
    """Muestra información del sistema en el sidebar"""
    with st.sidebar:
        st.markdown("### 📊 Estado del Sistema")
        
        # Obtener estado actual
        try:
            from servicios.api import ClienteAPI
            cliente = ClienteAPI()
            estado = cliente.obtener_estado_simulacion()
            
            if estado and estado.get('simulacion_activa'):
                st.success("✅ Simulación Activa")
                
                metricas = estado.get('metricas_generales', {})
                st.metric("Vértices", metricas.get('total_vertices', 0))
                st.metric("Aristas", metricas.get('total_aristas', 0))
                st.metric("Pedidos", metricas.get('total_pedidos', 0))
                
                # Progreso de pedidos
                completados = metricas.get('pedidos_completados', 0)
                total = metricas.get('total_pedidos', 1)
                progreso = completados / total if total > 0 else 0
                
                st.progress(progreso)
                st.caption(f"Completados: {completados}/{total}")
                
            else:
                st.warning("⚠️ Sin Simulación Activa")
                st.info("Inicie una simulación en la pestaña correspondiente")
        
        except Exception:
            st.error("❌ Error de Conexión")
        
        st.markdown("---")
        
        # Información de la aplicación
        st.markdown("### ℹ️ Información")
        st.caption("**Versión:** 1.0.0")
        st.caption("**Tecnología:** Streamlit + FastAPI")
        st.caption("**Autor:** Equipo de Desarrollo")

if __name__ == "__main__":
    main()
```

## 2. Pestaña de Simulación

### Control de Simulación
```python
# frontend/ui/simulacion.py

def mostrar_pestaña_simulacion():
    """Pestaña para configurar e iniciar simulaciones"""
    
    st.header("🎮 Configuración de Simulación")
    
    # Columnas para organizar controles
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Parámetros de Simulación")
        
        # Controles de configuración
        with st.form("config_simulacion"):
            # Slider para vértices
            num_vertices = st.slider(
                "🏢 Número de Vértices",
                min_value=10,
                max_value=150,
                value=15,
                help="Total de puntos en la red (clientes, almacenes, recargas)"
            )
            
            # Slider para aristas
            min_aristas = num_vertices - 1  # Mínimo para conectividad
            max_aristas = min(300, (num_vertices * (num_vertices - 1)) // 2)
            
            num_aristas = st.slider(
                "🔗 Número de Aristas",
                min_value=min_aristas,
                max_value=max_aristas,
                value=max(20, min_aristas),
                help=f"Conexiones entre vértices (mínimo {min_aristas} para conectividad)"
            )
            
            # Slider para pedidos
            num_pedidos = st.slider(
                "📦 Número de Pedidos",
                min_value=1,
                max_value=500,
                value=10,
                help="Pedidos iniciales a generar"
            )
            
            # Información calculada
            st.markdown("#### 📊 Distribución de Vértices")
            clientes = int(num_vertices * 0.6)
            almacenes = int(num_vertices * 0.2)
            recargas = num_vertices - clientes - almacenes
            
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.metric("👥 Clientes", f"{clientes} (60%)")
            with col_info2:
                st.metric("🏪 Almacenes", f"{almacenes} (20%)")
            with col_info3:
                st.metric("⚡ Recargas", f"{recargas} (~20%)")
            
            # Botón para iniciar simulación
            iniciar = st.form_submit_button(
                "🚀 Iniciar Simulación",
                type="primary",
                use_container_width=True
            )
            
            if iniciar:
                iniciar_nueva_simulacion(num_vertices, num_aristas, num_pedidos)
    
    with col2:
        st.subheader("📈 Estado Actual")
        mostrar_estado_simulacion_actual()
        
        st.subheader("⚙️ Controles Avanzados")
        
        if st.button("🔄 Reiniciar Simulación", type="secondary"):
            reiniciar_simulacion()
        
        if st.button("📋 Generar Reporte", type="secondary"):
            generar_reporte_simulacion()
        
        # Configuraciones adicionales
        with st.expander("⚙️ Configuración Avanzada"):
            autonomia_dron = st.number_input(
                "Autonomía del Dron",
                min_value=10.0,
                max_value=100.0,
                value=50.0,
                step=5.0,
                help="Autonomía máxima en unidades de energía"
            )
            
            algoritmo_ruta = st.selectbox(
                "Algoritmo de Ruta",
                ["BFS", "DFS", "Dijkstra"],
                index=0,
                help="Algoritmo para cálculo de rutas"
            )
            
            st.session_state.config_avanzada = {
                'autonomia_dron': autonomia_dron,
                'algoritmo_ruta': algoritmo_ruta
            }

def iniciar_nueva_simulacion(num_vertices: int, num_aristas: int, num_pedidos: int):
    """Inicia una nueva simulación con los parámetros dados"""
    
    with st.spinner("🔄 Inicializando simulación..."):
        try:
            from servicios.api import ClienteAPI
            cliente_api = ClienteAPI()
            
            # Preparar datos para la API
            datos_simulacion = {
                "num_vertices": num_vertices,
                "num_aristas": num_aristas,
                "num_pedidos": num_pedidos,
                "porcentaje_clientes": 0.6,
                "porcentaje_almacenes": 0.2,
                "porcentaje_recargas": 0.2
            }
            
            # Llamar API
            respuesta = cliente_api.inicializar_simulacion(datos_simulacion)
            
            if respuesta and respuesta.get('exito'):
                st.success("✅ ¡Simulación iniciada exitosamente!")
                
                # Mostrar detalles de la simulación creada
                datos = respuesta.get('datos', {})
                
                st.markdown("#### 🎯 Simulación Creada")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("ID Simulación", datos.get('simulacion_id', 'N/A'))
                with col2:
                    st.metric("Vértices Creados", datos.get('vertices_creados', 0))
                with col3:
                    st.metric("Conectividad", "✅" if datos.get('conectividad_verificada') else "❌")
                
                # Invalidar cache para forzar actualización
                if 'cache' in st.session_state:
                    st.session_state.cache.clear()
                
                # Recargar página para mostrar nuevos datos
                st.rerun()
                
            else:
                mensaje_error = respuesta.get('mensaje', 'Error desconocido') if respuesta else 'No se recibió respuesta'
                st.error(f"❌ Error al iniciar simulación: {mensaje_error}")
        
        except Exception as e:
            st.error(f"❌ Error de conexión: {str(e)}")
            st.info("💡 Verifique que el backend esté ejecutándose")

def mostrar_estado_simulacion_actual():
    """Muestra el estado actual de la simulación"""
    
    try:
        from servicios.api import ClienteAPI
        cliente_api = ClienteAPI()
        estado = cliente_api.obtener_estado_simulacion()
        
        if not estado:
            st.warning("⚠️ No hay simulación activa")
            return
        
        if estado.get('simulacion_activa'):
            st.success("✅ Simulación Activa")
            
            # Métricas principales
            metricas = estado.get('metricas_generales', {})
            
            st.metric("🆔 ID", estado.get('simulacion_id', 'N/A'))
            st.metric("⏱️ Tiempo", estado.get('tiempo_transcurrido', '00:00:00'))
            
            # Estado de pedidos
            total = metricas.get('total_pedidos', 0)
            completados = metricas.get('pedidos_completados', 0)
            en_proceso = metricas.get('pedidos_en_proceso', 0)
            pendientes = metricas.get('pedidos_pendientes', 0)
            
            # Gráfico de estado de pedidos
            if total > 0:
                fig_estado = crear_grafico_estado_pedidos(completados, en_proceso, pendientes)
                st.plotly_chart(fig_estado, use_container_width=True)
        else:
            st.info("ℹ️ Sin simulación activa")
    
    except Exception as e:
        st.error("❌ Error al obtener estado")

def crear_grafico_estado_pedidos(completados: int, en_proceso: int, pendientes: int):
    """Crea gráfico del estado de pedidos"""
    import plotly.graph_objects as go
    
    labels = ['Completados', 'En Proceso', 'Pendientes']
    values = [completados, en_proceso, pendientes]
    colors = ['#10b981', '#f59e0b', '#ef4444']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker_colors=colors,
        hole=0.4
    )])
    
    fig.update_layout(
        title="Estado de Pedidos",
        height=300,
        showlegend=True,
        margin=dict(t=50, b=0, l=0, r=0)
    )
    
    return fig
```

## 3. Pestaña de Exploración de Red

### Visualización Interactiva del Grafo
```python
# frontend/ui/red.py

def mostrar_pestaña_red():
    """Pestaña para explorar y visualizar la red de transporte"""
    
    st.header("🌐 Explorar Red de Transporte")
    
    # Verificar simulación activa
    if not verificar_simulacion_activa():
        st.warning("⚠️ Inicie una simulación para explorar la red")
        return
    
    # Layout en dos columnas
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📍 Visualización de la Red")
        mostrar_grafo_red()
    
    with col2:
        st.subheader("🛣️ Calcular Ruta")
        mostrar_calculadora_rutas()

def mostrar_grafo_red():
    """Visualiza el grafo de la red con NetworkX y Matplotlib"""
    
    try:
        from servicios.api import ClienteAPI
        from visualizacion.grafo import VisualizadorGrafo
        
        cliente_api = ClienteAPI()
        
        # Obtener datos de la red
        vertices = cliente_api.obtener_vertices()
        aristas = cliente_api.obtener_aristas()
        
        if not vertices or not aristas:
            st.error("❌ No se pudieron obtener datos de la red")
            return
        
        # Crear visualizador
        visualizador = VisualizadorGrafo()
        
        # Opciones de visualización
        with st.expander("⚙️ Opciones de Visualización"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                mostrar_etiquetas = st.checkbox("Mostrar Etiquetas", value=True)
                mostrar_pesos = st.checkbox("Mostrar Pesos", value=False)
            
            with col2:
                layout_algoritmo = st.selectbox(
                    "Algoritmo de Layout",
                    ["spring", "circular", "kamada_kawai", "planar"],
                    index=0
                )
            
            with col3:
                tamaño_nodos = st.slider("Tamaño de Nodos", 100, 1000, 300)
                ancho_aristas = st.slider("Grosor de Aristas", 1, 5, 2)
        
        # Generar y mostrar gráfico
        fig = visualizador.crear_grafico_red(
            vertices=vertices,
            aristas=aristas,
            mostrar_etiquetas=mostrar_etiquetas,
            mostrar_pesos=mostrar_pesos,
            layout=layout_algoritmo,
            tamaño_nodos=tamaño_nodos,
            ancho_aristas=ancho_aristas
        )
        
        st.pyplot(fig)
        
        # Información adicional
        with st.expander("📊 Información de la Red"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Vértices", len(vertices))
                clientes = len([v for v in vertices if v.get('tipo') == 'cliente'])
                st.metric("Clientes", clientes)
            
            with col2:
                st.metric("Total Aristas", len(aristas))
                almacenes = len([v for v in vertices if v.get('tipo') == 'almacenamiento'])
                st.metric("Almacenes", almacenes)
            
            with col3:
                densidad = (2 * len(aristas)) / (len(vertices) * (len(vertices) - 1)) if len(vertices) > 1 else 0
                st.metric("Densidad", f"{densidad:.3f}")
                recargas = len([v for v in vertices if v.get('tipo') == 'recarga'])
                st.metric("Estaciones Recarga", recargas)
    
    except Exception as e:
        st.error(f"❌ Error al visualizar la red: {str(e)}")

def mostrar_calculadora_rutas():
    """Interfaz para calcular rutas entre vértices"""
    
    try:
        from servicios.api import ClienteAPI
        
        cliente_api = ClienteAPI()
        vertices = cliente_api.obtener_vertices()
        
        if not vertices:
            st.error("❌ No hay vértices disponibles")
            return
        
        # Formulario para seleccionar origen y destino
        with st.form("calcular_ruta"):
            st.markdown("#### 📍 Seleccionar Puntos")
            
            # Filtrar vértices por tipo para facilitar selección
            almacenes = [v for v in vertices if v.get('tipo') == 'almacenamiento']
            clientes = [v for v in vertices if v.get('tipo') == 'cliente']
            
            # Selectbox para origen (normalmente almacenes)
            opciones_origen = {f"{v['id_vertice']} - {v.get('nombre', 'Sin nombre')}": v['id_vertice'] for v in almacenes}
            origen_display = st.selectbox(
                "🏪 Almacén Origen",
                options=list(opciones_origen.keys()),
                help="Seleccione el almacén de origen"
            )
            origen_id = opciones_origen[origen_display] if origen_display else None
            
            # Selectbox para destino (normalmente clientes)
            opciones_destino = {f"{v['id_vertice']} - {v.get('nombre', 'Sin nombre')}": v['id_vertice'] for v in clientes}
            destino_display = st.selectbox(
                "👤 Cliente Destino",
                options=list(opciones_destino.keys()),
                help="Seleccione el cliente destino"
            )
            destino_id = opciones_destino[destino_display] if destino_display else None
            
            # Configuración del algoritmo
            algoritmo = st.selectbox(
                "🧮 Algoritmo",
                ["BFS", "DFS", "Dijkstra"],
                index=0,
                help="Algoritmo para calcular la ruta"
            )
            
            autonomia = st.number_input(
                "⚡ Autonomía del Dron",
                min_value=10.0,
                max_value=100.0,
                value=50.0,
                step=5.0,
                help="Autonomía máxima en unidades de energía"
            )
            
            calcular = st.form_submit_button(
                "🧭 Calcular Ruta",
                type="primary",
                use_container_width=True
            )
            
            if calcular and origen_id and destino_id:
                calcular_y_mostrar_ruta(origen_id, destino_id, algoritmo, autonomia)
    
    except Exception as e:
        st.error(f"❌ Error en calculadora de rutas: {str(e)}")

def calcular_y_mostrar_ruta(origen_id: str, destino_id: str, algoritmo: str, autonomia: float):
    """Calcula y muestra la ruta entre dos puntos"""
    
    with st.spinner("🧭 Calculando ruta..."):
        try:
            from servicios.api import ClienteAPI
            
            cliente_api = ClienteAPI()
            
            # Datos para calcular ruta
            datos_ruta = {
                "origen_id": origen_id,
                "destino_id": destino_id,
                "algoritmo": algoritmo,
                "autonomia_maxima": autonomia
            }
            
            # Llamar API
            respuesta = cliente_api.calcular_ruta_directa(datos_ruta)
            
            if respuesta and respuesta.get('exito'):
                ruta = respuesta.get('ruta_calculada')
                
                # Mostrar resultado exitoso
                st.success("✅ ¡Ruta calculada exitosamente!")
                
                # Información de la ruta
                st.markdown("#### 🛣️ Información de la Ruta")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("💰 Costo Total", f"{ruta.get('costo_total', 0):.2f}")
                with col2:
                    requiere_recarga = "✅" if ruta.get('requiere_recarga') else "❌"
                    st.metric("⚡ Requiere Recarga", requiere_recarga)
                with col3:
                    st.metric("⏱️ Tiempo Estimado", ruta.get('tiempo_estimado', 'N/A'))
                
                # Mostrar secuencia de vértices
                secuencia = ruta.get('secuencia_vertices', [])
                if secuencia:
                    st.markdown("#### 📍 Secuencia de Vértices")
                    ruta_texto = " → ".join(secuencia)
                    st.code(ruta_texto, language=None)
                
                # Mostrar estaciones de recarga si las hay
                estaciones_recarga = ruta.get('estaciones_recarga', [])
                if estaciones_recarga:
                    st.markdown("#### ⚡ Estaciones de Recarga Utilizadas")
                    for estacion in estaciones_recarga:
                        st.info(f"🔋 {estacion}")
                
                # Opción para completar entrega
                if st.button("📦 Crear Pedido para esta Ruta", type="secondary"):
                    crear_pedido_desde_ruta(origen_id, destino_id, ruta)
            
            else:
                mensaje_error = respuesta.get('mensaje', 'No se pudo calcular la ruta') if respuesta else 'Error de conexión'
                st.error(f"❌ {mensaje_error}")
        
        except Exception as e:
            st.error(f"❌ Error al calcular ruta: {str(e)}")

def crear_pedido_desde_ruta(origen_id: str, destino_id: str, ruta: dict):
    """Permite crear un pedido basado en una ruta calculada"""
    
    st.markdown("#### 📦 Crear Pedido")
    
    with st.form("crear_pedido_ruta"):
        descripcion = st.text_input(
            "Descripción del Pedido",
            value="Pedido desde calculadora de rutas",
            help="Descripción del contenido a entregar"
        )
        
        peso = st.number_input(
            "Peso (kg)",
            min_value=0.1,
            max_value=10.0,
            value=1.0,
            step=0.1,
            help="Peso del paquete en kilogramos"
        )
        
        prioridad = st.selectbox(
            "Prioridad",
            ["BAJA", "MEDIA", "ALTA", "CRITICA"],
            index=1,
            help="Prioridad de entrega del pedido"
        )
        
        crear = st.form_submit_button("📦 Crear Pedido", type="primary")
        
        if crear:
            try:
                from servicios.api import ClienteAPI
                
                cliente_api = ClienteAPI()
                
                # Obtener cliente asociado al destino
                vertices = cliente_api.obtener_vertices()
                cliente_destino = next((v for v in vertices if v['id_vertice'] == destino_id), None)
                
                if not cliente_destino:
                    st.error("❌ No se encontró cliente destino")
                    return
                
                # Datos del pedido
                datos_pedido = {
                    "cliente_id": destino_id,
                    "almacenamiento_origen_id": origen_id,
                    "descripcion": descripcion,
                    "peso": peso,
                    "prioridad": prioridad
                }
                
                respuesta = cliente_api.crear_pedido(datos_pedido)
                
                if respuesta and respuesta.get('exito'):
                    st.success("✅ ¡Pedido creado exitosamente!")
                    pedido = respuesta.get('pedido')
                    st.info(f"📋 ID del Pedido: {pedido.get('id_pedido')}")
                else:
                    st.error("❌ Error al crear pedido")
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
```

## 4. Visualización de Grafos

### Componente de Visualización
```python
# frontend/visualizacion/grafo.py

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from typing import List, Dict, Any, Optional, Tuple

class VisualizadorGrafo:
    """Clase para visualizar grafos de la red de transporte"""
    
    def __init__(self):
        # Configuración de colores por tipo de vértice
        self.colores_vertices = {
            'cliente': '#3b82f6',      # Azul
            'almacenamiento': '#10b981', # Verde
            'recarga': '#f59e0b'       # Naranja
        }
        
        # Configuración de formas por tipo
        self.formas_vertices = {
            'cliente': 'o',      # Círculo
            'almacenamiento': 's', # Cuadrado
            'recarga': '^'       # Triángulo
        }
    
    def crear_grafico_red(self, vertices: List[Dict], aristas: List[Dict],
                         mostrar_etiquetas: bool = True,
                         mostrar_pesos: bool = False,
                         layout: str = 'spring',
                         tamaño_nodos: int = 300,
                         ancho_aristas: int = 2,
                         resaltar_ruta: Optional[List[str]] = None) -> plt.Figure:
        """
        Crea un gráfico completo de la red
        """
        
        # Crear grafo de NetworkX
        G = nx.Graph()
        
        # Agregar vértices con atributos
        for vertice in vertices:
            G.add_node(
                vertice['id_vertice'],
                tipo=vertice['tipo'],
                nombre=vertice.get('nombre', vertice['id_vertice'])
            )
        
        # Agregar aristas con pesos
        for arista in aristas:
            G.add_edge(
                arista['origen'],
                arista['destino'],
                peso=arista['peso']
            )
        
        # Configurar figura
        fig, ax = plt.subplots(figsize=(14, 10))
        fig.patch.set_facecolor('white')
        
        # Calcular layout
        if layout == 'spring':
            pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
        elif layout == 'circular':
            pos = nx.circular_layout(G)
        elif layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(G)
        elif layout == 'planar':
            if nx.is_planar(G):
                pos = nx.planar_layout(G)
            else:
                pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
        else:
            pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
        
        # Dibujar nodos por tipo
        for tipo_vertice in ['cliente', 'almacenamiento', 'recarga']:
            nodos_tipo = [n for n in G.nodes() if G.nodes[n]['tipo'] == tipo_vertice]
            
            if nodos_tipo:
                nx.draw_networkx_nodes(
                    G, pos,
                    nodelist=nodos_tipo,
                    node_color=self.colores_vertices[tipo_vertice],
                    node_shape=self.formas_vertices[tipo_vertice],
                    node_size=tamaño_nodos,
                    alpha=0.8,
                    ax=ax
                )
        
        # Dibujar aristas
        if resaltar_ruta:
            # Dibujar aristas normales
            aristas_normales = [(u, v) for u, v in G.edges() if not self._es_arista_en_ruta(u, v, resaltar_ruta)]
            nx.draw_networkx_edges(
                G, pos,
                edgelist=aristas_normales,
                width=ancho_aristas,
                alpha=0.3,
                edge_color='gray',
                ax=ax
            )
            
            # Dibujar aristas de la ruta resaltada
            aristas_ruta = [(u, v) for u, v in G.edges() if self._es_arista_en_ruta(u, v, resaltar_ruta)]
            nx.draw_networkx_edges(
                G, pos,
                edgelist=aristas_ruta,
                width=ancho_aristas * 2,
                alpha=1.0,
                edge_color='red',
                ax=ax
            )
        else:
            nx.draw_networkx_edges(
                G, pos,
                width=ancho_aristas,
                alpha=0.6,
                edge_color='gray',
                ax=ax
            )
        
        # Mostrar etiquetas de nodos
        if mostrar_etiquetas:
            etiquetas = {n: G.nodes[n]['nombre'] for n in G.nodes()}
            nx.draw_networkx_labels(
                G, pos,
                labels=etiquetas,
                font_size=8,
                font_weight='bold',
                ax=ax
            )
        
        # Mostrar pesos de aristas
        if mostrar_pesos:
            etiquetas_aristas = {(u, v): f"{G[u][v]['peso']:.1f}" for u, v in G.edges()}
            nx.draw_networkx_edge_labels(
                G, pos,
                edge_labels=etiquetas_aristas,
                font_size=6,
                ax=ax
            )
        
        # Configurar título y leyenda
        ax.set_title("Red de Transporte de Drones", fontsize=16, fontweight='bold', pad=20)
        
        # Crear leyenda
        self._crear_leyenda(ax)
        
        # Configurar ejes
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Ajustar márgenes
        plt.tight_layout()
        
        return fig
    
    def crear_grafico_ruta_especifica(self, vertices: List[Dict], aristas: List[Dict], 
                                    ruta: List[str]) -> plt.Figure:
        """
        Crea un gráfico enfocado en una ruta específica
        """
        return self.crear_grafico_red(
            vertices=vertices,
            aristas=aristas,
            mostrar_etiquetas=True,
            mostrar_pesos=True,
            resaltar_ruta=ruta,
            tamaño_nodos=500
        )
    
    def _es_arista_en_ruta(self, u: str, v: str, ruta: List[str]) -> bool:
        """Verifica si una arista está en la ruta especificada"""
        if not ruta or len(ruta) < 2:
            return False
        
        for i in range(len(ruta) - 1):
            if (ruta[i] == u and ruta[i + 1] == v) or (ruta[i] == v and ruta[i + 1] == u):
                return True
        return False
    
    def _crear_leyenda(self, ax):
        """Crea leyenda para el gráfico"""
        from matplotlib.patches import Patch
        
        elementos_leyenda = [
            Patch(facecolor=self.colores_vertices['cliente'], label='👥 Clientes'),
            Patch(facecolor=self.colores_vertices['almacenamiento'], label='🏪 Almacenes'),
            Patch(facecolor=self.colores_vertices['recarga'], label='⚡ Recarga')
        ]
        
        ax.legend(
            handles=elementos_leyenda,
            loc='upper right',
            bbox_to_anchor=(1, 1),
            frameon=True,
            fancybox=True,
            shadow=True
        )
```

## 5. Servicios de API

### Cliente API REST
```python
# frontend/servicios/api.py

import requests
import json
from typing import Dict, List, Optional, Any
import streamlit as st

class ClienteAPI:
    """Cliente para comunicación con la API del backend"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.timeout = 30
    
    def obtener_estado_simulacion(self) -> Optional[Dict[str, Any]]:
        """Obtiene el estado actual de la simulación"""
        try:
            response = requests.get(
                f"{self.base_url}/api/simulacion/estado",
                timeout=self.timeout
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            st.error(f"Error de conexión: {e}")
            return None
    
    def inicializar_simulacion(self, datos: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Inicializa una nueva simulación"""
        try:
            response = requests.post(
                f"{self.base_url}/api/simulacion/inicializar",
                json=datos,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            st.error(f"Error al inicializar simulación: {e}")
            return None
    
    def obtener_vertices(self) -> Optional[List[Dict[str, Any]]]:
        """Obtiene todos los vértices de la red"""
        try:
            response = requests.get(
                f"{self.base_url}/api/vertices",
                timeout=self.timeout
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('vertices', [])
            return None
        except Exception as e:
            st.error(f"Error al obtener vértices: {e}")
            return None
    
    def obtener_aristas(self) -> Optional[List[Dict[str, Any]]]:
        """Obtiene todas las aristas de la red"""
        try:
            response = requests.get(
                f"{self.base_url}/api/aristas",
                timeout=self.timeout
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('aristas', [])
            return None
        except Exception as e:
            st.error(f"Error al obtener aristas: {e}")
            return None
    
    def calcular_ruta_directa(self, datos: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Calcula ruta directa entre dos puntos"""
        try:
            response = requests.post(
                f"{self.base_url}/api/rutas/calcular-directa",
                json=datos,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            st.error(f"Error al calcular ruta: {e}")
            return None
    
    def obtener_pedidos(self, filtros: Dict[str, Any] = None) -> Optional[List[Dict[str, Any]]]:
        """Obtiene lista de pedidos con filtros opcionales"""
        try:
            params = filtros or {}
            response = requests.get(
                f"{self.base_url}/api/pedidos",
                params=params,
                timeout=self.timeout
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('pedidos', [])
            return None
        except Exception as e:
            st.error(f"Error al obtener pedidos: {e}")
            return None
    
    def crear_pedido(self, datos: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Crea un nuevo pedido"""
        try:
            response = requests.post(
                f"{self.base_url}/api/pedidos",
                json=datos,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            return response.json() if response.status_code == 201 else None
        except Exception as e:
            st.error(f"Error al crear pedido: {e}")
            return None
    
    def obtener_estadisticas_generales(self) -> Optional[Dict[str, Any]]:
        """Obtiene estadísticas generales del sistema"""
        try:
            response = requests.get(
                f"{self.base_url}/api/estadisticas/generales",
                timeout=self.timeout
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            st.error(f"Error al obtener estadísticas: {e}")
            return None
    
    def obtener_rutas_frecuentes(self, limite: int = 10) -> Optional[Dict[str, Any]]:
        """Obtiene las rutas más frecuentemente utilizadas"""
        try:
            response = requests.get(
                f"{self.base_url}/api/rutas/frecuentes",
                params={'limite': limite},
                timeout=self.timeout
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            st.error(f"Error al obtener rutas frecuentes: {e}")
            return None
```

El frontend proporciona una interfaz completa e intuitiva que permite a los usuarios interactuar eficientemente con todas las funcionalidades del sistema logístico de drones, desde la configuración de simulaciones hasta el análisis detallado de rutas y estadísticas.
