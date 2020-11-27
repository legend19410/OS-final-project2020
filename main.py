import spn
import pygame
import fcfs


class OS:

    def __init__(self, window, algorithm):
        self.time = 1
        self.CPU = CPU()
        self.window = window
        self.processes = [(1,5,33),(2,2,32),(3,3,44),(4,9,27),(5,10,58),(6,20,34),(7,30, 80)] #(process ID, arrival time, burst time)
        self.queue = Queue()
        self.prev_queue_len = 0 
        self.algoritm = algorithm(self.queue)
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
                self.processList.append(Process(self.CPU, self.queue, process[0],process[1], process[2]))


    def drawAllProcesses(self):
        """draw all processes in process list on the screen"""
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
            if proc.center_x() >= self.CPU.center_x():      # this stops the process from moving pass the cpu
                continue                                    # once pass cpu start pos + the diameter of the process
                                                            # then never move that process again.
                                                            # if self.prev_queue_len!=self.queue.getLength():
            
            if proc.center_x() == proc.getMemLocation():
                # pass
                location_infront = proc.getMemLocation()+2*CIRCLE_RADIUS #memory location directlt in front
                                                                          #of location of current process
                #shift up process in queue if location is available
                if self.queue.locationAvailability(location_infront):
                    proc.move()
                    proc.changeMemLocation()
                    
            else:                                           # else process not at front of the queue; worry about process infront
                                                            # this checks if there is a process directly infront. If not move
                if not(self.processList[i-1].x_pos-self.processList[i-1].radius == proc.x_pos+proc.radius):
                    proc.move()
                
        self.lock = self.algoritm.selectProcess(self.lock)  # selects shortest job and moves it into processor 
                                                            # if it is available


class Queue():
    def __init__(self):
        self.queue = []              # list storing process and location in queue
        self.mem_locations=[]        # stores location of each mem slot (x_pos, availability)
        self.color = (255, 0, 0)     # red color
        self.x_pos = 300
        self.y_pos = 70
        self.width = 420
        self.height = 60
        self.font = pygame.font.SysFont(None, 30)

    def draw(self, window):
        """draw the queue on the screen"""

        # draw the rectangle to hold maximum 7 processes
        pygame.draw.rect(window, self.color, pygame.Rect(self.x_pos, self.y_pos, self.width, self.height), 3)


        # draw the vertical lines for each cell of the queue. 60 is the diameter of a process
        line_nums= list(range(1, MAX_QUEUE_SLOTS+1))[::-1]

        for i in line_nums:
            pygame.draw.line(window, self.color, (self.x_pos+(60*i), self.y_pos),(self.x_pos+(60*i), self.y_pos+self.height))

        #assign x coordinate to each memory slot in queue
        if(not self.mem_locations):#only want to do this the first time the queue is drawn because queue
                                   #is drawn on each iteration of the main loop and would overwrite the
                                   #the availability status of a slot location and cause problems
            for i in line_nums:    #this loop assigns an x coordinate to each slot in the queue created above
                                   #this x coordinate is used to denote the location of a process in the queue
                                   #  
                #assign x coordinate to each memory slot in queue and assign its default availability status
                mem_location = self.x_pos+(60*i)-CIRCLE_RADIUS
                self.mem_locations.append([mem_location,True])

        # print(self.mem_locations)

        


        # draw label 'Queue' at the top of the queue
        txt = self.font.render("Queue", True, (0, 0, 255))
        window.blit(txt, [self.x_pos + 200, self.y_pos - 25])

    def getQueue(self):
        """returns the ready queue"""
        return self.queue

    def end_x(self):
        """returns x coordinate of right edge of object"""
        return self.x_pos + self.width
    
    def center_y(self):
        """returns y coordinate of queue's center"""
        return self.y_pos + self.height//2
    
    def nextAvailableLocation(self):
        """returns x coordinate next available queue location"""
        if len(self.queue) < MAX_QUEUE_SLOTS:
            slot_num = len(self.queue)
            return self.mem_locations[slot_num][0]
        return -1
    
    def lockMemLocation(self, xcor):
        """changes the avaibility of a memory location to false"""
        for index in range(len(self.mem_locations)):
            if self.mem_locations[index][0] == xcor:
                self.mem_locations[index][1]=False
    
    def unlockMemLocation(self, xcor):
        """changes the avaibility of a memory location to true"""
        for index in range(len(self.mem_locations)):
            if self.mem_locations[index][0] == xcor:
                self.mem_locations[index][1]=True

    def removeProcess(self, index):
        """removes process at location of index from queue"""
        del self.queue[index]
    
    def locationAvailability(self, query):
        for location, availability in self.mem_locations:
            if query == location and availability:
                return True
        return False 
        
    def getLength(self):
        """returns lenght of queue"""
        return len(self.queue)


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
        self.color = (0, 0, 255)                               #blue color
        self.label_x_pos = 875                                 #label surface x pos
        self.label_y_pos = 0                                   #label surface y pos
        self.label_font = pygame.font.SysFont(None, 30)
        self.label_width, self.label_height = self.label_font.size("CPU")      #label surface width

        self.currentProcess = None
        self.x_pos = 825                                            #x_pos of cpu image
        self.y_pos = self.label_y_pos+\
                     self.label_height+5                            #y pos pf cpu image
        self.cpu_image = pygame.image.load('cpu.jpg')
        self.width = 150                                            #width of cpu image
        self.height = 153                                           #height of cpu image

    def draw(self, window):
        """draw an outline of the cpu and make it invisible by making the color white
            Also draw the cpu image"""
            
        #draw CPU label
        txt = self.label_font.render("CPU", True, self.color)
        window.blit(txt, [self.label_x_pos, self.label_y_pos])

        # draw cpu image
        window.blit(self.cpu_image, (self.x_pos, self.y_pos))

    
    def center_x(self):
        """returns y coordinates of CPU's center"""
        return self.x_pos + self.width//2


