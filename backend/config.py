import os
import dotenv

dotenv.load_dotenv()

DB_PASSWORD = os.getenv('DB_PASSWORD')
ENV = os.getenv('ENV')

#test

if ENV == "sample":
    DB_NAME = "sample_data"
else:
    DB_NAME = "prod_data"
