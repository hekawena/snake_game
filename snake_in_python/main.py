from turtle import *
from random import randrange
from freegames import square, vector

# 游戏配置
GRID_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGHT = 20
SPEED = 100  # 初始速度（毫秒）
LEVEL_SCORE = 5  # 每关需要的分数

# 游戏状态
food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)
score = 0
level = 1
game_over = False
paused = False
difficulty = "Normal"  # Easy/Normal/Hard

# 全局 Turtle 对象
menu_pen = None
status_pen = None

def reset_game():
    """重置游戏状态"""
    global food, snake, aim, score, level, game_over, paused, SPEED
    food = vector(0, 0)
    snake = [vector(10, 0)]
    aim = vector(0, -10)
    score = 0
    level = 1
    game_over = False
    paused = False
    SPEED = get_speed_by_difficulty()
    move_food()
    clear()
    if menu_pen:
        menu_pen.clear()
    display_status()
    if not game_over:
        move()

def get_speed_by_difficulty():
    """根据难度返回速度"""
    if difficulty == "Easy":
        return 150
    elif difficulty == "Hard":
        return 50
    else:  # Normal
        return 100

def change_difficulty(new_diff):
    """改变游戏难度"""
    global difficulty
    difficulty = new_diff
    if not paused and not game_over:
        reset_game()
    display_menu()

def change(x, y):
    """改变蛇的方向"""
    if not paused and not game_over:
        aim.x = x
        aim.y = y

def inside(head):
    """检查是否在边界内"""
    return -GRID_WIDTH / 2 * GRID_SIZE < head.x < GRID_WIDTH / 2 * GRID_SIZE - GRID_SIZE and \
           -GRID_HEIGHT / 2 * GRID_SIZE < head.y < GRID_HEIGHT / 2 * GRID_SIZE - GRID_SIZE

def move_food():
    """随机移动食物位置"""
    while True:
        food.x = randrange(-GRID_WIDTH // 2 + 1, GRID_WIDTH // 2) * GRID_SIZE
        food.y = randrange(-GRID_HEIGHT // 2 + 1, GRID_HEIGHT // 2) * GRID_SIZE
        print(f"Food moved to: ({food.x}, {food.y})")  # 调试
        if food not in snake:
            break

def check_level():
    """检查是否过关"""
    global level, SPEED
    if score >= level * LEVEL_SCORE:
        level += 1
        SPEED = max(30, SPEED - 10)
        move_food()
        display_status()

def display_status():
    """显示分数和关卡"""
    global status_pen
    if status_pen is None:
        status_pen = Turtle()
        status_pen.hideturtle()
        status_pen.penup()
    status_pen.clear()
    status_pen.goto(-GRID_WIDTH * GRID_SIZE / 2 + 10, GRID_HEIGHT * GRID_SIZE / 2 - 30)
    status_pen.write(f"Score: {score}  Level: {level}  Difficulty: {difficulty}",
                     font=("Arial", 12, "normal"))

def display_menu():
    """显示菜单选项"""
    global menu_pen
    if menu_pen is None:
        menu_pen = Turtle()
        menu_pen.hideturtle()
        menu_pen.penup()
    menu_pen.clear()
    menu_pen.goto(0, 0)
    menu_pen.color("blue")
    if paused and not game_over:
        menu_pen.write("PAUSED\n\nPress P to continue\nR to restart\nQ to quit",
                       align="center", font=("Arial", 16, "bold"))
    elif game_over:
        menu_pen.write("GAME OVER\n\nFinal Score: {}\nPress R to restart\nQ to quit".format(score),
                       align="center", font=("Arial", 16, "bold"))

def toggle_pause():
    """暂停/继续游戏"""
    global paused
    if not game_over:
        paused = not paused
        display_menu()
        if not paused:
            move()

def quit_game():
    """退出游戏"""
    bye()

def move():
    """移动蛇"""
    global score, game_over

    if paused or game_over:
        return

    head = snake[-1].copy()
    head.move(aim)
    print(f"Head at: ({head.x}, {head.y}), Food at: ({food.x}, {food.y})")  # 调试

    # 碰撞检测
    if not inside(head) or head in snake:
        game_over = True
        display_menu()
        return

    snake.append(head)

    # 吃到食物（宽度检测）
    if abs(head.x - food.x) < GRID_SIZE and abs(head.y - food.y) < GRID_SIZE:
        print("Food eaten!")  # 调试
        score += 1
        move_food()
        check_level()
    else:
        snake.pop(0)

    clear()

    # 绘制蛇身
    for body in snake:
        square(body.x, body.y, GRID_SIZE, 'black')

    # 绘制食物
    square(food.x, food.y, GRID_SIZE, 'green')

    display_status()
    update()
    ontimer(move, SPEED)

# 初始化游戏
setup(GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE)
hideturtle()
tracer(False)
listen()

# 游戏控制按键
onkey(lambda: change(GRID_SIZE, 0), 'Right')
onkey(lambda: change(-GRID_SIZE, 0), 'Left')
onkey(lambda: change(0, GRID_SIZE), 'Up')
onkey(lambda: change(0, -GRID_SIZE), 'Down')

onkey(toggle_pause, 'p')
onkey(reset_game, 'r')
onkey(quit_game, 'q')

onkey(lambda: change_difficulty("Easy"), '1')
onkey(lambda: change_difficulty("Normal"), '2')
onkey(lambda: change_difficulty("Hard"), '3')

# 初始食物位置
move_food()
display_status()

# 开始游戏
move()
done()