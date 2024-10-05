# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Visualizer.
"""

from graphillion import GraphSet

def output_all_graphs(gs, filename, limit = 100):
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()
    G.add_edges_from(GraphSet.universe())
    pos = nx.spring_layout(G, seed = 0)

    n = min(gs.len(), limit)
    col = min(n, 10)
    row = ((n - 1) // col) + 1

    fig, ax = plt.subplots(row, col, figsize = (5 * col, 5 * row))
    #fig, ax = plt.subplots(row, col, figsize = (10, 5))

    for i, g in enumerate(gs):
        H = nx.Graph()
        H.add_edges_from(list(g))
        edge_widths = [5 if H.has_edge(*e) else 1 for e in G.edges()]
        edge_colors = ['red' if H.has_edge(*e) else 'black' for e in G.edges()]
        if row > 1:
            nx.draw_networkx(G, pos, width=edge_widths, edge_color = edge_colors, ax=ax[(i // col), (i % col)])
        else:
            nx.draw_networkx(G, pos, width=edge_widths, edge_color = edge_colors, ax=ax[i % col])
        if i >= limit:
            break

    fig.savefig(filename)
