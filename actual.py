import time
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Real-Time Data SOLARCAR CHIEF",
    page_icon="〽️",
    layout="wide",
)

# dataset_url = 'https://docs.google.com/spreadsheets/d/1dQk1tVT_62rLE5r2mm8PVdHxBfw5sJHELIfxpX9mHdg/edit?usp=sharing'
# csv_export_link = f'{dataset_url.replace("/edit", "")}/export?format=csv'
# you should probably change this 
ex_data = '/Users/himanishkolli/Downloads/DummyData - Sheet1.csv'
@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(ex_data)

df = get_data()

# Rest of your code...


#dashboard title

st.title("Crew Chief Live Data")

#create single element container
placeholder = st.empty()
kphUnits = True
setSpeed = 55

#unit converter
if st.toggle("Units: "):
    kphUnits = not kphUnits
    st.write("miles/mph")
else:
    st.write("kilometers/kph") 

lat = [37.7749, 32.7767, 40.4406, 41.8781, 42.2808]
long = [-122.4194, -96.7970, -79.9959, -87.6298, -83.7430]

routeLat = []
routeLong = []
colors = []
sizes = []

for i in range(len(lat)-1):
    startLat = lat[i]
    endLat = lat[i+1]
    startLong = long[i]
    endLong = long[i+1]
    diffLat = endLat-startLat
    diffLong = endLong-startLong
    j = 0
    while (j != 100):
        startLat += (diffLat)/100
        startLong += (diffLong)/100
        routeLat.append(startLat)
        routeLong.append(startLong)
        colors.append((255, 95, 21))
        sizes.append(10)
        j += 1

for i in range(len(lat)):
    routeLat.append(lat[i])
    routeLong.append(long[i])
    if (i == 0 or i == len(lat)-1):
        colors.append((251, 236, 93))
    else:
        colors.append((0, 0, 128))
    sizes.append(75000)

#dummy values for the car
routeLat.append(0)
routeLong.append(0)
colors.append((0, 255, 255))
sizes.append(50000)

#chat?
prompt = st.chat_input("Enter Message")
if prompt:
    st.write(f"[insert name] has sent the following prompt: {prompt}")

#live feed simulation
for seconds in range(100000):
    
    df["speed_new"] = df["speed"] * np.random.choice(range(5,9))
    df["power_new"] = df["power"] * np.random.choice(range(5,9))
    df["time_new"] = df["time"] + 1
    # creating KPI to display
    avg_speed = (np.mean(df["speed_new"])/np.random.choice(range(5,9))).round(1)
   
    distance_left = np.random.choice(range(10,90))
    fig = px.line(
        data_frame=df, y="power_new", x=df["time_new"]
    )

    #unit conversions 
    if not kphUnits:
        avg_speedU = avg_speed/1.609
        setSpeedU = setSpeed/1.609
        distance_leftU = distance_left/1.609
    else:
        avg_speedU = avg_speed
        setSpeedU = setSpeed
        distance_leftU = distance_left

    #cruise control
    ifCC = np.random.choice(range(0,2))
    if (ifCC == 0):
        CC = "ON"
    else:
        CC = "OFF"
    if (CC=="ON"):
        setSPEED = setSpeedU
    else:
        setSPEED = "N/A"
    
    #nos level
    nosLvlNum =  ifCC = np.random.choice(range(0,3))
    if (nosLvlNum == 0):
        nosLevel = "normal"
    elif (nosLvlNum == 1):
        nosLevel = "super"
    else:
        nosLevel = "ultra"

    with placeholder.container():
        # create three columns
        kpi1, fig_col2, fig_col3 = st.columns([0.5, 2, 1])

        kpi1.metric(
            label = "CURRENT SPEED",
            value = avg_speedU,
        )
        kpi1.metric(
            label = "CRUISE CONTROL",
            value = CC,
        )
        kpi1.metric(
            label = "SET SPEED",
            value = setSPEED,
        )
        kpi1.metric(
            label = "NOS",
            value = nosLevel,
        )

        kpi1.metric(
            label = "DISTANCE TO CHECKPOINT",
            value = distance_leftU,
        )
        # create two columns for charts
        # fig_col1, fig_col2, fig_col3 = st.columns([1,1,1])
        with fig_col2:
            st.markdown("### net power")
            additional_data = {'x': [5, 6, 7],
                'y': [14, 15, 16]}

            # Add additional trace to the existing graph
            fig.add_trace(px.line(additional_data, x='x', y='y').data[0])
            st.write(fig)

        with fig_col3:
            # st.markdown("### Second Chart")
            # fig2 = px.histogram(data_frame=df, x="time")        
            # st.write(fig2)
            if seconds < len(routeLat)-(len(lat)+1):
                lat1 = routeLat[seconds]
                long1 = routeLong[seconds]
            else:
                lat1 = routeLat[len(routeLat)-2]
                long1 = routeLong[len(routeLat)-2]
            
            routeLat[len(routeLat)-1] = lat1
            routeLong[len(routeLat)-1] = long1
            
            df1 = pd.DataFrame({
            "col1": routeLat,
            "col2": routeLong,
            "col3": colors,
            "col4": sizes,
            })

            st.map(df1,
                latitude='col1',
                longitude='col2',
                color= 'col3',
                size= 'col4',
                zoom=2.5)
                 
    time.sleep(1)