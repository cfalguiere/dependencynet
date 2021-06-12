"""
Fixtures for
purpose : build graph programmatically
No dataset
The graph
- consists of subsystems, artefacts and repository
- a susbsystem groups many artefacts
- artefacts may depend on each other
- a home made artefact may have a repository
"""
import pytest

# module import
from dependencynet.schema import SchemaBuilder
from dependencynet.model import ModelBuilder

from dependencynet.network.graphbuilder import ResourceNode
from dependencynet.network.graphbuilder import GraphBuilder
from dependencynet.network.stylebuilder import StyleBuilder


@pytest.fixture
def schema_libs():
    schema = SchemaBuilder().resource('subsystem', 'S') \
                             .resource('artefact', 'A') \
                             .resource('repository', 'R') \
                             .render()
    return schema


@pytest.fixture
def model_libs(schema_libs):
    model = ModelBuilder().with_schema(schema_libs).render()
    return model


@pytest.fixture
def class_mapping_libs():
    return {'subsystem': SubSystemNode,
            'artefact': ArtefactNode,
            'repository': RepositoryNode}


# networkx classes

class SubSystemNode(ResourceNode):
    def __init__(self, nid, label):
        super().__init__({'id': f'S{nid}', 'label': label}, 'subsystem')


class ArtefactNode(ResourceNode):
    def __init__(self, nid, name, version):
        super().__init__({'id': f'A{nid}', 'label': f'{name}:{version}'}, 'artefact')
        self.data['name'] = name
        self.data['version'] = version


class RepositoryNode(ResourceNode):
    def __init__(self, nid, label):
        super().__init__({'id': f'R{nid}', 'label': label}, 'repository')


@pytest.fixture
def graph_model_libs(class_mapping_libs, model_libs):
    graph_model = GraphBuilder().with_types(class_mapping_libs).with_model(model_libs).render()

    def create_system(nid, label):
        node = SubSystemNode(nid, label)
        graph_model.G.add_node(node)
        return node

    def create_artefact(nid, label, version):
        node = ArtefactNode(nid, label, version)
        graph_model.G.add_node(node)
        return node

    def create_repository(nid, label):
        node = RepositoryNode(nid, label)
        graph_model.G.add_node(node)
        return node

    def add_edge(nid_left, nid_right):
        graph_model.G.add_edge(nid_left, nid_right)

    systen_gui = create_system('gui', 'Web Site Gui')
    system_api = create_system('api', 'Web Site API')
    system_iam = create_system('iam', 'IAM Service')

    add_edge(systen_gui, system_api)
    add_edge(system_api, system_iam)

    artefact_gui = create_artefact('gui', 'web-site-gui', 'v1.5.2')
    add_edge(systen_gui, artefact_gui)

    artefact_vue = create_artefact('vue', 'vue-js', '3.0.11')
    add_edge(artefact_gui, artefact_vue)

    artefact_api = create_artefact('api', 'web-site-api', 'v1.8.1')
    add_edge(system_api, artefact_api)

    artefact_rest = create_artefact('rest', 'flask', '2.0.1')
    add_edge(artefact_api, artefact_rest)

    repo_front = create_repository('front', 'web/front')
    add_edge(artefact_gui, repo_front)

    repo_back = create_repository('back', 'web/back')
    add_edge(artefact_api, repo_back)

    return graph_model


@pytest.fixture
def graph_style_libs(schema_libs):
    graph_style = StyleBuilder(schema_libs).render()
    return graph_style
