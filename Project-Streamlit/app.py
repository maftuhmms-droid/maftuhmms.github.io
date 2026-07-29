import streamlit as st
import datetime
import pandas as pd
import plotly.express as px

#initialize connection
conn = st.connection("postgresql", type="sql")
# Perform query.
df = conn.query('SELECT * FROM mytable;', ttl="10m")

today = datetime.datetime.now()
formatted_date = today.strftime("%Y-%m-%d-%H:%M")

#================================================

# if "list_income" not in st.session_state:
#     st.session_state.list_income = []

# if "list_expend" not in st.session_state:
#     st.session_state.list_expend = []

# if "list_loan" not in st.session_state:
#     st.session_state.list_loan = []

if "transactions" not in st.session_state:
    st.session_state.transactions = []



def input_nominal():
    global nominal
    nominal = st.sidebar.number_input(
        "Nominal",
        min_value = 0,
        max_value = 100000000,
        step = 500,
        )
    return nominal
    

st.title("(FD) - FROM THIS")
st.sidebar.markdown("<h3>Input This !", unsafe_allow_html=True)
# Print results.
for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")

type_of = st.sidebar.radio(
    "Select the menu",
    ["Income", "Expend", "Loan"]
)

def date():
    global selected_date
    selected_date = st.sidebar.date_input(
    "Choose a date",
    value = today
    #datetime.date(2027, 7, 2)
    )

#===================================================

if type_of == "Income":
    whats = st.sidebar.radio("Type",
        ["Sallary","Other"]
    )
    desc_income = ""
    if whats == "Sallary":
        input_nominal()
        month_sallary = st.sidebar.select_slider("Select Month", ["Jan","Feb","Mar","Apr","Mei","Jun","Jul","Aug","Sep","Okt","Nov","Des"])
        month_number = {
            "Jan":1,
            "Feb":2,
            "Mar":3,
            "Apr":4,
            "Mei":5,
            "Jun":6,
            "Jul":7,
            "Aug":8,
            "Sep":9,
            "Okt":10,
            "Nov":11,
            "Des":12
        }

        selected_date = datetime.date(
            2026,
            month_number[month_sallary],
            1
        )
        desc = "Monthly"
    elif whats == "Other":
        input_nominal()
        date()
        desc = st.sidebar.text_input("Description")


elif type_of == "Expend":
    whats = st.sidebar.radio(
        "Type",
        ["Premiere","Secondary"]
    )
    input_nominal()
    date()
    desc = st.sidebar.text_input("Description")

elif type_of == "Loan":
    whats = st.sidebar.radio(
            "Type",
            ["Sp","Gp","Other"]
        )
    input_nominal()
    date()
    desc = st.sidebar.text_input("Description")
    
    
else:
    st.write("Error Else type")

if st.sidebar.button("Add"):
    st.session_state.transactions.append(
        {
            "menu": type_of,
            "type": whats,
            "nominal": nominal,
            "date": selected_date,
            "desc": desc
        }
    )
    st.sidebar.success(
            f"Success add at {formatted_date}"
        )



# st.subheader("Expend")
# st.dataframe(pd.DataFrame(st.session_state.list_expend))

# st.subheader("Loan")
# st.dataframe(pd.DataFrame(st.session_state.list_loan))



df = pd.DataFrame(st.session_state.transactions)
if not df.empty and "menu" in df.columns:
    income = df[df["menu"]=="Income"]["nominal"].sum()
    expend = df[df["menu"]=="Expend"]["nominal"].sum()
    loan = df[df["menu"]=="Loan"]["nominal"].sum()
   
else:
    income = 0
    expend = 0
    loan = 0

if not df.empty and "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])
    df["Year"] = df["date"].dt.year
    df["Month"] = df["date"].dt.strftime("%b")
    df["MonthNumber"] = df["date"].dt.month

#======================================================
# df = pd.DataFrame({
#     "Month": [],
#     "Income": [],
#     "Expend": [],
#     "Lack": []
#     }
# )

# st.bar_chart(
#     df,
#     x="Month",
#     y=["Income", "Expend", "Lack"],
#     color=["#1AFF00", "#E5FF00", "#FF0000"],
# )

if not df.empty and "Year" in df.columns:
    for year in sorted(df["Year"].unique()):

        st.subheader(f"{year}")

        chart = (
            df[df["Year"]==year]
            .groupby(
                ["MonthNumber","Month","menu"]
            )["nominal"]
            .sum()
            .unstack(fill_value=0)
            .reset_index()
            .sort_values("MonthNumber")
        )

        chart = chart.drop(columns="MonthNumber")

        fig = px.bar(
            chart,
            x="Month",
            y=[
                col for col in chart.columns 
                if col != "Month"
            ],
            barmode="group",
            color_discrete_map={
                "Income": "#1AFF00",
                "Expend": "#E5FF00",
                "Loan": "#FF0000"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:
    st.info("Not yet transaction")

st.subheader("Data")
st.dataframe(pd.DataFrame(st.session_state.transactions))

