import requests
import pandas as pd

sql = "SELECT * from EPD_202009 limit 1000"
url = "https://opendata.nhsbsa.net/api/3/action/datastore_search_sql?sql=%s" % sql

data = requests.get(url)

records = data.json()['result']['result']['records']

df = pd.DataFrame(records)

analysis = df.groupby(['BNF_CODE', 'CHEMICAL_SUBSTANCE_BNF_DESCR'])['QUANTITY'].sum()
print(analysis)

# analysis.to_csv('my_data.csv')

