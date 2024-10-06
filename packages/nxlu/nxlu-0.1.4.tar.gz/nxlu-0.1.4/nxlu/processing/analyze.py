import inspect
import logging
import random
import threading
import types
import warnings
from collections.abc import Callable
from typing import Any

import networkx as nx
import numpy as np
from sentence_transformers import SentenceTransformer

from nxlu.constants import ALGORITHM_SUBMODULES, CUSTOM_ALGORITHMS, GENERATORS_TO_DICT
from nxlu.utils.misc import cosine_similarity

warnings.filterwarnings("ignore")

random.seed(42)
rng = np.random.default_rng(seed=42)
logger = logging.getLogger("nxlu")


__all__ = [
    "map_algorithm_result",
    "get_algorithm_function",
    "apply_algorithm",
    "register_custom_algorithm",
    "GraphProperties",
    "filter_relevant_nodes",
]

_hits_lock = threading.Lock()


def map_algorithm_result(graph: nx.Graph, algorithm: str, result: Any) -> None:
    """Map the algorithm's result back to the graph's node, edge, or graph attributes.

    Parameters
    ----------
    graph : nx.Graph
        The graph to update.
    algorithm : str
        The name of the algorithm applied.
    result : Any
        The result returned by the algorithm.

    Returns
    -------
    None
    """
    if isinstance(result, dict):
        if all(graph.has_node(node) for node in result):
            for node, value in result.items():
                graph.nodes[node].setdefault("algorithm_results", {})[algorithm] = value
            logger.info(f"Mapped node attributes for algorithm '{algorithm}'.")
            return

        if all(isinstance(key, tuple) and graph.has_edge(*key) for key in result):
            for edge, value in result.items():
                for key in graph[edge[0]][edge[1]]:
                    graph.edges[edge[0], edge[1], key].setdefault(
                        "algorithm_results", {}
                    )[algorithm] = value
            logger.info(f"Mapped edge attributes for algorithm '{algorithm}'.")
            return

        graph.graph.setdefault("algorithm_results", {})[algorithm] = result
        logger.info(f"Mapped graph-level attribute for algorithm '{algorithm}'.")
        return

    if isinstance(result, list):
        if all(isinstance(item, tuple) and len(item) == 2 for item in result):
            for edge in result:
                if graph.has_edge(*edge):
                    for key in graph[edge[0]][edge[1]]:
                        graph.edges[edge[0], edge[1], key].setdefault(
                            "algorithm_results", {}
                        )[algorithm] = True
            logger.info(f"Mapped edge presence for algorithm '{algorithm}'.")
            return

        graph.graph.setdefault("algorithm_results", {})[algorithm] = result
        logger.info(
            f"Mapped list as graph-level attribute for algorithm '{algorithm}'."
        )
        return

    if isinstance(result, (int, float, str)):
        graph.graph.setdefault("algorithm_results", {})[algorithm] = result
        logger.info(f"Mapped scalar graph-level attribute for algorithm '{algorithm}'.")
        return

    logger.warning(
        f"Unhandled result type for algorithm '{algorithm}'. No mapping performed."
    )


def get_algorithm_function(algorithm_name: str) -> Callable:
    """Retrieve the appropriate algorithm function by name.

    Parameters
    ----------
    algorithm_name : str
        The name of the algorithm to retrieve.

    Returns
    -------
    Callable
        The function corresponding to the algorithm.

    Raises
    ------
    ValueError
        If the algorithm is not found in NetworkX or custom algorithms.
    """
    if algorithm_name in CUSTOM_ALGORITHMS:
        algorithm = CUSTOM_ALGORITHMS[algorithm_name]
        logger.debug(f"Found custom algorithm: {algorithm_name}")
    elif hasattr(nx.algorithms, algorithm_name):
        algorithm = getattr(nx.algorithms, algorithm_name)
        logger.debug(f"Found NetworkX algorithm: {algorithm_name}")
    else:
        for module in ALGORITHM_SUBMODULES:
            if hasattr(module, algorithm_name):
                algorithm = getattr(module, algorithm_name)
                logger.debug(
                    f"Found algorithm '{algorithm_name}' in submodule '"
                    f"{module.__name__}'."
                )
                break
        else:
            error_msg = f"Algorithm '{algorithm_name}' not found in NetworkX or custom "
            "algorithms."
            logger.error(error_msg)
            raise ValueError(error_msg)

    return algorithm


def analyze_relationships(graph: nx.Graph) -> str:
    """Generate a summary of all relationships within the graph, including edge weights.

    Parameters
    ----------
    graph : nx.Graph
        The NetworkX graph to analyze.

    Returns
    -------
    str
        A summary string of all relationships in the graph.
    """
    relationship_summary = "Graph Relationships:\n"
    for u, v, data in graph.edges(data=True):
        relation = data.get("relation", "EDGE")
        weight = data.get("weight", "N/A")
        relationship_summary += f"{u} -- {relation} (Weight: {weight}) --> {v}\n"
    return relationship_summary


