import sys
from random import randint
from tkinter import *
from tkinter import messagebox

#define grid,properties(master, width, height, offset,grid_width, grid_x, grid_y,bg),func(gridlist,draw)
class Grid(object):
    def __init__(self, master = None, width = 1000, height = 500, grid_width = 20, offset = 10,bg = 'green'):
        self.master = master
        self.width = width
        self.height = height
        self.offset = offset
        self.grid_width = grid_width
        self.bg = bg
        self.grid_x = self.width/self.grid_width
        self.grid_y = self.height/self.grid_width
        self.canvas = Canvas(self.master, width = self.width+2*offset, height = self.height+2*offset,bg = self.bg)
        self.canvas.pack()
        self.grid_list()

    def grid_list(self):
        grid_list = []
        for x in range(int(self.grid_x)):
            for y in range(int(self.grid_y)):
                grid_list.append((x,y))
        self.grid_list = grid_list
    def draw_block(self,pos,color):
        x = pos[0]*self.grid_width+self.offset
        y = pos[1]*self.grid_width+self.offset
        self.canvas.create_rectangle(x,y,x+self.grid_width,y+self.grid_width,fill = color , outline = self.bg)

#define random_generated food properties(x,y,color) func(set_pos,show_food)
class Food(object):
    def __init__(self,grid,color = 'red'):
        self.grid = grid
        self.color = color
        self.setpos()
    def setpos(self):
        x = randint(0,self.grid.grid_x-1)
        y = randint(0,self.grid.grid_y-1)
        self.pos =  (x,y)
    def show_food(self):
        self.grid.draw_block(self.pos,self.color)

#define Snake properties(body, color, status, gameover_marker, score) func(move)
class Snake(object):
    def __init__(self,grid,food,color = 'black'):
        self.body = [(8, 6), (8, 7), (8, 8)]
        self.speed = 100
        self.direction = 'Right'
        self.color = color
        self.status = 'run'
        self.score = 0
        self.gameover_marker = False
        self.food = food
        self.grid = grid
        self.availiable_area()
    def show_snake(self):
        for i in self.body:
            self.grid.draw_block(i,self.color)
    def availiable_area(self):
        self.avaliable_blocks = [i for i in self.grid.grid_list if i not in self.body[2:]]
    def refresh_food(self):
        while self.food.pos in self.body:
            self.food.setpos()
        self.food.show_food()
    def change_direction(self,direction):
        self.direction = direction
    def move(self):
        current_head = self.body[0]
        if self.direction == 'Up':
            new_head = (current_head[0], current_head[1]-1)
        elif self.direction == 'Down':
            new_head = (current_head[0], current_head[1]+1)
        elif self.direction == 'Left':
            new_head = (current_head[0]-1,current_head[1])
        else:
            new_head = (current_head[0]+1, current_head[1])

        if current_head == self.food.pos:
            self.refresh_food()
            self.score += 1
        else:
            pop = self.body.pop()
            self.grid.draw_block(pop,self.grid.bg)
        self.body.insert(0, new_head)
        if not current_head  in self.avaliable_blocks:
            self.status = 'stop'
            self.gameover_marker = True
        if current_head in self.body[2:]:
            self.gameover_marker = True
        else:
            self.grid.draw_block(new_head,self.color)


#define main game panel
class snake_game(Frame):
    def __init__(self,master = None, *args, **kwargs):
        Frame.__init__(self,master)
        self.master = master
        self.grid = Grid()
        self.food = Food(self.grid)
        self.snake = Snake(self.grid,self.food)
        self.bind_all("<Key>", self.evt)
        self.snake.show_snake()
        self.snake.refresh_food()
        self.show_score = 'score:'+str(self.snake.score)
        self.label_var = Variable()
        self.degree = Variable()
        self.degree.set('A')
        self.score_label = Label(self.master, font=('Arial', 20), textvariable=self.label_var)
        self.score_label.pack()
        self.class_easy = Radiobutton(self.master, text='简单', font=('Arial', 16),variable=self.degree, value='A')
        self.class_nomal = Radiobutton(self.master, text='中等', font=('Arial', 16), variable=self.degree, value='B')
        self.class_hard = Radiobutton(self.master, text='困难', font=('Arial', 16), variable=self.degree, value='C')
        self.class_easy.pack()
        self.class_nomal.pack()
        self.class_hard.pack()
    def run(self):
        if self.snake.status == 'run' and not self.snake.gameover_marker:
            self.snake.move()
            self.label_var.set('（按空格键暂停，按s键开始） score:'+str(self.snake.score))
            if self.degree.get() == 'A':
                self.snake.speed = 300
            elif self.degree.get() == 'B':
                self.snake.speed = 180
            else:
                self.snake.speed = 100
            print(self.snake.speed)
        if self.snake.gameover_marker:
            message = messagebox.showinfo('game over','game over you score is %s' %self.snake.score)
            if message == 'ok':
                sys.exit()
        self.after(self.snake.speed,self.run)
    def evt(self, event):
        dict = {'Up':'Down','Down':'Up','Left':'Right','Right':'Left'}
        if event.keysym in dict.keys() and not self.snake.direction == dict[event.keysym]:
            self.snake.change_direction(event.keysym)
        elif event.keysym == 'space':
            self.snake.status = 'stop'
        elif event.keysym == 's':
            self.snake.status = 'run'

if __name__ == '__main__':
    root = Tk()
    snake_game_t = snake_game(root)
    print(snake_game_t.snake.score)
    snake_game_t.run()
    root.update()
    snake_game_t.mainloop()
