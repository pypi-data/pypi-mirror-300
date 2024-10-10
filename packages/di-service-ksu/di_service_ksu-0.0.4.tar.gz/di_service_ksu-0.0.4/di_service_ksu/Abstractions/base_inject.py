#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>


from abc import ABCMeta
from typing import Protocol, runtime_checkable

from ..Utilites.ext_reflection import ExtReflection

@runtime_checkable
class BaseInject(Protocol, metaclass=ABCMeta):
    def __init_subclass__(cls) -> None:
        for attr, value in cls.__dict__.items():
            if callable(value):
                if attr == '__init__':
                    setattr(cls, attr, ExtReflection.init_inject(value))
        
        return super().__init_subclass__()