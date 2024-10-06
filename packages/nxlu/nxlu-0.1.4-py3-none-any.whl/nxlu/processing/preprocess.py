import logging
import warnings
from typing import Any

import networkx as nx
import numpy as np
from pydantic import BaseModel, Field, field_validator
from scipy.spatial import cKDTree

from nxlu.config import RescalingMethod

warnings.filterwarnings("ignore")


logger = logging.getLogger("nxlu")


__all__ = [
    "SubgraphSelectionConfig",
    "GraphThresholdingConfig",
    "GraphRescalingConfig",
    "CleanGraphConfig",
    "SubgraphSelection",
    "GraphThresholding",
    "GraphRescaling",
    "CleanGraph",
    "remove_self_loops",
    "symmetrize_graph",
    "is_symmetric",
    "copy_node_attributes",
    "copy_edge_attributes",
    "create_subgraph",
    "assign_default_weights",
]


class SubgraphSelectionConfig(BaseModel):
    """Configuration for selecting subgraphs.

    Attributes
    ----------
    defragment : bool
        Whether to defragment the graph by removing isolated nodes.
    prune_components : bool
        Whether to prune small connected components.
    min_nodes : Optional[int]
        Minimum number of nodes in connected components to retain (used with
        prune_components).
    hubness : Optional[str]
        Method to define important nodes ('betweenness', 'eigenvector', 'richclub').
    sd_cutoff : Optional[int]
        Number of standard deviations for selecting important nodes.
    use_lcc : bool
        Whether to retain the largest connected component.
    """

    defragment: bool = Field(False, description="Whether to defragment the graph.")
    prune_components: bool = Field(
        False, description="Whether to prune small components."
    )
    min_nodes: int | None = Field(
        None, description="Minimum nodes for component pruning."
    )
    hubness: str | None = Field(
        None,
        description="Method to select important nodes ('betweenness', 'eigenvector', "
        "'richclub').",
    )
    sd_cutoff: int | None = Field(
        1, description="Standard deviation cutoff for selecting important nodes."
    )
    use_lcc: bool = Field(
        False, description="Whether to use the largest connected component."
    )


class GraphThresholdingConfig(BaseModel):
    method: str = Field(
        ...,
        description="Thresholding method ('absolute', 'proportional', 'MST')",
        pattern="^(absolute|proportional|MST)$",
    )
    value: float | None = Field(
        None,
        gt=0,
        description="Threshold value (absolute/proportional). Required if method is "
        "'absolute' or 'proportional'.",
    )
    min_span_tree: bool = Field(
        False, description="Use Minimum Spanning Tree for thresholding"
    )
    dens_thresh: bool = Field(False, description="Use density-based thresholding")

    @field_validator("value")
    @classmethod
    def check_value_required(cls, v, info):
        method = info.data.get("method")
        if method in ["absolute", "proportional"] and v is None:
            raise ValueError("Value is required for absolute and proportional methods.")
        return v


class GraphRescalingConfig(BaseModel):
    """Configuration for rescaling graph adjacency matrices, including normalization,
    standardization, and conversion of weights to distances.

    Attributes
    ----------
    method : str
        The rescaling method to apply ('normalize', 'standardize', 'invert', "
        "'binarize').
    """

    method: RescalingMethod = Field(
        ...,
        description="Rescaling method ('normalize', 'standardize', 'invert', "
        "'binarize').",
    )


class CleanGraphConfig(BaseModel):
    force_symmetry: bool = Field(True, description="Force symmetry in the graph")
    remove_self_loops: bool = Field(True, description="Remove self-loops in the graph")
    threshold: GraphThresholdingConfig | None = Field(
        None, description="Threshold configuration"
    )
    subgraph: SubgraphSelectionConfig | None = Field(
        None, description="Subgraph selection configuration"
    )
    rescale: GraphRescalingConfig | None = Field(
        None, description="Rescaling configuration"
    )


