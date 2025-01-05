from flask import Flask, render_template, jsonify, request
import requests
import urllib3
import webbrowser
import pandas as pd

# Flask version 0.1

urllib3.disable_warnings()
session = requests.Session()

product_df = pd.read_csv('data/prodlist.csv')
#prefilled watchlist
watchlist_df = pd.DataFrame({
        'id': [5742, 271],
        'name': ["Red Bull Energy Drink 4x250ml", "Arnott's Tim Tam Original Chocolate Biscuits 200g"],
        'has_exact_match': [True, True],
        'Coles_ID': [9043363, 329607],
        'Woolies_ID': [162609, 36066]})

app = Flask(__name__)

def coles(prodID):
    url = "https://www.coles.com.au/api/products"
    payload = {
        "productIds": prodID,
        "storeId": "7663",
        "filters": {}}
    headers = {
        "authority": "www.coles.com.au",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    try:
        r = requests.request("POST", url, json=payload, headers=headers, verify=False)
        data = r.json()   
        brand = data['results'][0]['brand']
        product_name = data['results'][0]['name']
        price = data['results'][0]['pricing']['now']
        wasprice = data['results'][0]['pricing']['was']
    except requests.ConnectionError:
        print('Unable to connect')
        exit()
    except requests.RequestException as e:
        print(e)
        exit()
        
    # Identify real specials
    special = False
    for k, v in data['results'][0]['pricing'].items():
        if k == 'promotionType':
            if v and wasprice != 0:
                special = True

    return ['Coles', special, brand + " " + product_name, "{:.2f}".format(price)]

def woolies(prodID, key):
    headers = {"cookie": 'bm_sz=' + key, "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"}
    url = f"https://www.woolworths.com.au/apis/ui/product/detail/{prodID}"
    try:
        r = session.request("GET", url, headers=headers)
        data = r.json()
        special = data['Product']['InstoreIsOnSpecial']
        desc = data['Product']['DisplayName']
        price = data['Product']['InstorePrice']
    except requests.ConnectionError:
        print('Unable to connect')
        exit()
    except requests.RequestException as e:
        print(e)
        exit()
    return ['Woolworths', special, desc, "{:.2f}".format(price)]

def query_df(query):
    matches = product_df[product_df["name"].str.contains(query, case=False)]
    return matches.to_dict(orient='records')

def fetch_data():
    c_data=[]
    ww_data=[]
    
    # process coles
    for i in watchlist_df['Coles_ID']:##
        row = coles(i)
        c_data.append(row)

    # process woolworths
    session.get('https://www.woolworths.com.au/', headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"})
    cookie = session.cookies.get_dict()
    bm_key = cookie.get('bm_sz')
    for i in watchlist_df['Woolies_ID']:##
        row = woolies(i, bm_key)
        ww_data.append(row)
    return c_data, ww_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    c_data, ww_data = fetch_data()
    return jsonify(c_data=c_data, ww_data=ww_data)

@app.route("/search")
def search():
    query = request.args.get("query", "").lower()
    results = query_df(query)
    print(len(results), "results")  # Debugging output
    return jsonify(results)

@app.route("/add-item", methods=["POST"])
def add_item():
    global watchlist_df
    data = request.get_json()
    item_id = data.get("id")
    new_item = product_df[product_df['id'] == item_id]
    watchlist_df = pd.concat([watchlist_df, new_item], ignore_index=True)
    print(f'Added: {new_item.iloc[0]['name']}')
    return jsonify({"success": True})

if __name__ == '__main__':
    url = 'http://127.0.0.1:5000'
    webbrowser.open_new(url)
    app.run()

