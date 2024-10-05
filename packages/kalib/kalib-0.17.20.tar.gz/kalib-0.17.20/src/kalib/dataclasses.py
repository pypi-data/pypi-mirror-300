"""This module provides advanced utilities for working with data classes,
configurations, and automatic class generation. It extends the standard
`dataclasses` module with additional features such as validation,
serialization, dynamic class creation, and integration with custom logging
mechanisms.

**Key Components:**

- **Data Classes**:
  - `dataclass`: A custom data class decorator that extends the standard
    `dataclass` with additional functionality, such as:

    - Custom initialization to handle extra parameters and maintain memoization.

    - Policy handling for including or excluding extra items not defined inschema.

    - Methods for loading from various sources (e.g. files, json, dict).

    - Validation of field types and default values against the defined schema.

    - Serialization methods (`as_dict`, `as_json`) for converting instances
      to different formats.

    - Overloaded operators (`&`, `|`, `^`, `-`, `+`) for combining and comparing
      data class instances.

    - Property `is_valid` to check if an instance conforms to the defined schema.

- **Data Class Variants**:
  - `DataClassMutable`: A mutable variant of the custom `dataclass` (i.e., not frozen).

  - `DataClassFlexible`: That ignores extra fields, but save in separate attribute.

- **Automatic Class Generation**:
  - `autoclass`: A function that generates classes with automatic configuration
    loading and validation based on provided field names.

    - Can create classes dynamically for given field names.

    - Provides class-level and instance-level getters for configuration fields.

    - Includes methods like `from_dict`, `from_tuple`, `from_module`, and
      `from_namespace` for constructing instances from various sources.

**Usage and Purpose**:

- The module is designed to provide a flexible and powerful way to work with
  configurations and data classes, especially in scenarios where configurations
  need to be loaded, validated, and converted between different formats.

- It allows for automatic loading and validation of configurations from various
  sources, enforcing type correctness and required fields as defined in the schema.

- The custom `dataclass` class extends functionality by integrating with a logging
  system (`Logging.Mixin`), enabling informative messages and error reporting.

- Overloaded operators and serialization methods facilitate easy manipulation
  and comparison of data class instances, supporting operations like merging
  configurations or extracting differences.

- The auto class generation utilities enable dynamic creation of classes based on
    configuration schemas, which is useful for applications that need handle
    different configurations at runtime or generate classes based on external
    data sources.

**Notes**:

- Care should be taken to handle exceptions properly, especially when loading
  configurations, to ensure that errors are reported and managed appropriately.

- The module is designed to be extensible and adaptable to various use cases
  involving data classes and configurations, making it a valuable tool for
  developers working with complex data structures and dynamic class generation.
"""

from dataclasses import _FIELD, _MISSING_TYPE, Field, is_dataclass
from dataclasses import dataclass as base_dataclass
from datetime import date, datetime
from enum import IntFlag, auto
from operator import attrgetter, itemgetter
from pathlib import Path
from types import ModuleType, UnionType
from typing import (
    Any,
    ClassVar,
    Generic,
    Optional,
    Union,
    _UnionGenericAlias,
    get_args,
    get_origin,
)

from kalib.datastructures import json, loads
from kalib.descriptors import cache, pin
from kalib.importer import required, sort
from kalib.internals import (
    Nothing,
    Who,
    class_of,
    get_owner,
    is_callable,
    is_class,
    is_collection,
    is_iterable,
    issubstance,
    iter_inheritance,
    unique,
)
from kalib.logging import Args, Logging
from kalib.misc import sourcefile
from kalib.text import Str

REPR_LIMIT = 2 ** 14


def capitalize_snakes(something):
    return ''.join(map(str.capitalize, filter(bool, something.split('_'))))


class ConfigurationError(Exception):
    ...


class ConfigurationEvaluationError(ConfigurationError):
    ...


class ConfigurationSchemeError(ConfigurationError):
    ...


class ConfigurationSchemeMissingError(ConfigurationSchemeError):
    ...


class ConfigurationTypeError(ConfigurationSchemeError, TypeError):
    ...


