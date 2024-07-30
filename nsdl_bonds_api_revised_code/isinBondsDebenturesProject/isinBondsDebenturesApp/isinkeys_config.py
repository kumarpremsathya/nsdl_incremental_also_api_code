init_keys = [
        "Issuer Details",
        "Instrument details",
        "coupon details"
        "redemption details",
        "credit rating details",
        "listing details",
        "restructuring details",
        "Default details",
        "key contacts",
        "key documents"
]
init_values = [
    "issuer_details",
    "instrument_details",
    "coupon_details",
    "redemption_details",
    "credit_ratings",
    "listing_details",
    "restructuring",
    "default_details",
    "keycontacts",
    "keydocuments"
]
issuer_details_keys_list = [
    "issuerName",
    "issuerFormerName",
    "typeofIssuerBasedonOwnership",
    "macro-EconomicSector",
    "sector",
    "industry",
    "basicIndustry",
    "corporateIdentityNumber(CIN)",
    "legalEntityIdentifier(LEI)",
    "detailsOfGroupCompanies"
]
issuer_details_values_to_find = [
    "issuerName",
    "formerNameOne",
    # "formerNameTwo",
    # "formerNameThree",
    "issuerTypeOwner",
    "macro",
    "sector",
    "industry",
    "basicIndusrty",
    "cin",
    "lei",
    "issuerDetails"
]

instrument_details_columns = [
    "Instrument details",
    "credit/enhancement/guarentee",
    "further issue",
    "convertibility",
    "asset cover",
    "trade price"
]

instrument_details_keys_list = [
    "instrumentDescription(Long)",
    "faceValue(in)",
    "issuePrice(in)",
    "totalIssueSize(in Cr.)",
    "amountRaised(in Rs.)",
    "greenShoeOption",
    "totalAllotmentQuantity",
    "allotmentDate",
    "whetherDebenturesOrBondsArePerpetualInNature",
    "redemptionDateOrLastConversionDate",
    "tenureOfTheInstrumentAtTheTimeOfIssuance(years)",
    "tenureOfTheInstrumentAtTheTimeOfIssuance(months)",
    "tenureOfTheInstrumentAtTheTimeOfIssuance(days)",
    "categoryOfInstrument",
    "modeOfIssue",
    "series",
    "tranchNumber",
    "principalProtected",
    "whetherSecuredorUnsecured",
    "seniorityInRepayment",
    "detailsOfAssetCover",
    "whetherTaxFree",
    "ifTaxfree,QuoteTheSectionOfTheIncomeTaxAct,1961UnderWhichItIsTaxFree",
    "whetherBondsOrDebenturesFallUnderInfrastructureCategoryAsPerGovernmentNotification",
    "objectOfTheIssue",
    "scheduledOpeningDate",
    "scheduledClosingDate",
    "actualClosingDate",
]
instrument_details_values_to_find = [
    "instrumentDesc",
    "faceValue",
    "issuePrice",
    "totalIssueSize",
    "amountRaised",
    "greenShoeOption",
    "totalAllotmentQuantity",
    "allotmentDate",
    "perpetualInNature",
    "redemptionDate",
    # "tenureYears" "tenureMonths" "tenureDays",
    "tenureYears",
    "tenureMonths",
    "tenureDays",
    "category",
    "modeOfIssue",
    "series",
    "trancheNumber",
    "principalProtected",
    "secured",
    # "natureOfInstrument": "-",
    "seniorityRepayment",
    "securedDetails",
    "taxFree",
    "incomeTaxSection",
    "infrastructureCategory",
    "objectOfIssue",
    "scheduledOpeningDate",
    "scheduledClosingDate",
    "actualClosingDate",
    # "intrumentTypeOther": "-"
]

credit_enhancement_keys_list = [
    "creditEnhancement",
    "creditEnhancementFacilityAvailed",
    "guaranteeDetails",
    "whetherGuaranteedOrPartiallyGuaranteed",
]

credit_enhancement_values_to_find = [
    "creditEnhanceDetails",
    "creditEnhancementAvailed",
    "guaranteeDetails",
    "guarantee"
]

further_issue_keys_list = [
    "serialNo", 
    "dateofAllotment",
    "allotmentQuantity",
    "cumulativeQuantity",
    "issuePrice(in Rs.)",
    "issueSize(in Rs.)",
    "cum.IssueSize(in Rs.)",
    "totalAmtRaised(in Rs.)",
    "cum.AmtRaised(in Rs.)"
]

