import pandas as pd
import json
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import datetime

# File paths
csv_file = 'refugee-population-by-country-or-territory-of-origin.csv'
metadata_file = 'refugee-population-by-country-or-territory-of-origin.metadata.json'

# Load and preprocess CSV
data = pd.read_csv(csv_file)
data.rename(columns={data.columns[-1]: 'Population'}, inplace=True)
data['Year'] = pd.to_datetime(data['Year'], format='%Y').dt.year

year_min = data['Year'].min()
year_max = data['Year'].max()

# Marks every 20 years for clarity:
year_marks_map = {str(y): str(y) for y in range(year_min, year_max+1, 5)}
year_marks_top10 = {str(y): str(y) for y in range(year_min, year_max+1, 10)}

# Load metadata
with open(metadata_file, 'r', encoding='utf-8') as f:
    metadata = json.load(f)

chart_title = metadata.get("charts", {}).get("title", "Refugee Population by Country or Territory of Origin")
data_unit = "Refugee Population"

default_year = 2023

color_scale = ['#fff7bc', '#fee391', '#fec44f', '#fe9929', '#d95f0e', '#993404']

def get_population_category(value):
    if value <= 1000:
        return "0 - 1,000"
    elif value <= 5000:
        return "1,000 - 5,000"
    elif value <= 10000:
        return "5,000 - 10,000"
    elif value <= 50000:
        return "10,000 - 50,000"
    elif value <= 100000:
        return "50,000 - 100,000"
    elif value <= 500000:
        return "100,000 - 500,000"
    elif value <= 1000000:
        return "500,000 - 1,000,000"
    else:
        return "1,000,000+"

categories = [
    "0 - 1,000",
    "1,000 - 5,000",
    "5,000 - 10,000",
    "10,000 - 50,000",
    "50,000 - 100,000",
    "100,000 - 500,000",
    "500,000 - 1,000,000",
    "1,000,000+"
]

category_colors = {
    "0 - 1,000": color_scale[0],
    "1,000 - 5,000": color_scale[1],
    "5,000 - 10,000": color_scale[2],
    "10,000 - 50,000": color_scale[3],
    "50,000 - 100,000": color_scale[4],
    "100,000 - 500,000": color_scale[5],
    "500,000 - 1,000,000": color_scale[5],
    "1,000,000+": color_scale[5]
}

def dark_theme(fig):
    fig.update_layout(
        paper_bgcolor='black',
        plot_bgcolor='black',
        font=dict(color='white', family='Arial,sans-serif'),
        margin=dict(l=20, r=20, t=30, b=30)
    )
    fig.update_xaxes(title_font=dict(color='white'))
    fig.update_yaxes(title_font=dict(color='white'))
    return fig

app = Dash(__name__)
app.title = chart_title

app.index_string = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>{chart_title}</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                margin:0; padding:0; background:black; color:white; font-family:Arial,sans-serif;
                overflow:hidden; 
            }}
            .container {{
                display:grid;
                grid-template-columns: 50% 50%;
                grid-template-rows: 100%;
                height:100vh;
                width:100vw;
            }}
            .left-col {{
                display:flex; flex-direction:column; align-items:center; justify-content:flex-start;
                padding:10px; box-sizing:border-box;
            }}
            .right-col {{
                display:flex; flex-direction:column; 
                padding:10px; box-sizing:border-box;
            }}
            .title {{
                text-align:center; font-size:14px; margin:5px 0;
            }}
            .subtitle {{
                text-align:center; font-size:10px; color:#ccc; margin:0 auto;
            }}
            h2 {{
                font-size:12px; text-align:center; margin:5px 0;
            }}
            .controls {{
                text-align:center; margin:5px 0; font-size:10px; color:white;
            }}
            button {{
                background:#333; color:white; border:none; cursor:pointer; padding:3px 6px; margin:0 3px;
                font-size:10px;
            }}
            .right-top {{
                flex:1; display:flex; flex-direction:row; align-items:stretch; justify-content:space-between; margin-bottom:5px;
            }}
            .right-bottom {{
                flex:1; display:flex; flex-direction:column; align-items:center; justify-content:flex-start;
            }}
            .chart-box {{
                flex:1; display:flex; flex-direction:column; align-items:center; justify-content:flex-start;
                margin:0 5px; box-sizing:border-box;
            }}
            .dropdown-container {{
                width:90%; margin:0 auto;
            }}
            .slider-container {{
                width:95%; margin:5px auto;
            }}
        </style>
    </head>
    <body>
        {{%app_entry%}}
        {{%config%}}
        {{%scripts%}}
        {{%renderer%}}
    </body>
