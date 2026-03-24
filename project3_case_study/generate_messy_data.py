import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

n = 500
dates = []
for _ in range(n):
    base_date = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 365))
    choice = np.random.choice(['iso', 'us', 'ddmon'])
    if choice == 'iso':
        dates.append(base_date.strftime('%Y-%m-%d'))
    elif choice == 'us':
        dates.append(base_date.strftime('%m/%d/%y'))
    else:
        dates.append(base_date.strftime('%d-%b-%y'))

df = pd.DataFrame({
    'order_date': dates,
    'customer': [f"customer_{np.random.randint(1,100)}" for _ in range(n)],
    'product': np.random.choice(['A', 'B', 'C', 'D', 'E'], n),
    'sales': np.random.uniform(10, 1000, n).round(2),
    'quantity': np.random.randint(1, 20, n),
    'region': np.random.choice(['North', 'South', 'East', 'West', ''], n, p=[0.25,0.25,0.25,0.24,0.01])
})

df.loc[np.random.choice(n, 30, replace=False), 'sales'] = np.nan
df.loc[np.random.choice(n, 20, replace=False), 'customer'] = ''
df.loc[10:20, 'product'] = df.loc[10:20, 'product'] + ' '
df.loc[30:40, 'region'] = df.loc[30:40, 'region'].str.lower()
df = pd.concat([df, df.sample(10)], ignore_index=True)

df.to_csv('messy_data.csv', index=False)
print("Messy dataset created: messy_data.csv")
