import tkinter as tk
import random

# Game configuration
GAME_WIDTH = 1000
GAME_HEIGHT = 700
SNAKE_SIZE = 20
UPDATE_DELAY = 100  # milliseconds

# Colors
BACKGROUND_COLOR = "#000000"   
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        
        # Create canvas for game display
        self.canvas = tk.Canvas(root, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()

        # Create Play and Pause buttons
        self.play_button = tk.Button(root, text="Play", command=self.play_game)
        self.play_button.pack(side=tk.LEFT, padx=20)
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_game)
        self.pause_button.pack(side=tk.LEFT, padx=20)
        
        # Initialize game variables
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.snake_direction = "Right"
        self.food = self.create_food()
        self.score = 0
        self.game_over = False
        self.paused = False

        # Create snake and food
        self.create_snake()
        self.create_food_display() 

        # Bind keys for controlling the snake
        self.root.bind("<Left>", self.turn_left)
        self.root.bind("<Right>", self.turn_right)
        self.root.bind("<Up>", self.turn_up)
        self.root.bind("<Down>", self.turn_down)

    def create_snake(self):
        """Draw the snake on the canvas."""
        self.snake_squares = []
        for x, y in self.snake:
            square = self.canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill=SNAKE_COLOR)
            self.snake_squares.append(square)

    def create_food(self):
        """Create food at a random location."""
        x = random.randint(0, (GAME_WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        y = random.randint(0, (GAME_HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
        return x, y

    def create_food_display(self):
        """Display food on the canvas."""
        if hasattr(self, 'food_square'):
            self.canvas.delete(self.food_square)
        x, y = self.food
        self.food_square = self.canvas.create_oval(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill=FOOD_COLOR)

    def move_snake(self):
        """Move the snake in the current direction."""
        head_x, head_y = self.snake[0]

        if self.snake_direction == "Left":
            head_x -= SNAKE_SIZE
        elif self.snake_direction == "Right":
            head_x += SNAKE_SIZE
        elif self.snake_direction == "Up":
            head_y -= SNAKE_SIZE
        elif self.snake_direction == "Down":
            head_y += SNAKE_SIZE

        # Insert new head position
        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]

    def check_collisions(self):
        """Check for collisions with walls, self, or food."""
        head_x, head_y = self.snake[0]

        # Check if snake hits walls
        if head_x < 0 or head_x >= GAME_WIDTH or head_y < 0 or head_y >= GAME_HEIGHT:
            self.game_over = True

        # Check if snake collides with itself
        if len(self.snake) != len(set(self.snake)):
            self.game_over = True

        # Check if snake eats food
        if self.snake[0] == self.food:
            self.score += 1
            self.snake.append(self.snake[-1])  # Grow the snake
            self.food = self.create_food()  # Create new food
            self.create_food_display()

    def update_snake_position(self):
        """Update the positions of the snake squares."""
        for square, (x, y) in zip(self.snake_squares, self.snake):
            self.canvas.coords(square, x, y, x + SNAKE_SIZE, y + SNAKE_SIZE)

    def game_loop(self):
        """Main game loop."""
        if not self.game_over and not self.paused:
            self.move_snake()
            self.check_collisions()
            self.update_snake_position()
            self.root.after(UPDATE_DELAY, self.game_loop)
        elif self.game_over:
            self.canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2, text=f"Game Over! Score: {self.score}", fill="white", font=('Arial', 24))

    def play_game(self):
        """Resume the game."""
        if self.game_over:
            self.reset_game()
        self.paused = False
        self.game_loop()

    def pause_game(self):
        """Pause the game."""
        self.paused = True

    def reset_game(self):
        """Reset the game to the initial state."""
        self.canvas.delete("all")
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.snake_direction = "Right"
        self.food = self.create_food()
        self.score = 0
        self.game_over = False
        self.create_snake()
        self.create_food_display()

    def turn_left(self, event):
        if self.snake_direction != "Right":
            self.snake_direction = "Left"

    def turn_right(self, event):
        if self.snake_direction != "Left":
            self.snake_direction = "Right"

    def turn_up(self, event):
        if self.snake_direction != "Down":
            self.snake_direction = "Up"

    def turn_down(self, event):
        if self.snake_direction != "Up":
            self.snake_direction = "Down"

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
