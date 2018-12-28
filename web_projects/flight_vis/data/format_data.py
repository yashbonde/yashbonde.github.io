'''
Following are the tasks done by this script:
* add information about the airport by also giving out names
* finalise a data frame with following fields:
  ['AP_CODE', 'AP_NAME', 'FLT_OPERATOR', 'FLT_NUMBER', 'TAKE_OFF_TIME']
* store the dataframe in JSON format

===== Proper JSON Format is =====

{ "record1":
    {"SourceAirportCode":"AGR",
     "SourceAirport":"Agra",
     "DestinationAirportCode":"VNS",
     "DestinationAirport":"Varanasi",
     "AirlineCode":"AI",
     "AirlineName":"Air India",
     "FlightNumber":406,
     "ScheduledTime":1320},
  "record2":
    {"SourceAirportCode":"AGR",
     "SourceAirport":"Agra",
     "DestinationAirportCode":"VNS",
     "DestinationAirport":"Varanasi",
     "AirlineCode":"AI",
     "AirlineName":"Air India",
     "FlightNumber":406,
     "ScheduledTime":1320}
}

=================================

NOTE: all the data is for 2017, latest data could not be obtained
'''

import pandas as pd
import json

city_code = {
    'AGX': 'Agatti Island',
    'AMD': 'Ahmedabad',
    'AJL': 'Aizawl',
    'AKD': 'Akola',
    'IXV': 'Along',
    'LKO': 'Lucknow',
    'LUH': 'Ludhiana',
    'IXB': 'Bagdogra',
    'IXE': 'Mangalore',
    'IXL': 'Leh',
    'RGH': 'Balurghat',
    'IXD': 'Allahabad',
    'SHL': 'Shillong',
    'BEK': 'Bareli',
    'BEP': 'Bellary',
    'BLR': 'Bangalore',
    'BUP': 'Bhatinda',
    'BHU': 'Bhavnagar',
    'BHO': 'Bhopal',
    'BBI': 'Bhubaneswar',
    'BKB': 'Bikaner',
    'PAB': 'Bilaspur',
    'IXR': 'Ranchi',
    'GAU': 'Guwahati',
    'CBD': 'Car Nicobar',
    'IXC': 'Chandigarh',
    'MAA': 'Chennai',
    'BOM': 'Mumbai',
    'IXU': 'Aurangabad',
    'COK': 'Kochi',
    'COH': 'Cooch Behar',
    'CDP': 'Cuddapah',
    'UDR': 'Udaipur',
    'GOI': 'Goa',
    'NMB': 'Daman',
    'DAE': 'Daparizo',
    'DAI': 'Darjeeling',
    'DED': 'Dehra Dun',
    'DEP': 'Deparizo',
    'IDR': 'Indore',
    'DBD': 'Dhanbad',
    'DIB': 'Dibrugarh',
    'DMU': 'Dimapur',
    'DIU': 'Diu',
    'DHM': 'Dharamsala',
    'ISK': 'Nasik',
    'GAY': 'Gaya',
    'GOP': 'Gorakhpur',
    'JGA': 'Jamnagar',
    'GUX': 'Guna',
    'GWL': 'Gwalior',
    'HSS': 'Hissar',
    'HBX': 'Hubli',
    'HYD': 'Hyderabad',
    'DEL': 'New Delhi',
    'JLR': 'Jabalpur',
    'JGB': 'Jagdalpur',
    'JSA': 'Jaisalmer',
    'PYB': 'Jeypore',
    'JDH': 'Jodhpur',
    'IXH': 'Kailashahar',
    'IXQ': 'Kamalpur',
    'IXY': 'Kandla',
    'KNU': 'Kanpur',
    'IXK': 'Keshod',
    'HJR': 'Khajuraho',
    'AGR': 'Agra',
    'IXN': 'Khowai',
    'KLH': 'Kolhapur',
    'KTU': 'Kota',
    'CCJ': 'Kozhikode',
    'KUU': 'Bhuntar Kullu',
    'IXS': 'Silchar',
    'IXI': 'Lilabari',
    'PNQ': 'Pune',
    'IXM': 'Madurai',
    'LDA': 'Malda',
    'MOH': 'Mohanbari',
    'IMF': 'Imphal',
    'MZA': 'Muzaffarnagar',
    'MZU': 'Muzaffarpur',
    'MYQ': 'Mysore',
    'NDC': 'Nanded',
    'CCU': 'Kokata',
    'NVY': 'Neyveli',
    'OMN': 'Osmanabad',
    'PGH': 'Pantnagar',
    'IXT': 'Pasighat',
    'IXP': 'Pathankot',
    'PAT': 'Patna',
    'CJB': 'Coimbatore',
    'PNY': 'Pondicherry',
    'PBD': 'Porbandar',
    'IXZ': 'Port Blair',
    'PUT': 'Puttaparthi',
    'RPR': 'Raipur',
    'ATQ': 'Amritsar',
    'RJA': 'Rajamundry',
    'RAJ': 'Rajkot',
    'RJI':'Rajouri',
    'RMD': 'Ramagundam',
    'RTC': 'Ratnagiri',
    'REW': 'Rewa',
    'RRK': 'Rourkela',
    'JRH': 'Jorhat',
    'BHJ': 'Bhuj',
    'RUP': 'Rupsi',
    'SXV': 'Salem',
    'TEZ': 'Tezpur',
    'IXG': 'Belgaum',
    'JAI': 'Jaipur',
    'TNI': 'Satna',
    'IXJ': 'Jammu',
    'SSE': 'Sholapur',
    'SLV': 'Shimla',
    'IXA': 'Agartala',
    'IXW': 'Jamshedpur',
    'NAG': 'Nagpur',
    'SXR': 'Srinagar',
    'STV': 'Surat',
    'TEI': 'Tezu',
    'TJV': 'Thanjavur',
    'TRV': 'Trivandrum',
    'TIR': 'Tirupati',
    'TRZ': 'Trichy',
    'TCR': 'Tuticorin',
    'BDQ': 'Vadodara',
    'VNS': 'Varanasi',
    'VGA': 'Vijayawada',
    'VTZ': 'Vishakhapatnam',
    'WGC': 'Warangal',
    'ZER': 'Zero',
    'SAG': 'Shirdi',
    'TCN': 'Tehuacan',
    'VDY': 'Vidyanagar'
}

