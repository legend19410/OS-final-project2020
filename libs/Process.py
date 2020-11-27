import pygame

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
        self.process_image = pygame.image.load("resources/images/exe.png")
        self.process_image = pygame.transform.scale(self.process_image, (60, 60))

    def draw(self, window):
        """ Draw all processes on the screen along with there respective labels and time remaining on cpu """

        # Draw the circle that represents the process
        #pygame.draw.circle(window, self.color , (self.x_pos, self.y_pos), self.radius)
        window.blit(self.process_image, [self.x_pos - 30, self.y_pos - 30])

        # Draw the label on the process eg 'P1'
        txt = self.font.render(self.label, True, (0,0,255))
        window.blit(txt, [self.x_pos - 10,self.y_pos - 10])

        # If the process is in the cpu draw the label just below the cpu otherwise draw it just below the process
        if self.inCPU:
            txt = self.font.render(str(self.burstTime)+"ms", True, (0, 0, 255))
            window.blit(txt, [self.x_pos - 25, self.y_pos + 85])
        else:
            txt = self.font.render(str(self.burstTime) + "ms", True, (0, 0, 255))
            window.blit(txt, [self.x_pos - 25, self.y_pos + 38])

    def move(self):
        """ Move the process and make it aware if it is in the cpu or queue """
        self.x_pos += self.velocity
        self.setQueueParams()

    def setQueueParams(self):
        """ If process is within the bounds of the queue then set it as inQueue. if not
            set inQueue to false and if it was marked as in the queue before, remove it.
            Likewise if process is in the cpu set it as inCpu else set inCpu to false """

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
        """ Get the starting x point of the process circle """
        return self.x_pos + self.radius

    def start_x(self):
        """ Get the ending x point of the process circle """
        return self.x_pos - self.radius
