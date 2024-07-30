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

# Function to process restructuring data
def process_restructuring(data):
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
    
    row2 = {
        "restructuring_corporateActionEvent": data.get("corporateActionEvent"),
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

    return pd.DataFrame([row1, row2])

# Function to process key contacts data
def process_key_contacts(data):
    rows = []

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

    lead_data = {
        "key_contacts_arranger": None,
        "key_contacts_Name": data.get("leadName"),
        "key_contacts_contact_person": None,
        "key_contacts_office_address": data.get("leadAddr"),
        "key_contacts_contact_details": data.get("leadContact"),
        "key_contacts_email": data.get("leadCompOffEmail"),
        "key_contacts_website": data.get("leadWebAddr"),
        "key_contacts_type": "lead"
    }
    rows.append(lead_data)

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

    return pd.DataFrame(rows)



# Function to process and extract default details data
def process_default_details(data):
    # Create a DataFrame from the response data
    df = pd.DataFrame(data)
    
    # Add the "default_details_" prefix to each column name
    df.columns = [f"default_details_{col}" for col in df.columns]
    return df

# List of ISIN numbers to process
isin_numbers = ['INE001W07011','INE001W08126', 'INE008A08R30','INE001W08134','INE001W08142','INE005X08026']

# URL and headers for the requests
base_url_ratings = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/credit-ratings?isin={}"
base_url_instruments = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/instruments?isin={}"
base_url_restructuring = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/restructuring?isin={}"
base_url_key_contacts = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/keycontacts?isin={}"
base_url_default_details = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/defaultdetail?isin={}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.indiabondinfo.nsdl.com/',
    'Origin': 'https://www.indiabondinfo.nsdl.com'
}

all_combined_data = []

for isin in isin_numbers:
    # Fetch data for ratings, instruments, restructuring, key contacts, and default details
    url_ratings = base_url_ratings.format(isin)
    url_instruments = base_url_instruments.format(isin)
    url_restructuring = base_url_restructuring.format(isin)
    url_key_contacts = base_url_key_contacts.format(isin)
    url_default_details = base_url_default_details.format(isin)
    
    data_ratings = fetch_data(url_ratings, headers)
    data_instruments = fetch_data(url_instruments, headers)
    data_restructuring = fetch_data(url_restructuring, headers)
    data_key_contacts = fetch_data(url_key_contacts, headers)
    data_default_details = fetch_data(url_default_details, headers)
    
    # Process each type of data into DataFrames
    if data_ratings:
        df_ratings = process_ratings(data_ratings, isin).reset_index(drop=True)
    else:
        df_ratings = pd.DataFrame(columns=[f'credit_rating_{col}' for col in ['isin', 'type']])  # Empty DataFrame with expected columns

    if data_instruments:
        df_instruments = process_instruments(data_instruments, isin).reset_index(drop=True)
    else:
        df_instruments = pd.DataFrame(columns=['isin', 'instrument_type'])  # Empty DataFrame with expected columns
    
    if data_restructuring:
        df_restructuring = process_restructuring(data_restructuring).reset_index(drop=True)
    else:
        df_restructuring = pd.DataFrame(columns=['restructuring_corporateActionEvent', 'restructuring_isin', 'restructuring_secType', 'restructuring_allotmentDate', 'restructuring_redemptionDate', 'restructuring_category', 'restructuring_couponRate', 'restructuring_couponBasis', 'restructuring_interestPaymentFrequency', 'restructuring_type'])  # Empty DataFrame with expected columns

    if data_key_contacts:
        df_key_contacts = process_key_contacts(data_key_contacts).reset_index(drop=True)
    else:
        df_key_contacts = pd.DataFrame(columns=['key_contacts_arranger', 'key_contacts_Name', 'key_contacts_contact_person', 'key_contacts_office_address', 'key_contacts_contact_details', 'key_contacts_email', 'key_contacts_website', 'key_contacts_type'])  # Empty DataFrame with expected columns

    if data_default_details:
        df_default_details = process_default_details(data_default_details).reset_index(drop=True)
    else:
        
       df_default_details = pd.DataFrame(columns=['default_details_' + col for col in ['srNo','issueNature', 'issueSize', 'interestDueDate', 'redemptionDueDate', 'defaultDetails', 'actualPaymentDetails', 'verificationStatus', 'verificationDate', 'dataSource']])  # Empty DataFrame with expected columns

    
    # Determine the maximum number of rows between df_ratings, df_key_contacts, df_default_details, and df_restructuring
    max_rows = max(len(df_ratings), len(df_key_contacts), len(df_default_details), len(df_restructuring))
    
    # Repeat rows of df_instruments to match max_rows
    df_instruments_repeated = pd.concat([df_instruments] * max_rows, ignore_index=True).reset_index(drop=True)
    
    # Combine df_instruments_repeated with df_ratings, df_restructuring, df_default_details, and df_key_contacts
    combined_data = pd.concat([df_instruments_repeated, df_ratings, df_restructuring, df_default_details, df_key_contacts], axis=1)
    
    all_combined_data.append(combined_data)

