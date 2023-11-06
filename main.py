from scraper import Scraper
from google_bigquery.connect_to_bigquery import BigQueryService
from google.cloud import bigquery


class Context:
    def __init__(self):
        self.data=[]
        self.state=None
        self.description="nothing"

def main(url):
    context=Context()
    table_id="vast-art-396609.my_data_set_1.players_stats"
    schema=[
    bigquery.SchemaField("rank", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("player_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("goals", "INTEGER", mode="REQUIRED"),
    ]
    big_query_service=BigQueryService()
    big_query_service.create_table(table_id=table_id, schema=schema)
    my_scrapper=Scraper(url=url, context=context)
    my_scrapper.main()
    big_query_service.load_data_into_table(table_id=table_id, data=context.data, columns=["rank", "player_name", "goals"], schema=schema)
    
if __name__== "__main__":
    url= "https://www.premierleague.com/stats/top/players/goals"
    main(url=url)