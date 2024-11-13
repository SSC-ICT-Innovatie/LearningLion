
from DataFetcher.libraries.data_classes.range_enum import Range
from querier.libraries import database, query
from querier.libraries.embedding import Embedding

def run_local_query_stores(prompt):
  print("Querying stores")
  embed = Embedding()
  data = database.Database(embed)
  data.setup_database(range=Range.Tiny)
  querier = query.Query()
  querier.setup_querier(data)
  return querier.query(prompt)
  
def getDocumentBlobFromDatabase(UUID):
  embed = Embedding()
  data = database.Database(embed)
  db_connection = data.get_database_connection()
  cursor = db_connection.cursor()
  cursor.execute("SELECT document FROM documents WHERE UUID = ?", (UUID,))
  item = cursor.fetchone()
  cursor.close()
  data.close_database_connection()
      # No need to close the connection here; it will be closed automatically
  if item:
      return item[0]
  else:
      return None  # Or handle the case where the UUID doesn't exist