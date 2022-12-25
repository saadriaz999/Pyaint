from utils.Settings import *


class HelperFunctions:

    @classmethod
    def init_grid(cls, rows, columns, color):
        grid = []

        for i in range(rows):
            grid.append([])
            for _ in range(columns):  # use _ when variable is not required
                grid[i].append(color)
        return grid

    @classmethod
    def draw_grid(cls, win, arrow_button, current_layer, grid_stack):
        # showing the arrow beside the current selected layer
        arrow_button.y = 75 + current_layer * 50

        grid = grid_stack.show_merged_stack_view()

        for i, row in enumerate(grid):
            for j, pixel in enumerate(row):
                pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

        if DRAW_GRID_LINES:
            for i in range(ROWS + 1):
                pygame.draw.line(win, SILVER, (0, i * PIXEL_SIZE), (WIDTH, i * PIXEL_SIZE))
            for i in range(COLS + 1):
                pygame.draw.line(win, SILVER, (i * PIXEL_SIZE, 0), (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))

    @classmethod
    def draw_mouse_position_text(cls, win, buttons):
        pos = pygame.mouse.get_pos()
        pos_font = get_font(MOUSE_POSITION_TEXT_SIZE)
        try:
            row, col = cls.get_row_col_from_pos(pos)
            text_surface = pos_font.render(str(row) + ", " + str(col), 1, BLACK)
            win.blit(text_surface, (5, HEIGHT - TOOLBAR_HEIGHT))
        except IndexError:
            for button in buttons:
                if not button.hover(pos):
                    continue

                if button.text == "Clear":
                    text_surface = pos_font.render("Clear Everything", 1, BLACK)
                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                    break
                if button.text == "Erase":
                    text_surface = pos_font.render("Erase", 1, BLACK)
                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                    break

                if button.name == 'small_width':
                    text_surface = pos_font.render("Small-Sized Brush", 1, BLACK)
                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                    break
                if button.name == 'medium_width':
                    text_surface = pos_font.render("Medium-Sized Brush", 1, BLACK)
                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                    break
                if button.name == 'large_width':
                    text_surface = pos_font.render("Large-Sized Brush", 1, BLACK)
                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                    break
                if button.text == 'Delete':
                    text_surface = pos_font.render("Delete Layer(s)", 1, BLACK)
                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                    break
                if button.text == 'Merge':
                    text_surface = pos_font.render("Merge Layer(s)", 1, BLACK)
                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                    break
                if button.text == 'Visible':
                    text_surface = pos_font.render("Toggle Visibility", 1, BLACK)
                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                    break
                if button.text == 'Swap':
                    text_surface = pos_font.render("Swap Layers", 1, BLACK)
                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                    break
                if button.text == '+':
                    text_surface = pos_font.render("Add Layer", 1, BLACK)
                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                    break
                if button.name and button.name[:5] == 'Layer':
                    text_surface = pos_font.render("Edit Layer", 1, BLACK)
                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                    break
                if button.name and button.name[:8] == 'Checkbox':
                    text_surface = pos_font.render("Select Layer", 1, BLACK)
                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                    break
                if button.name and button.name[:8] == 'Checkbox':
                    text_surface = pos_font.render("Fill Bucket", 1, BLACK)
                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                    break

                if button.name and button.name == 'show_selected' or \
                        button.name and button.name[:7] == 'Move Up' or \
                        button.name and button.name[:9] == 'Move Down':
                    pass
                else:
                    r, g, b = button.color
                    text_surface = pos_font.render("( " + str(r) + ", " + str(g) + ", " + str(b) + " )", 1, BLACK)

                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))

    @classmethod
    def draw_brush_widths(cls, win, size_small, size_medium, size_large, buttons, brush_size):
        for button in buttons:
            if button.name and button.name[-5:] == 'width':
                # Set border colour
                if button.color == BLACK:
                    border_color = GRAY
                else:
                    border_color = BLACK
                # Set border width
                if ((brush_size == 1 and button.width == size_small) or (
                        brush_size == 2 and button.width == size_medium) or (
                        brush_size == 3 and button.width == size_large)):
                    border_width = 4
                else:
                    border_width = 2
                # Draw border
                pygame.draw.ellipse(win, border_color, (button.x, button.y, button.width, button.height),
                                    border_width)  # border

    @classmethod
    def draw(cls, win, buttons, arrow_button, current_layer, grid_stack, size_small, size_medium,
             size_large, brush_size):

        # this is a wrapper function that calls other functions

        win.fill(BG_COLOR)
        cls.draw_grid(win, arrow_button, current_layer, grid_stack)

        for button in buttons:
            button.draw(win)

        cls.draw_brush_widths(win, size_small, size_medium, size_large, buttons, brush_size)
        cls.draw_mouse_position_text(win, buttons)
        pygame.display.update()

    @classmethod
    def get_row_col_from_pos(cls, position):
        x, y = position
        row = y // PIXEL_SIZE
        col = x // PIXEL_SIZE

        if row >= ROWS:
            raise IndexError
        if col >= ROWS:
            raise IndexError
        return row, col

    @classmethod
    def paint_using_brush(cls, row, col, grid, drawing_color, brush_size):
        if brush_size == 1:
            grid[row][col] = drawing_color
        else:  # for values greater than 1
            r = row - brush_size + 1
            c = col - brush_size + 1

            for i in range(brush_size * 2 - 1):
                for j in range(brush_size * 2 - 1):
                    if r + i < 0 or c + j < 0 or r + i >= ROWS or c + j >= COLS:
                        continue
                    grid[r + i][c + j] = drawing_color

        pass

    @classmethod
    # Checks whether the coordinated are within the canvas
    def check_in_bounds(cls, row, col):
        if row < 0 or col < 0:
            return 0
        if row >= ROWS or col >= COLS:
            return 0
        return 1

    @classmethod
    def fill_bucket(cls, row, col, color, grid):

        # Visiting array
        vis = [[0 for _ in range(101)] for _ in range(101)]

        # Creating queue for bfs
        obj = [[row, col]]

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
            if cls.check_in_bounds(x + 1, y) == 1 and vis[x + 1][y] == 0 and grid[x + 1][y] == preColor:
                obj.append([x + 1, y])
                vis[x + 1][y] = 1

            # For Downside Pixel or Cell
            if cls.check_in_bounds(x - 1, y) == 1 and vis[x - 1][y] == 0 and grid[x - 1][y] == preColor:
                obj.append([x - 1, y])
                vis[x - 1][y] = 1

            # For Right side Pixel or Cell
            if cls.check_in_bounds(x, y + 1) == 1 and vis[x][y + 1] == 0 and grid[x][y + 1] == preColor:
                obj.append([x, y + 1])
                vis[x][y + 1] = 1

            # For Left side Pixel or Cell
            if cls.check_in_bounds(x, y - 1) == 1 and vis[x][y - 1] == 0 and grid[x][y - 1] == preColor:
                obj.append([x, y - 1])
                vis[x][y - 1] = 1
