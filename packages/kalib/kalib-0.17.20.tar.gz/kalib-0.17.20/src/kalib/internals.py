"""This module provides a collection of utility functions and classes for
introspection, type checking, and reflection in Python. It includes functions
to analyze objects, their types, inheritance hierarchies, and modules. The
module is designed to facilitate advanced programming tasks that require
detailed information about objects and their relationships.

**Key components:**

- **Constants**:
  - `IS_WINDOWS`: A boolean indicating if the current operating system is Windows.
  - `Nothing`: An instance of `NothingClass`, representing a singleton "nothing" value.

- **Class `Singleton`**: A metaclass for creating singleton classes. It ensures
  that only one instance of a class exists.

- **Class `NothingClass`**: A class that represents a singleton "nothing" value,
  which evaluates to `False`.

- **Type Checking Functions**:
  - `is_callable(obj)`: Checks if an object is callable.
  - `is_collection(obj)`: Checks if an object is a collection (and a sequence)
    but not a string or bytes.
  - `is_iterable(obj)`: Checks if an object is iterable.

- **Utility Functions**:
  - `unique(iterable, key=None, include=None, exclude=None)`: Yields unique elements
    from an iterable, optionally using a key function and inclusion/exclusion sets.
  - `trim_module_path(full)`: Trims the module path to exclude standard library
    directories and returns a tuple indicating if it's standard library code and
    the trimmed path.
  - `is_internal(x)`: Determines if an object is part of the standard library
    or built-in modules.
  - `class_of(obj)`: Returns the class of an object.
  - `issubstance(obj, types)`: Checks if an object matches a given type or types,
    handling complex typing constructs like `Union` and `Generic`.
  - `iter_inheritance(obj, include=None, exclude=None, exclude_self=True,
    exclude_stdlib=True, reverse=False)`: Iterates over the inheritance
    hierarchy (MRO) of an object with options to include or exclude certain
    types or modules.
  - `get_mro(obj, glue=None, **kw)`: Returns the method resolution order (MRO)
    of an object as a tuple or joined string.
  - `get_entity(obj, name, **kw)`: Retrieves an attribute from an object or its
    superclasses, returning the attribute and its owner class.
  - `get_owner(obj, name, **kw)`: Retrieves the owner class of an attribute.
  - `get_attr(obj, name, default=None, **kw)`: Retrieves an attribute from an
    object or its superclasses, with a default value if not found.
  - `get_module(x)`: Returns the module where an object is defined.
  - `get_module_name(x)`: Returns the name of the module where an object is defined.
  - `Who(obj, full=True, addr=False)`: Returns the fully qualified name of an object,
    with options to include the module and memory address.
  - `Is(obj, **kw)`: Returns a string representation of an object, including its
    type and value.
  - `objectname(obj, full=True)`: Returns the name of an object, handling functions,
    methods, classes, and modules.
  - `sourcefile(obj, **kw)`: Returns the source file path where an object is defined.
  - `stackoffset(order=None, shift=0)`: Calculates the stack frame offset, ignoring
    frames from specified files or modules.
  - `stackfilter(x)`: Filters out stack frames based on predefined patterns, used
    to clean up stack traces.
  - `stacktrace(count=None, join=True)`: Retrieves the current stack trace as a string
    or list of strings.
  - `about(something)`: Provides detailed information about an object, including
    its type, source file, and MRO.
  - `its_imported_module_name(name)`: Checks if a given module name corresponds
    to an imported module.
  - `get_module_from_path(path)`: Attempts to find the module name corresponding
    to a given file path.

- **Aliases for Common Functions**:
  - `mro`: Alias for `get_mro`.
  - `is_awaitable`: Alias for `inspect.isawaitable`.
  - `is_builtin`: Alias for `inspect.isbuiltin`.
  - `is_class`: Alias for `inspect.isclass`.
  - `is_coroutine`: Alias for `inspect.iscoroutine`.
  - `is_function`: Alias for `inspect.isfunction`.
  - `is_method`: Alias for `inspect.ismethod`.
  - `is_module`: Alias for `inspect.ismodule`.

The module relies on standard libraries such as `inspect`, `functools`, `typing`,
`pathlib`, and `sys`, as well as some utilities from the `kalib` package. It is
designed to support advanced introspection tasks, making it useful for debugging,
serialization, type checking, and dynamic code analysis.
"""
from collections.abc import Callable, Collection, Iterable, Mapping, Sequence
from contextlib import suppress
from functools import cache, partial
from inspect import (
    getmodule,
    getsourcefile,
    isawaitable,
    isbuiltin,
    isclass,
    iscoroutine,
    isfunction,
    ismethod,
    ismodule,
)
from itertools import filterfalse
from os.path import splitext
from pathlib import Path
from platform import architecture
from re import sub
from sys import modules
from sysconfig import get_paths
from traceback import extract_stack, format_stack
from types import FunctionType, LambdaType, UnionType
from typing import Any, Generic, Union, get_args, get_origin

