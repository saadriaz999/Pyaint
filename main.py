from utils import *

WIN = pygame.display.set_mode((WIDTH + RIGHT_TOOLBAR_WIDTH, HEIGHT))
GRID_STACK = GridStack(ROWS, COLS, BG_COLOR)
pygame.display.set_caption("Pyaint")
STATE = "COLOR"


def init_grid(rows, columns, color):
    grid = []

    for i in range(rows):
        grid.append([])
        for _ in range(columns):    #use _ when variable is not required
            grid[i].append(color)
    return grid


def draw_grid(win, grid):
    # TODO: start
    # showing the arrow beside the current selected layer
    arrow_button.y = 90 + CURRENT_LAYER * 50

    # displaying the current chosen layer
    if CURRENT_LAYER == -1:
        grid = GRID_STACK.show_merged_stack_view()
    else:
        grid = GRID_STACK.grid_stack[CURRENT_LAYER]
    # # TODO: end

    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pygame.draw.line(win, SILVER, (0, i * PIXEL_SIZE), (WIDTH, i * PIXEL_SIZE))
        for i in range(COLS + 1):
            pygame.draw.line(win, SILVER, (i * PIXEL_SIZE, 0), (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))


def draw_mouse_position_text(win):
    pos = pygame.mouse.get_pos()
    pos_font = get_font(MOUSE_POSITION_TEXT_SIZE)
    try:
        row, col = get_row_col_from_pos(pos)
        text_surface = pos_font.render(str(row) + ", " + str(col), 1, BLACK)
        win.blit(text_surface, (5 , HEIGHT - TOOLBAR_HEIGHT))
    except IndexError:
        for button in buttons:
            if not button.hover(pos):
                continue
            if button.text == "Clear":
                text_surface = pos_font.render("Clear Everything", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.text == "Erase":
                text_surface = pos_font.render("Erase", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            r,g,b = button.color
            text_surface = pos_font.render("( " + str(r) + ", " + str(g) + ", " + str(b) + " )", 1, BLACK)

            win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))

        for button in brush_widths:
            if not button.hover(pos):
                continue
            if button.width == size_small:
                text_surface = pos_font.render("Small-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.width == size_medium:
                text_surface = pos_font.render("Medium-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.width == size_large:
                text_surface = pos_font.render("Large-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break


def draw_brush_widths(win):
    brush_widths = [
        Button(rtb_x - size_small/2, 480, size_small, size_small, drawing_color, None, None, "ellipse"),
        Button(rtb_x - size_medium/2, 510, size_medium, size_medium, drawing_color, None, None, "ellipse") ,
        Button(rtb_x - size_large/2, 550, size_large, size_large, drawing_color, None, None, "ellipse")
    ]
    for button in brush_widths:
        button.draw(win)
        # Set border colour
        border_color = BLACK
        if button.color == BLACK:
            border_color = GRAY
        else:
            border_color = BLACK
        # Set border width
        border_width = 2
        if ((BRUSH_SIZE == 1 and button.width == size_small) or (BRUSH_SIZE == 2 and button.width == size_medium) or (BRUSH_SIZE == 3 and button.width == size_large)):
            border_width = 4
        else:
            border_width = 2
        # Draw border
        pygame.draw.ellipse(win, border_color, (button.x, button.y, button.width, button.height), border_width) #border


def draw(win, grid, buttons):
    win.fill(BG_COLOR)
    draw_grid(win, grid)

    for button in buttons:
        button.draw(win)

    # draw_button.draw(win)
    draw_brush_widths(win)
    draw_mouse_position_text(win)
    pygame.display.update()


def get_row_col_from_pos(pos):
    x, y = pos
    row = y // PIXEL_SIZE
    col = x // PIXEL_SIZE

    if row >= ROWS:
        raise IndexError
    if col >= ROWS:
        raise IndexError
    return row, col


def paint_using_brush(row, col, size):
    if BRUSH_SIZE == 1:
        grid[row][col] = drawing_color
    else: #for values greater than 1
        r = row-BRUSH_SIZE+1
        c = col-BRUSH_SIZE+1

        for i in range(BRUSH_SIZE*2-1):
            for j in range(BRUSH_SIZE*2-1):
                if r+i<0 or c+j<0 or r+i>=ROWS or c+j>=COLS:
                    continue
                grid[r+i][c+j] = drawing_color

    pass


# Checks whether the coordinated are within the canvas
def inBounds(row, col):
    if row < 0 or col < 0:
        return 0
    if row >= ROWS or col >= COLS:
        return 0
    return 1


def fill_bucket(row, col, color):

  # Visiting array
  vis = [[0 for i in range(101)] for j in range(101)]

  # Creating queue for bfs
  obj = []

  # Pushing pair of {x, y}
  obj.append([row, col])

  # Marking {x, y} as visited
  vis[row][col] = 1

  # Until queue is empty
  while len(obj) > 0:

    # Extracting front pair
    coord = obj[0]
    x = coord[0]
    y = coord[1]
    preColor = grid[x][y]

    grid[x][y] = color

    # Popping front pair of queue
    obj.pop(0)

    # For Upside Pixel or Cell
    if inBounds(x + 1, y) == 1 and vis[x + 1][y] == 0 and grid[x + 1][y] == preColor:
      obj.append([x + 1, y])
      vis[x + 1][y] = 1

    # For Downside Pixel or Cell
    if inBounds(x - 1, y) == 1 and vis[x - 1][y] == 0 and grid[x - 1][y] == preColor:
      obj.append([x - 1, y])
      vis[x - 1][y] = 1

    # For Right side Pixel or Cell
    if inBounds(x, y + 1) == 1 and vis[x][y + 1] == 0 and grid[x][y + 1] == preColor:
      obj.append([x, y + 1])
      vis[x][y + 1] = 1

    # For Left side Pixel or Cell
    if inBounds(x, y - 1) == 1 and vis[x][y - 1] == 0 and grid[x][y - 1] == preColor:
      obj.append([x, y - 1])
      vis[x][y - 1] = 1


run = True

clock = pygame.time.Clock()

drawing_color = BLACK

# TODO: START
SELECTED_LAYERS = []
CURRENT_LAYER = 0
grid = GRID_STACK.grid_stack[CURRENT_LAYER]

small_button_height = 14
small_button_width = 14

medium_button_height = 30
medium_button_width = 30
medium_button_space = 32

button_y_top_row = HEIGHT - TOOLBAR_HEIGHT / 2 - medium_button_height - 1
button_y_bot_row = HEIGHT - TOOLBAR_HEIGHT/2 + 1
# TODO: END

large_button_width = 40
large_button_height = 40
large_button_space = 42

size_small = 25
size_medium = 35
size_large = 50

rtb_x = WIDTH + RIGHT_TOOLBAR_WIDTH/2
brush_widths = [
    Button(rtb_x - size_small/2, 480, size_small, size_small, drawing_color, None, "ellipse"),
    Button(rtb_x - size_medium/2, 510, size_medium, size_medium, drawing_color, None, "ellipse") ,
    Button(rtb_x - size_large/2, 550, size_large, size_large, drawing_color, None, "ellipse")
]

# Adding Buttons
buttons = []

for i in range(int(len(COLORS)/2)):
    buttons.append(Button(100 + medium_button_space * i, button_y_top_row - 14, medium_button_width, medium_button_height, COLORS[i]))

for i in range(int(len(COLORS)/2)):
    buttons.append(Button(100 + medium_button_space * i, button_y_bot_row - 14, medium_button_width, medium_button_height, COLORS[i + int(len(COLORS) / 2)]))


buttons.append(Button(WIDTH - 2 * large_button_space, button_y_top_row, large_button_width, large_button_height, WHITE, "Erase", BLACK))  # Erase Button
buttons.append(Button(WIDTH - large_button_space, button_y_top_row, large_button_width, large_button_height, WHITE, "Clear", BLACK))  # Clear Button
buttons.append(Button(WIDTH - 3 * large_button_space - 10, button_y_top_row, large_button_width, large_button_height, name ="FillBucket", image_url="assets/paint-bucket.png")) #FillBucket


draw_button = Button(5, HEIGHT - TOOLBAR_HEIGHT/2 - 30, 60, 60, drawing_color)
buttons.append(draw_button)

# TODO: START (ADD BUTTONS)
# arrow button to show which layer is currently viewing
arrow_button = Button(rtb_x + 32, 40, 12, 24, BLACK, name='arrow', shape='left_arrow')
buttons.append(arrow_button)

# button to view entire stack
view_button = Button(rtb_x - 10, 30, large_button_width, large_button_height, TEAL, 'View', BLACK)
buttons.append(view_button)

# buttons for individual layers
layer_buttons = []
for i in range(GRID_STACK.MAX_LAYERS):
    layer_buttons.append(Button(rtb_x - 10, 80 + 50 * i, large_button_width, large_button_height, ORANGE, f'Layer{i + 1}', BLACK))

buttons.append(layer_buttons[0])

# buttons for selecting the layers
layer_button_checkboxes = []
for i in range(GRID_STACK.MAX_LAYERS):
    layer_button_checkboxes.append(Button(rtb_x - 30, 93 + 50 * i, small_button_width, small_button_height, RED, '', BLACK, name=f'Checkbox Layer {i+1}'))

buttons.append(layer_button_checkboxes[0])

# button for adding layers
add_button = Button(rtb_x - 10, 130, large_button_width, large_button_height, FUCHSIA, '+', BLACK)
buttons.append(add_button)

# button for deleting layers
delete_button = Button(rtb_x - 48, 350, medium_button_width, medium_button_height, GRAY, 'Delete', BLACK)
buttons.append(delete_button)

# button for merging layers
merge_button = Button(rtb_x - 16, 350, medium_button_width, medium_button_height, GRAY, 'Merge', BLACK)
buttons.append(merge_button)

# button for swapping layers
swap_button = Button(rtb_x + 16, 350, medium_button_width, medium_button_height, GRAY, 'Swap', BLACK)
buttons.append(swap_button)
# TODO: END

while run:
    clock.tick(FPS) #limiting FPS to 60 or any other value

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #if user closed the program
            run = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            try:
                row, col = get_row_col_from_pos(pos)

                if CURRENT_LAYER != -1:
                    if STATE == "COLOR":
                        paint_using_brush(row, col, BRUSH_SIZE)

                    elif STATE == "FILL":
                        fill_bucket(row, col, drawing_color)

            except IndexError:
                for button in buttons:
                    if not button.clicked(pos):
                        continue
                    if button.text == "Clear":
                        grid = init_grid(ROWS, COLS, BG_COLOR)
                        drawing_color = BLACK
                        draw_button.color = drawing_color
                        STATE = "COLOR"
                        break

                    if button.name == "FillBucket":
                        STATE = "FILL"
                        break

                    # TODO: START
                    if button.text == '+':
                        buttons.append(layer_buttons[GRID_STACK.num_layers])
                        buttons.append(layer_button_checkboxes[GRID_STACK.num_layers])
                        GRID_STACK.add_layer()
                        add_button.y += 50
                        if GRID_STACK.num_layers == 5:
                            buttons.remove(add_button)
                        break

                    if button.text == 'View':
                        CURRENT_LAYER = -1
                        break

                    if button.text and button.text[:5] == 'Layer':
                        CURRENT_LAYER = int(button.text[-1]) - 1
                        grid = GRID_STACK.grid_stack[CURRENT_LAYER]
                        break

                    if button.name and button.name[:8] == 'Checkbox':
                        layer_clicked = int(button.name[-1]) - 1
                        if layer_clicked in SELECTED_LAYERS:
                            SELECTED_LAYERS.remove(layer_clicked)
                            layer_button_checkboxes[layer_clicked].color = RED
                        else:
                            SELECTED_LAYERS.append(layer_clicked)
                            layer_button_checkboxes[layer_clicked].color = GREEN
                        break

                    if button.text == 'Delete':
                        if GRID_STACK.num_layers - len(SELECTED_LAYERS) < 1 or not SELECTED_LAYERS:
                            break

                        # removing extra layer buttons and their checkmarks
                        for i in range(len(SELECTED_LAYERS)):
                            buttons.remove(layer_buttons[GRID_STACK.num_layers-1-i])
                            buttons.remove(layer_button_checkboxes[GRID_STACK.num_layers-1-i])

                        # delete layer from grid_stack object
                        SELECTED_LAYERS.sort(reverse=True)
                        for layer in SELECTED_LAYERS:
                            GRID_STACK.delete_layer(layer)

                        # adding the add-layer button
                        if SELECTED_LAYERS:
                            add_button.y = 80 + 50 * GRID_STACK.num_layers

                        # unchecking all checkbox buttons
                        for check_button in layer_button_checkboxes:
                            check_button.color = RED

                        # unchecking all selected layers in from the backend and setting current layer
                        # to view layer
                        SELECTED_LAYERS = []
                        CURRENT_LAYER = -1

                        # adding the add button to button list if number of layers less than 5
                        if GRID_STACK.num_layers < 5:
                            buttons.append(add_button)

                        break

                    if button.text == 'Merge':
                        if GRID_STACK.num_layers == 1 or not SELECTED_LAYERS:
                            break

                        # removing extra layer buttons and their checkmarks
                        for i in range(len(SELECTED_LAYERS)-1):
                            buttons.remove(layer_buttons[GRID_STACK.num_layers-1-i])
                            buttons.remove(layer_button_checkboxes[GRID_STACK.num_layers-1-i])

                        # merging all layers
                        top_layer = min(SELECTED_LAYERS)
                        SELECTED_LAYERS.sort()
                        for layer in SELECTED_LAYERS:
                            if layer != top_layer:
                                GRID_STACK.merge_layer(top_layer, layer)
                                for i in range(len(SELECTED_LAYERS)):
                                    if SELECTED_LAYERS[i] > layer:
                                        SELECTED_LAYERS[i] -= 1

                        # adding the add-layer button
                        if SELECTED_LAYERS:
                            add_button.y = 80 + 50 * GRID_STACK.num_layers

                        # unchecking all checkbox buttons
                        for check_button in layer_button_checkboxes:
                            check_button.color = RED

                        # unchecking all selected layers in from the backend and setting current layer
                        # to view layer
                        SELECTED_LAYERS = []
                        CURRENT_LAYER = -1

                        # adding the add button to button list if number of layers less than 5
                        if GRID_STACK.num_layers < 5:
                            buttons.append(add_button)

                        break

                    if button.text == 'Swap':
                        if len(SELECTED_LAYERS) != 2:
                            break

                        GRID_STACK.swap_layers(SELECTED_LAYERS[0], SELECTED_LAYERS[1])
                        break
                    # TODO: END

                    drawing_color = button.color
                    draw_button.color = drawing_color

                    break

                for button in brush_widths:
                    if not button.clicked(pos):
                        continue
                    #set brush width
                    if button.width == size_small:
                        BRUSH_SIZE = 1
                    elif button.width == size_medium:
                        BRUSH_SIZE = 2
                    elif button.width == size_large:
                        BRUSH_SIZE = 3

                    STATE = "COLOR"


    draw(WIN, grid, buttons)

pygame.quit()