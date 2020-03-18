#Recommendar
from py2neo import Graph, Relationship, Node

USER_NAME = 'neo4j' #Neo4j User Name
USER_PASSWORD = '123456' #User password

def connect():
    graph = Graph("bolt://localhost:7687", auth=(USER_NAME, USER_PASSWORD))
    return graph

query = """
//Total article per journal/conference
MATCH (n) <-[:PUBLISHED_IN]-(article:Article)
WITH n, count(article) AS TotalArticle

MATCH (n)<-[:PUBLISHED_IN]-(article)-[:HAS_KEYWORD]->(keyword:Keyword)
WHERE keyword.title IN ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying']
WITH  n, TotalArticle, count(DISTINCT article) as DBArticle
WHERE toFloat(DBArticle)/toFloat(TotalArticle) >= 0.9
WITH  n AS DBConfJour

//Now, we have all the conference or journals from the DB Community
//We find all the papers from this DB Community

MATCH (DBConfJour) <--(dbArticle:Article)
WITH  dbArticle as dbArticle1, dbArticle as dbArticle12
//Now calculate the citation of papers from the same commuinity
MATCH (dbArticle1)-[dbCite:CITED_BY]->(dbArticle2)
WITH dbArticle1 as DBPapers, count(DISTINCT dbArticle2) AS CiteCount
ORDER BY CiteCount DESC
WITH  DBPapers, CiteCount
//Now we have papers of the db comminity according to the citation count from the same community
//Next we have to calculate the pagerank of the papers
CALL algo.pageRank.stream(
'MATCH (DBPapers) RETURN id(DBPapers) AS id', 
"MATCH (d1:Article)-[:CITED_BY]->(d2:Article) RETURN id(d1) as source, id(d2) as target",  {graph:'cypher', iterations:5, dampingFactor:0.85})
YIELD nodeId, score
WITH DISTINCT algo.asNode(nodeId) AS Top100Article, score AS Rank
ORDER BY Rank DESC
LIMIT 100
//WE have top 100 papers now, we just need to find the authors of them
MATCH (Top100Article)<-[wr:WRITTEN]-(topAuthor:Author)
WITH topAuthor.name as Gurus, count( DISTINCT Top100Article) as NumPapers
WHERE NumPapers >= 2
RETURN Gurus, NumPapers
ORDER BY NumPapers DESC
"""

if __name__ == "__main__":
    print("===========Finding Gurus and number of paper in top 100========================")
    graph = connect()
    data = graph.run(query).data()
    for d in data:
        print(d)
