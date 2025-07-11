#!/usr/bin/env python3
"""
Script para ejecutar la API de Simulación Logística de Drones con Swagger UI habilitado.

Uso:
    python run_api_swagger.py

La documentación estará disponible en:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc  
- OpenAPI JSON: http://localhost:8000/openapi.json
"""

import uvicorn
import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importaciones
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def main():
    """
    Ejecuta la API con configuración optimizada para Swagger.
    """
    print("🚀 Iniciando API de Simulación Logística de Drones")
    print("📚 Documentación disponible en:")
    print("   • Swagger UI: http://localhost:8000/docs")
    print("   • ReDoc: http://localhost:8000/redoc")
    print("   • OpenAPI JSON: http://localhost:8000/openapi.json")
    print("   • Estado de la API: http://localhost:8000/")
    print("   • Salud del sistema: http://localhost:8000/health")
    print("   • Algoritmos disponibles: http://localhost:8000/algoritmos")
    print("-" * 60)
    
    try:
        uvicorn.run(
            "Backend.API.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True,
            reload_dirs=[str(root_dir / "Backend")],
            reload_excludes=["*.log", "*.pyc", "__pycache__"],
        )
    except KeyboardInterrupt:
        print("\n✅ API detenida por el usuario")
    except Exception as e:
        print(f"❌ Error al ejecutar la API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
