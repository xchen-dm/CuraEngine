import lldb


def __lldb_init_module(debugger, internal_dict):
    lldb.formatters.Logger._lldb_formatters_debug_level = 2
    logger = lldb.formatters.Logger.Logger()
    logger >> "curaengine lldb tools init"

    simpleValues = ['Temperature',
                    'Velocity',
                    'Acceleration',
                    'LayerIndex',
                    'AngleDegrees',
                    'Ratio']
    for sv in simpleValues:
        debugger.HandleCommand("type summary add -F {}.getSimpleValueSummary cura::{}".format(__name__, sv))

    debugger.HandleCommand("type summary add -F " + __name__ + ".PointSummary ClipperLib::IntPoint")
    debugger.HandleCommand("type summary add -F " + __name__ + ".PointSummary cura::Point")
    debugger.HandleCommand("type summary add -F " + __name__ + ".AABB3DSummary cura::AABB3D")
    debugger.HandleCommand("type summary add -F " + __name__ + ".ExtruderTrainSummary cura::ExtruderTrain")
    debugger.HandleCommand("type summary add -F " + __name__ + ".LayerPlanSummary cura::LayerPlan")
    debugger.HandleCommand("type summary add -F " + __name__ + ".PolygonsSummary cura::Polygons")
    debugger.HandleCommand("type summary add -F " + __name__ + ".WallToolPathsSummary cura::WallToolPaths")
    debugger.HandleCommand("type summary add -F " + __name__ + ".ExtrusionJunctionSummary cura::ExtrusionJunction")
    debugger.HandleCommand("type summary add -F " + __name__ + ".ExtrusionLineSummary cura::ExtrusionLine")
    debugger.HandleCommand("type summary add -F " + __name__ + ".BeadingSummary cura::BeadingStrategy::Beading")
    debugger.HandleCommand("type summary add -F " + __name__ + ".SkeletalTrapezoidationGraphSummary cura::SkeletalTrapezoidation::graph_t")
    debugger.HandleCommand("type summary add -F " + __name__ + ".voronoi_vertexSummary boost::polygon::voronoi_vertex<double>")
    debugger.HandleCommand("type summary add -F " + __name__ + ".TransitionMiddleSummary cura::SkeletalTrapezoidationEdge::TransitionMiddle")


def getSimpleValueSummary(value, internal_dict):
    return "{}".format(value.GetChildMemberWithName("value").GetValue())


def getAxisValues(value, axes='xyz'):
    return {
        axis: value.GetChildMemberWithName("x").GetValueAsSigned()
        for axis in axes
    }


def ExtrusionJunctionSummary(value, internal_dict):
    x =  value.GetChildMemberWithName("p").GetChildMemberWithName("X").GetValueAsSigned()
    y =  value.GetChildMemberWithName("p").GetChildMemberWithName("Y").GetValueAsSigned()
    w = value.GetChildMemberWithName("w").GetValueAsSigned()
    perimeter = value.GetChildMemberWithName("perimeter_index").GetValueAsSigned()
    region = value.GetChildMemberWithName("region_id").GetValueAsSigned()
    return f"{{'x': {x}, 'y': {y}, 'width': {w}, 'perimeter': {perimeter}, 'region': {region}}}"


def ExtrusionLineSummary(value, internal_dict):
    line = []
    for i in range(value.GetChildMemberWithName("junctions").GetNumChildren()):
        junction = value.GetChildMemberWithName("junctions").GetChildAtIndex(i)
        line.append(
            [junction.GetChildMemberWithName("p").GetChildMemberWithName("X").GetValueAsSigned(),
             junction.GetChildMemberWithName("p").GetChildMemberWithName("Y").GetValueAsSigned(),
             junction.GetChildMemberWithName("w").GetValueAsSigned()])
    return "{}".format(line)


def voronoi_vertexSummary(value, internal_dict):
    x = value.GetChildMemberWithName("x_").GetValueAsSigned()
    y = value.GetChildMemberWithName("y_").GetValueAsSigned()
    return f"{{'x': {x}, 'y': {y}}}"


def TransitionMiddleSummary(value, internal_dict):
    pos = value.GetChildMemberWithName("pos").GetValueAsSigned()
    lower_bead_count = value.GetChildMemberWithName("lower_bead_count").GetValueAsSigned()
    return f"{{'pos': {pos}, 'lower_bead_count': {lower_bead_count}}}"


