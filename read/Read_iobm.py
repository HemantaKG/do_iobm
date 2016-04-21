'''
Created on Oct 12, 2015

@author: hemant
'''

import subprocess
import threading
import datetime, time
from optparse import OptionParser

# No of sample sets to run
N= None
# maximum No of threads to run
T= None
# output to be stored into the file 
outfilename= None
# list of data block sizes in MB
block_size= [0.1, 1, 10, 100, 1000, 5000, 10000]
# output file handler
out_write

# thread class which runnes 'dd' command over list of data blocks
class iobmThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID= threadID
        self.name= name
        
    def run(self):
	for i in block_size:
		# active thread count always less than 'T+1' (i.e. main thread+ T), in other words call 'dd' command 
		if threading.activeCount() <= T+1:
			# call 'dd' run function over data block[i], with this thread instance
        		iobm_multithread_read(self.name, i)
			#time.sleep(10)

# call free_drivecache() to free drive cache content...		
#def free_drivecache():
#    cmd_free_cache= "sync && sh -c 'echo 3 > /proc/sys/vm/drop_caches'"
#    subprocess.Popen(cmd_free_cache, shell=True)

def iobm_multithread_read(threadName, i):
    # write results (i.e dd command outputs) into file "file_read_thread<i>.txt"
    #out_write = open(outfilename, 'a')
    # converting data block size from MB to KB
    size= int(i* 1000)
    
    # if data block size less 1000MB i.e 1GB execute if block, for greater than 1GB datablocks execute else block
    if size <= 1000000:
    	# clear drive catch
  	#free_drivecache()
        cmddd= "dd if=/home/hemanta.g/iotest/file"+str(size)+" of=/tmp/file"+str(size) + " bs="+str(size)+"kB count=1"
        p= subprocess.Popen(cmddd, shell=True, stderr=subprocess.PIPE)
        ts_end= datetime.datetime.now()
        wr= str(p.communicate())+threadName+'\n'
    else:
    	# clear drive catch
	#free_drivecache()
        cmddd= "dd if=/home/hemanta.g/iotest/file1000000 of=/tmp/file1000000 bs=1000000kB count="+str(i/1000)
        p= subprocess.Popen(cmddd, shell=True, stderr=subprocess.PIPE)
        wr= str(p.communicate())+threadName+'\n'
        
    # write 'dd' command output into the output file 
    out_write.write(wr)
    #out_write.close()
    
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
		# write results (i.e dd command outputs) into file "file_read_thread<i>.txt"
		out_write = open(outfilename, 'a')
        	iobm(T)
        	out_write.close()
        	
        	time.sleep(10)
        	i= i+1
    print "Exiting Main Thread"

if __name__ == "__main__":
    parser= OptionParser()
    parser.add_option("-t", "--threads", dest="threads", default="2", help="total # of threads")
    parser.add_option("-s", "--sampleset", dest="sampleset", default="10", help="total # of sample sets")
    parser.add_option("-o", "--output", dest="output", default="out_read", help="name of the output file")
    (option, arge)= parser.parse_args()
    
    T= int(option.threads)
    N= int(option.sampleset)
    O= option.ouput
    outfilename= O+ str(T) + ".txt"
    
    main()
