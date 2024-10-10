from abc import abstractmethod
from typing import Protocol, runtime_checkable

from example_package_alitrix1.Abstractions.base_inject import BaseInject
from enum_type_message import EnumTypeMessage

@runtime_checkable
class BaseMessage(BaseInject, Protocol):

    @abstractmethod
    def set_msg(msg_type:EnumTypeMessage, msg:str):
        pass

    @abstractmethod
    def show_message(self, msg_type:EnumTypeMessage, message:str):
        pass