class SubgraphSelection:
    """A class that handles the selection of subgraphs, including defragmentation, hub
    selection, component pruning, and extraction of the largest connected component.

    The class provides methods to apply various graph selection techniques to prune
    isolated nodes, remove small components, select important nodes (hubs) based on
    centrality metrics, and extract the largest connected component.

    Parameters
    ----------
    config : SubgraphSelectionConfig
        Configuration object that contains the settings for subgraph selection,
        such as whether to defragment, prune small components, use hub selection,
        or extract the largest connected component.

    Methods
    -------
    apply(G)
        Apply the subgraph selection based on the provided configuration.
    defragment(G)
        Remove isolated nodes (degree 0) from the graph.
    prune_small_components(G, min_nodes)
        Prunes components that have fewer than the specified minimum number of nodes.
    lcc(G)
        Extract the largest connected component of the graph.
    hub_selection(G, method="betweenness", sd=1)
        Select and retains hubs (important nodes) in the graph based on a specified
        centrality measure.
    """

    def __init__(self, config: SubgraphSelectionConfig):
        self.config = config

    def apply(self, G: nx.Graph) -> nx.Graph:
        """Apply subgraph selection based on the configuration.

        Parameters
        ----------
        G : nx.Graph
            The input graph.

        Returns
        -------
        nx.Graph
            The graph after subgraph selection is applied. Depending on the
            configuration, this may include defragmentation (removal of isolated
            nodes), pruning of small components, hub selection, and extraction of the
            largest connected component.
        """
        if self.config.defragment:
            G, _ = self.defragment(G)
        if self.config.prune_components and self.config.min_nodes is not None:
            G = self.prune_small_components(G, self.config.min_nodes)
        if self.config.hubness:
            G = self.hub_selection(
                G, method=self.config.hubness, sd=self.config.sd_cutoff
            )
        if self.config.use_lcc:
            G = self.lcc(G)
        return G

    @staticmethod
    def defragment(G: nx.Graph) -> tuple[nx.Graph, list]:
        """Remove isolated nodes (degree 0) from the graph.

        Parameters
        ----------
        G : nx.Graph
            The input graph.

        Returns
        -------
        tuple[nx.Graph, list]
            A tuple containing the defragmented graph (with isolated nodes removed) and
            a list of the removed nodes.
        """
        G_tmp = G.copy()
        isolates = [n for (n, d) in G_tmp.degree() if d == 0]
        pruned_nodes = []
        for node in isolates:
            G_tmp.remove_node(node)
            pruned_nodes.append(node)
        return G_tmp, pruned_nodes

    @staticmethod
    def prune_small_components(G: nx.Graph, min_nodes: int) -> nx.Graph:
        """Prunes components that have fewer than the specified minimum number of nodes.

        Parameters
        ----------
        G : nx.Graph
            The input graph.
        min_nodes : int
            The minimum number of nodes a component must have to be retained.

        Returns
        -------
        nx.Graph
            The pruned graph, containing only components that have at least the
            specified number of nodes. If no components meet the minimum size
            requirement, an empty graph is returned.
        """
        G_tmp = G.copy()
        components = list(nx.connected_components(G_tmp))
        components.sort(key=len, reverse=True)
        good_components = [comp for comp in components if len(comp) >= min_nodes]

        if not good_components:
            # Handle the case where no components meet the requirement
            return (
                nx.Graph()
            )  # Return an empty graph or leave the original graph untouched

        return nx.compose_all([nx.subgraph(G_tmp, comp) for comp in good_components])

    def lcc(self, G):
        """Extract the largest connected component (LCC) of the graph.

        Parameters
        ----------
        G : nx.Graph
            The input graph.

        Returns
        -------
        nx.Graph
            A subgraph containing the largest connected component. If the input graph
            has no nodes, it returns the input graph.
        """
        if G.number_of_nodes() == 0:
            return G  # Return empty graph if there are no nodes
        return G.subgraph(sorted(nx.connected_components(G), key=len, reverse=True)[0])

    @classmethod
    def hub_selection(
        cls, G: nx.Graph, method: str = "betweenness", sd: int = 1
    ) -> nx.Graph:
        """Select hubs (important nodes) in the graph based on a centrality measure and
        retains only those with centrality values above a certain threshold.

        Parameters
        ----------
        G : nx.Graph
            The input graph.
        method : str, optional
            The centrality measure to use for hub selection. Options include
            "betweenness", "eigenvector", and "richclub". Default is "betweenness".
        sd : int, optional
            The number of standard deviations below the mean centrality value
            to use as the threshold for removing nodes. Default is 1.

        Returns
        -------
        nx.Graph
            The graph after hub selection is applied. Nodes with centrality values
            below the threshold are removed.
        """
        try:
            if method == "eigenvector":
                ranking = nx.eigenvector_centrality(G, weight="weight").items()
            elif method == "richclub" and len(G.nodes()) > 4:
                ranking = nx.rich_club_coefficient(G, seed=42, Q=100).items()
            else:
                ranking = nx.betweenness_centrality(G, weight="weight").items()

            r = [x[1] for x in ranking]
            m = sum(r) / len(r) - sd * np.std(r)
            Gt = G.copy()
            for k, v in ranking:
                if v < m:
                    Gt.remove_node(k)

            return SubgraphSelection.defragment(Gt)[0]
        except Exception:
            logger.warning("Hub selection failed. Returning original graph.")
            return G


