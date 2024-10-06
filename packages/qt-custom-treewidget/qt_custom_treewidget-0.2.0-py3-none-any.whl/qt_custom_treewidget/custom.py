from enum import Enum
from typing import List

from qtpy import QtCore, QtGui, QtWidgets


class ColumnNames(Enum):
    pass


class Delegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, collumn_type: ColumnNames):
        super().__init__()
        self.collumn_type = collumn_type

    def displayText(self, value, locale):
        if not isinstance(value, TreeItem):
            return "NOT TREE ITEM"

        text = value.get_text(self.collumn_type)

        if isinstance(text, float):
            return f"{text:.2f}"

        return str(text)

    def createEditor(self, parent, option, index):
        widget = index.data(QtCore.Qt.ItemDataRole.DisplayRole)
        if not isinstance(widget, TreeItem):
            return None

        return widget.get_editor(self.collumn_type, parent)

    def setModelData(self, editor, model, index):
        widget = index.data(QtCore.Qt.ItemDataRole.DisplayRole)
        if isinstance(widget, TreeItem):
            widget.apply_widget(self.collumn_type, editor)

    def paint(self, painter: QtGui.QPainter, option: QtWidgets.QStyleOptionViewItem, index: QtCore.QModelIndex):
        item = index.data(QtCore.Qt.ItemDataRole.DisplayRole)

        if not isinstance(item, TreeItem):
            return None

        rect = option.rect  # type: ignore

        color = item.get_color()
        if color:
            painter.fillRect(rect, color)

        text_color = item.get_text_color()
        if text_color:
            font = painter.font()
            font.setBold(True)

        return super().paint(painter, option, index)


class TreeItem(QtWidgets.QTreeWidgetItem):
    def __init__(self):
        super().__init__()

        for i in range(15):
            self.setData(i, QtCore.Qt.ItemDataRole.DisplayRole, self)

    def get_text(self, column_type: ColumnNames) -> str:
        raise NotImplementedError()

    def get_editor(self, collumn_type: ColumnNames, parent: QtWidgets.QWidget) -> QtWidgets.QWidget | None:
        return None

    def apply_widget(self, collumn_type: ColumnNames, widget: QtWidgets.QWidget):
        return None

    def get_color(self) -> QtGui.QColor | None:
        return None

    def get_text_color(self) -> QtGui.QColor | None:
        return None

    def add(self, item: "TreeItem"):
        self.addChild(item)


class TreeviewViewer(QtWidgets.QTreeWidget):
    def __init__(self):
        super().__init__()

    def add(self, item: TreeItem):
        self.addTopLevelItem(item)

    def set_columns(self, column_type: List[ColumnNames]):
        self.setColumnCount(len(column_type))
        self.setHeaderLabels([column.value for column in column_type])

        self.delegates = []
        for i in range(len(column_type)):
            delegate = Delegate(column_type[i])
            self.delegates.append(delegate)
            self.setItemDelegateForColumn(i, delegate)

    def get_selected_items(self) -> List[TreeItem]:
        return [item for item in self.selectedItems() if isinstance(item, TreeItem)]

    def refresh_ui(self):
        self.viewport().update()
