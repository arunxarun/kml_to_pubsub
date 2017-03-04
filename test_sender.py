import sys
import pytest
from pytest import fail
import json
import logging
from datetime import datetime
from sender import Sender
from parser import Parser
from google.cloud import pubsub
import mock
from mock import patch


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class MockTopic:
    def __init__(self):
        self.call_ct = 0

    def publish(self,message):
        self.call_ct += 1


class TestFixtures:
    def __init__(self):
        self.id = 'foo'
        self.offset = 5
        f = open("./test_data/short_kml_file.json")

        self.raw_data = f.read()
        self.parser = Parser()

        self.topic = MockTopic()




@pytest.fixture(scope = "module")
def getFixtures():
    return TestFixtures()


def testSendDataWithNullData(getFixtures):
    try:
        pubsub = "foo"
        sender = Sender(getFixtures.topic)
        sender.sendData(None,1)

    except Exception as ex:
        assert(type(ex) is ValueError)



def testSendDataWithInvalidBatchSize(getFixtures):

    try:
        raw_data = getFixtures.raw_data
        extracted_data = json.loads(raw_data)
        parsed_data = getFixtures.parser.parseData(getFixtures.id,getFixtures.offset,extracted_data['data'])

        sender = Sender(getFixtures.topic)
        sender.sendData(parsed_data,0)

    except Exception as ex:
        assert(type(ex) is ValueError)


def testSendDataWithValidParams(getFixtures):
    try:

        raw_data = getFixtures.raw_data
        extracted_data = json.loads(raw_data)
        parsed_data = getFixtures.parser.parseData(getFixtures.id,getFixtures.offset,extracted_data['data'])

        sender = Sender(getFixtures.topic)
        sender.sendData(parsed_data,1)

    except Exception as ex:
        fail(ex)
        fail("should not reach here after sending data with valid parameters")
