from dotenv import load_dotenv
load_dotenv()
from agno.playground import Playground, serve_playground_app
from agno.playground.settings import PlaygroundSettings
from agent.agent_ventas import Agente_Ventas
from fastapi.middleware.cors import CORSMiddleware
# Crear configuración personalizada con la nueva URL en CORS
playground = Playground(agents=[Agente_Ventas])
app = playground.get_app(use_async=True)

# Añadir o reemplazar el middleware CORS después de crear la aplicación
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://agno.com",
        "https://www.agno.com",
        "https://app.agno.com",
        "https://app-stg.agno.com",
        "https://frontagente.onrender.com"  # Tu URL adicional
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
if __name__ == "__main__":
    serve_playground_app("main:app", host="0.0.0.0", reload=True)
