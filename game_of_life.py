import pygame
import numpy as np


class GameOfLife:
    def __init__(self):
        # COLORS
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREY = (128, 128, 128)

        pygame.init()
        self.mode = "Auto"
        self.win_size = (1200, 600)
        self.window = pygame.display.set_mode(self.win_size)
        pygame.display.set_caption(f"Game of Life - {self.mode} Mode")
        pygame.display.update()

        self.grid_size = 10
        self.grid = np.zeros(shape=(self.win_size[0]//self.grid_size, (self.win_size[1]-60)//self.grid_size), dtype=bool)
        self.running = True
        self.gen = 1
        self.change_gen_list = [1, 2, 3, 4, 5, 10, 20, 30, 50, 60]
        self.change_gen = self.change_gen_list[0]
        self.auto_play = False
        self.clock = pygame.time.Clock()
        self.show_grid = True

        self.main()

    def get_grid(self, x, y):
        grid = (y//self.grid_size, x//self.grid_size)
        return grid

    def create_life(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                self.grid[i][j] = np.random.choice([True, False], p=[0.3, 0.7])

    def next_gen(self):
        alive_mat = np.zeros(shape=self.grid.shape, dtype='int8')
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                alive_c = 0
                if i != 0 and j != 0 and self.grid[i-1][j-1]:
                    alive_c += 1
                if i != 0 and self.grid[i-1][j]:
                    alive_c += 1
                if i != 0 and j != len(self.grid[i]) - 1 and self.grid[i-1][j+1]:
                    alive_c += 1
                if j != 0 and self.grid[i][j-1]:
                    alive_c += 1
                if j != len(self.grid[i]) - 1 and self.grid[i][j+1]:
                    alive_c += 1
                if i != len(self.grid) - 1 and j != 0 and self.grid[i+1][j-1]:
                    alive_c += 1
                if i != len(self.grid) - 1 and self.grid[i+1][j]:
                    alive_c += 1
                if i != len(self.grid) - 1 and j != len(self.grid[i]) - 1 and self.grid[i+1][j+1]:
                    alive_c += 1
                alive_mat[i][j] = alive_c

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] and (alive_mat[i][j] < 2 or alive_mat[i][j] > 3):
                    self.grid[i][j] = False
                else:
                    if alive_mat[i][j] == 3:
                        self.grid[i][j] = True

    def add_text(self, text, size, color, x, y):
        font = pygame.font.SysFont(None, size)
        screen_text = font.render(text, True, color)
        self.window.blit(screen_text, [x, y])

    def draw_grid(self):
        grid_color = self.GREY
        x_lim, y_lim = self.win_size[0], self.win_size[1] - 60

        for x in range(0, x_lim, self.grid_size):
            pygame.draw.line(self.window, grid_color, (x, 0), (x, y_lim))
        for y in range(0, y_lim, self.grid_size):
            pygame.draw.line(self.window, grid_color, (0, y), (x_lim, y))
        pygame.draw.line(self.window, grid_color, (0, y_lim), (x_lim, y_lim))

    def draw_life(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j]:
                    pygame.draw.rect(self.window, self.BLACK, (i * self.grid_size, j * self.grid_size, self.grid_size, self.grid_size))

    def main(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.mode == "Auto":
                            self.create_life()
                        elif self.mode == "Manual":
                            self.grid = np.zeros(shape=(self.win_size[0] // self.grid_size, (self.win_size[1] - 60) // self.grid_size), dtype=bool)
                        self.gen = 1
                    elif event.key == pygame.K_1:
                        self.mode = "Auto"
                        pygame.display.set_caption(f"Game of Life - {self.mode} Mode")
                    elif event.key == pygame.K_2:
                        self.mode = "Manual"
                        pygame.display.set_caption(f"Game of Life - {self.mode} Mode")
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.change_gen = self.change_gen_list[0] if self.change_gen == 'On Press' else 'On Press'
                        if self.change_gen == 'On Press':
                            self.auto_play = False
                    elif self.change_gen != 'On Press' and event.key == pygame.K_LEFT:
                        ind = self.change_gen_list.index(self.change_gen)
                        if ind == 0:
                            self.change_gen = self.change_gen_list[-1]
                        else:
                            self.change_gen = self.change_gen_list[ind - 1]
                    elif self.change_gen != 'On Press' and event.key == pygame.K_RIGHT:
                        ind = self.change_gen_list.index(self.change_gen)
                        if ind == len(self.change_gen_list) - 1:
                            self.change_gen = self.change_gen_list[0]
                        else:
                            self.change_gen = self.change_gen_list[ind + 1]
                    if event.key == pygame.K_RETURN:
                        if self.change_gen != 'On Press':
                            self.auto_play = False if self.auto_play else True
                        else:
                            self.next_gen()
                            self.auto_play = False
                            self.gen += 1
                    if event.key == pygame.K_TAB:
                        self.show_grid = False if self.show_grid else True
                if event.type == pygame.MOUSEBUTTONDOWN and self.mode == 'Manual':
                    if event.button == 1:
                        x, y = pygame.mouse.get_pos()
                        y, x = self.get_grid(x, y)
                        self.grid[x][y] = False if self.grid[x][y] else True

            self.window.fill(self.WHITE)
            self.draw_life()
            if self.show_grid:
                self.draw_grid()

            self.add_text(text=f"Generation: {self.gen}", size=25, color=self.BLACK, x=30, y=self.win_size[1]-40)
            self.add_text(text=f"Gen change: {self.change_gen if self.change_gen=='On Press' else str(self.change_gen)+' FPS'}", size=25, color=self.BLACK, x=250, y=self.win_size[1]-40)
            pygame.display.update()

            if self.auto_play:
                self.gen += 1
                self.next_gen()
                self.clock.tick(self.change_gen)


if __name__ == '__main__':
    GameOfLife()
