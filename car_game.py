import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Game settings
FPS = 60
CAR_WIDTH = 50
CAR_HEIGHT = 80
LANE_WIDTH = 100
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 80
OBSTACLE_SPEED = 5

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Car Game")
clock = pygame.time.Clock()

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
    
    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, CAR_WIDTH, CAR_HEIGHT))
        # Car details
        pygame.draw.rect(screen, BLACK, (self.x + 10, self.y + 10, 30, 20))  # windshield
        pygame.draw.circle(screen, BLACK, (self.x + 10, self.y + CAR_HEIGHT - 10), 8)  # wheels
        pygame.draw.circle(screen, BLACK, (self.x + CAR_WIDTH - 10, self.y + CAR_HEIGHT - 10), 8)
    
    def move_left(self):
        if self.x > LANE_WIDTH:
            self.x -= self.speed
    
    def move_right(self):
        if self.x < WIDTH - LANE_WIDTH - CAR_WIDTH:
            self.x += self.speed

class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = OBSTACLE_SPEED
    
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        # Obstacle details
        pygame.draw.rect(screen, BLACK, (self.x + 10, self.y + 50, 30, 20))  # windshield
    
    def move(self):
        self.y += self.speed
    
    def is_off_screen(self):
        return self.y > HEIGHT

def draw_road():
    # Draw road
    pygame.draw.rect(screen, GRAY, (LANE_WIDTH, 0, WIDTH - 2 * LANE_WIDTH, HEIGHT))
    
    # Draw lane dividers
    for i in range(0, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 2, i, 4, 20))

def check_collision(car, obstacle):
    car_rect = pygame.Rect(car.x, car.y, CAR_WIDTH, CAR_HEIGHT)
    obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
    return car_rect.colliderect(obstacle_rect)

def game_over_screen(score):
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, RED)
    screen.blit(text, (WIDTH // 2 - 200, HEIGHT // 2 - 100))
    
    font_small = pygame.font.Font(None, 36)
    score_text = font_small.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2))
    
    restart_text = font_small.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(restart_text, (WIDTH // 2 - 220, HEIGHT // 2 + 50))
    
    pygame.display.flip()

def main():
    # Initialize player car
    player_car = Car(WIDTH // 2 - CAR_WIDTH // 2, HEIGHT - CAR_HEIGHT - 20)
    
    # Obstacles list
    obstacles = []
    obstacle_timer = 0
    
    # Game variables
    score = 0
    game_over = False
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
        
        if not game_over:
            # Handle input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_car.move_left()
            if keys[pygame.K_RIGHT]:
                player_car.move_right()
            
            # Create obstacles
            obstacle_timer += 1
            if obstacle_timer > 60:  # Create new obstacle every 60 frames
                lane = random.choice([LANE_WIDTH + 25, WIDTH // 2 - OBSTACLE_WIDTH // 2, WIDTH - LANE_WIDTH - OBSTACLE_WIDTH - 25])
                obstacles.append(Obstacle(lane, -OBSTACLE_HEIGHT))
                obstacle_timer = 0
            
            # Move and check obstacles
            for obstacle in obstacles[:]:
                obstacle.move()
                
                # Check collision
                if check_collision(player_car, obstacle):
                    game_over = True
                
                # Remove off-screen obstacles
                if obstacle.is_off_screen():
                    obstacles.remove(obstacle)
                    score += 1
            
            # Draw everything
            screen.fill(GREEN)  # Grass background
            draw_road()
            player_car.draw()
            
            for obstacle in obstacles:
                obstacle.draw()
            
            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (10, 10))
            
            pygame.display.flip()
        
        else:
            # Game over screen
            game_over_screen(score)
            
            # Wait for restart or quit
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                main()  # Restart game
                return
            if keys[pygame.K_q]:
                running = False
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()
