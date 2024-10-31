# game.py
import pygame
import xml.etree.ElementTree as ET
import random
from collections import deque

# Import the connected_taxiways from ConTax.py
from ConTax import connected_taxiways

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1200, 900
INFO_PANEL_WIDTH = 300  # Width of the info panel on the right
screen = pygame.display.set_mode((WIDTH + INFO_PANEL_WIDTH, HEIGHT))
pygame.display.set_caption("KML Map Viewer with Aircraft Data")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
GRAY = (30, 30, 30)

# Parse the KML file
file_path = 'Map-final/resources/FINAL.kml'  # Update the file path as needed
tree = ET.parse(file_path)
root = tree.getroot()

# Define the KML namespace
namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

# Lists to store the coordinates of points (locations) and lines (map paths)
locations = []
lines = []

# Extract points (locations) and lines with their names
for placemark in root.findall('.//kml:Placemark', namespace):
    name_elem = placemark.find('kml:name', namespace)
    name = name_elem.text.strip() if name_elem is not None else None

    point = placemark.find('.//kml:Point/kml:coordinates', namespace)
    if point is not None:
        coords = point.text.strip().split(',')
        lon, lat = float(coords[0]), float(coords[1])
        locations.append({'name': name, 'coordinates': (lon, lat)})

    line_string = placemark.find('.//kml:LineString/kml:coordinates', namespace)
    if line_string is not None:
        line_coords = line_string.text.strip().split()
        path = []
        for coord in line_coords:
            lon, lat, _ = map(float, coord.split(','))
            path.append((lon, lat))
        lines.append({'name': name, 'path': path})

# Find the bounds of the data
all_coords = [loc['coordinates'] for loc in locations] + [coord for line in lines for coord in line['path']]
lon_min = min(coord[0] for coord in all_coords)
lon_max = max(coord[0] for coord in all_coords)
lat_min = min(coord[1] for coord in all_coords)
lat_max = max(coord[1] for coord in all_coords)

# Add a small margin to the bounds
margin = 0.1
lon_range = lon_max - lon_min
lat_range = lat_max - lat_min
lon_min -= lon_range * margin
lon_max += lon_range * margin
lat_min -= lat_range * margin
lat_max += lat_range * margin

def convert_coords(lon, lat):
    """Converts geographical coordinates to pixel coordinates on the display."""
    x = (lon - lon_min) / (lon_max - lon_min) * WIDTH
    y = HEIGHT - (lat - lat_min) / (lat_max - lat_min) * HEIGHT
    return int(x), int(y)

# Function to interpolate paths
def interpolate_path(path, num_points=10):
    """Interpolates the path to add more points for smoother movement."""
    if len(path) < 2:
        return path
    interpolated = []
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        segment = [start.lerp(end, t / num_points) for t in range(num_points)]
        interpolated.extend(segment)
    interpolated.append(path[-1])
    return interpolated

# Convert all lines to pixel coordinates and interpolate
for line in lines:
    pixel_path = [pygame.math.Vector2(convert_coords(lon, lat)) for lon, lat in line['path']]
    interpolated_pixel_path = interpolate_path(pixel_path, num_points=10)
    line['pixel_path'] = interpolated_pixel_path

# Build a mapping from line names to pixel paths
line_name_to_pixel_path = {}
for line in lines:
    if line['name']:
        line_name_to_pixel_path[line['name']] = line['pixel_path']

# Initialize Pygame font
pygame.font.init()
font = pygame.font.SysFont(None, 24)

# Define the Aircraft class
class Aircraft:
    def __init__(self, name, start_position, path):
        self.name = name  # Assign a name to the aircraft
        self.position = start_position.copy()  # Copy to avoid modifying the original
        self.path = path
        self.path_index = 0  # Start from the first point
        self.speed = 1.0  # Adjust speed for visibility

    def move(self):
        if self.path_index < len(self.path) - 1:
            next_position = self.path[self.path_index + 1]
            direction = (next_position - self.position)
            distance = direction.length()
            if distance == 0:
                self.position = next_position
                self.path_index += 1
            elif distance <= self.speed:
                self.position = next_position
                self.path_index += 1
            else:
                direction = direction.normalize()
                self.position += direction * self.speed
        else:
            # Aircraft has reached the end of its path
            pass

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.position.x), int(self.position.y)), 5)
        # Display aircraft name near the aircraft
        text_surface = font.render(self.name, True, WHITE)
        screen.blit(text_surface, (self.position.x + 10, self.position.y - 10))

# Build a combined graph that considers both logical and spatial connections
def build_combined_graph(connected_taxiways, line_name_to_pixel_path):
    graph = {}
    threshold = 10.0  # Adjusted threshold in pixels

    for taxiway, connections in connected_taxiways.items():
        if taxiway not in line_name_to_pixel_path:
            continue  # Skip taxiways not present in the KML file
        graph[taxiway] = set()
        path1 = line_name_to_pixel_path[taxiway]
        endpoints1 = [path1[0], path1[-1]]
        for conn in connections:
            if conn not in line_name_to_pixel_path:
                continue  # Skip connections not present in the KML file
            path2 = line_name_to_pixel_path[conn]
            endpoints2 = [path2[0], path2[-1]]
            # Check if taxiways are physically connected
            connected = False
            for point1 in endpoints1:
                for point2 in endpoints2:
                    if point1.distance_to(point2) < threshold:
                        connected = True
                        break
                if connected:
                    break
            if connected:
                graph[taxiway].add(conn)
    return graph

