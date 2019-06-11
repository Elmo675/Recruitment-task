#!/usr/bin/python3
from multiprocessing import Process, Manager, Value, cpu_count
from functions import grab_text,grab_photo 

#Classes
class Task:
    def __init__(self,Type,Url):
        #initialize the variables
        self.func = grab_text if Type == 'text' else grab_photo
        self.url  = Url
        self.manager = Manager()
        self.result = self.manager.list()
        
        # status determine the progress of task
        #-2 = Cannot make new folder
        #-1 = Error while handling the site connection
        # 0 = Task created  
        # 1 = Connection completed
        # 2 = Url formated 
        # 3 = Task Done
        self.INFO = ["Can't make new folder","Error while handling the site connection",
                     "Task created","Connection completed",
                     "Url formated","Task Done"]
        self.status = Value('i',0)
        self.start()
        
    def start(self):
        Process(target = self.func , args = self.get_args()).start()

    def get_args(self):
        return [self.url,self.status,self.result]

    def get_result(self):
        return self.result

    def get_status(self):
        return self.status.value



#class Task_Menager:
#    def __init__(self,cpu_count):
#        self.cpu_count = Value('i',cpu_count)
#        self.manager = Manager() 
#        self.que = self.manager.list()
#        self.done = self.manager.list()
#        Process(target = run , args = [self.que,self.done,self.cpu_count]).start()
#
#    def add_task(self,task):
#        self.que.put(task)
#        self.number +=1
#        
#    def get_result(self):
#        return self.done


    
#def run(que,done,cpu_count):
#    for ii in range(10000):
#        for i in range(len(que)):
#            item = que[i]
#            status = item.get_status()
#            if status == 0 and cpu_count.value >0:
#                item.start()
#                cpu_count.value -=1
#            if status == 3:
#                cpu_count.value +=1
#                done.append([self.que[count].get_id(),self.que[count].get_result()])
#                del que[i]
#            if status == -1:
#                del que[i]

        
def test_Task_Controll_Positive(Url,Type='text'):
    test = Task(Type,Url)
    test.start()
    while (test.get_status() !=3):
        None
    result = test.get_result()
    for i in range(len(result)):
        print (result[i])
    print()
    print (test.get_status())

def test_Task_Controll_Negative(Url,Type='text'):    
    test = Task(Type,Url)
    test.start()
    while (test.get_status() >= 0):
        None
    print (test.get_status())
#def test2():
#    manager = Manager() 
#    que = manager.list()
#    done = manager.list()
#    test = Task_Menager(2,que,done)
#    test.add_task(Task('text','https://www.quora.com/How-can-I-extract-only-text-data-from-HTML-pages'))
#    for _ in range(1000):
#        print(test.get_result())


if __name__ == '__main__':
    #Test Purpose
    print ("Test positive text")
    test_Task_Controll_Positive('https://www.quora.com/How-can-I-extract-only-text-data-from-HTML-pages')
    print ("Test positive image(no images)")
    test_Task_Controll_Positive('https://www.quora.com/How-can-I-extract-only-text-data-from-HTML-pages','image')
    print ("Test positive image (images downloaded)")
    test_Task_Controll_Positive('https://pixabay.com/','image')
    print ("Test negative text")
    test_Task_Controll_Negative('https://www.quoradada.com/How-can-I-extract-only-text-data-from-HTML-pages')
    print ("Test negative image")
    test_Task_Controll_Negative('www.google.com','image')
    
    
    

