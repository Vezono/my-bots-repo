import threading

def hostloshod(test):
    print('Launching "loshadkin.py"...')
    exec(open("loshadkin.py").read())
    
threading.Timer(1,hostloshod,args=['test']).start()

print('All apps launched!')    