IS_WINDOWS = 'windows' in architecture()[1].lower()


class NothingClass:
    def __bool__(self):
        return False

Nothing = NothingClass()


class Singleton(type):
    key = '__singleton_instance__'

    def __call__(self, *args, **kw):  # noqa: N804
        value = getattr(self, self.key, Nothing)
        if value is Nothing:
            value = super().__call__(*args, **kw)
            setattr(self, self.key, value)
        return value


def is_callable(obj):
    return isinstance(obj, Callable)


def is_collection(obj):
    return (
        isinstance(obj, Collection) and
        isinstance(obj, Sequence) and
        not isinstance(obj, bytes | str))


def is_mapping(obj):
    return isinstance(obj, Mapping)


def is_iterable(obj):
    return isinstance(obj, Iterable)



def unique(iterable, /, key=None, include=None, exclude=None):
    skip = include is None

    if not key:
        exclude = set(exclude or ())
        include = frozenset(include or ())

    else:
        exclude = set(map(key, exclude or ()))
        include = frozenset(map(key, include or ()))

    excluded = exclude.__contains__
    included = include.__contains__
    is_dict = isinstance(iterable, dict)

    for element in iterable:

        k = key(element) if key else element
        if not excluded(k) and (skip or included(k)):

            yield (element, iterable[element]) if is_dict else element
            exclude.add(k)

@cache
def trim_module_path(full):
    dirs = get_paths()

    path = str(full)
    if IS_WINDOWS:
        path = path.lower()

    for scheme, reason in (
        ('stdlib', True),
        ('purelib', False),
        ('platlib', False),
        ('platstdlib', True),
    ):
        subdir = dirs[scheme]
        if IS_WINDOWS:
            subdir = subdir.lower()

        if path.startswith(subdir):
            return reason, str(full)[len(subdir) +1:]

    subdir = str(Path(__file__).parent.parent)

    if IS_WINDOWS:
        subdir = subdir.lower()

    if path.startswith(subdir):
        return False, str(full)[len(subdir) +1:]

    return None, str(full)


def is_internal(x):
    if (isbuiltin(x) or isbuiltin(class_of(x))):
        return True

    elif (module := get_module(x)):

        try:
            path = module.__file__

        except AttributeError:
            if Who(module) == 'builtins':
                return True
            raise

        is_stdlib = trim_module_path(path)[0]
        if is_stdlib is not None:
            return is_stdlib

    return False


def class_of(obj):
    return obj if isclass(obj) else type(obj)


