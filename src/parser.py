import logging
from logging import Logger
from datetime import datetime
from datetime import timedelta
import json


class Parser:
    def parseData(self,id, offset, data):
        if id == None:
            raise ValueError("expecting non null ID")

        if offset == None:
            raise ValueError("expecting non null offset")

        if data == None:
            raise ValueError("expecting non null data")
        else:
            if type(data) is not dict:
                raise(ValueError("expecting valid JSON dictionary"))
            if data.has_key("features") == False:
                raise KeyError("features data not found in submitteddata")

        logging.debug("loading all data")
        # look for 'features' array
        features = data["features"]
        logging.debug(str(features))
        events = []
        for feature in features:
            coordTimes = feature["properties"]["coordTimes"]
            heartRates = feature["properties"]["heartRates"]
            coordinates = feature["geometry"]["coordinates"]

            logging.debug("assembling events")
            for i in range(0, len(coordTimes)):
                logging.debug("in event loop")
                logging.debug("coordtime = %s",coordTimes[i])
                logging.debug("heartRate = %s",heartRates[i])
                logging.debug("coordinates = %s",coordinates[i])
                event = {}
                event["id"] = id

                event["time"] = self.getOffsetTime(coordTimes[i],offset).strftime("%Y-%m-%dT%H:%M:%SZ")
                event["heartRate"] = heartRates[i]
                event["coordinates"] = coordinates[i]
                events.append(event)


        return events

    def getOffsetTime(self,timeAsString, offsetSeconds):
        # example string: 2016-10-09T15:48:54Z
        dt = datetime.strptime(timeAsString,"%Y-%m-%dT%H:%M:%SZ")
        td = timedelta(seconds=offsetSeconds)
        dtOffset = dt+td
        return dtOffset
