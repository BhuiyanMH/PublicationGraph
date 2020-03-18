from py2neo import Graph, Relationship, Node

USER_NAME = 'neo4j'  # Neo4j User Name
USER_PASSWORD = '123456'  # User password


def connect():
    graph = Graph("bolt://localhost:7687", auth=(USER_NAME, USER_PASSWORD))
    return graph
def triangle_count_algo():
    query = """CALL algo.triangleCount.stream('Article', "CITED_BY")
    YIELD nodeId,triangles as Triangles, coefficient
    RETURN algo.getNodeById(nodeId).title AS Article_Title, Triangles, coefficient
    ORDER BY coefficient DESC LIMIT 10"""
    return connect().run(query).data()

if __name__ == "__main__":
    connect()
    trianlge_count = triangle_count_algo()
    print("List of Articles and their traingle counts:")
    for count in trianlge_count:
        print(count)

