from sqlalchemy import Column, Integer, String, Text, LargeBinary, JSON
from sqlalchemy.dialects.mysql import VARCHAR,BOOLEAN
from sqlalchemy.ext.declarative import declarative_base
from gai.agent.Base import Base
from gai.agent.fsm.pydantic.AgentFlowPydantic import AgentFlowPydantic

class AgentFlow(Base):
    __tablename__ = 'AgentFlow'

    Id = Column(String(36), primary_key=True)
    Name = Column(String(255), nullable=False)
    Description = Column(Text, nullable=True)
    StateDiagram = Column(Text, nullable=True)

    def to_pydantic(self):
        return AgentFlowPydantic.from_orm(self)
