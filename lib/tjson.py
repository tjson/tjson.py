# -*- encoding: utf-8 -*-

import datetime, json, sys, re
from _tjson.datatype import Datatype
from Exceptions import EncodingError, ParseError

class tjson:

    re_name_check = re.compile(r"^(.*):([A-Za-z0-9\<]+[\>]*)$")

    class object(dict):
        def __init__(self, **kwargs):
            super(tjson.object, self).__init__(**kwargs)

    def object_decoder(self, obj):
            # print "--" , obj
            tmp = tjson.object()

            for key, val in obj.iteritems():

                # if key is not "b:i" or key is not "example:A<O>":
                #     return obj

                if not tjson.re_name_check.match(key):
                    raise ParseError("invalid tag: {}".format(key))

                name = tjson.re_name_check.match(key).group(1).encode("utf-8")
                tag = tjson.re_name_check.match(key).group(2).encode("utf-8")

                the_type = Datatype.parse(tag)
                # print "val : ",val, val[0].__class__
                tmp[name] = the_type.convert(val)
            # print tmp
            return tmp

    def parse(self, string):
        try:
            utf8_string = string.encode("utf-8")
        except:
            raise EncodingError("Encoding error.")

        if type(utf8_string) is not str:
            raise TypeError("Not a string error.")

        return json.loads(utf8_string, object_hook=self.object_decoder)

    def generate(self, dict_string):

        if type(dict_string) is not dict:
            raise TypeError
        tmp = Datatype()
        return tmp.datatype_generate(dict_string)