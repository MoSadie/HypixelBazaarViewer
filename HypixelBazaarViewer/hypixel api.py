import requests
import json
import string

#every Bazaar product: https://api.hypixel.net/skyblock/bazaar/products?key=YourApiKey
#nice spreadsheet with prices: https://docs.google.com/spreadsheets/d/1_ej-xLzpVEvrGmp3JOXRFC5B_gHwJPMpB3SYMC3dDDY/edit#gid=0
print('''  ______ _      _____ __  __ __  __ ______ _____   _____ 
 |  ____| |    |_   _|  \/  |  \/  |  ____|  __ \ / ____|
 | |__  | |      | | | \  / | \  / | |__  | |__) | (___  
 |  __| | |      | | | |\/| | |\/| |  __| |  _  / \___ \ 
 | |    | |____ _| |_| |  | | |  | | |____| | \ \ ____) |
 |_|__  |______|_____|_|  |_|_|  |_|______|_|__\_\_____/ 
 |  _ \   /\    |___  /   /\        /\   |  __ \         
 | |_) | /  \      / /   /  \      /  \  | |__) |        
 |  _ < / /\ \    / /   / /\ \    / /\ \ |  _  /         
 | |_) / ____ \  / /__ / ____ \  / ____ \| | \ \         
 |____/_/____\_\/_____/_/    \_\/_/____\_\_|__\_\        
 \ \    / /_   _|  ____\ \        / /  ____|  __ \       
  \ \  / /  | | | |__   \ \  /\  / /| |__  | |__) |      
   \ \/ /   | | |  __|   \ \/  \/ / |  __| |  _  /       
    \  /   _| |_| |____   \  /\  /  | |____| | \ \       
  ___\/  _|_____|______|   \/  \/   |______|_|  \_\      
 |___ \ / _ \ / _ \/_ |                                  
   __) | | | | | | || |                                  
  |__ <| | | | | | || |                                  
  ___) | |_| | |_| || |                                  
 |____/ \___/ \___/ |_|                                  
                                                         
                               ''')


print()
print()

#Select a product
Product = input('What product you want to see? For example: Wheat\n')
print('Ok, you want to see the product ' + Product)

#making input lowercase 
NormalPName = Product
Product = Product.lower()

# Read/Get API Key
try:
    # Read cached API Key
    with open('apiKey.json', 'r') as apiFile:
        apiKeyString = apiFile.read()

    apiKeyJson = json.loads(apiKeyString)

    if apiKeyJson['success'] == True:
        ApiKey = apiKeyJson['key']
    else:
        raise FileNotFoundError
    
    # Check API Key by sending a request
    payload = {'key': ApiKey}
    request = requests.get('https://api.hypixel.net/key', params=payload)
    jsonData = request.json()

    if jsonData['success'] != True:
        print('Problem encountered testing API key: ' + jsonData['cause'])
        print('Reprompting user for API key.')
        raise FileNotFoundError

except FileNotFoundError:
    ApiKey = input('What is your API key? (use /api new in-game if you do not have one)\n')
    print('Ok, your ApiKey is:  ' + ApiKey)
    with open('apiKey.json', 'w') as apiFile:
        apiKeyJson = { 'success': True, 'key': ApiKey}
        apiFile.write(json.dumps(apiKeyJson))

#Read Merchant Prices

    # read file, or download it if it doesn't exist
try:
    with open('Prices.json', 'r') as myfile:
        data=myfile.read()
except FileNotFoundError:
    print('Downloading latest prices from GitHub...')
    pricesRequest = requests.get("https://raw.githubusercontent.com/wwhtrbbtt/HypixelBazaarViewer/master/HypixelBazaarViewer/Prices.json")
    data = pricesRequest.text
    with open('Prices.json', 'w') as priceFile:
        priceFile.write(data)
        print('Successfully cached merchant prices!')

    # parse data
NPCPrices = json.loads(data)

FileReadSuccses = (NPCPrices['success'])
print('Was reading the merchant prices file a success? ' + 'Yes!' if FileReadSuccses else 'No!')


    #getting the NPC prices
NPCSellPrice = (NPCPrices['productIds'][Product]['MerchantSellPrice'])
NPCBuyPrice = (NPCPrices['productIds'][Product]['MerchantBuyPrice'])

    #printing the prices

print('You can buy ' + NormalPName + ' from an NPC for ' + str(NPCBuyPrice) + ' coins and sell via NPC for ' + str(NPCSellPrice) + ' coins')

ProductId = (NPCPrices['productIds'][Product]['NormalName'])


# Get Bazaar Prices

    #Request Bazaar Prices
payload = {'key': ApiKey}
r = requests.get('https://api.hypixel.net/skyblock/bazaar', params=payload)
#print('`The Api URL is: ' + r.url)
JSONData = (r.json())
result = str(JSONData)


    #Check for successful connection
if JSONData['success'] != True:
    print('Was connecting to the Hypixel API a success? No!')
    print('Here is the cause: ' + JSONData['cause'])
    raise RuntimeError(JSONData['cause'])
else:
    print('Was connecting to the Hypixel API a success? Yes!')


    #Get the requested prices
sellPrice = (JSONData['products'][ProductId]['quick_status']['sellPrice'])
buyPrice = (JSONData['products'][ProductId]['quick_status']['buyPrice'])


    #Round prices
rSellPrice = round(sellPrice, 2)
rBuyPrice = round(buyPrice, 2)

    #Print Prices
print('You can buy ' + NormalPName + ' from the bazaar for ' + str(rBuyPrice) + ' coins and sell it to the bazaar for ' + str(rSellPrice) + ' coins')


    #Calculate Profit
Profit = rSellPrice - NPCBuyPrice
rProfit = round(Profit, 2)

print()
print()
print()
print('--------------------------------------')

if rProfit > 0:
    print('You would make ' + str(rProfit) + ' coins per item with this, do it!')
else:
    print('You would lose coins, ('+ str(rProfit) + ' coins) dont do it!')