def issubstance(obj, types):  # noqa: PLR0911, PLR0912
    if types is None:
        return False

    if types in (Any, obj):
        return True

    if get_origin(types) in (Generic, Union, UnionType):
        klass = class_of(obj)
        included_types = get_args(types)
        if Any in included_types:
            return True

        for i in included_types:
            try:
                if issubstance(klass, i):
                    return True
            except TypeError:
                continue
        return False

    if is_collection(types) and not isinstance(types, tuple):
        types = tuple(types)

    if is_collection(types):
        if not types:
            return False

        elif Any in types:
            return True

    if get_args(types):
        types = get_origin(types)

    if types in (Any, obj):
        return True

    if is_collection(types) and obj in types:
        return True

    try:
        if (result := (
            isclass(obj) and
            (obj is types or issubclass(obj, types)))
        ):
            return result

        if not is_collection(types):
            return isinstance(obj, types)

        for sometype in types:
            if (result := issubstance(obj, sometype)):
                return result

    except TypeError as e:
        msg = f'invalid check what {Who.Is(obj)} is instance of {Who.Is(types)}'
        raise TypeError(msg) from e


def iter_inheritance(  # noqa: PLR0913
    obj,
    include        = None,
    exclude        = None,
    exclude_self   = True,
    exclude_stdlib = True,
    reverse        = False,
):
    order = class_of(obj).__mro__[:-1]

    if not exclude_self:
        order = unique((obj, *order), key=id)
    else:
        order = unique(filter(lambda x: x is not obj, order), key=id)

    if reverse:
        order = reversed(list(order))

    if include:
        if isinstance(include, FunctionType | LambdaType):
            order = filter(include, order)
        else:
            if not is_iterable(include):
                include = (include,)
            order = filter(include.__contains__, order)

    if exclude:
        if isinstance(exclude, FunctionType | LambdaType):
            order = filterfalse(exclude, order)
        else:
            if not is_iterable(exclude):
                exclude = (exclude,)
            order = filterfalse(exclude.__contains__, order)

    if exclude_stdlib:
        order = filterfalse(is_internal, order)

    yield from order


def get_mro(obj, /, **kw):

    func = kw.pop('func', None)
    glue = kw.pop('glue', None)

    result = iter_inheritance(obj, **kw)

    if func:
        result = tuple(map(func, result))

    if glue:
        result = glue.join(result)

    return result


def get_entity(obj, name, **kw):

    index = kw.pop('index', 0)
    kw.setdefault('exclude_self', False)
    kw.setdefault('exclude_stdlib', False)

    counter = 0
    for something in iter_inheritance(obj, **kw):
        try:
            attr = something.__dict__[name]
            if not counter - index:
                return attr, something
            counter += 1
        except KeyError:
            continue
    raise KeyError


def get_owner(obj, name, **kw):
    try:
        return get_entity(obj, name, **kw)[1]
    except KeyError:
        ...


def get_attr(obj, name, default=None, **kw):
    try:
        return get_entity(obj, name, **kw)[0]
    except KeyError:
        return default


def get_module(x):
    if ismodule(x):
        return x

    elif (
        (module := getmodule(x)) or
        (module := getmodule(class_of(x)))
    ):
        return module


def get_module_name(x):
    if module := get_module(x):
        with suppress(AttributeError):
            return module.__spec__.name


def Who(obj, /, full=True, addr=False): # noqa: N802
    key = '__name_full__' if full else '__name_short__'

    def get_name():
        try:
            store = obj.__dict__
            with suppress(KeyError):
                return store[key]
        except AttributeError:
            store = None

        name = objectname(obj, full=full)
        if store is not None:
            with suppress(AttributeError, TypeError):
                setattr(obj, key, name)
        return name

    name = get_name()
    if addr:
        name = f'{name}#{id(obj):x}'
    return name


def Is(obj, /, **kw): # noqa: N802
    from kalib.datastructures import try_json

    kw.setdefault('addr', True)
    msg = f'{Who(obj, **kw)}'

    if class_of(obj) is not obj:
        msg = f'({msg}):{try_json(obj)}'
    return msg


Who.Name = partial(Who, full=False)
Who.Is = Is


