"""This module provides a collection of utility functions and classes for
various purposes such as timing, data collection, partial function application,
lazy evaluation, and more.

Key components:

- **Function `Now`**: Returns the current datetime with optional timezone
  information and allows for time adjustments using keyword arguments.

- **Function `stamp`**: Returns UNIX timestamp of the current time, optionally adjusted.

- **Class `Timer`**: A context manager for measuring execution time. It records
  the start and end times of a code block, providing the time spent (`spent`) and
  the elapsed time (`delta`).

- **Class `Collector`**: A context manager for collecting and aggregating statistical
  data over time. It tracks events and computes statistics like median values and load
  averages over specified intervals defined in `Limits`.

- **Class `Partial`**: An extension of `functools.partial` that supports lazy
  evaluation and caching of partial function calls. It includes additional features
  like logging and result introspection.

- **Function `lazy_proxy_to`**: A decorator factory for creating lazy proxy attributes
  in classes. It forwards attribute access to another object or method, enabling
  dynamic attribute resolution and reducing code duplication.

- **Function `incremental_delay`**: Generates a function that computes delays based
  on an exponential backoff strategy. It's useful for implementing retry mechanisms
  with incremental delays and optional randomness.

- **Function `sourcefile`**: Retrieves the source file path of a given object, with
  optional templating for formatting. It enhances introspection capabilities.

- **Function `to_tuple`**: Ensures the input is converted to a tuple, handling both
  iterable and non-iterable inputs appropriately.

- **Function `toml_read`**: Reads and parses a TOML file using the appropriate library
  based on the Python version (`tomllib` for Python >= 3.11, `tomli` otherwise).

- **Function `yaml_read`**: Reads and parses a YAML file using a safe loader from the
  `yaml` library, ensuring secure parsing.

- **Function `unique`**: A deprecated function that redirects to
  `kalib.internals.unique`, emitting a deprecation warning for backward compatibility.

- **Function `cycler`**: Returns a function that cycles indefinitely through the
  given array. Useful for creating infinite iterators over a sequence.

- **Function `shuffler`**: Returns a function that shuffles the given array and
  cycles through it, providing a randomized iterator over the elements.

This module relies on external dependencies from the `kalib` package, including
modules for descriptors (`kalib.descriptors`), internal utilities (`kalib.internals`),
and logging (`kalib.logging`). It also conditionally imports modules based on the
Python version to maintain compatibility.

Overall, the utilities in this module are designed to enhance code efficiency,
readability, and functionality by providing common tools needed for advanced
programming tasks.
"""

from collections import Counter, defaultdict, deque
from contextlib import suppress
from datetime import datetime, timedelta, timezone
from functools import cached_property, partial
from itertools import cycle
from math import exp
from operator import attrgetter, methodcaller
from pathlib import Path
from random import shuffle, uniform
from statistics import median
from sys import stderr, stdin, stdout, version_info
from time import time

from kalib.descriptors import pin, prop
from kalib.internals import (
    Nothing,
    Who,
    class_of,
    get_attr,
    is_class,
    is_collection,
    is_iterable,
)
from kalib.internals import sourcefile as generic_sourcefile

if version_info >= (3, 11):
    from tomllib import load as toml_load
else:
    from tomli import load as toml_load  # ==3.10


tty = all(map(methodcaller('isatty'), (stderr, stdin, stdout)))


def Now(tz=True, /, **kw):  # noqa: N802
    if tz:
        result = datetime.now(tz=timezone.utc if tz is True else tz)
    else:
        result = datetime.utcnow()  # noqa: DTZ003

    return (result + timedelta(**kw)) if kw else result


def stamp(**kw):
    return Now(**kw).replace(tzinfo=None).timestamp()


class Timer:

    @prop.cls
    def now(self):
        return time()

    @prop.cls
    def stamp(self):
        return stamp()

    def __init__(self):
        self._start = None
        self.spent = None

    def __enter__(self):
        self._start = time()

    def __exit__(self, *args):
        self.spent = time() - self._start

    @property
    def delta(self):
        return time() - self._start


