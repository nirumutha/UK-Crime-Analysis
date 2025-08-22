import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Part 1: Loading the Data ---
main_folder_path = '/Users/nirajmutha/Downloads/Crime'
print(f"Searching for CSV files in: {main_folder_path}...")

all_csv_files = []
# (Error handling for file path not found)
try:
    for root, dirs, files in os.walk(main_folder_path):
        for file in files:
            if file.endswith('.csv'):
                full_path = os.path.join(root, file)
                all_csv_files.append(full_path)
except FileNotFoundError:
    print(f"Error: Directory not found at '{main_folder_path}'. Please check the path.")
    exit()

print(f"Found {len(all_csv_files)} CSV files.")

if all_csv_files:
    df_list = [pd.read_csv(file) for file in all_csv_files]
    crime_df = pd.concat(df_list, ignore_index=True)
    print("Successfully combined all raw files.")
else:
    print("No CSV files found.")
    exit()

# --- Part 2: Cleaning the Data ---
print("\nStarting data cleaning...")
crime_df.drop(columns=['Context', 'Crime ID'], inplace=True)
crime_df.dropna(subset=['Longitude', 'Latitude'], inplace=True)
# FIX: Added format='%Y-%m' to make date conversion more efficient and remove the warning.
crime_df['Month'] = pd.to_datetime(crime_df['Month'], format='%Y-%m')
print("Data cleaning complete! ✨")

# --- Part 3: Preparing Data for the Combined Chart ---
print("\nPreparing data for visualization...")
# Get the top 5 crime types for each police force
top_crimes_per_force = crime_df.groupby('Falls within')['Crime type'].apply(lambda x: x.value_counts().nlargest(5).index)

# Create a single list of all unique top crime types
unique_top_crimes = pd.Index(top_crimes_per_force.explode().unique())

# Filter the main DataFrame to only include these top crimes
plot_df = crime_df[crime_df['Crime type'].isin(unique_top_crimes)]

# --- Part 4: The New, Improved Visualization ---
print("Generating combined crime profile chart...")

plt.figure(figsize=(14, 10)) # Adjusted figure size for clarity
sns.set_style("whitegrid")

# Create a count plot that automatically groups by police force
ax = sns.countplot(
    data=plot_df,
    y='Crime type',
    hue='Falls within',
    palette='viridis',
    order=plot_df['Crime type'].value_counts().index # Order bars by overall frequency
)

# Set title and labels
plt.title('Comparison of Top Crime Types Across Police Forces', fontsize=16, weight='bold')
plt.xlabel('Total Crime Count (May 2023 - May 2025)', fontsize=12)
plt.ylabel('Crime Type', fontsize=12)
plt.legend(title='Police Force')

plt.tight_layout()
plt.show()

print("\nProcess finished.")