def objectname(obj, full=True):

    def post(x):
        return sub(r'^([\?\.]+)', '', sub('^(__main__|__builtin__|builtins)', '', x))

    def get_module_from(x):
        return getattr(x, '__module__', get_module_name(x)) or '?'

    def get_object_name(x):
        if obj is Any:
            return 'typing.Any' if full else 'Any'

        name = getattr(x, '__qualname__', x.__name__)
        module = get_module_from(x)

        if not name.startswith(module):
            name = f'{module}.{name}'
        return name


    def main(obj):
        if ismodule(obj):
            return get_module_name(obj)

        for itis in iscoroutine, isfunction, ismethod:
            if itis(obj):
                name = get_object_name(obj)
                with suppress(AttributeError):
                    name = f'{objectname(obj.im_self or obj.im_class)}.{post(name)}'
                return name

        cls = class_of(obj)
        if cls is property:
            return get_object_name(obj.fget)

        return get_object_name(cls)

    name = post(main(obj))
    return name if full else name.rsplit('.', 1)[-1]


def sourcefile(obj, **kw):
    kw.setdefault('exclude_self', False)
    kw.setdefault('exclude_stdlib', False)

    for i in iter_inheritance(obj, **kw):
        with suppress(TypeError):
            return getsourcefile(i)


def stackoffset(order=None, /, shift=0):
    stack = extract_stack()[:-1]

    def normalize(x):
        if not isinstance(x, bytes | str):
            x = sourcefile(x)
        return str(Path(x))

    @cache
    def is_ignored_frame(x):
        for path in order:
            if x.startswith(path):
                return True
    if order:
        counter = 0
        if isinstance(order, str | bytes):
            order = [order]
        order = set(map(normalize, filter(bool, order)))

        for no, frame in enumerate(reversed(stack)):
            if not is_ignored_frame(frame.filename):
                if counter >= shift:
                    return len(stack) - no -1
                else:
                    counter += 1
    return 0


def stackfilter(x):
    skip = (
        'kalib/descriptors.py", line 113, in __get__',
        'kalib/descriptors.py", line 56, in type_checker',
        'kalib/descriptors.py", line 135, in call',
        'kalib/descriptors.py", line 102, in call',
    )

    x = x.lstrip()
    if x.startswith('File "<frozen importlib._'):
        return True

    return any(filter(x.__contains__, skip))


def stacktrace(count=None, /, join=True):
    if count is None:
        count = stackoffset(__file__) + 1

    stack = format_stack()

    if count > 0:
        stack = stack[:count]

    elif count <= 0:
        return stack[len(stack) + count -2].rstrip()

    stack = tuple(map(str.strip, filterfalse(stackfilter, stack)))
    return '\n'.join(stack) if join else stack


def about(something):
    try:
        path = sourcefile(something)
    except TypeError:
        try:
            path = getsourcefile(something)
        except TypeError:
            path = None

    mro = get_mro(something, glue=', ')

    std = ('3rd party', 'from stdlib')[is_internal(something)]
    return f'{Who.Is(something)} ({std}) from {path=}, {mro=}'


@cache
def its_imported_module_name(name):

    with suppress(KeyError):
        return bool(modules[name])

    chunks = name.split('.')
    return sum(
        '.'.join(chunks[:no + 1]) in modules
        for no in range(len(chunks))) >= 2  # noqa: PLR2004

@cache
def get_module_from_path(path):
    def get_path_without_extension(path):
        return splitext(Path(path).absolute().resolve())[0]  # noqa: PTH122

    stem = get_path_without_extension(path)
    for name, module in modules.items():
        with suppress(AttributeError):
            if module.__file__ and stem == get_path_without_extension(module.__file__):
                return name

is_awaitable = isawaitable
is_builtin   = isbuiltin
is_class     = isclass
is_coroutine = iscoroutine
is_function  = isfunction
is_method    = ismethod
is_module    = ismodule
