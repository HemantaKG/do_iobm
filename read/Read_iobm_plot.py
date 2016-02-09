'''
Created on Oct 13, 2015

@author: hemant
'''
#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy

no_threads= 6
x = [0.1, 1, 10, 100, 1000, 5000, 10000]#Block size in MB
y = []
y1= []
directory_path= "/home/hemant/icts_hemanta_ws/IO_Banchmarking/src/storage/read1"#path to data-sets

fig = plt.figure(figsize=(6,4))
fig.suptitle('Read Performance on raidz2', fontsize=10, fontweight='bold')
ax = fig.add_subplot(111)

def ReadDataPoints(directory_path, thread):
    global y, y1
    y= []
    y1=[]
    fileName= directory_path+"/file_read_thread"+str(thread)+".txt"
    fop = open(fileName, 'r')
    lines = fop.readlines()
    fop.close()
    
    y100kB= []
    y1MB = []
    y10MB = []
    y100MB = []
    y1GB = []
    y5GB = []
    y10GB= []
    
    def conv_strore(s):
        if "kB/s" in line.split(' ')[13]:
            s.append(float(line.split(' ')[12])/ 1000000) # convert to GB
        elif "MB/s" in line.split(' ')[13]:
            s.append(float(line.split(' ')[12])/ 1000) # convert to GB
        else:
            s.append(float(line.split(' ')[12]))
    
    for line in lines:
        #print "kB/s" in line.split(' ')[13]
        if line.find("10 GB")!= -1:
            conv_strore(y10GB)
        
        if line.find("5.0 GB")!= -1:
            conv_strore(y5GB)
        
        if line.find("1.0 GB")!= -1:
            conv_strore(y1GB)
                
        if line.find("100 kB")!= -1:
            conv_strore(y100kB)
                
        if line.find("1.0 MB")!= -1:
            conv_strore(y1MB)
                
        if line.find("10 MB")!= -1:
            conv_strore(y10MB)
                
        if line.find("100 MB")!= -1:
            conv_strore(y100MB)
            
    y.append((numpy.average(y100kB))*8)
    y.append((numpy.average(y1MB))*8)
    y.append((numpy.average(y10MB))*8)
    y.append((numpy.average(y100MB))*8)
    y.append((numpy.average(y1GB))*8)
    y.append((numpy.average(y5GB))*8)
    y.append((numpy.average(y10GB))*8)
    
    y100kB = None
    y1MB = None
    y10MB = None
    y100MB = None
    y1GB = None
    y5GB = None
    y10GB = None
    
    ax.semilogx(x,y, marker='o', label= "thread"+str(thread))
    #for xy in zip(x, y):                                                
        #ax.annotate('(%s, %s)' % xy, xy=xy) 

def read_WriteDataFile(directory_path):
    thread_list= []
    for i in range(no_threads):
        thread_list.append(2**i)
    for thread in thread_list:
        ReadDataPoints(directory_path, thread) 
        
def show_Plot():
    ax.set_xlabel('block size(MB) in log scale', fontsize= 7)
    ax.set_ylabel('bandwidth per thread (Gbits/sec)', fontsize= 7)
    plt.legend(loc=2, ncol= 1, borderaxespad=0., prop={'size':6})
    plt.grid()
    plt.savefig('12_read_performance_raidz2.png',dpi=200)
    #plt.show()
    
def main():
    read_WriteDataFile(directory_path)
    show_Plot()
    print 'END'
    
if __name__== "__main__":
    main()
