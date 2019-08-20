Solarwinds Interface Traffic Forecaster 

Concept: This is way to predict what the next N number of values are for a certain interface in your orion database. As with machine learning the results vary so all options should be tested for accuracy per interface. After a model has been ran it outputs a value, the closer that value is to zero the better the model is performing.

Requirements: Python version 3.6(64bit), Keras, Numpy, orionsdk, pandas

System Variables must be set to establish connection with orion

server = os.environ['server'],
name = os.environ['name'],
password = os.environ['password']

So lets walk through what a typical forecast can look like

First download and change into the project, then install the requirements and set your system variables

The first of the two commands that need to be ran is:
"python CreateModel.py inOrOut interfaceID algorithm numberInSeries"
where the variables
inOrOut: To monitor the  interface's traffic BPS going in or out (options = "in" "out")

interfaceID: what the ID is for that interface (same as in SWIS)

algorithm: the algorithm to try and map the time series only 4 are available ("cnn3","cnn24", "lstm", "lstmcnn")

numberInSeries: the length of the time series to pull from SWIS (should be longer than 100)

Over here a typical command could look like: 
"C:\dev\Python\Forecaster>python CreateModel.py in 6924 cnn3 1000"

This command will start the process of generating the model and at the end output a score back to you, the closer the score is to zero the better the model is performing. 

The last few lines of our output are:


Epoch 27/30
798/798 [==============================] - 0s 30us/step - loss: 0.0071

Epoch 28/30
798/798 [==============================] - 0s 29us/step - loss: 0.0071

Epoch 29/30
798/798 [==============================] - 0s 30us/step - loss: 0.0071

Epoch 30/30
798/798 [==============================] - 0s 30us/step - loss: 0.0071

0.007097733344844714

Rounding the last number (the testing score) leads to the exact same as the loss on training, that will rarely happen as one is a training set and one is a testing set but hey kinda cool that it did. 

It should be noted that two files were created. 
Those are used to store the model and the weights associated with the model. 
The files have a date in their name so you can know if the data is old. Keep in mind there generally isn't a need to re-create the model until it starts to make bad predictions. If you dont want to worry about when the error for predictions has become a problem then you could always just take the naive appraoch and recreate the model maybe every day, week, or month. 

Play around with the interface ids and each algorithm seeing which one works(AKA what has the best score) for which type of interface(some interfaces are on the edge of networks and have bursty behavior whereas some are in the center of a network and have somewhat more consistant flow of packets)

So now that we have a trained model we need to apply it to some real world data to forecast some values. 

So lets make a prediction, the command looks like:
"python PredictNext.py inOrOut interfaceID algorithm window_size"

where all three of the variables inOrOut, interfaceID and algorithm are the same as before

window_size: the number of predictions to forecast into the future, the larger the value the more inaccurate the preditions become 


This command will output to you the window_size number of forecasts, starting with the most recent value first. I would not set too big of a value for window_size as it can tend to get inaccurate after a bit. 

Alright, happy forecasting :)



Summary:
    
    Run the CreateModel.py script until you find a model that outputs a low test score, for starters I would run CreateModel.py with each of the 4 and see which has an output closest to zero. Once you find a model that you like remember those parameters so that you only have to re-train the model (AKA run CreateModel.py) every day, week, or month. 
    
    Run the PredictNext.py script everytime you want to predict what the next N values are for your interface traffic. 
    The larger the value of N the less accurate the model is because it cant use the most recent true values of interface traffic. I would run the PredictNext.py script either every minute, 30 minutes, hour, 6-hours, or day with the window_size set to a low value. The frequency to run this script, which has correlation to window_size, depends how accurate you want your predictions and even more importantly what interval you have polling set to run in orion for interface traffic (AKA every minute, 10 minutes, hour, 6 hours, day ... get the log of interface traffic)
