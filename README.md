Solarwinds Interface Traffic Forecaster 

Concept: This is way to predict what the next N number of values are for a certain interface in your orion database. As with machine learning the results vary so all options should be tested for accuracy. After a model has been ran it outputs a value, the closer that value is to zero the better the model is performing.

Requirements: Python3.6, Keras, Numpy, orionsdk, pandas
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

Testing score 0.007097733344844714

Rounding the testing score leads the exact same as the loss on training, that will rarely happen as one is a training set and one is a testing set but hey kinda cool that it did. 

It should be noted that two files were created. 
Those are used to store the model and the weights associated with the model. 
They have a date associated with them so you can know if the data is old. Keep in mind there generally isn't a need to re-create the model until it starts to make bad predictions. If you dont want to worry about continually checking what the error is then you could always just take the naive appraoch and recreate the model maybe every day, week, or month. 

Play around with the interface ids and each algorithm seeing which one works(AKA what has the best score) for which type of interface(some interfaces are on the edge of networks and have bursty behavior whereas some are in the center of a network and have somewhat more consistant flow of packets)

If we had a typical router that we wanted to know information about we can set a script to maybe make calls to see what the next n guesses would be. (the larger the value of n the more imprecise the values will get)

So lets make a prediction, the command looks like:
"python PredictNext.py inOrOut interfaceID algorithm window_size"

all three of inOrOut interfaceID and algorithm variables are the same as before

window_size: the number of predictions to forecast into the future, the larger the value the more inaccurate the preditions become 


Alright, happy forecasting :)



Summary:
    
    Run the CreateModel.py script until you find a model that outputs a low test score, for starters I would run CreateModel.py with each of the 4 and see which has an output closest to zero. Once you find a model that you like remember those parameters so that you only have to re-train the model (AKA run CreateModel.py) every day, week, or month. 
    
    Run the PredictNext.py script everytime you want to predict what the next N values are for your interface traffic. 
    The larger the value of N the less accurate the model is because it cant use the most recent true values of interface traffic. I would run the PredictNext.py script either every minute, 30 minutes, hour, 6-hours, or day with the window_size set to a low value. The frequency to run this script, which has correlation to window_size, depends how accurate you want your predictions and even more importantly what interval you have polling set to run in orion for interface traffic (AKA every minute, 10 minutes, hour, 6 hours, day ...)