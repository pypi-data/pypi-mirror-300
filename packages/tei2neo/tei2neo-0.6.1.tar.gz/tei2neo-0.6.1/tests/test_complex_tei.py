import os

from tei2neo import parse
from semper_backend.utils import GraphUtils

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'xml_testfiles',
)

def _load_graph(graph, filename):

    filename = os.path.join(FIXTURE_DIR, filename)
    if not os.path.isfile(filename):
        raise ValueError("File {} does not exist.".format(filename))
    doc, status, soup = parse(filename=filename)
    tx = graph.begin()
    doc.save(tx)
    tx.commit() 


def test_inner_relationships(graph):
    """Tests whether elements that refer to each other
    via "prev", "next" attributes are actually linked
    via such relationships
    """
    tei_file = '20_Ms_217_103.xml'
    _load_graph(graph, tei_file)
    
    gut = GraphUtils(graph)
    gut.link_inner_relationships(tei_file)

