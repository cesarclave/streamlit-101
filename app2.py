import pandas as pd
import streamlit as st
import plotly.express as px

# Assuming your data is saved as 'bank_transactions.csv'
data = pd.read_csv("data.csv")

# Convert 'Date' column to datetime format (if needed)
if pd.api.types.is_string_dtype(data['Date']):
    data['Date'] = pd.to_datetime(data['Date'])

# Group data by desired time frequency (e.g., daily, weekly, monthly)
time_frequency = st.sidebar.selectbox(
    "Select Time Frequency", ["Daily", "Weekly", "Monthly"]
)
if time_frequency == "Daily":
    grouped_data = data.resample('D', on='Date')
elif time_frequency == "Weekly":
    grouped_data = data.resample('W-SUN', on='Date')  # Group by weeks starting from Sunday
elif time_frequency == "Monthly":
    grouped_data = data.resample('M', on='Date')
else:
    raise ValueError("Invalid time frequency")

# Calculate the desired metric (e.g., sum, average) for the chosen time frequency
metric = st.sidebar.selectbox(
    "Select Metric", ["Sum", "Average"]
)
if metric == "Sum":
    aggregation_func = lambda x: x.sum()
elif metric == "Average":
    aggregation_func = lambda x: x.mean()
else:
    raise ValueError("Invalid metric")

# Group and aggregate data based on user selections
grouped_data = grouped_data['Montant (EUR)'].apply(aggregation_func).reset_index()

# Streamlit app layout
st.title("Time Series Analysis")

# Display a time series graph using plotly express
fig = px.line(
    grouped_data, x='Date', y='metric', title=f"{metric} Spending over Time ({time_frequency})"
)

# Customize chart appearance using Plotly Express options (optional)
# Learn more: https://plotly.com/python/line-charts/
# fig.update_layout(...)

st.plotly_chart(fig)

# Optional: Display some summary statistics
st.subheader("Summary Statistics")
st.write(grouped_data[metric].describe())
