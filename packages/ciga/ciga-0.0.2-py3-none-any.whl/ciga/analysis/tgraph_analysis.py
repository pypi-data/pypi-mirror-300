import pandas as pd
from typing import Callable, Dict, Any, List
from ..ciga import TGraph
from .graph_analysis import graph_degree, graph_betweenness, graph_closeness
from tqdm import tqdm


def sequential_analysis(tg: TGraph,
                        analysis_func: Callable[..., Dict[str, List[float]]],
                        *,
                        start=None,
                        end=None,
                        **analysis_kwargs) -> pd.DataFrame:
    """
    Perform analysis on a time-varying graph sequentially.
    :param tg:
    :param analysis_func:
    :param start:
    :param end:
    :param analysis_kwargs:
    :return:
    """
    results = pd.DataFrame()
    # add position columns to results
    for col in tg._position:
        results[col] = []
    results['character'] = []

    # get time steps
    time_steps = tg.data.index.unique().tolist()
    if start:
        time_steps = [step for step in time_steps if step >= start]
    if end:
        time_steps = [step for step in time_steps if step <= end]

    for step in tqdm(time_steps, desc='Processing time steps', unit='step'):
        graph = tg.get_graph(step)

        measures = analysis_func(graph, **analysis_kwargs)
        for col, val in zip(tg._position, step):
            measures[col] = val
        measures['character'] = graph.vs['name']

        results = pd.concat([results, measures], axis=0).reset_index(drop=True)

    return results


def tgraph_degree(tgraph: TGraph, *, start=None, end=None, weighted=False, normalized=False) -> pd.DataFrame:
    return sequential_analysis(tgraph, analysis_func=graph_degree, start=start, end=end, weighted=weighted,
                               normalized=normalized)


def tgraph_betweenness(tgraph: TGraph, *, start=None, end=None, weighted=False, normalized=True,
                       cutoff=None, sources=None, targets=None) -> pd.DataFrame:
    return sequential_analysis(tgraph, analysis_func=graph_betweenness, start=start, end=end, weighted=weighted,
                               normalized=normalized, cutoff=cutoff, sources=sources, targets=targets)


def tgraph_closeness(tgraph: TGraph, *, start=None, end=None, weighted=False, normalized=True,
                     cutoff=None) -> pd.DataFrame:
    return sequential_analysis(tgraph, analysis_func=graph_closeness, start=start, end=end, weighted=weighted, normalized=normalized,
                               cutoff=cutoff)

# def eigenvector_centrality(tgraph: TGraph, *, start=None, end=None, max_iter=100, tol=1e-06, weight=None) -> pd.DataFrame:
#     def eigenvector_centrality_func(graph: ig.Graph) -> Dict[str, List[float]]:
#         if weight is not None:
#             weights = graph.es[weight]  # Assuming 'weight' is the name of the edge attribute
#         else:
#             weights = None
#         eigenvector = graph.eigenvector_centrality(
#             weights=weights,
#             directed=graph.is_directed(),
#             niter=max_iter,
#             epsilon=tol
#         )
#         return {'eigenvector': eigenvector}
#
#     return sequential_analysis(tgraph, eigenvector_centrality_func, start=start, end=end)
