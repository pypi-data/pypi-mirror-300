from .custom import ColumnNames, TreeviewViewer, TreeItem
from qtpy import QtWidgets
import time


class CustomCollumnNames(ColumnNames):
    NAME = "Name"
    TEST = "Test"


class MyCustomObject:
    def __init__(self, name: str):
        self.name = name

    @property
    def time(self):
        return time.time()


class CustomGroup(TreeItem):
    def __init__(self):
        super().__init__()

    def get_text(self, collumn_type: ColumnNames):
        return "Group"


class CustomItem(TreeItem):
    def __init__(self, object: MyCustomObject):
        super().__init__()
        self.object = object

    def get_text(self, collumn_type: ColumnNames):
        if collumn_type == CustomCollumnNames.NAME:
            return self.object.name + "we"
        elif collumn_type == CustomCollumnNames.TEST:
            return str(self.object.time)
        else:
            raise NotImplementedError()


def main():
    app = QtWidgets.QApplication([])
    window = TreeviewViewer()
    for g in range(3):
        group = CustomGroup()
        window.add(group)
        for i in range(3):
            item = CustomItem(MyCustomObject(f"Object {i}"))
            group.add(item)

    window.set_columns([CustomCollumnNames.NAME, CustomCollumnNames.TEST])
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