def fields_cast(data):
    return ', '.join(f'({Who(data[k])}){k}' for k in sort(data))


@base_dataclass(kw_only=True)
class FieldDescriptions:
    name          : str
    type          : Any
    default       : Any
    factory       : Any
    typename      : str
    default_class : Any
    required      : bool


class dataclass(Logging.Mixin):  # noqa: N801

    def __init_subclass__(cls, *args, **kw):

        kw.update(getattr(cls, '__dataclass_options__', None) or {})
        kw.setdefault('eq', True)
        kw.setdefault('frozen', True)
        kw.setdefault('kw_only', True)

        self = base_dataclass(cls, *args, **kw)
        generic_initialize = self.__init__

        def __init__(self, *args, **kw):  # noqa: N807
            self.__dict__.update({
                '__instance_memoized__': {},
                '__non_model_items__': kw.pop('unused', {})})
            generic_initialize(self, *args, **kw)

        self.__init__ = __init__
        return self

    class Policy(IntFlag):
        Strict  = auto()
        Include = auto()
        Exclude = auto()

    policy = Policy.Strict

    @pin.cls
    def __fields__(cls):
        def make(x):
            if get_origin(x.type) in (Generic, Union, UnionType):
                name = ' | '.join(map(Who, get_args(x.type)))
            else:
                name = Who(x.type)

            factory = x.default_factory
            required = (
                {_MISSING_TYPE} ==
                set(map(class_of, (x.default, factory))))

            klass = class_of(x.default)
            return FieldDescriptions(
                name     = x.name,
                type     = x.type,
                typename = name,

                factory = factory,
                default = x.default,
                default_class = klass,
                required = required,
            )

        return tuple(map(make, cls.__dataclass_fields__.values()))

    @pin.cls
    def __fields_dict__(cls):
        fields = {f.name: f for f in cls.__fields__}
        if not issubstance(cls, dataclass):
            parents = class_of(cls).__mro__
            msg = f'{Who(cls)} must be a dataclass, {parents=}'
            raise ConfigurationTypeError(msg)

        for key, field in fields.items():
            if get_origin(field.type) is ClassVar:
                continue

            value = field.default
            if (
                field.default_class is not _MISSING_TYPE
                and not issubstance(value, field.type)
            ):
                config = json.repr(fields)
                msg = (
                    f'{Who(cls)}: ({field.typename}) '
                    f'{key=} invalid default value ({Who(value)}), {config=}')
                raise ConfigurationEvaluationError(msg)

        return fields

    @pin.cls
    def __mro_classes__(cls):
        result = []
        logging = class_of(Logging.Mixin).__name__
        skip = {BaseAutoClass, DataClassFlexible, Logging.Mixin, dataclass}

        for c in iter_inheritance(cls, exclude_stdlib=False):
            if c not in skip and c.__name__ != logging:
                result.append(c)
        return tuple(result)

    @classmethod
    def _process_extra_items(cls, data):
        extra = {}
        if data:
            policy = cls.policy
            if policy & cls.Policy.Exclude:
                extra = dict(data)
            else:
                msg = f'{Who(cls)}[{policy=}]: extra: {fields_cast(data)} passed'
                raise ConfigurationEvaluationError(msg)

        return {}, extra

    @classmethod
    def _preload(cls, data, *args, **kw):  # noqa: ARG003
        return data

    @classmethod
    def _post(cls, data, *args, **kw):  # noqa: ARG003
        return data

    @classmethod
    def _process(cls, data, *args, **kw):  # noqa: ARG003
        fields = cls.__fields_dict__

        if isinstance(data, dict):
            data = dict(data)
            for key, field in fields.items():
                try:
                    if (
                        class_of(field.type) not in (UnionType, _UnionGenericAlias)
                        and issubclass(field.type, dataclass)
                        and isinstance(data[key], dataclass | dict)
                    ):
                        data[key] = field.type.load(data.pop(key))

                except KeyError as e:
                    msg = (
                        f'{Who(cls)}: require missing ({field.typename}):'
                        f'{key=}; got {fields_cast(data)}')
                    raise ConfigurationEvaluationError(msg) from e

        if not args:
            if isinstance(data, dict):
                return dict(data)

            if is_dataclass(data):
                result = {}
                for key, field in fields.items():
                    try:
                        result[key] = getattr(data, key)
                    except AttributeError as e:
                        msg = (
                            f'{Who(cls)}: require missing ({field.typename}):'
                            f'{key=}; got {fields_cast(data)}')
                        raise ConfigurationEvaluationError(msg) from e

                return result

        elif len(args) + 1 != len(fields):
            data = json.repr(data)
            msg = (f'{Who(cls)}: scheme {len(fields):d} '
                   f"fields ({' '.join(tuple(fields))}) "
                   f"couldn't match to {len(args) + 1:d} "
                   f'taken args: {Args(data, *args)}')
            raise ConfigurationEvaluationError(msg)

        args = (data, *args)
        if not fields and args:
            msg = (f"{Who(cls)}: scheme haven't any fields, "
                   f'taken args: {Args(args)}')
            raise ConfigurationEvaluationError(msg)

        required = len(list(filter(attrgetter('required'), fields.values())))
        if required > len(args):
            msg = (f'{Who(cls)}: scheme {required=} '
                   f"fields ({' '.join(tuple(fields))}) "
                   f"couldn't match to {len(args):d} "
                   f'taken args: {Args(data, *args)}')
            raise ConfigurationEvaluationError(msg)

        return dict(zip(list(fields)[:len(args)], args, strict=True))

    @classmethod
    def from_file(cls, path, *args, **kw):
        with Path(path).open('rb') as fd:
            return cls.load(json.loads(fd.read()), *args, **kw)

    @classmethod
    def loads(cls, body, *args, **kw):
        return cls.load(loads(body) or json.loads(body), *args, **kw)

    @classmethod
    def load(cls, data, *args, **kw):
        if isinstance(data, cls) and class_of(data) is cls:
            return data.copy(**kw)

        fields = cls.__fields_dict__
        validate = kw.pop('validate', True)

        data = cls._preload(data, *args, **kw)
        data = cls._process(data, *args, **kw)

        additional_items, unused_items = (
            cls._process_extra_items(
                dict(unique(data, exclude=fields))))

        result = dict(unique(data, include=fields))
        result.update(additional_items)

        for key, field in unique(fields, exclude=result):
            value = field.default

            if issubstance(value, _MISSING_TYPE):
                types = getattr(field.type, '__args__', None)
                if (
                    (field.typename != 'builtins.NoneType') and
                    (not types or not issubstance(None, types))
                ):
                    if not issubstance(field.factory, _MISSING_TYPE):
                        value = field.factory()
                    else:
                        msg = (
                            f'{Who(cls)}: require missing ({field.typename}):'
                            f'{key=}; got {fields_cast(data)}')
                        raise ConfigurationEvaluationError(msg)
                else:
                    value = None

            result[key] = value

        self = cls(unused=unused_items, **cls._post(result, *args, **kw))
        try:
            if validate and not self.is_valid:
                data = json.repr(data)[:REPR_LIMIT]
                self.log.warning(f'{Who(cls)}: invalid data={data}')

        except ConfigurationError as e:

            for message in e.args[1].values():
                self.log.error(f'{Who(cls)}: {message}')  # noqa: TRY400

            self.log.error(f'{e.args[0]}')  # noqa: TRY400
            raise

        return self

    @property
    def extra_kwargs(self):
        return dict(self.__dict__['__non_model_items__'])

    @pin.any
    def as_dict(self) -> dict:
        return dict(self.__fields_dict__ if is_class(self) else self)

    @pin
    def as_json(self) -> str:
        return json.dumps(self.as_dict)

    @pin
    def as_sql(self) -> dict:
        def sql_cast(key, value):

            if value is None:
                return 'NULL'

            elif isinstance(value, str):
                return f'"{value}"'

            elif isinstance(value, bool | int):
                return int(value)

            elif isinstance(value, datetime):
                return value.strftime('"%Y-%m-%d %H:%M:%S"')

            elif isinstance(value, date):
                return value.strftime('"%Y-%m-%d"')

            msg = f'{key=}: {Who.Is(value)}'
            self.log.exception(msg)
            raise TypeError(msg)

        return {k: sql_cast(k, v) for k, v in self.as_dict.items()}

    def to_sql(self, glue=',', /, callback=None):
        return glue.join(
            f'{k}={v}' for k, v in self.as_sql.items()
            if not is_callable(callback) or callback(v))

    @pin
    def export(self):
        return self.as_dict | self.extra_kwargs

    def copy(self, /, **kw):
        return self.load(self.export | kw)


    def __iter__(self):
        for key, field in self.__fields_dict__.items():
            try:
                value = getattr(self, key)

            except AttributeError as e:
                msg = (
                    f'{Who(self)}: scheme defined ({Who(key)}) '
                    f'{key!a} missing, but expected {field=}')
                raise ConfigurationEvaluationError(msg) from e

            yield key, value

    @pin
    def fields(self):
        return tuple(map(itemgetter(0), self))

    def __and__(self, other):

        if self is other:
            return self.copy()

        elif isinstance(other, dataclass):
            other = other.export


        if isinstance(other, dict):
            return from_dict({
                k: v for k, v in self.export.items()
                if k in other and v == other[k]}, name=Who(other, full=False))

        elif is_collection(other):
            ...

        elif isinstance(other, str):
            other = [other]

        else:
            msg = f'{Who.Is(other)} must be dict | str | Iterable | {Who(dataclass)}'
            self.log.fatal(msg)
            raise TypeError(msg)

        data = self.export
        return from_dict(
            {k: data[k] for k in set(data) & set(other)}, name=Who(other, full=False))

    def __xor__(self, other):

        if not other:
            return self.copy()

        elif self is other:
            raise ValueError

        elif isinstance(other, dataclass):
            other = other.export


        if isinstance(other, dict):
            export = self.export
            return from_dict({
                k: export.get(k, other[k])
                for k, v in set(export) ^ set(other)}, name=Who(other, full=False))

        msg = f'{Who.Is(other)} must be dict | {Who(dataclass)}'
        self.log.fatal(msg)
        raise TypeError(msg)


    def __sub__(self, other):

        if not other:
            return self.copy()

        elif self is other:
            raise ValueError

        elif isinstance(other, dataclass):
            other = other.export


        if isinstance(other, dict):
            return self.load({
                k: v for k, v in self.export.items()
                if k not in other or v == other[k]})

        elif is_collection(other):
            ...

        elif isinstance(other, str):
            other = [other]

        else:
            msg = f'{Who.Is(other)} must be dict | str | Iterable | {Who(dataclass)}'
            self.log.fatal(msg)
            raise TypeError(msg)

        return from_dict(
            {k: v for k, v in self.export.items() if k not in other},
            name=Who(other, full=False))

    def __or__(self, other):

        if self is other or not other:
            return self.copy()

        elif isinstance(other, dataclass):
            other = other.export

        else:
            msg = f'{Who.Is(other)} must be dict | {Who(dataclass)}'
            self.log.fatal(msg)
            raise TypeError(msg)

        return from_dict(self.export | other, name=Who(other, full=False))

    def __add__(self, other):

        if isinstance(other, dataclass):
            other = other.export

        if isinstance(other, dict):
            return self.load({
                k: v for k, v in self.export.items()
                if k in other and v != other[k]})

        return self.__or__(other)

    @pin
    def is_valid(self):
        result = {}
        fields = self.__fields_dict__

        for key, value in self:
            field = fields[key]

            objecttype = field.type

            if field.type in (False, True):
                objecttype = bool

            elif field.type in (False, True):
                objecttype = None

            if not issubstance(value, objecttype):
                result[key] =(
                    f'({field.typename}) {key!a} invalid type ({Who.Is(value)})')

        if result:
            msg = f"{Who(self)}: {'; '.join(sort(result))}"
            raise ConfigurationEvaluationError(msg, result)
        return True


