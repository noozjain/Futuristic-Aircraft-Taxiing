import pygame



pygame.init()

screen = pygame.display.set_mode((1200,628))
img = pygame.image.load("C:/Users/jainh/OneDrive/Desktop/Final data/final_layout.png")
img1 = pygame.image.load("C:/Users/jainh/Downloads/aircraft.png")

x= 200
y = 99
change_x = 2
change_y = 2

taxiway_nodes = {'A10': (90,90), 'A9':(235,92), 'A8': (284,94), 'A7' : (411,95), 'A6': (499,98), 'A5': (605,100), 'A4': (711,97), 
                 'A3': (735,96), 'A2': (993,98), 'A1': (1016,99),
                 'H10': (187,526), 'H9':(207,527), 'H8': (335,529), 'H7' : (480,530), 'H6': (600,532), 'H5': (703,533), 'H4': (821,533), 
                 'H3': (947,534), 'H2': (1093, 537), 'H1': (1112,533)}

def moving_plane(x,y):
    pygame.draw.circle(
    screen,
    (255,0,0),
    (x,y),
    4,
    )
running = True 

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(pygame.transform.scale(img, (1200,628)), (0,0))

    # pygame.draw.circle(
    #     screen,
    #     (255,0,0),
    #     taxiway_nodes['a10'],
    #     4,
    # )
    for i in taxiway_nodes.keys():
        pygame.draw.circle (
            screen, 
            (89,123,34),
            taxiway_nodes[i],
            4,
        )

        
    if x<=88:
        change_x +=0.3
    if x>=1015:
        change_x-=0.3
    if x == 90:
        change_x = -x
        change_y -= 0.3
        y+=change_y
    
    x+=change_x
    # y += change_y
    moving_plane(x,y)


    pygame.display.update()
