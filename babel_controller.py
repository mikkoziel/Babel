import codecs
import collections.abc
import json
import os

from PyQt5.QtWidgets import QTreeWidgetItem, QFormLayout


class BabelController:
    def __init__(self):
        self.languages = None
        self.data = {}

    def read_data_from_file_chooser(self, filenames):
        print(filenames)
        data = {}
        for file in filenames:
            with codecs.open(file, 'r', 'utf-8') as f:
                read_data = f.read()
                filename = os.path.basename(file)
                lang = filename[0:filename.find(".")]
                # self.languages.append(os.path.basename(file))
                data[lang] = json.loads(read_data)
        return data

    def create_item_tree(self, data):
        items = []
        for key, values in data.items():
            items = self.update_item_tree(items, values)
            # item = QTreeWidgetItem([key])
            # for value in values:
            #     child = QTreeWidgetItem([value])
            #     item.addChild(child)
            # items.append(item)
        return items

    def update_item_tree(self, d, u):
        items = []
        for k, v in u.items():
            item = QTreeWidgetItem([k])
            if isinstance(v, collections.abc.Mapping):
                item.addChildren(self.update_item_tree(d, v))
            # else:
            #     child = QTreeWidgetItem([v])
            #     # x = d.get(k, [])
            #     # x.append(v)
            #     # d[k] = x
            #     item.addChild(child)
            items.append(item)
        return items

    def get_dict_path(self, item):
        p = item
        dict_path = [item.text(0)]
        while p.parent() is not None:
            p = p.parent()
            dict_path.append(p.text(0))
            # print(p.text(0))
        dict_path.reverse()
        print(dict_path)
        return dict_path

    def getTranslation(self, d, dict_path):
        tmp = d.get(dict_path.pop(0))

        if isinstance(tmp, collections.abc.Mapping):
            return self.getTranslation(tmp, dict_path)
        else:
            return tmp

    def save_files(self, data, form, active_tree_item):
        count = form.rowCount()
        for i in range(count):
            label = form.itemAt(i, QFormLayout.LabelRole).widget().text()
            value = form.itemAt(i, QFormLayout.FieldRole).widget().text()
            print(label + " " + value)

            dict_path = self.get_dict_path(active_tree_item)



    def merge_languages(self, data):
        for key_dict, value_dict in data.items():
            self.languages.append(key_dict)
            self.data = self.update_(self.data, value_dict)

            # for key, value in value_dict:
            #     self.dict_iter([key], value)
        print(self.data)

    def update_(self, d, u):
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = self.update_(d.get(k, {}), v)
            else:
                x = d.get(k, [])
                x.append(v)
                d[k] = x
        return d