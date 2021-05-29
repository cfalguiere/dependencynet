"""
Tests graph style generation
"""

# module import
from dependencynet.network.stylebuilder import StyleBuilder


def test_graphstyle(schema_towns, compact_columns_towns):
    sb = StyleBuilder(schema_towns)
    graph_style = sb.render()

    selectors = [style['selector'] for style in graph_style]

    # check whether each node type is represented
    for element in compact_columns_towns:
        selector = f'node.{element}'
        assert selector in selectors
        i = selectors.index(selector)
        assert 'background-color' in graph_style[i]['css']
        assert 'color' in graph_style[i]['css']
