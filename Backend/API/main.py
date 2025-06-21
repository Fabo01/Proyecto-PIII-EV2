"""
API principal para la simulacion logistica de drones de Correos Chile.
Incluye todos los endpoints de gestion de entidades, rutas, simulacion y estadisticas.
"""

from Backend.API.DTOs.BaseArista import BaseArista
from Backend.API.DTOs.BaseVertice import BaseVertice
from Backend.API.DTOs.BaseRuta import BaseRuta
from Backend.API.DTOs.BasePedido import BasePedido
from Backend.API.DTOs.BaseSimulacionConfig import BaseSimulacionConfig
from Backend.Aplicacion.SimAplicacion.Aplicacion_Simulacion import SimulacionAplicacionService
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# --- Importar el router de simulacion ---
from Backend.API.simulacion_endpoints_enrutador import router as simulacion_router

# --- Importar todos los routers de los módulos API ---
from Backend.API.rutas_enrutador import router as rutas_router
from Backend.API.recargas_enrutador import router as recargas_router
from Backend.API.pedidos_enrutador import router as pedidos_router
from Backend.API.estadisticas_enrutador import router as estadisticas_router
from Backend.API.clientes_enrutador import router as clientes_router
from Backend.API.almacenamientos_enrutador import router as almacenamientos_router
from Backend.API.aristas_enrutador import router as aristas_router
from Backend.API.vertices_enrutador import router as vertices_router

app = FastAPI()

# Permitir CORS para desarrollo local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sim_service = SimulacionAplicacionService()

# --- Incluir el router modular de simulacion y todos los routers de la API ---
app.include_router(simulacion_router)
app.include_router(rutas_router)
app.include_router(recargas_router)
app.include_router(pedidos_router)
app.include_router(estadisticas_router)
app.include_router(clientes_router)
app.include_router(almacenamientos_router)
app.include_router(aristas_router)
app.include_router(vertices_router)


@app.get("/", tags=["Root"])
def root():
    """
    Endpoint raiz que devuelve un mensaje de bienvenida y estado basico de la API.
    """
    return {
        "mensaje": "API de Simulacion de Drones Correos Chile activa.",
        "endpoints": [
            "/simulacion", "/rutas", "/recargas", "/pedidos", "/estadisticas", "/clientes", "/almacenamientos", "/aristas", "/vertices"
        ]
    }
