#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from typing import Type, TypeVar

from ..Enums.service_life import ServiceLifetime

T = TypeVar('T', bound='ServiceDescriptor')

class ServiceDescriptor():
    def __init__(self) -> None:
        self.ServiceType: Type = None
        self.ImplementationType: Type	 = None
        self.Implementation:object = None
        self.Lifetime:ServiceLifetime = None
	
    @classmethod
    def create(cls: Type[T], serviceType:Type , lifetime:ServiceLifetime)-> T:
         new_instance = cls()
         new_instance.ServiceType = serviceType
         new_instance.Lifetime = lifetime

         return new_instance

    @classmethod
    def create(cls: Type[T], implementation:object, lifetime:ServiceLifetime)-> T:
        new_instance = cls()
        new_instance.ServiceType = type(implementation)
        new_instance.Implementation = implementation
        new_instance.Lifetime = lifetime

        return new_instance
    
    @classmethod
    def create(cls: Type[T], serviceType:Type, implementationType:Type, lifetime: ServiceLifetime)-> T:
        new_instance = cls()
        new_instance.ServiceType = serviceType
        new_instance.ImplementationType = implementationType
        new_instance.Lifetime = lifetime

        return new_instance