# CSCI6710
CSCI6710 Homework 4

## Team Members:
Kristen Griffith, Katie Warren, Abigail Holloway

## Prerequisites
- It is required that you run this on a Linux machine. This is because it uses [Tensorflow Decision Forests](https://www.tensorflow.org/decision_forests), which is currently only supported on Linux.
- It is recommended to have Python 3.10 (I have not tried this on earlier versions of Python) - install with `sudo apt install python3.10`.
- It is required to have `pip` installed - install with `sudo apt install pip`.

## Notes
I was not able to get Tensorflow JS working as it did not appear to support tree-based methods, so I went ahead and set up a flask server to serve predictions from a model trained on the backend. I generated 1000 samples of training data based on a threshold-based method (see vampire_data.csv).

## Instructions
1. Clone the Repository: `git clone https://github.com/LiffAM1/CSCI6710.git`
2. Open a terminal in the install folder or `cd` there
2. Install the requirements.txt to get the python package requirements: `pip install -r requirements.txt`
3. Run the flask app in the base directory: `flask run`
4. Wait until the model trains (NOTE: The model trains whenever the app is run due to issues with loading Tensorflow SavedModels that I was running in to). You will see this when the model site is ready:
![image](https://user-images.githubusercontent.com/22064340/224601366-c0669ab6-a52f-4bf1-8ce1-e97fba27e146.png)
5. Navigate to http://localhost:5000/static/index.html in your browser
6. You should be able to use the form and select different processing methods.

## Notes
I was not able to get Tensorflow JS working with a tree-based method since it seems like it is mainly for use with neural networks and is not compatible with Tensorflow Decision Forests or other Tensorflow Saved Models. I made the decision to do the training and predicting against the model from the backend using regular Tensorflow. I generated the data (vampire_data.csv) using a threshold-based method in Google Sheets and trained the model using a random sample of 2/3 of the data each time.

**If you have issues getting the Flask server or dependencies running, please grade the assignment as-is without the extra credit (just open and run index.html in the browser and do not select Decision Forest as the logic processing method).**
