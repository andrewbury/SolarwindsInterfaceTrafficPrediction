import forecaster 
import orionconnection
import sys
from numpy import array
import rollingwindow
import datetime

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



def main():


    if len(sys.argv) != 5:
        quit()

    inOrOut = sys.argv[1]#options: "in", "out"
    interfaceid = int(sys.argv[2])#option: whatever is in your orion database for interfaceids
    algorithm = sys.argv[3]#options: cnn3, cnn24, lstm, lstmcnn
    length_series = int(sys.argv[4])#option: integer(above 400 in length)


    ins, insTrains, outs, outsTrains = orionconnection.getInterface(length_series, interfaceid)

    sequence = ins
    trains = insTrains

    n_features = 1

    if inOrOut == "out":
        sequence = outs
        trains = outsTrains
      
    
    if algorithm == "cnn3":
        window_size = 3
        model = forecaster.getModelCNNWindow3(sequence)
    elif algorithm == "cnn24":
        window_size = 24
        model = forecaster.getModelCNNWindow24(sequence, window_size, n_features)
    elif algorithm == "lstm":
        window_size = 3
        model = forecaster.getModelLSTM(sequence)
    elif algorithm == "lstmcnn":
        window_size = 3
        model = forecaster.getModelLSTM(sequence)
    
    filename, weightfile = createFilenames(inOrOut, interfaceid, algorithm)
    

    forecaster.saveModel(model, filename, weightfile)
    


if __name__ == '__main__':
    main()
