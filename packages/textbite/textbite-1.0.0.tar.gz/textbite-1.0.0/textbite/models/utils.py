from typing import List, Tuple, Set
from enum import Enum

import torch

from textbite.models.joiner.graph import Graph


class ModelType(Enum):
    GCN = 1
    MLP = 2
    

def edge_indices_to_edges(from_indices: List[int], to_indices: List[int]) -> List[Tuple[int, int]]:
    assert len(from_indices) == len(to_indices)
    return [(from_index, to_index) for from_index, to_index in zip(from_indices, to_indices)]


def get_transitive_subsets(positive_edges: List[Tuple[int, int]]) -> List[Set[Tuple[int, int]]]:
    positive_subsets = []
    for from_idx, to_idx in positive_edges:
        subset = [(from_idx, to_idx)]
        while True:
            from_indices = [f for f, _ in subset]
            to_indices = [t for _, t in subset]
            left_positive_edges = [(f, t) for f, t in positive_edges if t in from_indices and (f, t) not in subset]
            right_positive_edges = [(f, t) for f, t in positive_edges if f in to_indices and (f, t) not in subset]

            if not left_positive_edges and not right_positive_edges:
                break

            subset.extend(left_positive_edges)
            subset.extend(right_positive_edges)

        subset = set(subset)
        if subset not in positive_subsets:
            positive_subsets.append(set(subset))

    return positive_subsets


def get_similarities(node_features, edge_indices):
    lhs_nodes = torch.index_select(input=node_features, dim=0, index=edge_indices[0, :])
    rhs_nodes = torch.index_select(input=node_features, dim=0, index=edge_indices[1, :])
    similarities = torch.cosine_similarity(lhs_nodes, rhs_nodes, dim=1)
    similarities = torch.sigmoid(similarities)
    return similarities


class GraphNormalizer:
    def __init__(self, graphs: List[Graph]):
        edge_stats_1 = torch.zeros_like(graphs[0].edge_attr[0])
        edge_stats_2 = torch.zeros_like(graphs[0].edge_attr[0])
        nb_edges = 0

        node_stats_1 = torch.zeros_like(graphs[0].node_features[0])
        node_stats_2 = torch.zeros_like(graphs[0].node_features[0])
        nb_nodes = 0

        for g in graphs:
            edge_stats_1 += g.edge_attr.sum(axis=0)
            edge_stats_2 += g.edge_attr.pow(2).sum(axis=0)
            nb_edges += g.edge_attr.shape[0]

            node_stats_1 += g.node_features.sum(axis=0)
            node_stats_2 += g.node_features.pow(2).sum(axis=0)
            nb_nodes += g.node_features.shape[0]

        self.edge_mu = edge_stats_1 / nb_edges
        self.edge_std = (edge_stats_2 / nb_edges - self.edge_mu.pow(2)).sqrt()

        self.node_mu = node_stats_1 / nb_nodes
        self.node_std = (node_stats_2 / nb_nodes - self.node_mu.pow(2)).sqrt()

    def normalize_graphs(self, graphs: List[Graph]) -> None:
        for g in graphs:
            g.edge_attr = (g.edge_attr - self.edge_mu) / self.edge_std
            g.node_features = (g.node_features - self.node_mu) / self.node_std
