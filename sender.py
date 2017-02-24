import sys
import logging
from logging import Logger
import json


class Sender:
    def __init__(self,topic):
        self.topic = topic



    def sendData(self, data, batch_size):
        if data == None:
            raise ValueError("Expecting non null data")

        if len(data) == 0:
            raise ValueError("Expecting an array of data with at least 1 element")

        if batch_size <= 0:
            raise ValueError("Expecting batch size > 0")


        logging.debug("sending array of "+str(len(data))+" data elements")

        # this is where we send things to google pubsub by batch_size

        buffer = []
        for i in range(0, len(data)):

            buffer.append(data[i])
            if len(buffer) == batch_size:
                logging.debug("publishing "+ str(buffer))
                self.topic.publish(buffer)
                del buffer[:]

        # handle the leftovers if there are any.

        leftovers = len(data) % batch_size;

        if(leftovers > 0):
            self.topic.publish(buffer)
