from flask import Flask, render_template, request, redirect, url_for

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String, Sequence

# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# create declarative_base instance
Base = declarative_base()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pfkp_admin:changeme@localhost:5432/pfkp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# an Engine, which the Session will use for connection resources
some_engine = create_engine('postgresql://pfkp_admin:changeme@localhost:5432/pfkp')

# create a configured "Session" class
Session = sessionmaker(bind=some_engine)

# create a Session
session = Session()

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

@app.route('/projects', methods = ['GET', 'POST'])
def processProjectsEndpoint():
   if request.method == 'GET':
       return getProjects()
   elif request.method == 'POST':
       newProject = Project(
           name=request.form['name'],
           description=request.form['description'],
           status='NEW'
       )
       session.add(newProject)
       session.commit()
       return jsonify(newProject.serialize)


from flask import jsonify

def getProjects():
    projects = session.query(Project).all()
    return jsonify(projects=[p.serialize for p in projects])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

