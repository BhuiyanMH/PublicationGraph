#Find the impact factors of the journals in your graph
from py2neo import Graph, Relationship, Node

USER_NAME = 'neo4j' #Neo4j User Name
USER_PASSWORD = '123456' #User password

def connect():
    graph = Graph("bolt://localhost:7687", auth=(USER_NAME, USER_PASSWORD))
    return graph

query = """
MATCH (jrn:Journal)<-[:PUBLISHED_IN]-(art:Article)
WHERE art.year IN [2018, 2019]
WITH jrn, Count(art) as TotalArt
MATCH (jrn:Journal)<-[:PUBLISHED_IN]-(art:Article)-[c:CITED_BY]->(a:Article{year:2020})
WITH jrn, TotalArt, count(c) as TotalCite
RETURN jrn.title AS Journal, toFloat(TotalCite)/TotalArt AS ImpactFactor
ORDER BY ImpactFactor DESC
"""

if __name__ == "__main__":
    print("===========Finding the impact factors of the journals========================")
    graph = connect()
    data = graph.run(query).data()
    for d in data:
        print(d)
