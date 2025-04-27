# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from helper_functions import text_to_df

# Initialize the app
app = Dash()
server = app.server

# App layout
app.layout = [

    # title
    html.Div(children='Dash Dollars',style={'color': 'red', 'fontSize': 60, 'textAlign':'center',"font-weight": "bold"}),

    # instructions
    html.H3(children='1. Visit www.doordash.com and Sign in'),
    html.H3(children='2. Click on \'Orders\''),
    html.H3(children='3. Scroll to the Very Bottom'),
    html.H3(children='4. Hit Ctrl+A and Ctrl+C'),
    html.H3(children='5. Paste Copied Text into Textbox'),

    
    dcc.Textarea(
        id='copy_input',
        value='Copy and paste here',
        style={'width': '20%', 'height': 30},
    ),
    
    dcc.Graph(id='bar_plot'),
    dcc.Graph(id='line_plot')

]

# Input Text Response
@callback(
    Output('bar_plot', 'figure'),
    Output('line_plot', 'figure'),
    Input('copy_input', 'value')
)
def update_output(text):
    df = text_to_df(text)
    group_by_resturant_df = df.groupby('Resturant').Price.sum().to_frame().reset_index().sort_values(by='Price',ascending=False)
    bar_plot = px.bar(group_by_resturant_df, x='Resturant', y='Price')
    line_plot = px.line(df, x='Date',y='running_total_price')
    return bar_plot, line_plot

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
