import os
import streamlit as st
import pandas as pd
import mysql.connector
import json
import numpy as np
import plotly.express as px
import plotly.io as pio

MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "phone_pe"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""

india = json.load(open("states_india.geojson","r"))



mysql_conn = mysql.connector.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    database=MYSQL_DATABASE,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD
)
mysql_cursor = mysql_conn.cursor()
ID = []
state_list = []
Year = []
Quarter = []
State = []
District = []
Registered_Users = []
Total_transaction_Count = []
Total_transaction_Amount = []
Recharge_bill_payments_Count = []
Recharge_bill_payments_Amount = []
Peer_to_peer_payments_Count = []
Peer_to_peer_payments_Amount = []
Merchant_payments_Count = []
Merchant_payments_Amount = []
Financial_Services_Count = []
Financial_Services_Amount = []
Other_payment_Count = []
Other_payment_Amount = []
is_data_available = [0,0,0,0,0]
count_array = [0,0,0,0,0]
amount_array = [0,0,0,0,0]
payment_category = {
	"Recharge & bill payments":0,
	"Peer-to-peer payments":1,
	"Merchant payments":2,
	"Financial Services":3,
	"Others":4
}
# State_ID = {
# 	'andaman & nicobar islands': 'AN',
# 	'andhra pradesh' : 'AP',
# 	'puducherry': 'PY',
# 	'tamil nadu' : 'TN',
# 	'uttar pradesh': 'UP',
# 	'madhya pradesh' : 'MP',
# 	'tripura': 'TR',
# 	'lakshadweep' : 'LD',
# 	'manipur' : 'MN',
# 	'maharashtra' : 'MH',
# 	'dadra & nagar haveli & daman & diu' : 'DD',
# 	'meghalaya' : 'ML',
# 	'haryana' : 'HR',
# 	'rajasthan' : 'RJ',
# 	'ladakh' : 'LA',
# 	'punjab' : 'PB',
# 	'assam' : 'AS',
# 	'jharkhand': 'JH',
# 	'odisha' : 'OR',
# 	'bihar' : 'BR',
# 	'kerala' : 'KL',
# 	'karnataka': 'KA',
# 	'chandigarh': 'CH',
# 	'telangana' : 'TG',
# 	'himachal pradesh': 'HP' ,
# 	'west bengal' : 'WB',
# 	'gujarat': 'GJ',
# 	'sikkim': 'SK',
# 	'nagaland': 'NL',
# 	'mizoram': 'MZ',
# 	'chhattisgarh': 'CT',
# 	'jammu & kashmir': 'JK',
# 	'goa': 'GA',
# 	'arunachal pradesh': 'AR',
# 	'delhi': 'DL',
# 	'uttarakhand': 'UT',
# }
State_ID = {
	'andaman & nicobar islands': 35,
	'andhra pradesh' : 28,
	'puducherry': 34,
	'tamil nadu' : 33,
	'uttar pradesh': 9,
	'madhya pradesh' : 23,
	'tripura': 16,
	'lakshadweep' : 31,
	'manipur' : 14,
	'maharashtra' : 27,
	'dadra & nagar haveli & daman & diu' : 25,
	'meghalaya' : 17,
	'haryana' : 6,
	'rajasthan' : 8,
	'ladakh' : 40,
	'punjab' : 3,
	'assam' : 18,
	'jharkhand': 20,
	'odisha' : 21,
	'bihar' : 10,
	'kerala' : 32,
	'karnataka': 29,
	'chandigarh': 4,
	'telangana' : 0,
	'himachal pradesh': 2 ,
	'west bengal' : 19,
	'gujarat': 24,
	'sikkim': 11,
	'nagaland': 13,
	'mizoram': 15,
	'chhattisgarh': 22,
	'jammu & kashmir': 1,
	'goa': 30,
	'arunachal pradesh': 12,
	'delhi': 7,
	'uttarakhand': 5,
}
def clear_arrays():
	state_list.clear()
	ID.clear()
	Year.clear()
	Quarter.clear()
	State.clear()
	District.clear()
	Registered_Users.clear()
	Total_transaction_Count.clear()
	Total_transaction_Amount.clear()
	Recharge_bill_payments_Count.clear()
	Recharge_bill_payments_Amount.clear()
	Peer_to_peer_payments_Count.clear()
	Peer_to_peer_payments_Amount.clear()
	Merchant_payments_Count.clear()
	Merchant_payments_Amount.clear()
	Financial_Services_Count.clear()
	Financial_Services_Amount.clear()
	Other_payment_Count.clear()
	Other_payment_Amount.clear()

