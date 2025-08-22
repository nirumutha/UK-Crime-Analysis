import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Part 1 & 2: Loading and Cleaning Data ---
# This section remains the same to prepare your DataFrame.
main_folder_path = '/Users/nirajmutha/Downloads/Crime'
print("Loading and cleaning data...")

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
print("Data ready for new analysis.")


# --- Part 3: Calculate the "Unsolved" Rate ---
print("Calculating unsolved crime rates...")

# The key category for an "unsolved" crime.
UNSOLVED_CATEGORY = 'Investigation complete; no suspect identified'

# Group by force and crime type, then calculate the rate.
# First, count total crimes in each group.
total_crimes = crime_df.groupby(['Falls within', 'Crime type']).size()
# Next, count unsolved crimes in each group.
unsolved_crimes = crime_df[crime_df['Last outcome category'] == UNSOLVED_CATEGORY].groupby(['Falls within', 'Crime type']).size()

# Combine the two series and calculate the rate.
outcome_df = pd.DataFrame({'Total': total_crimes, 'Unsolved': unsolved_crimes}).fillna(0)
outcome_df['Unsolved Rate (%)'] = (outcome_df['Unsolved'] / outcome_df['Total']) * 100
outcome_df.reset_index(inplace=True)


# --- Part 4: Visualize the Results ---
print("Generating charts...")

# Focus on the same key crimes for a clear comparison.
crimes_to_compare = [
    'Violence and sexual offences',
    'Bicycle theft',
    'Shoplifting',
    'Burglary'
]
plot_data = outcome_df[outcome_df['Crime type'].isin(crimes_to_compare)]

# Create the faceted plot with the warning fix
g = sns.catplot(
    data=plot_data,
    x='Unsolved Rate (%)',
    y='Falls within',
    col='Crime type',
    kind='bar',
    hue='Falls within', # FIX: Assign the y-variable to hue
    legend=False,       # FIX: Disable the automatic legend
    col_wrap=2,
    sharex=False,
    palette='plasma',
    height=4,
    aspect=1.5
)

g.fig.suptitle('Percentage of Unsolved Crimes by Type', y=1.03, fontsize=16, weight='bold')
g.set_axis_labels('Unsolved Rate (%)', 'Police Force')
g.set_titles("Crime Type: {col_name}")

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.show()