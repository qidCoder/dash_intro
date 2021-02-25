import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ---------- Import and clean data (importing csv into pandas)
df = pd.read_csv("intro_bees.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)#lines it up
print(df[:5])

bee_killers = ["Disease", "Other", "Pesticides", "Pests_excl_Varroa", "Unknown", "Varroa_mites"]

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="affected_by",
                 options=[
                     {"label": x, "value": x} for x in bee_killers],
                 multi=False,#prevents selecting multiple choices
                 value="Pesticides",#default value
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(#the callback is what connects the app layout to the graph
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='affected_by', component_property='value')]
)
def update_graph(option_slctd):#must always define a function after callback. Arguments must match number of inputs
    print(option_slctd)
    print(type(option_slctd))

    container = "The bee-killer chosen by the user was: {}".format(option_slctd)

    dff = df.copy()#makes a copy of the data frame to play around with inside the function
    dff = dff[dff["Affected by"] == option_slctd]
    dff = dff[(dff["State"] == "Idaho") | (dff["State"] == "New York") | (dff["State"] == "New Mexico")]

    # Plotly Express
    fig = px.line(
        data_frame = dff, 
        x="Year", 
        y="Pct of Colonies Impacted", 
        color="State",
        template = "plotly_dark"
    )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