operator_code_ = {
    '9I' : 'Alliance Air',
    'S2' : 'Jet Lite',
    '6E' : 'Indigo',
    '9W' : 'Jet Airways',
    'AI' : 'Air India',
    'SG' : 'Spice Jet',
    'UK' : 'Vistara Air',
    'G8' : 'Go Air',
    'I5' : 'Air Asia',
    '2T' : 'True Jet',
    'LB' : 'Air Costa (defunct)'
}

# script
df = pd.read_csv('./flight_schedule.csv')

# get final columns and dropping columns
cols = ['SrcAirportCode', 'SrcAirportName', 'DstAirportCode', 'DstAirportName',
        'AirlineCode', 'AirlineName', 'FlightNumber', 'ScheduledTime']

cols_drop = ['ARRIVAL_DEPARTURE_FLAG', 'TIME_ZONE', 'EFF_DT_FROM', 'EFF_DT_TILL']

# drop columns
df = df.drop(columns = cols_drop)

# get the data in a dictionary and convert it to data frame
src_ = df['LOCAL_AIRPORT'].values.tolist()
src_full_ = [city_code[i] for i in src_]
dst_ = df['SOURCE_DESTINATION'].values.tolist()
dst_full_ = [city_code[i] for i in dst_]
arl_ = df['AIRLINE_CODE'].values.tolist()
arl_full_ = [operator_code_[i] for i in arl_]
fltnum_ = df['FLIGHT_NUMBER'].values.tolist()
scht_ = df['SCHED_TIME'].values.tolist()

df_cols = ['SourceAirportCode', 'SourceAirport', 'DestinationAirportCode',
           'DestinationAirport', 'AirlineCode', 'AirlineName', 'FlightNumber',
           'ScheduledTime']
list_con = [src_, src_full_, dst_, dst_full_, arl_, fltnum_, scht_]

# df_dump = pd.DataFrame(df_dict)

df_ = {
    'SourceAirportCode': src_,
    'SourceAirport': src_full_,
    'DestinationAirportCode': dst_,
    'DestinationAirport': dst_full_,
    'AirlineCode': arl_,
    'FlightNumber': fltnum_,
    'ScheduledTime': scht_
}

# 
with open('./flight_data.json', 'w') as f:
    json.dump(df_, f)

print('[*] JSON saved at: ./flight_data.json')