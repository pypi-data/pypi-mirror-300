import uuid
import os
import json
import time
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import update

from gai.agent.fsm.dalc.AgentFlow import AgentFlow
from gai.agent.fsm.pydantic.AgentFlowPydantic import AgentFlowPydantic

class AgentFlowRepository:

    def __init__(self, session: Session):
        self.session = session

    def create_agent_flow(self, name: str, description: str, state_diagram: str) -> str:
        agent_flow = AgentFlow(Id=str(uuid.uuid4()), Name=name, Description=description, StateDiagram=state_diagram)
        self.session.add(agent_flow)
        self.session.commit()
        return agent_flow.Id
    
    def get_agent_flow(self, agent_flow_id: str) -> AgentFlowPydantic:
        agent_flow = self.session.query(AgentFlow).get(agent_flow_id)
        return AgentFlowPydantic.from_orm(agent_flow)
    
    def get_agent_flow_by_name(self, name: str) -> AgentFlowPydantic:
        agent_flow = self.session.query(AgentFlow).filter(AgentFlow.Name == name).first()
        return AgentFlowPydantic.from_orm(agent_flow)
    
    def list_agent_flows(self) -> List[AgentFlowPydantic]:
        agent_flows = self.session.query(AgentFlow).all()
        return [AgentFlowPydantic.from_orm(agent_flow) for agent_flow in agent_flows]
    
    def update_agent_flow(self, agent_flow_id: str, name: str, description: str, state_diagram: str) -> None:
        self.session.query(AgentFlow).filter(AgentFlow.Id == agent_flow_id).update({"Name": name, "Description": description, "StateDiagram": state_diagram})
        self.session.commit()

    def delete_agent_flow(self, agent_flow_id: str) -> None:
        self.session.query(AgentFlow).filter(AgentFlow.Id == agent_flow_id).delete()
        self.session.commit()


