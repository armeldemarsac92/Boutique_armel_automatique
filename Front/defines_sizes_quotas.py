import streamlit as st
import plotly.graph_objs as go
import json
import time

data_file = "../Assets/Data/size_quotas.json"

def save_data(data):
    with open(data_file, "w") as file:
        json.dump(data, file)

def load_data():
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


st.write("Pie chart with 6 adjustable values")

# Create initial values for the pie chart
labels = ["Taille XS", "Taille S", "Taille M", "Taille L", "Taille XL", "Taille XXL"]
values = [10, 20, 30, 10, 20, 10]

# Create a pie chart with the initial values
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

# Display the chart
#plotly_chart = st.plotly_chart(fig)

# Get the updated values from the user
new_values = []
for i in range(len(labels)):
    new_value = st.slider(f"Adjust value for {labels[i]}", 0, 100, values[i], step=1)
    new_values.append(new_value)

# Update the pie chart with the new values
fig.update_traces(values=new_values)
plotly_chart = st.plotly_chart(fig)

values_graph = fig.data[0].values

st.write("Selected values:", values_graph)

while True:
    save_data(new_values)
    time.sleep(1)

