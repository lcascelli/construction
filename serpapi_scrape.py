#Final full script
import pandas as pd
from serpapi.google_search import GoogleSearch


#CREATE MORE SOPHISTICATED LIST CREATION FOR PROJECT MATERIALS.
concrete_search_df = pd.read_excel('C:/Users/Liam/Documents/00 Python/streamlit/construction_projects/Estimates All.xlsx', sheet_name='Concrete_List')
concrete_search = concrete_search_df['Concrete_Ingredients'].tolist()

plumbing_search_df = pd.read_excel('C:/Users/Liam/Documents/00 Python/streamlit/construction_projects/Estimates All.xlsx', sheet_name='Plumbing_List')
plumbing_search = plumbing_search_df['Plumbing_Ingredients'].tolist()

tenant_improvement_df = pd.read_excel('C:/Users/Liam/Documents/00 Python/streamlit/construction_projects/Estimates All.xlsx', sheet_name='Tenant_Improve_List')
tenant_improvement_search = tenant_improvement_df['Tenant_Improve_Ingredients'].tolist()

def fetch_shopping_results(query):
    params = {
        "engine": "google_shopping",
        "q": query,
        "uule": "Long Beach, California, United States",
        "hl": "en",
        "gl": "us",
        "google_domain": "google.com",
        "api_key": "b765ff492f14ad72644e647a388f1e2f973eca27edc96a7c435601fc0d2230dd"
    }
    return_data = GoogleSearch(params).get_dict()
    return return_data
def results_to_dataframe(return_data, product_type):
    items = return_data.get("shopping_results", [])
    data = []
    for item in items:
        data.append({
            "Title": item.get("title"),
            "Price": item.get("price"),
            "Store": item.get("source"),
            "Link": item.get("product_link") 
        })
    df = pd.DataFrame(data)
    df['Product Type'] = product_type
    
    return df

dataframes = []

#TEMPORARY LOOPS. NEED TO CREATE LOOP FOR ALL MATERIALS 

for item in concrete_search:
    return_data = fetch_shopping_results(item)
    df = results_to_dataframe(return_data, item)
    df['Project Source'] = "concrete project" 
    dataframes.append(df)

for item in plumbing_search: 
    return_data = fetch_shopping_results(item)
    df = results_to_dataframe(return_data, item)
    df['Project Source'] = "plumbing project" 
    dataframes.append(df)

for item in tenant_improvement_search:
    return_data = fetch_shopping_results(item)
    df = results_to_dataframe(return_data, item)
    df['Project Source'] = "tenant improvement project" 
    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)
combined_df["Price"] = pd.to_numeric(combined_df["Price"].str.replace("$", "").str.replace(",", ""), errors="coerce")
print(combined_df)
combined_df.to_excel('C:/Users/Liam/Documents/00 Python/streamlit/construction_projects/Final_Search_Results.xlsx', index=False)