import requests
import json
from datetime import datetime

DATE = str(datetime.now().date())

url = "https://api.mercadolibre.com/sites/MLA/search?category=MLA3025#json"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
response = json.loads(response.text)
data = response['results']

output_path = "/opt/airflow/dags/data/items.tsv"


def getItemClean(item, key):
    return str(item.get(key, '')).replace("\t", " ").strip() if item.get(key) else "null"

with open(output_path, "w", encoding="utf-8") as file:
    for item in data:
        _id = getItemClean(item, "id")
        title = getItemClean(item, "title").replace("'", "''")  # Escapamos las comillas simples
        price = getItemClean(item, "price")
        thumbnail = getItemClean(item, "thumbnail")
        permalink = getItemClean(item, "permalink")
        seller = getItemClean(item.get('seller', {}), "nickname").replace("'", "''")  # Escapamos las comillas simples

        file.write(f"{_id}\t'{title}'\t{price}\t{thumbnail}\t{permalink}\t'{seller}'\n{DATE}\n") 

    