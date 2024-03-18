import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_school_data(num_schools, start_date, end_date):
    schools = []
    for i in range(num_schools):
        school_id = f'school_{i+1}'
        city_gdp = np.random.normal(50000, 10000)
        baseline_achievement = np.random.normal(3.0, 0.5)
        baseline_crime_rate = np.random.normal(5, 2)
        schools.append((school_id, city_gdp, baseline_achievement, baseline_crime_rate))
    return schools

def assign_to_groups(schools):
    np.random.seed(42)  # Set a fixed random seed for reproducibility
    np.random.shuffle(schools)
    mid = len(schools) // 2
    treatment_group = schools[:mid]
    control_group = schools[mid:]
    return treatment_group, control_group

def generate_gpa_data(schools, start_date, end_date, intervention_date, treatment_group):
    data = []
    for school in schools:
        school_id, city_gdp, baseline_achievement, baseline_crime_rate = school
        current_date = start_date
        while current_date <= end_date:
            if current_date < intervention_date:
                gpa = np.random.normal(baseline_achievement, 0.1)
            else:
                if school in treatment_group:
                    gpa = np.random.normal(baseline_achievement + 0.2, 0.1)  # Reduce treatment effect to 0.2
                else:
                    gpa = np.random.normal(baseline_achievement, 0.1)
            data.append((school_id, current_date, gpa, city_gdp, baseline_achievement, baseline_crime_rate))
            current_date += timedelta(days=30)
    return data

num_schools = 200  # Reduce number of schools to a more realistic value
start_date = datetime(2020, 1, 1)
end_date = datetime(2022, 12, 31)
intervention_date = datetime(2021, 7, 1)

schools = generate_school_data(num_schools, start_date, end_date)
treatment_group, control_group = assign_to_groups(schools)
data = generate_gpa_data(schools, start_date, end_date, intervention_date, treatment_group)

df = pd.DataFrame(data, columns=['school_id', 'date', 'gpa', 'city_gdp', 'baseline_achievement', 'baseline_crime_rate'])

print("Summary statistics:")
print(df.describe())

print("\nCorrelation matrix:")
print(df.corr())

print("\nRegression analysis:")
from statsmodels.formula.api import ols
model = ols('gpa ~ C(school_id) + city_gdp + baseline_achievement + baseline_crime_rate', data=df).fit()
print(model.summary())