class GraphThresholding:
    """
    Apply various thresholding techniques to an adjacency matrix.

    This class provides methods to apply thresholding techniques such as
    absolute thresholding, proportional thresholding, and minimum spanning tree (MST)
    thresholding to a given adjacency matrix.

    Parameters
    ----------
    config : GraphThresholdingConfig
        Configuration specifying the thresholding method and associated parameters.

    Methods
    -------
    apply(matrix)
        Apply the specified thresholding method to the input adjacency matrix.
    local_thresholding_prop(matrix, thr)
        Apply proportional thresholding to the matrix, retaining a fraction of edges.
    local_thresholding_mst(matrix)
        Apply minimum spanning tree (MST) thresholding to the matrix, preserving the
        minimum set of edges that maintain graph connectivity.
    local_thresholding_abs(matrix, thr)
        Apply absolute thresholding, removing edges below a certain weight.
    """

    def __init__(self, config: GraphThresholdingConfig):
        """
        Initialize the GraphThresholding instance with the specified configuration.

        Parameters
        ----------
        config : GraphThresholdingConfig
            Configuration containing the thresholding method and threshold value.
        """
        self.config = config

    def apply(self, matrix: np.ndarray) -> np.ndarray:
        """
        Apply the selected thresholding method to the input adjacency matrix.

        Depending on the thresholding method specified in the configuration,
        the method applies either proportional, absolute, or MST thresholding to
        the adjacency matrix.

        Parameters
        ----------
        matrix : np.ndarray
            The adjacency matrix representing the graph to be thresholded.

        Returns
        -------
        np.ndarray
            The thresholded adjacency matrix.

        Raises
        ------
        ValueError
            If the specified thresholding method is not recognized.
        """
        if self.config.method == "proportional":
            return self.local_thresholding_prop(matrix, self.config.value)
        if self.config.method == "absolute":
            return self.local_thresholding_abs(matrix, self.config.value)
        if self.config.method == "MST":
            return self.local_thresholding_mst(matrix)
        raise ValueError(f"Unknown thresholding method: {self.config.method}")

    @staticmethod
    def local_thresholding_prop(matrix: np.ndarray, thr: float) -> np.ndarray:
        """
        Apply proportional thresholding to the adjacency matrix.

        Retain a proportion of the edges with the highest weights, based on the
        specified threshold value. This method ensures that only the top `thr` fraction
        of edges (by weight) are preserved.

        Parameters
        ----------
        matrix : np.ndarray
            The adjacency matrix representing the graph.
        thr : float
            The proportion of edges to retain, with `thr` between 0 and 1.

        Returns
        -------
        np.ndarray
            The thresholded adjacency matrix with only the top `thr` fraction of edges.

        Raises
        ------
        ValueError
            If the threshold value (`thr`) is not provided or is None.
        """
        conn_matrix = np.nan_to_num(matrix)
        if thr is None:
            raise ValueError(
                "Threshold value 'thr' must be provided for proportional thresholding."
            )

        # Number of edges to keep
        num_edges = int(
            np.count_nonzero(conn_matrix) / 2 * thr
        )  # Divide by 2 for undirected graph
        num_edges = max(num_edges, 1)

        # Get all edge weights
        n = conn_matrix.shape[0]
        edges = [
            (i, j, conn_matrix[i, j])
            for i in range(n)
            for j in range(i + 1, n)
            if conn_matrix[i, j] > 0
        ]

        # Sort edges by weight descending
        edges_sorted = sorted(edges, key=lambda x: x[2], reverse=True)

        # Keep top 'num_edges' edges
        top_edges = edges_sorted[:num_edges]

        # Create a new adjacency matrix
        thresholded_matrix = np.zeros_like(conn_matrix)
        for i, j, w in top_edges:
            thresholded_matrix[i, j] = w
            thresholded_matrix[j, i] = w  # Ensure symmetry

        return thresholded_matrix

    @staticmethod
    def local_thresholding_mst(matrix: np.ndarray) -> np.ndarray:
        """
        Apply minimum spanning tree (MST) thresholding to the adjacency matrix.

        Retain the minimum number of edges necessary to maintain the graph's
        connectivity. For disconnected graphs, MSTs are computed for each connected
        component.

        Parameters
        ----------
        matrix : np.ndarray
            The adjacency matrix representing the graph.

        Returns
        -------
        np.ndarray
            The thresholded adjacency matrix representing the MST.
        """
        conn_matrix = np.nan_to_num(matrix)
        G = nx.from_numpy_array(np.abs(conn_matrix))  # Updated function
        if not nx.is_connected(G):
            # Compute MST for each connected component
            mst = nx.Graph()
            for component in nx.connected_components(G):
                subgraph = G.subgraph(component)
                mst_sub = nx.minimum_spanning_tree(subgraph)
                mst = nx.compose(mst, mst_sub)
        else:
            mst = nx.minimum_spanning_tree(G)

        # Create adjacency matrix from MST
        mst_matrix = nx.to_numpy_array(mst)
        return mst_matrix

    @staticmethod
    def local_thresholding_abs(matrix: np.ndarray, thr: float) -> np.ndarray:
        """
        Apply absolute thresholding to the adjacency matrix.

        Retain edges whose weights are greater than or equal to the specified
        threshold value.

        Parameters
        ----------
        matrix : np.ndarray
            The adjacency matrix representing the graph.
        thr : float
            The threshold value. Edges with weights below this value will be removed.

        Returns
        -------
        np.ndarray
            The thresholded adjacency matrix with edges below the threshold removed.
        """
        conn_matrix = np.nan_to_num(matrix)
        thresholded_matrix = np.where(conn_matrix >= thr, conn_matrix, 0)
        return thresholded_matrix


