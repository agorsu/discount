import requests
from rich.table import Table
from rich.console import Console

# Supermarket discount tracker - terminal version

# Product codes for each supermarket
c_watchlist = ['9043363', '329607']
ww_watchlist = ['162609', '36066']

def coles(prodID):
    url = "https://www.coles.com.au/api/products"
    payload = {
        "productIds": prodID,
        "storeId": "7663",
        "filters": {}}
    headers = {
        "authority": "www.coles.com.au",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
    response = requests.request("POST", url, json=payload, headers=headers)
    data = response.json()   
    brand = data['results'][0]['brand']
    product_name = data['results'][0]['name']
    price = data['results'][0]['pricing']['now']
    
    # Look for promotionType if exists
    special = False
    for k, v in data['results'][0]['pricing'].items():
        if k == 'promotionType':
            if v:
                special = True
    
    return ['Coles', special, brand + " " + product_name, "{:.2f}".format(price)]

def woolies(prodID, key):
    headers = {"cookie": 'bm_sz=' + key, "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"}
    url = f"https://www.woolworths.com.au/apis/ui/product/detail/{prodID}"
    r = session.request("GET", url, headers=headers)
    data = r.json()
    special = data['Product']['InstoreIsOnSpecial']
    desc = data['Product']['DisplayName']
    price = data['Product']['InstorePrice']
    return ['Woolworths', special, desc, "{:.2f}".format(price)]

c_data=[]
ww_data=[]
session = requests.Session()
console = Console()

# process coles
with console.status('Loading: Coles', spinner='point'):
    for i in c_watchlist:
        row = coles(i)
        c_data.append(row)

# process woolworths
with console.status('Loading: Woolworths', spinner='point'):
    response = session.get('https://www.woolworths.com.au/', headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"})
    cookie = session.cookies.get_dict()
    bm_key = cookie.get('bm_sz')
    for i in ww_watchlist:
        row = woolies(i, bm_key)
        ww_data.append(row)

#rich table
table = Table(title='Discount Tracker')
table.add_column('Product')
table.add_column('Coles', justify='right')
table.add_column('Woolies', justify='right')

#highlight price
for i in range(len(c_data)):
    if ww_data[i][1] and c_data[i][1]:
        table.add_row(c_data[i][2], "[bold yellow]" + c_data[i][3], "[bold yellow]" + ww_data[i][3])
    elif ww_data[i][1]:
        table.add_row(c_data[i][2], c_data[i][3], "[bold yellow]" + ww_data[i][3])
    elif c_data[i][1]:
        table.add_row(c_data[i][2], "[bold yellow]" + c_data[i][3], ww_data[i][3])
    else:
        table.add_row(c_data[i][2], c_data[i][3], ww_data[i][3])

console = Console()
console.print(table)