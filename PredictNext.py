from Helpers import forecaster
from Helpers import orionconnection
import sys
import datetime
import numpy as np
from CreateModel import createFilenames

"""
Parameters: <direction> "in","out" (Tells what direction on the interface to analyze)      
    <interfaceID>  1, 2, 3, ..., n (integer id of interface to analyze)
    <algorithm> "cnn3","cnn24", "lstm", "lstmcnn" (algorithm that was used to train model)
    <window_size> 1, 6, 24 (integer of how many values you wish to forecast, gets less accurate the larger you go)

Input: Takes in as input from stdin a double array of size window_size(see model creation)

Output: Print the next forecasted value given the previous window_size

Summary: 
    This script is used to predict what the next n points will be for a interface's in / out bps
    This script is dependent on the CreateModel.py script which is used to intially create a model 
    It should be noted that all models are currently being saved as two different files (see method getFilenames above)
"""
def main():

    if len(sys.argv) != 5:
        quit("ERROR:\nParameters: <direction> <interfaceID> <algorithm> <window_size>")

    inOrOut = sys.argv[1]#options: "in", "out"
    interfaceid = int(sys.argv[2])#option: whatever is in your orion database for interfaceids
    algorithm = sys.argv[3]#options: cnn3, cnn24, lstm, lstmcnn
    window_size = int(sys.argv[4])#)options: int, amount they want us to predict


    filename, weight_file = createFilenames(inOrOut, interfaceid, algorithm)

    model = forecaster.getModel(filename, weight_file)


    lastNum = 3
    if algorithm == "cnn24":
        lastNum = 24

    #last window array is by default set to interface traffic in
    last_window_array, outs = orionconnection.getLatest(lastNum, interfaceid)

    if inOrOut == "out":
        last_window_array = outs
    
    predictions = list()
    itr = 0

    while itr < window_size:
        predictions.append(forecaster.predict_next(model, last_window_array, lastNum)[0][0])
        last_window_array = np.delete(last_window_array, 0)
        last_window_array = np.append(last_window_array, predictions[itr])
        itr += 1
    
    print(predictions)
    
    



    



    


if __name__ == '__main__':
    main()