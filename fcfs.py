class FCFS:

    def __init__(self, queue):
        self.queue = queue

    def selectProcess(self, lock):
        """select next process to execute"""
        
        ready_queue = self.queue.getQueue()                     #get ready queue    
        if ready_queue:                                         #if a job was found in queue
            next_job =  ready_queue[0]                                                                      
    
            if not lock:
                next_job.selected = True                        # if lock not on move process beyond front and set lock to true
                next_job.move()                                 #moves process to CPU
                index = self.queue.getQueue().index(next_job)   #index of shortest job in queue
                self.queue.removeProcess(index)                     #removes process from queue
                self.queue.unlockMemLocation(next_job.getMemLocation()) #frees up queue slot another process 
                # print("Move Process to CPU")
                lock = True
        return lock