def get_country_data():
	clear_arrays()
	for year in os.listdir(f"C:/Users/SHAMS NAVEETH/Desktop/phonepe/Phonepe-data-master/data/aggregated/transaction/country/india/"):
		if(year == "state"):
			continue
		for quarter in range(1,5):
			transcation_data = pd.read_json(f"C:/Users/SHAMS NAVEETH/Desktop/phonepe/Phonepe-data-master/data/aggregated/transaction/country/india/{year}/{quarter}.json")
			user_data = pd.read_json(f"C:/Users/SHAMS NAVEETH/Desktop/phonepe/Phonepe-data-master/data/aggregated/user/country/india/{year}/{quarter}.json")
			Year.append(year)
			Quarter.append(quarter)
			Registered_Users.append(user_data['data']['aggregated']['registeredUsers'])
			count_array = [0,0,0,0,0]
			amount_array = [0,0,0,0,0]
			for category in transcation_data['data']['transactionData']:
				count_array[payment_category[category['name']]] = category['paymentInstruments'][0]['count']
				amount_array[payment_category[category['name']]] = category['paymentInstruments'][0]['amount']
		
			Recharge_bill_payments_Count.append(count_array[0])
			Recharge_bill_payments_Amount.append(amount_array[0])
			Peer_to_peer_payments_Count.append(count_array[1])
			Peer_to_peer_payments_Amount.append(amount_array[1])
			Merchant_payments_Count.append(count_array[2])
			Merchant_payments_Amount.append(amount_array[2])
			Financial_Services_Count.append(count_array[3])
			Financial_Services_Amount.append(amount_array[3])
			Other_payment_Count.append(count_array[4])
			Other_payment_Amount.append(amount_array[4])

	mysql_cursor.execute("""
         DROP TABLE IF EXISTS Country;
	""")
	mysql_cursor.execute("""
		CREATE TABLE IF NOT EXISTS Country (
			Year INT,
			Quarter INT, 
			Registered_Users INT,
			Recharge_bill_payments_Count INT,
			Recharge_bill_payments_Amount INT,
			Peer_to_peer_payments_Count INT,
			Peer_to_peer_payments_Amount INT,
			Merchant_payments_Count INT,
			Merchant_payments_Amount INT,
			Financial_Services_Count INT,
			Financial_Services_Amount INT,
			Other_payment_Count INT,
			Other_payment_Amount INT
        );
    """)
	for x in range(0, len(Year)):
	    mysql_cursor.execute("""
	        INSERT INTO Country(Year, Quarter, Registered_Users, Recharge_bill_payments_Count, Recharge_bill_payments_Amount,  
	            Peer_to_peer_payments_Count, Peer_to_peer_payments_Amount, Merchant_payments_Count, Merchant_payments_Amount, 
	            Financial_Services_Count, Financial_Services_Amount, Other_payment_Count, Other_payment_Amount)
	        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
	        """, (
	        Year[x],
	        Quarter[x],
	        Registered_Users[x],
	        Recharge_bill_payments_Count[x],
	        Recharge_bill_payments_Amount[x],
	        Peer_to_peer_payments_Count[x],
	        Peer_to_peer_payments_Amount[x],
	        Merchant_payments_Count[x],
	        Merchant_payments_Amount[x],
	        Financial_Services_Count[x],
	        Financial_Services_Amount[x],
	        Other_payment_Count[x],
	        Other_payment_Amount[x]
	        ))
	    mysql_conn.commit()

	

