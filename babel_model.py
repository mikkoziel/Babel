from functools import reduce  # forward compatibility for Python 3
import operator


class ApplicationData:

    def getFromDict(self, data_dict, map_list):
        return reduce(operator.getitem, map_list, data_dict)

    def setInDict(self, data_dict, map_list, value):
        self.getFromDict(data_dict, map_list[:-1])[map_list[-1]] = value

