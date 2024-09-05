import re
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from streamlit_extras.metric_cards import style_metric_cards

import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

st.set_page_config(page_title="Voyage Value", page_icon="✈️", layout="wide", initial_sidebar_state="expanded")
alt.themes.enable("dark")

st.sidebar.title('Voyage Value')
uploaded_file = st.sidebar.file_uploader("Choose a file", type=(["csv","xlsx","xls"]))
if uploaded_file is None:
    st.info("Upload a file")
    st.stop()
# st.download_button('Download', 'Data.csv')
data_category = st.sidebar.selectbox(f"Type of Data", ['Employee Data', 'Travel Data', 'Expense Data'])

df = pd.read_excel(uploaded_file)
# with st.expander("Data Preview"):
#     st.dataframe(df)

# Employee Data
if data_category == 'Employee Data':
    dash_1 = st.container()
    with dash_1:
        st.markdown("<h2 style='text-align: center;'>Employee Data Dashboard</h2>", unsafe_allow_html=True)
        st.write("")

    dash_2 = st.container()
    with dash_2:
        total_employees = len(df['Employee Name'].unique())
        departments = len(df['Department'].unique())
        locations = len(df['Location'].unique())

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Number of Employees", value= total_employees)
        col2.metric(label="Number of Departments", value= departments)
        col3.metric(label="Number of HQ Locations", value= locations)
        style_metric_cards(border_left_color="#0083B8", background_color= "3E14B7")
    
    dash_3 = st.container()
    with dash_3:
        grouped_df = df.groupby(['Department', 'Seniority Level']).size().reset_index(name='Count')
        fig = px.bar(grouped_df, x='Department', y='Count', color='Seniority Level', 
             title='Seniority Level Distribution Across Departments')
        fig.update_layout(barmode='stack', xaxis_title='Department', yaxis_title='Number of Employees', legend_title='Seniority Level')
        st.plotly_chart(fig, use_container_width=True)
        
    dash_4 = st.container()
    with dash_4:
            counts, bins = np.histogram(df['Employee Age'], bins=range(20, 60, 2))
            bins = 0.5 * (bins[:-1] + bins[1:])
            fig = px.bar(x=bins, y=counts, labels={'x':'Employee Age', 'y':'count'}, title='Distribution of Employees by age')
            st.plotly_chart(fig, use_container_width=True)

    dash_5 = st.container()
    with dash_5:
            col1, col2 = st.columns([4,1.5])
            with col1:
                fig = px.histogram(df, x='Employee Status', color='Seniority Level', barmode='group')
                fig.update_layout(title='Seniority Level Distribution by Employee Status',
                                xaxis_title='Employee Status',
                                yaxis_title='Count')
                st.plotly_chart(fig)

            with col2:
                gender_counts = df['Employee Gender'].value_counts().reset_index()
                gender_counts.columns = ['Employee Gender', 'Count']
                fig = px.pie(gender_counts, values='Count', names='Employee Gender', title='Distribution of Employees by gender')
                st.plotly_chart(fig, use_container_width=True)

def extract_distance(distance_str):
    number = re.search(r'(\d+)', distance_str)
    if number:
        return int(number.group(1))
    return 0

# Travel Data
if data_category == 'Travel Data':            
    dash_6 = st.container()
    with dash_6:
        st.markdown("<h2 style='text-align: center;'>Travel Data Dashboard</h2>", unsafe_allow_html=True)
        st.write("")

    dash_7 = st.container()
    with dash_7:
        total_trips = len(df['Trip ID'].unique())
        average_time = int(df['Duration'].mean())
        df['Distance (miles)'] = df['Travel Distance'].apply(extract_distance)
        total_distance = df['Distance (miles)'].sum()

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Number of Trips", value= total_trips)
        col2.metric(label="Average Duration of trips", value= average_time)
        col3.metric(label="Total Distance Travelled", value= f'{total_distance} miles')
        style_metric_cards(border_left_color="#0083B8", background_color= "3E97DB")

    dash_8 = st.container()
    with dash_8:
        col1, col2 = st.columns([3,1.5])
        with col1:
            n_accommodation_type = df['Accommodation type'].value_counts().sort_values(ascending=False)
            fig = px.bar(df, x= n_accommodation_type.index, y= n_accommodation_type.values, title='Distribution of Accommodation')
            fig.update_layout(xaxis_title='Accommodation Type', yaxis_title='Number of Employees', legend_title='Seniority Level')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            locations = df['Location'].value_counts().reset_index()
            locations.columns = ['Location', 'Count']
            fig = px.pie(locations, values='Count', names='Location', title='Top Destinations')
            st.plotly_chart(fig, use_container_width=True)

    dash_9 = st.container()
    with dash_9:
        df['Start date'] = pd.to_datetime(df['Start date'])
        df['End date'] = pd.to_datetime(df['End date'])
        df['Month'] = df['Start date'].dt.strftime('%Y-%m')

        monthly_distance = df.groupby('Month')['Distance (miles)'].sum().reset_index()
        fig = px.area(monthly_distance, x='Month', y='Distance (miles)',
                        title='Monthly Travel Distance',
                        labels={'Month': 'Month', 'Travel Distance': 'Total Travel Distance'})
        st.plotly_chart(fig, use_container_width=True)

    dash_10 = st.container()
    with dash_10:
        col1, col2 = st.columns([1.5,3])
        with col1:
            purpose_counts = df.groupby(['Purpose of Travel', 'Location']).size().reset_index(name='Count')
            fig = px.sunburst(purpose_counts, path=['Purpose of Travel', 'Location'], values='Count',
                            title='Purpose of Travel Distribution by Destination')
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            grouped_data = df.groupby(['Transportation type', 'Travel Class']).size().reset_index(name='count')
            fig = px.bar(grouped_data, x='Transportation type', y='count', color='Travel Class',
                        title='Transportation Type vs Travel Class',
                        labels={'transportation Type': 'Transportation Type', 'count': 'Number of Employees', 'Travel Class': 'Travel Class'},
                        barmode='group')
            st.plotly_chart(fig, use_container_width=True)

