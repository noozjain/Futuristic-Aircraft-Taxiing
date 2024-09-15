import pygame
import numpy as np
import random 

mid = []
a = {}
planes_created = True
planes_list = []
pygame.init()
pygame.display.set_caption("  KIAL (VOBL) Map")
window_icon = pygame.image.load("C:/Users/jainh/OneDrive/Desktop/Capstone/Implementation/Pygame Code/Window icon.png")
pygame.display.set_icon(window_icon)

screen = pygame.display.set_mode((1200,628))
img = pygame.image.load("C:/Users/jainh/OneDrive/Desktop/Capstone/Implementation/Final data/final_layout.png")
wide_body_img = pygame.image.load("C:/Users/jainh/Downloads/wide_body.png")
font = pygame.font.Font('freesansbold.ttf', 8)

x = 640 
y = 518
speed_x = 0.1
speed_y = 0.1

taxiway_nodes_1 = {'P_1': ((1011,142),(1046,173),(1063,166),(1024,124)), 'P_2': ((1047,173),(1047,511),(1063,511),(1063,166)),
                   
                 'Q_1': ((1008,107),(1030,90),(1082,147),(1071,157)), 'Q_2': ((1071,157),(1082,147),(1082,511),(1071,511)),

                 'P1': ((1063,166),(1071,166),(1071,185),(1063,185)), 'D3': ((1063,202),(1071,202),(1071,215),(1063,215)),

                 'N1_2':((1063,308),(1071,308),(1071,322),(1063,322)), 'N1_1':((1046,308),(1046,322),(978,322),(978,308)),

                 'N1':((993,215),(984,215),(984,308),(993,308)), 'M1': ((963,215),(978,215),(978,375),(963,375)),

                 'D2':((993,215),(1046,215),(1046,203),(993,203)), 'N2': ((998,203),(982,203),(982,142),(998,142)),

                 'M2': ((977,203),(963,203),(963,142),(977,142)), 'C2': ((963,182),(963,196),(897,196),(897,182)),

                 'B1_1': ((898,142),(878,142),(878,201),(898,201)), 'D1_1': ((963,215),(877,215),(877,203),(963,203)),

                 'D1_2': ((877,213),(877,194),(800,194),(800,213)), 'B': ((1011,142),(1024,124),(772,124),(772,142)),

                 'H': ((180,526),(1100,526),(1100,511), (180,511)), 'B6': ((79,107),(93,107),(93,195), (79,195)),
                
                'K': ((249,107), (284,107),(273,127),(273,164) ,(258,164), (258,127)), 'B4': ((517,107), (555,107),(545,118), (542,173),(527,173), (527,118)),


                'B2': ((746,107),(771,107),(771,138), (765,149),(765,173), (753,173),(753,149), (746,138)),

                'A': ((79,90), (1029,90) ,(1008,107), (79,107)), 'L_small': ((258,164),(273,164),(273,173), (258,173)),

                'L': ((258,173),(258,195),(800,195),(800,173)),
                
                'N_runway': ((80,40),(80,56), (1022,56),(1022,40)), 'S_runway':((180,573),(180,560),(1120,560),(1120,573)),
                
                'M3': ((962,107),(962,124),(983,124),(983,107)), 'B1_2': ((874,107),(874,124),(904,124),(904,107)),

                'G4': ((646,511),(646,491),(672,491), (672,511)), 'G': ((672,491), (672,504), (1047,504),(1047,491)),

                'G1': ((1120,526), (1120,491), (1100,491), (1100,526)), 'C1': ((878,173), (878,194), (800,194), (800,173))

                 }

