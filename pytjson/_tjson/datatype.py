import re, datetime
from Helpers.freezable_list import FrozenDict
from pytjson.Exceptions import ParseError

class Datatype:
    # Initializer, will be overriden below
    TAGS = {}
    isScalar = re.compile(r'^[a-z0-9]*$')
    isBin = re.compile('^[01]{8}$')
    isOnlyNumbers = re.compile('^\-?(0|[1-9][0-9]*)$')
    isNonScalar = re.compile(r'^([A-Z][a-z0-9]*)\<(.*)\>$')

    @staticmethod
    def parse(tag):

        if not isinstance(tag, (str, unicode)):
            raise TypeError("expected String, got {}".format(type(tag)))

        if tag == "O":
            # Object
            return Datatype.TAGS[tag]

        elif Datatype.isNonScalar.match(tag):
            tmp_inner = Datatype.isNonScalar.match(tag).group(2)
            tmp_type = Datatype.isNonScalar.match(tag).group(1)
            inner = Datatype.parse(tmp_inner)
            if tmp_type == "A":
                tmp = Array(inner)
            else:
                tmp = Datatype.TAGS[tmp_type]
            return tmp

        elif Datatype.isScalar.match(tag):
            # Scalar
            return Datatype.TAGS[tag]
        else:
            raise ParseError("couldn't parse tag: {}".format(repr(tag)))

    @staticmethod
    def identify_type(obj, is_unicode):

        if type(obj) is dict:
            return Datatype.TAGS["O"]
        elif type(obj) is list:
            t = Array(None)
            return t._identify_type(obj)
        elif isinstance(obj, (str)):
            return Datatype.TAGS["s"]
        elif type(obj) is int:
            return Datatype.TAGS["i"]
        elif type(obj) is float:
            return Datatype.TAGS["f"]
        elif isinstance(obj, datetime.datetime):
            return Datatype.TAGS["t"]
        elif is_unicode:
            return Datatype.TAGS["b"]

        else:
            raise TypeError("don't know how to serialize #{obj.class} as TJSON")

    def datatype_generate(self, obj):
        is_unicode = False if not isinstance(obj, unicode) else True
        return self.identify_type(obj, is_unicode).generate(obj)


class Scalar(Datatype):
    @staticmethod
    def isScalar():
        return True


class NonScalar(Datatype):
    def __init__(self, inner_type):
        self.inner_type = inner_type

    @staticmethod
    def isScalar():
        return False


class Number(Scalar):
    pass


class Integer:
    @staticmethod
    def generate(int_data):
        # Integers are serialized as strings to sidestep the limits of some JSON parsers
        return str(int_data).encode("utf-8")


class Binary(Scalar):
    pass


from datatypes.string import String
from datatypes.timestamp import Timestamp
from datatypes.float import Float
from datatypes.integer import SignedInt, UnsignedInt
from datatypes.array import Array
from datatypes.binary import Binary16, Binary32, Binary64
from datatypes.object import Object


class Datatype(Datatype):
    Datatype.TAGS = FrozenDict(
        O = Object(None),
        b = Binary64(),
        b16 = Binary16(),
        b32 = Binary32(),
        b64 = Binary64(),
        f = Float(),
        i = SignedInt(),
        s =  String(),
        t = Timestamp(),
        u = UnsignedInt()
    )
