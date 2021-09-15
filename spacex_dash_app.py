# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Other dataframes needed
df_site = spacex_df[['Launch Site','class']]
pie_data = df_site.groupby(['Launch Site', 'class']).agg({'class': ['count']}).reset_index()
pie_data.columns = ['Launch Site', 'Success', 'Total']
df_scatter = spacex_df[['Launch Site', 'Payload Mass (kg)', 'class', 'Booster Version Category']]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},                                    
                                        {'label': 'CCAFS LC-40', 'value': 'LC40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'SLC40'},
                                        {'label': 'KSC LC-39A', 'value': 'LC39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'SLC4E'},
                                    ],
                                    value='ALL',
                                    placeholder='Select a Lauch Site here',
                                    searchable=True
                                ),
                                html.Div(id='dd-output-container'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload Range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[min_payload, max_payload],
                                    marks={
                                        0: '0',
                                        2500: '2500',
                                        5000: '5000',
                                        7500: '7500',
                                        10000: '10000'
                                    },
                                ),
                                html.Div(id='output-container-range-slider'),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                Input(component_id='site-dropdown', component_property='value'))

# Add computation to callback function and return graph
def get_graph(site_selected):
    # Select Launch Site
    if site_selected == 'ALL':
        df_pie = pie_data[pie_data['Success']==1]
        g_title = 'All Sites Success Rate'
        g_names = 'Launch Site'
    elif site_selected == 'LC40':
        df_pie = pie_data[pie_data['Launch Site']=='CCAFS LC-40']
        g_title = 'CCAFS LC-40 Success Rate' 
        g_names = 'Success'   
    elif site_selected == 'SLC40':
        df_pie = pie_data[pie_data['Launch Site']=='CCAFS SLC-40']
        g_title = 'CCAFS SLC-40 Success Rate' 
        g_names = 'Success'        
    elif site_selected == 'LC39A':
        df_pie = pie_data[pie_data['Launch Site']=='KSC LC-39A']
        g_title = 'KSC LC-39A Success Rate'  
        g_names = 'Success'       
    elif site_selected == 'SLC4E':
        df_pie = pie_data[pie_data['Launch Site']=='VAFB SLC-4E'] 
        g_title = 'VAFB SLC-4E Success Rate' 
        g_names = 'Success'       
    

    fig = px.pie(df_pie, values='Total', names=g_names, title=g_title)    
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])

# Add computation to callback function and return graph
def update_scat_chart(site_selected, payload_range):
    # Select Launch Site
    if site_selected == 'ALL':
        df_scat = df_scatter
        g_title = 'Correlation between Payload Mass and Success for All Sites'
    elif site_selected == 'LC40':
        df_scat = df_scatter[df_scatter['Launch Site']=='CCAFS LC-40']
        g_title = 'Correlation between Payload Mass and Success for CCAFS LC-40'
    elif site_selected == 'SLC40':
        df_scat = df_scatter[df_scatter['Launch Site']=='CCAFS SLC-40']
        g_title = 'Correlation between Payload Mass and Success for CCAFS SLC-40' 
    elif site_selected == 'LC39A':
        df_scat = df_scatter[df_scatter['Launch Site']=='KSC LC-39A']
        g_title = 'Correlation between Payload Mass and Success for KSC LC-39A'  
    elif site_selected == 'SLC4E':
        df_scat = df_scatter[df_scatter['Launch Site']=='VAFB SLC-4E'] 
        g_title = 'Correlation between Payload Mass and Success for VAFB SLC-4E' 
    
    # Select Payload Range
    low, high = payload_range
    mask = (df_scat['Payload Mass (kg)'] > low) & (df_scat['Payload Mass (kg)'] < high)
    
    fig = px.scatter(df_scat[mask], x='Payload Mass (kg)', y='class', color='Booster Version Category', title=g_title)
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
