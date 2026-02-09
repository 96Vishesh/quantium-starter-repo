import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# Load processed data
df = pd.read_csv("formatted_sales.csv")

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Sort by date
df = df.sort_values(by='date')

# Aggregate total sales per day
daily_sales = df.groupby('date')['sales'].sum().reset_index()

# Create line chart
fig = px.line(
    daily_sales,
    x='date',
    y='sales',
    title="Pink Morsel Sales Over Time",
    labels={
        "date": "Date",
        "sales": "Total Sales"
    }
)

# Add vertical line safely (no annotation)
fig.add_shape(
    type="line",
    x0="2021-01-15",
    x1="2021-01-15",
    y0=0,
    y1=daily_sales['sales'].max(),
    line=dict(color="red", dash="dash")
)

# Dash App
app = Dash(__name__)

app.layout = html.Div([
    html.H1(
        "Soul Foods Sales Dashboard",
        style={'textAlign': 'center'}
    ),

    html.H3(
        "Pink Morsel Sales Before vs After Price Increase (Jan 15, 2021)",
        style={'textAlign': 'center'}
    ),

    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