class DataClassMutable(dataclass):
    __dataclass_options__ = {'frozen': False}  # noqa: RUF012


class DataClassFlexible(dataclass):
    policy = dataclass.Policy.Exclude


class BaseAutoClass(Logging.Mixin):
    __field__ = None

    @classmethod
    def __autoclasses_fields__(cls):
        hier = iter_inheritance(
            cls, exclude_stdlib=False,
            include=lambda x: issubstance(x, BaseAutoClass))

        for klass in hier:
            if klass is get_owner(klass, '__field__') and klass.__field__:
                yield klass

    @pin.root
    def __autoclasses__(cls):
        return frozenset(map(attrgetter('__field__'), cls.__autoclasses_fields__()))


@cache
def make_getters(field):
    Field, _field = field.capitalize(), f'_{field}'  # noqa: N806

    class autoclass(BaseAutoClass):  # noqa: N801
        __field__ = field

        def __init__(self, *args, **kw) -> None:
            # TODO: валидировать (опционально) принимаемый конфиг проактивно здесь
            setattr(self, f'_{field}', kw.pop(field, Nothing))
            if (
                get_owner(class_of(self), Field) is
                get_owner(BaseAutoClass, Field)
            ):
                self.log.warning(
                    f"{Who(self)}.{Field}{sourcefile(self, '(in %s)')} "
                    f"isn't defined, but required because "
                    f"it's {field} schema for instances")


            if (
                get_owner(class_of(self), field) !=
                get_owner(BaseAutoClass, field)
            ):
                self.log.warning(
                    f'{Who(self)}.{field} property overrided', once=True)

            elif getattr(self, f'_{field}', Nothing) is Nothing:
                self.log.warning(
                    f"{Who(self)}{sourcefile(self, 'from %s')} it's class "
                    f'with dataclass.BaseAutoClass (by {Who(BaseAutoClass)}), '
                    f'but initialized without {field}={{}} passed to __init__; '
                    f'{Who(self)}.{field} call now useless', trace=True, shift=-1)

            if self in args:
                where = 'as first arg' if args[0] is self else 'into args'
                self.log.warning(
                    f'{Who(self, addr=True)}: self {where} passed',
                    trace=True, shift=-1)

            try:
                super().__init__(*args, **kw)

            except TypeError:
                self.log.fatal(
                    f'{Who(self)}: {Who(super())}'
                    f'.__init__(*{args=}, **{kw=}) failed')
                raise

    def ClassGetter(cls):  # noqa: N802
        msg = (
            f"{Who(cls)}.{Field}{sourcefile(cls, '(from %s)')} "
            f"isn't defined, but required because it's config schema for instances")
        raise TypeError(msg)

    def InstanceGetter(self):  # noqa: N802
        scheme = getattr(self, Field)

        if scheme is None:
            msg = f"{Who(self)}.{Field} isn't defined or None instead dataclass"
            raise ConfigurationSchemeMissingError(msg)

        if not issubclass(scheme, dataclass):
            inheritance = ' -> '.join(map(Who, scheme.__mro_classes__))
            msg = f'{Who(self)}.{Field} must be dataclass, {inheritance=}'
            raise ConfigurationTypeError(msg)

        if getattr(self, _field, Nothing) is Nothing:
            classes = [
                f'{Who(cls)}{sourcefile(cls, "(%s)")}'
                for cls in scheme.__mro_classes__]
            msg = (
                f'{Who(self)}.{_field} missing, probably you forgot to pass '
                f'{field} dict as kwarg via super().__init__({field}=), check in '
                f"{', '.join(classes)}")
            raise ConfigurationSchemeMissingError(msg)

        config = getattr(self, _field)
        try:
            result = scheme.load(config)

        except Exception as e:
            config = json.repr(config)
            inheritance = ' -> '.join(map(Who, scheme.__mro_classes__))
            msg = (
                f"{Who(self)} couldn't load {config} "
                f'into {scheme=} ({inheritance})')
            if getattr(self, _field, None) is None:
                msg = (
                    f'{msg}, maybe you forgot to pass {field} as kwarg to '
                    f'{Who(self, full=False)}({field}=)?')
            raise ConfigurationSchemeError(msg) from e

        self.log.debug(f'{result}', once=False)
        return result

    autoclass.__name__ = f'{autoclass.__name__}({field})'
    autoclass.__qualname__ = f'{autoclass.__name__}'

    ClassGetter.__name__ = Field
    InstanceGetter.__name__ = field

    ClassGetter.__qualname__ = f'{autoclass.__qualname__}.{Field}'
    InstanceGetter.__qualname__ = f'{autoclass.__qualname__}.{field}'

    setattr(autoclass, Field, pin.cls(ClassGetter))
    setattr(autoclass, field, pin(InstanceGetter))

    return autoclass


