# Diagramas UML del Sistema de Simulación Logística

Este documento contiene todos los diagramas UML que describen la arquitectura y comportamiento del sistema de simulación logística de drones para Correos Chile.

## 1. Diagrama de Arquitectura General

```mermaid
graph TB
    subgraph "Frontend"
        UI[Frontend Streamlit]
        Cache[Sistema de Cache]
        Vis[Visualizaciones]
    end
    
    subgraph "Backend API"
        Router[Enrutadores FastAPI]
        DTOs[DTOs de Respuesta]
        Map[Mapeadores]
    end
    
    subgraph "Capa de Aplicación"
        AppServ[Servicios de Aplicación]
        DomServ[Servicios de Dominio]
    end
    
    subgraph "Capa de Dominio"
        Sim[Simulación]
        Ent[Entidades]
        Fab[Fábricas]
        Estr[Estrategias de Ruta]
        Obs[Observadores]
    end
    
    subgraph "Capa de Infraestructura"
        Repo[Repositorios]
        TDA[Estructuras TDA]
        Hash[HashMap]
        AVL[Árbol AVL]
        Grafo[Grafo]
    end
    
    UI --> Router
    Router --> AppServ
    AppServ --> DomServ
    DomServ --> Sim
    Sim --> Ent
    Sim --> Fab
    Sim --> Estr
    Sim --> Repo
    Repo --> TDA
    Router --> DTOs
    DTOs --> Map
    Map --> Ent
```

## 2. Diagrama de Clases - Entidades de Dominio

```mermaid
classDiagram
    class Cliente {
        +int id_cliente
        +string nombre
        +string tipo_elemento = "cliente"
        -List~Pedido~ _pedidos
        +agregar_pedido(pedido)
        +eliminar_pedido(pedido)
        +obtener_pedidos()
        +total_pedidos()
        +limpiar_pedidos()
    }
    
    class Almacenamiento {
        +int id_almacenamiento
        +string nombre
        +string tipo_elemento = "almacenamiento"
        -List~Pedido~ _pedidos
        +agregar_pedido(pedido)
        +obtener_pedidos()
        +total_pedidos()
        +limpiar_pedidos()
    }
    
    class Recarga {
        +int id_recarga
        +string nombre
        +string tipo_elemento = "recarga"
        +__str__()
    }
    
    class Pedido {
        +int id_pedido
        +Vertice cliente_v
        +Vertice origen_v
        +Vertice destino_v
        +int prioridad
        +string status
        +Ruta ruta
        +datetime fecha_creacion
        +asignar_ruta(camino, peso_total)
        +actualizar_status(nuevo_status)
    }
    
    class Ruta {
        +Vertice origen
        +Vertice destino
        +List~Arista~ camino
        +float peso_total
        +string algoritmo
        +float tiempo_calculo
        +es_valida()
        +__str__()
    }
    
    Cliente ||--o{ Pedido : "tiene"
    Almacenamiento ||--o{ Pedido : "origina"
    Pedido ||--o| Ruta : "asignada"
```

## 3. Diagrama de Clases - TDA (Estructuras de Datos)

```mermaid
classDiagram
    class Vertice {
        -Element _elemento
        +elemento()
        +__hash__()
        +__str__()
        +__repr__()
    }
    
    class Arista {
        -Vertice _origen
        -Vertice _destino
        -float _peso
        +origen()
        +destino()
        +peso()
        +opuesto(vertice)
        +__str__()
    }
    
    class Grafo {
        -HashMap _vertices
        -HashMap _aristas
        +insertar_vertice(elemento)
        +insertar_arista(origen, destino, peso)
        +vertices()
        +aristas()
        +aristas_incidentes(vertice, salientes)
        +eliminar_vertice(vertice)
        +eliminar_arista(arista)
    }
    
    class HashMap {
        -List _buckets
        -int _size
        -int _capacity
        +insertar(clave, valor)
        +obtener(clave)
        +eliminar(clave)
        +existe(clave)
        +claves()
        +valores()
        +items()
    }
    
    class AVL {
        -NodoAVL _raiz
        +insertar(clave, valor)
        +buscar(clave)
        +eliminar(clave)
        +obtener_mas_frecuentes(top)
        +recorrido_inorden()
    }
    
    Grafo --> Vertice : "contiene"
    Grafo --> Arista : "contiene"
    Vertice --> Cliente : "encapsula"
    Vertice --> Almacenamiento : "encapsula"
    Vertice --> Recarga : "encapsula"
    Arista --> Vertice : "conecta"
```

