from csv_converter import CSVConverter
from functools import partial

class HistoricalConverter(CSVConverter):
    def __init__(self, file):
        CSVConverter.__init__(self, file)

    def _process(self):
        situation_root = self._xpath(self._xml_tree, ".//d:measurementSiteRecord")

        for i in range(len(situation_root)):
            situation_xpath = partial(self._xpath, situation_root[i])
            index_list = []

            id = situation_root[i].attrib["id"]
            latitude_txt = situation_xpath(".//d:latitude")[0].text
            longitude_txt = situation_xpath(".//d:longitude")[0].text
            for index in situation_xpath(".//d:measurementSpecificCharacteristics"):
                index_data = [x.text for x in index]



            try:
                lanes = situation_xpath(".//d:measurementSiteNumberOfLanes")[0].text
            except IndexError:
                lanes = "INVALID NUMBER OF LANES"

            string_to_append = str(id) + "," + str(latitude_txt) + "," + str(longitude_txt) + "," + str(lanes)+ ";"

            self._buffer_to_write.append(string_to_append)
            # self._buffer_to_write.append(str(lanes)+";")

            # for index in indices_list:
            #     self._buffer_to_write.append(index.text)



HistoricalConverter('F:\\Minor project DATA\\sensors.xml')