def autoclass(*args):
    if len(args) == 1:
        return make_getters(args[0])
    return tuple(map(make_getters, args))


def simple(classname, *names, **kw):
    mro = kw.pop('mro', None) or ()
    if not is_iterable(mro):
        mro = [mro]
    mro = [*list(mro), BaseAutoClass, dataclass]

    fields = {}
    default = _MISSING_TYPE()
    for name in names:
        field = Field(default, default, True, True, None, True, {}, True)  # noqa: FBT003
        field.name = name
        field.type = Optional[Any]  # noqa: UP007
        field._field_type = _FIELD  # noqa: SLF001
        fields[name] = field

    fields['__annotations__'] = {f.name: f.type for f in fields.values()}

    return type(classname, tuple(mro), fields)


def from_dict(*args, **kw):
    mro = kw.pop('mro', [])

    if (
        len(args) >= 2 and  # noqa: PLR2004
        isinstance(args[0], str) and
        isinstance(args[1], dict)
    ):
        classname, data = args[:2]
        args = args[2:]

    elif (
        len(args) == 1 and kw and
        isinstance(args[0], str)
    ):
        classname = args[0]
        args, data = (), dict(kw)

    elif (
        len(args) == 1 and
        kw.get('name') and
        isinstance(args[0], dict)
    ):
        classname = kw.pop('name')
        args, data = args[1:], args[0]

    elif len(args) >= 1 and isinstance(args[0], dict):
        classname, data = Who(autoclass), args[0]
        args = args[1:]

    elif not args and kw:
        classname, data = Who(autoclass), dict(kw)

    else:
        msg = f'for {Who(autoclass)}(*{args=}, **{kw=})'
        raise NotImplementedError(msg)

    return simple(classname, *data, mro=mro).load(data, *args, **kw)