def apply_algorithm(graph: nx.Graph, algorithm_name: str, **kwargs) -> Any:
    """Apply a NetworkX algorithm or a custom algorithm to the graph.

    Parameters
    ----------
    graph : nx.Graph
        The input graph.
    algorithm_name : str
        The name of the algorithm to apply.
    **kwargs : Additional keyword arguments for the algorithm.

    Returns
    -------
    Any
        The result of the algorithm.

    Raises
    ------
    ValueError
        If the algorithm is not found or an error occurs during application.
    """
    logger.info(f"Applying algorithm: {algorithm_name}")

    try:
        algorithm = get_algorithm_function(algorithm_name)
    except ValueError:
        logger.exception("Error getting algorithm function")
        raise

    try:
        sig = inspect.signature(algorithm)
        # set default for 'k' if not provided
        if "k" in sig.parameters and "k" not in kwargs:
            kwargs["k"] = 100
            logger.info("Parameter 'k' set to 100 by default.")

        # check and set default for 'weight'
        if "weight" in sig.parameters and "weight" not in kwargs:
            all_weights_numeric = all(
                isinstance(attrs.get("weight", 1.0), (int, float))
                for _, _, attrs in graph.edges(data=True)
            )
            if all_weights_numeric:
                kwargs["weight"] = "weight"
                logger.info("Parameter 'weight' set to 'weight'.")
            else:
                for u, v, attrs in graph.edges(data=True):
                    if "weight" not in attrs or not isinstance(
                        attrs["weight"], (int, float)
                    ):
                        graph.edges[u, v]["weight"] = 1.0
                kwargs["weight"] = "weight"
                logger.info("Assigned default weight of 1.0 for non-numeric edges.")
    except (ValueError, TypeError) as e:
        logger.warning(
            f"Could not inspect signature of '{algorithm_name}': {e}. Proceeding "
            f"without setting 'k' or 'weight'."
        )

    try:
        result = algorithm(graph, **kwargs)
        logger.info(f"Algorithm '{algorithm_name}' applied successfully.")
    except Exception as e:
        error_msg = f"Error applying algorithm '{algorithm_name}': {e!s}"
        logger.exception(error_msg)
        raise ValueError(error_msg)

    if algorithm_name in GENERATORS_TO_DICT:
        try:
            result = dict(result)
            logger.debug(f"Converted generator result of '{algorithm_name}' to dict.")
        except Exception as e:
            error_msg = f"Failed to convert generator result of '{algorithm_name}' to "
            f"dict: {e!s}"
            logger.exception(error_msg)
            raise ValueError(error_msg)
    elif isinstance(result, types.GeneratorType):
        result = list(result)
        logger.debug(f"Converted generator result of '{algorithm_name}' to list.")

    return result


def register_custom_algorithm(name: str, func: Callable) -> None:
    """Register a custom algorithm.

    Parameters
    ----------
    name : str
        The name of the custom algorithm.
    func : Callable
        The function implementing the custom algorithm.
    """
    CUSTOM_ALGORITHMS[name] = func


