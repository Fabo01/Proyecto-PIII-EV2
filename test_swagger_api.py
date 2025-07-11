#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de la API con Swagger.
"""

import requests
import json
import time

# Configuración
API_BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Prueba los endpoints principales de la API"""
    
    print("🧪 Iniciando pruebas de la API...")
    
    try:
        # 1. Verificar estado de la API
        print("\n1. Verificando estado de la API...")
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            print("✅ API está activa")
            print(f"   Respuesta: {response.json()}")
        else:
            print(f"❌ Error en API: {response.status_code}")
            return
        
        # 2. Verificar salud del sistema
        print("\n2. Verificando salud del sistema...")
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Sistema saludable")
            health_data = response.json()
            print(f"   Estado: {health_data.get('status')}")
        
        # 3. Verificar algoritmos disponibles
        print("\n3. Obteniendo algoritmos disponibles...")
        response = requests.get(f"{API_BASE_URL}/algoritmos")
        if response.status_code == 200:
            algoritmos = response.json()
            print("✅ Algoritmos disponibles:")
            for alg, info in algoritmos.get('algoritmos', {}).items():
                print(f"   • {alg}: {info.get('nombre')}")
        
        # 4. Inicializar simulación
        print("\n4. Inicializando simulación...")
        simulacion_config = {
            "n_vertices": 15,
            "m_aristas": 20,
            "n_pedidos": 10
        }
        response = requests.post(f"{API_BASE_URL}/simulacion/iniciar", json=simulacion_config)
        if response.status_code == 200:
            print("✅ Simulación inicializada")
            sim_data = response.json()
            print(f"   Clientes: {len(sim_data.get('clientes', []))}")
            print(f"   Pedidos: {len(sim_data.get('pedidos', []))}")
        else:
            print(f"❌ Error al inicializar simulación: {response.status_code}")
            print(f"   Detalle: {response.text}")
        
        # 5. Listar pedidos
        print("\n5. Listando pedidos...")
        response = requests.get(f"{API_BASE_URL}/pedidos/")
        if response.status_code == 200:
            pedidos = response.json()
            print(f"✅ {len(pedidos)} pedidos encontrados")
            if pedidos:
                primer_pedido = pedidos[0]
                pedido_id = primer_pedido.get('id_pedido')
                print(f"   Primer pedido ID: {pedido_id}")
                
                # 6. Calcular ruta para el primer pedido
                print(f"\n6. Calculando ruta para pedido {pedido_id}...")
                response = requests.post(f"{API_BASE_URL}/rutas/calcular/{pedido_id}/dijkstra")
                if response.status_code == 200:
                    ruta = response.json()
                    print("✅ Ruta calculada exitosamente")
                    print(f"   Peso total: {ruta.get('peso_total')}")
                    print(f"   Algoritmo: {ruta.get('algoritmo')}")
                else:
                    print(f"❌ Error al calcular ruta: {response.status_code}")
                
                # 7. Actualizar estado del pedido
                print(f"\n7. Actualizando estado del pedido {pedido_id} a 'entregado'...")
                response = requests.patch(f"{API_BASE_URL}/pedidos/{pedido_id}/estado", json="entregado")
                if response.status_code == 200:
                    pedido_actualizado = response.json()
                    print("✅ Estado actualizado exitosamente")
                    print(f"   Nuevo estado: {pedido_actualizado.get('status')}")
                else:
                    print(f"❌ Error al actualizar estado: {response.status_code}")
                    print(f"   Detalle: {response.text}")
        
        # 8. Obtener estadísticas
        print("\n8. Obteniendo estadísticas...")
        response = requests.get(f"{API_BASE_URL}/estadisticas/")
        if response.status_code == 200:
            estadisticas = response.json()
            print("✅ Estadísticas obtenidas")
            print(f"   Total rutas: {estadisticas.get('total_rutas', 0)}")
            print(f"   Total pedidos: {estadisticas.get('total_pedidos', 0)}")
        
        print("\n🎉 ¡Todas las pruebas completadas exitosamente!")
        print("\n📚 Documentación Swagger disponible en:")
        print(f"   • Swagger UI: {API_BASE_URL}/docs")
        print(f"   • ReDoc: {API_BASE_URL}/redoc")
        print(f"   • OpenAPI JSON: {API_BASE_URL}/openapi.json")
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar a la API")
        print("   Asegúrate de que la API esté ejecutándose en http://localhost:8000")
        print("   Ejecuta: python -m uvicorn Backend.API.main:app --host 0.0.0.0 --port 8000 --reload")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

if __name__ == "__main__":
    test_api_endpoints()
