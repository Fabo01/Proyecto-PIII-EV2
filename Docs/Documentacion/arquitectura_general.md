# Arquitectura General del Sistema

## Descripción General
El sistema de simulación logística de drones para Correos Chile está diseñado como una aplicación modular que implementa una arquitectura por capas (layered architecture). El sistema gestiona una red de drones autónomos que realizan entregas considerando limitaciones de energía, estaciones de recarga y optimización de rutas.

## Arquitectura por Capas

### 1. Capa de Presentación (Frontend)
- **Ubicación**: `frontend/` y `frontendv2/`
- **Responsabilidades**:
  - Interfaz visual con Streamlit
  - Dashboard interactivo con 5 pestañas funcionales
  - Visualización de grafos, rutas y estadísticas
  - Interacción del usuario con la simulación

#### Subcapas:
- **UI**: Componentes de interfaz organizados por funcionalidad
- **Servicios**: Cliente API para comunicación con el backend
- **Visualización**: Grafos, árboles AVL, gráficos estadísticos
- **Utils**: Validaciones y manejo de errores

### 2. Capa de API (Backend/API)
- **Ubicación**: `Backend/API/`
- **Responsabilidades**:
  - Endpoints REST para todas las funcionalidades
  - Mapeo entre DTOs y objetos de dominio
  - Manejo de peticiones HTTP
  - Validación de entrada

#### Componentes:
- **Enrutadores**: Organizados por entidad (clientes, pedidos, rutas, etc.)
- **DTOs**: Objetos de transferencia de datos
- **Mapeadores**: Conversión entre dominio y DTOs

### 3. Capa de Aplicación (Backend/Aplicacion)
- **Ubicación**: `Backend/Aplicacion/`
- **Responsabilidades**:
  - Orquestación de casos de uso
  - Coordinación entre servicios
  - Gestión de transacciones

### 4. Capa de Servicios (Backend/Servicios)
- **Ubicación**: `Backend/Servicios/`
- **Responsabilidades**:
  - Lógica de negocio especializada
  - Implementación de casos de uso
  - Gestión de la simulación
  - Auditoría y observadores

### 5. Capa de Dominio (Backend/Dominio)
- **Ubicación**: `Backend/Dominio/`
- **Responsabilidades**:
  - Entidades del negocio puras
  - Reglas de negocio fundamentales
  - Algoritmos de rutas
  - Interfaces de contratos

#### Subdominios:
- **Entidades**: Cliente, Pedido, Almacenamiento, Recarga, Ruta
- **Algoritmos**: Estrategias de cálculo de rutas (BFS, DFS)
- **Fábricas**: Creación de entidades complejas
- **Interfaces**: Contratos para repositorios y servicios

### 6. Capa de Infraestructura (Backend/Infraestructura)
- **Ubicación**: `Backend/Infraestructura/`
- **Responsabilidades**:
  - Implementación de repositorios
  - Estructuras de datos especializadas (TDA)
  - Persistencia en memoria
  - Gestión de datos

#### Componentes:
- **Repositorios**: Gestión de entidades en memoria
- **TDA**: Árbol AVL, HashMap, Grafo personalizado

## Principios Arquitectónicos

### 1. Separación de Responsabilidades
- Cada capa tiene una responsabilidad específica y bien definida
- No hay dependencias circulares entre capas
- La comunicación entre capas sigue un flujo unidireccional

### 2. Inversión de Dependencias
- Las capas superiores definen interfaces
- Las capas inferiores implementan estas interfaces
- El dominio es independiente de la infraestructura

### 3. Modularidad
- Cada módulo tiene una función específica
- Fácil mantenimiento y escalabilidad
- Código reutilizable y testeable

### 4. Unicidad de Entidades
- Uso de HashMap para acceso O(1) a entidades
- Relaciones reales entre objetos (no solo IDs)
- Repositorios gestionan instancias únicas

## Flujo de Datos Principal

```
Usuario (Frontend) 
    ↓ HTTP Request
API Endpoints 
    ↓ DTOs
Servicios de Aplicación 
    ↓ Objetos de Dominio
Servicios de Negocio 
    ↓ Entidades
Repositorios 
    ↓ TDA
Estructuras de Datos
```

## Patrones de Diseño Implementados

### 1. Repository Pattern
- Abstracción del acceso a datos
- Implementado en `Backend/Infraestructura/Repositorios/`

### 2. Factory Pattern
- Creación de entidades complejas
- Implementado en `Backend/Dominio/EntFabricas/`

### 3. Strategy Pattern
- Algoritmos de cálculo de rutas intercambiables
- Implementado en `Backend/Dominio/AlgEstrategias/`

### 4. Observer Pattern
- Notificación de eventos en la simulación
- Implementado en `Backend/Servicios/Observer/`

### 5. DTO Pattern
- Transferencia de datos entre capas
- Implementado en `Backend/API/DTOs/`

### 6. Mapper Pattern
- Conversión entre objetos de dominio y DTOs
- Implementado en `Backend/API/Mapeadores/`

## Consideraciones de Rendimiento

### 1. Estructuras de Datos Optimizadas
- **HashMap**: Acceso O(1) a entidades por ID
- **Árbol AVL**: Gestión balanceada de rutas frecuentes O(log n)
- **Grafo**: Representación eficiente de la red de transporte

### 2. Algoritmos Eficientes
- **BFS Modificado**: Exploración considerando autonomía energética
- **Algoritmos de grafos**: Conectividad garantizada
- **Caching**: Resultados de rutas frecuentes

### 3. Escalabilidad
- Soporte hasta 150 vértices, 300 aristas, 500 pedidos
- Arquitectura preparada para crecimiento
- Separación clara facilita optimizaciones futuras

## Tecnologías Utilizadas

### Backend
- **Python 3.12**: Lenguaje principal
- **FastAPI**: Framework para APIs REST
- **Uvicorn**: Servidor ASGI

### Frontend
- **Streamlit**: Framework de interfaz web
- **NetworkX**: Visualización de grafos
- **Matplotlib**: Gráficos y visualizaciones
- **Plotly**: Gráficos interactivos

### Estructuras de Datos
- **Implementaciones propias**: AVL, HashMap, Grafo
- **Optimizadas para el dominio**: Consideraciones específicas del negocio

## Configuración y Despliegue
- **Desarrollo**: Ejecutión local con servidores separados
- **Frontend**: `streamlit run frontend/main.py`
- **Backend**: `uvicorn Backend.API.main:app`
- **Configuración**: Variables de entorno y archivos de configuración

Esta arquitectura garantiza mantenibilidad, escalabilidad y separación clara de responsabilidades, facilitando el desarrollo y evolución del sistema.
