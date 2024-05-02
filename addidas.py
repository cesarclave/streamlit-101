import streamlit as st
import pandas as pd
import datetime
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_excel("Adidas.xlsx")

st.set_page_config(page_title="Superstore!!!", page_icon=":bar_chart:",layout="wide")
