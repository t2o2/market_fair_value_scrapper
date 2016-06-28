# from splinter import Browser
#
# with Browser() as browser:
#     # Visit URL
#     baseurl = "http://www.morningstar.com/market-valuation/market-fair-value-graph.aspx"
#     query = "?Ticker=AllStock&Period=M1"
#     url = baseurl + query
#     browser.visit(url)
#

import urllib.request
from PIL import Image
import pytesseract
import re
import os

overall_list = [
    # Super Sector
    'Cyclical',
    'Defensive',
    'Sensitive',
    # Sector
    'Basic Materials',
    'Consumer Cyclical',
    'Financial Services',
    'Real Estate',
    'Consumer Defensive',
    'Healthcare',
    'Utilities',
    'Communication Services',
    'Energy',
    'Industrials',
    'Technology',
    # Industry - Basic Materials
    'Agricultural Inputs',
    'Aluminum',
    'Building Materials',
    'Chemicals',
    'Coal',
    'Copper',
    'Gold',
    'Industrial Metals & Minerals',
    'Lumber & Wood Production',
    'Paper & Paper Products',
    'Silver',
    'Specialty Chemicals',
    'Steel',
    # Industry - Consumer Cyclical
    'Advertising Agencies',
    'Apparel Manufacturing',
    'Apparel Stores',
    'Auto & Truck Dealerships',
    'Auto Manufacturers',
    'Auto Parts',
    'Broadcasting - Radio',
    'Broadcasting - TV',
    'Department Stores',
    'Footwear & Accessories',
    'Gambling',
    'Home Furnishings & Fixtures',
    'Home Improvement Stores',
    'Leisure',
    'Lodging',
    'Luxury Goods',
    'Marketing Services',
    'Media - Diversified',
    'Packaging & Containers',
    'Personal Services',
    'Publishing',
    'Recreational Vehicles',
    'Residential Construction',
    'Resorts & Casinos',
    'Restaurants',
    'Rubber & Plastics',
    'Specialty Retail',
    'Textile Manufacturing'
    # Industry - Financial Services
    'Asset Management',
    'Banks - Global',
    'Banks - Regional - Africa',
    'Banks - Regional - Asia',
    'Banks - Regional - Australia',
    'Banks - Regional - Canada',
    'Banks - Regional - Europe',
    'Banks - Regional - Latin America',
    'Banks - Regional - US',
    'Capital Markets',
    'Credit Services',
    'Financial Exchanges',
    'Insurance - Diversified',
    'Insurance - Life',
    'Insurance - Property & Casualty',
    'Insurance - Reinsurance',
    'Insurance - Specialty',
    'Insurance Brokers',
    'Savings & Cooperative Banks',
    'Specialty Finance',
    # Industry - Real Estate
    'Real Estate - General',
    'Real Estate Services',
    'REIT - Diversified',
    'REIT - Healthcare Facilities',
    'REIT - Hotel & Motel',
    'REIT - Industrial',
    'REIT - Office',
    'REIT - Residential',
    'REIT - Retail',
    # Industry - Consumer Defensive
    'Beverages - Brewers',
    'Beverages - Soft Drinks',
    'Beverages - Wineries & Distilleries',
    'Confectioners',
    'Discount Stores',
    'Education & Training Services',
    'Farm Products',
    'Food Distribution',
    'Grocery Stores',
    'Household & Personal Products',
    'Packaged Foods',
    'Pharmaceutical Retailers',
    'Tobacco',
    # Industry - Healthcare
    'Biotechnology',
    'Diagnostics & Research',
    'Drug Manufacturers - Major',
    'Drug Manufacturers - Specialty & Generic',
    'Health Care Plans',
    'Long-Term Care Facilities',
    'Medical Care',
    'Medical Devices',
    'Medical Distribution',
    'Medical Instruments & Supplies',
    # Industry - Utilities
    'Utilities - Diversified',
    'Utilities - Independent Power Producers',
    'Utilities - Regulated Electric',
    'Utilities - Regulated Gas',
    'Utilities - Regulated Water',
    # Industry - Communication Services
    'Pay TV',
    'Telecom Services',
    # Industry - Energy
    'Oil & Gas Drilling',
    'Oil & Gas E&P',
    'Oil & Gas Equipment & Services',
    'Oil & Gas Integrated',
    'Oil & Gas Midstream',
    'Oil & Gas Refining & Marketing',
    # Industry - Industrials
    'Aerospace & Defense',
    'Airlines',
    'Airports & Air Services',
    'Business Equipment',
    'Business Services',
    'Conglomerates',
    'Diversified Industrials',
    'Engineering & Construction',
    'Farm & Construction Equipment',
    'Industrial Distribution',
    'Infrastructure Operations',
    'Integrated Shipping & Logistics',
    'Metal Fabrication',
    'Pollution & Treatment Controls',
    'Railroads',
    'Rental & Leasing Services',
    'Security & Protection Services',
    'Shipping & Ports',
    'Staffing & Outsourcing Services',
    'Tools & Accessories',
    'Truck Manufacturing',
    'Trucking',
    'Waste Management',
    # Industry - Technology
    'Communication Equipment',
    'Computer Distribution',
    'Computer Systems',
    'Consumer Electronics',
    'Contract Manufacturers',
    'Data Storage',
    'Electronic Components',
    'Electronic Gaming & Multimedia',
    'Electronics Distribution',
    'Health Information Services',
    'Information Technology Services',
    'Internet Content & Information',
    'Scientific & Technical Instruments',
    'Semiconductor Equipment & Materials',
    'Semiconductor Memory',
    'Semiconductors',
    'Software - Application',
    'Software - Infrastructure',
    'Solar',
]

overview = {}
for name in overall_list:
    print(name)
    with open(name + '.png', "wb") as f:
        url_name = name.replace(' ', '%20').replace('&', '!')
        url = 'http://www.morningstar.com/market-valuation/market_valuation_graph.aspx?Ticker=' + url_name + '&Period=AL'
        f.write(urllib.request.urlopen(url).read())
    im = Image.open(name + '.png')
    if im.size[0] > 185:
        im = im.crop([0, 0, 190, 25])
    text = pytesseract.image_to_string(im)
    pattern = re.compile(" (\d|l). ?(l|\d)(l|\d)")
    result = pattern.search(text)
    if result is not None:
        overview[name] = float(result.group(0).replace(' ', '').replace('l', '1'))
    else:
        overview[name] = 0
        print(text)

with open('result.csv', 'w') as f:
    for key, value in overview.items():
        f.write(key + ',' + str(value) + '\n')
