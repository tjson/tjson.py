import base64
from pytjson.Exceptions import ParseError
from pytjson._tjson.datatype import Binary


class Binary16(Binary):
    @staticmethod
    def tag():
        return "b16"

    @staticmethod
    def convert(str_data):

        if not isinstance(str_data, (str, unicode)):
            raise TypeError("expected String, got {}: {}".format(type(str_data), repr(str_data)))

        if all(x.isupper() for x in str_data):
            raise ParseError("base16 must be lower case: {}".format(repr(str_data)))

        if all(x.islower() for x in str_data) and all(x.isdigit() for x in str_data):
            raise ParseError("invalid base16: {}".format(repr(str_data)))

        if "=" in str_data:
            raise ParseError("padding disallowed: {}".format(str_data))

        return base64.b16decode(str_data.upper())

    @staticmethod
    def generate(str_data):
        return base64.b16encode(str_data).lower().replace("=", "").encode("ascii")


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
        return base64.b32encode(binary).lower().replace("=", "").encode("ascii")


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
        return base64.urlsafe_b64encode(binary).replace("=", "").encode("ascii")
