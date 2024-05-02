import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Suivi compate bancaire",
                   page_icon=":bar_chart:",
                   layout="wide")

df = pd.read_csv("data.csv")
df['Date'] = pd.to_datetime(df['Date'])
df['Crédit/Débit'].mask( df['Montant (EUR)'] > 0, 'Crédit' , inplace=True )
df['Crédit/Débit'].mask( df['Montant (EUR)'] < 0, 'Débit' , inplace=True )

# 
st.sidebar.header("Choisir un filtre: ")

category = st.sidebar.multiselect(
        "Choisir la Catégorie:" ,
        options=df["Catégorie"].unique(),
        default=df["Catégorie"].unique()
        )

sub_category = st.sidebar.multiselect(
        "Choisir la sous catégorie" ,
        options=df["Sous-Catégorie"].unique(),
        default=df["Sous-Catégorie"].unique()
        )

credit_debit = st.sidebar.multiselect(
        "Crédit/Débit" ,
        options=df["Crédit/Débit"].unique(),
        default=df["Crédit/Débit"].unique()
        )

operation_type = st.sidebar.multiselect(
        "Choisir le type d'opération:" ,
        options=df["Type d'opération"].unique(),
        default=df["Type d'opération"].unique()
        )

# target = st.sidebar.multiselect(
#         "Choisir le Bénéficiare/Débiteur:" ,
#         options=df["Bénéficiaire/Débiteur"].unique(),
#         default=df["Bénéficiaire/Débiteur"].unique()
#         )

# sub_category = st.sidebar.multiselect(
#         "Choisir le Bénéficiare/Débiteur:" ,
#         options=df["Bénéficiaire/Débiteur"].unique(),
#         default=df["Bénéficiaire/Débiteur"].unique()
#         )

df_selection = df.query("Catégorie == @category & \
                        `Sous-Catégorie` == @sub_category & \
                        `Crédit/Débit` == @credit_debit & \
                        `Type d'opération` == @operation_type") #`a b`

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
df_daily_total = df_selection[['Date','Montant (EUR)']].groupby(pd.Grouper(key="Date", freq="D")).sum().reset_index()
fig_daily_total = px.line(df_daily_total, x='Date', y="Montant (EUR)")
st.plotly_chart(fig_daily_total)