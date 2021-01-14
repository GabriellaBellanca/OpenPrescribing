#Request module retrives data from websites.
import requests
import pandas as pd

''' Defining Function takes the name of a drug (case insensitive)' and gives bnf codes '''
def get_bnf_codes(drug):
    response = requests.get('https://openprescribing.net/api/1.0/bnf_code/?format=json&q=%s' % drug)
    data = response.json()
    return pd.DataFrame(data)


def get_spending_by_month_for_bnf_code(bnf_code):
    response = requests.get('https://openprescribing.net/api/1.0/spending/?format=json&code=%s' % bnf_code)
    data = response.json()
    return pd.DataFrame(data)


def get_ccg_spending_by_month_for_bnf_code(bnf_code):
    response = requests.get('https://openprescribing.net/api/1.0/spending_by_ccg/?format=json&code=%s' % bnf_code)
    data = response.json()
    return pd.DataFrame(data)

spending_by_bnf_code = {}#create a dictionary
bnf_code_by_drug_name = {}
for drug in ["amoxicillin", "doxycycline", "clarithromycin","Erythromycin"]:
    codes = get_bnf_codes(drug)
    bnf_code_by_drug_name[drug] = codes
    for code in codes["id"]:
        print(code)
        spending_by_bnf_code[code] = get_spending_by_month_for_bnf_code(code)

items = []
for drug in bnf_code_by_drug_name.keys():
    df = bnf_code_by_drug_name[drug]
    df["generic_drug"] = drug
    items.append(df)
drug_lookup = pd.concat(items)

items = []
for bnf_code in spending_by_bnf_code.keys():
    df = spending_by_bnf_code[bnf_code]
    df["bnf_code"] = bnf_code
    items.append(df)
total_spending_drug = pd.concat(items)

merged_data = pd.merge(total_spending_drug,drug_lookup,left_on="bnf_code", right_on="id")

merged_data.pivot_table(values="actual_cost",index="date", columns="generic_drug", aggfunc="sum")

merged_data.pivot_table(values="quantity", index= "date", columns="generic_drug", aggfunc="sum")
