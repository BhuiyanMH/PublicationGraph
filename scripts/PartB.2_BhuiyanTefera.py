#Find the top 3 most cited papers of each conference.
from py2neo import Graph, Relationship, Node

USER_NAME = 'neo4j' #Neo4j User Name
USER_PASSWORD = '123456' #User password

def connect():
    graph = Graph("bolt://localhost:7687", auth=(USER_NAME, USER_PASSWORD))
    return graph

query = """
MATCH (c:Conference)<-[:PUBLISHED_IN]-(a1:Article)-[cite:CITED_BY]->(a2:Article)
WITH c.title AS Conference, a1.title as Article, count(cite) AS CiteCount
ORDER BY Conference, CiteCount DESC
WITH Conference, collect(Article) AS ArticleList, collect(CiteCount) AS CitationList
RETURN Conference, ArticleList[0..3] AS Top3CitedPaper,CitationList[0..3] AS Citation
"""

if __name__ == "__main__":
    print("===========Finding the top 3 most cited papers of each conference========================")
    graph = connect()
    data = graph.run(query).data()
    for d in data:
        print(d)