## 4. Diagrama de Secuencia - Inicialización de Simulación

```mermaid
sequenceDiagram
    participant UI as Frontend
    participant API as API Router
    participant AppServ as App Service
    participant DomServ as Domain Service
    participant Sim as Simulación
    participant Fab as Fábricas
    participant Repo as Repositorios
    
    UI->>API: POST /simulacion/iniciar
    API->>AppServ: iniciar_simulacion(n_vertices, m_aristas, n_pedidos)
    AppServ->>DomServ: iniciar_simulacion()
    DomServ->>Sim: iniciar_simulacion()
    
    Sim->>Fab: limpiar() - todas las fábricas
    Sim->>Repo: limpiar() - todos los repositorios
    
    Sim->>Fab: crear_clientes(n_clientes)
    Fab->>Repo: agregar(cliente)
    
    Sim->>Fab: crear_almacenamientos(n_almacenamientos)
    Fab->>Repo: agregar(almacenamiento)
    
    Sim->>Fab: crear_recargas(n_recargas)
    Fab->>Repo: agregar(recarga)
    
    Sim->>Fab: crear_vertices() y crear_aristas()
    Fab->>Repo: agregar(vertice/arista)
    
    Sim->>Fab: crear_pedidos(n_pedidos)
    Fab->>Repo: agregar(pedido)
    
    Sim-->>DomServ: estado_simulacion
    DomServ-->>AppServ: estado_simulacion
    AppServ-->>API: response_data
    API-->>UI: JSON response
```

## 5. Diagrama de Secuencia - Cálculo de Ruta

```mermaid
sequenceDiagram
    participant UI as Frontend
    participant API as API Router
    participant Serv as Service
    participant Fab as Fabrica Rutas
    participant Estr as Estrategia
    participant Grafo as Grafo
    participant Map as Mapeador
    
    UI->>API: POST /rutas/calcular/{id_pedido}/{algoritmo}
    API->>Serv: calcular_ruta(id_pedido, algoritmo)
    Serv->>Serv: obtener_pedido(id_pedido)
    Serv->>Fab: calcular_ruta(pedido, grafo, algoritmo)
    
    Fab->>Fab: seleccionar_estrategia(algoritmo)
    Fab->>Estr: calcular_ruta(origen, destino, grafo, autonomia)
    
    Estr->>Grafo: aristas_incidentes(vertice)
    Grafo-->>Estr: lista_aristas
    
    Estr->>Estr: algoritmo_busqueda()
    Estr-->>Fab: camino, peso_total
    
    Fab->>Fab: crear_ruta(camino, peso_total, algoritmo)
    Fab-->>Serv: ruta
    
    Serv->>Map: a_dto(ruta)
    Map-->>Serv: ruta_dto
    Serv-->>API: ruta_dto
    API-->>UI: JSON response
```

## 6. Diagrama de Estados - Pedido

```mermaid
stateDiagram-v2
    [*] --> Pendiente
    Pendiente --> En_Ruta : asignar_ruta()
    En_Ruta --> Entregado : entregar_pedido()
    En_Ruta --> Pendiente : error_entrega()
    Entregado --> [*]
    
    Pendiente : status = "pendiente"
    En_Ruta : status = "en_ruta"
    Entregado : status = "entregado"
```

## 7. Diagrama de Componentes - Estrategias de Ruta

