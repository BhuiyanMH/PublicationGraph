from py2neo import Graph, Relationship, Node

USER_NAME = 'neo4j'  # Neo4j User Name
USER_PASSWORD = '123456'  # User password


def connect():
    graph = Graph("bolt://localhost:7687", auth=(USER_NAME, USER_PASSWORD))
    return graph
def page_rank_algo():
    query = """CALL algo.pageRank.stream('Article', 'CITED_BY', {iterations:20, dampingFactor:0.85})
    YIELD nodeId, score
    RETURN algo.getNodeById(nodeId).title as Article, score as PageRank
    ORDER BY PageRank DESC"""
    return connect().run(query).data()
if __name__ == "__main__":
    connect()
    scores = page_rank_algo()
    print("List of Articles and their page rank score: ")
    for score in scores:
        print(score)