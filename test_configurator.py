import sys
import pytest
from pytest import fail

import json
import logging
from configurator import Configurator

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


TEST_DATA_DIR = "./test_data/"
MISSING_PID = TEST_DATA_DIR + "missingPID.yml"
MISSING_APPCREDS = TEST_DATA_DIR + "missingAppCreds.yml"
MISSING_DISABLEGRPC = TEST_DATA_DIR + "missingDisableGRPCFlag.yml"
MISSING_TOPIC = TEST_DATA_DIR + "missingTopic.yml"


# GOOGLE_PROJECT_ID: key-prism-91820
# PUBSUB_TOPIC: testpubsub
# # This token is used to verify that requests originate from your
# # application. It can be any sufficiently random string.
# GOOGLE_CLOUD_DISABLE_GRPC: True
# GOOGLE_APPLICATION_CREDENTIALS: ./key/service-key.json

def testWithMissingProjectId():
    try:
        conf = Configurator(MISSING_PID)
        fail("should not reach here, expecting exception at creation time")
    except Exception as ex:
        assert(type(ex) is ValueError)
        assert "GOOGLE_PROJECT_ID" in str(ex)


def testWithMissingTopic():
    try:
        conf = Configurator(MISSING_TOPIC)
        fail("should not reach here, expecting exception at creation time")
    except Exception as ex:
        assert(type(ex) is ValueError)
        assert "PUBSUB_TOPIC" in str(ex)

def testWithMissingApplicationCredentials():
    try:
        conf = Configurator(MISSING_APPCREDS)
        fail("should not reach here, expecting exception at creation time")
    except Exception as ex:
        assert(type(ex) is ValueError)
        assert "GOOGLE_APPLICATION_CREDENTIALS" in str(ex)

def testWithMissingDisableGRPC():
    try:
        conf = Configurator(MISSING_DISABLEGRPC)
        assert(conf.config['GOOGLE_CLOUD_DISABLE_GRPC'] == True)
    except Exception as ex:
        fail("should not thrown an exception")