def get_state_data():
	clear_arrays()
	for folder in os.listdir("C:/Users/SHAMS NAVEETH/Desktop/phonepe/Phonepe-data-master/data/aggregated/transaction/country/india/state"):
		for year in os.listdir(f"C:/Users/SHAMS NAVEETH/Desktop/phonepe/Phonepe-data-master/data/aggregated/transaction/country/india/state/{folder}"):
			for quarter in range(1,5):
				transcation_data = pd.read_json(f"C:/Users/SHAMS NAVEETH/Desktop/phonepe/Phonepe-data-master/data/aggregated/transaction/country/india/state/{folder}/{year}/{quarter}.json")
				user_data = pd.read_json(f"C:/Users/SHAMS NAVEETH/Desktop/phonepe/Phonepe-data-master/data/aggregated/user/country/india/state/{folder}/{year}/{quarter}.json")
				ID.append(State_ID[folder.replace('-',' ')])
				State.append(folder.replace('-',' '))
				Year.append(year)
				Quarter.append(quarter)
				Registered_Users.append(user_data['data']['aggregated']['registeredUsers'])
				count_array = [0,0,0,0,0]
				amount_array = [0,0,0,0,0]
				for category in transcation_data['data']['transactionData']:
					count_array[payment_category[category['name']]] = category['paymentInstruments'][0]['count']
					amount_array[payment_category[category['name']]] = category['paymentInstruments'][0]['amount']
			
				Recharge_bill_payments_Count.append(count_array[0])
				Recharge_bill_payments_Amount.append(amount_array[0])
				Peer_to_peer_payments_Count.append(count_array[1])
				Peer_to_peer_payments_Amount.append(amount_array[1])
				Merchant_payments_Count.append(count_array[2])
				Merchant_payments_Amount.append(amount_array[2])
				Financial_Services_Count.append(count_array[3])
				Financial_Services_Amount.append(amount_array[3])
				Other_payment_Count.append(count_array[4])
				Other_payment_Amount.append(amount_array[4])


	for i in range(0,len(State)):
		print(f"{State[i]} - {Year[i]} - {Quarter[i]} - {Financial_Services_Count[i]} - {Registered_Users[i]}")
	mysql_cursor.execute("""
         DROP TABLE IF EXISTS State;
	""")
	mysql_cursor.execute("""
		CREATE TABLE IF NOT EXISTS State (
			State VARCHAR(255),
			ID INT,
			Year INT,
			Quarter INT, 
			Registered_Users INT,
			Recharge_bill_payments_Count INT,
			Recharge_bill_payments_Amount INT,
			Peer_to_peer_payments_Count INT,
			Peer_to_peer_payments_Amount INT,
			Merchant_payments_Count INT,
			Merchant_payments_Amount INT,
			Financial_Services_Count INT,
			Financial_Services_Amount INT,
			Other_payment_Count INT,
			Other_payment_Amount INT
        );
    """)
	for x in range(0, len(State)):
	    mysql_cursor.execute("""
	        INSERT INTO State(State, ID,  Year, Quarter, Registered_Users, Recharge_bill_payments_Count, Recharge_bill_payments_Amount,  
	            Peer_to_peer_payments_Count, Peer_to_peer_payments_Amount, Merchant_payments_Count, Merchant_payments_Amount, 
	            Financial_Services_Count, Financial_Services_Amount, Other_payment_Count, Other_payment_Amount)
	        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
	        """, (
	        State[x],
	        ID[x],
	        Year[x],
	        Quarter[x],
	        Registered_Users[x],
	        Recharge_bill_payments_Count[x],
	        Recharge_bill_payments_Amount[x],
	        Peer_to_peer_payments_Count[x],
	        Peer_to_peer_payments_Amount[x],
	        Merchant_payments_Count[x],
	        Merchant_payments_Amount[x],
	        Financial_Services_Count[x],
	        Financial_Services_Amount[x],
	        Other_payment_Count[x],
	        Other_payment_Amount[x]
	        ))
	    mysql_conn.commit()

def get_state_map_data():
	clear_arrays()
	for year in os.listdir(f"C:/Users/SHAMS NAVEETH/Desktop/phonepe/Phonepe-data-master/data/map/transaction/hover/country/india"):
		if(year == "state"):
			continue
		for quarter in range(1,5):
			transcation_data = pd.read_json(f"C:/Users/SHAMS NAVEETH/Desktop/phonepe/Phonepe-data-master/data/map/transaction/hover/country/india/{year}/{quarter}.json")
			user_data = pd.read_json(f"C:/Users/SHAMS NAVEETH/Desktop/phonepe/Phonepe-data-master/data/map/user/hover/country/india/{year}/{quarter}.json")
			for state in transcation_data['data']['hoverDataList']:
				Year.append(year)
				Quarter.append(quarter)
				State.append(state['name'])
				ID.append(State_ID[state['name']])
				Total_transaction_Count.append(state['metric'][0]["count"])
				Total_transaction_Amount.append(state['metric'][0]['amount'])
				Registered_Users.append(user_data['data']['hoverData'][state['name']]['registeredUsers'])

	mysql_cursor.execute("""
         DROP TABLE IF EXISTS State_map;
	""")
	mysql_cursor.execute("""
		CREATE TABLE IF NOT EXISTS State_map (
			State VARCHAR(255),
			ID INT,
			Year INT,
			Quarter INT, 
			Total_transaction_amount BIGINT,
			Total_transaction_count INT,
			Registered_users INT
        );
    """)
	for x in range(0, len(State)):
	    mysql_cursor.execute("""
	        INSERT INTO State_map(State, ID, Year, Quarter, Total_transaction_amount,Total_transaction_count,Registered_users)
	        VALUES (%s, %s, %s, %s, %s, %s, %s);
	        """, (
	        State[x],
	        ID[x],
	        Year[x],
	        Quarter[x],
	        Total_transaction_Amount[x],
	        Total_transaction_Count[x],
	        Registered_Users[x]
	        ))
	    mysql_conn.commit()

