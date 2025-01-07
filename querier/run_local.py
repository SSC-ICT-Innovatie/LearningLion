
from DataFetcher.libraries.data_classes.range_enum import Range
from querier.libraries import database, query
from querier.libraries.embedding import Embedding

def run_local_query_stores(prompt,range=Range.Tiny):
  print("Querying stores")
  embed = Embedding()
  data = database.Database(embed)
  data.setup_database(range=range)
  querier = query.Query()
  querier.setup_querier(data)
  data.close_database_connection()
  return querier.query(prompt)
  
def getDocumentBlobFromDatabase(UUID: str, range=Range.Tiny):
    # Initialize the embedding and database objects
    embed = Embedding()
    data = database.Database(embed)
    
    # Get the database connection based on the specified range
    db_connection = data.get_database_connection(range=range)
    
    # Open a cursor without using 'with'
    cursor = db_connection.cursor()
    cursor.execute("SELECT document FROM documents WHERE UUID = ?", (UUID,))
    item = cursor.fetchone()
    
    # Close the cursor and database connection
    cursor.close()
    data.close_database_connection()
    
    # Return the document if found, or None if not
    return item[0] if item else None