# Build the combined graph
graph = build_combined_graph(connected_taxiways, line_name_to_pixel_path)

def generate_taxiway_path(graph, start_taxiway, target_taxiways):
    visited = set()
    queue = deque()
    queue.append((start_taxiway, [start_taxiway]))
    visited.add(start_taxiway)
    while queue:
        current_taxiway, path = queue.popleft()
        if current_taxiway in target_taxiways:
            return path
        for neighbor in graph.get(current_taxiway, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return []  # No path found

def initialize_aircraft(locations, lines, max_aircrafts=8):
    aircrafts = []
    line_name_to_pixel_path = {line['name']: line['pixel_path'] for line in lines if line['name']}
    # Update L-paths to match your KML data
    l_paths = {name: line_name_to_pixel_path[name] for name in ['L1_LEFT', 'L2_LEFT', 'L3_LEFT'] if name in line_name_to_pixel_path}
    available_paths = list(l_paths.keys())
    all_taxiways = list(graph.keys())

    # Map L-paths to connected taxiways for assigning reachable taxiways
    l_path_connections = {}
    for l_path in l_paths.keys():
        l_path_connections[l_path] = graph.get(l_path, set())

    for i, loc in enumerate(locations[:max_aircrafts]):
        gate_position = pygame.math.Vector2(convert_coords(*loc['coordinates']))
        assigned_path_name = available_paths[i % len(available_paths)]
        assigned_path = l_paths[assigned_path_name]
        gate_x, gate_y = gate_position.x, gate_position.y

        # Find the point on the L-path closest in x to the gate
        selected_point = min(assigned_path, key=lambda pt: abs(pt.x - gate_x))
        vertical_down_point = pygame.math.Vector2(gate_x, selected_point.y)
        combined_path = [gate_position.copy(), vertical_down_point.copy()]
        if vertical_down_point != selected_point:
            combined_path.append(selected_point.copy())

        # Assign taxiways connected to the starting L-path
        connected_taxiways = l_path_connections.get(assigned_path_name, set())
        if not connected_taxiways:
            print(f"No connected taxiways found for {assigned_path_name}")
            continue

        # For testing purposes, let's assign all taxiways to each aircraft to ensure coverage
        assigned_taxiways = set(all_taxiways)

        # Generate taxiway path
        taxiway_path_names = generate_taxiway_path(graph, assigned_path_name, assigned_taxiways)
        if not taxiway_path_names:
            print(f"Aircraft {i+1} could not find a path to assigned taxiways.")
            continue

        # Append the pixel paths of the taxiways along the route
        for taxiway in taxiway_path_names:
            if taxiway in line_name_to_pixel_path:
                taxiway_pixel_path = [vec.copy() for vec in line_name_to_pixel_path[taxiway]]
                # Ensure paths connect smoothly
                if combined_path[-1].distance_to(taxiway_pixel_path[0]) < 10.0:
                    combined_path.extend(taxiway_pixel_path[1:])
                else:
                    combined_path.extend(taxiway_pixel_path)
            else:
                print(f"Warning: Taxiway {taxiway} not found in line_name_to_pixel_path")

        # Assign a name to the aircraft
        aircraft_name = f"Aircraft_{i+1}"
        aircraft = Aircraft(name=aircraft_name, start_position=combined_path[0], path=combined_path)
        aircrafts.append(aircraft)

    return aircrafts

# Initialize aircraft at gate positions, moving along assigned taxiways
aircrafts = initialize_aircraft(locations, lines, max_aircrafts=8)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen at the beginning of each frame
    screen.fill(BLACK)

    # Draw the lines (map paths)
    for line in lines:
        path = line['pixel_path']
        if len(path) > 1:
            pygame.draw.lines(screen, BLUE, False, path, 3)

    # Visualize endpoints for debugging
    for line in lines:
        path = line['pixel_path']
        if path:
            # Start point in green
            pygame.draw.circle(screen, (0, 255, 0), (int(path[0].x), int(path[0].y)), 3)
            # End point in red
            pygame.draw.circle(screen, (255, 0, 0), (int(path[-1].x), int(path[-1].y)), 3)

    # Draw the points (locations)
    for loc in locations:
        x, y = convert_coords(*loc['coordinates'])
        dash_length = 8  # Length of the dash
        dash_thickness = 2  # Thickness of the dash
        pygame.draw.line(screen, RED, (x, y - dash_length // 2), (x, y + dash_length // 2), dash_thickness)

    # Move and draw aircraft
    for aircraft in aircrafts:
        aircraft.move()
        aircraft.draw(screen)

    # Draw the info panel
    info_panel_rect = pygame.Rect(WIDTH, 0, INFO_PANEL_WIDTH, HEIGHT)
    pygame.draw.rect(screen, GRAY, info_panel_rect)

    # Display aircraft data in the info panel
    y_offset = 10
    for aircraft in aircrafts:
        name = aircraft.name
        pos = aircraft.position
        text_surface = font.render(f"{name}: ({pos.x:.1f}, {pos.y:.1f})", True, WHITE)
        screen.blit(text_surface, (WIDTH + 10, y_offset))
        y_offset += 30  # Adjust spacing between lines

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
