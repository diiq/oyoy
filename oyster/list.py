from oyster_object import OysterObject


class List(OysterObject):
    def __init__(self, items):
        self.items = items
        self.call = items[0]
        self.args = items[1:]

    def __str__(self):
        return "(%s)" % ", ".join([item.__str__() for item in self.items])

    def dup(self):
        return List(self.items)


##################################################################
# The following classes and constructors used during parsing only:


class PartialList(List):
    pass


def close_partial_lists(obj):
    if isinstance(obj, PartialList):
        return List(obj.items)
    return obj


def ensure_partial_list(obj):
    if not isinstance(obj, PartialList):
        return PartialList([obj])
    return obj


def enforce_list(obj):
    if isinstance(obj, PartialList):
        return List(obj.items)
    else:
        return List([obj])
