import sys
import pytest
from pytest import fail

import json
import logging
from datetime import datetime
from parser import Parser

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class TestFixtures:
    def __init__(self):
        self.id = 'foo'
        self.offset = 5
        f = open("./test_data/short_kml_file.json")

        raw_data = json.loads(f.read())
        self.data = raw_data["data"]



@pytest.fixture(scope = "module")
def getFixtures():
    return TestFixtures()

def testParseDataWithMissingId(getFixtures):

    try:
        parser = Parser()
        parsedData = parser.parseData(None,getFixtures.offset,getFixtures.data)
        fail("parser.parseData should have thrown an error on null id")
    except Exception as ex:
        assert(type(ex) is ValueError)

def testParseDataWithMissingOffSet(getFixtures):
    try:
        parser = Parser()
        parsedData = parser.parseData(getFixtures.id,None,getFixtures.data)
        fail("parser.parseData should have thrown an error on null offset")
    except Exception as ex:
        assert(type(ex) is ValueError)


def testParseDataWithNullData(getFixtures):
    try:
        parser = Parser()
        parsedData = parser.parseData(getFixtures.id,1,None)
        fail("parser.parseData should have thrown an error on null data")
    except Exception as ex:
        assert(type(ex) is ValueError)


def testParseDataWithNonJsonData(getFixtures):
    try:
        parser = Parser()
        data = "this is not JSON"
        parsedData = parser.parseData(getFixtures.id,1,data)
        fail("parser.parseData should have thrown an error on non JSON data")
    except Exception as ex:
        assert(type(ex) is ValueError)


def testParseDataWithInvalidJsonData(getFixtures):
    try:
        parser = Parser()
        data = {'foobar':'goo'}
        parsedData = parser.parseData(getFixtures.id,1,data)
        fail("parser.parseData should have thrown an error on incorrect JSON data")
    except Exception as ex:
        assert(type(ex) is KeyError)

def testParsedDataWithValidArgs(getFixtures):
    try:
        parser = Parser()
        parsedData = parser.parseData(getFixtures.id,getFixtures.offset,getFixtures.data)
        assert(parsedData != None)
        #logging.debug(parsedData)

        assert(len(parsedData) > 0)

        for  data in parsedData:
            assert data['id'] != None
            assert data['time'] != None
            assert data['heartRate'] != None
            assert data['coordinates'] != None

    except Exception as ex:
        logging.debug(str(ex))
        fail("should not have an exception when parsedData has valid input") # cause a failure


def testOffsetTimeGenerationWithInvalidArgs(getFixtures):
    parser = Parser()
    try:

        strTimeNow = "2016-10-09T15:48:54"
        dtOffset = parser.getOffsetTime(strTimeNow, getFixtures.offset)
        fail("should have thrown exception b/c invalid timestamp")
    except Exception as ex:
        assert(type(ex) is ValueError)

def testOffsetTimeGeneration(getFixtures):
    try:
        parser = Parser()

        strTimeNow = "2016-10-09T15:48:54Z"
        dtOffset = parser.getOffsetTime(strTimeNow, getFixtures.offset)
        assert(dtOffset.second == 59)

        strTimeNow = "2016-10-09T15:48:55Z"
        dtOffset = parser.getOffsetTime(strTimeNow, getFixtures.offset)
        assert(dtOffset.second == 0)
        assert(dtOffset.minute == 49)

        strTimeNow = "2016-10-09T15:48:56Z"
        dtOffset = parser.getOffsetTime(strTimeNow, getFixtures.offset)
        assert(dtOffset.second == 1)
        assert(dtOffset.minute == 49)

    except Exception as ex:
        logging.debug(str(ex))
        fail("should not have an exception when parsing valid time and offset") # cause a failure
