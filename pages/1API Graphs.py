import streamlit as st
import requests
import pandas as pd

st.header("API Graphs")
st.subheader("Illustrating the SpaceX API information graphically")
st.divider()

##########
# Graph
st.subheader("Graph of all SpaceX Lanches (successful and failed launches)")
st.write("Note: Graph will only display the range of years that have had launches. Use toggle switches and controls to change graph display.")



# Reading SpaceX API
api = requests.get("https://api.spacexdata.com/v3/launches")
data = api.json()

launchDict = {}
## Dict format: {"launch_year": [success count, fail count]}
for launch in data:
    launch_year, success = str(launch["launch_year"]), launch["launch_success"]
    if launch_year in launchDict:
        if success:
            launchDict[launch_year][0] += 1
        else:
            launchDict[launch_year][1] += 1
    else:
        if success:
            launchDict[launch_year] = [1,0]
        else:
            launchDict[launch_year] = [0,1]

## making sure all years are accounted for (ones with no launches)
launchyearList = list(launchDict.keys())
launchyearList.sort()
tempgraphDict = {}
for year in range(int(launchyearList[0]), int(launchyearList[-1])+1):
    if str(year) in launchDict:
        tempgraphDict[year] = launchDict[str(year)]
    else:
        tempgraphDict[year] = [0,0]



##########
# Creating line graph

## User edits

# Select date range
minYear, maxYear = int(launchyearList[0]), int(launchyearList[-1])
yearRange = st.slider("Range of years (inclusive):", minYear, maxYear, (minYear, maxYear))
st.write("Years:", yearRange)
(startYear, endYear) = yearRange
graphDict = {}
for key in tempgraphDict:
    if int(key) <= endYear and int(key) >= startYear:
        graphDict[key] = tempgraphDict[key]

st.write(graphDict)

# Toggle display total launches
displayTotal = st.checkbox("Display total launches")
if displayTotal:
    for year in graphDict:
        graphDict[year].append(graphDict[year][0]+graphDict[year][1])
    launchPoints = 3
else:
    launchPoints = 2

## Creating list for axis values of graph
yList = []
for launches in graphDict.values():
    yList += launches


xList = []
idList = []
for year in graphDict.keys():
    xList += [year] * launchPoints
    if displayTotal:
        idList += ["successful launches"] + ["failed launches"] + ["total launches"]
    else:
        idList += ["successful launches"] + ["failed launches"]

spaceXdf = pd.DataFrame(
    {
        "Year": xList,
        "Launch Count": yList,
        "Legend": idList
    })
st.line_chart(spaceXdf, x="Year", y="Launch Count", color="Legend")


#########

