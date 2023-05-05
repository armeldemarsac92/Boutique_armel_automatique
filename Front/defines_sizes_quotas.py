def app3():
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

    st.title("Proportion de tailles")

    st.write("Pie chart with 6 adjustable values")

    # Load data from file
    values = load_data()

    labels = ["Taille XS", "Taille S", "Taille M", "Taille L", "Taille XL", "Taille XXL"]

    # Set default values if the data file is empty or has a different length than labels
    if not values or len(values) != len(labels):
        values = [10, 20, 30, 10, 20, 10]

    colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3']

    # Create a pie chart with the initial values
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent', sort=False, marker=dict(colors=colors))])

    # Display the chart
    plotly_chart = st.plotly_chart(fig)

    # Get the updated values from the user
    new_values = values.copy()
    for i in range(len(labels)):
        new_value = st.slider(f"Adjust value for {labels[i]}", 0.0, 100.0, float(values[i]), step=0.01)

        if new_value != new_values[i]:
            new_values[i] = new_value

    # Update the pie chart with the new values
    fig.update_traces(values=new_values)
    plotly_chart = st.plotly_chart(fig)

    values_graph = fig.data[0].values

    st.write("Selected values:", values_graph)

    # Save data
    save_data(new_values)