# Combine all data into a single DataFrame
final_combined_df = pd.concat(all_combined_data, ignore_index=True)

# Save the combined DataFrame to an Excel file
final_combined_df.to_excel('output_combined_response.xlsx', index=False)

print("Excel file created successfully.")












df_default_details = pd.DataFrame(columns=['default_details_' + col for col in ['srNo','issueNature', 'issueSize', 'interestDueDate', 'redemptionDueDate', 'defaultDetails', 'actualPaymentDetails', 'verificationStatus', 'verificationDate', 'dataSource']])  # Empty DataFrame with expected columns






# import requests
# import pandas as pd

# # Function to fetch data from a given URL
# def fetch_data(url, headers):
#     session = requests.Session()
#     try:
#         response = session.get(url, headers=headers)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             print(f"Failed to retrieve data: {response.content}")
#             return None
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {e}")
#         return None

# # Function to process and extract ratings data
# def process_ratings(data, isin):
#     extracted_data_ratings = []

#     def extract_ratings(ratings, rating_type):
#         for rating in ratings:
#             rating['type'] = rating_type
#             rating['isin'] = isin
#             rating['instrument_type'] = 'debentures'
#             extracted_data_ratings.append(rating)

#     if 'currentRatings' in data:
#         extract_ratings(data['currentRatings'], 'currentRatings')
#     if 'earlierRatings' in data:
#         extract_ratings(data['earlierRatings'], 'earlierRatings')

#     df_ratings = pd.DataFrame(extracted_data_ratings)
#     if not df_ratings.empty:
#         df_ratings.columns = [f'credit_rating_{col}' for col in df_ratings.columns]
#     return df_ratings

# # Function to process and extract instruments data
# def process_instruments(data, isin):
#     extracted_data_instruments = {}

#     instruments_details = data['instrumentsVo']['instruments']
#     for key, value in instruments_details.items():
#         extracted_data_instruments[f"instruments_details_{key}"] = value

#     credit_enhancement = data['instrumentsVo']['creditEnhancement']
#     for key, value in credit_enhancement.items():
#         if isinstance(value, list) and value:
#             for sub_key, sub_value in value[0].items():
#                 extracted_data_instruments[f"credit_enhancement_{key}"] = sub_value
#         else:
#             extracted_data_instruments[f"credit_enhancement_{key}"] = value

#     further_issue = data['instrumentsVo']['furtherIssue']['furtherIssueVo']
#     for item in further_issue:
#         for key, value in item.items():
#             extracted_data_instruments[f"furtherissue_{key}"] = value

#     convertability = data['instrumentsVo']['convertability']
#     for key, value in convertability.items():
#         if isinstance(value, list) and value:
#             for sub_key, sub_value in value[0].items():
#                 extracted_data_instruments[f"convertability_{key}"] = sub_value
#         else:
#             extracted_data_instruments[f"convertability_{key}"] = value

#     asset_cover = data['instrumentsVo']['assetCover']
#     for key, value in asset_cover.items():
#         if isinstance(value, list) and value:
#             for sub_key, sub_value in value[0].items():
#                 extracted_data_instruments[f"asset_cover_{key}"] = sub_value
#         else:
#             extracted_data_instruments[f"asset_cover_{key}"] = value

#     trade_price = data['instrumentsVo']['tradePrice']['tradeList']
#     for item in trade_price:
#         for key, value in item.items():
#             extracted_data_instruments[f"tradeprice_{key}"] = value

