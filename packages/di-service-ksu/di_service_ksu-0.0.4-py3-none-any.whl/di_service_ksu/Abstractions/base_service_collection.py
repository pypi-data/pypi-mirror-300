#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from abc import ABC, abstractmethod
from typing import Type, TypeVar

from .base_di_container import BaseDIConteiner

TService = TypeVar('TService')

class BaseServiceCollection(ABC):
    @abstractmethod
    def RegisterSingleton(self, implementation:TService):
        pass

    @abstractmethod
    def RegisterSingleton(self, type_service:Type[TService], implementation:TService):
        pass

    @abstractmethod
    def RegisterTransient(self, implementation: TService):
        pass

    @abstractmethod
    def RegisterTransient(self, type_service:Type[TService], implementation:TService):
        pass

    @abstractmethod
    def GenerateContainer(self)->BaseDIConteiner:
        pass
