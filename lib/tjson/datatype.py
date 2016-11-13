import inspect
import re, sys, base64
from lib.Exceptions import *
from datetime import datetime, tzinfo, timedelta
import dateutil.parser

class Datatype:

    # Initializer, will be overriden below
    TAGS = {}
    isScalar = re.compile(r'^[a-z0-9]*$')
    isBin = re.compile('^[01]{8}$')
    isOnlyNumbers = re.compile('^\-?(0|[1-9][0-9]*)$')

    @staticmethod
    def parse(tag):

        if not isinstance(tag, (str, unicode)):
            raise TypeError("expected String, got {}".format(type(tag)))

        if tag == "O":
            # Object
            return Datatype.TAGS[tag]
        elif Datatype.isScalar.match(tag):

            # Scalar
            return Datatype.TAGS[tag]



class Scalar(Datatype):
    @staticmethod
    def isScalar():
        return True


class NonScalar(Datatype):
    def __init__(self, inner_type):
        self.inner_type = inner_type

    @staticmethod
    def inspect():
        return "#<#{self.class}<#{@inner_type.inspect}>>"

    @staticmethod
    def isScalar():
        return False


class Number(Scalar):
    pass


class String(Scalar):

    def tag(self):
        return "s"

    def convert(self, str_data):
        if not isinstance(str_data, (str, unicode)):
            raise TypeError("expected String, got #{str.class}: #{str.inspect}")

        try:
            str_data.decode("utf-8")
        except UnicodeError:
            raise EncodingError("expected UTF-8, got #{str.encoding.inspect}")

        return str_data

    def generate(self, obj):
        return str(obj)


class simple_utc(tzinfo):
    def tzname(self):
        return "UTC"
    def utcoffset(self, dt):
        return timedelta(0)


class Timestamp(Scalar):

        @staticmethod
        def tag():
            return "t"

        @staticmethod
        def convert(str_data):
            if not isinstance(str_data, (str, unicode)):
                raise TypeError("expected String, got #{str.class}: #{str.inspect}")

            pattern = re.compile(r'^\d{4}-\d{2}-\d{2}[T]\d{2}:\d{2}:\d{2}Z$')
            if not pattern.match(str_data):
                raise ParseError("invalid timestamp: #{str.inspect}")

            return dateutil.parser.parse(str_data)

        @staticmethod
        def generate(timestamp):
            return datetime.utcfromtimestamp(timestamp).replace(tzinfo=simple_utc()).isoformat().split("+")[0] + "Z"


class Float(Number):
    @staticmethod
    def tag():
        return "f"

    @staticmethod
    def convert(float_num):
        if not isinstance(float_num, (int, long, float)):
            raise TypeError("expected Float, got #{float.class}")

        return float(float_num)

    @staticmethod
    def generate(float_num):
        return float(float_num)


class Integer:
    @staticmethod
    def generate(int_data):
        # Integers are serialized as strings to sidestep the limits of some JSON parsers
        str(int_data)


class SignedInt(Integer):
    @staticmethod
    def tag():
        return "i"

    @staticmethod
    def convert(str_data):
        print type(str_data)

        if type(str_data) is not str:
            raise TypeError("expected String, got {} : {}".format(type(str_data), repr(str_data)))

        if not Datatype.isOnlyNumbers.match(str_data):
            raise ParseError("invalid integer: {}".format(repr(str_data)))

        result = int(str_data, 10)
        if result > sys.maxint:
            raise ParseError, "oversized integer: {}".format(result)
        elif result < (-sys.maxint - 1):
            raise ParseError, "undersized integer: {}".format(result)

        return result


class UnsignedInt(Integer):
    @staticmethod
    def tag():
        return "u"

    @staticmethod
    def convert(str_data):

        if type(str_data) is not str:
            raise TypeError("expected String, got {} : {}".format(type(str_data), repr(str_data)))

        if not Datatype.isOnlyNumbers.match(str_data):
            raise ParseError("invalid integer: {}".format(repr(str_data)))

        result = int(str_data)

        if result > (sys.maxint + sys.maxint + 1):
            raise ParseError("oversized integer: {}".format(result))
        return result


class Array(NonScalar):
    # Determine the type of a Ruby array (for serialization)

    @staticmethod
    def identify_type(array):
        inner_type = None

        for elem in array:
            t = Datatype.identify_type(elem)
            inner_type = (inner_type if not None else t)
            if inner_type != t:
                raise TypeError("array contains heterogenous types: #{array.inspect}")

        return inner_type

    @staticmethod
    def tag():
        return "A<#{@inner_type.tag}>"


class Binary(Scalar):
    pass


class Binary16(Binary):

        @staticmethod
        def tag():
            return "b16"

        @staticmethod
        def convert(str_data):

            if not isinstance(str_data, (str, unicode)):
                raise TypeError("expected String, got #{str.class}: #{str.inspect}")

            if all(x.isupper() for x in str_data):
                raise ParseError("base16 must be lower case: {}".format(repr(str_data)))

            if all(x.islower() for x in str_data) and all(x.isdigit() for x in str_data):
                raise ParseError("invalid base16: {}".format(repr(str_data)))

            if "=" in str_data:
                raise ParseError("padding disallowed: {}".format(str_data))

            return base64.b16decode(str_data.upper())

        @staticmethod
        def generate(str_data):
            base64.b16encode(str_data).lower().replace("=", "")


class Binary32(Binary):

    @staticmethod
    def tag():
        return "b32"

    @staticmethod
    def convert(str_data):
        if not isinstance(str_data, (str, unicode)):
                raise TypeError("expected String, got {}: {}".format(type(str_data), str_data))

        if all(x.isupper() for x in str_data):
            raise ParseError("base32 must be lower case: {}".format(repr(str_data)))

        if "=" in str_data:
            raise ParseError("padding disallowed: {}".format(str_data))

        try:
            return base64.b32decode(str_data.upper())
        except:
            raise ParseError("invalid base32: {}".format(str_data))

    @staticmethod
    def generate(binary):
        return base64.b32encode(binary).lower().replace("=", "")


class Binary64(Binary):

    @staticmethod
    def tag():
        return "b64"

    @staticmethod
    def convert(str_data):

        if not isinstance(str_data, (str, unicode)):
            raise TypeError("expected String, got {}: {}".format(type(str_data), str_data))

        if "=" in str_data:
            raise ParseError("padding disallowed: {}".format(str_data))
        if "+" in str_data or "/" in str_data:
            raise ParseError("base64url only: {}".format(str_data))

        try:
            return base64.urlsafe_b64decode(str_data.encode("utf-8") + "==")
        except:
            raise ParseError("invalid base64url: {}".format(str_data))

    @staticmethod
    def generate(binary):
        base64.urlsafe_b64encode(binary).replace("=", "").encode("utf-8")


class Object(NonScalar):

    @staticmethod
    def tag(self):
        return "O"

    @staticmethod
    def convert(obj):
        if not inspect.isclass(obj):
            raise TypeError("expected TJSON::Object, got #{obj.class}")

        return obj

class Datatype(Datatype):

    Datatype.TAGS = {

        "O": "Object()",
        #"A": Array(),
        "b": Binary64(),
        "b16": Binary16(),
        "b32": Binary32(),
        "b64": Binary64(),
        "f": Float(),
        "i": SignedInt(),
        "s": String(),
        "t": Timestamp(),
        "u": UnsignedInt()
    }