class Collector:

    Limits = 1, 5, 15

    def __init__(self, /, **variables):
        self._first_call = None
        self._vars = variables
        self._events = deque(maxlen=1000)

        self._current = None
        self._runtime = None

    def __enter__(self):
        ctime = time()
        if not self._first_call:
            self._first_call = ctime

        self._runtime = ctime
        self._current = current = Counter()

        for k, v in self._vars.items():
            current[k] = v()
        return current

    def __exit__(self, *args):
        self._events.append((self._runtime, time(), dict(self._current)))

    @property
    def stat(self):
        ctime = time()
        limits = tuple(i * 60.0 for i in self.Limits)

        deadline = ctime - max(limits)
        for head, tail, _ in tuple(self._events):
            if tail < deadline:
                self._events.popleft()
            elif head > deadline:
                break

        order = tuple(([], defaultdict(list),  i, ctime - i) for i in limits)
        for head, tail, data in self._events:
            for samples, metrics, _, deadline in order:
                if tail > deadline:
                    samples.append(tail - max(deadline, head))
                    for k, v in data.items():
                        if is_collection(v):
                            metrics[k].extend(v)
                        else:
                            metrics[k].append(v)

        result = []
        for samples, metrics, duration, _ in order:
            length = min(ctime - self._first_call, duration)

            data = {
                k: (median(v) if (k in self._vars) else sum(v) / length) if v else 0.0
                for k, v in metrics.items()}

            if 'load' not in data:
                data['load'] = sum(samples) / length
            result.append(data)

        return tuple(result)


class Partial:
    def __init__(self, *args, **kw):
        self._name  = kw.pop('name', None)
        self._value = None

        self.args = args
        self.kw   = kw
        self.calculated = False

    @cached_property
    def logger(self):
        from kalib.logging import Logging
        return Logging.get(self)

    @cached_property
    def head(self):
        try:
            return self.args[0]
        except IndexError:
            ...

    @cached_property
    def name(self):
        name = Who(self)
        if self._name:
            name = f'{name}.{self._name}'
        return name

    @cached_property
    def params(self):
        return f'(*{self.args}, **{self.kw})'

    @cached_property
    def value(self):
        if not self.calculated:
            msg = f'{Who(self)} never called'
            raise TypeError(msg)
        return self._value

    @property
    def result(self):
        if self.calculated:
            with suppress(RecursionError, TypeError):
                return self.value

    @cached_property
    def title(self):
        result = self.result
        result = f'={result}' if result else ''
        return f'{self.name}{self.params}{result}'

    def __len__(self):
        return len(self.args)

    def __repr__(self):
        return f'<{self.title} at 0x{id(self):x}>'


    def __call__(self, *args, **kw):
        if not self.calculated:
            title = f'{self.name}{self.params}(*{args}, **{kw})'
            try:
                if callable(self.head):
                    self._value = partial(*self.args, **self.kw)(*args, **kw)
                else:
                    args = (*self.args, *args)
                    if args:
                        self._value = args if len(args) > 1 else args[0]

            except Exception:
                self.log.error(title)  # noqa: TRY400
                raise

            self.calculated = True
        return self._value


