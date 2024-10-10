#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from .Abstractions.base_di_container import BaseDIConteiner, TService

class ResolveProvider():
    __container:BaseDIConteiner = None
    def __init__(self, container:BaseDIConteiner) -> None:
        if ResolveProvider.__container == None:
            ResolveProvider.__container:BaseDIConteiner = container

    def get_service(cls:TService)->TService | None:
        if ResolveProvider.__container == None:
            raise Exception('Not initialize ResolveProvider !')
        else:
            return ResolveProvider.__container.GetService(cls)