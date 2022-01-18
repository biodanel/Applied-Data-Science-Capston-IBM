# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
from jupyter_dash import JupyterDash
from dash import no_update

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create a dash application
app = JupyterDash(__name__)
JupyterDash.infer_jupyter_proxy_config()

# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
                                dcc.Dropdown(id='site-dropdown', options= [{'label': 'All Sites', 'value': 'ALL'}, 
                                                                           {'label':'CCAFS LC-40', 'value':'CCAFS LC-40'}, 
                                                                           {'label':'VAFB SLC-4E', 'value':'VAFB SLC-4E'},
                                                                           {'label':'KSC LC-39A', 'value':'KSC LC-39A'},
                                                                           {'label':'CCAFS SLC-40', 'value':'CCAFS SLC-40'}], value='ALL',
                                                                           placeholder='select a Launch Site here', searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                                          
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'}, value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output('success-pie-chart','figure'),Input('site-dropdown','value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', names='Launch Site', title='Total Success Launches by Site')
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', title='Total Success Launches for Site ' + entered_site)
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output('success-payload-scatter-chart', 'figure'), [Input('site-dropdown', 'value'), Input('payload-slider', 'value')])

def get_scatter(entered_site, payload_range):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        min_, max_ = payload_range
        range_ = (filtered_df['Payload Mass (kg)'] > min_) & (filtered_df['Payload Mass (kg)'] < max_)
        fig = px.scatter(filtered_df[range_], x="Payload Mass (kg)", y="class", color="Booster Version Category",
                         title = 'Correlation Between Payload and Success for All Sites')
    else:
        min_, max_ = payload_range
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        range_ = (filtered_df['Payload Mass (kg)'] > min_) & (filtered_df['Payload Mass (kg)'] < max_)
        fig = px.scatter(filtered_df[range_], x="Payload Mass (kg)", y="class", color="Booster Version Category",
                         title = 'Correlation Between Payload and Success for Site ' + entered_site)
    return fig
        
# Run the app
if __name__ == '__main__':
    app.run_server(mode="inline", host="localhost", debug=False, dev_tools_ui=False, dev_tools_props_check=False, port = 8050)