def lazy_proxy_to(*mapping, getter=attrgetter, default=Nothing, pre=None):  # noqa: PLR0915
    if isinstance(mapping[-1], str):
        bind = pin

    elif mapping[-1] is None:
        bind, mapping = None, mapping[:-1]

    else:
        bind, mapping = mapping[-1], mapping[:-1]


    def binder(cls):  # noqa: PLR0915
        pivot, mapping_list = mapping[0], mapping[1:]

        if not is_class(cls):
            msg = f"{Who.Is(cls)} isn't a class"
            raise TypeError(msg)

        if (
            not mapping_list or
            (len(mapping_list) == 1 and not isinstance(mapping_list[0], str))
        ):
            raise ValueError(f'empty {mapping_list=} for {pivot=}')

        for method in mapping_list:

            if not method.startswith('_') and get_attr(cls, method):
                msg = (
                    f'{Who(cls)} already exists {method!a}: '
                    f'{get_attr(cls, method)}')
                raise TypeError(msg)

            def wrapper(method, node):
                if not isinstance(pivot, str):
                    try:
                        return getattr(pivot, method)
                    except AttributeError:
                        msg = (
                            f'{Who(node)}.{method} proxied -> '
                            f"{Who(pivot)}.{method}, but last isn't exists")
                        raise TypeError(msg)  # noqa: B904

                try:
                    entity = getattr(node, pivot)
                except AttributeError:
                    msg = (
                        f'{Who(node)}.{method} proxied -> '
                        f'{Who(node)}.{pivot}.{method}, but '
                        f"{Who(node)}.{pivot} isn't exists")
                    raise TypeError(msg)  # noqa: B904

                if entity is None:
                    name = Who(entity) if getter is attrgetter else pivot
                    msg = (
                        f'{Who(node)}.{method} proxied -> '
                        f'{Who(node)}.{name}.{method}, but current '
                        f'{Who(node)}.{name} is None')

                    if default is Nothing:
                        raise TypeError(msg)

                    msg = f'{msg}; return {Who.Is(default)}'
                    cls.log.warning(msg)
                    attribute = default

                else:
                    try:
                        attribute = getter(method)(entity)

                    except (AttributeError, KeyError) as e:
                        name = Who(entity) if getter is attrgetter else pivot
                        msg = (
                            f'{Who(node)}.{method} proxied -> '
                            f"{Who(node)}.{name}.{method}, but last isn't exists "
                            f"('{method}' not in {Who(node)}.{name})")

                        if default is Nothing:
                            raise class_of(e)(msg) from e

                        msg = f'{msg}; return {Who.Is(default)}'
                        cls.log.warning(msg)
                        attribute = default

                return partial(pre, attribute) if pre else attribute

            wrapper.__name__ = method
            wrapper.__qualname__ = f'{pivot}.{method}'

            if bind is None:
                node = cls.__dict__[pivot]
                try:
                    value = node.__dict__[method]
                except KeyError:
                    value = getattr(node, method)
            else:
                wrap = partial(wrapper, method)
                wrap.__name__ = method
                wrap.__qualname__ = f'{pivot}.{method}'
                value = bind(wrap)

            setattr(cls, method, value)

        return cls
    return binder


def incremental_delay(limit=None, deviation=None, function=exp):
    def wrapper(attempt, *args, **kw):
        result = function(attempt, *args, **kw)

        if deviation:
            bias = uniform(1.0 - deviation, 1.0 + deviation)  # noqa: S311
            result = uniform(result * bias, result / bias)  # ~5.54..9.85  # noqa: S311
        return float(limit if limit and result >= limit else result)
    return wrapper


def sourcefile(something, template=None):
    source = generic_sourcefile(something)
    if not source:
        return ''
    elif not template:
        return str(source)
    return ' ' + (template % source)


def to_tuple(x):
    return tuple(x or ()) if is_iterable(x) else (x,)


def toml_read(path):
    with Path(path).open('rb') as fd:
        return toml_load(fd)


def yaml_read(path):
    from kalib.importer import required

    with Path(path).open('rb') as fd:
        return required('yaml.safe_load')(fd.read())


def unique(*args, **kw):
    from kalib.logging import Logging
    Logging.Default.deprecate('unique() moved to kalib.internals', shift=-3)
    from kalib.internals import unique
    return unique(*args, **kw)


def cycler(array):
    """Return a function that cycles through the given array."""
    iterator = cycle(array)
    return lambda: next(iterator)


def shuffler(array):
    """Return a function that shuffles the given array."""
    array = list(array)
    shuffle(array)
    return cycler(tuple(array))
