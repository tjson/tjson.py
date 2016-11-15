from lib2._tjson.datatype import NonScalar, Datatype


class Object(NonScalar):
    @staticmethod
    def tag():
        return "O"

    @staticmethod
    def convert(obj):
        if str(obj.__class__) != "<class '__main__.object'>":
            raise TypeError("expected TJSON::Object, got {}".format(obj))
        return obj

    @staticmethod
    def generate(obj):
        temp_dict = {}

        for key, val in obj.iteritems():

            if not isinstance(key, str):
                raise TypeError

            is_unicode = False if not isinstance(val, unicode) else True
            the_type = Datatype.identify_type(val, is_unicode)
            temp_dict[key + ":" + the_type.tag()] = the_type.generate(val)

        return temp_dict