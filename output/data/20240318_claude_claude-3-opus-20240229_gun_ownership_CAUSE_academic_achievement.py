import pandas as pd
import numpy as np
from datetime import datetime, timedelta

sample_size = 1971
num_years = 5
intervention_year = 3

cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
gdp_per_capita = [70000, 65000, 60000, 62000, 55000, 58000, 52000, 56000, 61000, 59000]
baseline_crime_rates = [5.2, 4.8, 6.1, 5.5, 4.3, 5.7, 4.1, 4.6, 5.0, 4.9]
baseline_academic_achievement = [3.2, 3.1, 2.9, 3.0, 2.8, 3.1, 2.7, 2.9, 3.0, 2.8]

data = []
start_date = datetime(2010, 1, 1)

for i in range(sample_size):
    city_idx = i % len(cities)
    city = cities[city_idx]
    gdp = gdp_per_capita[city_idx]
    crime_rate = baseline_crime_rates[city_idx]
    academic_achievement = baseline_academic_achievement[city_idx]
    
    treatment = 1 if np.random.random() < 0.5 else 0
    
    for year in range(num_years):
        date = start_date + timedelta(days=365*year)
        
        if year < intervention_year:
            gpa = academic_achievement + np.random.normal(0, 0.1)
        else:
            if treatment == 1:
                gpa = academic_achievement + np.random.normal(0.2, 0.1)
            else:
                gpa = academic_achievement + np.random.normal(0, 0.1)
        
        data.append([date, city, gdp, crime_rate, academic_achievement, treatment, gpa])

df = pd.DataFrame(data, columns=['date', 'city', 'gdp_per_capita', 'baseline_crime_rate', 'baseline_academic_achievement', 'treatment', 'high_school_mean_gpa'])
df['date'] = pd.to_datetime(df['date'])

df['city'] = pd.Categorical(df['city'], categories=cities, ordered=True)

df = df.sort_values(['city', 'date'])

df['high_school_mean_gpa'] = df['high_school_mean_gpa'].round(2)

df.to_csv('education_intervention_data.csv', index=False)