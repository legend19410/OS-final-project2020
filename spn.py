class SPN:

    def __init__(self, queue):
        self.queue = queue

    def selectProcess(self, lock):
        """select next process to execute"""
        shortest_job = self.findShortestJob()                       #finds shortest job in queue
        if shortest_job:                                            #if a job was found in queue
            if not lock:
                shortest_job.selected = True                                            # if lock not on move process beyond front and set lock to true
                shortest_job.move()                                 #moves process to CPU
                index = self.queue.getQueue().index(shortest_job)   #index of shortest job in queue
                self.queue.removeProcess(index)                     #removes process from queue
                self.queue.unlockMemLocation(shortest_job.getMemLocation()) #frees up queue slot another process 
                # print("Move Process to CPU")
                lock = True
        return lock


    def findShortestJob(self):
        """Finds the process with the shortest estimated burst time"""

        ready_queue = self.queue.getQueue()     #get ready queue
        # print(len(ready_queue))
        if(ready_queue):                        #if queue not empty
            shortest_job = ready_queue[0]       #intiliaze the shortest job to first process in queue
            for proc in ready_queue[1:]:
                if proc.getBurstTime() < shortest_job.getBurstTime():
                    shortest_job = proc
            return shortest_job
        return []
