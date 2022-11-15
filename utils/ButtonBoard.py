from utils import *


class ButtonBoard:

    def __init__(self, grid_stack):
        self.grid_stack = grid_stack
        self.drawing_color = BLACK
        self.buttons = []

        # top layer of color buttons
        for i in range(int(len(COLORS) / 2)):
            self.buttons.append(Button(100 + MEDIUM_BUTTON_SPACE * i, BUTTON_Y_TOP_ROW - 14, MEDIUM_BUTTON_WIDTH,
                                       MEDIUM_BUTTON_HEIGHT, COLORS[i]))

        # bottom layer of colour buttons
        for i in range(int(len(COLORS) / 2)):
            self.buttons.append(Button(100 + MEDIUM_BUTTON_SPACE * i, BUTTON_Y_BOT_ROW - 14, MEDIUM_BUTTON_WIDTH,
                                       MEDIUM_BUTTON_HEIGHT, COLORS[i + int(len(COLORS) / 2)]))

        # button showing the current chosen color
        self.draw_button = Button(5, HEIGHT - TOOLBAR_HEIGHT / 2 - 30, 60, 60, self.drawing_color)
        self.buttons.append(self.draw_button)

        # buttons to choose paint brush width
        self.small_brush_width_button = Button(RIGHT_TOOLBAR_CENTER - SIZE_SMALL / 2, 480, SIZE_SMALL, SIZE_SMALL,
                                               BLACK, None, shape="ellipse", name='small_width')
        self.medium_brush_width_button = Button(RIGHT_TOOLBAR_CENTER - SIZE_MEDIUM / 2, 510, SIZE_MEDIUM, SIZE_MEDIUM,
                                                self.drawing_color, None, shape="ellipse", name='medium_width')
        self.large_brush_width_button = Button(RIGHT_TOOLBAR_CENTER - SIZE_LARGE / 2, 550, SIZE_LARGE, SIZE_LARGE,
                                               self.drawing_color, None, shape="ellipse", name='large_width')

        self.buttons.append(self.small_brush_width_button)
        self.buttons.append(self.medium_brush_width_button)
        self.buttons.append(self.large_brush_width_button)

        # button to erase from canvas
        self.erase_button = Button(WIDTH - 2 * LARGE_BUTTON_SPACE, BUTTON_Y_TOP_ROW, LARGE_BUTTON_WIDTH,
                                   LARGE_BUTTON_HEIGHT, WHITE, "Erase", BLACK)
        self.buttons.append(self.erase_button)

        # button to clear canvas
        self.clear_button = Button(WIDTH - LARGE_BUTTON_SPACE, BUTTON_Y_TOP_ROW, LARGE_BUTTON_WIDTH,
                                   LARGE_BUTTON_HEIGHT, WHITE, "Clear", BLACK)
        self.buttons.append(self.clear_button)

        # fill bucket button
        self.fill_bucket_button = Button(WIDTH - 3 * LARGE_BUTTON_SPACE - 10, BUTTON_Y_TOP_ROW, LARGE_BUTTON_WIDTH,
                                         LARGE_BUTTON_HEIGHT, name="FillBucket", image_url="assets/paint-bucket.png")
        self.buttons.append(self.fill_bucket_button)

        # button to show which layer is currently viewing
        self.show_selected_button = Button(WIDTH + 2, 25, RIGHT_TOOLBAR_WIDTH - 3, LARGE_BUTTON_HEIGHT + 10, LIME,
                                           name='show_selected')
        self.buttons.append(self.show_selected_button)

        # button to view entire stack
        self.view_button = Button(RIGHT_TOOLBAR_CENTER + 5, 30, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT,
                                  TEAL, 'View', BLACK)

        # buttons for individual layers
        self.layer_buttons = []
        for i in range(self.grid_stack.get_max_num_layers()):
            self.layer_buttons.append(Button(RIGHT_TOOLBAR_CENTER + 5, 80 + 50 * i, LARGE_BUTTON_WIDTH,
                                             LARGE_BUTTON_HEIGHT, ORANGE, f'{i + 1}', BLACK, name=f'Layer{i + 1}'))
        self.buttons.append(self.layer_buttons[0])

        # buttons for selecting the layers
        self.layer_button_checkboxes = []
        for i in range(self.grid_stack.get_max_num_layers()):
            self.layer_button_checkboxes.append(Button(RIGHT_TOOLBAR_CENTER - 12, 93 + 50 * i, SMALL_BUTTON_WIDTH,
                                                SMALL_BUTTON_HEIGHT, RED, '', BLACK, name=f'Checkbox Layer {i + 1}'))
        self.buttons.append(self.layer_button_checkboxes[0])

        # buttons for moving layers up
        self.move_up_buttons = []
        for i in range(self.grid_stack.get_max_num_layers()):
            self.move_up_buttons.append(Button(RIGHT_TOOLBAR_CENTER - 30, 96 + 50 * i, MEDIUM_BUTTON_WIDTH,
                                        MEDIUM_BUTTON_HEIGHT, NAVY, shape='up_arrow', name=f'Move Up {i + 1}'))
        self.buttons.append(self.move_up_buttons[0])

        # buttons for moving layers down
        self.move_down_buttons = []
        for i in range(self.grid_stack.get_max_num_layers()):
            self.move_down_buttons.append(Button(RIGHT_TOOLBAR_CENTER - 30, 103 + 50 * i, MEDIUM_BUTTON_WIDTH,
                                          MEDIUM_BUTTON_HEIGHT, NAVY, shape='down_arrow',
                                          name=f'Move Down {i + 1}'))
        self.buttons.append(self.move_down_buttons[0])

        # button for adding layers
        self.add_button = Button(RIGHT_TOOLBAR_CENTER + 5, 130, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT, FUCHSIA, '+',
                                 BLACK)
        self.buttons.append(self.add_button)

        # buttons for toggling invisibility
        self.toggle_invisibility_button = Button(RIGHT_TOOLBAR_CENTER - 37, 392, LARGE_BUTTON_WIDTH,
                                                 LARGE_BUTTON_HEIGHT, GRAY, 'Visible', BLACK)
        self.buttons.append(self.toggle_invisibility_button)

        # button for deleting layers
        self.delete_button = Button(RIGHT_TOOLBAR_CENTER - 37, 350, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT, GRAY,
                                    'Delete', BLACK)
        self.buttons.append(self.delete_button)

        # button for merging layers
        self.merge_button = Button(RIGHT_TOOLBAR_CENTER + 5, 350, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT, GRAY,
                                   'Merge', BLACK)
        self.buttons.append(self.merge_button)

        # button for swapping layers
        self.swap_button = Button(RIGHT_TOOLBAR_CENTER + 5, 392, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT, GRAY,
                                  'Swap', BLACK)
        self.buttons.append(self.swap_button)

    def update_drawing_color(self, color):
        self.drawing_color = color
