# ----------------------------------------------------------------------
# Name:     graphics
# Purpose:  Visualization of the maze and solution
#
# Author:   Rula Khayrallah
#
# Copyright ©  Rula Khayrallah, 2020
# ----------------------------------------------------------------------
"""
Class definition to visualize the quest
"""
import tkinter
import time


class Display(object):
    """
    Visualization of a given solution to a quest

    Arguments:
    problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py)
    solution:  list of actions representing the solution to the quest

    Attributes:
    problem (a Problem object) representing the quest
            see Problem class definition in spartanquest.py)
    actions:  iterator yielding the actions representing the solution to
    the quest
    canvas:  tkinter widget used to visualize the solution
    medal_icon: set of Canvas ovals representing the remaining medals
    mascot: Canvas image representing Sammy the Spartan

    """
    time_interval = 100  # decrease time_interval for faster animation
    size = 40  # size in pixel for each grid position

    def __init__(self, problem, solution):
        self.medal_icon = {}
        self.problem = problem # save the problem info
        root = tkinter.Tk()
        root.title('Go Spartans!')
        self.canvas = tkinter.Canvas(root,
                                     width=self.size * problem.maze.width,
                                     height=self.size * problem.maze.height)
        self.canvas.grid()
        sammy_x, sammy_y = problem.mascot_position

        for y in range(problem.maze.height):
            for x in range(problem.maze.width):
                if problem.maze.is_wall((x, y)):
                    fill_color = 'blue'
                else:
                    fill_color = 'black'
                self.canvas.create_rectangle(x * self.size,
                                             y * self.size,
                                             (x + 1) * self.size,
                                             (y + 1) * self.size,
                                             fill=fill_color,
                                             outline="")

        # load the .gif image file
        sammy = tkinter.PhotoImage(file='sammy.gif')

        self.mascot = self.canvas.create_image((sammy_x + 0.5) * self.size,
                                               (sammy_y + 0.5) * self.size,
                                               image=sammy)
        for each_medal_x, each_medal_y in problem.medals:
            self.medal_icon[(each_medal_x, each_medal_y)] = \
                self.canvas.create_oval((each_medal_x + 0.25) * self.size,
                                        (each_medal_y + 0.25) * self.size,
                                        (each_medal_x + 0.75) * self.size,
                                        (each_medal_y + 0.75) * self.size,
                                        fill="gold",
                                        outline="")

        if solution is not None:
            self.actions = iter(solution)
            self.canvas.after(self.time_interval, self.move)
#            self.animate()
        root.mainloop()

    def animate(self):
        """
        Invoke the move method after the time interval.
        :return: None
        """
        self.canvas.after(self.time_interval, self.move)

    def move(self):
        """
        Move the mascot a single step according to the current action.
        Schedule the next move.
        :return: None
        """
        try:
            action = next(self.actions)
        except StopIteration:
            return
        else:
            x, y = self.problem.mascot_position
            new_x = x + self.problem.moves[action][0]
            new_y = y + self.problem.moves[action][1]
            position = (new_x, new_y)

            if not self.problem.maze.within_bounds(position):
                raise Exception('Falling off the maze....')
            elif self.problem.maze.is_wall(position):
                raise Exception('Crash!  Wall encountered')
            elif position in self.problem.medals:
                self.problem.medals.discard(position)
                self.canvas.itemconfigure(self.medal_icon[position],
                                          fill="")
            self.problem.mascot_position = position

            move_x, move_y = self.problem.moves[action]
            self.canvas.move(self.mascot,
                             move_x * self.size,
                             move_y * self.size)
            self.canvas.create_line((x + 0.5) * self.size,
                                    (y + 0.5) * self.size,
                                    (new_x + 0.5) * self.size,
                                    (new_y + 0.5) * self.size,
                                    arrow = tkinter.LAST,
                                    width = 3,
                                    fill = "yellow")

            self.canvas.after(self.time_interval, self.move)
