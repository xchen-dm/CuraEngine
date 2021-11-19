# GDB pretty printing support for CuraEngine

import gdb.printing
import gdb.types

class IntPointPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        x = self.val["X"]
        y = self.val["Y"]
        return f'[{x},{y}]'

    def display_hint(self):
        return "point"

class PathPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        cur_elem = self.val['_M_impl']['_M_start']
        end_elem = self.val['_M_impl']['_M_finish']
        x = []
        y = []
        while cur_elem != end_elem:
            point = cur_elem.dereference()
            x.append(str(point["X"]))
            y.append(str(point["Y"]))
            cur_elem = cur_elem + 1
        return "[" + ",".join(x) + "],[" + ",".join(y) + "]"

    def display_hint(self):
        return "array"

class PathsPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        cur_elem = self.val['_M_impl']['_M_start']
        end_elem = self.val['_M_impl']['_M_finish']
        points = []
        while cur_elem != end_elem:
            point = PathPrinter(cur_elem.dereference())
            points.append("[" + point.to_string() + "]")
            cur_elem = cur_elem + 1
        return "[" + ",".join(points) + "]"

    def display_hint(self):
        return "array"

class PolygonPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        paths = PathsPrinter(self.val["paths"])
        return paths.to_string()

    def display_hint(self):
        return "array"


class ListPolyItPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        p = self.val["it"]
        # TODO: take referenced polygon into account
        return str(p)


class ProximityPointLinkPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        a = self.val["a"]
        b = self.val["b"]
        dist = self.val["dist"]
        proximity_point_link_type = self.val["type"]
        return f"<a = {a}, b = {b}, dist = {dist}, type = {proximity_point_link_type}>"


class Point2LinkItemPrinter:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        first = self.val["first"]
        second = self.val["second"]
        return f"<first = {first}, second = {second}>"


def curaengine_lookup_function(val):
    basic_type = gdb.types.get_basic_type(val.type)
    name = str(basic_type)
    if name == "ClipperLib::IntPoint":
        return IntPointPrinter(val)
    if name.startswith("std::vector<ClipperLib::IntPoint,") and name.endswith(">"):
        return PathPrinter(val)
    if name.startswith("std::vector<std::vector<ClipperLib::IntPoint,") and name.endswith(">"):
        return PathsPrinter(val)
    if name == "cura::Polygons":
        return PolygonPrinter(val)
    # if name.startswith("std::pair<const ClipperLib::IntPoint, cura::ProximityPointLink") and name.endswith(">"):
    #     return Point2LinkItemPrinter(val)
    # if name == "const cura::ListPolyIt":
    #     return ListPolyItPrinter(val)
    # if name == "cura::ProximityPointLink":
    #     return ProximityPointLinkPrinter(val)


gdb.current_progspace().pretty_printers.append(curaengine_lookup_function)


class Plot(gdb.Command):
    def __init__(self):
        super(Plot, self).__init__("plot", gdb.COMMAND_OBSCURE)

    def invoke(self, args, from_tty):
        for arg in gdb.string_to_argv(args):
            data = gdb.parse_and_eval(arg)
            # plt.figure()
            # plt.plot([0, 10], [20, 30])
            # plt.show()
            print(data)

Plot()


