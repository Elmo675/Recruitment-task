#!/usr/bin/python3
from multiprocessing import Process, Manager, Value, cpu_count
from functions import grab_text 


#Classes
class Task:
    def __init__(self,Type,Url):
        #initialize the variables
        self.func = grab_text if Type == 'text' else grab_photo
        self.url  = Url
        self.result = Manager().list()
        
        # status determine the progress of task
        #-1 = Error while handling the site connection
        # 0 = Task created  
        # 1 = Connection completed
        # 2 = URL Text formated 
        # 3 = \<>?
        self.status = Value('i',0)
    def begin(self):
        Process(target = self.func , args = self.get_args()).start()
    def get_args(self):
        return [self.url,self.status,self.result]
    def get_result(self):
        return self.result
    
    def get_status(self):
        return self.status.value


        
    
    


if __name__ == '__main__':
    test = Task('text','https://www.quora.com/How-can-I-extract-only-text-data-from-HTML-pages')
    test.begin()
    while (test.get_status() !=3):
        None
    result = test.get_result()
    for i in range(len(result)):
        print (result[i])
        
    
    
    

