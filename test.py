from Dapp import Dapp
import sys 
import os 


if __name__=="__main__":
    source_path = os.environ['HOME']+'/HW3/Dapp.sol'

    dapp = Dapp(source_path)

    print ("Checking if contract is alive")

    alive= dapp.check_alive()

    if not alive:
        sys.exit("Contract not alive")

    print ("Registering Users...")

    rt=dapp.registerUser(1,"u1")
    print (rt)
    print ("="*20)
    rt=dapp.registerUser(1,"u2")
    print(rt)
    print ("="*20)
    rt=dapp.registerUser(2,"u2")
    print(rt)
    print ("="*20)
    rt=dapp.registerUser(2,"u2")
    print(rt)
    print ("="*20)   
    dapp.exit()