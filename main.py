from dotenv import load_dotenv
load_dotenv()
from agno.playground import Playground, serve_playground_app
from agent.agent_ventas import Agente_Ventas
from agent.agent_ventas_voice import Agente_Ventas_Voice
app = Playground(
     agents=[Agente_Ventas]).get_app(use_async=True)

if __name__ == "__main__":
    serve_playground_app("main:app",host="0.0.0.0", reload=True)
