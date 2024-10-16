import tkinter as tk
import random

# Game configuration constants
GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
INITIAL_BODY_PARTS = 3
SNAKE_COLOR = "#73EC8B"
FOOD_COLOR = "#C62E2E"
BG_COLOR = "#0B192C"

#hey dhruv this side i will make it more good so right now its a normal one that we played in 90s

# Snake class to handle snake behavior
class Snake:
    def __init__(self):
        self.body_size = INITIAL_BODY_PARTS
        self.coordinates = [[0, 0]] * self.body_size
        self.squares = []

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
            self.squares.append(square)

    def reset_snake(self):
        # Reset snake for new game
        self.coordinates = [[0, 0]] * self.body_size
        self.squares = []
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
            self.squares.append(square)

# Food class for food generation and placement
class Food:
    def __init__(self):
        self.create_food()

    def create_food(self):
        # Randomly generate food position on the grid
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# Main function for handling the snake's movement and game progression
def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    if check_collisions(x, y, snake):
        game_over()
        return

    # Update snake's body coordinates
    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    # Check if snake ate the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food.create_food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Recursively call next turn to keep the game running
    window.after(SPEED, next_turn, snake, food)

# Change direction of the snake based on user input
def change_direction(new_direction):
    global direction
    opposite_directions = {
        "left": "right", "right": "left", "up": "down", "down": "up"
    }

    # Ensure snake can't reverse direction into itself
    if direction != opposite_directions.get(new_direction):
        direction = new_direction

# Check for collisions with walls or self
def check_collisions(x, y, snake):
    # Collision with walls
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    # Collision with itself
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

# Function to display Game Over message and allow restart
def game_over():
    canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2 - 40, text="GAME OVER", fill="white", font=('consolas', 70))
    canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2 + 10, text="Press 'R' to Restart", fill="white", font=('consolas', 30))
    window.update()
    window.bind('<r>', restart_game)

# Function to reset and restart the game
def restart_game(event):
    global score, direction
    score = 0
    direction = "down"
    canvas.delete("all")
    label.config(text="Score: 0")
    snake.reset_snake()
    food.create_food()
    next_turn(snake, food)
    window.unbind('<r>')

# Tkinter window setup
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

# Initial direction and score
direction = "down"
score = 0

# Score display
label = tk.Label(window, text=f"Score: {score}", font=('consolas', 40))
label.pack()

# Game canvas setup
canvas = tk.Canvas(window, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Center the window on the screen
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind arrow keys to snake movement
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Initialize snake and food objects
snake = Snake()
food = Food()

# Start the game
next_turn(snake, food)

# Main event loop
window.mainloop()