class GraphRescaling:
    """A class to handle graph rescaling operations, including normalization,
    standardization, and conversion of weights to distances.

    This class provides methods for transforming weighted adjacency matrices by applying
    various rescaling techniques such as normalization, standardization, inverting
    weights, and binarization. These transformations are useful for preparing graphs
    for analysis, especially when edge weights need to be standardized or converted to
    distances.

    Parameters
    ----------
    config : GraphRescalingConfig
        Configuration object that specifies the rescaling method to be applied.

    Methods
    -------
    apply(matrix: np.ndarray) -> np.ndarray
        Apply the selected rescaling method based on the configuration.
    normalize(matrix: np.ndarray) -> np.ndarray
        Normalizes the matrix by its maximum edge weight.
    standardize(matrix: np.ndarray) -> np.ndarray
        Standardizes the matrix to the range [0, 1].
    invert(matrix: np.ndarray, copy: bool = False) -> np.ndarray
        Inverts the weights in the matrix to represent distances.
    binarize(matrix: np.ndarray, copy: bool = True) -> np.ndarray
        Binarizes the matrix by setting all non-zero elements to 1.
    _weight_conversion(W: np.ndarray, wcm: str) -> np.ndarray
        Convert the input weighted connection matrix based on the specified method.
    create_length_matrix(matrix: np.ndarray) -> tuple[np.ndarray, nx.Graph]
        Create a length matrix by inverting the weights and converting the matrix to a
        NetworkX graph.
    """

    def __init__(self, config):
        """Initialize the GraphRescaling object with a configuration.

        Parameters
        ----------
        config : GraphRescalingConfig
            Configuration object specifying the rescaling method.
        """
        self.config = config

    def apply(self, matrix: np.ndarray) -> np.ndarray:
        """Apply the selected rescaling method based on the configuration.

        Parameters
        ----------
        matrix : np.ndarray
            Weighted adjacency matrix to be rescaled.

        Returns
        -------
        np.ndarray
            The rescaled adjacency matrix after applying the selected method.
        """
        if self.config.method == "normalize":
            return self.normalize(matrix)
        if self.config.method == "standardize":
            return self.standardize(matrix)
        if self.config.method == "invert":
            return self.invert(matrix)
        if self.config.method == "binarize":
            return self.binarize(matrix)
        raise ValueError(f"Unknown rescaling method: {self.config.method}")

    @staticmethod
    def normalize(matrix: np.ndarray) -> np.ndarray:
        """Normalize the matrix by its maximum edge weight.

        Parameters
        ----------
        matrix : np.ndarray
            Weighted adjacency matrix to be normalized.

        Returns
        -------
        np.ndarray
            The normalized matrix where weights are divided by the maximum weight.
        """
        matrix = matrix.copy()
        max_val = np.max(np.abs(matrix))
        return matrix / max_val if max_val > 1e-12 else matrix

    @staticmethod
    def standardize(matrix: np.ndarray) -> np.ndarray:
        """Standardize the matrix to the range [0, 1].

        Parameters
        ----------
        matrix : np.ndarray
            Weighted adjacency matrix to be standardized.

        Returns
        -------
        np.ndarray
            The standardized matrix where weights are scaled to the range [0, 1].
        """
        matrix = matrix.copy()
        min_val, max_val = np.min(matrix), np.max(matrix)
        if max_val - min_val > 1e-12:
            return (matrix - min_val) / (max_val - min_val)
        return matrix

    @staticmethod
    def invert(matrix: np.ndarray) -> np.ndarray:
        """Invert the weights in the matrix to represent distances.

        Parameters
        ----------
        matrix : np.ndarray
            Weighted adjacency matrix where non-zero weights are inverted.

        Returns
        -------
        np.ndarray
            The matrix with inverted weights where non-zero weights are replaced by
            their reciprocals.
        """
        matrix = matrix.copy()
        matrix[matrix != 0] = 1.0 / np.clip(matrix[matrix != 0], 1e-12, None)
        matrix[np.isinf(matrix)] = 0
        return matrix

    @staticmethod
    def binarize(matrix: np.ndarray) -> np.ndarray:
        """Binarize the matrix by setting all non-zero elements to 1.

        Parameters
        ----------
        matrix : np.ndarray
            Weighted adjacency matrix to be binarized.

        Returns
        -------
        np.ndarray
            The binarized matrix where all non-zero weights are set to 1.
        """
        matrix = matrix.copy()
        matrix[matrix != 0] = 1
        return matrix

    @classmethod
    def _weight_conversion(cls, W: np.ndarray, wcm: str):
        """Convert the input weighted connection matrix based on the specified method.

        Parameters
        ----------
        W : np.ndarray
            Weighted connection matrix.
        wcm : str
            The conversion method. Either 'binarize' to binarize the matrix or
            'lengths' to convert weights to distances.

        Returns
        -------
        np.ndarray
            The converted connection matrix.
        """
        if wcm == "binarize":
            return cls.binarize(W)
        if wcm == "lengths":
            return cls.invert(W)

    @classmethod
    def create_length_matrix(cls, matrix):
        """Create a length matrix by inverting the weights and converting the matrix to
        a NetworkX graph.

        Parameters
        ----------
        matrix : np.ndarray
            Weighted adjacency matrix to be converted.

        Returns
        -------
        tuple[np.ndarray, nx.Graph]
            The inverted adjacency matrix and the corresponding NetworkX graph.
        """
        in_mat_len = cls._weight_conversion(matrix, "lengths")

        # Load numpy matrix as networkx graph
        G_len = nx.from_numpy_array(in_mat_len)
        return in_mat_len, G_len


