import pygame
from libs.OsObj import OsObj

class Table(OsObj):
    def __init__(self, processTable):
        super().__init__(pygame.Rect((267, 200), (480, 320)), \
            pygame.font.SysFont(None, 30), (255, 0, 0))
        self.table = processTable
        self.colWidth = 160
        self.rowHeight = 40

    def draw(self, window):
        """ Draw the process table with the info given onto the screen """

        # Centering table relative to window
        width, height = window.get_size()
        self.setCenterX(width//2)
        self.setY(height - self.height() - 10)
        
        # Draw the bounding rectangle
        pygame.draw.rect(window, self.bgColor, self.rect, 3)

        # Draw the three line for the columns
        t = self.width() // self.colWidth
        for i in range(1, t + 1):
            pygame.draw.line(window, self.bgColor, \
                (self.backX() + (self.colWidth*i), self.topY()), \
                (self.backX() + (self.colWidth*i), self.topY() + self.height()))

        # Draw the lines that separate the rows
        t = self.height() // self.rowHeight
        for i in range(1, t + 1):
            pygame.draw.line(window, self.bgColor, \
                (self.backX(), self.topY() + (self.rowHeight*i)), \
                (self.backX() + self.width(), self.topY() + (self.rowHeight*i)))

        # Draw the headings for the table
        txt = self.font.render("PROCESSES", True, self.txtColor)
        window.blit(txt, [self.backX() + 20, self.topY() + 10])
        txt = self.font.render("ARRIVAL TIME", True, self.txtColor)
        window.blit(txt, [self.backX() + 10 + 160, self.topY() + 10])
        txt = self.font.render("BURST TIME", True, self.txtColor)
        window.blit(txt, [self.backX() + 20 + (2*160), self.topY() + 10])

        # Draw all the table data for each row
        for i, process in enumerate(self.table):
            # Draw the process labels in the first column
            txt = self.font.render("P"+str(process[0]), True, self.txtColor)
            window.blit(txt, [self.backX() + 20, self.topY() + 10 + (40*(i+1))])

            # Draw the process arrival time in the second column
            txt = self.font.render(str(process[1]), True, self.txtColor)
            window.blit(txt, [self.backX() + 10 + 160, self.topY() + 10 + (40*(i+1))])

            # Draw the process burst time in the third column
            txt = self.font.render(str(process[2]), True, self.txtColor)
            window.blit(txt, [self.backX() + 20 + (2*160), self.topY() + 10 + (40*(i+1))])
