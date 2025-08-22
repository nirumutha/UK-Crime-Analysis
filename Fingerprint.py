import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import contextily as cx

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
print("Data ready for multi-map analysis.")

# --- Part 3: Filter for Oxford-specific data ---
thames_valley_df = crime_df[crime_df['Falls within'] == 'Thames Valley Police'].copy()
oxford_lon_bounds = [-1.32, -1.18]
oxford_lat_bounds = [51.72, 51.79]
oxford_df = thames_valley_df[
    (thames_valley_df['Longitude'] >= oxford_lon_bounds[0]) &
    (thames_valley_df['Longitude'] <= oxford_lon_bounds[1]) &
    (thames_valley_df['Latitude'] >= oxford_lat_bounds[0]) &
    (thames_valley_df['Latitude'] <= oxford_lat_bounds[1])
    ].copy()


# --- Part 4: Generate a Hotspot Map for a Specific Crime ---
# We will create a function to avoid repeating code.

def create_hotspot_map(data, crime_type, color_map):
    """Filters data for a crime type and generates a hotspot map image."""
    print(f"Generating hotspot map for: {crime_type}...")

    # Filter for the specific crime
    crime_specific_df = data[data['Crime type'] == crime_type]

    if crime_specific_df.empty:
        print(f"No data found for {crime_type}, skipping map.")
        return

    # Set up the plot
    fig, ax = plt.subplots(figsize=(12, 12))

    # Create the heatmap
    sns.kdeplot(
        data=crime_specific_df, x='Longitude', y='Latitude',
        fill=True, cmap=color_map, thresh=0.05, alpha=0.6, ax=ax
    )

    # Add the map background
    cx.add_basemap(ax, crs="EPSG:4326", source=cx.providers.OpenStreetMap.Mapnik)

    # Improve aesthetics
    ax.set_title(f'{crime_type} Hotspots in Oxford', fontsize=18, weight='bold')
    ax.axis('off')

    # Save the plot to a unique PNG file
    image_filename = f'oxford_hotspot_{crime_type.lower().replace(" ", "_")}.png'
    plt.savefig(image_filename, dpi=300, bbox_inches='tight')
    plt.close()  # Close the figure to free up memory
    print(f" -> Saved map as '{image_filename}'")


# --- Part 5: Create the Three Maps ---
create_hotspot_map(oxford_df, 'Burglary', 'Reds')
create_hotspot_map(oxford_df, 'Shoplifting', 'Blues')
create_hotspot_map(oxford_df, 'Public order', 'Greens')

print("\nProcess finished. All three maps have been saved.")