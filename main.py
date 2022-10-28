from utils import *
from utils.HelperFunctions import HelperFunctions

# setting display caption
pygame.display.set_caption('Pyaint')

# initializing the window
WIN = pygame.display.set_mode((WIDTH + RIGHT_TOOLBAR_WIDTH, HEIGHT))

# initializing the grid stack (layers of canvas)
GRID_STACK = GridStack(ROWS, COLS, BG_COLOR)

# creating an object to access helper functions
HF = HelperFunctions()

# setting starting state, color, and paint brush size
STATE = "COLOR"
drawing_color = BLACK
BRUSH_SIZE = 1

run = True
clock = pygame.time.Clock()

# initially keeping all layers not selected and first layer is viewed
SELECTED_LAYERS = []
CURRENT_LAYER = 0
grid = GRID_STACK.grid_stack[CURRENT_LAYER]


# Adding Buttons
buttons = []

# BRUSH_WIDTHS = [
#     Button(RIGHT_TOOLBAR_CENTER - SIZE_SMALL / 2, 480, SIZE_SMALL, SIZE_SMALL, drawing_color, None, "ellipse"),
#     Button(RIGHT_TOOLBAR_CENTER - SIZE_MEDIUM / 2, 510, SIZE_MEDIUM, SIZE_MEDIUM, drawing_color, None, "ellipse"),
#     Button(RIGHT_TOOLBAR_CENTER - SIZE_LARGE / 2, 550, SIZE_LARGE, SIZE_LARGE, drawing_color, None, "ellipse")
# ]

# adding brush width buttons
small_brush_width_button = Button(RIGHT_TOOLBAR_CENTER - SIZE_SMALL / 2, 480, SIZE_SMALL, SIZE_SMALL,
                                  BLACK, None, shape="ellipse", name='small_width')
medium_brush_width_button = Button(RIGHT_TOOLBAR_CENTER - SIZE_MEDIUM / 2, 510, SIZE_MEDIUM, SIZE_MEDIUM,
                                   drawing_color, None, shape="ellipse", name='medium_width')
large_brush_width_button = Button(RIGHT_TOOLBAR_CENTER - SIZE_LARGE / 2, 550, SIZE_LARGE, SIZE_LARGE,
                                  drawing_color, None, shape="ellipse", name='large_width')

buttons.append(small_brush_width_button)
buttons.append(medium_brush_width_button)
buttons.append(large_brush_width_button)

# top layer of color buttons
for i in range(int(len(COLORS) / 2)):
    buttons.append(Button(100 + MEDIUM_BUTTON_SPACE * i, BUTTON_Y_TOP_ROW - 14, MEDIUM_BUTTON_WIDTH,
                          MEDIUM_BUTTON_HEIGHT, COLORS[i]))

# bottom layer of colour buttons
for i in range(int(len(COLORS) / 2)):
    buttons.append(Button(100 + MEDIUM_BUTTON_SPACE * i, BUTTON_Y_BOT_ROW - 14, MEDIUM_BUTTON_WIDTH,
                          MEDIUM_BUTTON_HEIGHT, COLORS[i + int(len(COLORS) / 2)]))

# button to erase from canvas
erase_button = Button(WIDTH - 2 * LARGE_BUTTON_SPACE, BUTTON_Y_TOP_ROW, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT,
                      WHITE, "Erase", BLACK)
buttons.append(erase_button)

# button to clear canvas
clear_button = Button(WIDTH - LARGE_BUTTON_SPACE, BUTTON_Y_TOP_ROW, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT,
                      WHITE, "Clear", BLACK)
buttons.append(clear_button)

# fill bucket button
fill_bucket_button = Button(WIDTH - 3 * LARGE_BUTTON_SPACE - 10, BUTTON_Y_TOP_ROW, LARGE_BUTTON_WIDTH,
                            LARGE_BUTTON_HEIGHT, name="FillBucket", image_url="assets/paint-bucket.png")
buttons.append(fill_bucket_button)

# button showing the current chosen button
draw_button = Button(5, HEIGHT - TOOLBAR_HEIGHT / 2 - 30, 60, 60, drawing_color)
buttons.append(draw_button)

# arrow button to show which layer is currently viewing
arrow_button = Button(RIGHT_TOOLBAR_CENTER + 32, 40, 12, 24, BLACK, name='arrow', shape='left_arrow')
buttons.append(arrow_button)

# button to view entire stack
view_button = Button(RIGHT_TOOLBAR_CENTER - 10, 30, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT, TEAL, 'View', BLACK)
buttons.append(view_button)

# buttons for individual layers
layer_buttons = []
for i in range(GRID_STACK.MAX_LAYERS):
    layer_buttons.append(Button(RIGHT_TOOLBAR_CENTER - 10, 80 + 50 * i, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT,
                                ORANGE, f'Layer{i + 1}', BLACK))
buttons.append(layer_buttons[0])

# buttons for selecting the layers
layer_button_checkboxes = []
for i in range(GRID_STACK.MAX_LAYERS):
    layer_button_checkboxes.append(Button(RIGHT_TOOLBAR_CENTER - 30, 93 + 50 * i, SMALL_BUTTON_WIDTH,
                                          SMALL_BUTTON_HEIGHT, RED, '', BLACK, name=f'Checkbox Layer {i + 1}'))
buttons.append(layer_button_checkboxes[0])

# button for adding layers
add_button = Button(RIGHT_TOOLBAR_CENTER - 10, 130, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT, FUCHSIA, '+', BLACK)
buttons.append(add_button)

