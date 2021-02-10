from flask import Flask, request
from flask import jsonify
from json import dumps
from kafka import KafkaProducer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Project
from messaging_setup import ChangeProjectStatusMessage
import logging
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup logging
logger = logging.getLogger('App')
logger.setLevel(logging.INFO)

fileName = 'Python_Flask_Kafka_PostgreSQL.log'
if not os.path.exists(fileName):
    open(fileName, 'w').close()

handler = logging.FileHandler(fileName)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info("Starting app.py ..............")

PRODUCER_BOOTSTRAP_SERVERS = os.environ.get('PRODUCER_BOOTSTRAP_SERVERS', 'localhost:9092')
TOPIC_NAME = 'StartProcess'
producer = KafkaProducer(
    bootstrap_servers = [ PRODUCER_BOOTSTRAP_SERVERS ]
)

# Create an Engine, which the Session will use for connection resources
# The create a configured "Session" class and then create a Session
db_engine = create_engine('postgresql://pfkp_admin:changeme@localhost:5432/pfkp')
Session = sessionmaker(bind=db_engine)
dbSession = Session()

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

       dbSession.add(newProject)
       dbSession.commit()

       message = ChangeProjectStatusMessage(id = newProject.id)
       messageBody = dumps(message.__dict__)

       logger.info("Message Added to Queue: " + messageBody)

       producer.send(TOPIC_NAME, messageBody.encode('utf-8'))

       return jsonify(newProject.serialize)

def getProjects():
    projects = dbSession.query(Project).all()
    return jsonify(projects=[p.serialize for p in projects])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)

