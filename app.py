import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("formatted_sales.csv")

# Prepare data
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

# Create Dash app
app = Dash(__name__)

# Layout with styling
app.layout = html.Div(
    style={
        "backgroundColor": "#f4f6f9",
        "padding": "20px",
        "fontFamily": "Arial"
    },
    children=[

        html.H1(
            "Soul Foods Sales Dashboard",
            style={
                "textAlign": "center",
                "color": "#2c3e50"
            }
        ),

        html.H3(
            "Pink Morsel Sales Analysis",
            style={"textAlign": "center"}
        ),

        html.Div(
            style={"textAlign": "center", "marginBottom": "20px"},
            children=[
                html.Label("Select Region:",
                           style={"fontWeight": "bold"}),

                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True
                )
            ]
        ),

        dcc.Graph(id="sales-chart")
    ]
)

# Callback to update chart
@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):

    # Filter data
    if selected_region != "all":
        filtered_df = df[df['region'].str.lower() == selected_region]
    else:
        filtered_df = df.copy()

    # Aggregate daily sales
    daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()

    # Create line chart
    fig = px.line(
        daily_sales,
        x='date',
        y='sales',
        title="Sales Over Time",
        labels={
            "date": "Date",
            "sales": "Total Sales"
        }
    )

    # Price increase marker
    fig.add_shape(
        type="line",
        x0="2021-01-15",
        x1="2021-01-15",
        y0=0,
        y1=daily_sales['sales'].max() if not daily_sales.empty else 0,
        line=dict(color="red", dash="dash")
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="#f4f6f9"
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
