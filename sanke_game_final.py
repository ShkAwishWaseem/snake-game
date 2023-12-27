import pygame
import sys
import random

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the screen
WIDTH, HEIGHT = 800, 600  # Increased size
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        # Initialize the snake with one segment in the center of the grid
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.game_over = False
        self.score = 0  # Initialize the score

    def move(self):
        # Move the snake in the current direction
        if not self.game_over:
            head = self.body[0]
            new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
            self.body.insert(0, new_head)
            self.body.pop()  # Remove the last segment

    def grow(self):
        # Grow the snake by adding a new segment in the direction of movement
        if not self.game_over:
            tail = self.body[-1]
            new_segment = (tail[0] - self.direction[0], tail[1] - self.direction[1])
            self.body.append(new_segment)
            self.score += 1  # Increment the score

    def check_collision(self):
        # Check for collisions with the walls or itself
        if self.game_over:
            return True

        head = self.body[0]
        if (
            head in self.body[1:]
            or head[0] < 0
            or head[0] >= GRID_WIDTH
            or head[1] < 0
            or head[1] >= GRID_HEIGHT
        ):
            self.game_over = True
            return True

        return False

    def reset(self):
        # Reset the snake's position, direction, and score
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.game_over = False
        self.score = 0


class Apple:
    def __init__(self):
        # Initialize the apple with a random position
        self.position = (0, 0)
        self.spawn() # Randomly setting position of Applye

    def spawn(self):
        # Randomly spawn the apple within the grid
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))


class Game:
    def __init__(self):
        # Initialize the game window, clock, snake, apple, and paused state
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.apple = Apple()
        self.paused = False

    def handle_events(self):
        # Handle keyboard events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != DOWN:
                    self.snake.direction = UP
                elif event.key == pygame.K_DOWN and self.snake.direction != UP:
                    self.snake.direction = DOWN
                elif event.key == pygame.K_LEFT and self.snake.direction != RIGHT:
                    self.snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.snake.direction != LEFT:
                    self.snake.direction = RIGHT
                elif event.key == pygame.K_SPACE and self.snake.game_over:
                    self.snake.reset()
                elif event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                        

    def update(self):
        # Update the game state (snake movement, apple spawning, collision checks)
        if not self.paused:
            self.snake.move()
            if self.snake.body[0] == self.apple.position:
                self.snake.grow()
                self.apple.spawn()

            if self.snake.check_collision():
                # Don't exit the game immediately after a collision
                pass

    def draw(self):
        # Draw the game elements on the screen
        self.screen.fill(WHITE)

        # Draw snake
        for segment in self.snake.body:
            pygame.draw.rect(
                self.screen,
                GREEN,
                (
                    segment[0] * GRID_SIZE,
                    segment[1] * GRID_SIZE,
                    GRID_SIZE,
                    GRID_SIZE,
                ),
            )

        # Draw apple
        pygame.draw.rect(
            self.screen,
            RED,
            (
                self.apple.position[0] * GRID_SIZE,
                self.apple.position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE,
            ),
        )

        # Draw score at the top-left corner
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.snake.score}", True, GREEN)
        self.screen.blit(score_text, (10, 10))

        # Display game over message if the game is over
        if self.snake.game_over:
            font = pygame.font.Font(None, 36)
            game_over_text = font.render("Game Over! Press Space to restart.", True, RED)
            self.screen.blit(game_over_text, (WIDTH // 4, HEIGHT // 2))

        # Display paused message if the game is paused
        if self.paused:
            font = pygame.font.Font(None, 36)
            paused_text = font.render("Paused. Press Esc to unpause.", True, RED)
            self.screen.blit(paused_text, (WIDTH // 4, HEIGHT // 2))

        pygame.display.flip()

    def run(self):
        # Main game loop
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)  # Adjust the speed of the game


if __name__ == "__main__":
    # Create and run the game instance
    game = Game()
    game.run()


