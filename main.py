
import pygame
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


class OS:

    def __init__(self, window):
        self.time = 1
        self.CPU = CPU()
        self.window = window
        self.processes = [(1,5,33),(2,2,32),(3,3,44),(4,9,27),(5,10,58),(6,20,34),(7,30, 80)] #(process ID, arrival time, burst time)
        self.queue = Queue()
        self.processList = []       # store all created processes
        self.lock = False
        self.table = Table(self.processes)

    def run(self):

        self.queue.draw(self.window)
        self.CPU.draw(self.window)
        self.table.draw(self.window)

        self.createProcess()
        self.drawAllProcesses()
        self.moveProcesses()
        self.executeProcess()

        pygame.display.update()
        self.window.fill((255, 255, 255))
        self.time += 0.25

    def createProcess(self):
        """check the arrival time of each process and create it if arrival time match current timeD"""

        for process in self.processes:
            if process[1] == self.time:
                self.processList.append(Process(self.CPU, self.queue, process[0],process[2]))


    def drawAllProcesses(self):
        """draw all processes on the screen"""
        for process in self.processList:
            process.draw(self.window)

    def executeProcess(self):
        """if lock is true and there is a current process assigned to the cpu
            then decrease that process burst time until it becomes zero before removing
            the process from the cpu and releasing the lock"""

        if self.lock and self.CPU.currentProcess:
            self.CPU.currentProcess.burstTime -= 1
            if self.CPU.currentProcess.burstTime == 0:
                self.processList.remove(self.CPU.currentProcess)
                self.lock = False

    def moveProcesses(self):
        """iterate over all processes in the process list to determine if they can move"""
        for i, proc in enumerate(self.processList):
            if proc.end_x() > self.CPU.x_pos + 60:  # this stops the process from moving pass the cpu
                continue                            # once pass cpu start pos + the diameter of the process
                                                    # then never move that process again.
            if proc.end_x() == self.queue.end_x():  # if process at the front of the queue
                if not self.lock:                   # if lock not on move process beyond front and set lock to true
                    proc.move()
                    self.lock = True
                else:
                    pass                           # else dont move
            else:                                  # else process not at front of the queue; worry about process infront
                                                   # this checks if there is a process directly infront. If not move
                if not(self.processList[i-1].x_pos-self.processList[i-1].radius == proc.x_pos+proc.radius):
                    proc.move()




class Queue():
    def __init__(self):
        self.queue = []
        self.color = (255, 0, 0)  # red color
        self.x_pos = 300
        self.y_pos = 40
        self.width = 420
        self.height = 60
        self.font = pygame.font.SysFont(None, 30)

    def draw(self, window):
        """draw the queue on the screen"""

        # draw the rectangle to hold 7 processes
        pygame.draw.rect(window, self.color, pygame.Rect(self.x_pos, self.y_pos, self.width, self.height), 3)

        # draw the vertical lines for each cell of the queue. 60 is the diameter of a process
        t = self.width//60
        for i in range(1, t+1):
            pygame.draw.line(window, self.color, (self.x_pos+(60*i), self.y_pos),(self.x_pos+(60*i), self.y_pos+self.height))

        # draw label 'Queue' at the top of the queue
        txt = self.font.render("Queue", True, (0, 0, 255))
        window.blit(txt, [self.x_pos + 200, self.y_pos - 25])

    def end_x(self):
        return self.x_pos + self.width


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
        """Draw the process table with the info given onto the screen"""

        # draw the bounding rectangle
        pygame.draw.rect(window, self.color, pygame.Rect(self.x_pos, self.y_pos, self.width, self.height), 3)

        # draw the three line for the columns
        t = self.width // 160
        for i in range(1, t + 1):
            pygame.draw.line(window, self.color, (self.x_pos + (160 * i), self.y_pos),(self.x_pos + (160 * i), self.y_pos + self.height))

        # draw the lines that separate the rows
        t = self.height // 40
        for i in range(1, t + 1):
            pygame.draw.line(window, self.color, (self.x_pos, self.y_pos+(40*i)),(self.x_pos + self.width, self.y_pos + (40*i)))

        # draw the headings for the table
        txt = self.font.render("PROCESSES", True, (0, 0, 255))
        window.blit(txt, [self.x_pos + 20, self.y_pos + 10])
        txt = self.font.render("ARRIVAL TIME", True, (0, 0, 255))
        window.blit(txt, [self.x_pos + 10 + 160, self.y_pos + 10])
        txt = self.font.render("BURST TIME", True, (0, 0, 255))
        window.blit(txt, [self.x_pos + 20 + (2*160), self.y_pos + 10])

        # draw all the table data for each row
        for i, process in enumerate(self.table):

            # draw the process labels in the first column
            txt = self.font.render("P"+str(process[0]), True, (0, 0, 255))
            window.blit(txt, [self.x_pos + 20, self.y_pos + 10 + (40*(i+1))])

            # draw the process arrival time in the second column
            txt = self.font.render(str(process[1]), True, (0, 0, 255))
            window.blit(txt, [self.x_pos + 10 + 160, self.y_pos + 10 + (40*(i+1))])

            # draw the process burst time in the third column
            txt = self.font.render(str(process[2]), True, (0, 0, 255))
            window.blit(txt, [self.x_pos + 20 + (2*160), self.y_pos + 10 + (40*(i+1))])