further_issue_values_to_find = [
    "serialNo",
    "allotmentDate",
    "allotmentQuantity",
    "cumulativeQuantity",
    "issuePriceRs",
    "issueSizeRsCrs",
    "cummIssueSizeRsCrs",
    "totalAmountRaisedRsCrs",
    "cummAmountRaisedRsCrs",
]

convertibility_keys_list = [
    "typeOfConvertibility-A ",
    "typeOfConvertibility-B ",
    "convertibilityDetails"
]

convertibility_values_to_find = [
    "typeConvertibleA",
    "typeConvertibleB",
    "convertabilityList"
]
asset_cover_keys_list = [
    "whetherSecuredOrUnsecured",
    "detailsOfAssetCover",
    "assetCoverage",
    "assetPercentage"
    
]
asset_cover_values_to_find = [
    "securedFlag",
    "assetList",
    "assetCvge",
    "assetCvrPercent"
    
]

trade_price_keys_list = [
"exchange",
"tradeDate",	
"lastTradedPrice( )",
"weightedAveragePrice",
"weightedAverageYield",
"turnover(in Lacs)"
]
# list tradeList
trade_price_values_to_find = [
    "exchange",
    "tradeDate",
    "lastTradedPrice",
    "avgWeightedPrice",
    "avgWeightedYield",
    "turnoverLacs",
    # "dataChart"
    # "fromDate"
    # "toDate"
]

coupon_details_column =[
    "coupon details",
    "cash flow schedule",
    "step up/step down details"
]

coupon_details_keys_list = [
    "couponBasis",
    "couponRate",
    "frequencyOfInterestPayment",
    "couponType",
    "compoundingFrequencyDetails",
    "couponResetProcess",
    "defaultInterestRate",
    "dayCountConvention",
    "detailsOfVariableCouponRate",
    "additionalDetails"
]
coupon_details_values_to_find= [
    "couponBasis",
    "couponRate",
    "interestPaymentFrequency",
    "couponType",
    "frequencyDescription",
    "couponResetProcess",
    "interestRate",
    "dayCountConvention",
    " ",
    "additionalDetails"
]

new_coupon_details_keys_list = [
    "couponBasis",
    "UnderlyingOrReferenceOrBenchmarkIndex",
    "+/-Spread",
    "couponRate",
    "frequencyofInterestPayment",
    "frequencyDescription",
    "couponType",
    "compoundingFrequencyDetails",
    "baseRate",
    "capRate",
    "floorRate",
    "initialFixingDate",
    "initialFixingLevel",
    "finalFixingDate",
    "finalFixingLevel",
    "observationdate(s)",
    "underlyingPerformanceOrPayOff",
    "participationRate",
    "couponPayoutformula",
    "couponResetProcess",
    "defaultInterestRate",
    "dayCountConvention",
    "detailsOfVariableCouponRate",
    "additionalDetails"
]
new_coupon_details_values_to_find= [
    "couponBasis",
    "benchmarkIndex", #"couponDetails""coupenBasicVo": [
    "plusMinusSpread",  #"couponDetails""coupenBasicVo": [
    "couponRate",
    "interestPaymentFrequency",
    " ",
    "couponType",
    "frequencyDescription",
    "baseRate",  #"couponDetails""coupenBasicVo": [
    "capRate",    # "couponDetails""coupenBasicVo": [
    "floorRate",   # "couponDetails""coupenBasicVo": [
    "initialFixingDate",
    "initialFixingLevel",
    "finalFixingDate",
    "finalFixingLevel",
    "",
    "performance",
    "participationRate",
    "couponPayoutformula",
    "couponResetProcess",
    "interestRate",
    "dayCountConvention",
    " ",
    "additionalDetails"
]
new_coupon_additional_details_keys_list = [
    "underlyingOrReferenceOrBenchmarkIndex",
    "+/-Spread",
    "baseRate",
    "capRate",
    "floorRate",
]

new_coupon_additional_details_values_to_find= [
    "benchmarkIndex", #"couponDetails""coupenBasicVo": [
    "plusMinusSpread",  #"couponDetails""coupenBasicVo": [
    "baseRate",  #"couponDetails""coupenBasicVo": [
    "capRate",    # "couponDetails""coupenBasicVo": [
    "floorRate",   # "couponDetails""coupenBasicVo": [
]



cash_flow_schedule_keys_list = [
"basicDetails",
"interestPaymentDetails",
"redemptionPaymentDetails"
]

cash_flow_schedule_values_to_find = [
"cashFlowSchedule", #list
"interestCashFlowSchedule", #list
"redemptionCashFlowSchedule" #list
]

