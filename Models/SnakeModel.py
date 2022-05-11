
import numpy as np
from enum import Enum
from itertools import product
from random import sample

from PyQt5.QtCore import QBasicTimer
from PyQt5.QtCore import Qt

from Common.DeQueue import DeQueue
from Common.QtModel import QtStaticModel

class DIRECTION(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4


class SnakeModel(QtStaticModel):
    # Variables will be initialized locally
    head = tuple
    snake = lambda: DeQueue(dtype=[('x', np.int32), ('y', np.int32)])
    wall = set
    food = tuple
    timer = QBasicTimer
    direction = lambda: DIRECTION.DOWN
    grid_height = int
    grid_width = int
    grid_coords = set
    snake_set = set
    score = int
    snake_alive = bool
    
    def initializeGrid(self, tail, head, food, height, width, wall):
        # ToDo - Make circular list for snake
        self.head = head
        self.snake.set_data([tail, head])
        self.snake.reallocate(height * width)
        self.wall = wall
        self.food = food
        self.grid_height = height
        self.grid_width = width
        self.score = 0
        self.grid_coords = {pos for pos in product(range(width), range(height)) if pos not in wall}
        self.snake_set = {tuple(pos) for pos in self.snake}
        self.snake_alive = True
        
        if (head[0] - tail[0]) == 1 and (head[1] == tail[1]):
            self.direction = DIRECTION.RIGHT
        elif (head[0] - tail[0]) == -1 and (head[1] == tail[1]):
            self.direction = DIRECTION.LEFT
        elif (head[1] - tail[1]) == 1 and (head[0] == tail[0]):
            self.direction = DIRECTION.DOWN
        elif (head[1] - tail[1]) == -1 and (head[0] == tail[0]):
            self.direction = DIRECTION.UP
        else:
            raise ValueError("Tail should be adjacent to head.")

    def set_direction(self, key):
        if key == Qt.Key_Left:
            if self.direction != DIRECTION.RIGHT:
                self.direction = DIRECTION.LEFT
  
        elif key == Qt.Key_Right:
            if self.direction != DIRECTION.LEFT:
                self.direction =  DIRECTION.RIGHT
  
        elif key == Qt.Key_Down:
            if self.direction != DIRECTION.UP:
                self.direction = DIRECTION.DOWN
  
        elif key == Qt.Key_Up:
            if self.direction != DIRECTION.DOWN:
                self.direction = DIRECTION.UP

    def get_unoccupied_position(self):
        valid_coords = self.grid_coords - self.snake_set
        
        if valid_coords:
            return sample(valid_coords, 1)[0]
        else:
            print('All postions are occupied!')
            return (0, 0)

    def place_food(self):
        self.food = self.get_unoccupied_position()

    def check_food(self):
        if self.head == self.food:
            self.place_food()
            self.score += 1
            return True
        return False

    def check_snake_not_dead(self):
        if self.head in self.snake_set or self.head in self.wall:
            return False
        return True

    def update_head_position(self):
        x, y = self.head
        
        if self.direction == DIRECTION.LEFT:
            x -= 1
            x %= self.grid_width
  
        if self.direction == DIRECTION.RIGHT:
            x += 1
            x %= self.grid_width
  
        if self.direction == DIRECTION.DOWN:
            y += 1
            y %= self.grid_height
  
        if self.direction == DIRECTION.UP:
            y -= 1
            y %= self.grid_height
  
        self.head = (x, y)

    def move_snake(self, grow_snake=False):
        self.update_head_position()

        if not self.check_food():
            self.snake_set.remove(tuple(self.snake.pop_front()))
        
        if self.check_snake_not_dead():
            self.snake.add_back(self.head)
            self.snake_set.add(self.head)
        else:
            self.timer.stop()
            self.snake_alive = False


    def update(self):
        self.move_snake()
        return self.snake_alive