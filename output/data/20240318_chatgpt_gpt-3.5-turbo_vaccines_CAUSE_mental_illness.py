import pandas as pd
import numpy as np
import random
import datetime

# Setting random seed for reproducibility
random.seed(42)

# Setting up the data
sample_size = 1847
start_date = datetime.date(2020, 1, 1)

data = {'ID': range(1, sample_size + 1),
        'Group': np.random.choice(['Control', 'Intervention'], sample_size),
        'Income': np.random.normal(50000, 10000, sample_size),
        'EducationLevel': np.random.choice(['High School', 'College', 'Graduate'], sample_size),
        'Age': np.random.randint(60, 90, sample_size),
        'Health': np.random.choice(['Good', 'Fair', 'Poor'], sample_size),
        'Date': [start_date + datetime.timedelta(days=random.randint(1, 365)) for _ in range(sample_size)]}

df = pd.DataFrame(data)

# Generating mental illness diagnosis based on intervention
df['MentalIllnessDiagnosis'] = 0
df.loc[df['Group'] == 'Intervention', 'MentalIllnessDiagnosis'] = np.random.binomial(1, 0.7, df['Group'].value_counts()['Intervention'])

df = df.sort_values(by='Date')

df.to_csv('senior_citizens_mental_illness_data.csv', index=False)