# button for deleting layers
delete_button = Button(RIGHT_TOOLBAR_CENTER - 48, 350, MEDIUM_BUTTON_WIDTH, MEDIUM_BUTTON_HEIGHT, GRAY, 'Delete', BLACK)
buttons.append(delete_button)

# button for merging layers
merge_button = Button(RIGHT_TOOLBAR_CENTER - 16, 350, MEDIUM_BUTTON_WIDTH, MEDIUM_BUTTON_HEIGHT, GRAY, 'Merge', BLACK)
buttons.append(merge_button)

# button for swapping layers
swap_button = Button(RIGHT_TOOLBAR_CENTER + 16, 350, MEDIUM_BUTTON_WIDTH, MEDIUM_BUTTON_HEIGHT, GRAY, 'Swap', BLACK)
buttons.append(swap_button)

# run infinite loop
while run:
    # limiting FPS to 60 or any other value
    clock.tick(FPS)

    # check every event that happens
    for event in pygame.event.get():

        # if user closed the program
        if event.type == pygame.QUIT:
            run = False

        # if user clicked on the left mouse button
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            # get coordinates of mouse click
            try:
                row, col = HF.get_row_col_from_pos(pos)

                # if user is not in view mode
                if CURRENT_LAYER != -1:

                    # paint individual cells
                    if STATE == "COLOR":
                        HF.paint_using_brush(row, col, grid, drawing_color, BRUSH_SIZE)

                    # paint using bucket
                    elif STATE == "FILL":
                        HF.fill_bucket(row, col, drawing_color, grid)

            # exception thrown when user did not click on canvas
            except IndexError:

                # loop through button list to check if user clicked any button
                for button in buttons:

                    # do nothing if no button was clicked
                    if not button.clicked(pos):
                        continue

                    # if clear button was clicked
                    if button.text == "Clear":
                        grid = HF.init_grid(ROWS, COLS, BG_COLOR)
                        drawing_color = BLACK
                        draw_button.color = drawing_color
                        STATE = "COLOR"
                        break

                    # if fill bucket button was clicked
                    if button.name == "FillBucket":
                        STATE = "FILL"
                        break

                    # if add layer button was clicked
                    if button.text == '+':
                        buttons.append(layer_buttons[GRID_STACK.num_layers])
                        buttons.append(layer_button_checkboxes[GRID_STACK.num_layers])
                        GRID_STACK.add_layer()
                        add_button.y += 50
                        if GRID_STACK.num_layers == 5:
                            buttons.remove(add_button)
                        break

                    # if view button was clicked
                    if button.text == 'View':
                        CURRENT_LAYER = -1
                        break

                    # if any of the layer button was clicked
                    if button.text and button.text[:5] == 'Layer':
                        CURRENT_LAYER = int(button.text[-1]) - 1
                        grid = GRID_STACK.grid_stack[CURRENT_LAYER]
                        break

                    # if any of the checkbox button was clicked
                    if button.name and button.name[:8] == 'Checkbox':
                        layer_clicked = int(button.name[-1]) - 1
                        if layer_clicked in SELECTED_LAYERS:
                            SELECTED_LAYERS.remove(layer_clicked)
                            layer_button_checkboxes[layer_clicked].color = RED
                        else:
                            SELECTED_LAYERS.append(layer_clicked)
                            layer_button_checkboxes[layer_clicked].color = GREEN
                        break

                    # if the delete button was clicked
                    if button.text == 'Delete':
                        if GRID_STACK.num_layers - len(SELECTED_LAYERS) < 1 or not SELECTED_LAYERS:
                            break

                        # removing extra layer buttons and their checkmarks
                        for i in range(len(SELECTED_LAYERS)):
                            buttons.remove(layer_buttons[GRID_STACK.num_layers - 1 - i])
                            buttons.remove(layer_button_checkboxes[GRID_STACK.num_layers - 1 - i])

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

                    # if the delete button was clicked
                    if button.text == 'Merge':
                        if GRID_STACK.num_layers == 1 or not SELECTED_LAYERS:
                            break

                        # removing extra layer buttons and their checkmarks
                        for i in range(len(SELECTED_LAYERS) - 1):
                            buttons.remove(layer_buttons[GRID_STACK.num_layers - 1 - i])
                            buttons.remove(layer_button_checkboxes[GRID_STACK.num_layers - 1 - i])

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

                    # if the swap button was clicked
                    if button.text == 'Swap':
                        # don't do anything if exactly two layers were not selected
                        if len(SELECTED_LAYERS) != 2:
                            break

                        # swap the layers
                        GRID_STACK.swap_layers(SELECTED_LAYERS[0], SELECTED_LAYERS[1])
                        break

                    # is small brush width was clicked
                    if button.name == 'small_width':
                        # set brush size to small and mode to color
                        BRUSH_SIZE = 1
                        STATE = "COLOR"
                        break

                    # is medium brush width was clicked
                    elif button.name == 'medium_width':
                        # set brush size to medium and mode to color
                        BRUSH_SIZE = 2
                        STATE = "COLOR"
                        break

                    # if large brush width was clicked
                    elif button.name == 'large_width':
                        # set the brush size to large and mode to color
                        BRUSH_SIZE = 3
                        STATE = "COLOR"
                        break

                    # change the drawing color if any color button was clicked
                    drawing_color = button.color
                    draw_button.color = drawing_color

                    break

    # draw changes on the canvas
    HF.draw(WIN, buttons, arrow_button, CURRENT_LAYER, GRID_STACK, SIZE_SMALL, SIZE_MEDIUM, SIZE_LARGE, BRUSH_SIZE)

pygame.quit()
