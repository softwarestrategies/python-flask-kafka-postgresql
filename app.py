from flask import Flask, request
from flask import jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Project

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pfkp_admin:changeme@localhost:5432/pfkp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# an Engine, which the Session will use for connection resources
some_engine = create_engine('postgresql://pfkp_admin:changeme@localhost:5432/pfkp')

# Create a configured "Session" class and then create a Session
Session = sessionmaker(bind=some_engine)
session = Session()

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

def getProjects():
    projects = session.query(Project).all()
    return jsonify(projects=[p.serialize for p in projects])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