```mermaid
graph TB
    subgraph "Estrategias de Ruta"
        IRuta[IRutaEstrategia]
        BFS[RutaEstrategiaBFS]
        DFS[RutaEstrategiaDFS]
        Dijkstra[RutaEstrategiaDijkstra]
        Floyd[RutaEstrategiaFloydWarshall]
        Topo[RutaEstrategiaTopological]
        Kruskal[RutaEstrategiaKruskal]
    end
    
    subgraph "Contexto"
        Fabrica[FabricaRutas]
        Sim[Simulación]
    end
    
    IRuta <|-- BFS
    IRuta <|-- DFS
    IRuta <|-- Dijkstra
    IRuta <|-- Floyd
    IRuta <|-- Topo
    IRuta <|-- Kruskal
    
    Fabrica --> IRuta : "usa"
    Sim --> Fabrica : "delega"
```

## 8. Diagrama de Despliegue

```mermaid
graph TB
    subgraph "Cliente (Navegador)"
        Browser[Streamlit Frontend]
    end
    
    subgraph "Servidor de Aplicación"
        FastAPI[FastAPI Backend]
        Python[Python Runtime]
    end
    
    subgraph "Almacenamiento"
        Memory[Memoria RAM]
        HashMap[HashMap Structures]
        AVL[AVL Trees]
        Logs[Archivos de Log]
    end
    
    Browser -.->|HTTP/JSON| FastAPI
    FastAPI --> Python
    Python --> Memory
    Memory --> HashMap
    Memory --> AVL
    Python --> Logs
```

## 9. Diagrama de Flujo - Algoritmo BFS con Recarga

```mermaid
flowchart TD
    Start([Inicio BFS]) --> Init[Inicializar cola con origen]
    Init --> CheckQueue{¿Cola vacía?}
    CheckQueue -->|Sí| NotFound[No hay ruta]
    CheckQueue -->|No| Dequeue[Sacar vértice actual]
    
    Dequeue --> CheckDestination{¿Es destino?}
    CheckDestination -->|Sí| Found[Ruta encontrada]
    CheckDestination -->|No| GetEdges[Obtener aristas salientes]
    
    GetEdges --> ForEach[Para cada arista]
    ForEach --> CheckWeight{¿Peso <= autonomía?}
    CheckWeight -->|No| NextEdge[Siguiente arista]
    CheckWeight -->|Sí| CheckEnergy{¿Energía suficiente?}
    
    CheckEnergy -->|No| NextEdge
    CheckEnergy -->|Sí| CheckRecharge{¿Es recarga?}
    CheckRecharge -->|Sí| Recharge[Restaurar energía]
    CheckRecharge -->|No| Continue[Continuar]
    
    Recharge --> Enqueue[Encolar nuevo estado]
    Continue --> Enqueue
    Enqueue --> NextEdge
    NextEdge --> CheckQueue
    
    Found --> End([Fin])
    NotFound --> End
```

## 10. Diagrama de Observadores

```mermaid
classDiagram
    class ISujeto {
        <<interface>>
        +agregar_observador(observador)
        +quitar_observador(observador)
        +notificar_observadores(evento, datos)
    }
    
    class IObservador {
        <<interface>>
        +actualizar(evento, datos)
    }
    
    class Simulacion {
        -List~IObservador~ _observadores
        +agregar_observador(observador)
        +notificar_observadores(evento, datos)
    }
    
    class AuditoriaObservador {
        +actualizar(evento, datos)
        +registrar_evento(evento, datos)
    }
    
    class EstadisticasObservador {
        +actualizar(evento, datos)
        +actualizar_metricas(datos)
    }
    
    ISujeto <|-- Simulacion
    IObservador <|-- AuditoriaObservador
    IObservador <|-- EstadisticasObservador
    Simulacion --> IObservador : "notifica"
```

## Convenciones de Diagramas

- **Líneas sólidas**: Relaciones fuertes/composición
- **Líneas punteadas**: Dependencias débiles/uso
- **Rombos sólidos**: Composición
- **Rombos vacíos**: Agregación
- **Triángulos**: Herencia/implementación

## Notas de Implementación

1. **Unicidad**: Todas las entidades se manejan mediante HashMap para garantizar O(1) y unicidad
2. **Estrategias**: Patrón Strategy para algoritmos de ruta intercambiables
3. **Observadores**: Patrón Observer para auditoría y eventos transversales
4. **TDA**: Estructuras de datos personalizadas optimizadas para el dominio
5. **Clean Architecture**: Separación clara entre capas con flujo de dependencias hacia el dominio