# Expense Data
if data_category == 'Expense Data':            
    dash_11 = st.container()
    with dash_11:
        st.markdown("<h2 style='text-align: center;'>Travel Spending</h2>", unsafe_allow_html=True)
        st.write("")
    
    dash_12 = st.container()
    with dash_12:
        total_trips = len(df['Trip ID'].unique())
        trip_expenditure = int(df['Accommodation Cost'].sum() + df['Transportation Cost'].sum() + df['Meal Expenses'].sum())
        avg_expenditure = int(df['Total Travel Expense'].mean())

        col1, col2, col3 = st.columns(3)
        col1.metric(label="Number of Trips", value= total_trips)
        col2.metric(label="Average Cost Per Trip", value= f'$ {avg_expenditure}')
        col3.metric(label="Total Trip Expenditure", value= f'$ {trip_expenditure}')
        style_metric_cards(border_left_color="#0083B8", background_color= "3E97DB")

    dash_13 = st.container()
    with dash_13:
        df['Start date'] = pd.to_datetime(df['Start date'])
        df['Month'] = df['Start date'].dt.strftime('%Y-%m')
        monthly_expenses = df.groupby('Month')[['Accommodation Cost', 'Transportation Cost', 'Meal Expenses']].sum().reset_index()
        melted_expenses = monthly_expenses.melt(id_vars='Month', var_name='Expense Type', value_name='Cost')
        fig = px.line(melted_expenses, x='Month', y='Cost', color='Expense Type',
                    title='Monthly Expenses for Accommodation, Transportation, and Meals',
                    labels={'Month': 'Month', 'Cost': 'Total Cost ($)'})
        st.plotly_chart(fig, use_container_width=True)

    dash_14 = st.container()
    with dash_14:
        col1, col2 = st.columns([3,1.5])
        with col1:
            df['Start date'] = pd.to_datetime(df['Start date'])
            df['Month'] = df['Start date'].dt.strftime('%Y-%m')
            df['Miscellaneous Expenses'] = df['Tips/Gratuities'] + df['Conference Fees'] + df['Visa/Passport Fees'] + df['Business Supplies']
            monthly_expense = df.groupby('Month').agg({
                'Tips/Gratuities': 'sum',
                'Conference Fees': 'sum',
                'Visa/Passport Fees': 'sum',
                'Business Supplies': 'sum',
            }).reset_index()
            melted_expenses = monthly_expense.melt(id_vars='Month', var_name='Expense Type', value_name='Cost')
            fig = px.bar(melted_expenses, x='Month', y='Cost', color='Expense Type',
                        title='Monthly Miscellaneous Expenses',
                        labels={'Month': 'Month', 'Cost': 'Total Cost', 'Expense Type': 'Type of Expense'})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            insurance = df['Travel Insurance'].value_counts().reset_index()
            insurance.columns = ['Travel Insurance', 'Count']
            fig = px.pie(insurance, values='Count', names='Travel Insurance', title='Travel Insurance of Employees')
            st.plotly_chart(fig, use_container_width=True)

    dash_15 = st.container()
    with dash_15:
        col1, col2 = st.columns([3,3])
        with col1:
            expense_columns = ['Transportation Cost', 'Accommodation Cost', 'Meal Expenses', 
                   'Conference Fees', 'Visa/Passport Fees', 'Business Supplies', 
                   'Tips/Gratuities']
            expense_data = df[expense_columns].sum().reset_index()
            expense_data.columns = ['Expense Category', 'Total Amount']
            fig = px.pie(expense_data, names='Expense Category', values='Total Amount', title='Percentage of Total Travel Expenses')
            st.plotly_chart(fig)

        with col2:
            df['Start date'] = pd.to_datetime(df['Start date'])
            df['Month'] = df['Start date'].dt.strftime('%Y-%m')
            monthly_expense = df.groupby('Month')['Total Travel Expense'].sum().reset_index()
            fig = px.area(monthly_expense, x='Month', y='Total Travel Expense', title='Monthly Total Travel Expenses')
            st.plotly_chart(fig, use_container_width=True)

    dash_16 = st.container()
    with dash_16:
        avg_cost_per_department = df.groupby('Department')['Total Travel Expense'].mean().reset_index()
        fig = px.line(avg_cost_per_department, x='Department', y='Total Travel Expense', title='Average Travel Cost per Department')
        st.plotly_chart(fig, use_container_width=True)
    
    dash_17 = st.container()
    with dash_17:
        trip_type_costs = df.groupby('Transportation type')['Total Travel Expense'].sum().reset_index()
        fig = px.bar(trip_type_costs, x='Transportation type', y='Total Travel Expense', 
                    title='Comparison of Total Costs by Transportation type',
                    labels={'Transportation type': 'Transportation type', 'Total Travel Expense': 'Total Cost ($)'})
        st.plotly_chart(fig, use_container_width=True)