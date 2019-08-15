import forecaster
import sys
import datetime
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



def main():

    inOrOut = sys.argv[1]#options: "in", "out"
    interfaceid = int(sys.argv[2])#options: whatever is in your orion database for interfaceids
    algorithm = sys.argv[3]#options: cnn3, cnn24, lstm, lstmcnn

    filename, weight_file = getFilenames(inOrOut, interfaceid, algorithm)

    model = forecaster.getModel(filename, weight_file)

    while True:
        window = [i for i in input().split()]
        predictions = forecaster.predict_next(model, window, len(window))
        print("prediction= " + str(predictions[0][0]))




    


if __name__ == '__main__':
    main()