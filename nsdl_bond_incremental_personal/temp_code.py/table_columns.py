import requests
import pandas as pd

# Define the URL and headers for the request
url = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/defaultdetail?isin=INE005X08026"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.indiabondinfo.nsdl.com/',
    'Origin': 'https://www.indiabondinfo.nsdl.com'
}

# Use a session to handle cookies
session = requests.Session()

try:
    # Send the GET request
    response = session.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        print(f"Response Content: {data}")

        # Create a DataFrame from the response data
        df = pd.DataFrame(data)
        
        # Add the "default_details_" prefix to each column name
        df.columns = [f"default_details_{col}" for col in df.columns]
        
        # Save the DataFrame to an Excel file
        df.to_excel('output_default_details.xlsx', index=False)
        
        print("Excel file created successfully.")
    else:
        print(f"Failed to retrieve data: {response.content}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")



















# import requests
# import pandas as pd

# # Define the URL and headers for the request
# url = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/credit-ratings?isin=INE001W07011"
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     'Accept': 'application/json',
#     'Referer': 'https://www.indiabondinfo.nsdl.com/',
#     'Origin': 'https://www.indiabondinfo.nsdl.com'
# }

# # Use a session to handle cookies
# session = requests.Session()

# try:
#     # Send the GET request
#     response = session.get(url, headers=headers)
#     print(f"Status Code: {response.status_code}")
    
#     # Check if the request was successful
#     if response.status_code == 200:
#         data = response.json()
#         print(f"Response Content: {data}")

#         # Initialize an empty list to store extracted key-value pairs
#         extracted_data = []

#         # Function to extract key-value pairs from each rating section
#         def extract_ratings(ratings, rating_type):
#             for rating in ratings:
#                 rating['type'] = rating_type
#                 extracted_data.append(rating)

#         # Extract key-value pairs from 'currentRatings'
#         if 'currentRatings' in data:
#             extract_ratings(data['currentRatings'], 'currentRatings')

#         # Extract key-value pairs from 'earlierRatings'
#         if 'earlierRatings' in data:
#             extract_ratings(data['earlierRatings'], 'earlierRatings')

#         # Create a DataFrame from the extracted data
#         df = pd.DataFrame(extracted_data)

#         # Rename the columns to add 'credit_rating_' prefix
#         df.columns = [f'credit_rating_{col}' for col in df.columns]
        
#         # Save the DataFrame to an Excel file
#         df.to_excel('output_ratings.xlsx', index=False)
        
#         print("Excel file created successfully.")
#     else:
#         print(f"Failed to retrieve data: {response.content}")
# except requests.exceptions.RequestException as e:
#     print(f"Request failed: {e}")



# import requests
# import pandas as pd
# import json

# # Define the URL and headers for the request
# url = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/credit-ratings?isin=INE001W07011"
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     'Accept': 'application/json',
#     'Referer': 'https://www.indiabondinfo.nsdl.com/',
#     'Origin': 'https://www.indiabondinfo.nsdl.com'
# }

# # Use a session to handle cookies
# session = requests.Session()

# try:
#     # Send the GET request
#     response = session.get(url, headers=headers)
#     print(f"Status Code: {response.status_code}")
    
#     # Check if the request was successful
#     if response.status_code == 200:
#         data = response.json()
#         print(f"Response Content: {data}")

#          # Initialize an empty dictionary to store extracted key-value pairs
#         extracted_data = {}

#         # Extract the entire 'currentRatings' and 'earlierRatings' arrays as JSON strings
#         extracted_data['currentRatings'] = json.dumps(data.get('currentRatings', []))
#         extracted_data['earlierRatings'] = json.dumps(data.get('earlierRatings', []))

#         # Create a DataFrame from the extracted data
#         df = pd.DataFrame([extracted_data])
        
#         # Save the DataFrame to an Excel file
#         df.to_excel('output.xlsx', index=False)
        
#         print("Excel file created successfully.")
#     else:
#         print(f"Failed to retrieve data: {response.content}")
# except requests.exceptions.RequestException as e:
#     print(f"Request failed: {e}")










# import requests
# import pandas as pd

# # Define the URL and headers for the request
# url = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/instruments?isin=INE001W07011"
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     'Accept': 'application/json',
#     'Referer': 'https://www.indiabondinfo.nsdl.com/',
#     'Origin': 'https://www.indiabondinfo.nsdl.com'
# }

# # Use a session to handle cookies
# session = requests.Session()

# try:
#     # Send the GET request
#     response = session.get(url, headers=headers)
#     print(f"Status Code: {response.status_code}")
    
#     # Check if the request was successful
#     if response.status_code == 200:
#         data = response.json()
#         print(f"Response Content: {data}")

#         # Initialize an empty dictionary to store extracted key-value pairs
#         extracted_data = {}

#         # Extract key-value pairs from 'instruments'
#         instruments_details = data['instrumentsVo']['instruments']
#         for key, value in instruments_details.items():
#             extracted_data[f"instruments_details_{key}"] = value

#         # Extract key-value pairs from 'creditEnhancement'
#         credit_enhancement = data['instrumentsVo']['creditEnhancement']
#         for key, value in credit_enhancement.items():
#             if isinstance(value, list) and value:
#                 for sub_key, sub_value in value[0].items():
#                     extracted_data[f"credit_enhancement_{key}"] = sub_value
#             else:
#                 extracted_data[f"credit_enhancement_{key}"] = value

#         # Extract key-value pairs from 'furtherIssue'
#         further_issue = data['instrumentsVo']['furtherIssue']['furtherIssueVo']
#         for item in further_issue:
#             for key, value in item.items():
#                 extracted_data[f"furtherissue_{key}"] = value

