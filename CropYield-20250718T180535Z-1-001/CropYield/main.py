from flask import Flask, render_template, request, redirect, url_for, session
import numpy as np
import pandas as pd
import os
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import numpy as np
import cv2
from sklearn.ensemble import RandomForestRegressor
UPLOAD_FOLDER = 'static/uploads/'



app = Flask(__name__)


# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = '1a2b3c4d5e'



# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/')
def home():
    # Check if user is loggedin
        
        # User is loggedin show them the home page
    return render_template('index.html')
    # User is not loggedin redirect to login page



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/yield1')
def yield1():
    return render_template('recommendation.html')


@app.route('/result')
def result():
    return render_template('result.html')

@app.route("/predict", methods = ["GET", "POST"])
def predict():
    if request.method == "POST":
        
        # water
        water = float(request.form["water"])
        
        # UV
        UV = float(request.form["UV"])
        
        # area
        area = float(request.form["area"])
        
        # fertilizer
        fertilizer = float(request.form["fertilizer"])
        
        # Pesticide
        Pesticide = float(request.form["Pesticide"])
        
        # Region
        Region = float(request.form["Region"])

        

        sample_data = [water,UV,area,fertilizer,Pesticide,Region]
        clean_data = [float(i) for i in sample_data]
        ex1 = np.array(clean_data).reshape(1,-1)


        data=pd.read_csv(r"dataset.csv")
        data=data.drop(columns=['id','categories'],axis=1)

        # data.water = pd.DataFrame(data.water).replace(np.nan, pd.DataFrame.median(data.water))#Replacing NaN with median
        # data.uv = pd.DataFrame(data.uv).replace(np.nan, pd.DataFrame.median(data.uv))#Replacing NaN with median
        data.water = data.water.fillna(data.water.median())

# Replace NaN values with median in data.uv
        data.uv = data.uv.fillna(data.uv.median())

        data.drop(data[data['water']>200].index,inplace=True)

        X=data.iloc[:,:-1].values
        y=data.iloc[:,-1].values
        
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=3)
        
        regressor = RandomForestRegressor(n_estimators = 10, random_state = 50)
        regressor.fit(X_train, y_train)
        yhat=regressor.predict(ex1)
        res = yhat[0]  

        result= 27.6*res*area
                

            
					
        return render_template('result.html',prediction_text=res, result=result,res=1,area=area)

        
@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

    
if __name__ =='__main__':
	app.run()
