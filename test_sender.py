import sys
import pytest
from pytest import fail
import json
import logging
from datetime import datetime
from sender import Sender
from parser import Parser
import mock
from mock import patch

from pytest_mock import mocker
from google.cloud import pubsub

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
        f = open("../test_data/short_kml_file.json")

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
        parsedData = getFixtures.parser.parseData(getFixtures.id,getFixtures.offset,getFixtures.raw_data)
        assert(parsedData != None)
        pubsub = "foo"
        sender = Sender(getFixtures.topic)
        sender.sendData(parsedData,0)

    except Exception as ex:
        assert(type(ex) is ValueError)


def testSendDataWithValidParams(getFixtures):
    try:

        parsedData = getFixtures.parser.parseData(getFixtures.id,getFixtures.offset,getFixtures.raw_data)
        assert(parsedData != None)


        sender = Sender(getFixtures.topic)
        sender.sendData(parsedData,1)

    except Exception as ex:
        fail(ex)
        fail("should not reach here after sending data with valid parameters")
