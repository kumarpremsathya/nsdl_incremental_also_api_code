import ast
from django.shortcuts import render
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import  api_view
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_422_UNPROCESSABLE_ENTITY
    
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import *
from datetime import datetime
from isinBondsDebenturesApp.isinkeys_config import *
from rest_framework import serializers

def validate(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except:
        return False

@api_view(['get'])    
def getCustom404View(request,  **kwargs):
        return Response({"result": "Invalid URL"}, status=HTTP_404_NOT_FOUND)
    
@api_view(['get'])
def getIsinDetails(request,isin_number):
    print("isin_number======",isin_number)
    if isin_number == "":
        return Response({"error": "ISIN number is required as a query parameter."}, status=HTTP_400_BAD_REQUEST)
    try: 
        if  isin_number == "" or isin_number == " ":
            return Response({"Error": "Content mismatch"}, status= HTTP_422_UNPROCESSABLE_ENTITY)
        if len(isin_number) != 12:
            return Response({"Error": "Invalid ISIN"}, status= HTTP_400_BAD_REQUEST)
    except serializers.ValidationError as e:
        return Response({"Error": str(e), "status": e.status_code})

    try:
        isin_details = nsdl_instrument_details.objects.filter(isin=isin_number).values(
            'sr_no',
            'isin',
            'issuer_details',
            'type',
            'instrument_details',
            'coupon_details',
            'redemption_details',
            'credit_ratings',
            'listing_details',
            'restructuring',
            'default_details',
            'keycontacts',
            'keydocuments',
            'updated_date',
            'date_scraped')
        if isin_details.exists():
            # print(isin_details)
            isin_details_list = list(isin_details)
            # print(isin_details_list[0])
            result = {"result":isin_details_list[0]}
            
            print("issuer details ======",isin_details_list[0]["issuer_details"])
            issuer_details_dict = ast.literal_eval(isin_details[0]['issuer_details'])
            for key, value in issuer_details_dict.items():
                if key == 'secTypeDesc':
                    isintype = value
            print("isin type======",isintype)        
            issuer_details = isin_details_list[0]["issuer_details"]
            instrument_details = isin_details_list[0]["instrument_details"]
            couponDetails = isin_details_list[0]["coupon_details"]
            redemptionDetails = isin_details_list[0]["redemption_details"]
            creditRtingDetails = isin_details_list[0]["credit_ratings"]
            listingDetails = isin_details_list[0]["listing_details"]
            restructuring = isin_details_list[0]["restructuring"]
            defaultDetails = isin_details_list[0]["default_details"]
            keycontacts = isin_details_list[0]["keycontacts"]
            keydocuments = isin_details_list[0]["keydocuments"]
            
            if issuer_details != None:
                issuer_details_str = isin_details[0]['issuer_details']
                issuer_details_dict = ast.literal_eval(issuer_details_str)
                mapped_issuer_details = {
                    key: issuer_details_dict.get(value, None)
                    for key, value in zip(issuer_details_keys_list, issuer_details_values_to_find)
                }
            else:
                mapped_issuer_details = {
                    "IssuerDetailsStatus" : "No Record Found"
                }    
            if instrument_details != None:
                instrument_details_str = isin_details[0]['instrument_details']
                instrument_details_dict = ast.literal_eval(instrument_details_str)["instrumentsVo"]["instruments"]
                credit_enhancement_dict = ast.literal_eval(instrument_details_str)["instrumentsVo"]["creditEnhancement"]
                furtherIssue_dict = ast.literal_eval(instrument_details_str)["instrumentsVo"]["furtherIssue"]["furtherIssueVo"]
                convertability_dict = ast.literal_eval(instrument_details_str)["instrumentsVo"]["convertability"]
                assetCover_dict = ast.literal_eval(instrument_details_str)["instrumentsVo"]["assetCover"]
                tradePrice_dict = ast.literal_eval(instrument_details_str)["instrumentsVo"]["tradePrice"]["tradeList"]
                # print("instrument details ======",instrument_details_dict)
                # print("credit_enhancement_dict ======",credit_enhancement_dict)
                print("tradePrice_dict ======",tradePrice_dict)
                mapped_instrument_details = {
                    key: instrument_details_dict.get(value, None)
                    for key, value in zip(instrument_details_keys_list, instrument_details_values_to_find)
                } 
                # print("mapped_instrument_details",mapped_instrument_details)  
                mapped_credit_enhancement_details = {
                    key: credit_enhancement_dict.get(value, None)
                    for key, value in zip(credit_enhancement_keys_list, credit_enhancement_values_to_find)
                }  
                # print("mapped_credit_enhancement_details",mapped_credit_enhancement_details)
                
                mapped_furtherIssue_details_list = []
                for issue_dict in furtherIssue_dict:
                    mapped_furtherIssue_details = {
                        key: issue_dict.get(value, None)
                        for key, value in zip(further_issue_keys_list, further_issue_values_to_find)
                    }
                    mapped_furtherIssue_details_list.append(mapped_furtherIssue_details)
                print("mapped_furtherIssue_details_list=====",mapped_furtherIssue_details_list)
                for  index, details in enumerate(mapped_furtherIssue_details_list):
                    print("further issue s.no =====",details["serialNo"])
                    details["serialNo"] = index + 1
                mapped_convertability_details = {
                    key: convertability_dict.get(value, None)
                    for key, value in zip(convertibility_keys_list, convertibility_values_to_find)
                }  
                # print("mapped_convertability_dict_details",mapped_convertability_details)
                
               
                details_of_asset_cover = assetCover_dict.get('assetList', [])
                # print("details_of_asset_cover",details_of_asset_cover)

                mapped_assetCover_details_with_sr_no = []
                for index, detail in enumerate(details_of_asset_cover):
                    new_detail = {'sr.no': index + 1}
                    new_detail.update(detail)
                    mapped_assetCover_details_with_sr_no.append(new_detail)

                mapped_assetCover_details = {
                    key: assetCover_dict.get(value, None) if value != "assetList" else mapped_assetCover_details_with_sr_no
                    for key, value in zip(asset_cover_keys_list, asset_cover_values_to_find)
                }
                
                mapped_tradePrice_details_list = []
                for issue_dict in tradePrice_dict:
                    mapped_tradePrice_details = {
                        key: issue_dict.get(value, None)
                        for key, value in zip(trade_price_keys_list, trade_price_values_to_find)
                    }
                    mapped_tradePrice_details_list.append(mapped_tradePrice_details)
                # print("mapped_tradePrice_details_list",mapped_tradePrice_details_list)
                
                final_mapped_instrument_details = {
                    "instrumentDetails": mapped_instrument_details,
                    "creditEnhancement":mapped_credit_enhancement_details,
                    "furtherIssue":mapped_furtherIssue_details_list,
                    "convertability": mapped_convertability_details,
                    "assetCover":mapped_assetCover_details,
                    "tradePrice":mapped_tradePrice_details_list,
                }
            else:
                final_mapped_instrument_details = {
                    "instrumentDetailsStatus" : "No Record Found"
                }    
            if couponDetails != None:
                coupon_details_str = isin_details[0]['coupon_details']
                coupon_details_dict = ast.literal_eval(coupon_details_str)["coupensVo"]["couponDetails"]
                coupon_details_additional_dict = ast.literal_eval(coupon_details_str)["coupensVo"]["couponDetails"]["coupenBasicVo"]
                cashFlowScheduleDetails_dict = ast.literal_eval(coupon_details_str)["coupensVo"]["cashFlowScheduleDetails"]
                step_status_dict = ast.literal_eval(coupon_details_str)["coupensVo"]["stepStatus"]
                
                print("cashFlowScheduleDetails_dict ======",cashFlowScheduleDetails_dict)
                mapped_coupon_details = {
                    key: coupon_details_dict.get(value, None)
                    for key, value in zip(new_coupon_details_keys_list, new_coupon_details_values_to_find)
                }
                
                
                mapped_coupon_details["Details Of Variable Coupon Rate"] = '-'
                print("mapped_coupon_details=====",mapped_coupon_details)
                
                
                # coupon details respone ====== {'referenceIndexLinked': None, 'benchmarkIndex': None, 'plusMinusSpread': None, 'couponRate': None, 'baseRate': None, 'capRate': None, 'floorRate': None}
                for details in coupon_details_additional_dict:
                    print("coupon additional details ======", details)
                    mapped_coupon_additional_details = {
                    key: details.get(value, None)
                    for key, value in zip(new_coupon_additional_details_keys_list, new_coupon_additional_details_keys_list)
                }
                print("mapped_coupon_additional_details=====",mapped_coupon_additional_details)
                for key in mapped_coupon_additional_details:
                    print("dtails key ====",key)
                    if key in mapped_coupon_details:
                        print("mapped_coupon_details key======",key)
                        mapped_coupon_details[key] = mapped_coupon_additional_details[key]

                print("mapped_coupon_details after update ======", mapped_coupon_details)    
                # Filter out "isin" and "isinDesc" "source"from "basicDetails"
                filtered_basic_details = [
                    {key: value for key, value in detail.items() if key not in ["isin", "isinDesc","source","actualRecordDate"]}
                    for detail in cashFlowScheduleDetails_dict["cashFlowSchedule"]
                ]
                
                print("filtered_basic_details======",filtered_basic_details)
                
                revised_filtered_basic_details = []
                for index, basic_details in enumerate(filtered_basic_details):
                    mapped_basic_details_revised_key = {
                        key: basic_details.get(value, None)
                        for key, value in zip(basic_details_keys_list, basic_details_values_to_find)
                    }
                    revised_filtered_basic_details.append(mapped_basic_details_revised_key)
                
                
                print("revised_filtered_basic_details======",revised_filtered_basic_details)
                print("step_status_dict======",step_status_dict)
                mapped_cash_flow_details = {
                    key: cashFlowScheduleDetails_dict.get(value, None) if value != "cashFlowSchedule" else revised_filtered_basic_details
                    for key, value in zip(cash_flow_schedule_keys_list, cash_flow_schedule_values_to_find)
                }

                print("mapped_cash_flow_details",mapped_cash_flow_details)
                
                filtered_stepdown_details = []
                filtered_stepup_details = []
                if step_status_dict["stepUp"] != None:
                    filtered_stepup_details = [
                        {key: value for key, value in detail.items() if key not in ["reasonStepUp"]}
                        for detail in step_status_dict["stepUp"]
                    ]
                    for detail in filtered_stepup_details:
                        if "resetTypeStepUp" in detail:
                            detail["resetValueStepUp"] = detail.pop("resetTypeStepUp")
                
                if  step_status_dict["stepDown"] != None:
                    filtered_stepdown_details = [
                        {key: value for key, value in detail.items() if key not in ["reasonStepDown"]}
                        for detail in step_status_dict["stepDown"]
                    ]
                    for detail in filtered_stepdown_details:
                        if "resetTypeStepDown" in detail:
                            detail["resetValueStepDown"] = detail.pop("resetTypeStepDown")
                    print("filtered_basic_details======",filtered_basic_details)
                mapped_step_status_details = {
                    key: (
                        step_status_dict.get(value, None) 
                        if value not in ["stepUp", "stepDown"] 
                        else (filtered_stepup_details if value == "stepUp" else filtered_stepdown_details)
                    )
                    for key, value in zip(step_up_step_down_details_keys_list, step_up_step_down_details_values_to_find)
                }
                print("mapped_step_status_details",mapped_step_status_details) 
                
                final_mapped_coupon_details = {
                    "couponDetails":mapped_coupon_details,
                    "cashFlowScheduleDetails":mapped_cash_flow_details,
                    "stepUpStepDownDetails": mapped_step_status_details,
                }
            else:
                final_mapped_coupon_details = {
                    "coupondetailStatus": "No Record Found",
                }
                
            print("redemptionDetails======",redemptionDetails)
            if redemptionDetails != None:
                redemption_details_str = isin_details[0]['redemption_details']
                redemption_details_dict = ast.literal_eval(redemption_details_str)
                print("redemption_details_dict======",redemption_details_dict)
                details_of_putOption = redemption_details_dict.get('putOption', [])
                
                mapped_redemption_details = {
                    key: redemption_details_dict.get(value, None)
                    for key, value in zip(redemption_details_keys_list, redemption_details_values_to_find)
                } 
                mapped_put_call_option_details = {
                    key: redemption_details_dict.get(value, "No")
                    for key, value in zip(put_call_option_details_keys_list, put_call_option_details_values_to_find)
                } 
                flag = True
                print("mapped_put_call_option_details======",mapped_put_call_option_details)  
                if mapped_put_call_option_details["putOptionDetails"]['specifiedDates'] == "N.A":
                    flag = False
                if mapped_put_call_option_details["putOptionDetails"]['specifiedDates'] == "N.A.":
                    flag = False    
                if mapped_put_call_option_details["putOptionDetails"]['specifiedDates'] ==  None:
                    flag = False    
                # for key,value in mapped_put_call_option_details["putOptionDetails"].items():
                #     if ((key == "specifiedDates" and value != "N.A.") or (key == 'specifiedDates' and value != None)):
                #         print("welcome to key====",flag)
                #         flag = True
                print("mapped_put_======",mapped_put_call_option_details["putOptionDetails"]['specifiedDates'])          
                print("flag======",flag,type(flag))
                if  flag == True:  
                    print("welcome to flag")     
                    mapped_put_call_option_details = {
                        key: redemption_details_dict.get(value, "Yes")
                        for key, value in zip(put_call_option_details_keys_list, put_call_option_details_values_to_find)
                    }     
                final_mapped_redemption_details = {
                    "redemptionDetails": mapped_redemption_details,
                    "putCallOptionDetails": mapped_put_call_option_details,
                }
            else:
                final_mapped_redemption_details = {
                    "redemptionDetailStatus": "No Record Found"
                }
                    
            if creditRtingDetails != None:
                credit_rating_details_str = isin_details[0]['credit_ratings']
                credit_rating_details_dict = ast.literal_eval(credit_rating_details_str)
                print("credit_rating_details_dict======",credit_rating_details_dict)
                filtered_credit_current_rating_details_s_no = []
                filtered_credit_early_rating_details_s_no = []
                if credit_rating_details_dict["currentRatings"] != [] :
                    
                    details_credit_current_rating = credit_rating_details_dict.get('currentRatings',[])
                    for index, detail in enumerate(details_credit_current_rating):
                        new_detail = {'sr.no': index + 1}
                        new_detail.update(({key: value for key, value in detail.items() if key not in ["isin", "isinDesc", "issuerId","issuerName","updateDate","pressReleaseLink"]}))
                        filtered_credit_current_rating_details_s_no.append(new_detail)
                      
                if  credit_rating_details_dict["earlierRatings"] != []: 
                    
                    details_credit_early_rating = credit_rating_details_dict.get('earlierRatings',[])
                    print("details_credit_early_rating===",details_credit_early_rating)
                    for index, detail in enumerate(details_credit_early_rating):
                        new_detail = {'sr.no': index + 1}
                        new_detail.update(({key: value for key, value in detail.items() if key not in ["isin", "isinDesc", "issuerId","issuerName","updateDate","pressReleaseLink"]}))
                        filtered_credit_early_rating_details_s_no.append(new_detail)  
                    
                
                    
                mapped_credit_rating_details = {
                    key: (
                        credit_rating_details_dict.get(value, None) 
                        if value not in ["currentRatings", "earlierRatings"] 
                        else (filtered_credit_current_rating_details_s_no if value == "currentRatings" else filtered_credit_early_rating_details_s_no)
                        )
                    for key, value in zip(credit_rating_details_keys_list, credit_rating_details_values_to_find)
                }
                print("mapped_credit_rating_details====",mapped_credit_rating_details)
                if mapped_credit_rating_details["currentRating"] != []:
                    for details in mapped_credit_rating_details["currentRating"]:
                        print(details)
                        if details['datasource'] == 'CRA':
                            details['datasource'] = 'Rating Agency'
                    for index, currentdetails in enumerate(mapped_credit_rating_details["currentRating"]):
                        mapped_current_rating_details_revised_key = {
                            key: currentdetails.get(value, None)
                            for key, value in zip(earlier_rating_details_keys_list, earlier_rating_details_values_to_find)
                        }
                        # Update the list item with the revised dictionary
                        mapped_credit_rating_details["currentRating"][index] = mapped_current_rating_details_revised_key
                
                if  mapped_credit_rating_details["earlierRating"] != []:   
                    for details in mapped_credit_rating_details["earlierRating"]:
                        print(details)
                        if details['datasource'] == 'CRA':
                            details['datasource'] = 'Rating Agency'
                    print("mapped_credit_rating_details EARLIER RATING=====",mapped_credit_rating_details["earlierRating"])        
                    for index, earlierdetails in enumerate(mapped_credit_rating_details["earlierRating"]):
                        mapped_earlier_rating_details_revised_key = {
                            key: earlierdetails.get(value, None)
                            for key, value in zip(earlier_rating_details_keys_list, earlier_rating_details_values_to_find)
                        }
                        # Update the list item with the revised dictionary
                        mapped_credit_rating_details["earlierRating"][index] = mapped_earlier_rating_details_revised_key
        
                                  
            else:
                 mapped_credit_rating_details = {
                    "indicateWhetherTheInstrumentIsRated": "Null",
                    "creditRatingStatus" : "No credit Rating information available"
                }
                         
            print("isin_details[0]['listing_details']====",isin_details[0]['listing_details'],type(isin_details[0]['listing_details']))
            if listingDetails != None:
                listing_details_str = isin_details[0]['listing_details']
                listing_details_dict = ast.literal_eval(listing_details_str)
                print("listing_details_dict======",listing_details_dict)
                
                mapped_listing_details = {
                    key: listing_details_dict.get(value, None)
                    for key, value in zip(listing_details_keys_list, listing_details_values_to_find)
                } 
                
                # adding serial no key
                filtered_current_listed_s_no = []
                filtered_earlier_listed_s_no = []
                if mapped_listing_details["currentListing"] != [] :
                    details_credit_current_rating = mapped_listing_details.get('currentListing',[])
                    print("details_credit_current_rating======",details_credit_current_rating)
                    for index, detail in enumerate(details_credit_current_rating):
                        print("listing detail ======",detail)
                        new_detail = {'sr.no': index + 1}
                        new_detail.update(detail)
                        filtered_current_listed_s_no.append(new_detail)
                    mapped_listing_details["currentListing"] = filtered_current_listed_s_no
                    
                    # udating the key in the list 
                    for index, current_listing_details in enumerate(mapped_listing_details["currentListing"]):
                        mapped_current_listing_details_revised_key = {
                            key: current_listing_details.get(value, None)
                            for key, value in zip(current_listed_details_keys_list, current_listed_values_to_find)
                        }
                        # Update the list item with the revised dictionary
                        mapped_listing_details["currentListing"][index] = mapped_current_listing_details_revised_key
                
                if mapped_listing_details["earlierListing"] != [] :
                    details_credit_earlier_rating = mapped_listing_details.get('earlierListing',[])
                    print("details_credit_earlier_rating======",details_credit_earlier_rating)
                    for index, detail in enumerate(details_credit_earlier_rating):
                        print("listing detail ======",detail)
                        new_detail = {'sr.no': index + 1}
                        new_detail.update(detail)
                        filtered_earlier_listed_s_no.append(new_detail)
                    mapped_listing_details["earlierListing"] = filtered_earlier_listed_s_no      
                # udating the key in the list 
                    for index, earlier_listing_details in enumerate(mapped_listing_details["earlierListing"]):
                        mapped_earlier_listing_details_revised_key = {
                            key: earlier_listing_details.get(value, None)
                            for key, value in zip(current_listed_details_keys_list, current_listed_values_to_find)
                        }
                        # Update the list item with the revised dictionary
                        mapped_listing_details["earlierListing"][index] = mapped_earlier_listing_details_revised_key
            else:
                 mapped_listing_details = {
                    "listingStatus" : "No listing information available"
                }

            if restructuring != None:
                restructuring_str = isin_details[0]['restructuring']
                restructuring_dict = ast.literal_eval(restructuring_str)
                print("restructuring_dict======",restructuring_dict)
                mapped_restructuring = {
                    key: restructuring_dict.get(value, None)
                    for key, value in zip(restructuring_details_keys_list, restructuring_details_values_to_find)
                } 
            else:
                 mapped_restructuring = {
                    "restructuringStatus" : "No Record Found"
                }    
            
            if defaultDetails != None:
                defaultDetails_str = isin_details[0]['default_details']
                defaultDetails_dict = ast.literal_eval(defaultDetails_str)
                print("defaultDetails_dict======",defaultDetails_dict)
                    
                for details in defaultDetails_dict:
                    print(details)
                    if details["dataSource"] == "TR":
                        details["dataSource"] = "Debenture Trustee"
                  
                # udating the key in the list 
                revised_default_details_key = []
                for index, default_details in enumerate(defaultDetails_dict):
                    mapped_default_details_revised_key = {
                        key: default_details.get(value, None)
                        for key, value in zip(default_details_keys_list, default_details_values_to_find)
                    }
                    revised_default_details_key.append(mapped_default_details_revised_key)
                    
                # Sort the revised_default_details_key by 'sr.no'
                sorted_revised_default_details_key = sorted(revised_default_details_key, key=lambda x: x["sr.no"])   
                for index, item in enumerate(sorted_revised_default_details_key):
                    item['sr.no'] = index + 1    
                defaultDetails_dict = sorted_revised_default_details_key    
            else:
                 defaultDetails_dict = {
                    "defaultDetailStatus" : "No Record Found"
                }
            if keycontacts != None:
                keycontacts_str = isin_details[0]['keycontacts']
                keycontacts_dict = ast.literal_eval(keycontacts_str)
                print("keycontacts_dict======",keycontacts_dict) 
                mapped_issuer_keys_list = {
                    key: keycontacts_dict.get(value, None)
                    for key, value in zip(issuer_keys_list, issuer_values_to_find)
                } 
                mapped_registrar_keys_list = {
                    key: keycontacts_dict.get(value, None)
                    for key, value in zip(registrar_keys_list, registrar_values_to_find)
                } 
                mapped_debenture_trustee_keys_list = {
                    key: keycontacts_dict.get(value, None)
                    for key, value in zip(debenture_trustee_keys_list, debenture_trustee_values_to_find)
                } 
                mapped_lead_manager_keys_list = {
                    key: keycontacts_dict.get(value, None)
                    for key, value in zip(lead_manager_keys_list, lead_manager_values_to_find)
                } 
                                  
                mapped_arrangers_list = []
                mapped_arrangers_list =  keycontacts_dict["arrangers"] 
                print("mapped_arrangers_list======",mapped_arrangers_list)
                if mapped_arrangers_list != None:
                    for index, detail in enumerate(mapped_arrangers_list):
                        print(detail,detail["isin"])
                        del detail["isin"]
                        if 'regOffAddr' in detail:
                            detail['address'] = detail.pop('regOffAddr')
                        if 'email' in detail:
                            detail['emailID'] = detail.pop('email')
                        if 'website' in detail:
                            detail['websiteAddress'] = detail.pop('website')  
                mapped_keycontacts = {
                    "issuer": mapped_issuer_keys_list,
                    "registrar": mapped_registrar_keys_list,
                    "debuntureTrustee": mapped_debenture_trustee_keys_list,
                    "leadManager": mapped_lead_manager_keys_list,
                    "arrangerToTheIssue":mapped_arrangers_list
                }
            else:
                 mapped_keycontacts = {
                    "keyContactStatus" : "No Record Found"
                }    
            
            if keydocuments != None:
                keydocuments_str = isin_details[0]['keydocuments']
                keydocuments_dict = ast.literal_eval(keydocuments_str)
                print("keydocuments_dict======",keydocuments_dict) 
                filtered_keydocument_details = [
                        {key: value for key, value in detail.items() if key not in ["source", "fileId"]}
                        for detail in keydocuments_dict
                    ]
                print("filtered_keydocument_details======",filtered_keydocument_details) 
            else:
                filtered_keydocument_details = {
                    "keydocumentStatus": "No Record Found"
                }   
            formatted_result = {
                "isin":isin_details_list[0]["isin"],
                "type":isintype,
                "issuerDetails":mapped_issuer_details,
                "instrumentDetails":final_mapped_instrument_details,
                # "instrument_details": mapped_instrument_details,
                # "creditEnhancement":mapped_credit_enhancement_details,
                # "furtherIssue":mapped_furtherIssue_details_list,
                # "convertability": mapped_convertability_details,
                # "assetCover":mapped_assetCover_details,
                # "tradePrice":mapped_tradePrice_details_list,
                
                "couponDetails": final_mapped_coupon_details,
                # "coupon_details":mapped_coupon_details,
                # "cashFlowScheduleDetails":mapped_cash_flow_details,
                # "stepUpStepDownDetails": mapped_step_status_details,
                
                "redemptionDetails": final_mapped_redemption_details, 
                # "redemption_details": mapped_redemption_details,
                # "put_call_option_details": mapped_put_call_option_details,
                
                "creditRatings": mapped_credit_rating_details,
                "listingDetails": mapped_listing_details,
                "restructuring": mapped_restructuring,
                "defaultDetails": defaultDetails_dict,
                "keycontacts": mapped_keycontacts,
                "keydocuments": filtered_keydocument_details
                }
                
            
            # return Response({"issuer_details": mapped_issuer_details}, status=HTTP_200_OK)
            # return Response({"result": result}, status=HTTP_200_OK)
            # return Response( result, status=HTTP_200_OK)
            return Response(formatted_result, status=HTTP_200_OK)
        else:
            return Response({"error": "No data found for the given isin number."}, status=HTTP_400_BAD_REQUEST)
    except Exception as err:
        return Response({"error": f"Exception occurred: {err}"}, status=HTTP_400_BAD_REQUEST)
