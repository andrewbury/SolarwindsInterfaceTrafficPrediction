import forecaster
import sys
import datetime
import numpy as np
def getFilenames(inOrOut, interfaceid, algorithm):
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


def getSmoothedInput():
    window = [i for i in input().split()]
    smoothed_window = list()

    for row in window:
        smoothed_window.append(float(row))
    return np.log(smoothed_window)

def main():

    if len(sys.argv) != 5:
        quit()

    inOrOut = sys.argv[1]#options: "in", "out"
    interfaceid = int(sys.argv[2])#option: whatever is in your orion database for interfaceids
    algorithm = sys.argv[3]#options: cnn3, cnn24, lstm, lstmcnn
    with_smoothing = sys.argv[4]#options: t, f // if they are expected to have log transformed the data yet

    filename, weight_file = getFilenames(inOrOut, interfaceid, algorithm)

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