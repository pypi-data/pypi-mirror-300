from abc import abstractmethod
from typing import Protocol, runtime_checkable
from uuid import UUID

from example_package_alitrix1.Abstractions.base_inject import BaseInject

@runtime_checkable
class BaseRandomGUID(BaseInject, Protocol):
    @abstractmethod
    def get_id(self)->UUID:
        ...

    @abstractmethod
    def get_next(self)->UUID:
        ...