class CleanGraph:
    """A Class for preprocessing graphs with configurable options using Pydantic.

    This class handles various preprocessing steps such as rescaling, thresholding,
    subgraph selection, and node/edge attribute copying. The graph is processed based
    on the provided configuration.

    Attributes
    ----------
    config : CleanGraphConfig
        Configuration object for the graph processing.
    G : nx.Graph
        NetworkX graph instance provided as input.
    in_mat : np.ndarray
        Adjacency matrix of the graph.
    in_mat_raw : np.ndarray
        Raw adjacency matrix without any preprocessing.

    Methods
    -------
    clean() -> nx.Graph
        Cleans and processes the graph based on the provided configuration.
    rescale(in_mat: np.ndarray) -> np.ndarray
        Rescales the graph based on the selected method from the configuration.
    apply_thresholding(in_mat: np.ndarray) -> np.ndarray
        Thresholds the graph based on the selected thresholding method.
    apply_subgraph_selection(G: nx.Graph) -> nx.Graph
        Select subgraphs of the graph based on the selected method.
    knn_graph(k: int) -> nx.Graph
        Create a k-nearest neighbor graph from the adjacency matrix.
    length_matrix() -> tuple[np.ndarray, nx.Graph]
        Generates a length matrix by converting edge weights to distances.

    Notes
    -----
    This class uses Pydantic configurations to handle preprocessing operations
    on a graph, such as removing self-loops, selecting subgraphs, and handling
    node and edge attributes. It supports rescaling and thresholding the adjacency
    matrix before converting it back to a graph structure.
    """

    def __init__(self, G: nx.Graph, config: CleanGraphConfig):
        """Initialize the CleanGraph object with a graph and configuration.

        Parameters
        ----------
        G : nx.Graph
            The input NetworkX graph to be processed.
        config : CleanGraphConfig
            Configuration object for graph cleaning and processing.
        """
        self.G = G
        self.config = config
        self.in_mat_raw = nx.to_numpy_array(G)
        logger.info("Preprocessing -- Filling any NaN, Inf, and diagonal with 0...")
        self.in_mat = self._autofix(self.in_mat_raw)

    @staticmethod
    def _autofix(matrix: np.ndarray) -> np.ndarray:
        """Fix NaN, Inf, and diagonal issues in the adjacency matrix.

        Parameters
        ----------
        matrix : np.ndarray
            The adjacency matrix to be fixed.

        Returns
        -------
        np.ndarray
            The fixed adjacency matrix with NaN and Inf values replaced by 0.
        """
        np.fill_diagonal(matrix, 0)
        matrix[np.isinf(matrix)] = 0
        matrix[np.isnan(matrix)] = 0
        return matrix

    def rescale(self, in_mat):
        """Rescales the graph based on the configuration.

        Parameters
        ----------
        in_mat : np.ndarray
            Adjacency matrix of the graph to be rescaled.

        Returns
        -------
        np.ndarray
            The rescaled adjacency matrix.
        """
        if self.config.rescale:
            logger.info(
                f"Preprocessing -- Rescaling graph according to: {self.config.rescale}"
            )
            rescaler = GraphRescaling(self.config.rescale)
            return rescaler.apply(in_mat)
        return in_mat

    def apply_thresholding(self, in_mat) -> np.ndarray:
        """Apply thresholding to the graph based on the configuration.

        Parameters
        ----------
        in_mat : np.ndarray
            The adjacency matrix to be thresholded.

        Returns
        -------
        np.ndarray
            The thresholded adjacency matrix.
        """
        if self.config.threshold:
            logger.info(
                f"Preprocessing -- Thresholding graph according to: "
                f"{self.config.threshold}"
            )
            thresholder = GraphThresholding(self.config.threshold)
            return thresholder.apply(in_mat)
        return in_mat

    def apply_subgraph_selection(self, G) -> nx.Graph:
        """Select subgraphs based on the configuration.

        Parameters
        ----------
        G : nx.Graph
            The input graph for subgraph selection.

        Returns
        -------
        nx.Graph
            The graph after subgraph selection is applied.
        """
        if self.config.subgraph and self.config.subgraph.use_lcc:
            logger.info(
                f"Preprocessing -- Selecting subgraph according to "
                f"{self.config.subgraph}"
            )
            subgraph_selector = SubgraphSelection(self.config.subgraph)
            return subgraph_selector.apply(G)
        return G

    def clean(self) -> nx.Graph:
        """Process and clean the graph based on the provided configuration.

        Steps include rescaling, thresholding, and selecting subgraphs. After
        processing, the node and edge attributes from the original graph are copied
        back to the final processed graph.

        Returns
        -------
        nx.Graph
            The cleaned and processed graph.
        """
        H = self.G.copy()

        try:
            # Step 1: Rescale
            self.in_mat = self.rescale(self.in_mat_raw)
            logger.info("Rescaling completed successfully.")
        except Exception:
            logger.exception("Error during rescaling. Skipping this step.")

        try:
            # Step 2: Apply thresholding
            self.in_mat = self.apply_thresholding(self.in_mat)
            logger.info("Thresholding applied successfully.")
        except Exception:
            logger.exception("Error during thresholding. Skipping this step.")

        # Step 3: Convert matrix back to graph
        H = nx.from_numpy_array(self.in_mat, create_using=type(self.G))
        logger.info(
            f"Converted NumPy array back to graph with {H.number_of_nodes()} nodes "
            f"and {H.number_of_edges()} edges."
        )

        # Step 4: Relabel nodes
        nodelist = list(self.G.nodes())
        if len(nodelist) != H.number_of_nodes():
            logger.warning(
                "Mismatch between number of nodes in original graph and NumPy "
                "array. Skipping relabeling."
            )
        else:
            mapping = {i: nodelist[i] for i in range(len(nodelist))}
            H = nx.relabel_nodes(H, mapping)
            logger.info("Relabeled nodes to preserve original node identifiers.")

        try:
            # Step 5: Symmetry handling
            if self.config.force_symmetry and not is_symmetric(H):
                logger.info("Preprocessing -- Symmetrizing...")
                H = symmetrize_graph(H)
        except Exception:
            logger.exception("Error during symmetrization. Skipping this step.")

        try:
            # Step 6: Loop handling
            if self.config.remove_self_loops and nx.number_of_selfloops(H) > 0:
                logger.info("Preprocessing -- Removing Self-Loops...")
                H = remove_self_loops(H)
        except Exception:
            logger.exception("Error removing self-loops. Skipping this step.")

        try:
            # Step 7: Apply subgraph selection
            H = self.apply_subgraph_selection(H)
        except Exception:
            logger.exception("Error during subgraph selection. Skipping this step.")

        # Step 8: Re-attach original node and edge attributes
        copy_edge_attributes(self.G, H)
        copy_node_attributes(self.G, H)
        logger.info("Copied node and edge attributes from source graph to subgraph.")

        return H

    @staticmethod
    def _knn(conn_matrix: np.ndarray, k: int) -> nx.Graph:
        """
        Create a mutual k-nearest neighbor graph using scipy's cKDTree.

        Parameters
        ----------
        conn_matrix : np.ndarray
            The adjacency matrix representing similarities between nodes.
        k : int
            Number of nearest neighbors to consider for each node.

        Returns
        -------
        nx.Graph
            The mutual k-nearest neighbor graph.
        """
        # similarity -> distance
        max_similarity = np.max(conn_matrix)
        if max_similarity == 0:
            distance_matrix = np.full(conn_matrix.shape, 1e10)
        else:
            distance_matrix = max_similarity - conn_matrix
        np.fill_diagonal(distance_matrix, 0)  # Ensure zero distance for self-loops

        distance_matrix[distance_matrix == max_similarity] = 1e10

        kdtree = cKDTree(distance_matrix)
        _, indices = kdtree.query(
            distance_matrix, k=k + 1
        )  # +1 to exclude the self-loop

        knn_dict = {i: set(neighbors[1:]) for i, neighbors in enumerate(indices)}

        mutual_knn_edges = set()
        for i in knn_dict:
            for j in knn_dict[i]:
                if i < j and i in knn_dict[j]:
                    mutual_knn_edges.add((i, j))

        gra = nx.Graph()
        gra.add_nodes_from(range(conn_matrix.shape[0]))
        gra.add_edges_from(mutual_knn_edges)

        return gra

    def knn_graph(self, k: int) -> nx.Graph:
        """Create a k-nearest neighbor graph from the adjacency matrix.

        Parameters
        ----------
        k : int
            Number of nearest neighbors to consider for each node.

        Returns
        -------
        nx.Graph
            The k-nearest neighbor graph.
        """
        return self._knn(self.in_mat, k)

    @property
    def length_matrix(self):
        """Create a length matrix by converting weights to distances.

        Returns
        -------
        tuple[np.ndarray, nx.Graph]
            A tuple containing the length matrix and the corresponding NetworkX graph.
        """
        return self.rescaler.create_length_matrix(self.in_mat)


