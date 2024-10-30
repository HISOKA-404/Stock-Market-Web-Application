# Description: Stock Market Web Application to display data and charts on some stocks

# Importing required libraries 
import streamlit as st
import pandas as pd
from PIL import Image
import six.moves

# Stock Data 
# Amazon: 1997 - 24/03/2022
# Apple: 01/03/2010 - 28/02/2020
# Google: 04/01/2010 - 30/12/2022
# MSFT: 1986 - 24/03/2022
# Nvidia: 1999 - 28/08/2024
# Common Date Range: 01/03/2010 - 28/02/2020

st.write("""
Stock Market Web Application\n
**Visually** shows data on Stock! Date Range: March 1, 2010 - February 28, 2020         
""")

image = Image.open("D:/Programming/Projects/Stock Market Web Application/stock_market.jpeg")
st.image(image)

# Create a sidebar header
# User select date range and stock name/picker 
st.sidebar.header("User Input")

# Define a function to get date input from user
def get_input():
    start_date = st.sidebar.text_input("Start Date", "2010/03/01") 
    end_date = st.sidebar.text_input("End Date", "2020/02/28") 
    stock_symbol = st.sidebar.text_input("Stock Symbol", "AMZN")
    return start_date, end_date, stock_symbol

# Get company name with help of symbol
def get_company_name(symbol):
    match(symbol):
        case "AMZN":
            return "Amazon.com Inc"
        case "GOOGL":
            return "Alphabet Inc"
        case "MSFT":
            return "Microsoft Corp"
        case "AAPL":
            return "Apple Inc"
        case "NVDA":
            return "Nvidia Corp"
        case _:
            return "No Such Company Found"


# Take input from user to retrieve that particular company data
def get_company_data(symbol, start_date, end_date):
    match(symbol.upper()):
        case "AMZN":
            df = pd.read_csv("D:/Programming/Projects/Stock Market Web Application/Stock_Data/AMZN.csv")
        case "AAPL":
            df = pd.read_csv("D:/Programming/Projects/Stock Market Web Application/Stock_Data/AAPL.csv")  
        case "GOOGL":
            df = pd.read_csv("D:/Programming/Projects/Stock Market Web Application/Stock_Data/GOOGL.csv") 
        case "MSFT":
            df = pd.read_csv("D:/Programming/Projects/Stock Market Web Application/Stock_Data/MSFT.csv")
        case "NVDA":
            df = pd.read_csv("D:/Programming/Projects/Stock Market Web Application/Stock_Data/NVDA.csv")
        case _:
            df = pd.DataFrame(columns=["Date", "Open", "Close", "Volume", "High", "Low"])

    # Get the date range to show stock data during that period
    # Will convert date to datetime format for consistency
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Set the start and end indexes row both to 0
    start_row = 0
    end_row = 0
    
    # Start at the top of data_set Date column and check every row
    # There might be a problem if exact user selected start date is not found
    # So to find out from which row onwards we need to start displaying data  
    # User selected start date is less than or equal to date present in data_set: From this row onwards we will start displaying stock data
    # So we are running this loop in order to check the next date where we can start displaying stock data to user 
    for i in range(len(df)):
        if start_date<=pd.to_datetime(df["Date"][i]):
            start_row = i # We can start displaying stock data from this row
            break
    
    # Now we have to do the same process for end date 
    # Where the user selected end date should be greater than or equal to given date
    for j in range(len(df)):
        if end_date>=pd.to_datetime(df["Date"][len(df) - 1 - j]):
            end_row = len(df) - 1 - j
            break
    
    # Set the index to be date 
    # We want to access the stock data in this date range "using this index 
    df = df.set_index(pd.DatetimeIndex(df["Date"].values))
    
    return df.iloc[start_row:end_row+1, :] # return the data frame within this rows, 2nd parameter ():) describes return all the columns 

# Get the user input 
start_date, end_date, symbol = get_input()

# Get the company data
df = get_company_data(symbol, start_date, end_date)

# Get the company name 
company_name = get_company_name(symbol.upper())

# Display the close price
st.header(company_name+" Close Price\n")
st.line_chart(df['Close'])  

# Display the Volume
st.header(company_name+" Volume\n")
st.line_chart(df['Volume'])

# Get statistics on the data
st.header("Data Statistics")
st.write(df.describe())