def SkeletalTrapezoidationGraphSummary(value, internal_dict):
    ret = "{'edges': ["

    edges = value.GetChildMemberWithName("edges")
    no_edges = edges.GetNumChildren()

    for i in range(no_edges):
        edge = edges.GetChildAtIndex(i)
        from_node = edge.GetChildMemberWithName("from")
        from_x = from_node.GetChildMemberWithName("p").GetChildMemberWithName("X").GetValueAsSigned()
        from_y = from_node.GetChildMemberWithName("p").GetChildMemberWithName("Y").GetValueAsSigned()

        to_node = edge.GetChildMemberWithName("to")
        to_x = to_node.GetChildMemberWithName("p").GetChildMemberWithName("X").GetValueAsSigned()
        to_y = to_node.GetChildMemberWithName("p").GetChildMemberWithName("Y").GetValueAsSigned()

        data = edge.GetChildMemberWithName("data")
        is_central = data.GetChildMemberWithName("is_central").GetValueAsSigned()
        region = data.GetChildMemberWithName("region").GetValueAsUnsigned()
        ret += f"{{'from': [{from_x}, {from_y}], 'to': [{to_x}, {to_y}], 'is_central': {is_central}, 'region': {region} }},"

    ret = ret[:-1] + "], "
    ret += "'nodes': ["
    nodes = value.GetChildMemberWithName("nodes")
    no_nodes = nodes.GetNumChildren()

    for i in range(no_nodes):
        node = nodes.GetChildAtIndex(i)
        X = node.GetChildMemberWithName("p").GetChildMemberWithName("X").GetValueAsSigned()
        Y = node.GetChildMemberWithName("p").GetChildMemberWithName("Y").GetValueAsSigned()
        ret += f"[{X}, {Y}],"
    ret = ret[:-1] + "]}"
    return ret

def PointSummary(value, internal_dict):
    return "[{}, {}]".format(value.GetChildMemberWithName("X").GetValueAsSigned(),
                             value.GetChildMemberWithName("Y").GetValueAsSigned())


def AABB3DSummary(value, internal_dict):
    kwret = {}
    for bound in ['min', 'max']:
        axes = getAxisValues(value.GetChildMemberWithName(bound))
        kwret.update(dict(zip(['{}_{}'.format(k, bound) for k in axes.keys()], axes.values())))
    return "<{} = min[x: {x_min}, y: {y_min}, z: {z_min} ... max[x: {x_max}, y: {y_max}, z: {z_max}>".format(
        value.GetDisplayTypeName(), **kwret)


def ExtruderTrainSummary(value, internal_dict):
    return "nr = {}".format(value.GetChildMemberWithName("extruder_nr").GetValueAsUnsigned())


def LayerPlanSummary(value, internal_dict):
    # todo: make better
    return "<{} nr = {}>".format(value.GetDisplayTypeName(),
                                 value.GetChildMemberWithName("layer_nr").GetChildMemberWithName(
                                     "value").GetValueAsSigned())


def PolygonsSummary(value, internal_dict):
    paths = value.GetChildMemberWithName("paths")
    summary = ""
    if paths is None:
        return
    for i in range(paths.GetNumChildren()):
        path = paths.GetChildAtIndex(i)
        if path is None:
            return
        polypath = []
        for j in range(path.GetNumChildren()):
            line = path.GetChildAtIndex(j)
            if line is None:
                return
            polypath.append([line.GetChildMemberWithName("X").GetValueAsSigned(),
                             line.GetChildMemberWithName("Y").GetValueAsSigned()])
        summary += "{}, ".format(polypath)
    return "[{}]".format(summary[:-2])


def WallToolPathsSummary(value, internal_dict):
    return "<{} = no walls: {} with a width of 0th: {}, xth: {}, strategy type: {}>".format(value.GetDisplayTypeName(),
                                                                                            value.GetChildMemberWithName(
                                                                                                "inset_count").GetValueAsSigned(),
                                                                                            value.GetChildMemberWithName(
                                                                                                "bead_width_0").GetValueAsSigned(),
                                                                                            value.GetChildMemberWithName(
                                                                                                "bead_width_x").GetValueAsSigned(),
                                                                                            value.GetChildMemberWithName(
                                                                                                "strategy_type"))


def BeadingSummary(value, internal_dict):
    ret = {}
    ret["total_thickness"] = value.GetChildMemberWithName("total_thickness").GetValueAsSigned()
    ret["widths"] = []
    widths = value.GetChildMemberWithName("bead_widths")
    for i in range(widths.GetNumChildren()):
        ret["widths"].append(widths.GetChildAtIndex(i).GetValueAsSigned())
    ret["locations"] = []
    locations = value.GetChildMemberWithName("toolpath_locations")
    for i in range(widths.GetNumChildren()):
        ret["locations"].append(locations.GetChildAtIndex(i).GetValueAsSigned())
    return str(ret)
