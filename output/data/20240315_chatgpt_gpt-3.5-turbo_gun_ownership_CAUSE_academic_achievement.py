import pandas as pd
import numpy as np
import random
import datetime

# Create empty dataframe
data = pd.DataFrame(columns=['School_ID', 'Treatment', 'Date', 'GPA', 'Demographic_X'])

# Assign values
data['School_ID'] = np.random.choice(range(1, 100), 1972)
data['Treatment'] = np.random.choice([0, 1], 1972)  # 0 for control, 1 for intervention
data['Date'] = pd.date_range(start='1/1/2018', periods=1972)  # Date range for time series
data['GPA'] = np.random.normal(3.0, 0.5, 1972)  # GPA values
data['Demographic_X'] = np.random.choice(['A', 'B', 'C'], 1972)  # Demographic values

# Display dataframe
print(data.head())