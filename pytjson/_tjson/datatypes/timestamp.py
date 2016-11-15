from datetime import tzinfo, timedelta
from pytjson._tjson.datatype import Scalar


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
        return timestamp.replace(tzinfo=Timestamp._simple_utc()).isoformat().split("+")[0] + "Z"

    class _simple_utc(tzinfo):
        def tzname(self):
            return "UTC"

        def utcoffset(self, dt):
            return timedelta(0)
