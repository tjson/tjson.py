from lib._tjson.datatype import NonScalar, Datatype


class Object(NonScalar):
    @staticmethod
    def tag():
        return "O"

    @staticmethod
    def convert(obj):
        if str(obj.__class__) != "<class '__main__.object'>":
            raise TypeError("expected tjson.object, got {}".format(obj))
        return obj

    @staticmethod
    def generate(obj):
        new_generated_dict = {}

        for key, val in obj.iteritems():
            if not isinstance(key, str):
                raise TypeError

            is_unicode = False if not isinstance(val, unicode) else True
            the_type = Datatype.identify_type(val, is_unicode)
            new_generated_dict[key + ":" + the_type.tag()] = the_type.generate(val)

        return new_generated_dict