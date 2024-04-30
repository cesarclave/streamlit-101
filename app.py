import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Suivi compate bancaire",
                   page_icon=":bar_chart:",
                   layout="wide")

df = pd.read_csv("data.csv")
df['Date'] = pd.to_datetime(df['Date']).dt.date

# ----- SIDEBAR -----

st.sidebar.header("Choisir un filtre: ")

category = st.sidebar.multiselect(
        "Choisir la Catégorie:" ,
        options=df["Catégorie"].unique(),
        default=df["Catégorie"].unique()
        )

# operation_type = st.sidebar.multiselect(
#         "Choisir le type d'opération:" ,
#         options=df["Type d'opération"].unique(),
#         default=df["Type d'opération"].unique()
#         )

# target = st.sidebar.multiselect(
#         "Choisir le Bénéficiare/Débiteur:" ,
#         options=df["Bénéficiaire/Débiteur"].unique(),
#         default=df["Bénéficiaire/Débiteur"].unique()
#         )

df_selection = df.query("Catégorie == @category")

st.dataframe(df_selection)

# ----- MAINPAGE -----
st.title(":bar_chart: Sale Dashboard")
st.markdown("##")


# TOP KPI's
total_revenue = int(df_selection[df_selection["Montant (EUR)"]>0]["Montant (EUR)"].sum())
total_expense = int(df_selection[df_selection["Montant (EUR)"]<0]["Montant (EUR)"].sum())

left_column, middle_column = st.columns(2)

with left_column:
    st.subheader("Total revenue: ")
    st.subheader(f"EUR € {total_revenue:,}")

with left_column:
    st.subheader("Total expenses: ")
    st.subheader(f"EUR € {total_expense:,}")

# ------ Sales by category ------
sales_by_product_line = (
    df_selection.groupby(by=["Catégorie"])[["Montant (EUR)"]].sum().sort_values(by="Montant (EUR)")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Montant (EUR)",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by product line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white"
)

st.plotly_chart(fig_product_sales)

# ------ Date ------
# daily_spend = df.groupby(pd.Grouper(freq='D')).sum()

# fig_daily_spend = px.line(daily_spend, y='Montant (EUR)', title='Total Daily Spend')
# st.plotly_chart(fig)


# fig_daily_spend = px.line(pd.DataFrame(daily_spend).reset_index(), x='Date', y='Montant (EUR)', title='Total Daily Spend')
# st.plotly_chart(fig_daily_spend)
# daily_spend = df_selection.resample('D', on='Date')['Montant (EUR)'].sum()
# fig_daily_spend = px.line(pd.DataFrame(daily_spend).reset_index(), x='Date', y='Montant (EUR)', title='Total Daily Spend')

# st.plotly_chart(fig_daily_spend)