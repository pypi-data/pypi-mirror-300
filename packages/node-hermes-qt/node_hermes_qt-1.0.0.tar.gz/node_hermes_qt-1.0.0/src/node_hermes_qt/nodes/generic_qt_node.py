from abc import ABC, abstractmethod
from typing import Literal, Type

from pydantic import BaseModel
from qtpy import QtWidgets


class GenericNodeWidget(QtWidgets.QWidget):
    def __init__(self, component: "GenericQtNode"):
        super().__init__()
        self.node = component


class TabConfig(BaseModel):
    type: Literal["tab"]


class GenericQtNode(ABC):
    class Config(BaseModel):
        interface: TabConfig | None = None

    @property
    @abstractmethod
    def widget(self) -> Type[GenericNodeWidget]:
        raise NotImplementedError
