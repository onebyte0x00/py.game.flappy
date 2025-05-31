import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.25
FLAP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Load fonts
font = pygame.font.SysFont('Arial', 30)

class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0
        self.radius = 15
        
    def flap(self):
        self.velocity = FLAP_STRENGTH
        
    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Keep bird within screen bounds
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        if self.y > HEIGHT:
            self.y = HEIGHT
            self.velocity = 0
            
    def draw(self):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, int(self.y)), self.radius)
        # Draw eye
        pygame.draw.circle(screen, BLACK, (self.x + 5, int(self.y) - 5), 5)
        # Draw beak
        pygame.draw.polygon(screen, (255, 165, 0), [
            (self.x + self.radius, int(self.y)),
            (self.x + self.radius + 10, int(self.y)),
            (self.x + self.radius, int(self.y) - 5)
        ])
        
    def get_mask(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(100, HEIGHT - 100 - PIPE_GAP)
        self.top_pipe = pygame.Rect(self.x, 0, 50, self.height)
        self.bottom_pipe = pygame.Rect(self.x, self.height + PIPE_GAP, 50, HEIGHT - self.height - PIPE_GAP)
        self.passed = False
        
    def update(self):
        self.x -= PIPE_SPEED
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x
        
    def draw(self):
        pygame.draw.rect(screen, GREEN, self.top_pipe)
        pygame.draw.rect(screen, GREEN, self.bottom_pipe)
        
    def collide(self, bird):
        bird_mask = bird.get_mask()
        return bird_mask.colliderect(self.top_pipe) or bird_mask.colliderect(self.bottom_pipe)

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def game_over_screen(score):
    screen.fill(SKY_BLUE)
    game_over_text = font.render("Game Over", True, BLACK)
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    restart_text = font.render("Press R to Restart", True, BLACK)
    
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 60))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 60))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    bird = Bird()
    pipes = []
    score = 0
    last_pipe = pygame.time.get_ticks()
    running = True
    game_active = True
    
    while running:
        clock.tick(FPS)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird.flap()
                if event.key == pygame.K_q:
                    running = False
        
        # Update game objects
        if game_active:
            bird.update()
            
            # Generate new pipes
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe())
                last_pipe = time_now
                
            # Update pipes and check for collisions
            for pipe in pipes:
                pipe.update()
                
                # Check for collision
                if pipe.collide(bird):
                    game_active = False
                
                # Check if pipe passed bird for scoring
                if not pipe.passed and pipe.x < bird.x - 50:
                    pipe.passed = True
                    score += 1
                
                # Remove pipes that are off screen
                if pipe.x < -50:
                    pipes.remove(pipe)
            
            # Check if bird hit the ground or ceiling
            if bird.y >= HEIGHT or bird.y <= 0:
                game_active = False
        
        # Drawing
        screen.fill(SKY_BLUE)
        
        if game_active:
            bird.draw()
            for pipe in pipes:
                pipe.draw()
            draw_score(score)
        else:
            game_over_screen(score)
            # Reset game
            bird = Bird()
            pipes = []
            score = 0
            last_pipe = pygame.time.get_ticks()
            game_active = True
            
        pygame.display.update()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
