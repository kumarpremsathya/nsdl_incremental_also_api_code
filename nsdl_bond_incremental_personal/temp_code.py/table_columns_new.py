import requests
import pandas as pd

# Function to fetch data from a given URL
def fetch_data(url, headers):
    session = requests.Session()
    try:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve data: {response.content}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Function to process and extract ratings data
def process_ratings(data, isin):
    extracted_data_ratings = []

    def extract_ratings(ratings, rating_type):
        for rating in ratings:
            rating['type'] = rating_type
            rating['isin'] = isin
            rating['instrument_type'] = 'debentures'
            extracted_data_ratings.append(rating)

    if 'currentRatings' in data:
        extract_ratings(data['currentRatings'], 'currentRatings')
    if 'earlierRatings' in data:
        extract_ratings(data['earlierRatings'], 'earlierRatings')

    df_ratings = pd.DataFrame(extracted_data_ratings)
    if not df_ratings.empty:
        df_ratings.columns = [f'credit_rating_{col}' for col in df_ratings.columns]
    return df_ratings

# Function to process and extract instruments data
def process_instruments(data, isin):
    extracted_data_instruments = {}

    instruments_details = data['instrumentsVo']['instruments']
    for key, value in instruments_details.items():
        extracted_data_instruments[f"instruments_details_{key}"] = value

    credit_enhancement = data['instrumentsVo']['creditEnhancement']
    for key, value in credit_enhancement.items():
        if isinstance(value, list) and value:
            for sub_key, sub_value in value[0].items():
                extracted_data_instruments[f"credit_enhancement_{key}"] = sub_value
        else:
            extracted_data_instruments[f"credit_enhancement_{key}"] = value

    further_issue = data['instrumentsVo']['furtherIssue']['furtherIssueVo']
    for item in further_issue:
        for key, value in item.items():
            extracted_data_instruments[f"furtherissue_{key}"] = value

    convertability = data['instrumentsVo']['convertability']
    for key, value in convertability.items():
        if isinstance(value, list) and value:
            for sub_key, sub_value in value[0].items():
                extracted_data_instruments[f"convertability_{key}"] = sub_value
        else:
            extracted_data_instruments[f"convertability_{key}"] = value

    asset_cover = data['instrumentsVo']['assetCover']
    for key, value in asset_cover.items():
        if isinstance(value, list) and value:
            for sub_key, sub_value in value[0].items():
                extracted_data_instruments[f"asset_cover_{key}"] = sub_value
        else:
            extracted_data_instruments[f"asset_cover_{key}"] = value

    trade_price = data['instrumentsVo']['tradePrice']['tradeList']
    for item in trade_price:
        for key, value in item.items():
            extracted_data_instruments[f"tradeprice_{key}"] = value

    # Create a DataFrame with 'isin' and 'instrument_type' as the first columns
    df_instruments = pd.DataFrame([extracted_data_instruments])
    df_instruments.insert(0, 'isin', isin)
    df_instruments.insert(1, 'instrument_type', 'debentures')
    
    return df_instruments

# List of ISIN numbers to process
isin_numbers = ['INE001W07011','INE001W08126','INE001W08134','INE001W08142','INE001W08159','INE001W08167','INE002A07809','INE002A08534','INE002A08542','INE002A08567']  # Add more ISIN numbers as needed

# URL and headers for the requests
base_url_ratings = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/credit-ratings?isin={}"
base_url_instruments = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/instruments?isin={}"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.indiabondinfo.nsdl.com/',
    'Origin': 'https://www.indiabondinfo.nsdl.com'
}


all_combined_data = []

for isin in isin_numbers:
    # Fetch data for ratings and instruments
    url_ratings = base_url_ratings.format(isin)
    url_instruments = base_url_instruments.format(isin)
    
    data_ratings = fetch_data(url_ratings, headers)
    data_instruments = fetch_data(url_instruments, headers)
    
    if data_ratings:
        df_ratings = process_ratings(data_ratings, isin).reset_index(drop=True)  # Reset index here
    else:
        df_ratings = pd.DataFrame(columns=[f'credit_rating_{col}' for col in ['isin', 'type']])  # Empty DataFrame with expected columns

    if data_instruments:
        df_instruments = process_instruments(data_instruments, isin).reset_index(drop=True)  # Reset index here
    else:
        df_instruments = pd.DataFrame(columns=['isin', 'instrument_type'])  # Empty DataFrame with expected columns

    if not df_ratings.empty and not df_instruments.empty:
        # Repeat df_instruments for each row in df_ratings
        df_instruments_repeated = pd.concat([df_instruments] * len(df_ratings), ignore_index=True).reset_index(drop=True)  # Reset index here
        combined_data = pd.concat([df_instruments_repeated,df_ratings] , axis=1, ignore_index=True)
        combined_data.columns = list(df_instruments.columns)+list(df_ratings.columns)   # Resetting column names after concatenation
    else:
        combined_data = pd.concat([df_instruments, df_ratings], ignore_index=True)

    all_combined_data.append(combined_data)

# Combine all data into a single DataFrame
final_combined_df = pd.concat(all_combined_data, ignore_index=True)

# Save the combined DataFrame to an Excel file
final_combined_df.to_excel('output_combined.xlsx', index=False)

