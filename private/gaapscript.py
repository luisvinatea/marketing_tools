"""
GAAP Assigner

This script sets up a Streamlit application that allows users to upload a CSV file,
categorize transactions, and generate a balance sheet. The categorized values are stored 
and updated dynamically, and the final balance sheet can be downloaded as an Excel file.

Instructions:
1. Save this script as `gaap_assigner.py`.
2. Run the script using the command: `streamlit run gaap_assigner.py`.

Dependencies:
- pandas
- streamlit
- openpyxl

Ensure you have the required dependencies installed. You can install them using:
`pip install pandas streamlit openpyxl`

Code:
"""

import pandas as pd
import streamlit as st

# Function to split the 'Descrição' column
def split_descricao(descricao):
    parts = descricao.split(' - ')
    if len(parts) >= 4:
        transaction = parts[0]
        remittant = parts[1]
        bank = parts[3]
        return pd.Series([transaction, remittant, bank])
    else:
        return pd.Series([None, None, None])

# Function to retrieve total income and expenses for a given remittant
def get_totals(df, name):
    total_income = df[(df['Remittant'] == name) & (df['Type'] == 'Income')]['Amount'].sum()
    total_expenses = df[(df['Remittant'] == name) & (df['Type'] == 'Expense')]['Amount'].sum()
    return total_income, total_expenses

# Function to update the balance sheet based on user assignments
def update_balance_sheet(balance_sheet, category, income, expense):
    net_result = income - expense
    if category in balance_sheet:
        balance_sheet[category] += net_result
    else:
        balance_sheet[category] = net_result
    return balance_sheet

# Initialize the Streamlit app
st.title('GAAP Assigner')

# Initialize session state for the balance sheet
if 'balance_sheet' not in st.session_state:
    st.session_state['balance_sheet'] = {}

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file is not None:
    df_flow = pd.read_csv(uploaded_file)
    
    # Rename columns
    df_flow.rename(columns={'Valor': 'Amount', 'Data': 'Date'}, inplace=True)
    
    # Display the columns and head of the dataframe for debugging
    st.write("DataFrame Columns:", df_flow.columns.tolist())
    st.write("DataFrame Head:", df_flow.head())
    
    df_flow_copy = df_flow.copy()

    # Apply the function to the 'Descrição' column and create new columns
    df_flow_copy[['Transaction', 'Remittant', 'Bank']] = df_flow_copy['Descrição'].apply(split_descricao)

    # Drop the original 'Descrição' and 'Identificador' columns
    if 'Descrição' in df_flow_copy.columns and 'Identificador' in df_flow_copy.columns:
        df_flow_copy.drop(columns=['Descrição', 'Identificador'], inplace=True)
    
    # Check if the 'Amount' column exists
    if 'Amount' in df_flow_copy.columns:
        # Create the 'Type' column
        df_flow_copy['Type'] = df_flow_copy['Amount'].apply(lambda x: 'Income' if x > 0 else 'Expense')
    else:
        st.error("The 'Amount' column is not found in the uploaded CSV file.")

    # Convert 'Date' column to datetime if it exists
    if 'Date' in df_flow_copy.columns:
        df_flow_copy['Date'] = pd.to_datetime(df_flow_copy['Date'], dayfirst=True)
        df_flow_copy['Month'] = df_flow_copy['Date'].dt.month
        df_flow_copy['Year'] = df_flow_copy['Date'].dt.year

        # Select the time frame
        year = st.selectbox('Select Year', sorted(df_flow_copy['Year'].unique()))
        month = st.selectbox('Select Month', sorted(df_flow_copy[df_flow_copy['Year'] == year]['Month'].unique()))

        # Filter the dataframe based on the selected time frame
        df_filtered = df_flow_copy[(df_flow_copy['Year'] == year) & (df_flow_copy['Month'] == month)]

        # List all unique remittants in the filtered dataframe
        unique_remittants = df_filtered['Remittant'].unique()
        st.write(f"Unique remittants in {year}-{month}: {len(unique_remittants)}")

        # Display the unique remittants
        st.write(unique_remittants)

        # Allow user to select remittant and assign to a category
        selected_remittant = st.selectbox('Select a remittant to categorize', unique_remittants)
        categories = ['Cash and Banks', 'Accounts Receivable', 'Inventory of Consumable Material', 
                      'Buildings (net accumulated depreciation)', 'Vehicles and Machinery (net accumulated depreciation)', 
                      'Financial Investments', 'Current Bank Credit', 'Interest Payable', 
                      'Accounts Payable', 'Salaries Payable', 'Taxes Payable', 'Customer Advances', 
                      'Non-current Bank Credit']
        category = st.selectbox('Select the category for the selected remittant', categories)

        # Calculate totals for the selected remittant
        total_income, total_expenses = get_totals(df_filtered, selected_remittant)
        st.write(f"Total Income: {total_income}")
        st.write(f"Total Expenses: {total_expenses}")

        # Update session state balance sheet
        st.session_state['balance_sheet'] = update_balance_sheet(st.session_state['balance_sheet'], category, total_income, total_expenses)

        # Display balance sheet
        st.write(st.session_state['balance_sheet'])

        # Download the balance sheet as an Excel file
        if st.button('Download Balance Sheet'):
            balance_df = pd.DataFrame(list(st.session_state['balance_sheet'].items()), columns=['Category', 'Amount'])
            balance_df.to_excel('Balance_Sheet.xlsx', index=False)
            st.write("Balance sheet downloaded as 'Balance_Sheet.xlsx'")
