from flask import Flask,render_template,request
import numpy as np
import joblib
app = Flask(__name__)

def init():
    # load the saved model.
    global regressor
    regressor = joblib.load("insurence.pkl")

@app.route('/')
def welcome():
    return render_template('index.html')

# predict?age=31&sex=1&bmi=25.74&children=0&smoker=0&region=0
@app.route('/predict', methods=['GET'])
def predict():
    try:
        age = float(request.args.get('age'))
        sex = float(request.args.get('sex'))
        bmi = float(request.args.get('bmi'))
        children = float(request.args.get('children'))
        smoker = float(request.args.get('smoker'))
        region = float(request.args.get('region'))
        # Same order as the x_train dataframe
        features = [np.array([age, sex, bmi, children, smoker, region])]
        prediction = regressor.predict(features)
        return 'apparent_price' + str(prediction)
    except Exception as e:
        print(e)
        return 'Calculation Error'+ str(e), 500

@app.route('/submit',methods=['POST','GET'])
def submit():
    total_score=0
    try:
        if request.method == 'POST':
            age = int(request.form['age'])
            sex = request.form['sex']
            if sex == "female":
                sex = "1"
            elif sex == "male":
                sex = "0"
            else:
                return 'Input Error in Sex!' + sex
            bmi = float(request.form['bmi'])
            children = int(request.form['children'])
            smoker = request.form['smoker']
            if smoker == "no":
                smoker = "1"
            elif smoker == "yes":
                smoker = "0"
            else:
                return 'Input Error!'
            region = request.form['region']
            if region == "southeast":
                region = "0"
            elif region == "southwest":
                region = "1"
            elif region == "northeast":
                region = "2"
            elif region == "northwest":
                region = "3"
            else:
                return 'Input Error!'
            # Predict Apparent temperature
            # Same order as the x_train dataframe
            features = [np.array([age, sex,bmi,children,smoker,region])]
            prediction = regressor.predict(features)
            finalprice = np.round(prediction, 2)
            formatted_float = "$ {:,.2f}".format(finalprice[0])
            return render_template('index.html',price = str(formatted_float))
    except Exception as e:
        print(e)
        return 'Calculation Error'+str(e), 500
        
if __name__=='__main__':
    init()
    app.run(debug=True)
