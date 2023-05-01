import streamlit as st
import plotly.graph_objs as go
import json

data_file = "../Assets/Data/size_quotas.json"

def save_data(data):
    with open(data_file, "w") as file:
        json.dump([val / 100 for val in data], file)

def load_data():
    try:
        with open(data_file, "r") as file:
            return [val * 100 for val in json.load(file)]
    except FileNotFoundError:
        return []

st.write("Pie chart with 6 adjustable values")

# Load data from file
values = load_data()

labels = ["Taille XS", "Taille S", "Taille M", "Taille L", "Taille XL", "Taille XXL"]

# Set default values if the data file is empty or has a different length than labels
if not values or len(values) != len(labels):
    values = [10, 20, 30, 10, 20, 10]

# Create a pie chart with the initial values
fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

# Display the chart
plotly_chart = st.plotly_chart(fig)

# Get the updated values from the user
new_values = values.copy()
for i in range(len(labels)):
    new_value = st.slider(f"Adjust value for {labels[i]}", 0.0, 100.0, float(values[i]), step=0.01)

    if new_value != new_values[i]:
        diff = new_value - new_values[i]
        new_values[i] = new_value

        for j in range(len(labels)):
            if j != i:
                new_values[j] = max(0, new_values[j] - diff)
                diff = max(0, -diff)
                if diff == 0:
                    break

# Update the pie chart with the new values
fig.update_traces(values=new_values)
plotly_chart = st.plotly_chart(fig)

values_graph = fig.data[0].values

st.write("Selected values:", values_graph)

# Save data
save_data(new_values)