print("Excel file created successfully.")







import requests
import pandas as pd

# Define the URL and headers for the request
url = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/restructuring?isin=INE001W08126"
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

        # Extract the required key-value pairs for the first row
        row1 = {
            "restructuring_corporateActionEvent": data.get("corporateActionEvent"),
            "restructuring_isin": data.get("isin"),
            "restructuring_secType": data.get("secType"),
            "restructuring_allotmentDate": data.get("allotmentDate"),
            "restructuring_redemptionDate": data.get("redemptionDate"),
            "restructuring_category": data.get("category"),
            "restructuring_couponRate": data.get("couponRate"),
            "restructuring_couponBasis": data.get("couponBasis"),
            "restructuring_interestPaymentFrequency": data.get("interestPaymentFrequency"),
            "restructuring_type": "new"
        }
        
        # Extract the required key-value pairs for the second row
        row2 = {
            "restructuring_corporateActionEvent": data.get("corporateActionEvent"),  # Reuse the same value if needed
            "restructuring_isin": data.get("parentIsin"),
            "restructuring_secType": data.get("parentSecType"),
            "restructuring_allotmentDate": data.get("parentAllotmentDate"),
            "restructuring_redemptionDate": data.get("parentRedemptionDate"),
            "restructuring_category": data.get("parentCategory"),
            "restructuring_couponRate": data.get("parentCouponRate"),
            "restructuring_couponBasis": data.get("parentCouponBasis"),
            "restructuring_interestPaymentFrequency": data.get("parentInterestPaymentFrequency"),
            "restructuring_type": "old"
        }
        
        # Create a DataFrame from the extracted data
        df = pd.DataFrame([row1, row2])
        
        # Save the DataFrame to an Excel file
        df.to_excel('output_restructuring.xlsx', index=False)
        
        print("Excel file created successfully.")
    else:
        print(f"Failed to retrieve data: {response.content}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")




import requests
import pandas as pd

# Define the URL and headers for the request
url = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/keycontacts?isin=INE008A08R30"
# url = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/keycontacts?isin=INE001W08126"


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

        # Initialize a list to hold all rows of data
        rows = []

        # Extract and append issuer data
        issuer_data = {
            "key_contacts_arranger": None,
            "key_contacts_Name": None,
            "key_contacts_contact_person": data.get("issuerCompOffName"),
            "key_contacts_office_address": data.get("issuerRegAddr"),
            "key_contacts_contact_details": None,
            "key_contacts_email": data.get("issuerCompOffEmail"),
            "key_contacts_website": None,
            "key_contacts_type": "issuer"
        }
        rows.append(issuer_data)

        # Extract and append registrar data
        registrar_data = {
            "key_contacts_arranger": None,
            "key_contacts_Name": data.get("registrar"),
            "key_contacts_contact_person": data.get("regContactPerson"),
            "key_contacts_office_address": data.get("regOffAddr"),
            "key_contacts_contact_details": data.get("regContact"),
            "key_contacts_email": data.get("regCompOffEmail"),
            "key_contacts_website": data.get("regWebAddr"),
            "key_contacts_type": "registrar"
        }
        rows.append(registrar_data)

        # Extract and append debenture trustee data
        debenture_trustee_data = {
            "key_contacts_arranger": None,
            "key_contacts_Name": data.get("debtTrusteeName"),
            "key_contacts_contact_person": None,
            "key_contacts_office_address": data.get("debtTrusteeAddr"),
            "key_contacts_contact_details": data.get("debtTrusteeContact"),
            "key_contacts_email": data.get("debtTrusteeCompOffEmail"),
            "key_contacts_website": data.get("debtTrusteeWebAddr"),
            "key_contacts_type": "debenture_trustee"
        }
        rows.append(debenture_trustee_data)

        # Extract and append lead data
        lead_data = {
            "key_contacts_arranger": None,
            "key_contacts_Name": data.get("leadName'"),
            "key_contacts_contact_person": None,
            "key_contacts_office_address": data.get("leadAddr"),
            "key_contacts_contact_details": data.get("leadContact"),
            "key_contacts_email": data.get("leadCompOffEmail"),
            "key_contacts_website": data.get("leadWebAddr"),
            "key_contacts_type": "lead"
        }
        rows.append(lead_data)

         # Extract and append arranger data if not None
        if data.get("arrangers") is not None:
            for arranger in data.get("arrangers", []):
                arranger_data = {
                    "key_contacts_arranger": arranger.get("arranger"),
                    "key_contacts_Name":  None,
                    "key_contacts_contact_person": arranger.get("contactPerson"),
                    "key_contacts_office_address": arranger.get("regOffAddr"),
                    "key_contacts_contact_details": arranger.get("contact"),
                    "key_contacts_email": arranger.get("email"),
                    "key_contacts_website": arranger.get("website"),
                    "key_contacts_type": "arranger"
                }
                rows.append(arranger_data)

        # Create a DataFrame from the rows
        df = pd.DataFrame(rows)
        
        # Save the DataFrame to an Excel file
        df.to_excel('output_key_contacts.xlsx', index=False)
        
        print("Excel file created successfully.")
    else:
        print(f"Failed to retrieve data: {response.content}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
