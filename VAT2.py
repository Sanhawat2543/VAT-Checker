import os
import math
import numpy as np
import pandas as pd
from PIL import Image
import streamlit as st
from decimal import Decimal

def save_data(dataframe):
    dataframe.to_csv("data.csv", index=False)

def load_data():
    if os.path.exists("data.csv"):
        return pd.read_csv("data.csv")
    else:
        return pd.DataFrame(columns=['Name','ID', 'Principal', 'VAT','VAT (%)'])

def calculate_vat_percentage(total_amount, value_added_tax):
    vat_percent = value_added_tax / total_amount * Decimal('100')
    return vat_percent

def download_csv(dataframe):
    dataframe.to_csv("data.csv", index=False, encoding='utf-8-sig')
    with open("data.csv", 'rb') as f:
        csv = f.read()
    st.sidebar.download_button(
       "Press to Download",
       csv,
       "VATChecked.csv",
       "text/csv",
       key='download-csv'
    )

def main():
    st.set_page_config(page_title="VAT Checker", page_icon=":guardsman:", layout="wide")
    st.title("Value Added Tax Checker")
    st.markdown("This application allows you tod check the 7% value-added tax (VAT) of companies that you have entered.")

    dataframe = load_data()

    name = st.text_input("Enter a name:")
    no = st.text_input("Enter ID code:")
    total_amount = st.number_input("Enter total amount:",  step=0.01)
    value_added_tax = st.number_input("Enter value added tax:",  step=0.01)

    total_amount = Decimal(str(total_amount))
    value_added_tax = Decimal(str(value_added_tax))
    
    if  value_added_tax :
        vat_percent = calculate_vat_percentage(total_amount, value_added_tax)
        st.write(f'VAT is {vat_percent} %')
        data = {'Name': name, 'ID': str(no), 'Principal': total_amount, 'VAT': value_added_tax,'VAT (%)': vat_percent}

    if st.button("Submit"):
       if value_added_tax:
           if vat_percent == 7.00:
               dataframe = dataframe.append(data, ignore_index=True)
               save_data(dataframe)
               st.success("Submit Successful")
           else:
                st.warning("VAT is not 7.00%, please input another data.")
       else:
           st.error("VAT is not entered, please input the data first.")

    st.sidebar.title("Actions")

    if st.sidebar.button("Clear data"):
        if os.path.exists("data.csv"):
            os.remove("data.csv")
            st.success("Data cleared successfully.")
            dataframe = load_data()
        else:
            st.error("No data to clear.")

    if st.sidebar.button("Delete the last row"):
        if not dataframe.empty:
            dataframe = dataframe[:-1]
            save_data(dataframe)
            st.success("Row deleted successfully")
        else :
            st.error("No row to remove.")

    st.markdown("This is your inputted data.")
    st.write(dataframe.style.format(subset=['Principal', 'VAT','VAT (%)'], formatter="{:.2f}"))


    if os.path.exists("data.csv"):
        download_csv(dataframe)

    #st.sidebar.title("My Profile")
    #deaw = Image.open('deaw.jpg')
    #st.sidebar.image(deaw)



if __name__ == "__main__":
    main()