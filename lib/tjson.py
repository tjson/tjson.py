import json, sys, re
from tjson.datatype import Datatype
from Exceptions import *


class tjson:

    re_name_check = re.compile(r"^(.*):([A-Za-z0-9\<]+[\>]*)$")

    class Object(dict):
        def __init__(self, **kwargs):
            super(tjson.Object, self).__init__(**kwargs)

        def loads(self, json_string):
            if type(json_string) is not str:
                raise TypeError("Not a string error.")

            json.loads(json_string, object_hook=self.object_decoder)

        def object_decoder(self, obj):
            for key, val in obj.iteritems():

                if not tjson.re_name_check.match(key):
                    raise ParseError("invalid tag: {}".format(key))

                name = tjson.re_name_check.match(key).group(1)
                tag = tjson.re_name_check.match(key).group(2)

                the_type = Datatype.parse(tag)
                self.__setitem__(name, the_type.convert(val))
            return obj

    def parse(self, string):
        try:
            utf8_string = string.encode("utf-8")
        except:
            raise EncodingError("Encoding error.")

        object = self.Object()
        object.loads(utf8_string)
        return object

    def generate(self, dict_string):

        if type(dict_string) is not dict:
            raise TypeError
        tmp = Datatype()
        return tmp.datatype_generate(dict_string)


if __name__ == "__main__":

    s = tjson()
    print s.generate({"example": -520.0524})
