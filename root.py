from tkinter import Tk, Canvas
import random

# Globals
WIDTH = 800
HEIGHT = 600
SEG_SIZE = 20
IN_GAME = True


def pos():
    posx = SEG_SIZE * random.randint(1, (WIDTH - SEG_SIZE) / SEG_SIZE)
    posy = SEG_SIZE * random.randint(1, (HEIGHT - SEG_SIZE) / SEG_SIZE)
    return posx, posy


# Helper functions
def create_block(posx, posy):
    """ Creates an apple to be eaten """
    global BLOCK
    BLOCK = c.create_oval(posx, posy,
                          posx+SEG_SIZE, posy+SEG_SIZE,
                          fill="red")


def change_pos():
    i = 0
    posx, posy = pos()
    for segment in snake.segments:
        if (posx, posy) != segment.pos:
            i += 1
    print(i, ' ', len(snake.segments))
    if len(snake.segments) == i:
        create_block(posx, posy)
    else:
        change_pos()
        print("Chang")


def main():
    """ Handles game process """
    global IN_GAME
    if IN_GAME:
        snake.move()
        head_coords = c.coords(snake.segments[-1].instance)
        x1, y1, x2, y2 = head_coords
        # Check for collision with gamefield edges
        if x2 > WIDTH or x1 < 0 or y1 < 0 or y2 > HEIGHT:
            IN_GAME = False
        # Eating apples
        elif head_coords == c.coords(BLOCK):
            snake.add_segment()
            c.delete(BLOCK)
            change_pos()
        # Self-eating
        else:
            for index in range(len(snake.segments)-1):
                if head_coords == c.coords(snake.segments[index].instance):
                    IN_GAME = False
                    print("end game")
        root.after(100, main)
    # Not IN_GAME -> stop game and print message
    else:
        set_state(restart_text, 'normal')
        set_state(game_over_text, 'normal')


class Segment(object):
    """ Single snake segment """
    def __init__(self, x, y):
        self.instance = c.create_rectangle(x, y,
                                           x+SEG_SIZE, y+SEG_SIZE,
                                           fill="white")
        self.pos = (x, y)


class Snake(object):
    """ Simple Snake class """
    def __init__(self, segments):
        self.segments = segments
        # possible moves
        self.mapping = {"Down": (0, 1), "Right": (1, 0),
                        "Up": (0, -1), "Left": (-1, 0)}
        # initial movement direction
        self.vector = self.mapping["Right"]

    def move(self):
        """ Moves the snake with the specified vector"""
        for index in range(len(self.segments)-1):
            segment = self.segments[index].instance
            x1, y1, x2, y2 = c.coords(self.segments[index+1].instance)
            c.coords(segment, x1, y1, x2, y2)

        x1, y1, x2, y2 = c.coords(self.segments[-2].instance)
        c.coords(self.segments[-1].instance,
                 x1+self.vector[0]*SEG_SIZE, y1+self.vector[1]*SEG_SIZE,
                 x2+self.vector[0]*SEG_SIZE, y2+self.vector[1]*SEG_SIZE)

    def add_segment(self):
        """ Adds segment to the snake """
        last_seg = c.coords(self.segments[0].instance)
        x = last_seg[2] - SEG_SIZE
        y = last_seg[3] - SEG_SIZE
        self.segments.insert(0, Segment(x, y))

    def change_direction(self, event):
        """ Changes direction of snake """
        if event.keysym in self.mapping and self.vector != (-self.mapping[event.keysym][0], -self.mapping[event.keysym][1]):
            self.vector = self.mapping[event.keysym]

    def reset_snake(self):
        for segment in self.segments:
            c.delete(segment.instance)


def set_state(item, state):
    c.itemconfigure(item, state=state)


def clicked(event):
    global IN_GAME
    snake.reset_snake()
    IN_GAME = True
    c.delete(BLOCK)
    c.itemconfigure(restart_text, state='hidden')
    c.itemconfigure(game_over_text, state='hidden')
    start_game()


def start_game():
    global snake
    n, m = pos()
    create_block(n, m)
    snake = create_snake()
    # Reaction on keypress
    c.bind("<KeyPress>", snake.change_direction)
    main()


def create_snake():
    # creating segments and snake
    segments = [Segment(SEG_SIZE, SEG_SIZE),
                Segment(SEG_SIZE*2, SEG_SIZE),
                Segment(SEG_SIZE*3, SEG_SIZE)]
    return Snake(segments)


# Setting up window
root = Tk()
root.title("PythonicWay Snake")


c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#003300")
c.grid()
# catch keypressing
c.focus_set()
game_over_text = c.create_text(WIDTH/2, HEIGHT/2, text="GAME OVER!",
                               font='Arial 20', fill='red',
                               state='hidden')
restart_text = c.create_text(WIDTH/2, HEIGHT-HEIGHT/3,
                             font='Arial 30',
                             fill='white',
                             text="Click here to restart",
                             state='hidden')
c.tag_bind(restart_text, "<Button-1>", clicked)
start_game()
print(snake.segments[0].pos)
root.mainloop()