import sys

from lib.Exceptions import ParseError
from lib._tjson.datatype import Integer, Datatype


class SignedInt(Integer):
    @staticmethod
    def tag():
        return "i"

    @staticmethod
    def convert(str_data):
        str_data = str_data.encode("utf-8")
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

