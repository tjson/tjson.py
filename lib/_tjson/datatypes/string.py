from lib._tjson.datatype import Scalar


class String(Scalar):
    @staticmethod
    def tag():
        return "s"

    @staticmethod
    def convert(str_data):
        if not isinstance(str_data, (str, unicode)):
            raise TypeError("expected String, got #{str.class}: #{str.inspect}")

        try:
            str_data.decode("utf-8")
        except UnicodeError:
            raise EncodingError("expected UTF-8, got #{str.encoding.inspect}")

        return str_data.encode("utf-8")

    @staticmethod
    def generate(obj):
        return str(obj).encode("utf-8")
