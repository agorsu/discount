# Discount
Supermarket discount tracker

## Description
A simple terminal supermarket discount tracker for specials on products between both Coles and Woolworths supermarkets. Both prices are compared to each other with the specials highlighted.

## Getting Started

### Dependencies
* Requests
* Rich

## How to setup
Firstly download or clone this repo and then install the requirements;

1. Clone the repo
`git clone https://github.com/agorsu/discount.git`

2. Navigate to the project folder
`cd discount`

3. Install the requirements
`pip install -r requirements.txt`

4. Run
`python discount.py`

### Adding items
To add items to the tracker, the product code will be needed for your item from each supermarket.
This can be done by the following steps:

1. Search for the product on each supermarket website
2. Open the product page
3. Copy the item code found in the URL

   w<span>ww.c</span>oles.com.au/product/arnott's-tim-tam-original-chocolate-biscuits-200g-<strong>329607</strong>
   w<span>ww.w</span>oolworths.com.au/shop/productdetails/<strong>36066</strong>/arnott-s-tim-tam-original-chocolate-biscuits

5. Add the item code to the relevant supermarket watchlist:

   ```python
   c_watchlist = [9043363, 329607]
   ww_watchlist = [162609, 36066]
   ```

   Item codes are compared to their corresponding supermarket watchlist in the same order.



Give it a star :tada:
---------------------
Did you find this information useful, then give it a star 