#     # Create a DataFrame with 'isin' and 'instrument_type' as the first columns
#     df_instruments = pd.DataFrame([extracted_data_instruments])
#     df_instruments.insert(0, 'isin', isin)
#     df_instruments.insert(1, 'instrument_type', 'debentures')
    
#     return df_instruments

# # Function to process restructuring data
# def process_restructuring(data):
#     row1 = {
#         "restructuring_corporateActionEvent": data.get("corporateActionEvent"),
#         "restructuring_isin": data.get("isin"),
#         "restructuring_secType": data.get("secType"),
#         "restructuring_allotmentDate": data.get("allotmentDate"),
#         "restructuring_redemptionDate": data.get("redemptionDate"),
#         "restructuring_category": data.get("category"),
#         "restructuring_couponRate": data.get("couponRate"),
#         "restructuring_couponBasis": data.get("couponBasis"),
#         "restructuring_interestPaymentFrequency": data.get("interestPaymentFrequency"),
#         "restructuring_type": "new"
#     }
    
#     row2 = {
#         "restructuring_corporateActionEvent": data.get("corporateActionEvent"),
#         "restructuring_isin": data.get("parentIsin"),
#         "restructuring_secType": data.get("parentSecType"),
#         "restructuring_allotmentDate": data.get("parentAllotmentDate"),
#         "restructuring_redemptionDate": data.get("parentRedemptionDate"),
#         "restructuring_category": data.get("parentCategory"),
#         "restructuring_couponRate": data.get("parentCouponRate"),
#         "restructuring_couponBasis": data.get("parentCouponBasis"),
#         "restructuring_interestPaymentFrequency": data.get("parentInterestPaymentFrequency"),
#         "restructuring_type": "old"
#     }

#     return pd.DataFrame([row1, row2])

# # Function to process key contacts data
# def process_key_contacts(data):
#     rows = []

#     issuer_data = {
#         "key_contacts_arranger": None,
#         "key_contacts_Name": None,
#         "key_contacts_contact_person": data.get("issuerCompOffName"),
#         "key_contacts_office_address": data.get("issuerRegAddr"),
#         "key_contacts_contact_details": None,
#         "key_contacts_email": data.get("issuerCompOffEmail"),
#         "key_contacts_website": None,
#         "key_contacts_type": "issuer"
#     }
#     rows.append(issuer_data)

#     registrar_data = {
#         "key_contacts_arranger": None,
#         "key_contacts_Name": data.get("registrar"),
#         "key_contacts_contact_person": data.get("regContactPerson"),
#         "key_contacts_office_address": data.get("regOffAddr"),
#         "key_contacts_contact_details": data.get("regContact"),
#         "key_contacts_email": data.get("regCompOffEmail"),
#         "key_contacts_website": data.get("regWebAddr"),
#         "key_contacts_type": "registrar"
#     }
#     rows.append(registrar_data)

#     debenture_trustee_data = {
#         "key_contacts_arranger": None,
#         "key_contacts_Name": data.get("debtTrusteeName"),
#         "key_contacts_contact_person": None,
#         "key_contacts_office_address": data.get("debtTrusteeAddr"),
#         "key_contacts_contact_details": data.get("debtTrusteeContact"),
#         "key_contacts_email": data.get("debtTrusteeCompOffEmail"),
#         "key_contacts_website": data.get("debtTrusteeWebAddr"),
#         "key_contacts_type": "debenture_trustee"
#     }
#     rows.append(debenture_trustee_data)

#     lead_data = {
#         "key_contacts_arranger": None,
#         "key_contacts_Name": data.get("leadName"),
#         "key_contacts_contact_person": None,
#         "key_contacts_office_address": data.get("leadAddr"),
#         "key_contacts_contact_details": data.get("leadContact"),
#         "key_contacts_email": data.get("leadCompOffEmail"),
#         "key_contacts_website": data.get("leadWebAddr"),
#         "key_contacts_type": "lead"
#     }
#     rows.append(lead_data)

