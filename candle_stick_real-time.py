import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import requests

app = dash.Dash(__name__)

def drop_down(dd_id, dd_list_options, dd_init_value):
    return dcc.Dropdown(
                id=dd_id,
                options=dd_list_options,
                value=dd_init_value
            )

app.layout = html.Div(children=[
    html.H1("Real Time Candle Stick", 
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 30}),

    html.Div([
        html.Div([
            html.Label("Coin:"),
            drop_down('dropdown-coin', 
                        [{"label": "BTC / USD", "value": "btcusd"},
                        {"label": "ETH / USD", "value": "ethusd"},
                        {"label": "XRP / EUR", "value": "xrpeur"},
                        ],
                        'btcusd')
        ], style={'font-size': 20, 'margin-right': '20px', 'width': '200px'}),


        html.Div([
            html.Label("Timeframe:"),
            drop_down('dropdown-time',
                        [{"label": "30m", "value": "1800"},
                        {"label": "1h", "value": "3600"},
                        {"label": "1d", "value": "8640"},
                        ],
                        '3600')
        ], style={'font-size': 20, 'margin-right': '20px', 'width': '200px'}),


        html.Div([
            html.Label("Num of Candlesticks:"),
            drop_down('dropdown-bar',
                        [{"label": "15", "value": "15"},
                        {"label": "25", "value": "25"},
                        {"label": "50", "value": "50"},
                        ],
                        '15')
        ], style={'font-size': 20, 'margin-right': '20px', 'width': '200px'})
    ], style={'display': 'flex'}),
    
    html.Br(),

    html.P("Range Values:"),
    # dcc.RangeSlider(
    #     id='range-slider-id', 
    #     min=0,
    #     max=10,
    #     step=1,
    #     value=[0, 10]
    #     ),
    
    html.Div([
        dcc.RangeSlider(
            min=0,
            max=20,
            step=1, 
            value = [0,20], 
            id="range-slider-id"),
        ], id = "range-slider-container"),

    html.Br(),

    html.Div([
        html.Div(dcc.Graph(id='candle-stick-id')),
        html.Br(),
        html.Div(dcc.Graph(id="rsi-indicator-id")),
    ]),

    # Interval component for real-time updates
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,
        n_intervals=0
    )
])

@app.callback(
        Output("range-slider-container", "children"),
        Input("dropdown-bar", "value")
        )

def update_rangeslider(num_bars):
    return dcc.RangeSlider(
                            min=0, 
                            max=int(num_bars), 
                            step = 1,
                            value = [0, int(num_bars)], 
                            id = "range-slider-id"
                            )

@app.callback(
    Output(component_id='candle-stick-id', component_property='figure'),
    [Input(component_id='dropdown-coin', component_property='value'),
     Input(component_id='dropdown-time', component_property='value'),
     Input(component_id='dropdown-bar', component_property='value'),
     Input(component_id='range-slider-id', component_property='value'),
     Input('interval-component', 'n_intervals')]
)

def update_candle_stick(coin_pair, num_time, num_bar, range_values, n_intervals):
    url = f"https://www.bitstamp.net/api/v2/ohlc/{coin_pair}/"
    
    params = {
        "step": int(num_time),
        "limit": int(num_bar) + 14,
    }
    
    data = requests.get(url, params=params).json()["data"]["ohlc"]
    data = pd.DataFrame(data)
    data.timestamp = pd.to_datetime(data.timestamp, unit="s")
    
    data[["open", "high", "low", "close", "volume"]] = data[["open", "high", "low", "close", "volume"]].astype(float)
    
    data = data.groupby('timestamp').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).reset_index()

    data["RSI"] = ta.rsi(data["close"])

    # data = data.iloc[14:]
    data = data.iloc[range_values[0]:range_values[1]]
    
    candles = go.Figure(data=[go.Candlestick(
        x=data['timestamp'],
        open=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['close'],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])
    
    # Adjust layout for better spacing
    candles.update_layout(
        xaxis_rangeslider_visible=False,   # Remove range slider
        template="plotly_dark"
    )

    candles.update_layout(
        xaxis_title="Timestamp",
        yaxis_title="Price",
        transition_duration=500)
    
    return candles


@app.callback(
    Output(component_id='rsi-indicator-id', component_property='figure'),
    [Input(component_id='dropdown-coin', component_property='value'),
     Input(component_id='dropdown-time', component_property='value'),
     Input(component_id='dropdown-bar', component_property='value'),
     Input(component_id='range-slider-id', component_property='value'),
     Input('interval-component', 'n_intervals')]
)

def update_indicator_stick(coin_pair, num_time, num_bar, range_values, n_intervals):
    url = f"https://www.bitstamp.net/api/v2/ohlc/{coin_pair}/"
    
    params = {
        "step": int(num_time),
        "limit": int(num_bar) + 14,
    }
    
    data = requests.get(url, params=params).json()["data"]["ohlc"]
    data = pd.DataFrame(data)
    data.timestamp = pd.to_datetime(data.timestamp, unit="s")
    
    data[["open", "high", "low", "close", "volume"]] = data[["open", "high", "low", "close", "volume"]].astype(float)
    
    data = data.groupby('timestamp').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    }).reset_index()

    data["RSI"] = ta.rsi(data["close"])

    data = data.iloc[14:]
    data = data.iloc[range_values[0]:range_values[1]]

    indicator = px.line(x=data.timestamp, y=data["RSI"], height = 300, template = "plotly_dark")
    indicator.update_layout(
        xaxis_title="Timestamp",
        yaxis_title="RSI",
        transition_duration=500
    )
    
    return indicator


# Run the app
if __name__ == '__main__':
    app.run_server(port="8050")