taxiway_nodes_2 = {'A11': ((80,90), (100,90), (100,77),(80,77)), 'A10':((223,90),(247,90),(247,77),(223,77)) ,
                 
                 'A9': ((263,90),(302,90),(302,77),(263,77)), 'A8' : ((388,90), (433,90), (433,77),(388,77)),

                 'A7': ((479,90),(514,90),(514,77),(479,77)), 'A6': ((585,90),(623,90),(623,77),(585,77)), 

                 'A5': ((692,90),(727,90),(727,77),(692,77)), 'A4': ((728,90),(743,90),(743,77),(728,77)), 

                 'A2': ((985,90),(1001,90),(1001,77),(985,77)), 'A1': ((1008,90),(1022,90),(1022,77),(1008,77)),

                 'H10': ((180,526),(195,526),(195,537),(180,537)), 'H9':((198,526),(215,526),(215,537),(198,537)),
                 
                 'H8': ((325,526),(343,526),(343,537),(325,537)), 'H7' : ((462,526),(496,526),(496,537),(462,537)),
                 
                 'H6': ((581,526),(615,526),(615,537),(581,537)), 'H5': ((685,526),(718,526),(718,537),(685,537)),
                 
                 'H4': ((803,526),(836,526),(836,537),(803,537)), 'H3': ((936,526),(956,526),(956,537),(936,537)),
                 
                 'H2': ((1084, 526),(1100,526),(1100,547),(1084, 547)), 'H1': ((1104,526),(1120,526),(1120,549),(1104,549)), }

#Function to plot the parking spots
# def parking_spots():
#      for i in range(275,755,10):
#           pygame.draw.circle(
#                screen,
#                (0,0,255),
#                (i,170),
#                2,
#           )

#Function to plot the taxiway polygons         
def drawpoly():
    count = 0
    for i in taxiway_nodes_1.values():
            pygame.draw.polygon(screen,(0,255,0),i, width = 1)
            count +=1
            if count == len(taxiway_nodes_1.values()):
                break
            else:
                continue

#Function to plot the taxiway polygons attached to runway for a different color
def drawline_runway_taxiway():
    count = 0
    for i in taxiway_nodes_2.values():
            pygame.draw.polygon(screen,(255,0,0),i, width = 1)
            count +=1
            if count == len(taxiway_nodes_1.values()):
                break
            else:
                continue

