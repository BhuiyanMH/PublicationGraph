from py2neo import Graph, Relationship, Node

USER_NAME = 'neo4j' #Neo4j User Name
USER_PASSWORD = '123456' #User password

def connect():
    graph = Graph("bolt://localhost:7687", auth=(USER_NAME, USER_PASSWORD))
    return graph

#clear the database
def detach_data():
    print("Deleting Existing Data:")
    query = """match(n) detach delete n"""
    return connect().run(query).data()


# load the authors
def load_authors():
    print("Loading Authors")
    query = """LOAD CSV WITH HEADERS FROM "file:///authors.csv" as row FIELDTERMINATOR ';'
    CREATE (a:Author{id:toInteger(row.id), name:row.name})
    """
    return connect().run(query).data()


# load the keywords
def load_keywords():
    print("Loading Keywords")
    query = """ LOAD CSV WITH HEADERS FROM "file:///keywords.csv" as row FIELDTERMINATOR ';'
    CREATE (k:Keyword{id:toInteger(row.id), title:row.keyword})
    """
    return connect().run(query).data()


def load_journals():
    print("Loading Journals")
    query = """
     LOAD CSV WITH HEADERS FROM "file:///journal.csv" as row FIELDTERMINATOR ';'
     CREATE (j:Journal{id:toInteger(row.id), title:row.name, issn:row.issn, publisher:row.publisher})
     """
    return connect().run(query).data()


# load the journal articles
def load_Journals_articles():
    print("Loading Journals Articles")
    query = """ LOAD CSV WITH HEADERS FROM "file:///journal_article.csv" as row FIELDTERMINATOR ';'
    CREATE (:Article{id:toInteger(row.id), title:row.title, ee:row.ee, volume:toInteger(row.volume), page:row.pages, year:toInteger(row.year)})
    MERGE(j:Journal{id:toInteger(row.Journal)})
    MERGE(a:Article{id:toInteger(row.id)})
    CREATE(a)-[:PUBLISHED_IN]->(j)
    """
    return connect().run(query).data()


# load conference
def load_conference():
    print("Loading conference")
    query = """ LOAD CSV WITH HEADERS FROM "file:///conference.csv" as row FIELDTERMINATOR ';'
    MERGE (conf:Conference{id:toInteger(row.id)})
    ON CREATE SET conf.title=row.name;
    """
    return connect().run(query).data()

# load cities
def load_cities():
    print("Loading  Cities")
    query = """LOAD CSV WITH HEADERS FROM "file:///conference.csv" as row FIELDTERMINATOR ';'
    MERGE (c:City{name:row.city})"""
    return connect().run(query).data()


# creating relationship between cities and conferences
def load_city_conference():
    print("Loading City-Conference")
    query = """LOAD CSV WITH HEADERS FROM "file:///conference.csv" as row FIELDTERMINATOR ';'
    MERGE (conf:Conference{id:toInteger(row.id)})
    MERGE (c:City{name:row.city})
    MERGE (conf)-[:HELD_IN{edition:toInteger(row.edition), year:toInteger(row.year)}] -> (c)"""
    return connect().run(query).data()


# load the conference articles
def load_conference_article():
    print("Loading Article Conference")
    query = """LOAD CSV WITH HEADERS FROM "file:///conference_article.csv" as row FIELDTERMINATOR ';'
    CREATE (:Article{id:toInteger(row.id), title:row.title, ee:row.ee, page:row.pages})
    MERGE(c:Conference{id:toInteger(row.conference)})
    MERGE(a:Article{id:toInteger(row.id)})
    CREATE(a)-[:PUBLISHED_IN{edition:toInteger(row.edition)}]->(c)"""
    return connect().run(query).data()


# creating relationship between article and keyword
def load_article_keyword():
    print("Loading Article Keyword Relationship")
    query = """ LOAD CSV WITH HEADERS FROM "file:///article_keyword.csv" as row FIELDTERMINATOR ';'
    MERGE (a:Article{id:toInteger(row.id)})
    MERGE (k:Keyword{id:toInteger(row.keyword)})
    MERGE (a)-[:HAS_KEYWORD]->(k)"""
    return connect().run(query).data()


# creating relationship between author and article
def load_author_article():
    print("Loading Author Article Relationship")
    query = """LOAD CSV WITH HEADERS FROM "file:///author_article.csv" as row FIELDTERMINATOR ';'
    MERGE (author:Author{id:toInteger(row.author_id)})
    MERGE (paper:Article{id:toInteger(row.paper_id)})
    MERGE (author)-[:WRITTEN] -> (paper)"""
    return connect().run(query).data()


def load_citiation():
    print("Loading Citations")
    query = """LOAD CSV WITH HEADERS FROM"file:///citation.csv" as row FIELDTERMINATOR';'
    MERGE(paper1: Article{id: toInteger(row.paper_id)})
    MERGE(paper2: Article{id: toInteger(row.cited_paper)})
    MERGE(paper2) - [: CITED_BY] -> (paper1)"""
    return connect().run(query).data()


if __name__ == "__main__":
    print("===========Loading Data========================")
    connect()
    detach_data()
    load_authors()
    load_keywords()
    load_journals()
    load_Journals_articles()
    load_conference()
    load_cities()
    load_city_conference()
    load_conference_article()
    load_article_keyword()
    load_author_article()
    load_citiation()








    print("Data successfully loaded:")
