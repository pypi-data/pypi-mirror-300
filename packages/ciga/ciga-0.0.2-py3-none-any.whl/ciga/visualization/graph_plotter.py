from matplotlib import pyplot as plt
import igraph as ig


def iplot(graph, target=None, layout='auto', visual_style=None):
    # print('iplot')
    # print(graph.vs['name'])
    default_style = {
        "vertex_label": graph.vs["name"] if "name" in graph.vs.attributes() else None,
        # 2 decimal places for edge labels
        "edge_label": ["{:.2f}".format(weight) for weight in graph.es["weight"]] if "weight" in graph.es.attributes() else None,
        "bbox": (300, 300),  # You can adjust the size as needed
        "margin": 20,
        # Add more default styling options here if desired
    }

    if visual_style is not None:
        # Ensure that visual_style is a dictionary
        if not isinstance(visual_style, dict):
            raise TypeError("visual_style must be a dictionary of visual style attributes.")
        # Update the default style with user-provided style
        default_style.update(visual_style)

    if target is None:
        target = plt.subplots()[1]
    ig.plot(graph, layout=layout, target=target, **default_style)