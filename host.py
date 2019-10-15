import threading

def hostloshod(test):
    print('Launching "loshadkin.py"...')
    exec(open("loshadkin.py").read())
def hostgbball(test):
    print('Launching "gbball.py"...')
    exec(open("gbball.py").read())    
threading.Timer(1,hostloshod,args=['test']).start()
threading.Timer(1,hostgbball,args=['test']).start()
threading.Timer(2,print,args=['All apps launched!']).start() 
