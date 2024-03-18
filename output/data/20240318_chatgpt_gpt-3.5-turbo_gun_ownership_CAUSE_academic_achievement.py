import pandas as pd
import numpy as np
import datetime

np.random.seed(42)

# Create a date range for the period before the intervention
before_dates = pd.date_range(start='1/1/2020', end='6/30/2020')

# Create a date range for the period after the intervention
after_dates = pd.date_range(start='7/1/2020', periods=6, freq='M')

# Create the dataframe
data = {'Date': before_dates.tolist()*2 + after_dates.tolist()*2,
        'School_ID': np.repeat(range(1, 971), 4),
        'Treatment': np.tile([0, 1, 0, 1], 970),
        'GDP_per_capita': np.random.normal(50000, 10000, 1930),
        'Avg_Academic_Achievement': np.random.normal(75, 10, 1930),
        'Baseline_Crime_Rate': np.random.normal(100, 20, 1930)}

df = pd.DataFrame(data)
df['GPA'] = 0

# Simulate a GPA increase post-intervention for the treatment group
df.loc[df['Treatment'] == 1, 'GPA'] = np.random.normal(3.5, 0.5, sum(df['Treatment'] == 1))

df.head(10)