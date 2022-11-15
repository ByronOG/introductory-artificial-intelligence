# ----------------------------------------------------------------------
# Name:        treasurehunt
# Purpose:     Homework 8 - Demonstrate probabilistic reasoning
#
# Author:      Rula Khayrallah
#
# Copyright ©  Rula Khayrallah, 2022
# ----------------------------------------------------------------------
"""
A Treasure hunt under the sea

Usage:  treasurehunt.py size mode
  size       How many columns/rows in the grid?
  mode       discovery or guided?

Examples:
python treasurehunt.py 10 discovery
python treasurehunt.py 8 guided

Click on the 'SONAR' button to start taking sonar measurements. When you
are ready to make a decision and dive, click on the 'DIVE' button.
"""
import argparse
import tkinter
import random
import utils
from beliefs import Belief


class Problem(object):

    """
    Problem class

    Argument:
    size (int): the number of rows/columns in the game

    Attribute:
    treasure (tuple): the location of the treasure (x, y)
    """
    def __init__(self, size):
        # Pick a random location for the treasure
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        self.treasure = x, y

    def treasure_found(self, pos):
        """
        Determine if the dive is successful
        :param pos (tuple): diving position
        :return: boolean - True if the treasure is at that position
                 and False otherwise.
        """
        return pos == self.treasure

class Model(object):

    """
    Model class used to describe our sensor model

    """

    # Class variable sonar_model
    # The initial probabilities for distance <= 7
    # This is how to interpret the dictionary below:
    # P(red|d=0) = 0.7,  P(red|d=1) = 0.3, P(red|d=2) = 0.1,
    # P(red|d>=3) = 0
    # P(yellow|d=0) = 0.3, P(yellow|d=1) = 0.6, P(yellow|d=2) = 0.6, ...
    sonar_model = {'red': [0.7, 0.3, 0.1, 0],
                   'yellow': [0.3, 0.6, 0.6, 0.4, 0.3, 0.2, 0.1, 0],
                   'green': [0, 0.1, 0.3, 0.6, 0.7, 0.8, 0.9, 1]}


    def observe(self, pos, problem):
        """
        Return the color returned when the sonar is aimed at the given
        location.
        :param pos:  (tuple) sonar position
        :param problem: (Problem object)
        :return:
        color (string) : sensor reading
        """
        dist = utils.manhattan_distance(pos, problem.treasure)
        color = self.sample(dist)
        return color

    def sample(self, distance):
        """
        Sample a color reading based on the sensor model we have
        :param distance: (integer) Manhattan distance to the treasure
        :return: color (string) sensor reading
        """
        dist = []
        for each_color in self.sonar_model:
            farthest = len(self.sonar_model[each_color]) - 1
            if distance > farthest:
                d = farthest
            else:
                d = distance
            for i in range(int(self.sonar_model[each_color][d] * 100)):
                dist.append(each_color)
        return random.choice(dist)

    def pcolorgivendist(self, color, dist):
        """
        Return the conditional probability of the given sonar
        color given the distance
        :param color: (string) sensor reading
        :param dist: distance from sensor location to a given position
        :return: float probability
        """
        farthest = len(self.sonar_model[color]) - 1
        if dist <= farthest:
            return self.sonar_model[color][dist]
        else:
            return self.sonar_model[color][farthest]


