import numpy as np
import pandas as pd
from datetime import datetime

def generate_balanced_groups(n, p):
    group = np.random.choice(['control', 'treatment'], size=n, p=[1-p, p])
    return group

def generate_baseline_gpa(n, mean, std):
    baseline_gpa = np.random.normal(mean, std, size=n)
    baseline_gpa = np.clip(baseline_gpa, 0.0, 4.0)  # Restrict GPA to 0.0-4.0 range
    return baseline_gpa

def generate_post_intervention_gpa(baseline_gpa, group, treatment_effect):
    post_intervention_gpa = baseline_gpa + (group == 'treatment') * treatment_effect
    post_intervention_gpa = np.clip(post_intervention_gpa, 0.0, 4.0)  # Restrict GPA to 0.0-4.0 range
    return post_intervention_gpa

def generate_city_gdp_per_capita(n, mean, std):
    city_gdp_per_capita = np.random.normal(mean, std, size=n)
    city_gdp_per_capita = np.clip(city_gdp_per_capita, 0, None)  # Ensure non-negative GDP per capita
    return city_gdp_per_capita

def generate_baseline_crime_rate(n, mean, std):
    baseline_crime_rate = np.random.normal(mean, std, size=n)
    baseline_crime_rate = np.clip(baseline_crime_rate, 0, None)  # Ensure non-negative crime rate
    return baseline_crime_rate

sample_size = 1916
treatment_probability = 0.5
baseline_gpa_mean = 3.0
baseline_gpa_std = 0.5
treatment_effect = 0.2
city_gdp_per_capita_mean = 50000
city_gdp_per_capita_std = 10000
baseline_crime_rate_mean = 5
baseline_crime_rate_std = 2

group = generate_balanced_groups(sample_size, treatment_probability)
baseline_gpa = generate_baseline_gpa(sample_size, baseline_gpa_mean, baseline_gpa_std)
post_intervention_gpa = generate_post_intervention_gpa(baseline_gpa, group, treatment_effect)
city_gdp_per_capita = generate_city_gdp_per_capita(sample_size, city_gdp_per_capita_mean, city_gdp_per_capita_std)
baseline_crime_rate = generate_baseline_crime_rate(sample_size, baseline_crime_rate_mean, baseline_crime_rate_std)

start_date = datetime(2020, 1, 1)
end_date = datetime(2021, 12, 31)
intervention_date = datetime(2021, 1, 1)

dates = pd.date_range(start=start_date, end=end_date, freq='M')

data = {
    'high_school_id': range(1, sample_size + 1),
    'group': group,
    'city_gdp_per_capita': city_gdp_per_capita,
    'baseline_crime_rate': baseline_crime_rate
}

for i, date in enumerate(dates):
    if date < intervention_date:
        data[f'gpa_{date.strftime("%Y-%m")}'] = baseline_gpa
    else:
        data[f'gpa_{date.strftime("%Y-%m")}'] = post_intervention_gpa

df = pd.DataFrame(data)

print(df.head())