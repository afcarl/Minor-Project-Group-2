from lxml import etree
from functools import partial
import io
import gzip
import os


class CSVConverter:
    def __init__(self, file=None):
        self.__buffer_to_write = []
        file_name = file
        file = io.BytesIO(open(file, 'rb').read())
        file = gzip.GzipFile(fileobj=file)

        try:
            self.__xml_tree = etree.parse(file)

            self.__process()
            self.__write_to_file(file_name)

        except Exception as e:
            print(e)

    def __write_to_file(self, file):
        if not os.path.exists(file[:-20] + 'txts'):
            os.mkdir(file[:-20] + 'txts')
        file = file[:-20] + 'txts\\' + file[-20:]
        file = file[:-3]
        file += '.txt'

        with open(file, 'w') as write_file:
            write_file.write('\n'.join(self.__buffer_to_write))

    def __process(self):
        """Process the data by extracting the data from the XML file and writing it to a buffer"""
        sites_root = self.__xpath(self.__xml_tree, "//d:siteMeasurements")

        for i in range(len(sites_root)):
            # create a partial function
            site_xpath = partial(self.__xpath, sites_root[i])

            # get measured values elements
            measured_values = self.__xpath(sites_root[i], ".//d:basicData")

            # get the elements containing the time and id
            time_reference = site_xpath("./d:measurementTimeDefault")[0]    # get measurement time default element
            site_reference = site_xpath("./d:measurementSiteReference")[0]  # get site reference element

            # append time and id to the buffer
            self.__buffer_to_write.append(time_reference.text + ";")
            self.__buffer_to_write[i] += site_reference.attrib["id"] + ";"

            for v in measured_values:
                # check if the measured value is average speed
                if v.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "TrafficSpeed":
                    speed = self.__xpath(v, ".//d:speed")[0]
                    self.__buffer_to_write[i] += "-2," + speed.text + ";"
                # check if the measured value is traffic flow
                elif v.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"] == "TrafficFlow":
                    flow = self.__xpath(v, ".//d:vehicleFlowRate")[0]
                    self.__buffer_to_write[i] += flow.text + ",-2;"

    @staticmethod
    def __xpath(root, path):
        # namespaces dictionary
        ns = {"soap": "http://schemas.xmlsoap.org/soap/envelope/",
              "d": "http://datex2.eu/schema/2/2_0"}

        return root.xpath(path, namespaces=ns)
