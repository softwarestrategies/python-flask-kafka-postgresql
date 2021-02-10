from kafka import KafkaConsumer
from messaging_setup import ChangeProjectStatusMessage
from json import loads
from time import sleep
from database_setup import Project
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import os

# Setup logging
logger = logging.getLogger('KafkaConsumerApp')
logger.setLevel(logging.INFO)

fileName = 'Python_Flask_Kafka_PostgreSQL.log'
if not os.path.exists(fileName):
    open(fileName, 'w').close()

handler = logging.FileHandler(fileName)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Create an Engine, which the Session will use for connection resources
# The create a configured "Session" class and then create a Session
db_engine = create_engine('postgresql://pfkp_admin:changeme@localhost:5432/pfkp')
Session = sessionmaker(bind=db_engine)

logger.info("Starting kafka_consumer_app.py ..............")

TOPIC_NAME = 'StartProcess'
CONSUMER_BOOTSTRAP_SERVERS = os.environ.get('CONSUMER_BOOTSTRAP_SERVERS', 'localhost:9092')
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers = [ CONSUMER_BOOTSTRAP_SERVERS ],
    auto_offset_reset = 'earliest',
    enable_auto_commit = True,
    group_id = 'my-group-id'
)

for message in consumer:
    if (message.value):
        try:
            messageBody = message.value.decode("utf-8")
            logger.info("Message taken from Queue: " + messageBody)

            changeProjectStatusMessage = ChangeProjectStatusMessage(**loads( messageBody ))

            dbSession = Session()
            try:
                dbSession.query(Project).filter_by(id=changeProjectStatusMessage.id).update({"status": 'DONE'})
                dbSession.commit()
            except:
                dbSession.rollback()
                raise
            finally:
                dbSession.close()
        except:
            logger.error("Error with Message: " + messageBody)

    sleep(2)
