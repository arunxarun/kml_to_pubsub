import yaml
import os
from sender import Sender
from dataparser import DataParser
import logging
from google.cloud import pubsub

ENVVARS = "env_variables"

class Configurator:
    def __init__(self,config_file):
        loaded_yaml = yaml.load(open(config_file))
        self.config = {}
        # note that this project needs specific credentials in file specified by config_file to access google API endpoints.
        print loaded_yaml

        if loaded_yaml.has_key(ENVVARS) == False:
            raise(ValueError("expected "+ENVVARS+" key in loaded YAML file "+ config_file))

        sub_yaml = loaded_yaml[ENVVARS]

        if sub_yaml.has_key('GOOGLE_APPLICATION_CREDENTIALS') == False:
            raise ValueError("invalid configuration file, expecting value defined set in  GOOGLE_APPLICATION_CREDENTIALS key ")
        else:
            if os.path.isfile(config_file) == False:
                raise ValueError("expected valid service-key file at location "+config_file)

            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = sub_yaml['GOOGLE_APPLICATION_CREDENTIALS']
            self.config['GOOGLE_APPLICATION_CREDENTIALS'] = sub_yaml['GOOGLE_APPLICATION_CREDENTIALS']

        if sub_yaml.has_key('GOOGLE_PROJECT_ID') == False:
            raise ValueError("expected project ID value set in GOOGLE_PROJECT_ID key")
        else:
            self.config['GOOGLE_PROJECT_ID'] =  sub_yaml['GOOGLE_PROJECT_ID']

        if sub_yaml.has_key('PUBSUB_TOPIC') == False:
            raise ValueError("expected pubsub topic value set in PUBSUB_TOPIC key")
        else:
            self.config['PUBSUB_TOPIC'] = sub_yaml['PUBSUB_TOPIC']

        if sub_yaml.has_key('GOOGLE_CLOUD_DISABLE_GRPC') == False:
            self.config['GOOGLE_CLOUD_DISABLE_GRPC'] = True  # true by default
        else:
            self.config['GOOGLE_CLOUD_DISABLE_GRPC'] = sub_yaml['GOOGLE_CLOUD_DISABLE_GRPC']


    def getSender(self):

        ps = pubsub.Client(self.config['GOOGLE_PROJECT_ID'],None,None,self.config['GOOGLE_CLOUD_DISABLE_GRPC'])
        topic = ps.topic(self.config['PUBSUB_TOPIC'])

        return Sender(topic)


    def getDataParser(self):
        return DataParser()