class CPU:

    def __init__(self):
        self.currentProcess = None
        self.color = (255, 255, 255)  # red color
        self.x_pos = 840
        self.y_pos = 0
        self.width = 120
        self.height = 400
        self.font = pygame.font.SysFont(None, 30)
        self.cpu_image = pygame.image.load('cpu.jpg')

    def draw(self, window):
        """draw an outline of the cpu and make it invisible by making the color white
            Also draw the cpu image"""

        pygame.draw.rect(window, self.color, pygame.Rect(self.x_pos, self.y_pos, self.width, self.height), 3)
        txt = self.font.render("CPU", True, (0, 0, 255))
        window.blit(txt, [self.x_pos + 35, self.y_pos + 200])

        # draw cpu image
        window.blit(self.cpu_image, (825, 0))


class Process:

    def __init__(self, CPU, queue, id, burstTime):
        self.CPU = CPU
        self.burstTime = burstTime
        self.queue = queue
        self.color = (255, 0, 0) # red color
        self.x_pos = 30
        self.y_pos = 70
        self.radius = 30
        self.velocity = 30
        self.id = id
        self.label = "P"+str(self.id)
        self.inQueue = False
        self.inCPU = False
        self.font = pygame.font.SysFont(None,30)

    def draw(self, window):
        """Draw all processes on the screen along with there respective labels and time remaining on cpu"""

        # draw the circle that represents the process
        pygame.draw.circle(window, self.color , (self.x_pos, self.y_pos), self.radius)

        # draw the label on the process eg 'P1'
        txt = self.font.render(self.label, True, (0,0,255))
        window.blit(txt, [self.x_pos - 10,self.y_pos - 4])

        # if the process is in the cpu draw the label just below the cpu otherwise draw it just below the process
        if self.inCPU:
            txt = self.font.render(str(self.burstTime)+"ms", True, (0, 0, 255))
            window.blit(txt, [self.x_pos - 25, self.y_pos + 85])
        else:
            txt = self.font.render(str(self.burstTime) + "ms", True, (0, 0, 255))
            window.blit(txt, [self.x_pos - 25, self.y_pos + 38])

    def move(self):
        """move the process and make it aware if it is in the cpu or queue"""
        self.x_pos += self.velocity
        self.setQueueParams()

    def setQueueParams(self):
        """if process is within the bounds of the queue then set it as inQueue. if not
            set inQueue to false and if it was marked as in the queue before, remove it.
            Likewise if process is in the cpu set it as inCpu else set inCpu to false"""

        if (self.start_x() >= self.queue.x_pos) and (self.start_x() < self.queue.end_x()):
            self.inQueue = True
            self.queue.queue.append(self)
        else:
            self.inQueue = False
            if self in self.queue.queue:
                for i in range(len(self.queue.queue)):
                    if i == self.id:
                        del self.queue.queue[i]

        if (self.end_x() > self.CPU.x_pos) and (self.start_x() < self.CPU.x_pos+self.CPU.width):
            self.inCPU = True
            self.CPU.currentProcess = self
        else:
            self.inCPU = False

    def end_x(self):
        """get the starting x point of the process circle"""
        return self.x_pos + self.radius

    def start_x(self):
        """get the ending x point of the process circle"""
        return self.x_pos - self.radius

run = True

def closeGameOnQuit():
    global run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


if __name__ == '__main__':

    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    os = OS(window)
    while run:
        pygame.time.Clock().tick(5)  # frame rate 5 frames per second
        closeGameOnQuit()  # exit on click the quit button
        os.run()
    pygame.quit()