class Process:

    def __init__(self, CPU, queue, id, arrivalTime, burstTime):
        self.CPU = CPU
        self.arriveTime = arrivalTime
        self.burstTime = burstTime
        self.queue = queue
        self.color = (255, 0, 0)                # red color
        self.x_pos = 30
        self.y_pos = self.queue.center_y()
        self.mem_location = -1                  # memory location process is assigned x coordinate
        self.selected = False                     # process selected by algorithm
        self.radius = CIRCLE_RADIUS
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
        self.setLocation()


    def setLocation(self):
        """if process is within the bounds of the queue then set it as inQueue. if not
            set inQueue to false and if it was marked as in the queue before, remove it.
            Likewise if process is in the cpu set it as inCpu else set inCpu to false"""

        if self.center_x() >= self.queue.nextAvailableLocation():
            if not self.inQueue:
                self.mem_location = self.queue.nextAvailableLocation()
                self.queue.lockMemLocation(self.mem_location)
                self.queue.queue.append(self)
                self.inQueue = True
        else:
            self.inQueue = False


        if (self.end_x() > self.CPU.x_pos) and (self.start_x() < self.CPU.x_pos+self.CPU.width):
            self.inCPU = True
            self.CPU.currentProcess = self
        else:
            self.inCPU = False
    
    def getProximity(self):
        """"returns location of process as a tuple (inQueue, inCPU)"""
        return (self.inQueue, self.inCPU)

    def getBurstTime(self):
        """get estimated burst time of process"""
        return self.burstTime
    
    def getArrivalTime(self):
        """get arrival time of process"""
        return self.arriveTime

    def end_x(self):
        """get the ending x point of the process circle"""
        return self.x_pos + self.radius
    
    def start_x(self):
        """get the starting x point of the process circle"""
        return self.x_pos - self.radius

    def center_x(self):
        """get x position of circle (center of circle)"""
        return self.x_pos
    
    def getMemLocation(self):
        """returns the x coordinate of the memory location in queue that process was assigned"""
        return self.mem_location
    
    def changeMemLocation(self):
        """"decrements current memory location. OS detects available space in the queue
         and shifts process to memory location immediately to it's right"""
        self.queue.unlockMemLocation(self.mem_location)

        if not self.selected:
            self.mem_location+= 2*CIRCLE_RADIUS
            #print(self.mem_location)
            self.queue.lockMemLocation(self.mem_location)
            # print(self.mem_location)


run = True

def closeGameOnQuit():
    global run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


if __name__ == '__main__':
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 600
    CIRCLE_RADIUS=30    #radius of circle that represents a process
    MAX_QUEUE_SLOTS = 7

    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # os = OS(window,spn.SPN)
    os = OS(window,fcfs.FCFS)
    while run:
        pygame.time.Clock().tick(5)  # frame rate 5 frames per second
        closeGameOnQuit()  # exit on click the quit button
        os.run()
    pygame.quit()