def from_tuple(*fields, **kw):

    def wrapper(*args, **kwlocal):

        if len(args) == 1 and is_collection(args):
            args = args[0]

        if len(args) != len(fields):
            msg = f'{Who.Is(args)} must be {len(fields)} args: {fields}'
            raise TypeError(msg)

        return from_dict(dict(zip(fields, args, strict=False)), **(kw | kwlocal))

    return wrapper


def from_module(module, /, order=None, name=None):

    if isinstance(module, bytes | str):
        module = required(Str.to_ascii(module))

    if not isinstance(module, ModuleType):
        msg = f'{Who.Is(module)} must be {Who(ModuleType)} or bytes | str'
        Logging.get(module).fatal()
        raise TypeError(msg)

    data = {
        name: getattr(module, name)
        for name in (order or module.__all__)}
    return dataclass.FromDict(name, data) if name else dataclass.FromDict(data)


def from_namespace(namespace, /, callback=capitalize_snakes, name=None):
    data = {(callback(k) if callback else k): v for k, v in namespace._get_kwargs()}  # noqa: SLF001
    return dataclass.FromDict(name, data) if name else dataclass.FromDict(data)

dataclass.base      = BaseAutoClass
dataclass.exception = ConfigurationError

dataclass.flex      = DataClassFlexible
dataclass.mutable   = DataClassMutable

dataclass.auto      = autoclass
dataclass.simple    = simple
dataclass.dict      = from_dict
dataclass.module    = from_module
dataclass.space     = from_namespace
dataclass.tuple     = from_tuple
