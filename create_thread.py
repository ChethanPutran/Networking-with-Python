import threading

#Create threads
def create_thread(ip_list,credentials,functionToPerform):
    threads = []
    usernames,passwords = credentials

    for i,ip in enumerate(ip_list):
        th = threading.Thread(target=functionToPerform,args=(ip,usernames[i],passwords[i]))#args is a tuple with single element
        th.start()
        threads.append(th)

    #Instruct the program to wait until all thread has finished
    for th in threads:
        th.join()
        
     