def get_district_map_data():
	clear_arrays()
	for folder in os.listdir("C:/Users/SHAMS NAVEETH/Desktop/phonepe/Phonepe-data-master/data/map/transaction/hover/country/india/state"):
		for year in os.listdir(f"C:/Users/SHAMS NAVEETH/Desktop/phonepe/Phonepe-data-master/data/map/transaction/hover/country/india/state/{folder}"):
			for quarter in range(1,5):
				transcation_data = pd.read_json(f"C:/Users/SHAMS NAVEETH/Desktop/phonepe/Phonepe-data-master/data/map/transaction/hover/country/india/state/{folder}/{year}/{quarter}.json")
				user_data = pd.read_json(f"C:/Users/SHAMS NAVEETH/Desktop/phonepe/Phonepe-data-master/data/map/user/hover/country/india/state/{folder}/{year}/{quarter}.json")
				for district in transcation_data['data']['hoverDataList']:
					State.append(folder.replace('-',' '))
					Year.append(year)
					Quarter.append(quarter)
					District.append(district['name'])
					Total_transaction_Count.append(district['metric'][0]["count"])
					Total_transaction_Amount.append(district['metric'][0]['amount'])
					Registered_Users.append(user_data['data']['hoverData'][district['name']]['registeredUsers'])
	mysql_cursor.execute("""
         DROP TABLE IF EXISTS District_map;
	""")
	mysql_cursor.execute("""
		CREATE TABLE IF NOT EXISTS District_map (
			State VARCHAR(255),
			District VARCHAR(255),
			Year INT,
			Quarter INT, 
			Total_transaction_amount BIGINT,
			Total_transaction_count INT,
			Registered_users INT
        );
    """)

	for x in range(0, len(State)):
	    mysql_cursor.execute("""
	        INSERT INTO District_map(State, District, Year, Quarter, Total_transaction_amount,Total_transaction_count,Registered_users)
	        VALUES (%s, %s, %s, %s, %s, %s, %s);
	        """, (
	        State[x],
	        District[x],
	        Year[x],
	        Quarter[x],
	        Total_transaction_Amount[x],
	        Total_transaction_Count[x],
	        Registered_Users[x]
	        ))
	    mysql_conn.commit()


def show_map_data(data_option,year_option,quarter_option):
	print(data_option,year_option,quarter_option)
	sql_query = f"SELECT ID, {data_option}, State FROM State_map WHERE Quarter = {quarter_option} and Year = {year_option}"
	# mysql_cursor.execute("""
	#     SELECT  ID, `%s` ,State
	#     FROM State_map
	#     WHERE Quarter = %s and Year = %s
	# """,
	# (data_option,quarter_option,year_option) ) 
	mysql_cursor.execute(sql_query) 
	# for st in india['features']:
	# 	st["ID"] = st["properties"]["state_code"]

	results = mysql_cursor.fetchall()
	df = pd.DataFrame(results,columns = ["ID",data_option,"Name"])
	print(df)		
	fig = px.choropleth(
	    df,
	    locations="ID",
	    featureidkey = "properties.state_code",
	    geojson=india,
	    color=data_option,
	    # projection = "mercator",
	    hover_name="Name",
	    hover_data=[data_option],
	    title=f"{data_option.replace('_',' ')} for Year {year_option} and quarter {quarter_option}",
	    color_continuous_scale = [[0,'rgb(0,200,0)'],
	    								[0.5, 'rgb(0,0,200)'],
	    								[0.75, 'rgb(180,0,0)'],
	    								[1,'rgb(255,0,0)']]
	)	
	fig.update_coloraxes(showscale=False)	
	fig.update_geos(fitbounds="locations", visible=False, bgcolor = "rgba(0,0,0,0)")
	# fig.update_layout(width = 1000)

	fig.update_layout(
        autosize=False,
        margin = dict(
                l=0,
                r=0,
                b=0,
                t=20,
                pad=1,
                autoexpand=True
            ),
            width=800,
            # height=400,
    )
	fig.update_traces(hoverinfo = "none")
	st.plotly_chart(fig)

def get_map_data():
	clear_arrays()
	get_state_map_data()
	get_district_map_data()

