"""
This module provides helpers to setup the cytoscape graph style
"""
import logging


# TODO pattern builder
class StyleBuilder():
    logger = logging.getLogger(__name__)

    @classmethod
    def __init__(self, schema):
        self.schema = schema
        self.graph_style = None
        self.levels_colors = ['#BBD4EF', '#CBE4FF', '#DBF4FF']
        self.colors = {
            '1': '#F9EBDF',
            '2': '#b5dce1',
            '3': '#cfdaf0',
            '4': '#f4e3c9',
            '5': '#d7e0b1',
            '6': '#cecfe3',
            '7': '#CBE4F9',
            '8': '#d0e5d2',
            '9': '#D6CDEA',
            '10': '#f4e0e9',
            '11': '#CDF5F6',
            '12': '#d6cdc8',
            '13': '#Eff9DA',
            '14': '#f4d9d0',
            '15': '#c9d0e2'
            }

    def style_template():
        graph_style = [
            {
                'selector': 'node',
                'css': {
                    'label': 'data(id)',
                    'content': 'data(label)',
                    'font-size': '4pt',
                    'border-width': '0.5',
                    'text-valign': 'center',
                    'text-halign': 'center',
                    'label-font-weight': 'bold',
                    'tooltip-background-color': '#FFFFAA',
                    'height': '0.8em',
                    'width': '5em',
                    'text-wrap': 'wrap',
                    'text-max-width': '5em'
                   }
            },
            {
                'selector': 'node.level',
                'css': {
                    'shape': 'roundrectangle'
                }
            },
            {
                'selector': 'node.resource',
                'css': {
                    'shape': 'roundrectangle'
                }
            },
            {
                 'selector': 'edge',
                 'css': {
                    'shape': 'arrow',
                    'width': '0.5',
                    'line-color': '#444444',
                    'curve-style': 'bezier',
                    'target-arrow-color': '#444444',
                    'target-arrow-shape': 'triangle'
                 }
            }
        ]

        return graph_style

    @classmethod
    def render(self):
        # TODO manage too many colors
        self.graph_style = self.style_template()
        i = 0
        for k in self.schema.levels_keys():
            self.logger.info(f"adding level {k}")
            selecter = {
                            'selector': f'node.{k}',
                            'css': {
                                'color': 'black',
                                'background-color': self.levels_colors[i]
                            }
                        }
            self.graph_style.append(selecter)
            i += 1

        i = 0
        for k in self.schema.resources_keys():
            bgcolor = list(self.colors.values())[i]
            self.logger.info(f"adding resource {k}")
            selecter = {
                            'selector': f'node.{k}',
                            'css': {
                                'color': 'black',
                                'background-color': bgcolor
                            }
                        }
            self.graph_style.append(selecter)
            i += 1

        for (kl, kr) in self.schema.connections_pairs():
            k = self.schema.resource_definition(kl)['connect_id_name']
            self.logger.info(f"adding connections {k}")
            bgcolor = list(self.colors.values())[i]
            selecter = {
                            'selector': f'node.{k}',
                            'css': {
                                'color': 'black',
                                'background-color': bgcolor
                            }
                        }
            self.graph_style.append(selecter)
            i += 1

        return self.graph_style
