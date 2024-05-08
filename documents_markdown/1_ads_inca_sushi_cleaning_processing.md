# SEASONALITY CORRECTION FOR META ADS PERFORMANCE


## INTRODUCTION

This project aims to analyze the advertising data for "Inca Sushi" from 2021 to 2023, removing brazilian seasonality trends that have a direct impact on customer income.


## DATA PREPARATION

The dataset ads_inca_sushi_2021_2023.csv was loaded and preprocessed. Key steps included:

1. **Loading the data into a DataFrame.**
2. **Converting date columns to datetime format.**
3. **Sorting the data chronologically.**
4. **Resetting the index for easier data handling.**

```python
# Setting up the environment
import pandas as pd
import numpy as np
import holidays

# Read Dataset
df = pd.read_csv('ads_inca_sushi_2021_2023.csv')

# Convert date columns to datetime format
df['Início dos relatórios'] = pd.to_datetime(df['Início dos relatórios'])
df['Término dos relatórios'] = pd.to_datetime(df['Término dos relatórios'])

# Chronological Sorting and Index Reset
df_sorted = df.sort_values(by='Início dos relatórios')
df_sorted.reset_index(drop=True, inplace=True)
```

## DATA CLEANING

In this section we start identifying inconsistencies accross our DataFrame, the steps include:

1. **Removing redundancy of identical columns.**
2. **Adressing missing and irrelevant data via filtering the outlier age group.**
3. **Retrieving summary statistics to inspect for aditional problems.**
4. **Finally, filtering out ads with null expenditure.**

```python
# The name of the ad is not really relevant
df_sorted = df_sorted.drop('Nome do anúncio', axis=1)

#There is no need for the end of analysis column since the ads are grouped daily, so I am dropping from the DataFrame
df_sorted = df_sorted.drop('Término dos relatórios', axis=1)

# Check for missing values
missing_values = df_sorted.isnull().sum()

# I have no interest in analysing missclicks from now on, so we are filtering out the 65+ group
df_sorted = df_sorted[~df_sorted['Idade'].isin(['65+', 'Unknown'])]

# Engagement metric had 900 missing values, so we are dropping it
df_sorted = df_sorted.drop('Engajamento com a Página', axis=1)
```
### Now I'll take a look at types and statistics, since duplicates or unique values aren't really important for this analysis

```python
summary_stats = df_sorted.describe()

# Removing the ads that didnt really got to spend money
df_sorted = df_sorted[df_sorted['Valor usado (BRL)'] >= 0.19]

# Reassingning our DataFrame for the next step
df_clean = df_sorted
```

## DATA PROCESSING

In this step we will add further conditions to our data, in order to find underlying trends:

1. **Deaggregate and transform age ranges.**
2. **Group data by unique days, instead of repeated dates.**
3. **Create cost per result columns.**
4. **Create columns for week, month and year seasonality labels.**

```python
# Let's unpack our age range into numerical boundaries
df_clean[['Age Lower Bound', 'Age Upper Bound']] = df_clean['Idade'].str.split('-', expand=True).astype(int)

# Time to aggregate everything
df_clean = df_clean.groupby('Início dos relatórios').agg({
    'Alcance': 'sum',
    'Impressões': 'sum',
    'Cliques (todos)': 'sum',
    'Valor usado (BRL)': 'sum',
    'Age Lower Bound': 'mean',
    'Age Upper Bound': 'mean'
}).reset_index()

# New names!
df_clean.rename(columns={
    'Início dos relatórios': 'Day',
    'Alcance': 'Reach',
    'Impressões': 'Impressions',
    'Cliques (todos)': 'Clicks',
    'Valor usado (BRL)': 'Investment (BRL)',
    'Age Lower Bound': 'Avg Youngest Client',
    'Age Upper Bound': 'Avg Oldest Client'
}, inplace=True)

# Converting the average ages to integer type
df_clean['Avg Youngest Client'] = df_clean['Avg Youngest Client'].astype(int)
df_clean['Avg Oldest Client'] = df_clean['Avg Oldest Client'].astype(int)

# Rounding up monetary expenditures
df_clean['Investment (BRL)'] = df_clean['Investment (BRL)'].round(2)
```

### CREATING NEW COLUMNS

