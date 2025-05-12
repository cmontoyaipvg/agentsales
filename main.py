from dotenv import load_dotenv
load_dotenv()
from agno.playground import Playground, serve_playground_app
from agno.playground.settings import PlaygroundSettings
from agent.agent_ventas import Agente_Ventas

# Crear configuración personalizada con la nueva URL en CORS
settings = PlaygroundSettings()
settings.cors_origin_list.append("https://frontagente.onrender.com/")

# Pasar la configuración personalizada al constructor de Playground
app = Playground(
    agents=[Agente_Ventas],
    settings=settings
).get_app(use_async=True)

if __name__ == "__main__":
    serve_playground_app("main:app", host="0.0.0.0", reload=True)
