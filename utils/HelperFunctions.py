from utils import *


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
    def draw_grid(cls, win, grid):
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

    @classmethod
    def draw_mouse_position_text(cls, win):
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
                r, g, b = button.color
                text_surface = pos_font.render("( " + str(r) + ", " + str(g) + ", " + str(b) + " )", 1, BLACK)

                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))

            for button in brush_widths:
                if not button.hover(pos):
                    continue
                if button.width == size_small:
                    text_surface = pos_font.render("Small-Sized Brush", 1, BLACK)
                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                    break
                if button.width == size_medium:
                    text_surface = pos_font.render("Medium-Sized Brush", 1, BLACK)
                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                    break
                if button.width == size_large:
                    text_surface = pos_font.render("Large-Sized Brush", 1, BLACK)
                    win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                    break

    @classmethod
    def draw_brush_widths(cls, win):
        brush_widths = [
            Button(rtb_x - size_small / 2, 480, size_small, size_small, drawing_color, None, None, "ellipse"),
            Button(rtb_x - size_medium / 2, 510, size_medium, size_medium, drawing_color, None, None, "ellipse"),
            Button(rtb_x - size_large / 2, 550, size_large, size_large, drawing_color, None, None, "ellipse")
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
            if ((BRUSH_SIZE == 1 and button.width == size_small) or (
                    BRUSH_SIZE == 2 and button.width == size_medium) or (
                    BRUSH_SIZE == 3 and button.width == size_large)):
                border_width = 4
            else:
                border_width = 2
            # Draw border
            pygame.draw.ellipse(win, border_color, (button.x, button.y, button.width, button.height),
                                border_width)  # border

    @classmethod
    def draw(cls, win, grid, buttons):
        win.fill(BG_COLOR)
        cls.draw_grid(win, grid)

        for button in buttons:
            button.draw(win)

        # draw_button.draw(win)
        cls.draw_brush_widths(win)
        cls.draw_mouse_position_text(win)
        pygame.display.update()

    @classmethod
    def get_row_col_from_pos(cls, pos):
        x, y = pos
        row = y // PIXEL_SIZE
        col = x // PIXEL_SIZE

        if row >= ROWS:
            raise IndexError
        if col >= ROWS:
            raise IndexError
        return row, col

    @classmethod
    def paint_using_brush(cls, row, col, size):
        if BRUSH_SIZE == 1:
            grid[row][col] = drawing_color
        else:  # for values greater than 1
            r = row - BRUSH_SIZE + 1
            c = col - BRUSH_SIZE + 1

            for i in range(BRUSH_SIZE * 2 - 1):
                for j in range(BRUSH_SIZE * 2 - 1):
                    if r + i < 0 or c + j < 0 or r + i >= ROWS or c + j >= COLS:
                        continue
                    grid[r + i][c + j] = drawing_color

        pass

    @classmethod
    # Checks whether the coordinated are within the canvas
    def inBounds(cls, row, col):
        if row < 0 or col < 0:
            return 0
        if row >= ROWS or col >= COLS:
            return 0
        return 1

    @classmethod
    def fill_bucket(cls, row, col, color):

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
            if cls.inBounds(x + 1, y) == 1 and vis[x + 1][y] == 0 and grid[x + 1][y] == preColor:
                obj.append([x + 1, y])
                vis[x + 1][y] = 1

            # For Downside Pixel or Cell
            if cls.inBounds(x - 1, y) == 1 and vis[x - 1][y] == 0 and grid[x - 1][y] == preColor:
                obj.append([x - 1, y])
                vis[x - 1][y] = 1

            # For Right side Pixel or Cell
            if cls.inBounds(x, y + 1) == 1 and vis[x][y + 1] == 0 and grid[x][y + 1] == preColor:
                obj.append([x, y + 1])
                vis[x][y + 1] = 1

            # For Left side Pixel or Cell
            if cls.inBounds(x, y - 1) == 1 and vis[x][y - 1] == 0 and grid[x][y - 1] == preColor:
                obj.append([x, y - 1])
                vis[x][y - 1] = 1
