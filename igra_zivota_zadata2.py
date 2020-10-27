import numpy as np
import random
import threading 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import sys
import queue
N = 4
matrica=np.random.randint(2,size=(N,N))
listaMatrica = []
brojacCelija = 0

print(matrica) 

brojacCelijaLock = threading.Lock()
sledecaIteracija=threading.Condition()

class Celija(threading.Thread):
    def __init__(self,stanje,i,j):
        super().__init__()
        self.iteracija=0
        
        self.stanje=stanje
        self.i=i
        self.j=j
        self.stanjeKomsija = queue.Queue(maxsize=8)    

    
    
    def proveraSuseda(self):
        for x in range(self.i - 1, self.i + 2):
            for y in range(self.j - 1, self.j + 2):
                if x == self.i and y == self.j:
                    continue
                
                if x<0 or x>= N:
                    x=x % N
                if y < 0 or y>=N:
                    y = y % N
                self.azurirajQueue(x,y)      
                   
    
    def azurirajQueue(self,x,y):
        for celija in listaCelija:
            if celija.i == x and celija.j == y:
                celija.stanjeKomsija.put(self.stanje)
                 
    
 
                
           
          


    def promenaStanja(self,ziveKomsije):
        global matrica
        global brojacCelija

        if ziveKomsije < 2 or ziveKomsije > 3:
            self.stanje = 0
            matrica[self.i,self.j]=0
        elif self.stanje == 1 and (ziveKomsije == 2 or ziveKomsije == 3):
            self.stanje = 1
            matrica[self.i,self.j]=1
        elif self.stanje == 0 and ziveKomsije == 3:
            self.stanje = 1
            matrica[self.i,self.j]=1

        brojacCelijaLock.acquire()

        brojacCelija +=1

        brojacCelijaLock.release()

        self.iteracija+=1
        
    def run(self):
        global brojacCelija
       
        for _ in range(0,3):
            self.proveraSuseda()
            ziveKomsije=0
            for _ in range(0,8):
                
                ziveKomsije+=self.stanjeKomsija.get()
                
            
            time.sleep(0.1)
            
           
            self.promenaStanja(ziveKomsije)
            
            brojacCelijaLock.acquire()
            if brojacCelija == N * N:
                brojacCelija=0
                listaMatrica.append(matrica.copy())
                brojacCelijaLock.release()
                sledecaIteracija.acquire()
                sledecaIteracija.notify_all()
                sledecaIteracija.release()

            else:
                brojacCelijaLock.release()
                sledecaIteracija.acquire()
                sledecaIteracija.wait()
                sledecaIteracija.release()    


                           
listaCelija=[]         
for i in range(0,N):
    for j in range(0,N):
        celija = Celija(matrica[i][j],i,j)
        listaCelija.append(celija)
for celija in listaCelija:
    celija.start()
for celija in listaCelija:
    celija.join()


for matrica in listaMatrica:
   print(matrica)




   




           

