import turtle


def update_score(l_score, r_score, player, score_board):
    if player == 'l':
        l_score += 1
    else:
        r_score += 1

    score_board.clear()
    score_board.write(f'Left Player: {l_score} -- Right Player: {r_score}',
                      align='center', font=('Arial', 24, 'normal'))
    return l_score, r_score, score_board


def create_paddle(x, color):
    paddle = turtle.Turtle()
    paddle.speed(0)
    paddle.shape('square')
    paddle.color(color)
    paddle.shapesize(stretch_wid=6, stretch_len=2)
    paddle.penup()
    paddle.goto(x, 0)
    return paddle


def create_ball():
    ball = turtle.Turtle()
    ball.speed(40)
    ball.shape('circle')
    ball.color('blue')
    ball.penup()
    ball.goto(0, 0)
    ball.dx = 5
    ball.dy = -5
    return ball


def setup_game():
    screen = turtle.Screen()
    screen.title('Pong Arcade Game')
    screen.bgcolor('white')
    screen.setup(width=1000, height=600)

    l_paddle = create_paddle(-400, 'red')
    r_paddle = create_paddle(400, 'black')
    ball = create_ball()

    score_board = turtle.Turtle()
    score_board.speed(0)
    score_board.color('blue')
    score_board.penup()
    score_board.hideturtle()
    score_board.goto(0, 260)
    score_board.write('Left Player: 0 -- Right Player: 0',
                      align='center', font=('Arial', 24, 'normal'))

    return screen, ball, l_paddle, r_paddle, score_board


def pong_game():
    game_components = setup_game()
    screen, ball, l_paddle, r_paddle, score_board = game_components
    l_score = 0
    r_score = 0

    def l_paddle_up():
        if l_paddle.ycor() < 250:  # Boundary check
            l_paddle.sety(l_paddle.ycor() + 20)

    def l_paddle_down():
        if l_paddle.ycor() > -250:  # Boundary check
            l_paddle.sety(l_paddle.ycor() - 20)

    def r_paddle_up():
        if r_paddle.ycor() < 250:  # Boundary check
            r_paddle.sety(r_paddle.ycor() + 20)

    def r_paddle_down():
        if r_paddle.ycor() > -250:  # Boundary check
            r_paddle.sety(r_paddle.ycor() - 20)

    screen.listen()
    screen.onkeypress(l_paddle_up, 'e')
    screen.onkeypress(l_paddle_down, 'x')
    screen.onkeypress(r_paddle_up, 'Up')
    screen.onkeypress(r_paddle_down, 'Down')

    # Ball speed increment as the game progresses
    def increase_ball_speed():
        ball.dx *= 1.05
        ball.dy *= 1.05

    while True:
        screen.update()
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Ball collision with walls
        if ball.ycor() > 280:
            ball.sety(280)
            ball.dy *= -1

        if ball.ycor() < -280:
            ball.sety(-280)
            ball.dy *= -1

        # Ball goes off the right side
        if ball.xcor() > 500:
            ball.goto(0, 0)
            ball.dy *= -1
            l_score, r_score, score_board = update_score(
                l_score, r_score, 'l', score_board)
            increase_ball_speed()  # Increase ball speed
            continue

        # Ball goes off the left side
        if ball.xcor() < -500:
            ball.goto(0, 0)
            ball.dy *= -1
            l_score, r_score, score_board = update_score(
                l_score, r_score, 'r', score_board)
            increase_ball_speed()  # Increase ball speed
            continue

        # Paddle collision (Right)
        if ((ball.xcor() > 360) and (ball.xcor() < 370) and
                (ball.ycor() < r_paddle.ycor() + 50) and (ball.ycor() > r_paddle.ycor() - 50)):
            ball.setx(360)
            ball.dx *= -1

        # Paddle collision (Left)
        if ((ball.xcor() < -360) and (ball.xcor() > -370) and
                (ball.ycor() < l_paddle.ycor() + 50) and (ball.ycor() > l_paddle.ycor() - 50)):
            ball.setx(-360)
            ball.dx *= -1

        # End game if a player reaches 5 points
        if l_score == 5 or r_score == 5:
            score_board.goto(0, 0)
            score_board.write("Game Over! {} Player Wins!".format(
                'Left' if l_score == 5 else 'Right'),
                align='center', font=('Arial', 36, 'bold'))
            break  # Exit the game loop


if __name__ == '__main__':
    pong_game()
