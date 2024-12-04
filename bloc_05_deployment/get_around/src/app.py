import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

@st.cache_data
def load_data():
    return (
        pd.read_csv(Path("bloc_05_deployment/get_around/src/get_around_pricing_project.csv").resolve()),
        pd.read_excel(Path("bloc_05_deployment/get_around/src/get_around_delay_analysis.xlsx").resolve())
    )

pricing_data, delay_data = load_data()

# Data Cleaning
delay_cleaned = delay_data[(delay_data['state'] == 'ended') & delay_data['delay_at_checkout_in_minutes'].notnull()]
pricing_cleaned = pricing_data[(pricing_data['mileage'] > 0) & (pricing_data['rental_price_per_day'] > 0)]

# Streamlit App
st.title('GetAround Product Management Dashboard')

# Section 1: Revenue Impact
st.header('Impact on Owner Revenue by Minimum Delay Threshold')
thresholds = [60, 120, 180]
revenue_impact = []
for threshold in thresholds:
    affected = delay_cleaned[
        (delay_cleaned['time_delta_with_previous_rental_in_minutes'] < threshold) &
        (delay_cleaned['time_delta_with_previous_rental_in_minutes'] > 0)
    ]
    affected_rentals_ids = affected['rental_id']
    affected_revenue = pricing_cleaned[pricing_cleaned['Unnamed: 0'].isin(affected_rentals_ids)]['rental_price_per_day'].sum()
    total_revenue = pricing_cleaned['rental_price_per_day'].sum()
    revenue_loss_percentage = (affected_revenue / total_revenue) * 100
    revenue_impact.append({'threshold': threshold, 'revenue_loss_percentage': revenue_loss_percentage})

revenue_impact_df = pd.DataFrame(revenue_impact)
fig_revenue_impact = px.bar(
    revenue_impact_df,
    x='threshold',
    y='revenue_loss_percentage',
    title='Impact on Owner Revenue by Minimum Delay Threshold',
    labels={
        'threshold': 'Minimum Delay Threshold (Minutes)',
        'revenue_loss_percentage': 'Revenue Loss (%)'
    },
    color_discrete_sequence=['#AB63FA']
)
st.plotly_chart(fig_revenue_impact)

# Section 2: Number of Rentals Affected
st.header('Number of Rentals Affected by Minimum Delay Threshold')
affected_rentals = []
for threshold in thresholds:
    affected = delay_cleaned[
        (delay_cleaned['time_delta_with_previous_rental_in_minutes'] < threshold) &
        (delay_cleaned['time_delta_with_previous_rental_in_minutes'] > 0)
    ]
    affected_counts = affected['checkin_type'].value_counts().reset_index()
    affected_counts.columns = ['checkin_type', 'count']
    affected_counts['threshold'] = threshold
    affected_rentals.append(affected_counts)

affected_rentals_df = pd.concat(affected_rentals, ignore_index=True)
fig_affected_rentals = px.bar(
    affected_rentals_df,
    x='threshold',
    y='count',
    color='checkin_type',
    barmode='group',
    title='Number of Rentals Affected by Minimum Delay Threshold and Check-In Type',
    labels={
        'threshold': 'Minimum Delay Threshold (Minutes)',
        'count': 'Number of Rentals Affected',
        'checkin_type': 'Check-In Type'
    },
    color_discrete_sequence=px.colors.qualitative.Set1
)
st.plotly_chart(fig_affected_rentals)

# Section 3: Frequency of Late Check-Ins
st.header('Frequency of Late Check-Ins by Check-In Type')
delayed_impact = delay_cleaned[delay_cleaned['time_delta_with_previous_rental_in_minutes'] < 0]
late_checkin_frequency = delayed_impact['checkin_type'].value_counts().reset_index()
late_checkin_frequency.columns = ['checkin_type', 'count']
fig_late_checkin = px.bar(
    late_checkin_frequency,
    x='checkin_type',
    y='count',
    title='Frequency of Late Check-Ins by Check-In Type',
    labels={
        'checkin_type': 'Check-In Type',
        'count': 'Number of Late Check-Ins'
    },
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig_late_checkin)

# Section 4: Rental Delays Distribution
st.header('Number of Rentals Delayed Beyond Specific Thresholds')
delay_thresholds = [30, 60, 120]
delay_counts = []
for threshold in delay_thresholds:
    count = delay_cleaned[delay_cleaned['delay_at_checkout_in_minutes'] > threshold].shape[0]
    delay_counts.append({'threshold': threshold, 'count': count})

delay_counts_df = pd.DataFrame(delay_counts)
fig_delay_thresholds = px.bar(
    delay_counts_df,
    x='threshold',
    y='count',
    title='Number of Rentals Delayed Beyond Thresholds',
    labels={
        'threshold': 'Delay Threshold (Minutes)',
        'count': 'Number of Rentals'
    },
    color_discrete_sequence=['#FFA15A']
)
st.plotly_chart(fig_delay_thresholds)