#     if data.get("arrangers") is not None:
#         for arranger in data.get("arrangers", []):
#             arranger_data = {
#                 "key_contacts_arranger": arranger.get("arranger"),
#                 "key_contacts_Name":  None,
#                 "key_contacts_contact_person": arranger.get("contactPerson"),
#                 "key_contacts_office_address": arranger.get("regOffAddr"),
#                 "key_contacts_contact_details": arranger.get("contact"),
#                 "key_contacts_email": arranger.get("email"),
#                 "key_contacts_website": arranger.get("website"),
#                 "key_contacts_type": "arranger"
#             }
#             rows.append(arranger_data)

#     return pd.DataFrame(rows)

# # List of ISIN numbers to process
# isin_numbers = ['INE001W07011','INE001W08126','INE008A08R30']  # Add more ISIN numbers as needed

# # URL and headers for the requests
# base_url_ratings = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/credit-ratings?isin={}"
# base_url_instruments = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/instruments?isin={}"
# base_url_restructuring = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/restructuring?isin={}"
# base_url_key_contacts = "https://www.indiabondinfo.nsdl.com/bds-service/v1/public/bdsinfo/keycontacts?isin={}"
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     'Accept': 'application/json',
#     'Referer': 'https://www.indiabondinfo.nsdl.com/',
#     'Origin': 'https://www.indiabondinfo.nsdl.com'
# }

# all_combined_data = []

# for isin in isin_numbers:
#     # Fetch data for ratings and instruments
#     url_ratings = base_url_ratings.format(isin)
#     url_instruments = base_url_instruments.format(isin)
#     url_restructuring = base_url_restructuring.format(isin)
#     url_key_contacts = base_url_key_contacts.format(isin)
    
#     data_ratings = fetch_data(url_ratings, headers)
#     data_instruments = fetch_data(url_instruments, headers)
#     data_restructuring = fetch_data(url_restructuring, headers)
#     data_key_contacts = fetch_data(url_key_contacts, headers)
    
#     if data_ratings:
#         df_ratings = process_ratings(data_ratings, isin).reset_index(drop=True)  # Reset index here
#     else:
#         df_ratings = pd.DataFrame(columns=[f'credit_rating_{col}' for col in ['isin', 'type']])  # Empty DataFrame with expected columns

#     if data_instruments:
#         df_instruments = process_instruments(data_instruments, isin).reset_index(drop=True)  # Reset index here
#     else:
#         df_instruments = pd.DataFrame(columns=['isin', 'instrument_type'])  # Empty DataFrame with expected columns
    
#     if data_restructuring:
#         df_restructuring = process_restructuring(data_restructuring).reset_index(drop=True)  # Reset index here
#     else:
#         df_restructuring = pd.DataFrame(columns=['restructuring_corporateActionEvent', 'restructuring_isin', 'restructuring_secType', 'restructuring_allotmentDate', 'restructuring_redemptionDate', 'restructuring_category', 'restructuring_couponRate', 'restructuring_couponBasis', 'restructuring_interestPaymentFrequency', 'restructuring_type'])  # Empty DataFrame with expected columns

#     if data_key_contacts:
#         df_key_contacts = process_key_contacts(data_key_contacts).reset_index(drop=True)  # Reset index here
#     else:
#         df_key_contacts = pd.DataFrame(columns=['key_contacts_arranger', 'key_contacts_Name', 'key_contacts_contact_person', 'key_contacts_office_address', 'key_contacts_contact_details', 'key_contacts_email', 'key_contacts_website', 'key_contacts_type'])  # Empty DataFrame with expected columns

#     if not df_ratings.empty and not df_instruments.empty:
#         df_instruments_repeated = pd.concat([df_instruments] * len(df_ratings), ignore_index=True).reset_index(drop=True)  # Reset index here
#         combined_data = pd.concat([df_instruments_repeated, df_ratings], axis=1, ignore_index=True)
#         combined_data.columns = list(df_instruments.columns) + list(df_ratings.columns)  # Resetting column names after concatenation
#     else:
#         combined_data = pd.concat([df_instruments, df_ratings], ignore_index=True)

#     # Combine restructuring and key contacts data
#     combined_data = pd.concat([combined_data, df_restructuring, df_key_contacts], axis=1)
    
#     all_combined_data.append(combined_data)

# # Combine all data into a single DataFrame
# final_combined_df = pd.concat(all_combined_data, ignore_index=True)

# # Save the combined DataFrame to an Excel file
# final_combined_df.to_excel('output_response.xlsx', index=False)

# print("Excel file created successfully.")
