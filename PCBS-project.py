import pygame

# Main variables
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
width_window, height_window = 500, 500  # Size of the graphic window size


# Create the window
pygame.init()
screen = pygame.display.set_mode((width_window, height_window), pygame.DOUBLEBUF)
screen.fill(BLACK)  #  fill it with black




# Draw the visual stimulus
def display_visual_stimulus():
    pygame.draw.circle(screen, WHITE, (width_window//2, height_window/2), 100, 0)
    pygame.display.flip()

#Display the auditory stimulus
def display_auditory_stimulus():
    print('\a')
    
def trial(number_visual,number_auditory):
    




# wait until the window is closed
done = False
while not done:
    pygame.time.wait(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
pygame.quit()
