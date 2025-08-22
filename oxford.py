import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import contextily as cx # Import the new library

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
print("Data ready for mapping.")


# --- Part 3: Filter for Overall Theft in Thames Valley ---
print("Filtering data for overall theft...")
thames_valley_df = crime_df[crime_df['Falls within'] == 'Thames Valley Police'].copy()

theft_categories = [
    'Bicycle theft', 'Shoplifting', 'Theft from the person', 'Other theft',
    'Burglary', 'Robbery', 'Vehicle crime'
]
theft_df = thames_valley_df[thames_valley_df['Crime type'].isin(theft_categories)]

# --- Part 4: Create and Save a Static Heatmap with Map Context ---
print("Generating static heatmap with map background...")

# Set up the plot
fig, ax = plt.subplots(figsize=(12, 12))

# Create the 2D density plot (heatmap) on the axis 'ax'
sns.kdeplot(
    data=theft_df,
    x='Longitude',
    y='Latitude',
    fill=True,
    cmap='rocket_r',
    thresh=0.05,
    alpha=0.6, # Made it slightly more transparent to see the map
    ax=ax
)

# Limit the plot to the Oxford area
oxford_lon_bounds = [-1.32, -1.18]
oxford_lat_bounds = [51.72, 51.79]
ax.set_xlim(oxford_lon_bounds)
ax.set_ylim(oxford_lat_bounds)

# ADDITION: Add the map background using contextily
# We tell it that our data is in the standard GPS format (EPSG:4326)
cx.add_basemap(ax, crs="EPSG:4326", source=cx.providers.OpenStreetMap.Mapnik)

# Improve aesthetics
ax.set_title('Overall Theft Hotspots in Oxford', fontsize=18, weight='bold')
ax.axis('off')

# Save the plot to a PNG file
image_filename = 'oxford_theft_hotspots_with_map.png'
plt.savefig(image_filename, dpi=300, bbox_inches='tight')

plt.show()

print(f"\nProcess finished. A new map image has been saved as '{image_filename}'")