#Find the h-indexes of the authors in your grap
from py2neo import Graph, Relationship, Node

USER_NAME = 'neo4j' #Neo4j User Name
USER_PASSWORD = '123456' #User password

def connect():
    graph = Graph("bolt://localhost:7687", auth=(USER_NAME, USER_PASSWORD))
    return graph

query = """
MATCH (auth:Author)-[:WRITTEN]->(art1:Article)
MATCH (art1)-[cite:CITED_BY]->(art2:Article)
WITH auth.name as Author, art1.title as Article, count(cite) as Citation
ORDER BY Author, Citation DESC
WITH Author, collect(Citation) as citationList
UNWIND range(0, size(citationList)-1) as position WITH Author,
    CASE WHEN citationList[position] <= (position+1)
        THEN citationList[position]
        ELSE (position+1)
    END as index
RETURN Author, max(index) as HIndex
ORDER BY HIndex DESC
"""

if __name__ == "__main__":
    print("===========Calculating the H-index of authors========================")
    graph = connect()
    data = graph.run(query).data()
    for d in data:
        print(d)