def show_table_data(data_option,year_option,quarter_option):
	if(data_option == "Country wide detailed transaction data"):
		sql_query = f"SELECT Recharge_bill_payments_Count,Peer_to_peer_payments_Count,Financial_Services_Count,Merchant_payments_Count,Other_payment_Count FROM country WHERE Quarter = {quarter_option} and Year = {year_option}"	
		mysql_cursor.execute(sql_query)
		results = mysql_cursor.fetchall()
		df = pd.DataFrame(results, columns= ["Recharges Count","P2P Count","Financial Services Count","Merchant payments Count","Others Count"])
		st.write(df)
	if(data_option == "State wise detailed transaction data"):
		sql_query = f"SELECT State,Recharge_bill_payments_Count,Peer_to_peer_payments_Count,Financial_Services_Count,Merchant_payments_Count,Other_payment_Count FROM State WHERE Quarter = {quarter_option} and Year = {year_option}"	
		mysql_cursor.execute(sql_query)
		results = mysql_cursor.fetchall()
		df = pd.DataFrame(results, columns= ["State","Recharges Count","P2P Count","Financial Services Count","Merchant payments Count","Others Count"])
		st.write(df)
	if(data_option == "Top 10 states in terms of transaction value"):
		sql_query = f"SELECT  State, Total_transaction_Amount FROM State_map WHERE Quarter = {quarter_option} and Year = {year_option} ORDER BY Total_transaction_Amount DESC LIMIT 10"	
		mysql_cursor.execute(sql_query)
		results = mysql_cursor.fetchall()
		df = pd.DataFrame(results, columns= ["State","Total_transaction_Amount"])
		st.write(df)
	if(data_option == "Top 10 states in terms of user count"):
		sql_query = f"SELECT  State, Registered_Users FROM State_map WHERE Quarter = {quarter_option} and Year = {year_option} ORDER BY Registered_Users DESC LIMIT 10"	
		mysql_cursor.execute(sql_query)
		results = mysql_cursor.fetchall()
		df = pd.DataFrame(results, columns= ["State","User count"])
		st.write(df)	
	if(data_option == "Top 10 districts in terms of transaction value"):
		sql_query = f"SELECT  District, State, Total_transaction_Amount FROM District_map WHERE Quarter = {quarter_option} and Year = {year_option} ORDER BY Total_transaction_Amount DESC LIMIT 10"	
		mysql_cursor.execute(sql_query)
		results = mysql_cursor.fetchall()
		df = pd.DataFrame(results, columns= ["District","State","Total_transaction_Amount"])
		st.write(df)
	if(data_option == "Top 10 districts in terms of user count"):
		sql_query = f"SELECT  District, State, Registered_Users FROM District_map WHERE Quarter = {quarter_option} and Year = {year_option} ORDER BY Registered_Users DESC LIMIT 10"	
		mysql_cursor.execute(sql_query)
		results = mysql_cursor.fetchall()
		df = pd.DataFrame(results, columns= ["District","State","User count"])
		st.write(df)
	if(data_option == "Total transactional value for all states till now"):
		sql_query = f"SELECT  State, SUM(Total_transaction_Amount) FROM State_map GROUP BY State"	
		mysql_cursor.execute(sql_query)
		results = mysql_cursor.fetchall()
		df = pd.DataFrame(results, columns= ["State","Total transactional value"])
		st.write(df)
def main():
	table_data_options = ["Country wide detailed transaction data","State wise detailed transaction data",
							"Top 10 states in terms of transaction value","Top 10 states in terms of user count",
							"Top 10 districts in terms of transaction value", "Top 10 districts in terms of user count",
							"Total transactional value for all states till now"]

	visual_option = st.sidebar.selectbox("select the type of data you wish to see", options = ["map","table"])
	if(visual_option == "map"):
		data_option = st.sidebar.selectbox("select data you wish to see", options =  ["Registered_Users","Total_transaction_Amount","Total_transaction_Count"])
		year_option = st.sidebar.selectbox("select year", options = range(2018,2023))
		quarter_option = st.sidebar.selectbox("select quarter", options = range(1,5))
		if(st.sidebar.button("Show map")):
			show_map_data(data_option, year_option, quarter_option)
	if(visual_option == "table"):
		data_option = st.sidebar.selectbox("Select data you wish to see",options = table_data_options)
		if(data_option!="Total transactional value for all states till now"):
			year_option = st.sidebar.selectbox("select year", options = range(2018,2023))
			quarter_option = st.sidebar.selectbox("select quarter", options = range(1,5))
		else:
			year_option = 0
			quarter_option = 0

		if(st.sidebar.button("Show table")):
			show_table_data(data_option, year_option, quarter_option)	
	if(st.sidebar.button("fetch data")):
		get_country_data()		
		get_state_data()
		get_map_data()
if __name__ == '__main__':
    main()
