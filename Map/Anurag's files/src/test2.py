import matplotlib.pyplot as plt
from xml.etree import ElementTree as ET

# Load and parse the KML file
kml_file_path = "/Users/anuragvallur/Developer/Machine Learning/capstone/resources/proper2.kml"  # Replace with your KML file path
tree = ET.parse(kml_file_path)
root = tree.getroot()

# Extract all Placemark elements
placemarks = root.findall(".//{http://www.opengis.net/kml/2.2}Placemark")

# Function to plot KML coordinates based on placemarks
def plot_kml_coordinates(placemarks):
    plt.figure(figsize=(12.5,6.54))
    plt.style.use('dark_background')
    
    # Loop through each Placemark and plot its points as a line
    for placemark in placemarks:
        coords = []
        for coord in placemark.findall(".//{http://www.opengis.net/kml/2.2}coordinates"):
            coords_text = coord.text.strip()
            # Split the coordinates into lon, lat
            for coord_pair in coords_text.split():
                lon_lat_alt = coord_pair.split(',')
                lon_lat = list(map(float, lon_lat_alt[:2]))  # Only take lon, lat
                coords.append(lon_lat)
        
        if coords:
            # Extract lon and lat for current placemark
            lons, lats = zip(*coords)
            # Plot line connecting points within this placemark
            plt.plot(lons, lats, marker='o', linestyle='-', markersize=1, label='Path', color='w')
    
    # Add labels and title
    # plt.title("KML Points and Lines (Separate by Placemark)")
    # plt.xlabel("Longitude")
    # plt.ylabel("Latitude")
    # plt.grid(True)
    plt.axis("off")
    plt.savefig('gates.png',bbox_inches="tight")
    plt.show()


# Call the function to plot the coordinates
plot_kml_coordinates(placemarks)
# plt.figure(figsize = (12.5,6.54))