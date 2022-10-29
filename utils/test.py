# from GridStack import *
# from Settings import *
#
# gs = GridStack(ROWS, COLS, BG_COLOR)
# gs.add_layer()
#
# SELECTED_LAYERS = [9, 5, 2, 6]
# for i in range(len(SELECTED_LAYERS)):
#     if SELECTED_LAYERS[i] > 5:
#         SELECTED_LAYERS[i] -= 1
# print(SELECTED_LAYERS)
#
# # Adding Buttons
# buttons = []
#
# # adding brush width buttons
# small_brush_width_button = Button(RIGHT_TOOLBAR_CENTER - SIZE_SMALL / 2, 480, SIZE_SMALL, SIZE_SMALL,
#                                   BLACK, None, shape="ellipse", name='small_width')
# medium_brush_width_button = Button(RIGHT_TOOLBAR_CENTER - SIZE_MEDIUM / 2, 510, SIZE_MEDIUM, SIZE_MEDIUM,
#                                    drawing_color, None, shape="ellipse", name='medium_width')
# large_brush_width_button = Button(RIGHT_TOOLBAR_CENTER - SIZE_LARGE / 2, 550, SIZE_LARGE, SIZE_LARGE,
#                                   drawing_color, None, shape="ellipse", name='large_width')
#
# buttons.append(small_brush_width_button)
# buttons.append(medium_brush_width_button)
# buttons.append(large_brush_width_button)
#
# # top layer of color buttons
# for i in range(int(len(COLORS) / 2)):
#     buttons.append(Button(100 + MEDIUM_BUTTON_SPACE * i, BUTTON_Y_TOP_ROW - 14, MEDIUM_BUTTON_WIDTH,
#                           MEDIUM_BUTTON_HEIGHT, COLORS[i]))
#
# # bottom layer of colour buttons
# for i in range(int(len(COLORS) / 2)):
#     buttons.append(Button(100 + MEDIUM_BUTTON_SPACE * i, BUTTON_Y_BOT_ROW - 14, MEDIUM_BUTTON_WIDTH,
#                           MEDIUM_BUTTON_HEIGHT, COLORS[i + int(len(COLORS) / 2)]))
#
# # button to erase from canvas
# erase_button = Button(WIDTH - 2 * LARGE_BUTTON_SPACE, BUTTON_Y_TOP_ROW, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT,
#                       WHITE, "Erase", BLACK)
# buttons.append(erase_button)
#
# # button to clear canvas
# clear_button = Button(WIDTH - LARGE_BUTTON_SPACE, BUTTON_Y_TOP_ROW, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT,
#                       WHITE, "Clear", BLACK)
# buttons.append(clear_button)
#
# # fill bucket button
# fill_bucket_button = Button(WIDTH - 3 * LARGE_BUTTON_SPACE - 10, BUTTON_Y_TOP_ROW, LARGE_BUTTON_WIDTH,
#                             LARGE_BUTTON_HEIGHT, name="FillBucket", image_url="assets/paint-bucket.png")
# buttons.append(fill_bucket_button)
#
# # button showing the current chosen button
# draw_button = Button(5, HEIGHT - TOOLBAR_HEIGHT / 2 - 30, 60, 60, drawing_color)
# buttons.append(draw_button)
#
# # arrow button to show which layer is currently viewing
# show_selected_button = Button(RIGHT_TOOLBAR_CENTER + 32, 40, 12, 24, BLACK, name='arrow', shape='left_arrow')
# buttons.append(show_selected_button)
#
# # button to view entire stack
# view_button = Button(RIGHT_TOOLBAR_CENTER - 10, 30, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT, TEAL, 'View', BLACK)
# buttons.append(view_button)
#
# # buttons for individual layers
# layer_buttons = []
# for i in range(GRID_STACK.MAX_LAYERS):
#     layer_buttons.append(Button(RIGHT_TOOLBAR_CENTER - 10, 80 + 50 * i, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT,
#                                 ORANGE, f'Layer{i + 1}', BLACK))
# buttons.append(layer_buttons[0])
#
# # buttons for selecting the layers
# layer_button_checkboxes = []
# for i in range(GRID_STACK.MAX_LAYERS):
#     layer_button_checkboxes.append(Button(RIGHT_TOOLBAR_CENTER - 30, 93 + 50 * i, SMALL_BUTTON_WIDTH,
#                                           SMALL_BUTTON_HEIGHT, RED, '', BLACK, name=f'Checkbox Layer {i + 1}'))
# buttons.append(layer_button_checkboxes[0])
#
# # button for adding layers
# add_button = Button(RIGHT_TOOLBAR_CENTER - 10, 130, LARGE_BUTTON_WIDTH, LARGE_BUTTON_HEIGHT, FUCHSIA, '+', BLACK)
# buttons.append(add_button)
#
# # button for deleting layers
# delete_button = Button(RIGHT_TOOLBAR_CENTER - 48, 350, MEDIUM_BUTTON_WIDTH, MEDIUM_BUTTON_HEIGHT, GRAY, 'Delete', BLACK)
# buttons.append(delete_button)
#
# # button for merging layers
# merge_button = Button(RIGHT_TOOLBAR_CENTER - 16, 350, MEDIUM_BUTTON_WIDTH, MEDIUM_BUTTON_HEIGHT, GRAY, 'Merge', BLACK)
# buttons.append(merge_button)
#
# # button for swapping layers
# swap_button = Button(RIGHT_TOOLBAR_CENTER + 16, 350, MEDIUM_BUTTON_WIDTH, MEDIUM_BUTTON_HEIGHT, GRAY, 'Swap', BLACK)
# buttons.append(swap_button)