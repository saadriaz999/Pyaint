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
        self.show_selected_button = Button(WIDTH, 25, RIGHT_TOOLBAR_WIDTH, LARGE_BUTTON_HEIGHT + 10, LIME,
                                           name='show_selected')
        self.buttons.append(self.show_selected_button)

        # button to view entire stack
        self.view_button = Button(RIGHT_TOOLBAR_CENTER - 10, 30, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT, TEAL, 'View',
                                  BLACK)
        self.buttons.append(self.view_button)

        # buttons for individual layers
        self.layer_buttons = []
        for i in range(self.grid_stack.MAX_LAYERS):
            self.layer_buttons.append(Button(RIGHT_TOOLBAR_CENTER - 10, 80 + 50 * i, LARGE_BUTTON_WIDTH,
                                             LARGE_BUTTON_HEIGHT, ORANGE, f'Layer{i + 1}', BLACK))
        self.buttons.append(self.layer_buttons[0])

        # buttons for selecting the layers
        self.layer_button_checkboxes = []
        for i in range(self.grid_stack.MAX_LAYERS):
            self.layer_button_checkboxes.append(Button(RIGHT_TOOLBAR_CENTER - 30, 93 + 50 * i, SMALL_BUTTON_WIDTH,
                                                SMALL_BUTTON_HEIGHT, RED, '', BLACK, name=f'Checkbox Layer {i + 1}'))
        self.buttons.append(self.layer_button_checkboxes[0])

        # button for adding layers
        self.add_button = Button(RIGHT_TOOLBAR_CENTER - 10, 130, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT, FUCHSIA, '+',
                                 BLACK)
        self.buttons.append(self.add_button)

        # button for deleting layers
        self.delete_button = Button(RIGHT_TOOLBAR_CENTER - 48, 350, MEDIUM_BUTTON_WIDTH, MEDIUM_BUTTON_HEIGHT, GRAY,
                                    'Delete', BLACK)
        self.buttons.append(self.delete_button)

        # button for merging layers
        self.merge_button = Button(RIGHT_TOOLBAR_CENTER - 16, 350, MEDIUM_BUTTON_WIDTH, MEDIUM_BUTTON_HEIGHT, GRAY,
                                   'Merge', BLACK)
        self.buttons.append(self.merge_button)

        # button for swapping layers
        self.swap_button = Button(RIGHT_TOOLBAR_CENTER + 16, 350, MEDIUM_BUTTON_WIDTH, MEDIUM_BUTTON_HEIGHT, GRAY,
                                  'Swap', BLACK)
        self.buttons.append(self.swap_button)

    def update_drawing_color(self, color):
        self.drawing_color = color
