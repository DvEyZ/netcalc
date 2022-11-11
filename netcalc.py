# Network Calculator

import ipaddress as ip

def help(args):
    if (len(args) == 0):
        print("NetCalc commands:\n"
        "help - view a list of commands.\n"
        "netinfo ipaddress/mask - get informations about a network.\n"
        "vlsm network_address/mask subnet_1_size subnet_2_size ... - calculate how to divide network into subnets of specified size\n"
        "exit - ends NetCalc session")
    else:
        print("Invalid syntax")

def get_subnet_bytes(x):
    n = 0
    while ((2**n - 2) < x):
        n = n+1
    return 32 - n

def vlsm(args):
    if (len(args) < 2):
        print("Invalid syntax.")
        return None
    ipsplit = args[0].split("/")
    try:
        adres = ip.ip_address(ipsplit[0])
        
    except ValueError:
        print("Invalid address.")
        return None
    try:
        maska_int = int(ipsplit[1])
        if (maska_int < 0 or maska_int >= 32):
            print("Invalid mask.")
            return None
        maska_str = ""
        for i in range (0, maska_int):
            maska_str += "1"
        for i in range (maska_int, 32):
            maska_str += "0"
        maska_bin = int(maska_str, base=2)
        maska = ip.ip_address(maska_bin)
    except ValueError:
        print("Invalid mask.")
        return None
    if(adres != ip.ip_address(int(adres) & int(maska))):
        print("Invalid address.")
        return None
    subnets = []
    args.pop(0)
    for i in args:
        try:
            subnets.append(int(i))
        except:
            print("Invalid subnet.")
    j = 0
    last = adres
    for i in subnets:
        x = get_subnet_bytes(i)
        newmask = ''
        for i in range(0, x):
            newmask += '1'
        for i in range(0, 32 - len(newmask)):
            newmask += '0'
        print("Subnet " + str(j) + ": ")
        last = int(netinfo_out(ip.ip_address(last), ip.ip_address(int(newmask, base=2)))) + 1
        j = j+1
        print()

def netinfo(args):
    if (len(args) != 1):
        print("Invalid syntax.")
        return None
    ipsplit = args[0].split("/")
    try:
        adres = ip.ip_address(ipsplit[0])
    except ValueError:
        print("Invalid address.")
        return None
    try:
        maska_int = int(ipsplit[1])
        if (maska_int < 0 or maska_int >= 32):
            print("Invalid mask.")
            return None
        maska_str = ""
        for i in range (0, maska_int):
            maska_str += "1"
        for i in range (maska_int, 32):
            maska_str += "0"
        maska_bin = int(maska_str, base=2)
        maska = ip.ip_address(maska_bin)
    except ValueError:
        print("Invalid mask.")
        return None
    except:
        print("An unknown exception occured")
        return None

    adres_sieci = ip.ip_address(int(adres) & int(maska))

    netinfo_out(adres_sieci, maska)

def netinfo_out(s, m):
    b = ip.ip_address((int(s) | ~int(m)) + 2 ** 32)
    print("Network address:   " + str(s))
    print("Subnet mask:       " + str(m))
    print("Broadcast address: " + str(b))
    print("Host number:       " + str(int(b) - int(s) - 1))
    return b

def inp():
    print("NetCalc > ", end="")
    wejscie = input()
    wejscie_p = wejscie.split(" ")
    if (wejscie_p[0] == "netinfo"):
        netinfo(wejscie_p[1:])
    elif (wejscie_p[0] == "help"):
        help(wejscie_p[1:])
    elif (wejscie_p[0] == "exit"):
        quit()
    elif (wejscie_p[0] == "vlsm"):
        vlsm(wejscie_p[1:])

print(
    "+-----------------------------------------+\n"
    "|  Welcome to NetCalc network calculator. |\n"
    "|  Type \"help\" for the list of commands.  |\n"
    "+-----------------------------------------+\n") 
while (True):
    inp()

