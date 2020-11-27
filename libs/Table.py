import pygame

class Table:

    def __init__(self, processTable):
        self.table = processTable
        self.color = (255, 0, 0)  # red color
        self.width = 480
        self.height = 320
        self.x_pos = 267
        self.y_pos = 200
        self.font = pygame.font.SysFont(None, 30)

    def draw(self, window):
        """ Draw the process table with the info given onto the screen """

        # Draw the bounding rectangle
        pygame.draw.rect(window, self.color, pygame.Rect(self.x_pos, self.y_pos, self.width, self.height), 3)

        # Draw the three line for the columns
        t = self.width // 160
        for i in range(1, t + 1):
            pygame.draw.line(window, self.color, (self.x_pos + (160 * i), self.y_pos),(self.x_pos + (160 * i), self.y_pos + self.height))

        # Draw the lines that separate the rows
        t = self.height // 40
        for i in range(1, t + 1):
            pygame.draw.line(window, self.color, (self.x_pos, self.y_pos+(40*i)),(self.x_pos + self.width, self.y_pos + (40*i)))

        # Draw the headings for the table
        txt = self.font.render("PROCESSES", True, (0, 0, 255))
        window.blit(txt, [self.x_pos + 20, self.y_pos + 10])
        txt = self.font.render("ARRIVAL TIME", True, (0, 0, 255))
        window.blit(txt, [self.x_pos + 10 + 160, self.y_pos + 10])
        txt = self.font.render("BURST TIME", True, (0, 0, 255))
        window.blit(txt, [self.x_pos + 20 + (2*160), self.y_pos + 10])

        # Draw all the table data for each row
        for i, process in enumerate(self.table):

            # Draw the process labels in the first column
            txt = self.font.render("P"+str(process[0]), True, (0, 0, 255))
            window.blit(txt, [self.x_pos + 20, self.y_pos + 10 + (40*(i+1))])

            # Draw the process arrival time in the second column
            txt = self.font.render(str(process[1]), True, (0, 0, 255))
            window.blit(txt, [self.x_pos + 10 + 160, self.y_pos + 10 + (40*(i+1))])

            # Draw the process burst time in the third column
            txt = self.font.render(str(process[2]), True, (0, 0, 255))
            window.blit(txt, [self.x_pos + 20 + (2*160), self.y_pos + 10 + (40*(i+1))])
