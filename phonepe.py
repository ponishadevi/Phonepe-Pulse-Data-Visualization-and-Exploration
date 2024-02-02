import json
import streamlit as st
import pandas as pd
import requests
import pymysql
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors
from streamlit_option_menu import option_menu



pysql_connect=pymysql.connect(host='127.0.0.1',user='root',password='new_password',database="phonepe_pulse")
cur=pysql_connect.cursor()

#Aggregated_insurance
cur.execute("select * from aggregated_insurance")
pysql_connect.commit()
table1 = cur.fetchall()
Aggre_insurance = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

#Aggregated_transaction
cur.execute("select * from aggregated_transaction")
pysql_connect.commit()
table1 = cur.fetchall()
Aggre_transaction = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))


#Aggregated_user
cur.execute("select * from aggregated_user")
pysql_connect.commit()
table2 = cur.fetchall()
Aggre_user = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

#Map_insurance
cur.execute("select * from map_insurance")
pysql_connect.commit()
table4 = cur.fetchall()
Map_insurance = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

#Map_transaction
cur.execute("select * from map_transaction")
pysql_connect.commit()
table3 = cur.fetchall()
Map_transaction = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))


#Map_user
cur.execute("select * from map_user")
pysql_connect.commit()
table4 = cur.fetchall()
Map_user = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUsers", "AppOpens"))

#Top_insurance
cur.execute("select * from top_insurance")
pysql_connect.commit()
table7 = cur.fetchall()
Top_insurance = pd.DataFrame(table7,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))


#Top_transaction
cur.execute("select * from top_transaction")
pysql_connect.commit()
table5 = cur.fetchall()
Top_transaction = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))


#Top_user
cur.execute("select * from top_user")
pysql_connect.commit()
table6 = cur.fetchall()
Top_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUsers"))



def Aggre_insurance_Y(df, year):
    aiy = df[df["Years"] == year]
    aiy.reset_index(drop=True, inplace=True)

    aiyg = aiy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyg.reset_index(inplace=True)

    col1,col2= st.columns((2, 1))  # Adjust the width of col1
    with col1:
        fig_y_amount = px.line(aiyg, x="States", y="Transaction_amount", 
                       title=f"{year} TRANSACTION AMOUNT Trend",
                       labels={"Transaction_amount": "Transaction Amount"},
                       line_shape="linear",
                       color_discrete_sequence=plotly.colors.sequential.Viridis)
        st.plotly_chart(fig_y_amount)
    
        fig_count = px.bar(aiyg, x="States", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                           width=600, height=650, color="States", 
                           color_discrete_sequence=plotly.colors.qualitative.Plotly)
        st.plotly_chart(fig_count)



def Aggre_insurance_Y_Q(df, quarter):
    aiyq = df[df["Quarter"] == quarter]
    aiyq.reset_index(drop=True, inplace=True)

    aiyqg = aiyq.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyqg.reset_index(inplace=True)

    col1,col2 = st.columns((2, 1))  # Adjust the width of col1
    with col1:
        fig_q_amount = px.line(aiyqg, x="States", y="Transaction_amount", 
                       title=f"{quarter} QUARTER TRANSACTION AMOUNT Trend",
                       labels={"Transaction_amount": "Transaction Amount"},
                       line_shape="linear",
                       color_discrete_sequence=plotly.colors.qualitative.Vivid)
        st.plotly_chart(fig_q_amount)
    
        fig_q_count = px.bar(aiyqg, x="States", y="Transaction_count", 
                            title=f"{quarter} QUARTER TRANSACTION COUNT",
                            width=600, height=650, color="States", 
                            color_discrete_sequence=["green"] * len(aiyqg["States"].unique()))
        st.plotly_chart(fig_q_count)



    