class Game(object):

    """
    Game class for the treasure hunt

    Arguments:
    parent: the root window object
    size (int): the number of rows/columns in the game
    mode (string): discovery or guided?  No probabilities are shown in
        discovery mode and no sensor recommendations are shown.

    Attributes
    size (int): the number of rows/columns in the game
    mode (string): discovery or guided?
    canvas (Canvas): tkinter widget
    model (Model object) our world model of how the location of the
            treasure affects the sensor readings
    problem (Problem object) the specific problem (with random treasure
            location that we are trying to solve
    belief (Belief object) belief distribution based on the sensing
            evidence we have so far
    text (canvas text object): used to display the probability of each
            location
    message (Label) tkinter widget
    """

    square_size = 70 # length in pixels of the side of a grid square
    contrasting_color = {'blue': 'yellow', 'green': 'yellow',
                         'yellow': 'magenta', 'red': 'yellow',
                         'purple': 'yellow'}

    def __init__(self, parent, size, mode):

        self.size = size
        self.mode = mode

        parent.title('Under the Sea')
        sensor_button = tkinter.Button(parent, text='SONAR',
                                       command=self.sensor_mode)
        sensor_button.grid()
        action_button = tkinter.Button(parent, text='DIVE',
                                       command=self.diving_mode)
        action_button.grid()
        self.canvas = tkinter.Canvas(parent,
                                     width=self.size * self.square_size,
                                     height=self.size * self.square_size)
        self.canvas.grid()
        self.text = [[ None for row in range(self.size)]
                     for col in range(self.size)]
        # create the squares on the canvas
        for row in range(self.size):
            for column in range(self.size):
                self.canvas.create_rectangle(column * self.square_size,
                                             row * self.square_size,
                                             (column + 1) * self.square_size,
                                             (row + 1) * self.square_size,
                                             fill = 'blue',
                                             outline = 'white',
                                             tag = 'square')
                self.text[column][row] = self.canvas.create_text(
                    (column + 0.5) * self.square_size,
                    (row+ 0.5) * self.square_size,
                    text='')
        self.message = tkinter.Label(parent)
        self.message.grid()
        self.treasure_img = tkinter.PhotoImage(file="treasure.gif")
        self.oct = tkinter.PhotoImage(file="octopus.gif")

        self.model = Model()
        self.problem = Problem(size)
        self.belief = Belief(size)
        if self.mode == 'guided':
            self.showbeliefs()


    def sensor_mode(self):
        """
        Set the game to sensor mode - the method is invoked when the
        "SONAR" button is clicked.
        Once the game is in sensor mode, clicks on the grid result in
        sensor readings.
        """
        self.canvas.bind("<Button-1>", self.sense)
        self.message.configure(text='SONAR MODE')

    def diving_mode(self):
        """
        Set the game to diving mode - the method is invoked when the
        "SONAR" button is clicked.
        Once the game is in diving mode, clicks on the grid reveal
        whether the treasure is found at that location.
        """
        self.canvas.bind("<Button-1>", self.dive)
        self.message.configure(text='DIVING MODE')

    def dive(self, event):
        """
        A click at a given location represents a dive.
        Check if the dive is successful and update the GUI
        """
        y = event.y // self.square_size
        x = event.x // self.square_size
        square = self.canvas.find_closest((x + 0.1) * self.square_size,
                                          (y + 0.1)* self.square_size)[0]
        self.canvas.itemconfigure(square, fill="black")
        self.canvas.itemconfigure(self.text[x][y], text="")
        if self.problem.treasure_found((x, y)):
            self.canvas.create_image(
                (x + 0.5) * self.square_size,
                (y + 0.5) * self.square_size,
                image=self.treasure_img)
            self.message.configure(text='Treasure chest found!!!')
        else:
            self.canvas.create_image(
                (x + 0.5) * self.square_size,
                (y + 0.5) * self.square_size,
                image=self.oct)
            self.message.configure(text='Nope.  Try again')

    def sense(self, event):
        """
        A click at a given location represents a sonar reading.
        """
        x = event.x // self.square_size
        y = event.y // self.square_size
        square = self.canvas.find_closest((x + 0.1) * self.square_size,
                                          (y + 0.1)* self.square_size)[0]
        sensing_position = (x, y)
        color = self.model.observe(sensing_position, self.problem)
        self.belief.update(color, sensing_position, self.model)
        self.mark(square, color)
        if self.mode == 'guided':
            self.showbeliefs()
            self.show_recommendation()

    def showbeliefs(self):
        """
        Show the current belief distribution on the GUI
        """
        b = self.belief.current_distribution
        square = 1
        for i in range(self.size):
            for j in range(self.size):
                message = f'{b[(j, i)]:4.1}'
                color = self.canvas.itemcget(square, "fill")
                self.canvas.itemconfigure(self.text[j][i],
                                          text=message,
                                          fill=self.contrasting_color[color])
                square += 2

    def show_recommendation(self):
        """
        Show the recommendation returned by the belief module in purple
        on the GUI.
        """
        next_position = self.belief.recommend_sensing()
        if next_position != NotImplemented:
            nx, ny = next_position
            square = self.canvas.find_closest((nx + 0.1) * self.square_size,
                                              (ny + 0.1) * self.square_size)[0]
            self.canvas.itemconfigure(square, fill='purple')

    def mark(self, square, color):
        """
        Mark a given square with the specified color.

        :param square: tkinter id of the square to be marked
        :param color: (string)  'red', 'green' or 'yellow'
        """
        self.canvas.itemconfigure(square, fill=color)


def get_arguments():
    """
    Parse and validate the command line arguments
    :return: (tuple containing the size of the game and the algorithm
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('size',
                        help='How many columns/rows in the grid?',
                        nargs = '?',
                        type=int,
                        default=8)
    parser.add_argument('mode',
                        help='discovery or guided?',
                        nargs = '?',
                        type=str,
                        choices=['discovery', 'guided'],
                        default='guided')
    arguments = parser.parse_args()

    size = arguments.size
    mode = arguments.mode

    return size, mode

def main():
    # To get predictable results and test your code, uncomment the
    # statement below.  The game will be boring when you do that :(
    random.seed(10)
    size, mode = get_arguments()
    # Instantiate a root window
    root = tkinter.Tk()
    # Instantiate a Game object
    my_game = Game(root, size, mode)
    # Enter the main event loop
    root.mainloop()

if __name__ == '__main__':
    main()
