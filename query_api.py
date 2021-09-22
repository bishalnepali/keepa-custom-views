import requests
import urllib
import show_details
API_KEY = 'USE_API_KEY_FILE'
query_file  = input('Enter a query: ')


# Adding the API Key to the URL
parse_url = query_file.replace('YOUR_API_KEY',API_KEY)
decoded_url = urllib.parse.unquote(parse_url)

response = requests.get(decoded_url)
json_data = response.json()
print(json_data)
total_results = json_data['totalResults']
asin_list = json_data['asinList']
show_details.main(asin_list)
print("Done")