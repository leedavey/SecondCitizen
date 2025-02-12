import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Touch the Moving Circle")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game variables
clock = pygame.time.Clock()
circle_radius = 50
score = 0
circles = []
speed = 3  # Speed of circle movement

# Function to create a new circle with movement direction
def new_circle():
    x = random.randint(circle_radius, WIDTH - circle_radius)
    y = random.randint(circle_radius, HEIGHT - circle_radius)
    dx = random.choice([-speed, speed])  # Direction on x-axis
    dy = random.choice([-speed, speed])  # Direction on y-axis
    return pygame.Rect(x - circle_radius, y - circle_radius, circle_radius*2, circle_radius*2), (dx, dy)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the player touched a circle
            for i, (circle, _) in enumerate(circles[:]):
                if circle.collidepoint(event.pos):
                    del circles[i]
                    score += 1
                    # Add a new circle when one is touched
#                    circles.append(new_circle())

    # Move the circles
    new_circles = []
    for circle, (dx, dy) in circles:
        # Update circle position
        new_circle = circle.move(dx, dy)
        
        # Bounce off the edges
        if new_circle.left < 0 or new_circle.right > WIDTH:
            dx = -dx
        if new_circle.top < 0 or new_circle.bottom > HEIGHT:
            dy = -dy
        
        new_circles.append((new_circle, (dx, dy)))
    
    circles = new_circles

    # Draw everything
    screen.fill(WHITE)
    
    # Ensure there's always at least one circle
    if not circles:
        circles.append(new_circle())
        circles.append(new_circle())
        circles.append(new_circle())
        circles.append(new_circle())

    for circle, _ in circles:
        pygame.draw.circle(screen, RED, circle.center, circle_radius)

    # Display score
    font = pygame.font.Font(None, 36)
    score_display = font.render(f"Score: {score}", True, GREEN)
    screen.blit(score_display, (10, 10))

    # Update display
    pygame.display.flip()

    # Control game speed
    clock.tick(60)

pygame.quit()
