from astrapy import DataAPIClient
import os
from dotenv import load_dotenv



load_dotenv()
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_ENDPOINT =os.getenv("ASTRA_DB_ENDPOINT")

client = DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
db = client.get_database_by_api_endpoint(ASTRA_DB_ENDPOINT)


collection_name = "f1_docs"


if collection_name not in db.list_collection_names():
    db.create_collection(collection_name)
    print(f"Collection '{collection_name}' created.")
else:
    print(f"Collection '{collection_name}' already exists.")
