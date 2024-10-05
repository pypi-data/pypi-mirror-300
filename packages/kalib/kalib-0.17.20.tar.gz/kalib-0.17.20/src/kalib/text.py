"""This module provides advanced string handling utilities, particularly
focused on character encoding detection, conversion, and manipulation. It
defines the `Str` class, which acts as a wrapper around string or bytes
objects, offering methods to handle various encoding scenarios and to
facilitate text processing.

- **Functions:**

  - `generate_offsets`**: Generates a sequence of offsets used for iterating
    over a string or bytes object in a specific pattern, which is useful for
    charset detection algorithms.

  - `replace_class_with_str`**: A helper function used to ensure that methods
    receive string arguments instead of `Str` instances, by converting the first
    argument if necessary.

  - `get_mime`**: Attempts to detect the MIME type of given data using the `magic`
    library, returning a dictionary with `type` and `text` keys.

- **Class `Str`**: A sophisticated string wrapper that provides:

    - **Encoding and Decoding**: Methods to convert between bytes and string
      representations, handling different character encodings.

    - **Charset Detection**: Automatically detects the character encoding of
      the input data using custom logic and the `charset_normalizer` library.

    - **Lazy Proxying**: Uses the `lazy_proxy_to` decorator to proxy common
      string methods to the underlying string representation, allowing `Str` instances
      to behave like regular strings.

    - **Attributes and Methods**:
        - `representation`: Returns the original object in its uncast form.

        - `mime`: Retrieves the MIME type of the data if possible.

        - `charset`: Determines the most likely character encoding of the data.

        - `bytes`: Returns the data as a bytes object.

        - `string`: Returns the data as a string object.

        - `tokenize`: Splits the string into tokens based on a regular expression
        pattern.

The module leverages several external utilities from the `kalib` library,
including descriptors, internal helpers, and miscellaneous functions. It also
utilizes standard libraries like `contextlib`, `math`, and `re` for additional
functionality.

Overall, this module enhances string handling by providing robust methods for
encoding detection and conversion, making it particularly useful in scenarios
where text data may come in various encodings or formats.
"""

from contextlib import suppress
from math import log2
from re import findall

from kalib._internal import to_ascii
from kalib.descriptors import pin
from kalib.internals import Who, unique
from kalib.misc import lazy_proxy_to


