import threading

def hostloshod(test):
    print('Launching "loshadkin.py"...')
    execfile("loshadkin.py")
    
threading.Timer(1,hostloshod,args=['test']).start()

print('All apps launched!')    
