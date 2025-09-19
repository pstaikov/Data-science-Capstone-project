# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
print(spacex_df.head())
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
print("Payload range: ", min_payload, max_payload)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                    style={'textAlign': 'center', 'color': '#503D36',
                                        'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', 
                                    options=[{'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                    ],
                                    value='ALL',
                                    placeholder="Select Launch Site",
                                    searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0', 2000: '2000', 4000: '4000', 
                                        6000: '6000', 8000: '8000', 10000: '10000'},
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        all_sites_data = spacex_df.groupby("Launch Site", )[['class']].sum()
        fig = px.pie(all_sites_data, values='class', 
        names=all_sites_data.index, 
        title='Total Success Launches by Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        success_data = site_df['class'].value_counts()
        fig = px.pie(success_data, values=success_data.values,
        names = success_data.index,
        title=f"Total Success Launches for the Site {entered_site}"
        )
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), 
    Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(site, slider_values):
    print(site, slider_values)
    df = spacex_df
    title_end = 'All Sites'
    if site != 'ALL':
        df = spacex_df[spacex_df['Launch Site'] == site]
        title_end = site
    df = df[(df['Payload Mass (kg)'] >= slider_values[0]) & (df['Payload Mass (kg)'] <= slider_values[1])]
    fig = px.scatter(df, x='Payload Mass (kg)', 
        y='class', color='Booster Version Category',
        title=f"Correlation between payload mass and success for {title_end}")
    return fig


# Run the app
if __name__ == '__main__':
    app.run()
