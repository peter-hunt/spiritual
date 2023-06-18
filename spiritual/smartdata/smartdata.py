from json import load as json_load
from types import GenericAlias, UnionType

from ..myjson import dump as json_dump

__all__ = ['SmartData', 'is_type', 'load_value', 'dump_value']


def is_type(obj, type_):
    if issubclass(type_, SmartData):
        return type_.is_valid(obj)
    elif isinstance(type_, type):
        return isinstance(obj, type_)
    elif isinstance(type_, UnionType):
        for arg in type_.__args__:
            if is_type(obj, arg):
                return True
        return False
    elif isinstance(type_, GenericAlias):
        origin = type_.__origin__
        if origin is tuple or origin is set:
            if not isinstance(obj, list | origin):
                return False
        elif not isinstance(obj, origin):
            return False
        if origin is tuple:
            args = type_.__args__
            if len(args) != len(obj):
                return False
            for i, arg in enumerate(args):
                if not is_type(obj[i], arg):
                    return False
            return True
        elif origin is list:
            arg = type_.__args__[0]
            for item in obj:
                if not is_type(item, arg):
                    return False
            return True
        elif origin is dict:
            key_type, value_type = type_.__args__
            for key, value in obj.items():
                if not is_type(key, key_type) or not is_type(value, value_type):
                    return False
            return True
        elif origin is set:
            arg = type_.__args__[0]
            for item in obj:
                if not is_type(item, arg):
                    return False
            return True
        else:
            raise NotImplementedError(f'Unknown origin: {origin}')
    else:
        raise NotImplementedError(f'Unknown type: {type_}')


def load_value(obj, type_):
    if issubclass(type_, SmartData):
        return type_.loads(obj)
    elif isinstance(type_, type):
        return type_(obj)
    elif isinstance(type_, UnionType):
        for arg in type_.__args__:
            if is_type(obj, arg):
                return load_value(obj, arg)
    elif isinstance(type_, GenericAlias):
        origin = type_.__origin__
        if origin is tuple:
            args = type_.__args__
            if len(args) != len(obj):
                raise ValueError('Invalid number of arguments')
            return tuple(load_value(obj[i], arg) for i, arg in enumerate(args))
        elif origin is list:
            arg = type_.__args__[0]
            return [load_value(item, arg) for item in obj]
        elif origin is dict:
            key_type, value_type = type_.__args__
            return {load_value(key, key_type): load_value(value, value_type)
                    for key, value in obj.items()}
        elif origin is set:
            arg = type_.__args__[0]
            return {load_value(item, arg) for item in obj}
        else:
            raise NotImplementedError(f'Unknown origin: {origin}')
    else:
        raise NotImplementedError(f'Unknown type: {type_}')


def dump_value(obj):
    if isinstance(obj, SmartData):
        return obj.dumps()
    elif isinstance(obj, tuple | list | set):
        return [dump_value(item) for item in obj]
    elif isinstance(obj, dict):
        return {dump_value(key): dump_value(value)
                for key, value in obj.items()}
    else:
        return obj


class SmartData:
    def __init__(self, *args, **kwargs):
        fields = []
        positional = 0
        keyword = 0
        for key, type_ in self.__annotations__.items():
            if hasattr(self, key):
                keyword += 1
            else:
                positional += 1
            fields.append((key, type_, getattr(self, key, None)))
        if positional < len(args) or len(args) + len(kwargs) > positional + keyword:
            raise ValueError('Invalid number of arguments')

        for i, arg in enumerate(args):
            key, type_, default = fields[i]
            if not is_type(arg, type_):
                raise TypeError(f'Invalid type for argument {i}')
            setattr(self, key, arg)

        used_kwargs = {*()}
        for key, arg in kwargs.items():
            if key not in self.__annotations__:
                raise TypeError(f'Invalid keyword argument {key}')
            if not is_type(arg, self.__annotations__[key]):
                raise TypeError(f'Invalid type for keyword argument {key}')
            setattr(self, key, arg)
            used_kwargs.add(key)

        for key, type_, default in fields[len(args):]:
            if key in used_kwargs:
                continue
            if default is None:
                raise TypeError(f'Missing keyword argument {key}')
            setattr(self, key, default)

    @classmethod
    def is_valid(cls, obj):
        for key, type_ in cls.__annotations__.items():
            if key not in obj:
                return False
            if not is_type(obj[key], type_):
                return False
        return True

    @classmethod
    def load(cls, file):
        return cls.loads(json_load(file))

    @classmethod
    def loads(cls, obj):
        values = {}
        for key, type_ in cls.__annotations__.items():
            if key not in obj and getattr(cls, key, None) is None:
                raise ValueError(f'Missing key {key}')
            if not is_type(obj[key], type_):
                raise ValueError(f'Invalid type for key {key}')
            values[key] = load_value(obj[key], type_)
        return cls(**values)

    def dump(self, file):
        json_dump(self.dumps(), file)

    def dumps(self):
        obj = {}
        for key, type_ in self.__annotations__.items():
            obj[key] = dump_value(getattr(self, key))
        return obj
