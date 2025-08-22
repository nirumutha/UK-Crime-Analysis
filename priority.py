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
print("Data ready for Oxford-specific analysis.")

# --- Part 3: Create the Diagnostic Dataset for Oxford ---
print("Building the priority matrix dataset for Oxford...")

# First, filter for Thames Valley Police
thames_valley_df = crime_df[crime_df['Falls within'] == 'Thames Valley Police'].copy()

# Define the geographic boundaries for Oxford
oxford_lon_bounds = [-1.32, -1.18]
oxford_lat_bounds = [51.72, 51.79]

# Now, filter for crimes that occurred within Oxford's boundaries
oxford_df = thames_valley_df[
    (thames_valley_df['Longitude'] >= oxford_lon_bounds[0]) &
    (thames_valley_df['Longitude'] <= oxford_lon_bounds[1]) &
    (thames_valley_df['Latitude'] >= oxford_lat_bounds[0]) &
    (thames_valley_df['Latitude'] <= oxford_lat_bounds[1])
].copy()

# Calculate total volume for each crime type in Oxford
total_crimes_oxford = oxford_df['Crime type'].value_counts()

# Calculate the unsolved rate for each crime type in Oxford
UNSOLVED_CATEGORY = 'Investigation complete; no suspect identified'
unsolved_crimes_oxford = oxford_df[oxford_df['Last outcome category'] == UNSOLVED_CATEGORY]['Crime type'].value_counts()
unsolved_rate_oxford = (unsolved_crimes_oxford / total_crimes_oxford * 100).fillna(0)

# Combine into a single DataFrame
priority_df_oxford = pd.DataFrame({
    'Total Volume': total_crimes_oxford,
    'Unsolved Rate (%)': unsolved_rate_oxford
}).reset_index()
priority_df_oxford.rename(columns={'index': 'Crime type'}, inplace=True)

# --- Part 4: Visualization ---
print("Generating the Crime Priority Matrix for Oxford...")

plt.figure(figsize=(14, 10))
sns.set_style("whitegrid")

# Create the scatter plot
ax = sns.scatterplot(
    data=priority_df_oxford,
    x='Total Volume',
    y='Unsolved Rate (%)',
    size='Total Volume',
    sizes=(100, 2000),
    palette='plasma',
    hue='Unsolved Rate (%)',
    legend=False
)

# Add labels to each point
for i, row in priority_df_oxford.iterrows():
    plt.text(row['Total Volume'] + 50, row['Unsolved Rate (%)'], row['Crime type'], fontsize=9)

# Add lines for the four quadrants
plt.axvline(priority_df_oxford['Total Volume'].median(), color='grey', linestyle='--')
plt.axhline(priority_df_oxford['Unsolved Rate (%)'].median(), color='grey', linestyle='--')

# Add quadrant labels
ax.text(0.98, 0.98, 'High Volume,\nHigh Unsolved Rate\n(CHRONIC PROBLEMS)', transform=ax.transAxes, ha='right', va='top', fontsize=12, weight='bold', color='red')
ax.text(0.02, 0.98, 'Low Volume,\nHigh Unsolved Rate\n(Niche Challenges)', transform=ax.transAxes, ha='left', va='top', fontsize=12)
ax.text(0.02, 0.02, 'Low Volume,\nLow Unsolved Rate\n(Well-Managed)', transform=ax.transAxes, ha='left', va='bottom', fontsize=12)
ax.text(0.98, 0.02, 'High Volume,\nLow Unsolved Rate\n(Effective Process)', transform=ax.transAxes, ha='right', va='bottom', fontsize=12)

# Set titles and labels
plt.title('Crime Priority Matrix for Oxford', fontsize=18, weight='bold')
plt.xlabel('Crime Volume (Number of Incidents)', fontsize=12)
plt.ylabel('Unsolved Rate (%)', fontsize=12)
plt.xlim(0, priority_df_oxford['Total Volume'].max() * 1.15) # Adjust x-axis limit
plt.ylim(0, 100)

plt.tight_layout()
plt.show()