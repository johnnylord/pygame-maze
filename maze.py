import pygame
import numpy as np

class MazePlayer(pygame.sprite.Sprite):

    def __init__(self, position, texture, unit):
        super().__init__()
        self.prev_action = None
        self.unit = unit
        self.texture = texture
        self.texture[:, :, :] = np.array([0, 255, 0])
        self.image = pygame.surfarray.make_surface(np.transpose(texture ,(1, 0, 2)))
        self.rect = pygame.Rect(position, self.texture.shape[:2])

    def up(self):
        self.prev_action = pygame.K_UP
        self.rect.move_ip(0, -self.unit)

    def down(self):
        self.prev_action = pygame.K_DOWN
        self.rect.move_ip(0, self.unit)

    def right(self):
        self.prev_action = pygame.K_RIGHT
        self.rect.move_ip(self.unit, 0)

    def left(self):
        self.prev_action = pygame.K_LEFT
        self.rect.move_ip(-self.unit, 0)

    def stepback(self):
        if self.prev_action == pygame.K_UP:
            self.rect.move_ip(0, self.unit)
        elif self.prev_action == pygame.K_DOWN:
            self.rect.move_ip(0, -self.unit)
        elif self.prev_action == pygame.K_RIGHT:
            self.rect.move_ip(-self.unit, 0)
        elif self.prev_action == pygame.K_LEFT:
            self.rect.move_ip(self.unit, 0)


class MazeObstacle(pygame.sprite.Sprite):

    def __init__(self, position, texture):
        super().__init__()
        self.texture = texture
        self.image = pygame.surfarray.make_surface(np.transpose(texture ,(1, 0, 2)))
        self.rect = pygame.Rect(position, self.texture.shape[:2])


class Maze(pygame.sprite.Sprite):

    def __init__(self, position, texture):
        super().__init__()
        self.texture = texture
        self.image = pygame.surfarray.make_surface(np.transpose(texture ,(1, 0, 2)))
        self.rect = pygame.Rect(position, self.texture.shape[:2])


class MazeGame:

    def __init__(self, maze_path, unit):
        self.maze_path = maze_path
        self.unit = unit

        # The following attributes will be initialized later
        self.maze = None
        self.player = None
        self.obstacles = []
        self.exit_point = None

        # Build Maze
        with open(maze_path, "r") as f:
            # Reserve space for maze
            lines = f.read().strip('\n').split('\n') # Read the map
            maze = np.zeros((len(lines)*unit, len(lines[0])*unit, 3)) # (height, width, depth)

            # Initialize maze row by row
            for row, line in enumerate(lines):
                for col, symbol in enumerate(line):
                    if symbol == '@':   # black obstacle
                        # Set the color on this position to black in maze
                        maze[row*unit:row*unit+unit, col*unit:col*unit+unit, :] = 0

                        # Create obstacle
                        obstacle = MazeObstacle(
                                        (col*unit, row*unit),
                                        maze[row*unit:row*unit+unit, col*unit:col*unit+unit, :].copy())
                        self.obstacles.append(obstacle)
                    elif symbol == '#':   # white road
                        # Set the color on this position to white in maze
                        maze[row*unit:row*unit+unit, col*unit:col*unit+unit, :] = 255
                    elif symbol == 'S':   # green starting point
                        # Set the color on this position to white in maze
                        maze[row*unit:row*unit+unit, col*unit:col*unit+unit, :] = 255

                        # Create player
                        self.player = MazePlayer(
                                        (col*unit, row*unit),
                                        maze[row*unit:row*unit+unit, col*unit:col*unit+unit, :].copy(),
                                        self.unit)
                    elif symbol == 'E':   # red exit point
                        # Set the color on this position to red in maze
                        maze[row*unit:row*unit+unit, col*unit:col*unit+unit, 0] = 255

                        # Record the exit point
                        self.exit_point = (col*unit, row*unit)
                    else:
                        raise Exception("Invalid symbol in maze '%s'" % symbol)

        # Save maze
        self.maze = Maze((0, 0), maze.copy())

        # Create groups
        self.player_group = pygame.sprite.Group(self.player)
        self.obstacle_group = pygame.sprite.Group(self.obstacles)

    def finish(self):
        if (self.player.rect.left == self.exit_point[0]) and (self.player.rect.top == self.exit_point[1]):
            return True
        else:
            return False
