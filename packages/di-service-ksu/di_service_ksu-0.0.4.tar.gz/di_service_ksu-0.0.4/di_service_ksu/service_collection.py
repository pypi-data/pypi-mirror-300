#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from typing import Type
from .Abstractions.base_di_container import BaseDIConteiner
from .Abstractions.base_service_collection import BaseServiceCollection
from .Abstractions.service_descriptor import ServiceDescriptor
from .Enums.service_life import ServiceLifetime
from .dependency_container import DependencyContainer, TService

class ServiceCollection(BaseServiceCollection):
    def __init__(self) -> None:        
        self._serviceDescriptor:set[ServiceDescriptor] = set()

    def RegisterSingleton(self, implementation:TService):
        self._serviceDescriptor.add(ServiceDescriptor.create(type(implementation), ServiceLifetime.Singleton))
	
    def RegisterSingleton(self, type_service:Type[TService], implementation:TService):
        self._serviceDescriptor.add(ServiceDescriptor.create(type_service, implementation, ServiceLifetime.Singleton))

    def RegisterTransient(self, implementation: TService):
        self._serviceDescriptor.add(ServiceDescriptor.create(implementation, ServiceLifetime.Transient))

    def RegisterTransient(self, type_service:Type[TService], implementation:TService):
        self._serviceDescriptor.add(ServiceDescriptor.create(type_service, implementation, ServiceLifetime.Transient))

    def GenerateContainer(self)->BaseDIConteiner:
        return DependencyContainer(self._serviceDescriptor)