```python
# Calculate Cost per Reach
df_clean['Cost per Reach'] = df_clean['Investment (BRL)'] / df_clean['Reach']

# Calculate Cost per Impression
df_clean['Cost per Impression'] = df_clean['Investment (BRL)'] / df_clean['Impressions']

# Calculate Cost per Click
df_clean['Cost per Click'] = df_clean['Investment (BRL)'] / df_clean['Clicks']

# Replace any infinite or NaN values resulting from division by zero with zero
df_clean.replace([np.inf, -np.inf, np.nan], 0, inplace=True)

# Rounding again
df_clean['Cost per Reach'] = df_clean['Cost per Reach'].round(2)
df_clean['Cost per Impression'] = df_clean['Cost per Impression'].round(2)
df_clean['Cost per Click'] = df_clean['Cost per Click'].round(2)
```

### ADRESSING SEASONALITY

1) **Weekly**
```python
df_clean['Seasonality (week)'] = df_clean['Day'].dt.day_name()
```

2) **Monthly**

```python
# Create a holidays dictionary for Brazil for the years 2022-2023
br_holidays = holidays.Brazil(years=[2022, 2023])

# Define a function to determine the label for each day
def label_day(row):
    date = row['Day']
    day_of_week = date.weekday()
    month = date.month
    year = date.year
   
# Check if the date is a holiday or a Sunday
    if date in br_holidays or day_of_week == 6:
        return 'Holiday'
    
# Check for Advance Pay days (19th to 21st)
    if 19 <= date.day <= 21:
        return 'Advance Pay'

# Calculate the fifth business day of the month
    fifth_business_day = 5
    business_days_counted = 0
    current_date = pd.Timestamp(year=year, month=month, day=1)
    
# Considering Saturday as a business day
    while business_days_counted < fifth_business_day:
        if current_date.weekday() < 6:  
            business_days_counted += 1
        current_date += pd.Timedelta(days=1)
    
#Payday logic (28th of previous month to fifth business day of current month)
    if (date.day >= 28 and month == (date - pd.Timedelta(days=1)).month) or (date < current_date):
        return 'Payday'

# Default to Regular Day
    return 'Regular Day'

# Apply the function to each row
df_clean['Seasonality (month)'] = df_clean.apply(label_day, axis=1)
```

3) **Yearly**

```python
# Helper function to determine the season based on the month
def get_season(date):
    month = date.month
    
# Define the months for each season in the Southern Hemisphere

    if month in [12, 1, 2]:
        return 'Summer'
    elif month in [3, 4, 5]:
        return 'Autumn'
    elif month in [6, 7, 8]:
        return 'Winter'
    elif month in [9, 10, 11]:
        return 'Spring'

# Helper function to label special periods
def label_special_periods(date):
    month = date.month
    day = date.day

# Define special periods

    if (date.month == 12 and date.day >= 19) or (date.month == 1 and date.day <= 6):
        return 'Christmas'
    if date.month == 2 and (date.day >= 19 and date.day <= 25):  # Approximate range for Carnival
        return 'Carnival'
    if month == 4 and day >= 14 and day <= 21:  # Approximate range for Holy Week
        return 'Holy Week'
    if month == 6 and (day >= 8 and day <= 15):  # Week of June 12th
        return 'Namorados'
    if month == 7 and (day >= 15) or (month == 8 and day <= 1):  # July Vacation
        return 'July Vacation'
    if month == 9 and (day >= 5 and day <= 9):  # Near September 7th
        return "Brazil's Independence"
    if month == 10 and (day >= 10 and day <= 14):  # Around October 12th
        return "Aparecida's Day"
    if month == 11 and (day >= 24 and day <= 30):  # Approximate range for Thanksgiving
        return 'Thanksgiving'
    if month == 11 and (day >= 25) or (month == 12 and day <= 7):  # First installment of the 'Thirteenth Salary'
        return 'Thirteenth Salary'
      
# Default to regular season
    return get_season(date)
   
#Apply the function to each date in the DataFrame
df_clean['Seasonality (year)'] = df_clean['Day'].apply(label_special_periods)
```

## DATA ANALYSIS

### Now we make our last filter to retrieve the DataFrame of our interest:

```python
df_ready = df_clean[
    (df_clean['Seasonality(weekly)'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday'])) &
    (df_clean['Seasonality(montly)'] == 'Regular Day') &
    (df_clean['Seasonality(yearly)'].isin(['Summer', 'Autumn', 'Winter', 'Spring']))
]
```
Continues...

