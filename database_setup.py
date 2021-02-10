# for creating the mapper code
from sqlalchemy import Column, Integer, String, Sequence

# for configuration and class code
# create declarative_base instance
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# ===== Entities ====================

PROJECT_ID_SEQ = Sequence('project_id_seq')

class Project(Base):
    __tablename__ = 'project'

    id = Column(Integer, PROJECT_ID_SEQ, primary_key=True, autoincrement=True, server_default=PROJECT_ID_SEQ.next_value())
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    status = Column(String(250))

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'id': self.id,
        }
