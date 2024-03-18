Here is the revised Python code to generate a longitudinal dataset demonstrating the impact of an intervention on academic achievement in high schools, as measured by grade point average (GPA):

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

start_date = datetime(2020, 1, 1)
end_date = datetime(2022, 12, 31)
num_schools = 200
intervention_date = datetime(2021, 6, 1)

demographics = ['Urban', 'Suburban', 'Rural']
intervention_group = np.random.choice([0, 1], size=num_schools, p=[0.5, 0.5])

dates = pd.date_range(start=start_date, end=end_date, freq='M')
school_ids = list(range(1, num_schools + 1))

data = []
for school_id in school_ids:
    demographic = np.random.choice(demographics)
    gpa_baseline = np.random.normal(2.5, 0.3)
    for date in dates:
        if date < intervention_date:
            gpa_mean = gpa_baseline + np.random.normal(0, 0.1)
        else:
            if intervention_group[school_id - 1] == 1:
                gpa_mean = gpa_baseline + 0.15 + np.random.normal(0, 0.1)
            else:
                gpa_mean = gpa_baseline + np.random.normal(0, 0.1)
        
        gpa = np.clip(np.random.normal(gpa_mean, 0.3), 0.0, 4.0)
        data.append([school_id, date, gpa, intervention_group[school_id - 1], demographic])

df = pd.DataFrame(data, columns=['school_id', 'date', 'gpa', 'intervention_group', 'demographic'])
df['semester'] = pd.PeriodIndex(df['date'], freq='Q')
df_summary = df.groupby(['school_id', 'semester', 'intervention_group', 'demographic'])['gpa'].mean().reset_index()

print(df_summary.head(10))
print(df_summary.tail(10))