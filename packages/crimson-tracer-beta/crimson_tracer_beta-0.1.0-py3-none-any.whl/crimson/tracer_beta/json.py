import json
from crimson.tracer_beta.node import TraceNode


def trace_node_encoder(node: TraceNode):
    return node.to_dict()


def dumps_node(root: TraceNode, indent=2):
    tree_json = json.dumps(root, default=trace_node_encoder, indent=indent)
    return tree_json
