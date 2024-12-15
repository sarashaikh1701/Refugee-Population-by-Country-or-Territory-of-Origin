Global Refugee Population Visualization

Overview
    This project presents an interactive, web-based data visualization exploring global refugee populations by country or territory of origin from 1951 to 2023. Using a combination of choropleth maps, time-series line charts, bar charts, and small multiples, the visualization allows users to understand both global distributions and specific country-level trends over time. Additional features like animation, facetting, and log-scale options help manage the dataset’s complexity and highlight key insights.

Key Features
    Choropleth Map with Animation: 
    Visualize the global distribution of refugees across decades. Animate through years (Play/Pause) to watch distributions evolve and identify temporal patterns.
          
    Time-Series Analysis for Selected Countries: 
    Select any number of countries to see their refugee population trends over time. Switch between linear and logarithmic scales to handle large differences in population counts.
    
    Top 10 Bar Chart by Year:
    Instantly identify the top 10 refugee-origin countries for any chosen year. This ranking helps pinpoint major contributors and track changes in their positions over time.
    
    Small Multiples (Faceted Views):
    Compare the top 3 countries from a selected year side-by-side in separate time-series plots, reducing clutter and making it easier to analyze differences and similarities.

Data
    Source: UNHCR Refugee Population Statistics Database (processed by Our World in Data).
    Attributes:
    Year (1951–2023)
    Country (Entity)  
    Population (Refugee count)

    The dataset’s wide temporal range and substantial variation in population sizes introduce complexity. The visualization addresses this by using categorical color breaks for the choropleth map, log-scale           options for the time-series chart, and filtering controls.

Requirements
    Python 3.7+ recommended
    Dependencies:
      - Dash
      - Plotly
      - Pandas

All dependencies are listed in `requirements.txt`.

To Run:
    1. pip install -r requirements.txt
    2. python app.py