def remove_self_loops(graph: nx.Graph) -> None:
    """Remove all self-loop edges from the given NetworkX graph.

    Parameters
    ----------
    G : nx.Graph
        The graph from which to remove self-loops.

    Returns
    -------
    None
    """
    if graph.is_multigraph():
        # For MultiGraphs, remove all self-loop edges including their keys
        self_loops = list(graph.selfloop_edges(keys=True))
        logger.info(f"Found {len(self_loops)} self-loop(s) in the MultiGraph.")
        graph.remove_edges_from(self_loops)
    else:
        # For simple Graphs, remove all self-loop edges directly
        self_loops = list(nx.selfloop_edges(graph))
        logger.info(f"Found {len(self_loops)} self-loop(s) in the Graph.")
        graph.remove_edges_from(self_loops)


def symmetrize_graph(graph: nx.DiGraph, method: str = "avg") -> nx.Graph:
    """Force symmetry upon a directed NetworkX graph by creating an undirected
    symmetrized graph.

    Parameters
    ----------
    G : nx.Graph
        The input graph.
    method : str
        Method for symmetrizing the graph. Options are `avg`, `triu`, `or `tril`.

    Returns
    -------
    G : nx.Graph
        The graph with symmetry enforced.
    """
    if not isinstance(graph, (nx.DiGraph, nx.MultiDiGraph)):
        raise TypeError(
            "symmetrize_graph function requires a directed graph (DiGraph or "
            "MultiDiGraph)."
        )

    if method not in ["avg", "triu", "tril"]:
        raise ValueError("Method must be one of 'avg', 'triu', 'tril'.")

    sym_graph = nx.Graph()
    processed_pairs = set()
    nodelist = list(graph.nodes())  # Preserve node order
    for u in nodelist:
        for v in graph.successors(u):
            if u == v:
                continue  # Skip self-loops; handle separately if needed

            # Sort the node pair to avoid duplicate processing
            pair = tuple(sorted([u, v]))
            if pair in processed_pairs:
                continue  # Already processed this pair
            processed_pairs.add(pair)

            has_uv = graph.has_edge(u, v)
            has_vu = graph.has_edge(v, u)

            # Handle based on the symmetrization method
            if method == "avg":
                if has_uv and has_vu:
                    if graph.is_multigraph():
                        # Average over all reciprocal edge weights
                        weights_uv = [
                            d.get("weight", 1)
                            for _, d in graph.get_edge_data(u, v).items()
                        ]
                        weights_vu = [
                            d.get("weight", 1)
                            for _, d in graph.get_edge_data(v, u).items()
                        ]
                        avg_weight = (
                            sum(weights_uv) / len(weights_uv)
                            + sum(weights_vu) / len(weights_vu)
                        ) / 2
                    else:
                        # Single edge in each direction
                        weight_uv = graph[u][v].get("weight", 1)
                        weight_vu = graph[v][u].get("weight", 1)
                        avg_weight = (weight_uv + weight_vu) / 2
                    sym_graph.add_edge(u, v, weight=avg_weight)
                    logger.debug(f"Averaged weight for ({u}, {v}): {avg_weight}")
                elif has_uv:
                    if graph.is_multigraph():
                        weights_uv = [
                            d.get("weight", 1)
                            for _, d in graph.get_edge_data(u, v).items()
                        ]
                        avg_weight = sum(weights_uv) / len(weights_uv)
                    else:
                        avg_weight = graph[u][v].get("weight", 1)
                    sym_graph.add_edge(u, v, weight=avg_weight)
                    logger.debug(f"Copied weight for ({u}, {v}): {avg_weight}")
                elif has_vu:
                    if graph.is_multigraph():
                        weights_vu = [
                            d.get("weight", 1)
                            for _, d in graph.get_edge_data(v, u).items()
                        ]
                        avg_weight = sum(weights_vu) / len(weights_vu)
                    else:
                        avg_weight = graph[v][u].get("weight", 1)
                    sym_graph.add_edge(u, v, weight=avg_weight)
                    logger.debug(f"Copied weight for ({u}, {v}): {avg_weight}")

            elif method in ["triu", "tril"]:
                if has_uv and has_vu:
                    if graph.is_multigraph():
                        weights_uv = [
                            d.get("weight", 1)
                            for _, d in graph.get_edge_data(u, v).items()
                        ]
                        weights_vu = [
                            d.get("weight", 1)
                            for _, d in graph.get_edge_data(v, u).items()
                        ]
                        avg_weight = (sum(weights_uv) + sum(weights_vu)) / (
                            len(weights_uv) + len(weights_vu)
                        )
                    else:
                        weight_uv = graph[u][v].get("weight", 1)
                        weight_vu = graph[v][u].get("weight", 1)
                        avg_weight = (weight_uv + weight_vu) / 2
                    sym_graph.add_edge(u, v, weight=avg_weight)
                    logger.debug(f"Added edge ({u}, {v}) with weight {avg_weight}")
                elif has_uv:
                    if graph.is_multigraph():
                        weights_uv = [
                            d.get("weight", 1)
                            for _, d in graph.get_edge_data(u, v).items()
                        ]
                        avg_weight = sum(weights_uv) / len(weights_uv)
                    else:
                        avg_weight = graph[u][v].get("weight", 1)
                    sym_graph.add_edge(u, v, weight=avg_weight)
                    logger.debug(f"Added edge ({u}, {v}) with weight {avg_weight}")
                elif has_vu:
                    if graph.is_multigraph():
                        weights_vu = [
                            d.get("weight", 1)
                            for _, d in graph.get_edge_data(v, u).items()
                        ]
                        avg_weight = sum(weights_vu) / len(weights_vu)
                    else:
                        avg_weight = graph[v][u].get("weight", 1)
                    sym_graph.add_edge(u, v, weight=avg_weight)
                    logger.debug(f"Added edge ({u}, {v}) with weight {avg_weight}")

    return sym_graph


