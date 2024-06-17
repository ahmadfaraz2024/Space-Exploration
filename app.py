'''
from flask import Flask, render_template
import pickle

app = Flask(__name__)

# Load coefficients from pickle file
with open('top_coefficients_cost.pkl', 'rb') as f:
    coefficients_data = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html', coefficients_data=coefficients_data)

if __name__ == '__main__':
    app.run(debug=True)
'''


'''
from flask import Flask, render_template
import pickle
import plotly.graph_objs as go

app = Flask(__name__)

# Load coefficients from pickle file
with open('top_coefficients_cost.pkl', 'rb') as f:
    coefficients_data = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html', coefficients_data=coefficients_data)

@app.route('/graphs')
def graphs():
    graph_data = {}
    for category, coeffs in coefficients_data.items():
        max_coeffs = coeffs['top_max']
        min_coeffs = coeffs['top_min']
        max_features = list(max_coeffs.keys())
        max_values = list(max_coeffs.values())
        min_features = list(min_coeffs.keys())
        min_values = list(min_coeffs.values())

        # Create graphs
        max_graph = go.Bar(x=max_features, y=max_values, name='Top Maximum Coefficients', marker_color='rgb(91, 155, 213)')
        min_graph = go.Bar(x=min_features, y=min_values, name='Top Minimum Coefficients', marker_color='rgb(237, 125, 49)')

        # Convert graphs to JSON-compatible dictionaries
        max_graph_json = max_graph.to_plotly_json()
        min_graph_json = min_graph.to_plotly_json()

        # Add JSON graphs to graph_data
        graph_data[category] = {'max_graph': max_graph_json, 'min_graph': min_graph_json}

    return render_template('graphs.html', graph_data=graph_data)

if __name__ == '__main__':
    app.run(debug=True)
'''

import pickle

from flask import Flask, render_template
import pandas as pd
import plotly.express as px

df = pd.read_excel('final.xlsx')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rockets')
def rockets():
    return render_template('rockets.html')

@app.route('/missions')
def missions():
    return render_template('missions.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
def dashboard():

    #Space missions around the world
    map_fig = px.scatter_geo(df, locations='Location', locationmode='country names', 
                             hover_name='country',
                             title='Map of Space Missions Around the World')
    # Space mission trends over time
    space_mission_trends = px.line(df, x='Year', title='Space Mission Trends over Time')

    # Most active space companies
    most_active_companies = px.bar(df['Company Name'].value_counts().head(10), title='Most Active Space Companies')

    # Number of launches by year
    launches_by_year = px.histogram(df, x='Year', title='Number of Launches by Year')

    #Number of launches by decade
    launches_by_decade = px.histogram(df, x='Decade', title='Number of Launches by Year')

    # Number of launches by country
    launches_by_country = px.histogram(df, x='country', title='Number of Launches by Country')

    mission_outcomes = px.bar(df['Status Mission'].value_counts().reset_index(), 
                              x='count', y='Status Mission', 
                              title='Successful vs. Failed Missions')

    return render_template('dashboard.html',
                           space_mission_trends=space_mission_trends.to_html(include_plotlyjs=False, full_html=False),
                           most_active_companies=most_active_companies.to_html(include_plotlyjs=False, full_html=False),
                           launches_by_year=launches_by_year.to_html(include_plotlyjs=False, full_html=False),
                           launches_by_country=launches_by_country.to_html(include_plotlyjs=False, full_html=False)
                           ,map_fig=map_fig.to_html(include_plotlyjs=False, full_html=False)
                           ,mission_outcomes=mission_outcomes.to_html(include_plotlyjs=False, full_html=False),
                            launches_by_decade=launches_by_decade.to_html(include_plotlyjs=False, full_html=False))



# Load the data from pickle files
with open('top_coefficients_cost.pkl', 'rb') as f:
    cost_data = pickle.load(f)

with open('top_coefficients_success.pkl', 'rb') as f:
    success_data = pickle.load(f)

def create_chart(data, title):
    df = pd.DataFrame(data)
    fig = px.bar(df, x='Feature', y='Coefficient', title=title, color='Category')
    return fig.to_html(full_html=False)

@app.route('/analysis')
def analysis():
    cost_charts = {}
    success_charts = {}
    
    for category, coeffs in cost_data.items():
        if category != 'Season' and category!= 'Status':
            top_max_df = pd.DataFrame(coeffs['top_max'].items(), columns=['Feature', 'Coefficient'])
            top_max_df['Category'] = 'Top Max'
            top_min_df = pd.DataFrame(coeffs['top_min'].items(), columns=['Feature', 'Coefficient'])
            top_min_df['Category'] = 'Top Min'
            combined_df = pd.concat([top_max_df, top_min_df])
            cost_charts[category] = create_chart(combined_df, f'Cost Analysis: {category}')
    
    for category, coeffs in success_data.items():
        if category != 'Season' and category!= 'Status':
            top_max_df = pd.DataFrame(coeffs['top_max'].items(), columns=['Feature', 'Coefficient'])
            top_max_df['Category'] = 'Top Max'
            top_min_df = pd.DataFrame(coeffs['top_min'].items(), columns=['Feature', 'Coefficient'])
            top_min_df['Category'] = 'Top Min'
            combined_df = pd.concat([top_max_df, top_min_df])
            success_charts[category] = create_chart(combined_df, f'Success Analysis: {category}')
    
    return render_template('analysis.html', cost_charts=cost_charts, success_charts=success_charts)


if __name__ == '__main__':
    app.run(debug=True)
