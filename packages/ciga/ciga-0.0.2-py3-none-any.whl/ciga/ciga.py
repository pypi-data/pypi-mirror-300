import pandas as pd
import numpy as np
from igraph import Graph


class TGraph:

    def __init__(self, init_graph=None, data=None, position=None, directed=True):
        if data is None:
            raise ValueError("Data must be provided.")
        if position is None:
            raise ValueError("Position must be provided.")
        if 'weight' not in data.columns:
            raise ValueError("Weight column not found in data. Run calculate_weights() first.")

        self.data = data.copy()
        self._position = position
        self._layout = None
        self._directed = directed
        self._vnames = []
        self.name_to_id = {}
        self.id_to_name = {}
        self._cache_graph = None
        self._cache_time_point = tuple([-np.inf] * len(self._position))

        # set multi index if not already
        if not isinstance(self.data.index, pd.MultiIndex):
            self.data.set_index(list(self._position), inplace=True)

        if not self._directed:
            idx = self.data['source'] > self.data['target']
            self.data.loc[idx, ['source', 'target']] = self.data.loc[idx, ['target', 'source']].values

        if init_graph is None:
            self._init_graph = Graph(directed=self._directed)
            self._init_graph.vs['name'] = []
        else:
            self._init_graph = init_graph
            self._directed = init_graph.is_directed()

        # create name to id mapping
        self._vnames = self._init_graph.vs['name']
        self._create_vnames()

        self._cache_graph = self._init_graph.copy()

    def _create_vnames(self):
        self.name_to_id = {name: idx for idx, name in enumerate(self._vnames)}
        self.id_to_name = {idx: name for idx, name in enumerate(self._vnames)}

        return self._vnames

    @property
    def is_directed(self):
        return self._directed

    def get_graph(self, time_point=None):
        if time_point is None:
            time_point = tuple([np.inf] * len(self._position))
        if len(time_point) < len(self._position):
            time_point = tuple(list(time_point) + [np.inf] * (len(self._position) - len(time_point)))

        if self._cache_time_point and self._cache_time_point < time_point:
            start = list(self._cache_time_point)
            start[-1] += 1
            delta_data = self.take_interval(start=start, end=time_point)
        else:
            delta_data = self.take_interval(start=None, end=time_point)
            self._cache_graph = self._init_graph.copy()
            # also reset the name to id mapping

        if delta_data.empty:
            return self._cache_graph
        self._update_graph(self._cache_graph, delta_data)
        self._cache_time_point = time_point
        return self._cache_graph

    def get_delta_graph(self, start=None, end=None):
        # this should not change any data in the tgraph
        if start is not None and len(start) == len(self._position):
            start = list(start)
            start[-1] += 1
        delta_data = self.take_interval(start=start, end=end)
        if delta_data.empty:
            interval_graph = Graph(directed=self._directed)
        else:
            agg_data = delta_data.groupby(['source', 'target'], as_index=False)['weight'].sum()
            nodes = set(agg_data['source']).union(set(agg_data['target']))
            temp_node_to_id = {node: idx for idx, node in enumerate(nodes)}
            source_ids = agg_data['source'].map(temp_node_to_id)
            target_ids = agg_data['target'].map(temp_node_to_id)
            edges = list(zip(source_ids, target_ids))
            interval_graph = Graph(edges=edges, directed=self._directed)

        return interval_graph

    def _update_graph(self, graph, data):
        # print(data.head())
        agg_data = data.groupby(['source', 'target'], as_index=False)['weight'].sum()

        # NEW IMPLEMENTATION
        existing_nodes = set(graph.vs['name'])
        new_nodes = set(agg_data['source']).union(set(agg_data['target'])) - set(existing_nodes)

        # add new nodes to graph, also to self._vnames
        if new_nodes:
            graph.add_vertices(list(new_nodes))
            self._vnames = graph.vs['name']  # keep _vnames the newest
            # update name to id mapping, start from the last index
            for idx, node in enumerate(new_nodes, start=len(existing_nodes)):
                self.name_to_id[node] = idx
                self.id_to_name[idx] = node

        # add columns for source and target ids
        agg_data['source_id'] = agg_data['source'].map(self.name_to_id)
        agg_data['target_id'] = agg_data['target'].map(self.name_to_id)

        existing_edges = graph.get_edgelist()
        edges_in_data = pd.DataFrame(existing_edges, columns=['source_id', 'target_id'])

        # merge to identify existing and new edges
        df_merged = pd.merge(
            agg_data,
            edges_in_data,
            on=['source_id', 'target_id'],
            how='left',
            indicator=True
        )

        df_new_edges = df_merged[df_merged['_merge'] == 'left_only']
        df_to_update = df_merged[df_merged['_merge'] == 'both']

        new_edges = list(zip(df_new_edges['source_id'], df_new_edges['target_id']))
        new_weights = df_new_edges['weight'].tolist()
        edges_to_update = list(zip(df_to_update['source_id'], df_to_update['target_id']))
        existing_edge_ids_to_update = graph.get_eids(pairs=edges_to_update, directed=graph.is_directed())
        weight_updates = df_to_update['weight'].tolist()

        # Add new edges in bulk
        if new_edges:
            graph.add_edges(new_edges)
            # Set weights for new edges
            new_edge_ids = graph.es[-len(new_edges):].indices
            graph.es[new_edge_ids]['weight'] = new_weights

        # Update weights of existing edges in bulk
        if existing_edge_ids_to_update:
            # Retrieve current weights
            current_weights = graph.es[existing_edge_ids_to_update]['weight']
            # Update weights
            updated_weights = [cw + w for cw, w in zip(current_weights, weight_updates)]
            graph.es[existing_edge_ids_to_update]['weight'] = updated_weights

        return graph

    def take_interval(self, start=None, end=None):
        if start is None:
            start = [-np.inf] * len(self._position)
        else:
            if len(start) < len(self._position):
                start = list(start) + [None] * (len(self._position) - len(start))
            start = [s if s is not None else -np.inf for s in start]

        if end is None:
            end = [np.inf] * len(self._position)
        else:
            if len(end) < len(self._position):
                end = list(end) + [None] * (len(self._position) - len(end))
            end = [e if e is not None else np.inf for e in end]

        if len(self._position) > len(start) or len(self._position) > len(end):
            raise ValueError("The length of 'start/end' is out of range.")

        idx = pd.IndexSlice
        filtered_data = self.data.loc[idx[tuple(start): tuple(end)], :].copy()

        return filtered_data
