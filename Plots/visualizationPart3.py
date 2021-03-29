# Visualization Lab 3 Part 3
# Individual Submission - Alex Raygoza
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file from Datasets folder
#df1 and df2 are placed temporarely until all group members provide code
# we are only using df3 and df4
df1 = pd.read_csv('../Datasets/CoronavirusTotal.csv')
df2 = pd.read_csv('../Datasets/CoronaTimeSeries.csv')
df3 = pd.read_csv('../Datasets/Olympic2016Rio.csv')
df4 = pd.read_csv('../Datasets/Weather2014-15.csv')

app = dash.Dash()

# 1 Bar chart data -Alex Raygoza

# Removing empty spaces from State column to avoid errors
barchart_df = df3.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
# Sorting values and select first 20
barchart_df = df3.sort_values(by=['Total'], ascending=[False]).head(20)
# Preparing data
data_barchart = [go.Bar(x=barchart_df['NOC'], y=barchart_df['Total'], marker={'color': '#eba309'})]

# 2 Stack bar chart data -Alex Raygoza

# Removing empty spaces from State column to avoid errors
stackbarchart_df = df3.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
# Creating Gold column
stackbarchart_df['Gold'] = stackbarchart_df['Total'] - stackbarchart_df['Silver'] - stackbarchart_df[
    'Bronze']
# Creating sum of medals by Country Column
stackbarchart_df = stackbarchart_df.groupby(['NOC']).agg(
    {'Total': 'sum', 'Bronze': 'sum', 'Silver': 'sum', 'Gold': 'sum'}).reset_index()
# Sorting values and select 20 first value
stackbarchart_df = stackbarchart_df.sort_values(by=['Total'], ascending=[False]).head(20).reset_index()
# Preparing data
trace1_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Gold'], name='Gold Medals',
                              marker={'color': '#FFD700'})
trace2_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Silver'], name='Silver Medals',
                              marker={'color': '#9EA0A1'})
trace3_stackbarchart = go.Bar(x=stackbarchart_df['NOC'], y=stackbarchart_df['Bronze'], name='Bronze Medals',
                              marker={'color': '#CD7F32'})
data_stackbarchart = [trace1_stackbarchart, trace2_stackbarchart, trace3_stackbarchart]

# 3 Line Chart - Hari Dhimal- Completed

line_df = df4
line_df['date'] = pd.to_datetime(line_df['date'])
data_linechart = [go.Scatter(x=df4['date'], y=df4['actual_max_temp'], mode='lines', name='Max Temperature')]

# 4 Multi Line Chart - Kush Bhuva

multiline_df = df4
multiline_df['date'] = pd.to_datetime(multiline_df['date'])
trace1_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_mean_temp'], mode='lines', name='actual_mean_temp')
trace2_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_min_temp'], mode='lines', name='actual_min_temp')
trace3_multiline = go.Scatter(x=multiline_df['date'], y=multiline_df['actual_max_temp'], mode='lines', name='actual_max_temp')
data_multiline = [trace1_multiline, trace2_multiline, trace3_multiline]

# 5 Bubble chart - Hari Dhimal- Completed

bubble_df = df4.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
# preparing data
data_bubblechart = [
    go.Scatter(x=df4['average_min_temp'],
               y=df4['average_max_temp'],
               text=df4['date'],
               mode='markers', marker=dict(size=8, color='red'))]

# Heatmap - Mauricio Barrera

data_heatmap = [go.Heatmap(x=df4['day'],
                           y=df4['month'],
                           z=df4['record_max_temp'].values.tolist(),
                           colorscale='Jet')]

# Layout
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Div('Olympic 2016 Rio Medals', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represent the Medals of Rio Olympic 2016 of 10 first top countries of selected continent.'),
    dcc.Graph(id='graph1'),
    html.Div('Please select a continent', style={'color': '#ef3e18', 'margin':'10px'}),
    dcc.Dropdown(
        id='select-continent',
        options=[
            {'label': 'Asia', 'value': 'Asia'},
            {'label': 'Africa', 'value': 'Africa'},
            {'label': 'Europe', 'value': 'Europe'},
            {'label': 'North America', 'value': 'North America'},
            {'label': 'Oceania', 'value': 'Oceania'},
            {'label': 'South America', 'value': 'South America'}
        ],
        value='North America'
    ),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represents the total medals of Olympic 2016 of 20 first top countries.'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_barchart,
                  'layout': go.Layout(title='Total medals of Olympic 2016 of 20 first top countries',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Medals'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Stack bar chart', style={'color': '#df1e56'}),
    html.Div(
        'This stack bar chart represent Medals of Olympic 2016 of 20 first top countries.'),
    dcc.Graph(id='graph3',
              figure={
                  'data': data_stackbarchart,
                  'layout': go.Layout(title='Medals of Olympic 2016 of 20 first top countries',
                                      xaxis={'title': 'Country'}, yaxis={'title': 'Medals Won'},
                                      barmode='stack')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Line chart', style={'color': '#df1e56'}),
    html.Div('This line chart represent the Maximum Temperature of each day of the month in the given period.'),
    dcc.Graph(id='graph4',
              figure={
                  'data': data_linechart,
                  'layout': go.Layout(title='Maximum Temperature of each day of the month from 2014-07-01 to 2015-06-15',
                                      xaxis={'title': 'Month'}, yaxis={'title': 'Max Temperature'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Multi Line chart', style={'color': '#df1e56'}),
    html.Div(
        'This line chart represent the Min, Mean and Max temperature at a certain day.'),
    dcc.Graph(id='graph5',
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(
                      title='Min, Mean, and Max Temperature',
                      xaxis={'title': 'Date'}, yaxis={'title': 'Temperature'})
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bubble chart', style={'color': '#df1e56'}),
    html.Div(
        'This bubble chart represent the Average Min Temp and Average Max Temp of the given period.'),
    dcc.Graph(id='graph6',
              figure={
                  'data': data_bubblechart,
                  'layout': go.Layout(title='Weather Details',
                                      xaxis={'title': 'Average Minimum Temperature'}, yaxis={'title': 'Average Maximum Temperature'},
                                      hovermode='closest')
              }
              ),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Heat map', style={'color': '#df1e56'}),
    html.Div(
        'Heat Map Represent Max Temperature on Day of Week and Month of Year.'),
    dcc.Graph(id='graph7',
              figure={
                  'data': data_heatmap,
                  'layout': go.Layout(title='Max Temperature On Day of Week',
                                      xaxis={'title': 'Day of Week'}, yaxis={'title': 'Week of Month'}
                                      )
              }
              )
])


@app.callback(Output('graph1', 'figure'),
              [Input('select-continent', 'value')])
def update_figure(selected_continent):
    filtered_df = df3[df3['Continent'] == selected_continent]

    filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    new_df = filtered_df.groupby(['NOC'])['Total'].sum().reset_index()
    new_df = new_df.sort_values(by=['Total'], ascending=[False]).head(10)
    data_interactive_barchart = [go.Bar(x=new_df['NOC'], y=new_df['Total'], marker={'color': '#FFD700'})]
    return {'data': data_interactive_barchart, 'layout': go.Layout(title='Medals of Olympic 2016 '+selected_continent,
                                                                   xaxis={'title': 'Country'},
                                                                   yaxis={'title': 'Number of medals'})}


if __name__ == '__main__':
    app.run_server()
