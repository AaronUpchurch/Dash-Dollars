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
    html.Div(children='DASH DOLLARS',style={'color': '#fa3910', 'fontSize': 30, 'textAlign':'left',"font-weight": "bold",'font':'Copperplate'}),
    html.Hr(),
    # instructions
    html.H2(children='Steps:',style={'font-weight':'bold'}),
    html.H4(children='1. Visit www.doordash.com and Sign in'),
    html.H4(children='2. Click on \'Orders\' on the Left Sidebar'),
    html.H4(children='3. Scroll to the Very Bottom'),
    html.H4(children='4. Click Ctrl+A and Ctrl+C'),
    html.H4(children='5. Paste Copied Text into Textbox'),

    dcc.Textarea(
        id='copy_input',
        value='',
        style={'width': '20%', 'height': 30},
    ),
    html.Hr(),
    
    # plots
    html.H2(children='Plots:',style={'font-weight':'bold'}),  
    html.Div(children=[
        html.Div(dcc.Graph(id='resturant_bar_plot',style={'width': '80vh', 'height': '40vh','textAlign':'center'}),style={'display': 'inline-block'}),
        html.Div(dcc.Graph(id='day_of_week_bar_plot',style={'width': '80vh', 'height': '40vh','textAlign':'center'}),style={'display': 'inline-block'}),
        html.Div(dcc.Graph(id='most_expensive_purchases_plot',style={'width': '80vh', 'height': '40vh','textAlign':'center'}),style={'display': 'inline-block'}),
        html.Div(dcc.Graph(id='line_plot',style={'width': '80vh', 'height': '40vh','textAlign':'center'}),style={'display': 'inline-block'})
        ]
    )

]

# Input Text Response
@callback(
    Output('resturant_bar_plot', 'figure'),
    Output('day_of_week_bar_plot', 'figure'),
    Output('most_expensive_purchases_plot', 'figure'),
    Output('line_plot', 'figure'),
    
    Input('copy_input', 'value')
)
def update_output(text):
    df = text_to_df(text)
    
    group_by_resturant_df = df.groupby('Resturant').Price.sum().to_frame().reset_index().sort_values(by='Price',ascending=False)
    group_by_day_of_week_df = df.groupby('day_of_week').Price.sum().to_frame().reset_index().sort_values(by='Price',ascending=False)
    most_expensive_purchases_df = df.sort_values(by='Price',ascending=False).head()
    
    resturant_bar_plot = px.bar(group_by_resturant_df, x='Resturant', y='Price',labels = {'Resturant':'Resturant','Price':'Total Expense'},title="Expense by Resturant")
    line_plot = px.line(df, x='Date',y='running_total_price',labels = {'Date':'Date','running_total_price':'Total Expense'},title="Expense Over Time")
    day_of_week_bar_plot = px.bar(group_by_day_of_week_df, x='day_of_week', y='Price',labels = {'day_of_week':'Day of Week','Price':'Total Expense'},title="Expense by Day of Week")
    most_expensive_purchases_plot = px.bar(most_expensive_purchases_df, x='Resturant', y='Price',labels = {'Resturant':'Resturant','Price':'Expense'},title="Five Most Expensive Expenses",barmode='group')

    return resturant_bar_plot, day_of_week_bar_plot, most_expensive_purchases_plot, line_plot

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
    #app.run_server(debug=False)