def is_symmetric(graph: nx.DiGraph) -> bool:
    """Check if a directed NetworkX graph is symmetric. A graph is symmetric if for
    every edge (u, v, data), there exists an edge (v, u, data).

    Parameters
    ----------
    G : nx.Graph
        The input graph.

    Returns
    -------
    bool
        True if the graph is symmetric, False otherwise.
    """
    if not isinstance(graph, (nx.DiGraph, nx.MultiDiGraph)):
        logger.info("Undirected graphs are inherently symmetric.")
        return True  # Undirected graphs are symmetric by definition

    # Iterate over all edges in the graph
    for u, v, data in graph.edges(data=True):
        if not graph.has_edge(v, u):
            logger.debug(f"Missing reciprocal edge for ({u}, {v}).")
            return False  # Missing reciprocal edge

        if isinstance(graph, nx.DiGraph):
            # For simple DiGraph, compare edge data directly
            reciprocal_data = graph.get_edge_data(v, u)
            if reciprocal_data != data:
                logger.debug(f"Edge data mismatch for ({u}, {v}) and ({v}, {u}).")
                return False  # Edge data does not match

        elif isinstance(graph, nx.MultiDiGraph):
            # For MultiDiGraph, ensure that for each edge from u to v,
            # there's a corresponding edge from v to u with the same data
            # This accounts for multiple parallel edges
            reciprocal_edges = graph.get_edge_data(v, u)
            if not reciprocal_edges:
                logger.debug(f"No reciprocal edges found for ({u}, {v}).")
                return False  # No reciprocal edges found

            # Collect all edge attribute dictionaries for (u, v)
            uv_edge_attrs = [attr for key, attr in graph.get_edge_data(u, v).items()]

            # Collect all edge attribute dictionaries for (v, u)
            vu_edge_attrs = [attr for key, attr in graph.get_edge_data(v, u).items()]

            # Check that each (u, v) edge has a matching (v, u) edge
            for uv_attr in uv_edge_attrs:
                if uv_attr not in vu_edge_attrs:
                    logger.debug(
                        f"No matching edge data for {uv_attr} in reciprocal ({v}, {u})."
                    )
                    return False  # No matching reciprocal edge data found

    logger.info("The graph is symmetric.")
    return True  # All edges have matching reciprocals