</html>
"""

app.layout = html.Div([
    # 2-column layout: left = map; right = top 10 & small multiples (top), time series bottom
    html.Div([
        # Left Column (Map)
        html.Div([
            html.H1(chart_title, className='title'),
            html.P("Explore global refugee populations over time", className='subtitle'),
            html.H2("Global Distribution"),
            html.Div([
                html.Button("Play", id="play-button", n_clicks=0),
                html.Button("Pause", id="pause-button", n_clicks=0),
            ], className='controls'),
            html.Div([
                    # No style prop on slider, style on parent Div only
                dcc.Slider(
                    id='map-year-slider',
                    min=year_min,
                    max=year_max,
                    value=default_year,
                    marks=year_marks_map,
                    step=None,
                    updatemode='drag',
                    tooltip={'always_visible': False, 'placement': 'bottom'}
                    )
                ], className='slider-container'),
            dcc.Graph(id='choropleth-map', style={'height':'60%', 'width':'95%', 'margin':'5px auto'})
        ], className='left-col'),

        # Right Column
        html.Div([
            # Top: two chart-boxes side-by-side (Top 10 and Small Multiples)
            html.Div([
                html.Div([
                    html.H2("Top 10 Countries"),
                    html.Div([
                        dcc.Slider(
                            id='year-slider',
                            min=year_min,
                            max=year_max,
                            value=default_year,
                            marks=year_marks_top10,
                            step=None,
                            updatemode='drag',
                            tooltip={'always_visible': False, 'placement': 'bottom'}
                        )
                    ], className='controls', style={'width':'90%', 'margin':'5px auto'}),
                    # No color for bars => single color bars, no legend
                    dcc.Graph(id='top-10-bar', style={'height':'70%', 'width':'95%'})
                ], className='chart-box'),

                html.Div([
                    # Top 3 countries (Facets)
                    html.H2("Top 3 Countries (Facets)"),
                    dcc.Graph(id='small-multiples', style={'height':'70%', 'width':'95%'})
                ], className='chart-box'),

            ], className='right-top'),

            # Bottom: Time Series by Country (no linear/log radio)
            html.Div([
                html.H2("Time Series by Country"),
                html.Div([
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': c, 'value': c} for c in sorted(data['Entity'].unique())],
                        multi=True,
                        placeholder="Select countries",
                        style={'fontSize':'10px', 'color':'black'}
                    )
                ], className='controls dropdown-container'),
                dcc.Graph(id='time-series-plot', style={'height':'70%', 'width':'95%'})
            ], className='right-bottom')

        ], className='right-col'),

        dcc.Interval(id='year-interval', interval=1000, n_intervals=0, disabled=True)
    ], className='container', style={'width':'100vw','height':'100vh','backgroundColor':'black','overflow':'hidden'})
])

@app.callback(
    Output('time-series-plot', 'figure'),
    Input('country-dropdown', 'value')
)
def update_time_series(selected_countries):
    if not selected_countries:
        fig = px.line(title="Select countries")
        fig = dark_theme(fig)
        return fig
    filtered = data[data['Entity'].isin(selected_countries)]
    fig = px.line(
        filtered,
        x='Year',
        y='Population',
        color='Entity',
        labels={'Population': data_unit},
        title=""
    )
    # Always linear scale
    fig.update_yaxes(type='linear')
    fig = dark_theme(fig)
    return fig

@app.callback(
    Output('top-10-bar', 'figure'),
    Input('year-slider', 'value')
)
def update_top_10(year):
    filtered = data[data['Year'] == year].sort_values('Population', ascending=False).head(10)
    fig = px.bar(
        filtered,
        x='Population',
        y='Entity',
        orientation='h',
        labels={'Population': data_unit, 'Entity': 'Country'},
        title=f"Top 10 refugee population coutries in, {year}",
        color='Population',
        color_continuous_scale=color_scale
    )
    fig.update_layout(
        yaxis=dict(autorange='reversed'), 
        coloraxis_colorbar_title=None,  
        coloraxis_showscale=False,  
        showlegend=False
        )
    fig = dark_theme(fig)
    return fig

@app.callback(
    Output('small-multiples', 'figure'),
    Input('year-slider', 'value')
)
def update_small_multiples(year):
    filtered = data[data['Year'] == year].sort_values('Population', ascending=False).head(3)
    top_3 = filtered['Entity'].unique()
    df_top3 = data[data['Entity'].isin(top_3)]
    fig = px.line(
        df_top3,
        x='Year',
        y='Population',
        color='Entity',
        facet_col='Entity',
        facet_col_wrap=3,
        labels={'Population': data_unit}
    )
    fig.update_yaxes(matches=None)
    fig.update_layout(showlegend=False)
    fig = dark_theme(fig)
    return fig

@app.callback(
    Output('choropleth-map', 'figure'),
    Input('map-year-slider', 'value')
)
def update_map(selected_year):
    d = data[data['Year'] == selected_year].copy()
    d['Category'] = d['Population'].apply(get_population_category)
    fig = px.choropleth(
        d,
        locations='Code',
        locationmode='ISO-3',
        hover_name='Entity',
        hover_data={'Population': True, 'Code': False, 'Year': False, 'Category': True},
        color='Category',
        title=f"Refugee population by country or territory of origin, {selected_year}",
        category_orders={"Category": categories},
        color_discrete_map=category_colors
    )
    fig.update_layout(
        font=dict(color='white'),
        geo=dict(showframe=False, showcoastlines=False, projection_type='natural earth', bgcolor='black')
    )
    fig = dark_theme(fig)
    return fig

@app.callback(
    Output('year-interval', 'disabled'),
    Input('play-button', 'n_clicks'),
    Input('pause-button', 'n_clicks'),
    State('year-interval', 'disabled')
)
def play_pause_animation(play_n, pause_n, current_disabled):
    if play_n > pause_n:
        return False
    else:
        return True

@app.callback(
    Output('map-year-slider', 'value'),
    Input('year-interval', 'n_intervals'),
    State('map-year-slider', 'value'),
    State('year-interval', 'disabled')
)
def animate_year(n, current_year, disabled):
    if disabled:
        return current_year
    max_year = data['Year'].max()
    next_year = current_year + 1
    if next_year > max_year:
        next_year = data['Year'].min()
    return next_year

if __name__ == '__main__':
    app.run_server(debug=False, port=8050)
