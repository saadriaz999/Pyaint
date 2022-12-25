from utils import *
from utils.HelperFunctions import HelperFunctions
from utils.ButtonBoard import ButtonBoard

# setting display caption
pygame.display.set_caption('Pyaint')

# initializing the window
WIN = pygame.display.set_mode((WIDTH + RIGHT_TOOLBAR_WIDTH, HEIGHT))

# initializing the grid stack (layers of canvas)
GRID_STACK = GridStack(ROWS, COLS, BG_COLOR)

# initializing a button board to keep track of all buttons
BUTTON_BOARD = ButtonBoard(GRID_STACK)

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
INVISIBLE_LAYERS = []
CURRENT_LAYER = 0
grid = GRID_STACK.get_grid_stack_layer(CURRENT_LAYER)

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

                # paint individual cells
                if STATE == "COLOR":
                    if CURRENT_LAYER not in INVISIBLE_LAYERS:
                        HF.paint_using_brush(row, col, grid, drawing_color, BRUSH_SIZE)

                # paint using bucket
                elif STATE == "FILL":
                    HF.fill_bucket(row, col, drawing_color, grid)

            # exception thrown when user did not click on canvas
            except IndexError:

                # loop through button list to check if user clicked any button
                for button in BUTTON_BOARD.buttons:

                    # do nothing if no button was clicked
                    if not button.clicked(pos):
                        continue

                    # if clear button was clicked
                    if button.text == "Clear":
                        drawing_color = BLACK
                        BUTTON_BOARD.draw_button.color = drawing_color
                        GRID_STACK = GridStack(ROWS, COLS, BG_COLOR)
                        SELECTED_LAYERS = []
                        CURRENT_LAYER = 0
                        grid = GRID_STACK.get_grid_stack_layer(CURRENT_LAYER)
                        STATE = "COLOR"

                        # removing additional layer and checkbox buttons
                        for i in range(1, GRID_STACK.get_max_num_layers()):
                            # removing layer buttons
                            if BUTTON_BOARD.layer_buttons[i] in BUTTON_BOARD.buttons:
                                BUTTON_BOARD.buttons.remove(BUTTON_BOARD.layer_buttons[i])

                            # removing checkboxes
                            if BUTTON_BOARD.layer_button_checkboxes[i] in BUTTON_BOARD.buttons:
                                BUTTON_BOARD.buttons.remove(BUTTON_BOARD.layer_button_checkboxes[i])

                            # removing up buttons
                            if BUTTON_BOARD.move_up_buttons[i] in BUTTON_BOARD.buttons:
                                BUTTON_BOARD.buttons.remove(BUTTON_BOARD.move_up_buttons[i])

                            # removing down buttons
                            if BUTTON_BOARD.move_down_buttons[i] in BUTTON_BOARD.buttons:
                                BUTTON_BOARD.buttons.remove(BUTTON_BOARD.move_down_buttons[i])

                        # adjusting the add layer button checkbox for first layer
                        BUTTON_BOARD.add_button.y = 130
                        BUTTON_BOARD.layer_button_checkboxes[0].color = RED

                        break

                    # if fill bucket button was clicked
                    if button.name == "FillBucket":
                        STATE = "FILL"
                        break

                    # if add layer button was clicked
                    if button.text == '+':
                        BUTTON_BOARD.buttons.append(BUTTON_BOARD.layer_buttons[GRID_STACK.get_num_layers()])
                        BUTTON_BOARD.buttons.append(BUTTON_BOARD.layer_button_checkboxes[GRID_STACK.get_num_layers()])
                        BUTTON_BOARD.buttons.append(BUTTON_BOARD.move_up_buttons[GRID_STACK.get_num_layers()])
                        BUTTON_BOARD.buttons.append(BUTTON_BOARD.move_down_buttons[GRID_STACK.get_num_layers()])
                        GRID_STACK.add_layer()
                        BUTTON_BOARD.add_button.y += 50
                        if GRID_STACK.get_num_layers() == 5:
                            BUTTON_BOARD.buttons.remove(BUTTON_BOARD.add_button)
                        break

                    # if any of the layer button was clicked
                    if button.name and button.name[:5] == 'Layer':
                        CURRENT_LAYER = int(button.name[-1]) - 1
                        grid = GRID_STACK.get_grid_stack_layer(CURRENT_LAYER)
                        break

                    # if any of the checkbox button was clicked
                    if button.name and button.name[:8] == 'Checkbox':
                        layer_clicked = int(button.name[-1]) - 1
                        if layer_clicked in SELECTED_LAYERS:
                            SELECTED_LAYERS.remove(layer_clicked)
                            BUTTON_BOARD.layer_button_checkboxes[layer_clicked].color = RED
                        else:
                            SELECTED_LAYERS.append(layer_clicked)
                            BUTTON_BOARD.layer_button_checkboxes[layer_clicked].color = GREEN

                        break

                    # if any of the move down button was clicked
                    if button.name and button.name[:7] == 'Move Up':
                        layer_clicked = int(button.name[-1]) - 1

                        # do nothing if top layer was selected
                        if layer_clicked == 0:
                            pass

                        # swap layer and button names
                        else:
                            temp = BUTTON_BOARD.layer_buttons[layer_clicked].text
                            BUTTON_BOARD.layer_buttons[layer_clicked].text = BUTTON_BOARD.layer_buttons[layer_clicked - 1].text
                            BUTTON_BOARD.layer_buttons[layer_clicked - 1].text = temp

                            GRID_STACK.swap_layers(layer_clicked, layer_clicked - 1)
                            CURRENT_LAYER = layer_clicked - 1

                        break

                    # if any of the move down button was clicked
                    if button.name and button.name[:9] == 'Move Down':
                        layer_clicked = int(button.name[-1]) - 1

                        # do nothing if bottom layer was selected
                        if layer_clicked == GRID_STACK.get_num_layers() - 1:
                            pass

                        # swap layer
                        else:
                            temp = BUTTON_BOARD.layer_buttons[layer_clicked].text
                            BUTTON_BOARD.layer_buttons[layer_clicked].text = BUTTON_BOARD.layer_buttons[layer_clicked+1].text
                            BUTTON_BOARD.layer_buttons[layer_clicked + 1].text = temp

                            GRID_STACK.swap_layers(layer_clicked, layer_clicked + 1)
                            CURRENT_LAYER = layer_clicked + 1

                        break

                    # if the delete button was clicked
                    if button.text == 'Delete':
                        if GRID_STACK.get_num_layers() - len(SELECTED_LAYERS) < 1 or not SELECTED_LAYERS:
                            break

                        # removing extra layer buttons and their checkmarks
                        top_layer = min(SELECTED_LAYERS)
                        for i in range(len(SELECTED_LAYERS)):
                            BUTTON_BOARD.buttons.remove(BUTTON_BOARD.layer_buttons
                                                        [GRID_STACK.get_num_layers() - 1 - i])
                            BUTTON_BOARD.buttons.remove(BUTTON_BOARD.layer_button_checkboxes
                                                        [GRID_STACK.get_num_layers() - 1 - i])
                            BUTTON_BOARD.buttons.remove(BUTTON_BOARD.move_up_buttons
                                                        [GRID_STACK.get_num_layers() - 1 - i])
                            BUTTON_BOARD.buttons.remove(BUTTON_BOARD.move_down_buttons
                                                        [GRID_STACK.get_num_layers() - 1 - i])

                        # delete layer from __visible_grid_stack object
                        SELECTED_LAYERS.sort(reverse=True)
                        for layer in SELECTED_LAYERS:
                            GRID_STACK.delete_layer(layer)

                        # adding the add-layer button
                        if SELECTED_LAYERS:
                            BUTTON_BOARD.add_button.y = 80 + 50 * GRID_STACK.get_num_layers()

                        # unchecking all checkbox buttons
                        for check_button in BUTTON_BOARD.layer_button_checkboxes:
                            check_button.color = RED

                        # unchecking all selected layers in from the backend
                        SELECTED_LAYERS = []
                        CURRENT_LAYER = top_layer

                        # adding the add button to button list if number of layers less than 5
                        if GRID_STACK.get_num_layers() < 5:
                            if BUTTON_BOARD.add_button not in BUTTON_BOARD.buttons:
                                BUTTON_BOARD.buttons.append(BUTTON_BOARD.add_button)

                        break

                    # if the delete button was clicked
                    if button.text == 'Merge':
                        if GRID_STACK.get_num_layers() == 1 or not SELECTED_LAYERS:
                            break

                        # removing extra layer buttons and their checkmarks
                        top_layer = min(SELECTED_LAYERS)
                        for i in range(len(SELECTED_LAYERS) - 1):
                            BUTTON_BOARD.buttons.remove(BUTTON_BOARD.layer_buttons
                                                        [GRID_STACK.get_num_layers() - 1 - i])
                            BUTTON_BOARD.buttons.remove(BUTTON_BOARD.layer_button_checkboxes
                                                        [GRID_STACK.get_num_layers() - 1 - i])
                            BUTTON_BOARD.buttons.remove(BUTTON_BOARD.move_up_buttons
                                                        [GRID_STACK.get_num_layers() - 1 - i])
                            BUTTON_BOARD.buttons.remove(BUTTON_BOARD.move_down_buttons
                                                        [GRID_STACK.get_num_layers() - 1 - i])

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
                            BUTTON_BOARD.add_button.y = 80 + 50 * GRID_STACK.get_num_layers()

                        # unchecking all checkbox buttons
                        for check_button in BUTTON_BOARD.layer_button_checkboxes:
                            check_button.color = RED

                        # unchecking all selected layers in from the backend
                        SELECTED_LAYERS = []
                        CURRENT_LAYER = top_layer

                        # adding the add button to button list if number of layers less than 5
                        if GRID_STACK.get_num_layers() < 5:
                            if BUTTON_BOARD.add_button not in BUTTON_BOARD.buttons:
                                BUTTON_BOARD.buttons.append(BUTTON_BOARD.add_button)

                        break

                    # if the swap button was clicked
                    if button.text == 'Swap':
                        # don't do anything if exactly two layers were not selected
                        if len(SELECTED_LAYERS) != 2:
                            break

                        # swap the layers
                        GRID_STACK.swap_layers(SELECTED_LAYERS[0], SELECTED_LAYERS[1])
                        grid = GRID_STACK.get_grid_stack_layer(CURRENT_LAYER)
                        break

                    # if the toggle invisibility button was clicked
                    if button.text == 'Visible':
                        for layer in SELECTED_LAYERS:
                            # toggle button color
                            if BUTTON_BOARD.layer_buttons[layer].color == ORANGE:
                                BUTTON_BOARD.layer_buttons[layer].color = LIGHT_ORANGE
                            else:
                                BUTTON_BOARD.layer_buttons[layer].color = ORANGE

                            # toggle layer invisibility
                            GRID_STACK.toggle_layer_invisibility(layer)

                            # adding layer to invisible layers if needed
                            if layer in INVISIBLE_LAYERS:
                                INVISIBLE_LAYERS.remove(layer)
                            else:
                                INVISIBLE_LAYERS.append(layer)

                        break

                    # is small brush width was clicked
                    if button.name == 'small_width':
                        # set brush size to small and mode to color
                        BRUSH_SIZE = 1
                        STATE = "COLOR"
                        break

                    # is medium brush width was clicked
                    if button.name == 'medium_width':
                        # set brush size to medium and mode to color
                        BRUSH_SIZE = 2
                        STATE = "COLOR"
                        break

                    # if large brush width was clicked
                    if button.name == 'large_width':
                        # set the brush size to large and mode to color
                        BRUSH_SIZE = 3
                        STATE = "COLOR"
                        break

                    # change the drawing color if any color button was clicked
                    if button.name != 'show_selected':
                        drawing_color = button.color
                        BUTTON_BOARD.draw_button.color = drawing_color
                        BUTTON_BOARD.drawing_color = drawing_color

                        break

    # draw changes on the canvas
    HF.draw(WIN, BUTTON_BOARD.buttons, BUTTON_BOARD.show_selected_button, CURRENT_LAYER, GRID_STACK, SIZE_SMALL,
            SIZE_MEDIUM, SIZE_LARGE, BRUSH_SIZE)

pygame.quit()
