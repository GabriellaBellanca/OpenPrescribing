import requests
import pandas as pd

def run_sql(sql_query):
    url = "https://opendata.nhsbsa.net/api/3/action/datastore_search_sql?sql=%s" % sql_query
    data = requests.get(url)
    records = data.json()['result']['result']['records']
    return pd.DataFrame(records), data

df, data = run_sql("SELECT * from EPD_202009 limit 1000")

''' Function takes the name of a drug (case insensitive)' and gives bnf codes '''
def get_bnf_codes(drug):
    response = requests.get('https://openprescribing.net/api/1.0/bnf_code/?format=json&q=%s' % drug)
    data = response.json()
    return pd.DataFrame(data)

amoxicillin_codes = get_bnf_codes('amoxicillin')
print(amoxicillin_codes)

def get_spending_by_month_for_bnf_code(bnf_code):
    response = requests.get('https://openprescribing.net/api/1.0/spending/?format=json&code=%s' % bnf_code)
    data = response.json()
    return pd.DataFrame(data)


def get_ccg_spending_by_month_for_bnf_code(bnf_code):
    response = requests.get('https://openprescribing.net/api/1.0/spending_by_ccg/?format=json&code=%s' % bnf_code)
    data = response.json()
    return pd.DataFrame(data)

get_ccg_spending_by_month_for_bnf_code(amoxicillin_codes.iloc[0]['id'])