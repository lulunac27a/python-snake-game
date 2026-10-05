import turtle
import time
import random

# Game configuration variables
delay = 0.1  # delay between each game loop iteration
score = 0  # current score of the player
high_score = 0  # highest score achieved in the game

# Track the timestamp when the food was spawned/last eaten
last_eat_time = time.time()  # timestamp when the food was last eaten

# 1. Set up the game window
window = turtle.Screen()  # initialize the game window
window.title("Snake Game - Speed Combo Edition")  # set the window title
window.bgcolor("black")  # set the background color of the window
window.setup(width=600, height=600)  # set the window size
window.tracer(0)  # turn off automatic screen updates for smoother animation

# 2. Create the Snake Head
head = turtle.Turtle()  # create the snake head
head.speed(0)  # set the animation speed of the snake head
head.shape("square")  # set the shape of the snake head
head.color("green")  # set the color of the snake head
head.penup()  # ensure the snake head doesn't draw lines
head.goto(0, 0)  # position the snake head at the center
head.direction = "stop"  # initialize the snake's movement direction

# 3. Create the Snake Food
food = turtle.Turtle()  # create the snake food
food.speed(0)  # set the animation speed of the food
food.shape("circle")  # set the shape of the food
food.color("red")  # set the color of the food
food.penup()  # ensure the food doesn't draw lines
food.goto(0, 100)  # position the food at the starting location

segments = []  # list to keep track of all the snake body segments

# 4. Create the Scoreboard display
pen = turtle.Turtle()  # create the scoreboard turtle
pen.speed(0)  # set the animation speed of the scoreboard turtle
pen.color("white")  # set the color of the scoreboard text
pen.penup()  # ensure the scoreboard turtle doesn't draw lines
pen.hideturtle()  # hide the scoreboard turtle
pen.goto(0, 260)  # position the scoreboard at the top of the window
pen.write(
    "Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal")
)  # display the initial score and high score


# 5. Functions to handle movement logic
def go_up():  # function to change the snake's direction to up
    if head.direction != "down":
        head.direction = "up"


def go_down():  # function to change the snake's direction to down
    if head.direction != "up":
        head.direction = "down"


def go_left():  # function to change the snake's direction to left
    if head.direction != "right":
        head.direction = "left"


def go_right():  # function to change the snake's direction to right
    if head.direction != "left":
        head.direction = "right"


def move():  # function to move the snake based on its current direction
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
window.listen()  # set the window to listen for keyboard input
window.onkeypress(go_up, "Up")  # bind the "Up" arrow key to the go_up function
# bind the "Down" arrow key to the go_down function
window.onkeypress(go_down, "Down")
# bind the "Left" arrow key to the go_left function
window.onkeypress(go_left, "Left")
window.onkeypress(
    go_right, "Right"
)  # bind the "Right" arrow key to the go_right function


def reset_game():  # function to reset the game state after a collision
    # declare score and last_eat_time as global variables to modify them within the function
    global score, last_eat_time
    time.sleep(1)  # pause for a short moment before resetting the game
    head.goto(0, 0)  # move the snake's head to the center of the window
    head.direction = "stop"  # stop the snake's movement

    for segment in segments:  # move each segment off-screen
        segment.goto(1000, 1000)
    segments.clear()  # clear the list of segments

    score = 0  # reset the score
    last_eat_time = time.time()  # Reset the timer#reset the timer for food consumption
    pen.clear()  # clear the previous score display
    pen.write(
        f"Score: {score}  High Score: {high_score}",
        align="center",
        font=("Courier", 24, "normal"),
    )  # display the updated score and high score


# 7. Main Game Loop
while True:  # main game loop
    window.update()  # update the window to reflect changes

    # Check for a wall collision
    if (
        head.xcor() > 290
        or head.xcor() < -290
        or head.ycor() > 290
        or head.ycor() < -290
    ):  # check if the snake has collided with the wall
        reset_game()  # reset the game if the snake collides with the wall

    # Check if snake eats the food
    if head.distance(food) < 20:  # check if the snake has eaten the food
        # Calculate time passed since the last food item was eaten
        current_time = time.time()  # get the current time
        time_taken = (
            current_time - last_eat_time
        )  # calculate the time taken since the last food was eaten

        # --- SCORE BONUS LOGIC ---
        # Base points for eating food
        base_points = 10  # base points for eating food

        # Calculate a bonus: The faster you are, the higher the bonus.
        # Max bonus is 50 points, decreasing by 5 points for every second taken.
        bonus = max(
            0, int(50 - (time_taken * 5))
        )  # calculate the bonus points based on the time taken

        # Add points to score
        score += base_points + bonus  # update the score with base points and bonus

        # Reset the timer anchor for the next food piece
        last_eat_time = current_time  # update the last eat time to the current time
        # -------------------------

        # Move the food to a random spot on the grid
        # generate a random x-coordinate for the food
        x = random.randint(-280, 280)
        # generate a random y-coordinate for the food
        y = random.randint(-280, 280)
        food.goto(x, y)  # move the food to the new random location

        # Add a new segment to the snake body#create a new segment for the snake's body
        new_segment = turtle.Turtle()  # initialize a new turtle object for the segment
        new_segment.speed(0)  # set the speed of the segment to the maximum
        new_segment.shape("square")  # set the shape of the segment to a square
        new_segment.color("dark green")  # set the color of the segment
        new_segment.penup()  # ensure the segment doesn't draw lines
        # add the new segment to the list of segments
        segments.append(new_segment)

        if score > high_score:  # check if the current score exceeds the high score
            high_score = score  # update the high score if the current score is higher

        pen.clear()  # clear the previous score display
        # Optional: Displays the points earned on the scoreboard
        pen.write(
            f"Score: {score} (+{base_points + bonus})  High: {high_score}",
            align="center",
            font=("Courier", 18, "normal"),
        )  # display the updated score and high score on the scoreboard

    # Move the end segments first in reverse order to follow the head
    for index in range(
        len(segments) - 1, 0, -1
    ):  # move each segment to the position of the previous segment in reverse order
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is#ensure the first segment follows the head
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)

    move()  # move the snake in the current direction

    # Check for body collisions
    for segment in segments:
        if segment.distance(head) < 20:
            reset_game()

    time.sleep(delay)

window.mainloop()
