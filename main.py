from PIL import Image, ImageDraw

black_pix = (0, 0, 0, 255) # считаем что поля, крестики, нолики имеют такой цвет
image = Image.open('image.png')  # Открываем изображение
draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту
pix = image.load()  # Выгружаем значения пикселей

# Найдем границы игрового поля
area = {"top": 0, "bot": 0, "left": 0, "right": 0}
def find_top():
    for y in range(height):
        for x in range(width):
            if pix[x,y] == black_pix: 
                area["top"] = y
                return True
def find_bot():
    for y in reversed(range(height)):
        for x in range(width):
            if pix[x,y] == black_pix: 
                area["bot"] = y
                return True
def find_left():
    for x in range(width):
        for y in range(height):
            if pix[x,y] == black_pix: 
                area["left"] = x
                return True
def find_right():
    for x in reversed(range(width)):
        for y in range(height):
            if pix[x,y] == black_pix: 
                area["right"] = x
                return True
find_top()
find_bot()
find_left()
find_right()

# определяем границы каждой клетки
cells = [0] * 9 
for i in range(9):
    cells[i] = {"top": (area["top"] + ((area["bot"] - area["top"]) // 3) * (i // 3)), 
            "bot": (area["top"] + ((area["bot"] - area["top"]) // 3) * (1 + i // 3)), 
            "left": (area["left"] + ((area["right"] - area["left"]) // 3) * (i % 3)), 
            "right": (area["left"] + ((area["right"] - area["left"]) // 3) * (1 + i % 3)),
            "value": -1}

# определяем что находится в каждой клетке: 1 - крестик, 0 - нолик), -1 - ничего
# если в центре клетки черный пиксель, то в ней крестик, что и проверяется в первую очередь
# далее алгоритм работает следующим образом:
# если при проходе из левой границу в правую мы встретили четыре или три черные линии, то там круг
# иначе там одна или две черные линии, то есть ничего не стоит
# сделал именно так, так как не захотел отсекать части рамок, 
# а у нас при определении границ клеток части рамок заходят в них
for i in range(9):
    ycell = (cells[i]["top"] + cells[i]["bot"]) // 2
    if pix[(cells[i]["left"] + cells[i]["right"]) // 2, ycell] == black_pix:
        cells[i]["value"] = 1
    else:
        count = 0
        flag = False
        for x in range(cells[i]["left"], cells[i]["right"]):
            if pix[x, ycell] == black_pix:
                if flag == False:
                    count += 1
                    flag = True
            else:
                if flag:
                    flag = False
        if count == 3 or count == 4:
            cells[i]["value"] = 0

# Определяем победителя и сразу запоминаем координаты начала и конца линии, которую должны будем провести    
def check_line(first, second, third):
    if cells[first]["value"] == cells[second]["value"] and cells[second]["value"] == cells[third]["value"]:
        return True

line = (0, 0, 0, 0)
for n in range(3):
    if check_line(n * 3, n * 3 + 1, n * 3 + 2):
        line = (cells[n * 3]["left"], (cells[n * 3]["top"] + cells[n * 3]["bot"]) // 2, cells[n * 3 + 2]["right"], (cells[n * 3 + 2]["top"] + cells[n * 3 + 2]["bot"]) // 2)
        break
    if check_line(n, n + 3, n + 6):
        line = ((cells[n]["left"] + cells[n]["right"]) // 2, cells[n]["top"], (cells[n + 6]["left"] + cells[n + 6]["right"]) // 2, cells[n + 6]["bot"])
        break
if check_line(0, 4, 8):
    line = (cells[0]["left"], cells[0]["top"], cells[8]["right"], cells[8]["bot"])
if check_line(2, 4, 6):
    line = (cells[6]["left"], cells[6]["bot"], cells[2]["right"], cells[2]["top"])
if line == (0, 0, 0, 0):
    print("no winner")
    exit(0)

# Рисуем результат 
for x in range(width):
   for y in range(height):
        draw.point((x, y), pix[x,y])
draw.line(line, fill=(0, 0, 0, 255), width=7)

image.save("result.png", "png") 