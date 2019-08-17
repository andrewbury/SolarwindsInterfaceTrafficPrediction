Solarwinds Interface Traffic Forecaster 

Concept: This is way to predict what the next N number of values are for a certain interface in your orion database. As with machine learning the results vary so all options should be tested for accuracy. After a model has been ran it outputs a value, the closer that value is to zero the better the model is performing.

Requirements: Python3.6, Keras, Numpy, orionsdk
System Variables must be set to establish connection with orion 
server = os.environ['server']
name = os.environ['name']
password = os.environ['password']

So lets walk through what a typical forecast can look like

First download and change into the project 

then run the command :
"python CreatModel.py inOrOut interfaceID algorithm numberInSeries"
where the variables
inOrOut: To monitor the  interface's traffic BPS going in or out 
interfaceID: what the ID is for that interface (same as in SWIS)
algorithm: the algorithm to try and map the time series only 4 are available ("cnn3","cnn24", "lstm", "lstmcnn")
numberInSeries: the length of the time series to pull from SWIS (should be longer than 400)

Over here a typical command could look like: 
"C:\dev\Python\Forecaster>python CreateModel.py in 6924 cnn3 1000"

This command will walk you through the process of generating the model and at the end output a score back to you, the closer the score is to zero the better the model is performing. 

The last few lines of output are:


Epoch 27/30
798/798 [==============================] - 0s 30us/step - loss: 0.0071

Epoch 28/30
798/798 [==============================] - 0s 29us/step - loss: 0.0071

Epoch 29/30
798/798 [==============================] - 0s 30us/step - loss: 0.0071

Epoch 30/30
798/798 [==============================] - 0s 30us/step - loss: 0.0071
196/196 [==============================] - 0s 148us/step
0.007097733344844714

Rounding that leads the exact same thing, that will rarely happen as one is a training set and one is a testing set but hey kinda cool that it did. 

It should be noted that two files were created. 
Those are used to store the model and the weights associated with the model. 
They have a date associated with them so you can know if the data is somewhat old. I woud say fresh data should be monthly updated. 

Play around with the interface ids and each algorithm seeing which one works(AKA what has the best score) for which type of interface(some interfaces are on the edge of networks and have bursty behavior whereas some are in the center of a network and have somewhat more consistant flow of packets)

If we had a typical router that we wanted to know information about we can set a script to maybe make calls to see what the next n guesses would be. (the larger the value of n the more imprecise the values will get)

So lets make a prediction, the command looks like:
"python PredictNext.py inOrOut interfaceID algorithm withSmoothing"

all three of inOrOut interfaceID and algorithm variables are the same as before

withSmoothing: if we are going to feed the values smoothed (AKA have had a log base 10 transform done already)

I would say to always have withSmoothing set to f so that you can just send the scipt the last window_size of values. 

IMPORTANT: once you launch the PredictNext.py script you will be prompted to enter in a window_size of the last values so the model can predict the next value. The model will only predict the next value associated with the previous window_size of time units. So you must enter in the correct last window_size of values from your orion database. If I was using cnn3 which uses a window_size = 3, i would enter into stdin the value 3 units behind first, 2 units behind second, and 1 unit behind third. Send the values seperated by a space. The script will then output what its next guess is given the last window size. If you want to have the script keep guessing you just shift everything over. Input to stdin would look like value 2 units behind first, value 1 unit behind second, and first predict value third. The model will then give its second predict value, this can continue but it gets less accurate as you continue. 

Algorithm window_size 

cnn3 lstm and lstmcnn use window_size = 3

cnn24 has window_size = 24



Alright, happy predicting 