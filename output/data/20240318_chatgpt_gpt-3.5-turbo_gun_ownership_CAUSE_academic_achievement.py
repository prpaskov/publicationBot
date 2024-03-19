import numpy as np
import pandas as pd
import random
import datetime

n = 1985
np.random.seed(42)

# Generating random dates for before and after intervention
start_date = datetime.date(2010, 1, 1)
end_date = datetime.date(2020, 1, 1)
date_list = [start_date + datetime.timedelta(days=x) for x in range(0, n)]

# Generating random high school mean GPA before intervention
mean_gpa_before = np.random.normal(2.0, 0.5, n)

# Generating random high school mean GPA after intervention
mean_gpa_after = mean_gpa_before + np.random.normal(0.5, 0.2, n)

# Generating random city GDP per capita
city_gdp_capita = np.random.choice(np.arange(50000, 80000, 1000), n)

# Generating random academic achievement levels
academic_achievement = np.random.choice(np.arange(1, 10), n)

# Generating random baseline crime rates
baseline_crime_rates = np.random.choice(np.arange(100, 1000, 10), n)

# Generating treatment group assignment
treatment = np.random.choice([0, 1], n)

data = {
    'Date': date_list,
    'Mean_GPA_Before': mean_gpa_before,
    'Mean_GPA_After': mean_gpa_after,
    'City_GDP_Per_Capita': city_gdp_capita,
    'Academic_Achievement': academic_achievement,
    'Baseline_Crime_Rates': baseline_crime_rates,
    'Treatment_Group_Assignment': treatment
}

df = pd.DataFrame(data)
df.head()