import json
import os
import requests
# import subprocess
import pandas as pd
import mysql.connector as sql
# import streamlit as st
# from PIL import Image
# from streamlit_option_menu import option_menu
# import plotly.express as px

# data = requests.get('https://api.github.com/repos/PhonePe/pulse')
# repo = data.json()
# clone_url = repo['clone_url']

repo_name = 'pulse'
clone_dir = os.path.join(os.getcwd(), repo_name)
# subprocess.run(["git", "clone", clone_url, clone_dir], check=True)

#Agg_trans
path = '/Users/hemap/PycharmProjects/pulse/data/aggregated/transaction/country/india/state/'
Agg_state_list = os.listdir(path)
# Agg_state_list

df1 = {'State':[], 'Year':[], 'Quarter': [], 'Transaction_type': [],'Transaction_count': [], 'Transaction_amount':[]}
for i in Agg_state_list:
    p_i=path+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['transactionData']:
              Name=z['name']
              count=z['paymentInstruments'][0]['count']
              amount=z['paymentInstruments'][0]['amount']
              df1['Transaction_type'].append(Name)
              df1['Transaction_count'].append(count)
              df1['Transaction_amount'].append(amount)
              df1['State'].append(i)
              df1['Year'].append(j)
              df1['Quarter'].append(int(k.strip('.json')))
Agg_transaction = pd.DataFrame(df1)

#Agg_users
path1 = '/Users/hemap/PycharmProjects/pulse/data/aggregated/user/country/india/state/'
Agg_state2_list = os.listdir(path1)
# Agg_state2_list

df2 = {'State':[], 'Year':[], 'Quarter': [], 'brand':[],'reg_users_count':[],'percentage':[]}
for i in Agg_state2_list:
    p_i=path1+i+"/"
    Agg_yr=os.listdir(p_i)
    for j in Agg_yr:
        p_j=p_i+j+"/"
        Agg_yr_list=os.listdir(p_j)
        for k in Agg_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            try:
              for z in D['data']['usersByDevice']:
                Name=z['brand']
                count=z['count']
                percentage=z['percentage']
                df2['brand'].append(Name)
                df2['reg_users_count'].append(count)
                df2['percentage'].append(percentage)
                df2['State'].append(i)
                df2['Year'].append(j)
                df2['Quarter'].append(int(k.strip('.json')))
            except:
              pass
Agg_users = pd.DataFrame(df2)

path2 = '/Users/hemap/PycharmProjects/pulse/data/map/transaction/hover/country/india/state/'
map_state_list = os.listdir(path2)
# map_state_list

df3 = {'State':[], 'Year':[], 'Quarter': [], 'District': [],'Transaction_count': [], 'Transaction_amount':[]}
for i in map_state_list:
    p_i=path2+i+"/"
    map_yr=os.listdir(p_i)
    for j in map_yr:
        p_j=p_i+j+"/"
        map_yr_list=os.listdir(p_j)
        for k in map_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['hoverDataList']:
              Name=z['name']
              count=z['metric'][0]['count']
              amount=z['metric'][0]['amount']
              df3['District'].append(Name)
              df3['Transaction_count'].append(count)
              df3['Transaction_amount'].append(amount)
              df3['State'].append(i)
              df3['Year'].append(j)
              df3['Quarter'].append(int(k.strip('.json')))
Map_transaction = pd.DataFrame(df3)

#map_users
path3 = '/Users/hemap/PycharmProjects/pulse/data/map/user/hover/country/india/state/'
map_state_list2 = os.listdir(path3)
# map_state_list2

df4 = {'State':[], 'Year':[], 'Quarter': [],'District':[], 'reg_users_count':[], 'appOpens': []}
for i in map_state_list2:
    p_i=path3+i+"/"
    map_yr=os.listdir(p_i)
    for j in map_yr:
        p_j=p_i+j+"/"
        map_yr_list=os.listdir(p_j)
        for k in map_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['hoverData'].items():
              Name = z[0]
              reg_users=z[1]['registeredUsers']
              count=z[1]['appOpens']
              df4['District'].append(Name)
              df4['reg_users_count'].append(reg_users)
              df4['appOpens'].append(count)
              df4['State'].append(i)
              df4['Year'].append(j)
              df4['Quarter'].append(int(k.strip('.json')))
Map_users = pd.DataFrame(df4)

#top_transactions
path4 = '/Users/hemap/PycharmProjects/pulse/data/top/transaction/country/india/state/'
top_state_list = os.listdir(path4)
# top_state_list

df5 = {'State':[], 'Year':[], 'Quarter': [],'Pincode':[],'Transaction_count': [], 'Transaction_amount':[]}
for i in top_state_list:
    p_i=path4+i+"/"
    top_yr=os.listdir(p_i)
    for j in top_yr:
        p_j=p_i+j+"/"
        top_yr_list=os.listdir(p_j)
        for k in top_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['pincodes']:
              pincode=z['entityName']
              count=z['metric']['count']
              amount=z['metric']['amount']
              df5['Pincode'].append(pincode)
              df5['Transaction_count'].append(count)
              df5['Transaction_amount'].append(amount)
              df5['State'].append(i)
              df5['Year'].append(j)
              df5['Quarter'].append(int(k.strip('.json')))
