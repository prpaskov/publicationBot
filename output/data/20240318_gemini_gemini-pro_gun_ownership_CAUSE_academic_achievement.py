```python

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

# Create a list of 1914 high schools in the USA
high_schools = pd.DataFrame()
high_schools['SchoolID'] = range(1, 1915)
high_schools['city_gdp_per_capita'] = np.random.normal(100000, 20000, 1914)
high_schools['baseline_crime_rate'] = np.random.normal(500, 100, 1914)
high_schools['baseline_academic_achievement'] = np.random.normal(75, 10, 1914)

# Randomly assign half of the high schools to the treatment group and half to the control group
high_schools['treatment_group'] = np.random.choice([0, 1], 1914)

# Create a time series of high school mean GPA for both the treatment and control groups
start_date = datetime.now() - timedelta(days=365 * 5)
end_date = datetime.now()
dates = pd.date_range(start_date, end_date, freq='D')
high_schools['date'] = np.random.choice(dates, 1914)
high_schools['mean_gpa'] = np.random.normal(75, 10, 1914)

# Intervene on the treatment group at the midpoint of the time series
intervention_date = (end_date - start_date) / 2
high_schools.loc[high_schools['treatment_group'] == 1, 'mean_gpa'] = high_schools.loc[high_schools['treatment_group'] == 1, 'mean_gpa'].add(10, fill_value=0)
high_schools['treatment_group'] = high_schools['treatment_group'].astype('category')

```