def copy_node_attributes(source_graph: nx.Graph, target_graph: nx.Graph) -> None:
    """Copy node attributes from the source graph to the target graph for nodes present
    in both graphs.

    Parameters
    ----------
    source_graph : nx.Graph
        The original graph containing node attributes.
    target_graph : nx.Graph
        The subgraph to receive node attributes.
    """
    common_nodes = set(target_graph.nodes()).intersection(source_graph.nodes())
    node_attrs = {node: source_graph.nodes[node] for node in common_nodes}

    nx.set_node_attributes(target_graph, node_attrs)
    logger.debug(
        f"Copied attributes for {len(node_attrs)} nodes from source to target graph."
    )


def copy_edge_attributes(source_graph: nx.Graph, target_graph: nx.Graph) -> None:
    """Copy edge attributes from the source graph to the target graph for edges present
    in both graphs.

    Parameters
    ----------
    source_graph : nx.Graph
        The original graph containing edge attributes.
    target_graph : nx.Graph
        The subgraph to receive edge attributes.
    """
    edge_attrs = {}

    if isinstance(source_graph, (nx.MultiGraph, nx.MultiDiGraph)):
        # For MultiGraphs, include the key in the edge tuple
        for u, v, key in target_graph.edges(keys=True):
            if source_graph.has_edge(u, v, key):
                edge_attrs[(u, v, key)] = source_graph.edges[u, v, key]
    else:
        # For simple graphs, use (u, v) tuples
        for u, v in target_graph.edges():
            if source_graph.has_edge(u, v):
                edge_attrs[(u, v)] = source_graph.edges[u, v]

    nx.set_edge_attributes(target_graph, edge_attrs)
    logger.debug(
        f"Copied attributes for {len(edge_attrs)} edges from source to target graph."
    )


def create_subgraph(
    source_graph: nx.Graph,
    node_subset: list[Any] | None = None,
    edge_subset: list[tuple[Any, ...]] | None = None,
) -> nx.Graph:
    """Create a subgraph from the source graph containing only the specified subset of
    nodes, edges, or both. If both node_subset and edge_subset are provided, the
    function will ensure all relevant nodes and edges are included.

    Parameters
    ----------
    source_graph : nx.Graph
        The original graph from which to create the subgraph.
    node_subset : List[Any], optional
        The list of nodes to include in the subgraph. If not provided, the subgraph will
        be based solely on edge_subset.
    edge_subset : List[Tuple[Any, ...]], optional
        The list of edges (tuples of node pairs, possibly with keys) to include in the
        subgraph. If not provided, the subgraph will be based solely on node_subset.

    Returns
    -------
    nx.Graph
        The resulting subgraph containing only the specified nodes and/or edges.
    """
    if node_subset is None and edge_subset is None:
        raise ValueError("At least one of node_subset or edge_subset must be provided.")

    subgraph_nodes = set()

    # Handle node subset
    if node_subset:
        existing_nodes = [node for node in node_subset if source_graph.has_node(node)]
        missing_nodes = set(node_subset) - set(existing_nodes)

        if missing_nodes:
            logger.warning(
                f"The following nodes were not found in the source graph and will be "
                f"excluded: {missing_nodes}"
            )

        subgraph_nodes.update(existing_nodes)

    valid_edges = []

    # Handle edge subset
    if edge_subset:
        for edge in edge_subset:
            if len(edge) == 2:  # Case for standard Graph with (u, v)
                u, v = edge
                if source_graph.has_edge(u, v):
                    valid_edges.append((u, v))
                    subgraph_nodes.add(u)
                    subgraph_nodes.add(v)
                else:
                    logger.warning(
                        f"Edge ({u}, {v}) not found in the source graph and will be "
                        f"excluded."
                    )

            elif len(edge) == 3:  # Case for MultiGraph with (u, v, key)
                u, v, key = edge
                if source_graph.has_edge(u, v, key=key):
                    valid_edges.append((u, v, key))
                    subgraph_nodes.add(u)
                    subgraph_nodes.add(v)
                else:
                    logger.warning(
                        f"Edge ({u}, {v}, {key}) not found in the source graph and will"
                        f"be excluded."
                    )

            elif len(edge) == 4:  # Case for MultiGraph with (u, v, key, data)
                u, v, key, data = edge
                if source_graph.has_edge(u, v, key=key):
                    valid_edges.append((u, v, key, data))
                    subgraph_nodes.add(u)
                    subgraph_nodes.add(v)
                else:
                    logger.warning(
                        f"Edge ({u}, {v}, {key}, {data}) not found in the source graph "
                        f"and will be excluded."
                    )

            else:
                logger.error(
                    f"Edge tuple {edge} has an unsupported number of elements."
                )

    # Create the subgraph
    subgraph = source_graph.subgraph(subgraph_nodes).copy()

    # Handle edges for the subgraph
    if edge_subset:
        subgraph.remove_edges_from(list(subgraph.edges()))  # Remove any existing edges
        subgraph.add_edges_from(valid_edges)  # Add the valid edges

    logger.info(
        f"Created subgraph with {subgraph.number_of_nodes()} nodes and "
        f"{subgraph.number_of_edges()} edges."
    )

    return subgraph


def assign_default_weights(graph: nx.Graph, default_weight: float = 1.0) -> None:
    """Assign a default weight to all edges that lack a 'weight' attribute.

    Parameters
    ----------
    graph : nx.Graph
        The graph to process.
    default_weight : float
        The default weight to assign.

    Returns
    -------
    None
    """
    for u, v, data in graph.edges(data=True):
        if "weight" not in data:
            graph[u][v]["weight"] = default_weight
