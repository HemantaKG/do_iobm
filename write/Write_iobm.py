'''
Created on Oct 12, 2015

@author: hemant
'''

import subprocess
import threading
import datetime, time
from optparse import OptionParser

N= None # no of sets
T= None # no of threads
outfilename= None
block_size= [0.1, 1, 10, 100, 1000, 5000, 10000]# block size in MB

class iobmThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID= threadID
        self.name= name
    def run(self):
	#print "Starting " + self.name
	for i in block_size:
		if threading.activeCount() <= T+1:
        		iobm_multithread_read(self.name, i)
			time.sleep(10)
	#print "Exiting " + self.name

def free_drivecache():
    cmd_free_cache= "sync && sh -c 'echo 3 > /proc/sys/vm/drop_caches'"
    subprocess.Popen(cmd_free_cache, shell=True)

def iobm_multithread_read(threadName, i):
    out_write = open(outfilename, 'a') #write operation stdout into file "rx.txt"
    size= int(i* 1000) # block size in KB
    if size <= 1000000:
    	free_drivecache()
	cmddd= "dd if=/dev/zero of=/home/test/file_"+str(size)+" bs="+ str(size) +"kB count=1 conv=fdatasync oflag=dsync"
        p= subprocess.Popen(cmddd, shell=True, stderr=subprocess.PIPE)
        ts_end= datetime.datetime.now()
        wr= str(p.communicate())+threadName+'\n'
    else:
	free_drivecache()
	cmddd= "dd if=/dev/zero of=/home/test/file_1000000 bs=1000000kB count=" + str(i/1000) +" conv=fdatasync oflag=dsync"
        p= subprocess.Popen(cmddd, shell=True, stderr=subprocess.PIPE)
        wr= str(p.communicate())+threadName+'\n'
    out_write.write(wr)
    out_write.close()

def iobm(T):
    thread = None
    thread_instance= []
    for i in range(T):
        thread_instance.append(iobmThread(i, "Thread-"+str(i)))# Create new threads
    for thread in thread_instance: # Start new Threads
        thread.start()
    for thread in thread_instance: # join all new Threads
        thread.join()

def main():
    i= 1
    while i <= N:
	if threading.activeCount() == 1:
		print "set count: " +str(i)
        	iobm(T)# call method to create thread
        	time.sleep(10)
        	i= i+1
    print "Exiting Main Thread"

if __name__ == "__main__":
    parser= OptionParser()
    parser.add_option("-t", "--threads", dest="threads", default="2", help="total # of threads")
    parser.add_option("-s", "--sampleset", dest="sampleset", default="10", help="total # of sample sets")
    (option, arge)= parser.parse_args()
    
    T= int(option.threads)
    N= int(option.sampleset)
    outfilename= "file_write_thread" + str(T) + ".txt"
    
    main()