class GraphProperties:
    """A class to compute and store various properties of a NetworkX graph.

    This class provides a range of attributes describing the structural properties
    of a graph, such as whether it's connected, bipartite, weighted, or planar.
    It also includes methods for identifying hubs and authorities using the HITS
    algorithm.

    Attributes
    ----------
    graph : nx.Graph
        The input NetworkX graph.
    is_directed : bool
        Whether the graph is directed.
    num_nodes : int
        The number of nodes in the graph.
    num_edges : int
        The number of edges in the graph.
    density : float
        The density of the graph.
    is_strongly_connected : bool
        Whether the graph is strongly connected (only relevant for directed graphs).
    is_connected : bool
        Whether the graph is connected (weakly connected for directed graphs).
    is_bipartite : bool
        Whether the graph is bipartite.
    is_planar : bool
        Whether the graph is planar.
    is_tree : bool
        Whether the graph is a tree.
    has_edge_data : bool
        Whether the edges of the graph contain additional data.
    has_node_data : bool
        Whether the nodes of the graph contain additional data.
    is_multigraph : bool
        Whether the graph is a multigraph.
    is_weighted : bool
        Whether the graph is weighted.
    average_clustering : float
        The average clustering coefficient of the graph.
    degree_hist : list[int]
        The degree histogram of the graph.
    peak_degree : int or None
        The degree with the highest frequency in the graph, or None if no peak exists.
    hubs : list[str]
        List of influential hubs in the graph based on the HITS algorithm.
    authorities : list[str]
        List of influential authorities in the graph based on the HITS algorithm.

    Methods
    -------
    _identify_hits(G: nx.Graph, z_threshold: float = 1.5) -> tuple[list[str], list[str]]
    :
        Identify influential hubs and authorities in the graph using the HITS
        algorithm.
    _compute_peak_degree() -> int or None:
        Compute the peak degree of the graph based on the degree histogram.
    """

    def __init__(
        self,
        graph: nx.Graph,
        compute_peak_degree: bool = True,
        identify_hits: bool = True,
    ):
        """Initialize the GraphProperties object and computes various properties of the
        graph.

        Parameters
        ----------
        graph : nx.Graph
            The input NetworkX graph.
        compute_peak_degree : bool
            Compute the peak degree of the graph based on the degree histogram. Default
            is True
        identify_hits : bool
            Identify influential hubs and authorities in the graph using the HITS
            algorithm. Default is True.
        """
        self.graph = graph
        self.is_directed = graph.is_directed()
        self.num_nodes = graph.number_of_nodes()
        self.num_edges = graph.number_of_edges()
        self.density = nx.density(graph)
        self.is_strongly_connected = (
            nx.is_strongly_connected(graph) if self.is_directed else False
        )
        self.is_connected = (
            nx.is_connected(graph)
            if not self.is_directed
            else nx.is_weakly_connected(graph)
        )
        self.is_bipartite = (
            nx.is_bipartite(graph) if "bipartite" in graph.graph else False
        )
        self.is_planar = (
            nx.check_planarity(graph)[0] if "planar" in graph.graph else False
        )
        self.is_tree = nx.is_tree(graph) if "is_tree" in graph.graph else False
        self.has_edge_data = (
            any(graph.edges[edge] for edge in graph.edges())
            if "has_edge_data" in graph.graph
            else False
        )
        self.has_node_data = (
            any(graph.nodes[node] for node in graph.nodes())
            if "has_node_data" in graph.graph
            else False
        )
        self.is_multigraph = graph.is_multigraph()
        self.is_weighted = nx.is_weighted(graph)
        self.average_clustering = (
            nx.average_clustering(graph) if self.num_nodes > 0 else 0.0
        )
        self.degree_hist = nx.degree_histogram(graph) if self.num_nodes > 0 else []
        degrees = [d for n, d in graph.degree()]
        self.min_degree = min(degrees)
        self.max_degree = max(degrees)
        self.avg_degree = sum(degrees) / len(degrees)
        if compute_peak_degree:
            self.peak_degree = self._compute_peak_degree()
        if identify_hits:
            self.hubs, self.authorities = self._identify_hits(graph, z_threshold=2.5)

    @staticmethod
    def _identify_hits(
        G: nx.Graph, z_threshold: float = 1.5
    ) -> tuple[list[str], list[str]]:
        """Identify influential hubs and authorities in a graph using the HITS algorithm
        and dynamic z-score thresholding.

        Parameters
        ----------
        G : nx.Graph
            The input graph.
        z_threshold : float, optional
            Z-score threshold to identify outliers based on hub and authority scores,
            by default 1.5

        Returns
        -------
        Tuple[List[str], List[str]]
            A tuple containing two lists:
            - Hubs: List of nodes with hub scores beyond the z-score threshold.
            - Authorities: List of nodes with authority scores beyond the z-score
            threshold.
        """
        with _hits_lock:
            hits_hub_scores, hits_authority_scores = nx.hits(
                G, max_iter=50, normalized=True
            )

        hub_scores = np.array(list(hits_hub_scores.values()))
        authority_scores = np.array(list(hits_authority_scores.values()))

        mean_hub = np.mean(hub_scores)
        std_hub = np.std(hub_scores)

        mean_authority = np.mean(authority_scores)
        std_authority = np.std(authority_scores)

        hubs = [
            node
            for node, score in hits_hub_scores.items()
            if (score - mean_hub) / std_hub > z_threshold
        ]
        authorities = [
            node
            for node, score in hits_authority_scores.items()
            if (score - mean_authority) / std_authority > z_threshold
        ]

        logger.info(f"Hubs identified: {hubs}")
        logger.info(f"Authorities identified: {authorities}")

        return hubs, authorities

    def _compute_peak_degree(self):
        """Compute the peak degree in the graph based on the degree histogram.

        Returns
        -------
        int or None
            The degree with the highest frequency in the graph, or None if no peak
            exists.
        """
        if self.degree_hist:
            max_degree = max(self.degree_hist)
            return self.degree_hist.index(max_degree)
        return None


def filter_relevant_nodes(
    nodes: list[str], query: str, model: SentenceTransformer, z_threshold: float = 2.0
) -> list[str]:
    """Filter nodes based on their semantic relevance to the user's query using
    embeddings and z-score thresholding.

    Parameters
    ----------
    nodes : List[str]
        The list of node labels (hubs or authorities) to filter.
    query : str
        The user's query string.
    model : SentenceTransformer
        The sentence-transformer model used to generate embeddings.
    z_threshold : float, optional
        The z-score threshold for determining relevance, by default 2.0.

    Returns
    -------
    List[str]
        A list of nodes that are semantically relevant to the user's query.
    """
    if not nodes:
        return []

    query_embedding = model.encode([query])
    node_embeddings = model.encode(nodes)

    similarities = cosine_similarity(node_embeddings, query_embedding).flatten()

    mean_sim = np.mean(similarities)
    std_sim = np.std(similarities)
    if std_sim == 0:
        std_sim = 1e-10

    # dynamic threshold based on z-scores
    threshold = mean_sim + z_threshold * std_sim
    relevant_nodes = [
        node for node, sim in zip(nodes, similarities) if sim >= threshold
    ]

    logger.info(f"Filtered {len(relevant_nodes)} nodes as relevant to the query.")

    return relevant_nodes