Top_transaction = pd.DataFrame(df5)


#top_users
path5 = '/Users/hemap/PycharmProjects/pulse/data/top/user/country/india/state/'
top_state_list2 = os.listdir(path5)
# top_state_list2

df6 = {'State':[], 'Year':[], 'Quarter': [],'Pincode':[],'registeredUser': []}
for i in top_state_list2:
    p_i=path5+i+"/"
    top_yr=os.listdir(p_i)
    for j in top_yr:
        p_j=p_i+j+"/"
        top_yr_list=os.listdir(p_j)
        for k in top_yr_list:
            p_k=p_j+k
            Data=open(p_k,'r')
            D=json.load(Data)
            for z in D['data']['pincodes']:
              Pincode = z['name']
              users = z['registeredUsers']
              df6['Pincode'].append(Pincode)
              df6['registeredUser'].append(users)
              df6['State'].append(i)
              df6['Year'].append(j)
              df6['Quarter'].append(int(k.strip('.json')))
Top_users = pd.DataFrame(df6)


#Connecting to Mysql workbench
mydb = sql.connect(host="127.0.0.1",
                   user="root",
                   password="Mysql@2023",
                   database = 'PULSE',
                   port = "3306"
                  )
cursor = mydb.cursor()

# cursor.execute('CREATE DATABASE PULSE')
# cursor.execute('USE PULSE')
# table1 = '''CREATE TABLE Agg_Trans(
#                         STATE VARCHAR(255),
#                         YEAR int,
#                         Quarter int,
#                         Transaction_type VARCHAR(255),
#                         Transaction_count int,
#                         Transaction_amount DOUBLE
#                         )'''
#
# table2 = '''CREATE TABLE Agg_Users(
#                         STATE VARCHAR(255),
#                         YEAR int,
#                         Quarter int,
#                         Brand VARCHAR(255),
#                         reg_users_count int,
#                         Percentage DOUBLE
#                         )'''
#
# table3 = '''CREATE TABLE Map_Trans(
#                         STATE VARCHAR(255),
#                         YEAR int,
#                         Quarter int,
#                         District VARCHAR(255),
#                         Transaction_count int,
#                         Transaction_amount DOUBLE
#                         )'''
#
# table4 = '''CREATE TABLE Map_Users(
#                         STATE VARCHAR(255),
#                         YEAR int,
#                         Quarter int,
#                         District VARCHAR(255),
#                         reg_users_count int,
#                         AppOpens int
#                         )'''
#
# table5 = '''CREATE TABLE Top_Trans(
#                         STATE VARCHAR(255),
#                         YEAR int,
#                         Quarter int,
#                         District VARCHAR(255),
#                         Transaction_count int,
#                         Transaction_amount DOUBLE
#                         )'''
#
# table6 = '''CREATE TABLE Top_Users(
#                         STATE VARCHAR(255),
#                         YEAR int,
#                         Quarter int,
#                         Pincode int,
#                         reg_users_count int
#                         )'''
#
# tables = [table1,table2,table3,table4,table5,table6]
# for i in tables:
#     cursor.execute(i)
#
# cursor.execute('Show Tables')
# cursor.fetchall()
#
rows = list(Agg_transaction.itertuples(index=False, name=None))
for i in rows:
    query = 'INSERT INTO Agg_Trans VALUES (%s,%s,%s,%s,%s,%s)'
    cursor.execute(query,i)
    mydb.commit()

rows = list(Agg_users.itertuples(index=False, name=None))
for i in rows:
    query = 'INSERT INTO Agg_Users VALUES (%s,%s,%s,%s,%s,%s)'
    cursor.execute(query,i)
    mydb.commit()

rows = list(Map_transaction.itertuples(index=False, name=None))
for i in rows:
    query = 'INSERT INTO Map_Trans VALUES (%s,%s,%s,%s,%s,%s)'
    cursor.execute(query,i)
    mydb.commit()

rows = list(Map_users.itertuples(index=False, name=None))
for i in rows:
    query = 'INSERT INTO Map_Users VALUES (%s,%s,%s,%s,%s,%s)'
    cursor.execute(query,i)
    mydb.commit()

rows = list(Top_transaction.itertuples(index=False, name=None))
for i in rows:
    query = 'INSERT INTO Top_Trans VALUES (%s,%s,%s,%s,%s,%s)'
    cursor.execute(query,i)
    mydb.commit()

rows = list(Top_users.itertuples(index=False, name=None))
for i in rows:
    query = 'INSERT INTO Top_Users VALUES (%s,%s,%s,%s,%s)'
    cursor.execute(query,i)
    mydb.commit()