basic_details_keys_list = [
    "cashFlowsEvent",
    "recordDate",
    "dueDate",
    "amountPayable(per Unit)(Rs in Crs)",
    "dateOfPayment",
    "actualPaymentDate",
    "amountOfInterestPaidOrAmountRedeemed(Rs in Crs)",
    "amountOutstanding(Rs in Crs)",
    "changeInFrequencyOfPayment",
    "detailsOfChangeInFrequency",
    "reasonForNonPaymentOrDelayInPayment",
    # "actualRecordDate",
    # "source": null
]  

basic_details_values_to_find = [
    "cashFlowsEvent",
    "recordDate",
    "dueDate",
    "amountPayable",
    "paymentDate",
    "actualPaymentDate",
    "amountRedeemed",
    "amntOutstanding",
    "chngFreqPayment",
    "detailChngFreqPayment",
    "reasonDelayPayment",
    # "actualRecordDate",
    # "source": null
]                   

step_up_step_down_details_keys_list = [
"stepUpCouponOptionAvailable",
"stepUpDetails",
"stepDownCouponOptionAvailable",
"stepDownDetails"
]

step_up_step_down_details_values_to_find = [
"stepUpAvail",
"stepUp", #list
"stepDownAvail",
"stepDown", #list
]

redemption_details_column = [
    "redemption details",
    "put/call option details"
]

redemption_details_keys_list = [
    "redemptionType",
    "detailsOfPartialRedemption",
    "TotalQuantityOrValueRedeemed",
    "NetQuantity",
    "contingentEarlyRedemptionDetails",
    "maturityType",
    "AdditionalDetailsOfPartialRedemption",
    "redemptionPremiumDetails(if any)",
    "defaultedInRedemption",
    "reasonForRedemption"
]

   
   
redemption_details_values_to_find = [
    "redemptionType",
    "redemption", #list
     "totalQuantity",
    "netQuantity",
    "earlyRedemptionDetails",
    "maturityType",
    " ",
    "redemptionPremiumDetails",
    "defaultedRedemption",
    "reasonForRedemption"
]

detailsOfPartialRedemption_keys_list =[
     "Sr.No",
     "RedemptionMethod",
     "partialRedemptionDates",
     "quantityRedeemed",
     "valueRedeemed",
     "reasonForRedemption"
 ]

put_call_option_details_keys_list = [
"putOptionAvaialbe",
"putOptionDetails",
"callOptionAvailbale",
"callOptionDetails"
]

put_call_option_details_values_to_find = [
"",
"putOption",
"",
"callOption",
]

credit_rating_details_keys_list = [
    "indicateWhetherTheInstrumentIsRated",
    "currentRating",
    "earlierRating",
]

credit_rating_details_values_to_find = [
    "instrumentRateFlag",
    "currentRatings",
    "earlierRatings",
]
current_rating_details_keys_list = [
    "sr.no",
    "creditRatingAgencyName",
    "creditRating",
    "outlook",
    "watch",
    "ratingAction",
    "initialCreditRatingDate",
    "dateOfRatingChange",
    "dataSource",
    "verificationStatus",
    "dateOfVerification",
    
]

current_rating_details_values_to_find = [
    "sr.no",
    "creditRatingAgencyName",
    "currentRating",
    "outlook",
    "iciWatch",
    "ratingAction",
    "creditRatingDate",
    # "reviewDueDate",
    "ratingChangeDate",
    "datasource",
    "verificationStatus",
    "dateOfVerification",
]    

earlier_rating_details_keys_list = [
    "sr.no",
    "creditRatingAgencyName",
    "creditRating",
    "outlook",
    "watch",
    "ratingAction",
    "initialCreditRatingDate",
    "dateOfRatingChange",
    "dataSource",
    "verificationStatus",
    "dateOfVerification",
    
]

earlier_rating_details_values_to_find = [
    "sr.no",
    "creditRatingAgencyName",
    "currentRating",
    "outlook",
    "iciWatch",
    "ratingAction",
    "creditRatingDate",
    # "reviewDueDate",
    "ratingChangeDate",
    "datasource",
    "verificationStatus",
    "dateOfVerification",
]    




listing_details_keys_list = [
    "listingStatus",
    "currentListing",
    "earlierListing",
    # "UNListed"
]

listing_details_values_to_find = [
    "listingStatus",
    "listingDetails",
    "earlierListingDetails",
    # "UNListed"
]

current_listed_details_keys_list = [
    "sr.no",
    "exchangeName",
    "allotmentName",
    "lisingDate",
    "listingQuantity",
    "firstIssueOrFurtherIssue",
    "linkToLisingNotification",
    "linkToTermsheetOrIM",
]

