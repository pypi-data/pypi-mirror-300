#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

import inspect
from typing import Type, TypeVar

from .Abstractions.base_di_container import BaseDIConteiner
from .Enums.service_life import ServiceLifetime

TService = TypeVar('TService')

class DependencyContainer(BaseDIConteiner):
    def __init__(self, serviceDescriptors:set) -> None:
        self.__serviceDescriptors:set = serviceDescriptors
    
    def __GetService(self, serviceType:Type)->object:
        descriptor = [item for item in self.__serviceDescriptors if item.ServiceType == serviceType]

        if len(descriptor) > 0:
            descriptor = descriptor[0]
        else:
            #raise Exception(f"Service of type {serviceType.__name__} isn`t registered !")
            return None
        
        if descriptor.Implementation != None:
            return descriptor.Implementation

        if descriptor.ImplementationType != None:
            actualType = descriptor.ImplementationType
        else:
            actualType = descriptor.ServiceType

        if inspect.isabstract(actualType):
            raise Exception("Cannot instantiate abstract classes.")

        sig = inspect.signature(actualType)
        lst_args_obj = {}

        if len(sig.parameters) > 0:
            for item in sig.parameters:
                annotation = sig.parameters[item].annotation
                implement = self.__GetService(annotation)
                lst_args_obj[item] = implement
        else:
            implementation = actualType(**{'is_inject':True})
            if descriptor.Lifetime == ServiceLifetime.Singleton:
                descriptor.Implementation = implementation
            return implementation

        lst_args_obj.update({'is_inject':True})
        implementation = actualType(**lst_args_obj)

        if descriptor.Lifetime == ServiceLifetime.Singleton:
            descriptor.Implementation = implementation

        return implementation

    def GetService(self, cls:Type[TService]) -> TService | None:
        return self.__GetService(cls)