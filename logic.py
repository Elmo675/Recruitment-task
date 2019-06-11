#!/usr/bin/python3
from multiprocessing import Process,Queue, Manager, Value, cpu_count
from functions import grab_text 

#Classes
class Task:
    def __init__(self,Type,Url):
        #initialize the variables
        self.func = grab_text if Type == 'text' else grab_photo
        self.url  = Url
        self.manager = Manager()
        self.result = self.manager.list()
        self.id = id(self)
        
        # status determine the progress of task
        #-1 = Error while handling the site connection
        # 0 = Task created  
        # 1 = Connection completed
        # 2 = URL Text formated 
        # 3 = Task Done
        self.status = Value('i',0)

    def start(self):
        Process(target = self.func , args = self.get_args()).start()

    def get_args(self):
        return [self.url,self.status,self.result]

    def get_result(self):
        return self.result

    def get_status(self):
        return self.status.value

    def get_id(self):
        return self.id

class Task_Menager:
    def __init__(self,cpu_count,que,done):
        self.cpu_count = Value('i',cpu_count)
#        self.manager = Manager() 
#        self.que = self.manager.list()
#        self.done = self.manager.list()
        self.done = done
        self.que = Queue()
        Process(target = run , args = [self.que,self.done,self.cpu_count]).start()

    def add_task(self,task):
        self.que.put(task)
        self.number +=1
        
    def get_result(self):
        return self.done


    
def run(que,done,cpu_count):
    for ii in range(10000):
        for i in range(len(que)):
            item = que[i]
            status = item.get_status()
            if status == 0 and cpu_count.value >0:
                item.start()
                cpu_count.value -=1
            if status == 3:
                cpu_count.value +=1
                done.append([self.que[count].get_id(),self.que[count].get_result()])
                del que[i]
            if status == -1:
                del que[i]

        
def test1():
    test = Task('text','https://www.quora.com/How-can-I-extract-only-text-data-from-HTML-pages')
    test.start()
    while (test.get_status() !=3):
        print (test.get_status())
    result = test.get_result()
    for i in range(len(result)):
        print (result[i])

def test2():
    manager = Manager() 
    que = manager.list()
    done = manager.list()
    test = Task_Menager(2,que,done)
    test.add_task(Task('text','https://www.quora.com/How-can-I-extract-only-text-data-from-HTML-pages'))
    for _ in range(1000):
        print(test.get_result())


if __name__ == '__main__':
    test2()
    
        
    
    
    

