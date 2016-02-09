'''
Created on Jan 12, 2016

@author: hemant

<<$ filename -t #t -s #s>>
'''

import subprocess
import datetime, time
from optparse import OptionParser
from threading import Thread
import Queue
import glob
import fileinput
import os

noof_sets= None # no of sets
noof_threads= None # no of threads
writefilename= None
tmp_loc= "/tmp/iobm"# tmp storage of output files... marge all at last and store at local derictory...
block_size= [0.1, 1, 10, 100, 1000, 5000, 10000]# block size in MB

class iobmThread (Thread):
    def __init__(self, threadID, name, queue):
        Thread.__init__(self)
        self.threadID= threadID
        self.name= name
        self.queue= queue
        
    def run(self):
        while True:
		#print "Starting " + self.name
		name, i = self.queue.get()
        	iobm_multithread_write(self.name, i)
		#print "Exiting " + self.name
		self.queue.task_done()

# Free IO Buffer and Caches...
def free_drivecache():
    cmd_free_cache= "sync && sh -c 'echo 3 > /proc/sys/vm/drop_caches'"
    subprocess.Popen(cmd_free_cache, shell=True)

def iobm_multithread_write(threadName, i):
    #print "thread in run state: " +threadName
    out_write = open(tmp_loc+"/"+ writefilename+"_"+str(i)+".txt", 'a') #write operation stdout into file "x.txt"
    #ts_start= datetime.datetime.now()
    #lock = threading.Lock()
    #lock.acquire()
    #print "thread in run state: " +threadName +"block size"+ str(i)
    size= int(i* 1000) # block size in KB
    if size <= 1000000:
    	free_drivecache()
	#cmddd= "dd if=/dev/zero of=/tmp/file_"+threadName+"_"+str(size)+" bs="+ str(size) +"kB count=1 conv=fdatasync oflag=dsync"
	cmddd= "dd if=/dev/zero of=/sdisk01/test/file_"+str(size)+" bs="+ str(size) +"kB count=1 conv=fdatasync oflag=dsync"
        p= subprocess.Popen(cmddd, shell=True, stderr=subprocess.PIPE)
        #ts_end= datetime.datetime.now()
        wr= str(p.communicate())+threadName+'\n'
    else:
	free_drivecache()
	#cmddd= "dd if=/dev/zero of=/tmp/file_"+threadName+"_1000000 bs=1000000kB count=" + str(i/1000)+ " conv=fdatasync oflag=dsync"
        cmddd= "dd if=/dev/zero of=/sdisk01/test/file_1000000 bs=1000000kB count=" + str(i/1000)+ " conv=fdatasync oflag=dsync"
	p= subprocess.Popen(cmddd, shell=True, stderr=subprocess.PIPE)
        #ts_end= datetime.datetime.now()
        wr= str(p.communicate())+threadName+'\n'
    out_write.write(wr)
	#free_drivecache()
	#lock.release()	
    out_write.close()
    #print "thread complt run state: " +threadName
    #print ts_end- ts_start



def iobm(noof_threads, bs, queue):
    for q in range(noof_threads):
    	wrkr= iobmThread(noof_threads, "thread"+str(q), queue)
    	wrkr.daemon= True
    	wrkr.start()
    for i in range(noof_threads):
    	queue.put((i, bs))
    queue.join()

def results_out():
    file_list= glob.glob(tmp_loc+"/*.txt")
    with open(writefilename+".txt", "w") as file:
         lines= fileinput.input(file_list)
         file.writelines(lines)
         
def main():
    i= 1
    if not os.path.exists(tmp_loc):
       os.makedirs(tmp_loc)
    queue= Queue.Queue()
    #print threading.activeCount()
    while i <= noof_sets:
	#if threading.activeCount() == 1:
	if queue.empty() == True:
		print "set count: " +str(i)
		for bs in block_size:
        		iobm(noof_threads, bs, queue)# call method to create thread
        	time.sleep(10)
        	i= i+1
    if queue.empty() == True:
    	results_out()
    	os.system("rm -rf "+ tmp_loc)
    print "Exiting Main Thread"
    #print threading.activeCount()

if __name__ == "__main__":
    parser= OptionParser()
    parser.add_option("-t", "--threads", dest="threads", default="2", help="total # of threads")
    parser.add_option("-s", "--sampleset", dest="sampleset", default="10", help="total # of sample sets")
    (option, arge)= parser.parse_args()
    
    noof_threads= int(option.threads)
    noof_sets= int(option.sampleset)
    writefilename= "file_write_thread" + str(noof_threads)# + ".txt"
    
    main()
