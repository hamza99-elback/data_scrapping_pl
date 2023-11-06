from google.cloud import bigquery
import os
import pandas as pd
# gcloud bigquery datasets list --project=vast-art-396609

class NoTableFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
    pass


os.environ['GOOGLE_APPLICATION_CREDENTIALS']= "./google_bigquery/your-big-query-token-config.json"

class BigQueryService:
    def __init__(self):
        self.client=bigquery.Client()
        
    def get_data_using_query(self, query):
        """Get data from google BigQuery

        Args:
            query (str): _description_
        """
        query_job = self.client.query(query)  # API request
        if (query_job.state =="DONE"):
            rows = query_job.result()  # Waits for query to finish
            for row in rows:
                print(row)
    
    def create_table(self, schema, table_id):
        """Create a table in google BigQuery

        Args:
            schema (list): _description_
            table_name (str): _description_
        """
        
        try:
            # Check if the table exists
            try:
                table_exists = self.client.get_table(table_id, retry=bigquery.DEFAULT_RETRY)
                if table_exists:
                    print(f"Table users_test exists in dataset.")
            except Exception:
                raise NoTableFoundException(message="Table users_test does not exist in dataset.")
        except NoTableFoundException as e:
            print(f"Error when checking Table existance: {e}")
            table = bigquery.Table(table_id, schema=schema)
            table = self.client.create_table(table)  # Make an API request.
            print(
                "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
            )
    def load_data_into_table(self, table_id, data, columns, schema):
        """Load Data into BigQuery Table

        Args:
            table_name (str): _description_
            data (list): _description_
            schema (list): _description_
        """
        
        dataframe = pd.DataFrame(
            data,
            # In the loaded table, the column order reflects the order of the
            # columns in the DataFrame.
            columns=[
                "rank",
                "player_name",
                "goals"
            ]
        )
        job_config = bigquery.LoadJobConfig(
            # Specify a (partial) schema. All columns are always written to the
            # table. The schema is used to assist in data type definitions.
            schema=schema,
            # Optionally, set the write disposition. BigQuery appends loaded rows
            # to an existing table by default, but with WRITE_TRUNCATE write
            # disposition it replaces the table with the loaded data.
            write_disposition="WRITE_TRUNCATE",
        )

        job = self.client.load_table_from_dataframe(
            dataframe, table_id, job_config=job_config
        )  # Make an API request.
        print(job.result())  # Wait for the job to complete.

        # table = client.get_table(table_id)  # Make an API request.
        # print(
        #     "Loaded {} rows and {} columns to {}".format(
        #         table.num_rows, len(table.schema), table_id
        #     )
        # )
        
                
if __name__=="__main__":
    big_query_service=BigQueryService()
    QUERY = (
    'SELECT * FROM `bigquery-public-data.austin_311.311_service_requests` LIMIT 10')
    big_query_service.get_data_using_query(query=QUERY)
        
        
    