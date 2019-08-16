from Helpers import forecaster
import sys
import datetime
import numpy as np
from CreateModel import createFilenames

"""
When taking in values from stdin you must cast to a float before doing math arthmetic 
"""
def getSmoothedInput():
    window = [i for i in input().split()]
    smoothed_window = list()
    for row in window:
        smoothed_window.append(float(row))
    return np.log(smoothed_window)



"""
Parameters: <direction> "in","out" (Tells what direction on the interface to analyze)      
    <interfaceID>  1, 2, 3, ..., n (integer id of interface to analyze)
    <algorithm> "cnn3","cnn24", "lstm", "lstmcnn" (algorithm that was used to train model)
    <with_smoothing> "t", "f" (if the values that we are inputing into the model are smoothed or not)

Input: Takes in as input from stdin a double array of size window_size(see model creation)

Output: Print the next forecasted value given the previous window_size

Summary: 
    This script is used to predict what the next n points will be for a interface's in / out bps
    This script is dependent on the CreateModel.py script which is used to intially create a model 
    It should be noted that all models are currently being saved as two different files (see method getFilenames above)
"""
def main():

    if len(sys.argv) != 5:
        quit("ERROR:\nParameters: <direction> <interfaceID> <algorithm> <with_smoothing>")

    inOrOut = sys.argv[1]#options: "in", "out"
    interfaceid = int(sys.argv[2])#option: whatever is in your orion database for interfaceids
    algorithm = sys.argv[3]#options: cnn3, cnn24, lstm, lstmcnn
    with_smoothing = sys.argv[4]#options: t, f // if they are expected to have log transformed the data yet


    filename, weight_file = createFilenames(inOrOut, interfaceid, algorithm)

    model = forecaster.getModel(filename, weight_file)

    if with_smoothing == "t":
        while True:
            window = [i for i in input().split()]
            predictions = forecaster.predict_next(model, window, len(window))
            print("prediction= " + str(predictions[0][0]))
    else:
        while True:
            smooth = getSmoothedInput()#np.log(smoothed_window)
            predictions = forecaster.predict_next(model, smooth, len(smooth))
            print("prediction= " + str(np.exp(predictions[0][0])))




    


if __name__ == '__main__':
    main()