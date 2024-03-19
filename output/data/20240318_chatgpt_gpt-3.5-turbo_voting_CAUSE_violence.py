import pandas as pd
import numpy as np
import random
import datetime

# Set random seed for reproducibility
np.random.seed(42)

# Generate demographic data
demographics = pd.DataFrame({
    'income': np.random.normal(50000, 10000, 1783),
    'education_level': np.random.choice(['High School', 'College', 'Graduate'], 1783),
    'age': np.random.randint(60, 90, 1783),
    'health': np.random.choice(['Good', 'Fair', 'Poor'], 1783)
})

# Assign treatment group
demographics['treatment'] = np.random.choice([0, 1], 1783)

# Generate dates for the time series
start_date = datetime.date(2019, 1, 1)
end_date = datetime.date(2024, 12, 31)
dates = pd.date_range(start=start_date, end=end_date)

# Generate longitudinal dataset
data = pd.DataFrame({
    'date': np.repeat(dates, 1783),
    'income': np.repeat(demographics['income'].values, len(dates)),
    'education_level': np.repeat(demographics['education_level'].values, len(dates)),
    'age': np.repeat(demographics['age'].values, len(dates)),
    'health': np.repeat(demographics['health'].values, len(dates)),
    'treatment': np.repeat(demographics['treatment'].values, len(dates)),
    'reported_attack_on_household': np.random.binomial(1, 0.2, len(dates) * 1783)
})

data.head()