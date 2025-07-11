# 🚁 Sistema de Simulación Logística de Drones - Configuración Completa

## 📋 Guía de Inicio Rápido

### 1. Instalación de Dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la API con Swagger
```bash
# Opción 1: Script personalizado
python run_api_swagger.py

# Opción 2: Directamente con uvicorn
python -m uvicorn Backend.API.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Verificar la API
```bash
# Probar endpoints automáticamente
python test_swagger_api.py
```

### 4. Ejecutar Frontend Streamlit
```bash
streamlit run frontendv2/main.py
```

## 🔗 URLs Importantes

### Documentación API
- **Swagger UI Interactive**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **OpenAPI JSON Schema**: http://localhost:8000/openapi.json

### Aplicación Frontend
- **Streamlit Dashboard**: http://localhost:8501

### Endpoints de Estado
- **API Status**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health
- **Algoritmos**: http://localhost:8000/algoritmos
- **Swagger Config**: http://localhost:8000/swagger-config

## 🎯 Funcionalidades Implementadas

### ✅ Marcar Pedidos como Completados
- **Frontend**: Botón "✅ Marcar Entregado" en pestaña "Clientes y Pedidos"
- **API**: `PATCH /pedidos/{id}/estado` con body `"entregado"`
- **API Alt**: `POST /rutas/entregar/{id_pedido}`
- **Persistencia**: Estado se guarda y pedido no permite más rutas

### ✅ Algoritmos de Ruteo
- **BFS**: Búsqueda en amplitud
- **DFS**: Búsqueda en profundidad
- **Dijkstra**: Camino más corto ponderado
- **Floyd-Warshall**: Todos los caminos más cortos
- **Topological Sort**: Para grafos dirigidos acíclicos

### ✅ Gestión Completa de Simulación
- **Inicialización**: Parámetros configurables (vertices, aristas, pedidos)
- **Visualización**: Grafo interactivo con NetworkX/Matplotlib
- **Estadísticas**: Métricas en tiempo real
- **Persistencia**: Estados mantenidos durante la sesión

## 📱 Flujo de Uso Completo

### Desde Swagger UI (http://localhost:8000/docs)

1. **Inicializar Simulación**
   ```json
   POST /simulacion/iniciar
   {
     "n_vertices": 15,
     "m_aristas": 20,
     "n_pedidos": 10
   }
   ```

2. **Explorar Entidades**
   ```
   GET /vertices/     # Ver todos los vértices
   GET /pedidos/      # Ver todos los pedidos
   GET /clientes/     # Ver clientes específicamente
   ```

3. **Calcular Rutas**
   ```
   POST /rutas/calcular/1/dijkstra   # Ruta individual
   POST /rutas/calcular/1/todos      # Todos los algoritmos
   ```

4. **Marcar Entregas**
   ```
   PATCH /pedidos/1/estado
   Body: "entregado"
   ```

5. **Analizar Resultados**
   ```
   GET /estadisticas/               # Métricas generales
   GET /estadisticas/rutas_frecuentes
   ```

### Desde Frontend Streamlit (http://localhost:8501)

1. **Pestaña "Ejecutar Simulación"**
   - Configurar parámetros con sliders
   - Botón "Start Simulation"

2. **Pestaña "Explorar Red"**
   - Visualizar grafo generado
   - Seleccionar origen/destino
   - Calcular rutas interactivamente

3. **Pestaña "Clientes y Pedidos"**
   - Ver tabla de pedidos con estados
   - Botón "✅ Marcar Entregado" para cada pedido
   - Acciones de cálculo de rutas

4. **Pestaña "Análisis de Rutas"**
   - Estadísticas de rutas más frecuentes
   - Visualización del árbol AVL
   - Métricas de rendimiento

5. **Pestaña "Estadísticas"**
   - Gráficos de distribución
   - Métricas de sistema
   - Análisis de vertices más visitados

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
export API_HOST=0.0.0.0
export API_PORT=8000
export STREAMLIT_PORT=8501
export LOG_LEVEL=INFO
```

### Configuración de CORS
La API permite requests desde cualquier origen para desarrollo local.

### Logging
Los logs se muestran en consola con formato timestamp y nivel.

## 🧪 Testing

### Pruebas Automáticas
```bash
python test_swagger_api.py
```

### Pruebas Manuales en Swagger
1. Ir a http://localhost:8000/docs
2. Expandir cada endpoint
3. Usar "Try it out" para probar
4. Ver respuestas y esquemas

### Casos de Prueba Recomendados

1. **Simulación Básica**
   - 15 vertices, 20 aristas, 10 pedidos
   - Verificar que se crean todas las entidades

2. **Cálculo de Rutas**
   - Probar cada algoritmo disponible
   - Verificar que respetan autonomía de 50 unidades

3. **Gestión de Estados**
   - Crear pedido → calcular ruta → marcar entregado
   - Verificar que no se pueden calcular más rutas

4. **Análisis de Datos**
   - Generar múltiples rutas
   - Verificar estadísticas y frecuencias

## 📊 Métricas y Monitoreo

### Endpoints de Salud
- `GET /health` - Estado de componentes
- `GET /` - Info básica de la API

### Logs Importantes
- Creación de entidades de dominio
- Cálculo de rutas por algoritmo
- Cambios de estado de pedidos
- Errores de validación

### Rendimiento
- Tiempo de cálculo por algoritmo
- Memoria utilizada por estructuras TDA
- Throughput de requests por segundo

## 🚀 Próximos Pasos

### Mejoras Pendientes
- [ ] Autenticación JWT
- [ ] Rate limiting
- [ ] Persistencia en base de datos
- [ ] WebSockets para actualizaciones en tiempo real
- [ ] Export PDF de reportes
- [ ] Mapa geográfico real
- [ ] Métricas de Prometheus

### Extensiones
- [ ] API versioning (v2, v3)
- [ ] GraphQL endpoint
- [ ] Webhooks para eventos
- [ ] Batch operations
- [ ] Async background tasks

---

**¡Disfruta explorando la documentación Swagger en http://localhost:8000/docs!** 🎉
