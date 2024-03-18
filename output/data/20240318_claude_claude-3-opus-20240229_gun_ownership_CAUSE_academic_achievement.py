import pandas as pd
import numpy as np
from datetime import datetime, timedelta

num_schools = 1973
start_date = datetime(2020, 1, 1)
end_date = datetime(2022, 12, 31)

cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose'] * (num_schools // 10 + 1)
cities = cities[:num_schools]

gdp_per_capita = np.random.normal(50000, 10000, num_schools).astype(int)
baseline_academic_achievement = np.random.normal(3.0, 0.3, num_schools).round(2)
baseline_crime_rates = np.random.normal(5, 2, num_schools).round(2)

treatment_group = np.random.choice([0, 1], num_schools, p=[0.5, 0.5])

dates = pd.date_range(start=start_date, end=end_date, freq='M')

data = []
for school_id in range(num_schools):
    for date in dates:
        if treatment_group[school_id] == 1 and date >= datetime(2021, 7, 1):
            intervention_effect = np.random.normal(0.1, 0.02)
        else:
            intervention_effect = 0
        
        gpa = baseline_academic_achievement[school_id] + intervention_effect + np.random.normal(0, 0.05)
        crime_rate = baseline_crime_rates[school_id] - intervention_effect*2 + np.random.normal(0, 0.5)
        
        data.append({
            'school_id': school_id,
            'city': cities[school_id],
            'gdp_per_capita': gdp_per_capita[school_id],
            'baseline_academic_achievement': baseline_academic_achievement[school_id],
            'baseline_crime_rates': baseline_crime_rates[school_id],
            'treatment_group': treatment_group[school_id],
            'date': date,
            'gpa': round(gpa, 2),
            'crime_rate': round(max(crime_rate,0), 2)
        })

df = pd.DataFrame(data)
print(df.head(20))