#        _       __        __    __________    _____     __   __     __
#   	/ \	    |  |	  |__|  |__________|  |  _  \   |__|  \ \   / /
#      / _ \	|  |	   __       |  |      | |_)  |   __    \ \_/ /   Alitrix - Modern NLP
#     / /_\ \	|  |	  |  |      |  |      |  _  /   |  |    } _ {    Languages: Python, C#
#    / _____ \	|  |____  |  |      |  |      | | \ \   |  |   / / \ \   http://github.com/Alitrix
#   /_/     \_\	|_______| |__|	    |__|      |_|  \_\  |__|  /_/   \_\

# Licensed under the MIT License <http://opensource.org/licenses/MIT>
# SPDX-License-Identifier: MIT
# Copyright (c) 2020-2021 The Alitrix Authors <http://github.com/Alitrix>

from functools import wraps
import inspect
import itertools
from types import FunctionType
from typing import Any, TypeVar, Callable

T = TypeVar('T')
_C = TypeVar("_C", bound=Callable[..., None])

class ExtReflection():
    def get_methods_class(cls):
        return set((x, y) for x, y in cls.__dict__.items()
                    if isinstance(y, (FunctionType, classmethod, staticmethod))
                    and not(x.startswith("__") and x.endswith("__")))

    def get_list_parent_methods(cls):
        return set(itertools.chain.from_iterable(
            ExtReflection.get_methods_class(c).union(ExtReflection.get_list_parent_methods(c)) for c in cls.__bases__))

    def list_subclass_methods(cls, is_narrow:bool):
        methods = ExtReflection.get_methods_class(cls)
        if  is_narrow:
            parentMethods = ExtReflection.get_list_parent_methods(cls)
            return set(cls for cls in methods if not (cls in parentMethods))
        else:
            return methods
    
    def get_handler_method(object:object, name_method:str, *args)->Callable:
        call_method = getattr(object, name_method)
        return call_method
    
    def get_class_info(cls:T)->list:
        if type(cls) is type.__class__:
            class_params = inspect.signature(cls.__init__)
            class_args:list[dict] = []
            for param_name in class_params.parameters:
                param_d = class_params.parameters[param_name]
                type_param = param_d.annotation if not param_d.annotation is inspect._empty else param_d.default if not param_d.default is inspect._empty else cls
                class_args.append({'name':param_name, 'type':type_param})
        
        return class_args

    def get_function_info(fn:Callable[..., Any])->dict:
        if not callable(fn):
            raise Exception(f'{fn.__name__} - Is not callable object.')
        
        fn_datas:dict = {}
        fn_args:list[dict] = []
        
        fn_datas['class'] = inspect._findclass(fn)
        fn_datas['name'] = fn.__name__

        fn_params = inspect.signature(fn)
        for param_name in fn_params.parameters:
            param_d = fn_params.parameters[param_name]
            type_param = param_d.annotation if not param_d.annotation is inspect._empty else param_d.default
            fn_args.append({'name':param_name, 'type':type_param})

        fn_datas['params'] = fn_args

        return fn_datas

    def init_inject(func: _C)-> _C:
        from ..Abstractions.base_inject import BaseInject
        from ..resolve_provider import ResolveProvider
        @wraps(func)
        def wrapper(*args, **kwargs)->Any:
            if 'is_inject' not in kwargs:
                fn_datas = ExtReflection.get_function_info(func)
                new_kwarg = list(args)

                for item in fn_datas['params']:
                    if item['name'] != 'self':
                        if issubclass(item['type'], BaseInject):
                            search_service = ResolveProvider.get_service(item['type'])
                            if search_service != None:
                                new_kwarg.append(search_service)

                result = func(*new_kwarg, **kwargs)

                return result
            else:
                new_kwarg = {}
                for item in [item for item in kwargs if item != 'is_inject']:
                    element = {item:kwargs[item]}
                    new_kwarg.update(element)

                result = func(*args, **new_kwarg)

                return result

        return wrapper