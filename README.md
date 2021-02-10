# python-flask-kafka-postgresql

## About

I wanted to learn a few new Python skills and also write an integrated system to show I can do it.

This is a work-in-process and I will improve it as I learn best practices.

## Initial Setup

There are a few containers/systems that don't change once setup:  **PostgreSQL and Kafka**

To start setting things up, from the root directory start the needed docker containers:

    $ docker-compose up -d
    
    NOTE:  And if it is started, when you are done .. you want to make sure it is stopped
    
        $ docker-compose stop

This should start 3 containers, with Zookeeper, Kafka and PostgreSQL. This can be confirmed with the following:

    $ docker ps

### Kafka

To test that Kafka is setup with the 2 topics we'll be using, do the following.

Log onto the Kafka container. Then from its Bash prompt list topics. And then exit the container.

    python-flask-kafka-postgresql $  docker exec -it pfkp-kafka bash

        bash# kafka-topics.sh --list --bootstrap-server localhost:9092
        
            StartProcess
            FinishProcess

        bash# exit

### PostgreSQL

For this you will need some PostgreSQL client installed so that you can access & setup the database. I have PostgreSQL
installed on my machine and thus can/will be using **psql** from the commandline.

From the commandline, run the following script .. which will setup a database and a user:

    python-flask-kafka-postgresql $  psql -h localhost -p 5432 -d postgres -U postgres --password -f ./sql-scripts/create-database-and-user.sql
 
    Password: When asked for a password, use "changeme" - which is specified in the file docker-compose.yml)

        CREATE DATABASE
        CREATE ROLE
        GRANT

Now From the commandline, run this script .. which creates a table to use & populate it with a few records

    python-flask-kafka-postgresql $  psql -h localhost -p 5432 -d pfkp -U pfkp_admin --password -f ./sql-scripts/create-schema-and-populate.sql
 
        NOTE: This command has the database & user created in the previous SQL script running
 
    Password: 
        
        CREATE TABLE

To check that all is right, log in and make sure all is in place:

    python-flask-kafka-postgresql $  psql -h localhost -p 5432 -d pfkp -U pfkp_admin --password

        projectx=> \dt
    
            which should show you a list of tables
        
        projectx=> select * from project;
    
            which should show no projects,  but not fail either
        
        projectx=> \q        
        
            exit psql

## Usual Process

### API

### Messages and Database