#         # Extract key-value pairs from 'convertability'
#         convertability = data['instrumentsVo']['convertability']
#         for key, value in convertability.items():
#             if isinstance(value, list) and value:
#                 for sub_key, sub_value in value[0].items():
#                     extracted_data[f"convertability_{key}"] = sub_value
#             else:
#                 extracted_data[f"convertability_{key}"] = value

#         # Extract key-value pairs from 'assetCover'
#         asset_cover = data['instrumentsVo']['assetCover']
#         for key, value in asset_cover.items():
#             if isinstance(value, list) and value:
#                 for sub_key, sub_value in value[0].items():
#                     extracted_data[f"asset_cover_{key}"] = sub_value
#             else:
#                 extracted_data[f"asset_cover_{key}"] = value

#         # Extract key-value pairs from 'tradePrice'
#         trade_price = data['instrumentsVo']['tradePrice']['tradeList']
#         for item in trade_price:
#             for key, value in item.items():
#                 extracted_data[f"tradeprice_{key}"] = value

#         # Create a DataFrame from the extracted data
#         df = pd.DataFrame([extracted_data])
        
#         # Save the DataFrame to an Excel file
#         df.to_excel('output_results.xlsx', index=False)
        
#         print("Excel file created successfully.")
#     else:
#         print(f"Failed to retrieve data: {response.content}")
# except requests.exceptions.RequestException as e:
#     print(f"Request failed: {e}")


















# import requests
# import pandas as pd

# # Define the URL and headers for the request
# url = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/instruments?isin=INE001W07011"
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     'Accept': 'application/json',
#     'Referer': 'https://www.indiabondinfo.nsdl.com/',
#     'Origin': 'https://www.indiabondinfo.nsdl.com'
# }

# # Use a session to handle cookies
# session = requests.Session()

# try:
#     # Send the GET request
#     response = session.get(url, headers=headers)
#     print(f"Status Code: {response.status_code}")
    
#     # Check if the request was successful
#     if response.status_code == 200:
#         data = response.json()
#         print(f"Response Content: {data}")
        
#         # Extract the required keys and values
#         instruments_data = data['instrumentsVo']['instruments']
#         credit_enhancement_data = data['instrumentsVo']['creditEnhancement']
#         further_issue_data = data['instrumentsVo']['furtherIssue']['furtherIssueVo'][0]
#         convertability_data = data['instrumentsVo']['convertability']
#         asset_cover_data = data['instrumentsVo']['assetCover']
#         trade_price_data = data['instrumentsVo']['tradePrice']['tradeList'][0]
        
#         # Combine all extracted data into a single dictionary
#         combined_data = {**instruments_data, **credit_enhancement_data, **further_issue_data, 
#                          **convertability_data, **asset_cover_data, **trade_price_data}
        
#         # Create a DataFrame from the combined data
#         df = pd.DataFrame([combined_data])
        
#         # Save the DataFrame to an Excel file
#         df.to_excel('output.xlsx', index=False)
        
#         print("Excel file created successfully.")
#     else:
#         print(f"Failed to retrieve data: {response.content}")
# except requests.exceptions.RequestException as e:
#     print(f"Request failed: {e}")



# import requests
# import pandas as pd

# # Define the URL and headers for the request
# url = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/instruments?isin=INE001W07011"
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     'Accept': 'application/json',
#     'Referer': 'https://www.indiabondinfo.nsdl.com/',
#     'Origin': 'https://www.indiabondinfo.nsdl.com'
# }

# # Use a session to handle cookies
# session = requests.Session()

# try:
#     # Send the GET request
#     response = session.get(url, headers=headers)
#     print(f"Status Code: {response.status_code}")
    
#     # Check if the request was successful
#     if response.status_code == 200:
#         data = response.json()
#         print(f"Response Content: {data}")

#         # Initialize an empty dictionary to store extracted key-value pairs
#         extracted_data = {}

#         # Extract key-value pairs from 'instruments'
#         instruments_data = data['instrumentsVo']['instruments']
#         for key, value in instruments_data.items():
#             extracted_data[key] = value

#         # Extract key-value pairs from 'creditEnhancement'
#         credit_enhancement_data = data['instrumentsVo']['creditEnhancement']
#         for key, value in credit_enhancement_data.items():
#             if isinstance(value, list):
#                 extracted_data[key] = value[0] if value else None
#             else:
#                 extracted_data[key] = value

#         # Extract key-value pairs from 'furtherIssue'
#         further_issue_data = data['instrumentsVo']['furtherIssue']['furtherIssueVo'][0]
#         for key, value in further_issue_data.items():
#             extracted_data[key] = value

#         # Extract key-value pairs from 'convertability'
#         convertability_data = data['instrumentsVo']['convertability']
#         for key, value in convertability_data.items():
#             if isinstance(value, list):
#                 extracted_data[key] = value[0] if value else None
#             else:
#                 extracted_data[key] = value

#         # Extract key-value pairs from 'assetCover'
#         asset_cover_data = data['instrumentsVo']['assetCover']
#         for key, value in asset_cover_data.items():
#             if isinstance(value, list):
#                 extracted_data[key] = value[0] if value else None
#             else:
#                 extracted_data[key] = value

#         # Extract key-value pairs from 'tradePrice'
#         trade_price_data = data['instrumentsVo']['tradePrice']['tradeList'][0]
#         for key, value in trade_price_data.items():
#             extracted_data[key] = value

#         # Create a DataFrame from the extracted data
#         df = pd.DataFrame([extracted_data])
#         print("df========\n\n", df)
        
#         # Save the DataFrame to an Excel file
#         df.to_excel('output123.xlsx', index=False)
        
#         print("Excel file created successfully.")
#     else:
#         print(f"Failed to retrieve data: {response.content}")
# except requests.exceptions.RequestException as e:
#     print(f"Request failed: {e}")
