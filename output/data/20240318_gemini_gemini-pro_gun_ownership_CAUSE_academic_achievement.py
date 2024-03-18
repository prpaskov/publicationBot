import pandas as pd
from datetime import datetime
import numpy as np

# Generate random school IDs
school_ids = np.arange(1, 1799)

# Generate random treatment group assignment (0 = control, 1 = treatment)
treatment_group = np.random.choice([0, 1], size=1798)

# Generate random baseline GPA scores
baseline_gpa = np.random.normal(loc=3.0, scale=0.5, size=1798)

# Generate random post-intervention GPA scores for the control group
control_post_gpa = np.random.normal(loc=baseline_gpa[treatment_group == 0] + 0.1, scale=0.5, size=np.sum(treatment_group == 0))

# Generate random post-intervention GPA scores for the treatment group
treatment_post_gpa = np.random.normal(loc=baseline_gpa[treatment_group == 1] + 0.3, scale=0.5, size=np.sum(treatment_group == 1))

# Create a dataframe with the generated data
df = pd.DataFrame({
    "school_id": school_ids,
    "treatment_group": treatment_group,
    "baseline_gpa": baseline_gpa,
    "post_gpa": np.concatenate([control_post_gpa, treatment_post_gpa]),

    "time": ['2022-05-01'] * 899 + ['2023-05-01'] * 899
})

df.time = pd.to_datetime(df.time)

# Generate random demographic variables
df["sex"] = np.random.choice(["male", "female"], size=1798)
df["race"] = np.random.choice(["white", "black", "hispanic", "asian", "other"], size=1798)
df["income"] = np.random.choice(["low", "middle", "high"], size=1798)

# Ensure that the demographics are balanced between treatment groups
df = df.groupby(["treatment_group"]).apply(lambda x: x.sample(frac=1)).reset_index(drop=True)

# Print the dataframe
print(df)