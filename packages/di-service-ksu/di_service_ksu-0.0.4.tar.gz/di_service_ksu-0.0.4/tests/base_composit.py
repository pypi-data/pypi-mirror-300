from abc import abstractmethod
from typing import Protocol, runtime_checkable

from example_package_alitrix1.Abstractions.base_inject import BaseInject
from base_message import BaseMessage

@runtime_checkable
class BaseComposit(BaseInject, Protocol):   
    @abstractmethod
    def run_once(self)->BaseMessage:
        pass