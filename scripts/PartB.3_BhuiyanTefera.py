#For each conference find its community
from py2neo import Graph, Relationship, Node

USER_NAME = 'neo4j' #Neo4j User Name
USER_PASSWORD = '123456' #User password

def connect():
    graph = Graph("bolt://localhost:7687", auth=(USER_NAME, USER_PASSWORD))
    return graph

query = """
MATCH (conf:Conference)<-[pub:PUBLISHED_IN]-(art:Article)<-[:WRITTEN]-(auth:Author)
WITH conf.title AS Conference, collect(DISTINCT pub.edition) AS EditionList, auth.name AS Author
WHERE Size(EditionList)>4
RETURN Conference, collect(Author) AS Community
"""

if __name__ == "__main__":
    print("===========Finding conference community========================")
    graph = connect()
    data = graph.run(query).data()
    for d in data:
        print(d)
