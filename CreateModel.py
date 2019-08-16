import forecaster 
import orionconnection
import sys
from numpy import array
import rollingwindow
import datetime


"""
Creates a unique identifier via parameters given through command line and time of year/month
"""

def createFilenames(inOrOut, interfaceid, algorithm):
    dt = datetime.datetime.today()
    filename = ""
    filename += str(inOrOut)
    filename += str(interfaceid)
    filename += str(algorithm)
    filename += str(dt.year)
    filename += str(dt.month)
    filename += str(".json")

    weight_file = ""
    weight_file += str(inOrOut)
    weight_file += str(interfaceid)
    weight_file += str(algorithm)
    weight_file += str(dt.year)
    weight_file += str(dt.month)
    weight_file += str(".h5")

    return filename, weight_file


"""
Parameters: <direction> "in","out" (Tells what direction on the interface to analyze)      
    <interfaceID>  1, 2, 3, ..., n (integer id of interface to analyze)
    <algorithm> "cnn3","cnn24", "lstm", "lstmcnn" (algorithm that was used to train model)
    <length_series> 500, 1000, 5000 (length of time series to pull from orion sdk)
"""
def main():


    if len(sys.argv) != 5:
        quit("ERROR:\nParameters: <direction> <interfaceID> <algorithm> <length_series>")

    inOrOut = sys.argv[1]#options: "in", "out"
    interfaceid = int(sys.argv[2])#option: whatever is in your orion database for interfaceids
    algorithm = sys.argv[3]#options: cnn3, cnn24, lstm, lstmcnn
    length_series = int(sys.argv[4])#option: integer(above 400 in length)

    ins, insTrains, outs, outsTrains = orionconnection.getInterface(length_series, interfaceid)

    sequence = ins
    trains = insTrains

    n_features = 1
    window_size = 3

    if inOrOut == "out":
        sequence = outs
        trains = outsTrains   
    
    if algorithm == "cnn3":
        model = forecaster.getModelCNNWindow3(sequence)
    elif algorithm == "cnn24":
        window_size = 24
        model = forecaster.getModelCNNWindow24(sequence, window_size, n_features)
    elif algorithm == "lstm":
        model = forecaster.getModelLSTM(sequence)
    elif algorithm == "lstmcnn":
        model = forecaster.getModelLSTM(sequence)
    
    filename, weightfile = createFilenames(inOrOut, interfaceid, algorithm)
    
    forecaster.saveModel(model, filename, weightfile)

    X, y = rollingwindow.split_sequence(trains, window_size)
    X = X.reshape((X.shape[0], X.shape[1], n_features))

    print(model.evaluate(X, y))
    


if __name__ == '__main__':
    main()
