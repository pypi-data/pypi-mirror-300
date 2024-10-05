"""
base_graph module
"""

# from ..telemetry import log_graph_execution
from langgraph.graph import StateGraph


class BaseGraph:
    """
    BaseGraph manages the execution flow of a graph composed of interconnected nodes.

    Attributes:
        nodes (list): A dictionary mapping each node's name to its corresponding node instance.
        edges (list): A dictionary representing the directed edges of the graph where each
                      key-value pair corresponds to the from-node and to-node relationship.
        entry_point (str): The name of the entry point node from which the graph execution begins.

    Args:
        nodes (iterable): An iterable of node instances that will be part of the graph.
        edges (iterable): An iterable of tuples where each tuple represents a directed edge
                          in the graph, defined by a pair of nodes (from_node, to_node).
        entry_point (BaseNode): The node instance that represents the entry point of the graph.

    Raises:
        Warning: If the entry point node is not the first node in the list.

    Example:
        >>> BaseGraph(
        ...    nodes=[
        ...        fetch_node,
        ...        parse_node,
        ...        rag_node,
        ...        generate_answer_node,
        ...    ],
        ...    edges=[
        ...        (fetch_node, parse_node),
        ...        (parse_node, rag_node),
        ...        (rag_node, generate_answer_node)
        ...    ],
        ...    entry_point=fetch_node,
        ...    use_burr=True,
        ...    burr_config={"app_instance_id": "example-instance"}
        ... )
    """

    def create_graph(self) -> StateGraph:
        # self.graph =
        pass

    def compile(self):
        pass