def generate_offsets(x):
    power = int(log2(x))

    yield 0
    for base in range(power):
        bias = (2 ** (power - base))
        for no in range(x // bias + 1):
            if no % 2:
                yield no * bias


def replace_class_with_str(method, *args, **kw):
    if args and isinstance(args[0], Str):
        args = (str(args[0]), *args[1:])
    return method(*args, **kw)


def get_mime(data):
    from kalib.importer import optional
    if (
        data and
        (read := optional('magic.from_buffer', quiet=False)) and
        (detect_from := optional('magic.detect_from_content'))
    ):
        return {'text': read(data), 'type': detect_from(data).mime_type}


@lazy_proxy_to(
    'string',
    '__add__', '__contains__', '__eq__', '__format__', '__hash__', '__ge__',
    '__getitem__', '__gt__', '__iter__', '__le__', '__len__', '__lt__', '__mod__',
    '__mul__', '__ne__', '__rmod__', '__rmul__', '__sizeof__', 'capitalize',
    'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find',
    'format', 'format_map', 'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal',
    'isdigit', 'isidentifier', 'islower', 'isnumeric', 'isprintable', 'isspace',
    'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans',
    'partition', 'removeprefix', 'removesuffix', 'replace', 'rfind', 'rindex',
    'rjust', 'rpartition', 'rsplit', 'rstrip', 'split', 'splitlines', 'startswith',
    'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill',
    pin, pre=replace_class_with_str,
)
class Str:
    INTERNAL_CHARSET = 'utf-8'
    CHARDET_MAX_READ = 2 ** 20

    to_ascii = staticmethod(to_ascii)

    @classmethod
    def uncast(cls, something):
        if isinstance(something, bytes | str):
            return something

        elif isinstance(something, int):
            return str(something)

        if isinstance(something, Exception):
            return f'{Who(something)}: {something}'

        else:
            msg = f"({Who(something)}) {something=} isn't valid bytes | str"
            raise TypeError(msg)

        return something

    @classmethod
    def to_bytes(cls, something, *args, **kw):
        return bytes(cls(something, *args, **kw))

    @classmethod
    def to_str(cls, something, *args, **kw):
        return str(cls(something, *args, **kw))


    def __init__(self, something, /, encoding=None):
        self._object = something
        self._encoding = encoding or self.INTERNAL_CHARSET


    @pin
    def representation(self):
        return self.uncast(self._object)

    @pin
    def mime(self):
        with suppress(ImportError):
            return get_mime(self.bytes)

    @pin
    def chardet(self):
        from kalib.importer import required
        with suppress(Exception):
            func = required('charset_normalizer.detect')
            return func(bytes(self))

    @pin
    def charset_probe_order(self):
        result = [self._encoding]
        if meta := self.chardet:
            result.append(meta['encoding'])
        return tuple(unique([*result, 'ascii']))

    @pin
    def charset(self):
        string = self.representation
        is_bytes = isinstance(string, bytes)

        def binary_iter(x):
            getter = x.__getitem__
            offset = len(x) - len(x) % 2 - 1
            if offset != -1:

                iterator = generate_offsets(offset)
                offsets = map(getter, iterator)
                if not is_bytes:
                    offsets = map(ord, offsets)
                yield from enumerate(offsets)

        limit = self.CHARDET_MAX_READ
        if not is_bytes and len(string) <= limit:
            limit = 0

        chars = []
        default = 'ascii'
        if not string:
            return default

        for no, char in binary_iter(string):
            if no > limit:
                break

            if char < 0x20:  # noqa: PLR2004
                if char in (0x9, 0xa, 0xc, 0xd):
                    continue
                return 'binary'

            if char >= 0x7f:  # noqa: PLR2004, ANSI Extended Border
                if is_bytes:
                    default = 'ansi'
                else:
                    chars.append(char)
                    if len(chars) > 2 ** 1024:
                        return self.charset_probe

        return default if is_bytes else self.charset_probe

    @pin
    def charset_probe(self):
        string = self.representation

        if isinstance(string, bytes):
            method = string.decode
            order = self.charset_probe_order

        else:
            method = string.encode
            order = tuple(reversed(self.charset_probe_order))

        for charset in filter(bool, order):
            try:
                method(charset)
                return charset  # noqa: TRY300

            except (UnicodeEncodeError, UnicodeDecodeError):
                ...


    @pin
    def bytes(self):
        string = self.representation
        return string if isinstance(string, bytes) else string.encode(self._encoding)

    @pin
    def string(self):
        string = self.representation
        if isinstance(string, str):
            return string

        if self.charset != 'binary':
            return string.decode(self.charset)

        msg = f"couldn't decode {string!r} ({string!a})"
        if meta := self.charset:
            msg = f'{msg}, meta: {meta}'
        raise ValueError(msg)


    def __bytes__(self):
        return self.bytes

    def __str__(self):
        return self.string

    def __repr__(self):
        string = self.representation
        size = f'{len(self.bytes):d}'

        length = ''
        charset = (f'{self.charset} '.upper()) if self.charset else ''

        if isinstance(string, str) and len(self.bytes) != len(self.string):
            length =f'={len(self.string):d}'

        return (
            f'<{charset}{Who(self, full=False)}'
            f'[{Who(self._object, full=False)}'
            f'({size})]{length} at {id(self):#x}>')


    def tokenize(self, regex=r'([\w\d]+)'):
        return findall(regex, self.string)
