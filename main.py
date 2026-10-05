import turtle
import time
import random

# Game configuration variables
delay = 0.1
score = 0
high_score = 0

# Track the timestamp when the food was spawned/last eaten
last_eat_time = time.time()

# 1. Set up the game window
window = turtle.Screen()
window.title("Snake Game - Speed Combo Edition")
window.bgcolor("black")
window.setup(width=600, height=600)
window.tracer(0)

# 2. Create the Snake Head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("green")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# 3. Create the Snake Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

segments = []

# 4. Create the Scoreboard display
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center",
          font=("Courier", 24, "normal"))


# 5. Functions to handle movement logic
def go_up():
    if head.direction != "down":
        head.direction = "up"


def go_down():
    if head.direction != "up":
        head.direction = "down"


def go_left():
    if head.direction != "right":
        head.direction = "left"


def go_right():
    if head.direction != "left":
        head.direction = "right"


def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)


# 6. Keyboard bindings
window.listen()
window.onkeypress(go_up, "Up")
window.onkeypress(go_down, "Down")
window.onkeypress(go_left, "Left")
window.onkeypress(go_right, "Right")


def reset_game():
    global score, last_eat_time
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "stop"

    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()

    score = 0
    last_eat_time = time.time()  # Reset the timer
    pen.clear()
    pen.write(
        f"Score: {score}  High Score: {high_score}",
        align="center",
        font=("Courier", 24, "normal"),
    )


# 7. Main Game Loop
while True:
    window.update()

    # Check for a wall collision
    if (
        head.xcor() > 290
        or head.xcor() < -290
        or head.ycor() > 290
        or head.ycor() < -290
    ):
        reset_game()

    # Check if snake eats the food
    if head.distance(food) < 20:
        # Calculate time passed since the last food item was eaten
        current_time = time.time()
        time_taken = current_time - last_eat_time

        # --- SCORE BONUS LOGIC ---
        # Base points for eating food
        base_points = 10

        # Calculate a bonus: The faster you are, the higher the bonus.
        # Max bonus is 50 points, decreasing by 5 points for every second taken.
        bonus = max(0, int(50 - (time_taken * 5)))

        # Add points to score
        score += base_points + bonus

        # Reset the timer anchor for the next food piece
        last_eat_time = current_time
        # -------------------------

        # Move the food to a random spot on the grid
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        food.goto(x, y)

        # Add a new segment to the snake body
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("dark green")
        new_segment.penup()
        segments.append(new_segment)

        if score > high_score:
            high_score = score

        pen.clear()
        # Optional: Displays the points earned on the scoreboard
        pen.write(
            f"Score: {score} (+{base_points + bonus})  High: {high_score}",
            align="center",
            font=("Courier", 18, "normal"),
        )

    # Move the end segments first in reverse order
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()

    # Check for body collisions
    for segment in segments:
        if segment.distance(head) < 20:
            reset_game()

    time.sleep(delay)

window.mainloop()