current_listed_values_to_find = [
    "sr.no",
    "exchangeName",
    "allotmentDate",
    "listingDate",
    "listingQuantity",
    "issueType",
    "listingNotification",
    "termSheetLink",
]  


# key using response
# "EARLIER LISTED": [
#             {
#                 "sr.no": 1,
#                 "listingDate": "31-03-2022",
#                 "listingQuantity": "192",
#                 "termSheetLink": "https://www.bseindia.com/markets/debt/memorandum_data.aspx",
#                 "listingNotification": "https://www.bseindia.com/markets/MarketInfo/NoticesCirculars.aspx?id=0&txtscripcd=&pagecont=&subject=",
#                 "issueType": "First Issue",
#                 "exchangeName": "BSE",
#                 "allotmentDate": "29-03-2022"
#             }  

restructuring_details_keys_list =[
    "corporateActionEvent",
    "newIsin",
    "newInstrumentDescription",
    "newallotmentDate",
    "newRedemption Date/Last Conversion Date",
    "newcouponRate",
    "newcouponBasis",
    "newFrequency of Interest Payment",
    "newCategory of Instrument",
    "oldIsin",
    "oldInstrumentDescription",
    "oldAllotmentDate",
    "oldRedemption Date/Last Conversion Date",
    "oldcouponRate",
    "oldcouponBasis",
    "oldFrequency of Interest Payment",
    "oldCategory of Instrument",
   
]
restructuring_details_values_to_find =[
    "corporateActionEvent",
    "isin",
    "secType",
    "allotmentDate",
    "redemptionDate",
    "couponRate",
    "couponBasis",
    "interestPaymentFrequency",
    "category",
    "parentIsin",
    "parentSecType",
    "parentAllotmentDate",
    "parentRedemptionDate",
    "parentCouponRate",
    "parentCouponBasis",
    "parentInterestPaymentFrequency",
    "parentCategory",
]

default_details_keys_list = [
    "sr.no",
    "natureOfTheIssue",
    "issueSize",
    "dueDateOfInterest",
    "dueDateOfRedemption",
    "defaultDetails",
    "actualPaymentDateAndDetails",
    "dataSource",
    "verificationStatus",
    "dateOfVerification",
]

default_details_values_to_find = [
    "srNo",
    "issueNature",
    "issueSize",
    "interestDueDate",
    "redemptionDueDate",
    "defaultDetails",
    "actualPaymentDetails",
    "dataSource",
    "verificationStatus",
    "verificationDate",
]  
issuer_keys_list =[
    "registeredOfficeAddressOfIssuer",
    "nameOfTheComplianceOfficerOrCompanySecretary",
    "emailIDOfTheComplianceOfficerOrCompanySecretary"
]
issuer_values_to_find =[
    "issuerRegAddr",
    "issuerCompOffName",
    "issuerCompOffEmail"
]
registrar_keys_list =[
    "registrar",
    "registrarContactPerson",
    "registrarOfficeAddress",
    "contactDetails",
    "emailID",
    "websiteAddress",
]
registrar_values_to_find =[
    "registrar",
    "regContactPerson",
    "regOffAddr",
    "regContact",
    "regCompOffEmail",
    "regWebAddr",
]
debenture_trustee_keys_list = [
    "nameOfDebentureTrustee",
    "address",
    "contactDetails",
    "emailID",
    "websiteAddress"
    
]
debenture_trustee_values_to_find = [
    "debtTrusteeName",
    "debtTrusteeAddr",
    "debtTrusteeContact",
    "debtTrusteeCompOffEmail",
    "debtTrusteeWebAddr",
    
]
lead_manager_keys_list = [
    "nameOfTheLeadManager",
    "address",
    "contactDetails",
    "emailID",
    "websiteAddress"
]

lead_manager_values_to_find = [
    "leadName",
    "leadAddr",
    "leadContact",
    "leadCompOffEmail",
    "leadWebAddr",
]

arrangers_keys_list = [
    'isin', 
    'arranger',
    'contactPerson',
    'regOffAddr',
    'contact',
    'email',
    'website'
]

arrangers_values_to_find = [
    'isin', 
    'arranger',
    'contactPerson',
    'address',
    'contactDetails',
    'emailID',
    'websiteAddress'
]
# default details = list





# data_set = [(init_keys,init_values),(op_keys_list,op_values_to_find),(cf_keys_list,cf_values_to_find),(bs_keys_list,bs_values_to_find)]
