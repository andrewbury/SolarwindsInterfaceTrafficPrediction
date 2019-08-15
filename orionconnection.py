import orionsdk 
import requests
import pandas as pd
import numpy
import os 


server = os.environ['server']
name = os.environ['name']
password = os.environ['password']


swis = orionsdk.SwisClient(server, name, "")

verify = False
if not verify:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def getInterface(series_length, interface_id):
    s = "Select TOP "
    s += str(series_length)
    s += " it.InterfaceID, it.DateTime, it.InAveragebps, it.OutAveragebps FROM Orion.NPM.InterfaceTraffic it where InterfaceID = "
    s += str(interface_id)
    results = swis.query(s)

    times = list()
    ins = list()
    insTrains = list()
    outs = list()
    outsTrains = list()
    itr = 0

    series_length = int(series_length)
    percentile = ((series_length / 5) * 4)

    for row in results['results']:
        
        times.append(row['DateTime'])
        if itr >= series_length:
            break
        if itr > percentile:
            insTrains.append(numpy.log(row['InAveragebps']))
            outsTrains.append(numpy.log(row['OutAveragebps']))
            itr += 1
            continue 
        ins.append(numpy.log(row['InAveragebps']))
        outs.append(numpy.log(row['OutAveragebps']))
        itr += 1

    return ins, insTrains, outs, outsTrains