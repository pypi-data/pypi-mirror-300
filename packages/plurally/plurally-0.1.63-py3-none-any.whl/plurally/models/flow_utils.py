import networkx as nx

from plurally.models.node import Node
from plurally.models.subflow import Subflow
from plurally.models.utils import is_list_type


def get_annots_or_raise(node, handle, schema):
    if handle not in schema.model_fields:
        raise ValueError(
            f"Handle {handle} not found in node {node}, options are {list(schema.model_fields)}"
        )
    return schema.model_fields[handle]


def connect_nodes(
    graph, src_node: Node, src_handle: str, tgt_node: Node, tgt_handle: str
):
    if src_node is tgt_node:
        raise ValueError(f"Cannot connect node with itself: {src_node}")

    for node in (src_node, tgt_node):
        if node not in graph:
            raise ValueError(
                f"{node} was not added to {graph} before connecting"
                f" {src_handle} to {tgt_handle}"
            )

    get_annots_or_raise(src_node, src_handle, src_node.OutputSchema)
    inputs_annots = get_annots_or_raise(tgt_node, tgt_handle, tgt_node.InputSchema)

    # if tgt_handle is not a list and there already is a connection it is False
    if not is_list_type(inputs_annots):
        for src, tgt, key in graph.in_edges(tgt_node, data=True):
            if key["tgt_handle"] == tgt_handle:
                raise ValueError(
                    f"Node {tgt_node.name} already has a connection for {tgt_handle}"
                )

    if not tgt_node.validate_connection(src_node, src_handle, tgt_handle):
        raise ValueError(f"Connection between {src_node} and {tgt_node} is invalid")

    key = f"{src_handle}###{tgt_handle}"
    if (src_node, tgt_node, key) in graph.edges:
        raise ValueError(
            f"Connection between {src_node} and {tgt_node} with {src_handle=} and {tgt_handle=} already exists"
        )

    graph.add_edge(
        src_node,
        tgt_node,
        src_handle=src_handle,
        tgt_handle=tgt_handle,
        key=key,
    )


def disconnect_all_nodes_connected_to(graph, node_id: str, mode: str = "all"):
    to_remove = []

    for src_node, tgt_node, key in graph.edges:
        src_handle, tgt_handle = key.split("###")
        is_src = src_node.node_id == node_id or node_id in src_handle
        is_tgt = tgt_node.node_id == node_id or node_id in tgt_handle

        if mode == "all":
            if is_src or is_tgt:
                to_remove.append((src_node, tgt_node, key))
        elif mode == "input" and is_tgt:
            to_remove.append((src_node, tgt_node, key))
        elif mode == "output" and is_src:
            to_remove.append((src_node, tgt_node, key))

        if isinstance(src_node, Subflow):
            disconnect_all_nodes_connected_to(src_node.graph, node_id, mode)
        if isinstance(tgt_node, Subflow):
            disconnect_all_nodes_connected_to(tgt_node.graph, node_id, mode)

    for src_node, tgt_node, key in to_remove:
        graph.remove_edge(src_node, tgt_node, key=key)


def get_flatten_graph(in_graph):
    out_graph = nx.MultiDiGraph()
    edges = set()
    for node in in_graph.nodes:
        if isinstance(node, Subflow):
            out_graph = nx.compose(out_graph, node.graph)
        else:
            out_graph.add_node(node)

    for src, tgt, data in in_graph.edges(data=True):
        tgt_handle = data["tgt_handle"]
        src_handle = data["src_handle"]

        if isinstance(src, Subflow):
            src_id, src_handle = src_handle.split(".")
            src = src.get_node(src_id)

        if isinstance(tgt, Subflow):
            if "." in tgt_handle:
                tgt_id, tgt_handle = tgt_handle.split(".")
                tgt = tgt.get_node(tgt_id)
            else:
                assert tgt_handle == "run"
                # add virtual edges to each subnode.run handle
                for subnode in tgt.graph.nodes:
                    edges.add((src, src_handle, subnode, "run"))
                # do not add the one to the run handle of subflow
                # because subflow won't be in flatten graph
                continue
        edges.add((src, src_handle, tgt, tgt_handle))

    # we could skip checks here and make things faster if necessary
    for src, src_handle, tgt, tgt_handle in edges:
        connect_nodes(
            out_graph,
            src,
            src_handle,
            tgt,
            tgt_handle,
        )
    return out_graph
