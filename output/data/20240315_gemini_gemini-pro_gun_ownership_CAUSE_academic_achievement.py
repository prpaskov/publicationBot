import numpy as np
import pandas as pd
from statsmodels.tsa.statespace. sarimax import SARIMAX
from sklearn.model_selection import train_test_split
from sklearn. preprocessing import StandardScaler

# Define the parameters of the experiment
intervention_duration = 6 # in months
num_schools = 2167
num_time_points = 5 # 2 points before the intervention and 3 after

# Create a dataframe with the school and time-series data
df = pd.DataFrame({\
'school_id': np.arange(num_schools), \
'city_gdp_per_capita': np.random.randint(10000, 40000, num_schools), \
'baseline_crime_rate': np.random.randint(100, 1000, num_schools), \
'baseline_gpa': np.random.randint(2, 4, num_schools)})

# Convert time points to date time
date_range = pd.date_range(start='2020-01-01', periods=num_time_points, freq='3MS')
df['time_point'] = date_range

# Create a dummy variable for the intervention group
intervention_group = np.random.randint(0, 2, num_schools)
df['intervention_group'] = intervention_group

# Create a SARIMA model to simulate the time series data
sarima_model = SARIMAX(df.baseline_gpa, order=(1, 1, 1))
simulated_gpa = sarima_model.fit().forecast(steps=num_time_points)

# Assign the simulated GPA to the dataframe
df['simulated_gpa'] = simulated_gpa

# Intervene with the time series
df.loc[df.intervention_group == 1 & df.time_point >= '2020-07-01', 'simulated_gpa'] =\
df.loc[df.intervention_group == 1 & df.time_point >= '2020-07-01', \
'simulated_gpa'] + 0.3

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(df[['city_gdp_per_capita', \
'baseline_crime_rate', 'baseline_gpa', 'intervention_group']], \
df.simulated_gpa, test_size=0.2, random_state=42)

# Scale the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Fit a linear regression model to the data
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model on the test set
print('R-squared:', model.score(X_test, y_test))