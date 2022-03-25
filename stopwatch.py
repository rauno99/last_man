import time
class Stopwatch():
    def __init__(self):
        self.count = 0
        self.t = "00:00:00"

    def reset(self):
        self.count=1
        self.t = ('00:00:00')     

    def start(self):
        self.count=0
        self.timer()   

    def stop(self):
        self.count=1

    def timer(self):
        if(self.count==0):
            self.d = str(self.t)
            h,m,s = map(int,self.d.split(":")) 
            h = int(h)
            m=int(m)
            s= int(s)
            if(s<59):
                s+=1
            elif(s==59):
                s=0
                if(m<59):
                    m+=1
                elif(m==59):
                    m=0
                    h+=1
            if(h<10):
                h = str(0)+str(h)
            else:
                h= str(h)
            if(m<10):
                m = str(0)+str(m)
            else:
                m = str(m)
            if(s<10):
                s=str(0)+str(s)
            else:
                s=str(s)
            self.d=h+":"+m+":"+s           
            self.t = self.d
            print(self.t)
            if(self.count==0):
                time.sleep(1)
                self.timer()
stopwatch=Stopwatch() 
stopwatch.start()