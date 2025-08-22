import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Part 1 & 2: Loading and Cleaning Data ---
main_folder_path = '/Users/nirajmutha/Downloads/Crime'
print("Loading and cleaning data...")

# (This section is the same as before to load and clean crime_df)
all_csv_files = []
try:
    for root, dirs, files in os.walk(main_folder_path):
        for file in files:
            if file.endswith('.csv'):
                full_path = os.path.join(root, file)
                all_csv_files.append(full_path)
except FileNotFoundError:
    print(f"Error: Directory not found at '{main_folder_path}'.")
    exit()

if not all_csv_files:
    print("No CSV files found.")
    exit()

df_list = [pd.read_csv(file) for file in all_csv_files]
crime_df = pd.concat(df_list, ignore_index=True)

crime_df.drop(columns=['Context', 'Crime ID'], inplace=True, errors='ignore')
crime_df.dropna(subset=['Longitude', 'Latitude'], inplace=True)
crime_df['Month'] = pd.to_datetime(crime_df['Month'], format='%Y-%m')
print("Data ready for seasonality analysis.")


# --- Part 3: Calculate Seasonal Crime Rates ---
print("Analyzing seasonal trends for new crime types...")
population_data = {
    'Thames Valley Police': 2340000,
    'Cambridgeshire Constabulary': 678600,
    'Metropolitan Police Service': 9000000
}

# Add month number and year columns for grouping
crime_df['Month_Num'] = crime_df['Month'].dt.month
crime_df['Year'] = crime_df['Month'].dt.year

# CHANGE: Updated the list of crimes to analyze
crimes_to_analyze = ['Shoplifting', 'Bicycle theft']
seasonal_df = crime_df[crime_df['Crime type'].isin(crimes_to_analyze)]

# Calculate the monthly counts for each crime type and force
seasonal_counts = seasonal_df.groupby(['Falls within', 'Crime type', 'Year', 'Month_Num']).size().reset_index(name='Count')

# Now, get the average count for each month
avg_monthly_counts = seasonal_counts.groupby(['Falls within', 'Crime type', 'Month_Num'])['Count'].mean().reset_index()

# Normalize by population to get a rate
avg_monthly_counts['Population'] = avg_monthly_counts['Falls within'].map(population_data)
avg_monthly_counts['Avg Monthly Rate per 100k'] = (avg_monthly_counts['Count'] / avg_monthly_counts['Population']) * 100000

# --- Part 4: Visualization ---
print("Generating charts...")
sns.set_style("whitegrid")

# Create a faceted plot to show each crime type separately
g = sns.FacetGrid(avg_monthly_counts, col="Crime type", hue="Falls within", height=6, aspect=1.2, sharey=False, palette='viridis')
g.map(sns.lineplot, "Month_Num", "Avg Monthly Rate per 100k", linewidth=3, marker='o', markersize=8)
g.add_legend(title='Police Force')

# Improve the plot aesthetics
g.fig.suptitle('Seasonal Crime Rate Patterns', y=1.03, fontsize=16, weight='bold')
g.set_axis_labels("Month of the Year", "Avg. Incidents per 100k People")
g.set_titles("Crime Type: {col_name}")
g.set(xticks=range(1, 13))

# FIX: Adjust the plot to make space for the legend on the right
plt.subplots_adjust(right=0.85)

plt.show()