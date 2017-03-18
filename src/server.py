import sys
from flask import Flask, request
from flask_restful import Resource, Api
import logging
from logging import Logger
from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort
import json
from datetime import datetime
from datetime import timedelta
from dataparser import DataParser
from sender import Sender
from configurator import Configurator

app = Flask(__name__)
api = Api(app)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# TODO: load standard google credentials from YAML
CONFIG_FILE = "./app.yml"

configurator = Configurator(CONFIG_FILE)
sender = configurator.getSender()
dataparser = configurator.getDataParser()


class Publish(Resource):

    publish_args = {
        'uuid': fields.String(required=True),
        'batch_size': fields.Integer(required=True),
        'offset' : fields.Integer(required = True)
    }



    @use_kwargs(publish_args)
    def post(self,uuid, batch_size, offset):


        logging.debug("uuid = %s"%uuid)
        logging.debug("batch_size = %d"%batch_size)
        logging.debug("offset= %d"%offset)

        raw_json = request.get_json()
        raw_data = raw_json["data"]
        logging.debug(raw_data)
        try:
            logging.debug("parsing data")
            parsedData = parser.parseData(uuid, offset, raw_data)
            logging.debug("sending data")
            sender.sendData(parsedData, batch_size)
            return uuid, 201
        except Exception as ex:
            logging.debug(str(ex))
            return str(ex), 500


api.add_resource(Publish, '/publish')

if __name__ == '__main__':
    app.run(debug=True)