def Aggre_Transaction_type(df):
    # Fetch GeoJSON data
    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(geojson_url)

    if response.status_code == 200:
        geojson_data = response.json()
    else:
        st.error(f"Failed to fetch GeoJSON data. Status code: {response.status_code}")
        st.stop()

    # Streamlit App
    st.title("Transaction Data Visualization with Choropleth Map")

    # Dropdown for selecting State
    selected_state = st.selectbox("Select State", df["States"].unique())

    # Dropdown for selecting Transaction metric
    selected_metric = st.selectbox("Select Transaction Metric", ["Transaction_count", "Transaction_amount"])

    # Create Geographical Plot (Choropleth Map)
    fig_india_1 = px.choropleth_mapbox(df, geojson=geojson_data, locations="States", featureidkey="properties.ST_NM",
                                       color=selected_metric, color_continuous_scale="Viridis",
                                       hover_name="States", title=f"{selected_state} {selected_metric.capitalize()}",
                                       mapbox_style="carto-positron",
                                       center={"lat": 20.5937, "lon": 78.9629},
                                       zoom=4)

    # Set color for the selected state
    selected_data = df[df["States"] == selected_state]
    selected_color = 'red' if not selected_data.empty else 'blue'

    # Highlight the selected state
    selected_color = 'red' if not selected_data.empty else 'blue'

    fig_india_1.update_traces(marker=dict(line=dict(color=['red' if geo == selected_state else 'blue' for geo in fig_india_1['data'][0]['locations']])))

    # Display the choropleth map
    st.plotly_chart(fig_india_1, use_container_width=True)

    # Event handler for map selection
    st.write(f"You selected: {selected_state} - {selected_metric.capitalize()}")

    # Display bar chart for the selected state
    fig_bar_chart = px.bar(selected_data, x="Transaction_type", y=selected_metric,
                           title=f"{selected_metric.capitalize()} Breakdown for {selected_state}",
                           color="Transaction_type", color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig_bar_chart)

# Call the function for transaction visualizations



def Aggre_user_plot_1(df,year):
    aguy= df[df["Years"] == year]
    aguy.reset_index(drop= True, inplace= True)
    
    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_line_1 = px.bar(aguyg, x="Brands", y="Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline_r
)
    st.plotly_chart(fig_line_1)

    return aguy

def Aggre_user_plot_2(df,quarter):
    auqs= df[df["Quarter"] == quarter]
    auqs.reset_index(drop= True, inplace= True)
    

    fig_pie_1 = px.pie(data_frame=auqs, names="Brands", values="Transaction_count", hover_data="Percentage",
                      width=1000, title=f"{quarter} QUARTER TRANSACTION COUNT PERCENTAGE", hole=0.5,
                      color_discrete_sequence=px.colors.sequential.Plotly3)
    st.plotly_chart(fig_pie_1)

    return auqs

