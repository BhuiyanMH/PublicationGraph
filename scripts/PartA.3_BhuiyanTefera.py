#evolving the schema
from py2neo import Graph, Relationship, Node

USER_NAME = 'neo4j' #Neo4j User Name
USER_PASSWORD = '123456' #User password

def connect():
    graph = Graph("bolt://localhost:7687", auth=(USER_NAME, USER_PASSWORD))
    return graph

# load the organization
def load_organization():
    query = """LOAD CSV WITH HEADERS FROM "file:///organization.csv" as row FIELDTERMINATOR ';'
    CREATE (o:Organization{id:toInteger(row.id), name:row.name, type:row.type})
    MERGE(c:City{name:row.city})
    CREATE(o)-[:LOCATED_AT]->(c)
    """
    return connect().run(query).data()

# load the reviews
def load_review():
    query = """ LOAD CSV WITH HEADERS FROM "file:///review.csv" as row FIELDTERMINATOR ';'
    CREATE (r:Review{id:toInteger(row.id), comment:row.comment, decision:row.decision})
    MERGE(art:Article{id:toInteger(row.art_id)})
    MERGE(auth:Author{id:toInteger(row.reviewer_id)})
    MERGE (c{title:row.book_title})
    CREATE(art)<-[:ABOUT]-(r)
    CREATE(r)<-[:GIVE]-(auth)
    CREATE(r)<-[:HAS]-(c)
    """
    return connect().run(query).data()

#load affilication
def load_affilication():
    query = """
    LOAD CSV WITH HEADERS FROM "file:///auth_org.csv" as row FIELDTERMINATOR ';'
    MERGE(auth:Author{id:toInteger(row.auth_id)})
    MERGE(org:Organization{id:toInteger(row.org_id)})
    CREATE(org)<-[:AFFILIATED_TO]-(auth)
     """
    return connect().run(query).data()

if __name__ == "__main__":
    print("===========Evolving the Graph========================")
    connect()
    print("Creating the organization")
    load_organization()
    print("Creating the review")
    load_review()
    print("Creating the affiliation")
    load_affilication()
    print("Graph Evolved Successfully")
