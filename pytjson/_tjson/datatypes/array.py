from pytjson._tjson.datatype import NonScalar, Datatype


class Array(NonScalar):
    # Determine the type of a Ruby array (for serialization)

    def __init__(self, inner_type):
        NonScalar.__init__(self, inner_type)
        self.inner_type = inner_type

    def _identify_type(self, array):

        self.inner_type = None

        for elem in array:
            is_unicode = False if not isinstance(elem, unicode) else True
            t = Datatype.identify_type(elem, is_unicode)
            self.inner_type = (self.inner_type if self.inner_type is not None else t)

            if self.inner_type.__class__ != t.__class__:
                raise TypeError("array contains heterogenous types: #{array.inspect}")

        return Array(self.inner_type)

    def tag(self):
        return "A<{}>".format(self.inner_type.tag())

    def convert(self, array):

        if type(array) is not list:
            raise

        for key, val in enumerate(array):
            array[key] = self.inner_type.convert(val)

        return array

    @staticmethod
    def generate(array):
        for key, val in enumerate(array):
            tmp = Datatype()
            array[key] = tmp.datatype_generate(val)

        return array
