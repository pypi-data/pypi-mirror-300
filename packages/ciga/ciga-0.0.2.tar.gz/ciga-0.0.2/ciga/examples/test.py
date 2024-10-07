import ciga as cg
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import igraph as ig

from google.cloud import language_v2

import matplotlib.pyplot as plt

from viztracer import VizTracer


# sid = SentimentIntensityAnalyzer()
# Example usage

df = pd.read_csv('../../bigbang_lines_with_sentiment_utf8.csv')


# custom weight function
# input: interaction (str)
# output: weight (float)
# def weight_func(interaction):
#     # return sid.polarity_scores(interaction)['neg']
#     return 1

# tracer = VizTracer()
# tracer.start()

# load data
# interactions = cg.prepare_data(df, ('Season', 'Episode', 'Scene', 'Line'),
#                                 source='Speaker', target='Listener', interaction='Words')
# sub_interactions = cg.segment(interactions, start=(1, 1, 1, 1), end=(2, 1, 1, 1))
# print(sub_interactions)
weights = cg.prepare_data(df, ('Season', 'Episode', 'Scene', 'Line'), source='Speaker', target='Listener', interaction='Words', weight='weight')
sub_weights = cg.segment(weights, start=(1, 1, 1, 1), end=(2, 1, 1, 1))
# weights = cg.get_weights(sub_interactions, weight_func=analyze_sentiment)
# print(weights.head())
# print(weights)
# agg_weights = cg.agg_weights(weights, ('Season', 'Episode', 'Scene', 'Line'), agg_func=lambda x: sum(x))

# print(agg_weights)
# agg_weights.set_index(['Season', 'Episode', 'Scene', 'Line'], inplace=True)
# print(agg_weights)
# idx = pd.IndexSlice
# print(agg_weights.loc[idx[-1, 1, 2, 1]: idx[1, 1, 2, 4], :])

# create network
tg = cg.TGraph(data=sub_weights, position=('Season', 'Episode', 'Scene', 'Line'), directed=True)

# print(tg.data)
# graph = tg.get_graph((1, 1, 2))'
# graph = tg.get_graph((1, 1, 2, 1))
graph = tg.get_graph()

# print('tg._vnames:', tg._vnames)
# print(graph.vs['name'])

# print(graph.is_directed())
# tg.data.head()
fig, ax = plt.subplots()
cg.iplot(graph, target=ax)

# tracer.stop()
# tracer.save()

# centrality analysis
# res = cg.tgraph_degree(tg, weighted=True, normalized=True)
res1 = cg.tgraph_degree(tg, weighted=True, normalized=True)
# res2 = cg.tgraph_betweenness(tg, weighted=True, normalized=True)
# res3 = cg.tgraph_closeness(tg, weighted=True, normalized=True)
# print(res)
# res.head()

res1.to_csv('sentiment_score_degree.csv', index=False)
# res2.to_csv('sentiment_score_betweenness.csv', index=False)
# res3.to_csv('sentiment_score_closeness.csv', index=False)

plt.show()