def Aggre_user_plot_3(df,state):
    aguqy= df[df["States"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Brands")["Transaction_count"].sum())
    aguqyg.reset_index(inplace= True)

    fig_scatter_1= px.line(aguqyg, x= "Brands", y= "Transaction_count", markers= True,width=1000)
    st.plotly_chart(fig_scatter_1)
    return aguqy

   


def map_insure_plot_1(df, year):
    miys = df[df["Years"] == year]
    miysg = miys.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    miysg.reset_index(inplace=True)

    col1,col2 = st.columns(2)

    with col1:
        fig_map_bar_amount = px.bar(miysg, x="Districts", y="Transaction_amount",
                                    width=600, height=500, title=f"{str(year).upper()} DISTRICTS TRANSACTION AMOUNT",
                                    color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_amount)

    
        fig_map_bar_count = px.bar(miysg, x="Districts", y="Transaction_count",
                                   width=600, height=500, title=f"{str(year).upper()} DISTRICTS TRANSACTION COUNT",
                                   color_discrete_sequence=px.colors.sequential.Magma)

        st.plotly_chart(fig_map_bar_count)

# Call the function


def map_insure_plot_2(df, state):
    miys = df[df["States"] == state]
    miysg = miys.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    miysg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_map_pie_amount = px.pie(miysg, names="Districts", values="Transaction_amount",
                                     width=600, height=500, title=f"{state.upper()} DISTRICTS TRANSACTION AMOUNT",
                                     hole=0.5, color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_amount)

    
        fig_map_pie_count = px.pie(miysg, names="Districts", values="Transaction_count",
                                    width=600, height=500, title=f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                                    hole=0.5, color_discrete_sequence=px.colors.sequential.Oranges_r)

        st.plotly_chart(fig_map_pie_count)

# Call the second function


def map_trans_plot_1(df,state):
    mtys = df[df["States"] == state]
    mtysg = mtys.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    mtysg.reset_index(inplace=True)


    geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(geojson_url)

    if response.status_code == 200:
        geojson_data = response.json()
    else:
        st.error(f"Failed to fetch GeoJSON data. Status code: {response.status_code}")
        st.stop()
     # Dropdown for selecting State
    selected_state = st.selectbox("Select State", df["States"].unique())
    # Dropdown for selecting Transaction metric
    selected_metric = st.selectbox("Select Transaction Metric", ["Transaction_count", "Transaction_amount"])

    # Create Geographical Plot (Choropleth Map)
    fig_india_1 = px.choropleth_mapbox(df, geojson=geojson_data, locations="States", featureidkey="properties.ST_NM",
                                        color=selected_metric, color_continuous_scale="Viridis",
                                        hover_name="States", title=f"{selected_state} {selected_metric.capitalize()}",
                                        mapbox_style="carto-positron",
                                        center={"lat": 20.5937, "lon": 78.9629},
                                        zoom=4)

    # Display the choropleth map
    st.plotly_chart(fig_india_1, use_container_width=True)
    st.write(f"You selected: {selected_state} - {selected_metric.capitalize()}")
    # Streamlit columns for better organization
    col1, col2 = st.columns(2)
    with col1:
        # Creating Bar Chart for Transaction Amount:
        fig_map_amount = px.bar(mtys, x="Districts", y="Transaction_amount",
                                width=600, height=500, title=f"{selected_state.upper()} DISTRICTS TRANSACTION AMOUNT",
                                color_discrete_sequence=px.colors.sequential.Plasma)

        # Display the bar chart in the first column
        col1.plotly_chart(fig_map_amount)
    with col2:
            # Creating Bar Chart for Transaction Count:
        fig_map_count = px.bar(mtys, x="Districts", y="Transaction_count",
                                width=600, height=500, title=f"{selected_state.upper()} DISTRICTS TRANSACTION COUNT",
                                color_discrete_sequence=px.colors.sequential.Viridis)

        # Display the bar chart in the second column
        col2.plotly_chart(fig_map_count)


# Call the function




# Function to plot bar charts for registered users and app opens
def map_user_plot_1(df, year):
    muyg = df[df["Years"] == year]
    muyg.reset_index(drop=True, inplace=True)
    muygg = pd.DataFrame(muyg.groupby("States")[["RegisteredUsers", "AppOpens"]].sum())
    muygg.reset_index(inplace=True)

    # Create bar chart
    fig_bar_chart = px.bar(muygg, x="States", y=["RegisteredUsers", "AppOpens"],
                           width=1000, height=800, title=f"{year} REGISTERED USER AND APPOPENS",
                           color_discrete_sequence=px.colors.sequential.Magma)

    # Display the bar chart
    st.plotly_chart(fig_bar_chart)

# Call the function for Map_user


# Function to plot pie chart for registered users and app opens
def map_user_plot_2(df, quarter):
    muyq = df[df["Quarter"] == quarter]
    muyq.reset_index(drop=True, inplace=True)
    muyqg = muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace=True)

    # Create pie chart
    pie_data = pd.DataFrame({
        "States": muyqg["States"],
        "Values": muyqg[["RegisteredUsers", "AppOpens"]].sum(axis=1)  # Sum of RegisteredUsers and AppOpens
    })

    fig_pie = px.pie(pie_data, names="States", values="Values",
                     width=800, height=600, title=f"{quarter} REGISTERED USER AND APPOPENS",
                     color_discrete_sequence=px.colors.sequential.Viridis_r)

    # Display the pie chart
    st.plotly_chart(fig_pie)

# Call the function for Map_user


# Function to plot bar charts for registered users and app opens in a specific state
def map_user_plot_3(df, state):
    muyqs = df[df["States"] == state]
    muyqs.reset_index(drop=True, inplace=True)
    muyqsg = muyqs.groupby("Districts")[["RegisteredUsers", "AppOpens"]].sum()
    muyqsg.reset_index(inplace=True)

    # Create horizontal bar charts
    col1, col2 = st.columns(2)
    with col1:
        fig_registered_users = px.bar(muyqsg, x="RegisteredUsers", y="Districts", orientation="h",
                                      title=f"{state.upper()} REGISTERED USERS", height=800,
                                      color_discrete_sequence=px.colors.qualitative.Vivid)
        st.plotly_chart(fig_registered_users, use_container_width=True)

    with col2:
        fig_app_opens = px.bar(muyqsg, x="AppOpens", y="Districts", orientation="h",
                               title=f"{state.upper()} APPOPENS", height=800,
                               color_discrete_sequence=px.colors.sequential.Magma)
        st.plotly_chart(fig_app_opens, use_container_width=True)

# Call the function for Map_user


# Add more functions for other visualizations if needed


##TOP USER
def top_user_plot_1(df,year):
    tuy= df[df["Years"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUsers", barmode= "group", color= "Quarter",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plot_1)

    return tuy

def top_user_plot_2(df,state):
    tuys= df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)

    tuysg= pd.DataFrame(tuys.groupby("States")["RegisteredUsers"].sum())
    tuysg.reset_index(inplace= True)

    fig_top_plot_1 = px.bar(tuys, x="Quarter", y="RegisteredUsers", barmode="group",
                        width=1000, height=800, color="Pincodes", hover_data="Pincodes",
                        color_continuous_scale=px.colors.sequential.YlOrBr)


    st.plotly_chart(fig_top_plot_1)



# Assuming you have a DataFrame named 'Top_user' with columns 'States', 'Quarter', 'Pincodes', 'RegisteredUsers'

def top_user_plot_3(df, quarter):
    tuyq = df[df["Quarter"] == quarter]
    tuyq.reset_index(drop=True, inplace=True)
    tuysg = pd.DataFrame(tuyq.groupby(["States","Pincodes"])["RegisteredUsers"].sum())
    tuysg.reset_index(inplace=True)

    fig_bar_chart = px.bar(tuysg, x="States", y="RegisteredUsers",
                           color="Pincodes", width=1000, height=800,
                           title=f"{quarter} REGISTERED USERS ACROSS STATES",
                           color_discrete_sequence=px.colors.qualitative.Set1
                           )

    # Display the bar chart using st.plotly_chart
    st.plotly_chart(fig_bar_chart)

# Call the function with your DataFrame and the desired quarter


##-------------------------------------------------------------------------------------------------------------------------------------------------------###



def ques1():
 
    Trans_type = Aggre_transaction[["Transaction_type", "Transaction_count"]]
    Trans_t1 = Trans_type.groupby("Transaction_type")["Transaction_count"].sum().sort_values(ascending=False)
    Trans_t2 = pd.DataFrame(Trans_t1).reset_index()

    fig_transaction_type = px.pie(Trans_t2, values="Transaction_count", names="Transaction_type", color_discrete_sequence=px.colors.sequential.dense_r,
                                title="Top Transaction Types by Transaction Count")

    # Assuming st is Streamlit's module for displaying the chart
    return st.plotly_chart(fig_transaction_type)



def ques2():
    Alt= Aggre_transaction[["States", "Transaction_amount"]]
    At1= Alt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    At2= pd.DataFrame(At1).reset_index().head(10)

    fig_aggr_amt= px.bar(At2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_aggr_amt)


def ques3():
    Alt= Aggre_transaction[["States", "Transaction_amount"]]
    At1= Alt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    At2= pd.DataFrame(At1).reset_index().head(10)

    fig_aggr_amt1=px.bar(At2, x= "States", y= "Transaction_amount",title= " STATES WITH HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence= px.colors.sequential.Turbo)
    return st.plotly_chart(fig_aggr_amt1)


def ques4():
    brand = Aggre_user[["Brands", "Transaction_count"]]
    brand1 = brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2 = pd.DataFrame(brand1).reset_index()

    # Calculate percentage
    brand2["Percentage"] = (brand2["Transaction_count"] / brand2["Transaction_count"].sum()) * 100

    fig_brands = px.pie(brand2, values="Transaction_count", names="Brands", hover_data=["Percentage"],
                        color_discrete_sequence=px.colors.sequential.dense_r,
                        title="Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)


def ques5():
    MDT= Map_transaction[["Districts", "Transaction_amount"]]
    MDT1= MDT.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending= False)
    MDT2= pd.DataFrame(MDT1).reset_index().head(10)
    fig_Mhta= px.pie(MDT2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                        color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_Mhta)



def ques6():
    Mltd= Map_transaction[["Districts", "Transaction_amount"]]
    Mltd1= Mltd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    Mltd2= pd.DataFrame(Mltd1).head(10).reset_index()

    fig_pie_Mltd=px.pie(Mltd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    
    return st.plotly_chart(fig_pie_Mltd)


def ques7():    
    Mda = Map_user[["States", "AppOpens"]]
    Mda1 = Mda.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    Mda2 = pd.DataFrame(Mda1).reset_index().head(10)

    fig_pie_Mhsa=px.pie(Mda2, values="AppOpens", names="States", title="Top 10 States by App Opens",
        color_discrete_sequence=px.colors.qualitative.Dark2)
    return st.plotly_chart(fig_pie_Mhsa)


def ques8():
    Mda = Map_user[["Districts", "AppOpens"]]
    Mda1 = Mda.groupby("Districts")["AppOpens"].sum().sort_values(ascending=False)
    Mda2 = pd.DataFrame(Mda1).reset_index().head(10)
    
    fig_Mhda = px.pie(Mda2, values="AppOpens", names="Districts", title="Top 10 Districts by App Opens",
                      color_discrete_sequence=px.colors.sequential.Emrld_r)

    return st.plotly_chart(fig_Mhda)


def ques9():
    stc = Aggre_transaction[["States", "Transaction_count"]]
    stc1 = stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2 = pd.DataFrame(stc1).reset_index()

    fig_stc=px.bar(stc2, x="States", y="Transaction_count", title="States with Highest Transaction Count",
                        color="Transaction_count", color_continuous_scale=px.colors.sequential.Plasma)
    return st.plotly_chart(fig_stc)


def ques10():
    stc = Aggre_transaction[["States", "Transaction_count"]]
    stc1 = stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2 = pd.DataFrame(stc1).reset_index()

    fig_stc1= px.bar(stc2, x="States", y="Transaction_count", title="States with Lowest Transaction Count",
                        color_discrete_sequence='green')
    return st.plotly_chart(fig_stc1)

##-----------------------------------------------------------------------------------------------------------------------------------------------##
##STREAMLIT PART


# Set page configuration
st.set_page_config(layout="wide")


st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

st.write("Explore PhonePe's data visualizations and charts. Select options from the sidebar to navigate through different sections.")




# Custom CSS for styling main menu options
menu_styles = """
    .custom-select {
        background-color: #f4f4f4;
        padding: 10px;
        margin: 5px;
        border-radius: 5px;
        cursor: pointer;
    }
    .custom-select:hover {
        background-color: #ddd;
    }
"""

# Apply the custom CSS
st.markdown(f'<style>{menu_styles}</style>', unsafe_allow_html=True)

with st.sidebar:
    # Use st.selectbox to create main menu with custom styling
    select = st.selectbox("Main Menu", ["Home", "Data Exploration", "Top Charts"], format_func=lambda x: f'{x}', key="custom_selectbox")
     
    # Apply different styles based on the selected option
if select == "Home":
    st.sidebar.markdown('<span style="color: #3498db; font-size: 20px;">Home</span>', unsafe_allow_html=True)
    st.sidebar.markdown("Discover the world of PhonePe – your go-to digital payment and financial companion. Enjoy lightning-fast transactions, unbeatable security with PIN authorization, and a range of exciting features:")
    
    st.sidebar.write("✨ **Exclusive Offers:** Get access to special discounts, cashback, and rewards.")
    st.sidebar.write("🔐 **Secure Transactions:** Your security is our priority. PIN authorization ensures a safe experience.")
    st.sidebar.write("🔄 **Latest Features:** Explore the newest updates and enhancements for an even better experience.")
    
    st.sidebar.markdown("Ready to experience the future of digital payments? [Download the PhonePe app](https://www.phonepe.com/app-download/) now!")

    # Rest of the content in the main section remains unchanged
    col1, col2 = st.columns(2)
    # ... (existing content)


elif select == "Data Exploration":
    st.sidebar.markdown('<span style="color: #e74c3c; font-size: 20px;">Exploring PhonePe Pulse Data</span>', unsafe_allow_html=True)
    st.sidebar.markdown("Explore and analyze data from the PhonePe Pulse GitHub repository. Extract, transform, and visualize the data to gain valuable insights.")

    

    # Add your content specific to data exploration here


elif select == "Top Charts":

    # Customize the style for the Top Charts option in the sidebar
    st.sidebar.markdown('<span style="color: #2ecc71; font-size: 20px;">Top Charts</span>', unsafe_allow_html=True)
    st.sidebar.markdown("Explore the top charts and trends in PhonePe transactions.")
    
    # Add your additional content here if needed

# Check the selected option and apply different styles accordingly
if select == "Home":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.image("https://download.logo.wine/logo/PhonePe/PhonePe-Logo.wine.png", width=200) 
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        download_button = f'<a href="https://www.phonepe.com/app-download/" download><button>Download the App Now</button></a>'
        st.markdown(download_button, unsafe_allow_html=True)
    with col2:
        st.video("C:\\Users\\hp\\Downloads\\zen class 1\\project\\phonepe ad.mp4")    

    

    col3,col4= st.columns(2)

    with col3:
        st.video("c:\\Users\\hp\\Downloads\\zen class 1\\project\\graphic motion phonepe.mp4")

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")
    with col6:
        st.video("c:\\Users\\hp\\Downloads\\zen class 1\\project\\graphic motion phonepe_2.mp4")      
        
elif select == "Data Exploration":
    st.header("DATA EXPLORATION SECTION")
    # Add your content for Data Exploration section

    tab1, tab2, tab3= st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method = st.radio("**Select the Analysis Method(Aggregated)**",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("**Select the Year**", Aggre_insurance["Years"].min(), Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())

            Aggre_insurance_Y(Aggre_insurance,years)

            col1,col2= st.columns(2)
            with col1:
                
                quarters = st.slider("**Select the Quarter**", Aggre_insurance["Quarter"].min(), Aggre_insurance["Quarter"].max(), Aggre_insurance["Quarter"].min())

            Aggre_insurance_Y_Q(Aggre_insurance, quarters)



        elif method == "Transaction Analysis":
            #Select the State for Analyse the Transaction type
        
            Aggre_Transaction_type(Aggre_transaction) 
            col1,col2= st.columns(2)
            with col1:
                years_at= st.slider("**Select the Year**", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())

            df_agg_tran_Y= Aggre_insurance_Y(Aggre_transaction,years_at)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_at= st.slider("**Select the Quarter**", Aggre_transaction["Quarter"].min(), Aggre_transaction["Quarter"].max(),Aggre_transaction["Quarter"].min())

            df_agg_tran_Y_Q= Aggre_insurance_Y_Q(Aggre_transaction, quarters_at)
            
               
        elif method == "User Analysis":
            year_au= st.selectbox("Select the Year_AU",Aggre_user["Years"].unique())
            agg_user_Y= Aggre_user_plot_1(Aggre_user,year_au)

            quarter_au= st.selectbox("Select the Quarter_AU",agg_user_Y["Quarter"].unique())
            agg_user_Y_Q= Aggre_user_plot_2(agg_user_Y,quarter_au)

            state_au= st.selectbox("**Select the State_AU**",agg_user_Y["States"].unique())
            Aggre_user_plot_3(agg_user_Y_Q,state_au)

##---------------------------------------------------------------------------------------------------------------------------------------------##
    with tab2:
        method_map = st.radio("**Select the Analysis Method(MAP)**",["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])
        if method_map == "Map Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_m1= st.slider("**Select the Year_mi**", Map_insurance["Years"].min(), Map_insurance["Years"].max(),Map_insurance["Years"].min())

            map_insure_plot_1(Map_insurance, years_m1)

            col1,col2= st.columns(2)
            with col1:
                state_m1= st.selectbox("Select the State_mi", Map_insurance["States"].unique())

            map_insure_plot_2(Map_insurance,state_m1)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m1= st.slider("**Select the Quarter_mi**", Map_insurance["Quarter"].min(), Map_insurance["Quarter"].max(),Map_insurance["Quarter"].min())

            df_map_insur_Y_Q= Aggre_insurance_Y_Q(Map_insurance, quarters_m1)

        elif method_map == "Map Transaction Analysis":

            col1,col2= st.columns(2)
            with col1:
                years_m2= st.slider("**Select the Year_mi**", Map_transaction["Years"].min(), Map_transaction["Years"].max(),Map_transaction["Years"].min())

            df_map_tran_Y= Aggre_insurance_Y(Map_transaction, years_m2)

            col1,col2= st.columns(2)
            with col1:
                selected_state = st.selectbox("state", Map_transaction["States"].unique())

            map_trans_plot_1(Map_transaction,selected_state)
            col1,col2= st.columns(2)
            with col1:
                quarters_m2= st.slider("**Select the Quarter_mi**", Map_transaction["Quarter"].min(), Map_transaction["Quarter"].max(),Map_transaction["Quarter"].min())

            Aggre_insurance_Y_Q(Map_transaction, quarters_m2)
            
        

        elif method_map == "Map User Analysis":
            col1,col2= st.columns(2)
            with col1:
                year_mu1= st.selectbox("**Select the Year_mu**",Map_user["Years"].unique())
            map_user_Y= map_user_plot_1(Map_user, year_mu1)

            col1,col2= st.columns(2)
            with col1:
                quarter_mu1= st.selectbox("**Select the Quarter_mu**",Map_user["Quarter"].unique())
            map_user_plot_2(Map_user,quarter_mu1)

            col1,col2= st.columns(2)
            with col1:
                state_mu1= st.selectbox("**Select the State_mu**",Map_user["States"].unique())
            map_user_plot_3(Map_user,state_mu1)


##--------------------------------------------------------------------------------------------------------------------------------------------------------------------###
    with tab3:
        method_top = st.radio("**Select the Analysis Method(TOP)**",["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])

        if method_top == "Top Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t1= st.slider("**Select the Year_ti**", Top_insurance["Years"].min(), Top_insurance["Years"].max(),Top_insurance["Years"].min())
 
            df_top_insur_Y= Aggre_insurance_Y(Top_insurance,years_t1)

            
            col1,col2= st.columns(2)
            with col1:
                quarters_t1= st.slider("**Select the Quarter_ti**", Top_insurance["Quarter"].min(), Top_insurance["Quarter"].max(),Top_insurance["Quarter"].min())

            df_top_insur_Y_Q= Aggre_insurance_Y_Q(Top_insurance, quarters_t1)


        elif method_top == "Top Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t2= st.slider("**Select the Year_tt**", Top_transaction["Years"].min(), Top_transaction["Years"].max(),Top_transaction["Years"].min())
 
            df_top_tran_Y= Aggre_insurance_Y(Top_transaction,years_t2)

            col1,col2= st.columns(2)
            with col1:
                selected_state = st.selectbox("state", Map_transaction["States"].unique())

            map_trans_plot_1(Map_transaction,selected_state)

        elif method_top == "Top User Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t3= st.selectbox("**Select the Year_tu**", Top_user["Years"].unique())

            df_top_user_Y= top_user_plot_1(Top_user,years_t3)

            col1,col2= st.columns(2)
            with col1:
                state_t3= st.selectbox("**Select the State_tu**", Top_user["States"].unique())

            df_top_user_Y_S= top_user_plot_2(Top_user,state_t3)    
            
            col1,col2= st.columns(2)
            with col1:
                quarters_t1= st.slider("**Select the Quarter_ti**", Top_user["Quarter"].min(), Top_user["Quarter"].max(),Top_user["Quarter"].min())

            df_top_insur_Y_Q= top_user_plot_3(Top_user, quarters_t1)
##------------------------------------------------------------------------------------------------------------------------------------------------------------------------------##


elif select == "Top Charts":
    st.header("TOP CHARTS SECTION")

    # Add your content for Top Charts section


    ques= st.selectbox("**Select the Question**",("TOP TRANSACTION TYPES BY TRANSACTION COUNT","STATES WITH LOWEST TRANSACTION AMOUNT",
                                  "STATES WITH HIGHEST TRANSACTION AMOUNT","TOP MOBILE BRANDS OF TRANSACTION COUNT","TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                                  "TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT","TOP 10 STATES BY APP OPENS","TOP 10 DISTRICTS BY APP OPENS",
                                 "STATES WITH HIGHEST TRANSACTION COUNT","STATES WITH LOWEST TRANSACTION COUNT"
                                 ))
    
    if ques=="TOP TRANSACTION TYPES BY TRANSACTION COUNT":
        ques1()

    elif ques=="STATES WITH LOWEST TRANSACTION AMOUNT":
        ques2()

    elif ques=="STATES WITH HIGHEST TRANSACTION AMOUNT":
        ques3()

    elif ques=="TOP MOBILE BRANDS OF TRANSACTION COUNT":
        ques4()

    elif ques=="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT":
        ques5()

    elif ques=="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT":
        ques6()

    elif ques=="TOP 10 STATES BY APP OPENS":
        ques7()

    elif ques=="TOP 10 DISTRICTS BY APP OPENS":
        ques8()

    elif ques=="STATES WITH HIGHEST TRANSACTION COUNT":
        ques9()

    elif ques=="STATES WITH LOWEST TRANSACTION COUNT":
        ques10()

