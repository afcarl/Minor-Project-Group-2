from csv_converter import CSVConverter
from functools import partial
import string
from lxml import etree

class HistoricalConverter(CSVConverter):
    def __init__(self, file):
        CSVConverter.__init__(self, file)

    def _process(self):
        situation_root = self._xpath(self._xml_tree, ".//d:measurementSiteRecord")

        for i in range(len(situation_root)):
            situation_xpath = partial(self._xpath, situation_root[i])
            index_list = []
            # General sensor information
            try:
                id = situation_root[i].attrib["id"]
            except IndexError:
                id = "INVALID ID"
            try:
                latitude_txt = situation_xpath("./d:measurementSiteLocation/d:locationForDisplay/d:latitude")[0].text
            except IndexError:
                try:
                    latitude_txt = situation_xpath("./d:measurementSiteLocation/d:locationContainedInItinerary/d:location/d:locationForDisplay/d:latitude")[0].text
                except IndexError:
                    latitude_txt = "INVALID LATITUDE"
            try:
                longitude_txt = situation_xpath("./d:measurementSiteLocation/d:locationForDisplay/d:longitude")[0].text
            except IndexError:
                try:
                    longitude_txt = situation_xpath(
                        "./d:measurementSiteLocation/d:locationContainedInItinerary/d:location/d:locationForDisplay/d:longitude")[
                        0].text
                except IndexError:
                    longitude_txt = "INVALID LONGITUDE"
            try:
                location = situation_xpath("./d:measurementSiteName/d:values/d:value")[0].text
            except IndexError:
                location = "INVALID LOCATION"
            try:
                lanes = situation_xpath(".//d:measurementSiteNumberOfLanes")[0].text
            except IndexError:
                lanes = "INVALID NUMBER OF LANES"

            # Information by index
            root_indices = situation_xpath("./d:measurementSpecificCharacteristics")
            all_indices = ""
            for ix in range(len(root_indices)):
                current_index = partial(self._xpath,root_indices[ix])
                try:
                    vehicle_type = current_index("./d:measurementSpecificCharacteristics/d:specificVehicleCharacteristics/d:vehicleType")[0].text
                    index = root_indices[ix].attrib["index"]
                    try:
                        lane = current_index("./d:measurementSpecificCharacteristics/d:specificLane")[0].text
                    except IndexError:
                        lane = "INVALID LANE"
                    try:
                        type_measurement = current_index("./d:measurementSpecificCharacteristics/d:specificMeasurementValueType")[0].text
                    except IndexError:
                        type_measurement = "INVALID MEASUREMENT TYPE"

                    all_indices += str(index) + "," + str(lane) + "," + str(type_measurement) + ";"
                except IndexError:
                    pass

            try:
                string_to_append = str(id) + "," + str(location) + "," + str(latitude_txt) + "," + str(longitude_txt) + "," + str(lanes)+ ";" + all_indices
                print string_to_append
                self._buffer_to_write.append(string_to_append)
            except UnicodeEncodeError:
                printable = set(string.printable)
                filtered_location = filter(lambda x: x in printable,location)
                string_to_append = str(id) + "," + str(filtered_location) + "," + str(latitude_txt) + "," + str(
                    longitude_txt) + "," + str(lanes) + ";"
                print string_to_append
                self._buffer_to_write.append(string_to_append)


HistoricalConverter('C:\Users\TUDelft SID\Documents\\2017-2018\\2nd quarter\Minorproject software design and application\GitHub\src\Historical\sensors.xml')
