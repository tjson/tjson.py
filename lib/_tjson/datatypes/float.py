from lib._tjson.datatype import Number


class Float(Number):
    @staticmethod
    def tag():
        return "f"

    @staticmethod
    def convert(float_num):
        if not isinstance(float_num, (int, long, float)):
            raise TypeError("expected Float, got {}")

        return float(float_num)

    @staticmethod
    def generate(float_num):
        return float(float_num)
