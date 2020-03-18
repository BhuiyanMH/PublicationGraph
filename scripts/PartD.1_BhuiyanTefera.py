#Recommendar
from py2neo import Graph, Relationship, Node

USER_NAME = 'neo4j' #Neo4j User Name
USER_PASSWORD = '123456' #User password

def connect():
    graph = Graph("bolt://localhost:7687", auth=(USER_NAME, USER_PASSWORD))
    return graph

def define_community():
    print("=> Defining Community")
    query = """
    MATCH (aik:Keyword)
    WHERE  NOT aik.title IN ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying']
    MERGE (aiCom: AICommunity)
    MERGE (aiCom)-[:DEFINED_BY]->(aik)
    WITH aik
    MATCH (dbk:Keyword)
    WHERE  dbk.title IN ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying']
    MERGE (dbcom: DBCommunity)
    MERGE (dbcom)-[:DEFINED_BY]->(dbk)
    """
    return connect().run(query).data()

def find_db_community_conference_journal():
    print("=> Defining DB Community Conference Journal")
    query = """
    MATCH (n) <-[:PUBLISHED_IN]-(article:Article)
    WITH n, count(article) AS TotalArticle
    MATCH (n)<-[:PUBLISHED_IN]-(article)-[:HAS_KEYWORD]->(keyword:Keyword)
    WHERE keyword.title IN ['data management', 'indexing', 'data modeling', 'big data', 'data processing', 'data storage', 'data querying']
    WITH  n, TotalArticle, count(DISTINCT article) as DBArticle
    WHERE toFloat(DBArticle)/toFloat(TotalArticle) >= 0.9
    WITH  n AS DBConfJour
    MERGE (dbc:DBCommunity)
    MERGE (DBConfJour)-[:RELATED_TO]->(dbc)
    WITH DBConfJour
    MATCH (dbc:DBCommunity)<-[:RELATED_TO]-(DBConfJour) <--(dbArticle:Article)
    SET dbArticle.community = 'DB Community'
    """
    return connect().run(query).data()

def find_top_articles():
    print("=> Finding Rank of Articles")
    query = """
    //Now we have papers of the db community
    //Next we have to calculate the pagerank of the papers
    CALL algo.pageRank(
    'MATCH (dbArticle:Article{community:"DB Community"}) RETURN id(dbArticle) AS id',
    'MATCH (d1:Article{community:"DB Community"})-[:CITED_BY]->(d2:Article{community:"DB Community"}) RETURN id(d1) as source, id(d2) as target',
    {graph:'cypher', iterations:20, dampingFactor:0.85, write: true, writeProperty:"pagerank"})
    YIELD nodes, iterations, loadMillis, computeMillis, writeMillis, dampingFactor, write, writeProperty
    """
    return connect().run(query).data()

def find_gurus():
    print("=> Finding Gurus")
    query = """
    MATCH (dbArticle:Article{community:"DB Community"})
    WITH dbArticle as Top100Article
    ORDER BY dbArticle.pagerank DESC 
    LIMIT 100
    MATCH (Top100Article)<-[:WRITTEN]-(author: Author)
    WITH author AS Author, count(DISTINCT Top100Article) as NumArticle
    WHERE NumArticle >= 2
    WITH Author, NumArticle
    SET Author.guru="yes"
    RETURN Author.name AS Author, NumArticle
    ORDER BY NumArticle DESC
    """
    return connect().run(query).data()

if __name__ == "__main__":
    print("===========Finding Gurus and number of paper in top 100========================")
    graph = connect()
    define_community()
    find_db_community_conference_journal()
    find_top_articles()
    data = find_gurus()
    for d in data:
        print(d)