#Function to plot the midline of each polygon
def middle_line():
    for i in taxiway_nodes_1.values():
        x_min = 10000
        x_max = 0
        y_min = 10000
        y_max = 0
        for j in i:
            if j[0]<x_min:
                x_min = j[0]
            if j[0] > x_max:
                x_max = j[0]
            if j[1]<y_min:
                y_min = j[1]
            if j[1] > y_max:
                y_max = j[1]

        mid.append((x_min,((x_min+x_max)//2), x_max, y_min, ((y_min+y_max)//2),y_max))
    count = 0
    for i in taxiway_nodes_1.keys():
        a.update({i:mid[count]})
        count +=1
        
    return mid,a
      
#Function to find the minimum and maximum x and y coordinate for each taxiway
def max_min():
    # List to store the results
    min_max_list = []

    # Iterate over the dictionary items
    for key, coords in taxiway_nodes_1.items():
        # Separate x and y coordinates
        x_values = [tup[0] for tup in coords]
        y_values = [tup[1] for tup in coords]
        
        # Find max and min for each axis
        max_x = max(x_values)
        min_x = min(x_values)
        max_y = max(y_values)
        min_y = min(y_values)
        
        # Append the result as a tuple to the list
        min_max_list.append((key, (min_x, max_x), (min_y, max_y)))

    # Output the list
    # print(min_max_list)       
    # print(len(min_max_list))   

# Function to check if a point is inside a polygon using the ray-casting algorithm
def is_point_in_polygon(point, polygon):
    x, y = point
    n = len(polygon)
    inside = False

    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y

    return inside

# Function to check if a point is on the edge of a polygon
def is_point_on_edge(point, polygon, tolerance=3):
    x, y = point
    n = len(polygon)
    
    for i in range(n):
        p1x, p1y = polygon[i]
        p2x, p2y = polygon[(i + 1) % n]
        
        # Check if the point is near the line segment
        if p1x == p2x:  # Vertical line
            if min(p1y, p2y) <= y <= max(p1y, p2y) and abs(x - p1x) <= tolerance:
                return True
        elif p1y == p2y:  # Horizontal line
            if min(p1x, p2x) <= x <= max(p1x, p2x) and abs(y - p1y) <= tolerance:
                return True
        else:  # General case
            if min(p1x, p2x) <= x <= max(p1x, p2x) and min(p1y, p2y) <= y <= max(p1y, p2y):
                # Calculate the distance from point to the line
                dist = abs((p2y - p1y) * x - (p2x - p1x) * y + p2x * p1y - p2y * p1x) / (
                    ((p2y - p1y) ** 2 + (p2x - p1x) ** 2) ** 0.5
                )
                if dist <= tolerance:
                    return True

    return False

# Function to identify the location of a point
def identify_location(point):
    # Check if the point is inside any polygon
    for name, polygon in taxiway_nodes_1.items():
        if is_point_in_polygon(point, polygon):
            print(f"Inside {name}") 
            return point
    
    # Check if the point is on the edge of any polygon
    for name, polygon in taxiway_nodes_1.items():
        if is_point_on_edge(point, polygon):
            print(f"On the edge of {name}")
            return point,name
    
    return "Outside all regions"

#Function to update the location of plane on taxiway and get them to move
def update_plane_location(parking_gate):
    pygame.draw.circle(screen,(255,0,0), parking_gate, 4)

    identify_location(parking_gate)
    

    # x_location= identify_location(parking_gate)[0]
    # y_location = identify_location(parking_gate)[1]


    # print(x_location, y_location)

#Function to determine a collision
def collision():
    pass

#Function to initialise number of planes (try to randomise across dep and arr)
def create_planes(n):
    for i in range(0,n):
        x = random.randint(275,755)
        y = 170
        pygame.draw.circle(screen, (255,67,0), (x, y),2)
        print(f"Drew circle at ({x}, {y})")
        planes_list.append((x,y))
    return planes_list


#Fuction to end planes journey once it reaches gate
def start_end():
    pass

#Function to move plane from initial gate to taxiway cntreline
def move_from_gate(gate):
    middle_line()
    speed = 0.5
    y_mid = a['L'][4]
    for i in gate:
        x = i[0]
        y = i[1]
        while y!=y_mid:
            if y<y_mid:
                y+=speed
                pygame.draw.circle(screen, (255,0,0), (x,y),4)
            if y>y_mid:
                y-=speed
                pygame.draw.circle(screen, (255,0,0), (x,y),4)
            # y+=speed
    return y


running = True 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            location = identify_location(mouse_pos)
            # update_plane_location(location)           
            print(location)

        
    # screen.fill((0,0,0))
    
    # move_from_gate((366,176))

    middle_line()
    # print(a)
    # print(mid)

    for i in mid:
        if i[2]-i[0] > i[5]-i[3]:
            pygame.draw.line(
                screen, (0,0,255),
                (i[0],i[4]) , (i[2],i[4]),2,
            )
        else:
            pygame.draw.line(
            screen, (255,0,0),
            (i[1],i[3]) , (i[1],i[5]),2,
        )

        # text = font.render(i, True, (0,255,233))

        # screen.blit(text, taxiway_nodes_1[i][0])
    
    # test_plane = pygame.draw.circle(screen, (255,0,0), (600,450), 4)
    # print(identify_location((600,450)))
    # trial_movement()


    # if x>1100:
    #     # change_x+=1
    #     x-=speed_x

    # if x<84:
    #     # change_x = -1
    #     x+=speed_x
    # x+=speed_x
    # pygame.draw.circle(screen, (255,0,0), (x,y),4)
    drawpoly()
    drawline_runway_taxiway()
    max_min()
    # parking_spots()
    if planes_created:
        b = create_planes(5)
        move_from_gate(b)
        planes_created = False
    # update_plane_location((1063,511))

    
    pygame.display.update()
