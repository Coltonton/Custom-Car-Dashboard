import pyfirmata
import time



ardMega = pyfirmata.Arduino('COM8')
#it = pyfirmata.util.Iterator(ardMega)
#it.start()

#ardMega.digital[10].mode = pyfirmata.INPUT

while True:
    ardMega.digital[13].write(1)
    #sw = ardMega.digital[10].read()
    #print(sw)
    time.sleep(1)
    ardMega.digital[13].write(0)
    time.sleep(1)
    
