#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 16:14:45 2022

@author: jiahuiwu
"""

import pandas as pd
import numpy as np

rawData = pd.read_csv("Contracts_PrimeAwardSummaries_2022-05-05_H01M59S10_1.csv")

rawData = rawData.drop(["parent_award_agency_id", "parent_award_agency_name", "parent_award_id_piid", "disaster_emergency_fund_codes",
                    "outlayed_amount_funded_by_COVID-19_supplementals", "obligated_amount_funded_by_COVID-19_supplementals", 
                    "ordering_period_end_date",
                    "foreign_funding_description", "sam_exception", "sam_exception_description", "recipient_doing_business_as_name",
                    "cage_code", "recipient_congressional_district", "award_or_idv_flag", "award_type", "idv_type_code", "idv_type", 
                    "multiple_or_single_award_idv_code", 
                    "multiple_or_single_award_idv",
                    "type_of_idc_code", "type_of_idc", "inherently_governmental_functions", "inherently_governmental_functions_description",
                    "contract_bundling_code", "contract_bundling", "research_code", "research", "fair_opportunity_limited_sources_code", 
                    "fair_opportunity_limited_sources", "other_than_full_and_open_competition_code", 
                    "other_than_full_and_open_competition", "number_of_offers_received", "program_acronym",
                    "cost_accounting_standards_clause_code", "cost_accounting_standards_clause", 
                    "alaskan_native_corporation_owned_firm", "american_indian_owned_business",
                    "indian_tribe_federally_recognized", "native_hawaiian_organization_owned_firm",	
                    "tribally_owned_firm",
                    "veteran_owned_business",	
                    "service_disabled_veteran_owned_business",
                    'woman_owned_business',
                    'women_owned_small_business',
                    'economically_disadvantaged_women_owned_small_business',
                    'joint_venture_women_owned_small_business',
                    'joint_venture_economic_disadvantaged_women_owned_small_bus',
                    'minority_owned_business',
                    'subcontinent_asian_asian_indian_american_owned_business',
                    'asian_pacific_american_owned_business',
                    'black_american_owned_business',
                    'hispanic_american_owned_business',
                    'native_american_owned_business',
                    'other_minority_owned_business',
                    'contracting_officers_determination_of_business_size',
                    'contracting_officers_determination_of_business_size_code',
                    'emerging_small_business',
                    'community_developed_corporation_owned_firm',
                    'labor_surplus_area_firm',
                    'us_federal_government',
                    'federally_funded_research_and_development_corp',
                    'federal_agency',
                    'us_state_government',
                    'us_local_government',
                    'city_local_government',
                    'county_local_government',
                    'inter_municipal_local_government',
                    'local_government_owned',
                    'municipality_local_government',
                    'school_district_local_government',
                    'township_local_government',
                    'us_tribal_government',
                    'foreign_government',
                    'organizational_type',
                    'corporate_entity_not_tax_exempt',
                    'corporate_entity_tax_exempt',
                    'partnership_or_limited_liability_partnership',
                    'sole_proprietorship',
                    'small_agricultural_cooperative',
                    'international_organization',
                    'us_government_entity',
                    'community_development_corporation',
                    'domestic_shelter',
                    'educational_institution',
                    'foundation',
                    'hospital_flag',
                    'manufacturer_of_goods',
                    'veterinary_hospital',
                    'hispanic_servicing_institution',
                    'receives_contracts',
                    'receives_financial_assistance',
                    'receives_contracts_and_financial_assistance',
                    'airport_authority',
                    'council_of_governments',
                    'housing_authorities_public_tribal',
                    'interstate_entity',
                    'planning_commission',
                    'port_authority',
                    'transit_authority',
                    'subchapter_scorporation',
                    'limited_liability_corporation',
                    'foreign_owned',
                    'for_profit_organization',
                    'nonprofit_organization',
                    'other_not_for_profit_organization',
                    'the_ability_one_program',
                    'private_university_or_college',
                    'state_controlled_institution_of_higher_learning',
                    '1862_land_grant_college',
                    '1890_land_grant_college',
                    '1994_land_grant_college',
                    'minority_institution',
                    'historically_black_college',
                    'tribal_college',
                    'alaskan_native_servicing_institution',
                    'native_hawaiian_servicing_institution',
                    'school_of_forestry',
                    'veterinary_college',
                    'dot_certified_disadvantage',
                    'self_certified_small_disadvantaged_business',
                    'small_disadvantaged_business',
                    'c8a_program_participant',
                    'historically_underutilized_business_zone_hubzone_firm',
                    'sba_certified_8a_joint_venture',
                    'highly_compensated_officer_1_name',
                    'highly_compensated_officer_1_amount',
                    'highly_compensated_officer_2_name',
                    'highly_compensated_officer_2_amount',
                    'highly_compensated_officer_3_name',
                    'highly_compensated_officer_3_amount',
                    'highly_compensated_officer_4_name',
                    'highly_compensated_officer_4_amount',
                    'highly_compensated_officer_5_name',
                    'highly_compensated_officer_5_amount'], axis = 1)




data = rawData[["awarding_agency_name", 
                "awarding_agency_code", 
                "recipient_name",
                "recipient_address_line_1", 
                "recipient_address_line_2", 
                "recipient_state_code", 
                "recipient_state_name", 
                "recipient_state_name",
                "recipient_zip_4_code",
                "period_of_performance_start_date",
                "potential_total_value_of_award",
                "recipient_parent_name",
                "primary_place_of_performance_city_name",
                "primary_place_of_performance_county_name",
                "primary_place_of_performance_state_code",
                "primary_place_of_performance_state_name",
                "primary_place_of_performance_zip_4",
                "product_or_service_code_description",
                ]]

#check missing value
sum(data['recipient_name'] == "")
sum(data['recipient_name'].isna())

sum(data['recipient_state_code'] == "")
sum(data['recipient_state_code'].isna())

sum(data['period_of_performance_start_date'] == "")
sum(data['period_of_performance_start_date'].isna())

sum(data['potential_total_value_of_award'] == "" ) 
sum(data['potential_total_value_of_award'].isna())

sum(data["recipient_zip_4_code"].isna())
data = data.loc[data["recipient_zip_4_code"].notna(),]




data["recipient_address"] = data["recipient_address_line_1"].astype(str) + data["recipient_address_line_2"].astype(str)
data = data.drop(["recipient_address_line_1", "recipient_address_line_2"], axis = 1)

data.to_csv("out.csv")




