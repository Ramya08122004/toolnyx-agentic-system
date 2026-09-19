from fastapi import FastAPI
from pydantic import BaseModel
from .agent import Agent

app = FastAPI(title="Scalable Agentic Tool System", version="1.0.0")
agent = Agent()

class AgentRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"name": "Scalable Agentic Tool System", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tools")
def tools():
    return {"count": len(agent.registry.all()), "tools": [
        {"name": t.name, "domain": t.domain, "action": t.action, "description": t.description, "risk": t.risk}
        for t in agent.registry.all()
    ]}

@app.post("/agent")
def run_agent(request: AgentRequest):
    return agent.run(request.message)
