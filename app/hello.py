from flask import Flask,render_template,request
import requests
import urllib3, json
app=Flask(__name__)
@app.route('/',methods=['POST','GET'])
def hello():
    if request.method=='POST':
        ws=request.form['a']
        tpc=request.form['b']
        wd=request.form['c']
        try:
            ws=float(ws)
            tpc=float(tpc)
            wd=float(wd)
        except:
            return render_template('data.html',err_msg='Enter Valid Data')
        url = "https://iam.cloud.ibm.com/identity/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = "apikey=" + 'UcwmxIfzEJr5hlZ7dPgNftCxzG6X2820RNroBHZakzus' + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
        IBM_cloud_IAM_uid = "bx"
        IBM_cloud_IAM_pwd = "bx"
        response = requests.post(url, headers=headers, data=data, auth=(IBM_cloud_IAM_uid, IBM_cloud_IAM_pwd))
        print(response)
        iam_token = response.json()["access_token"]
        header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + iam_token,
                  'ML-Instance-ID': '6ca9583e-3e40-4bb0-8f96-bf033afc56df'}
        payload_scoring = {"input_data": [
            {"fields": ["Wind Speed (m/s)", "Theoretical_Power_Curve (KWh)", "Wind Direction (°)"],
             "values": [[ws,tpc,wd]]}]}
        response_scoring = requests.post(
            'https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/0bad6844-d41e-4864-ba88-dc7daed03b71/predictions?version=2020-09-01',
            json=payload_scoring, headers=header)
        print(response_scoring)
        a = json.loads(response_scoring.text)
        print(a)
        pred = a['predictions'][0]['values'][0][0]
        return render_template('data.html',result=pred)
    else:
        return render_template('data.html')

if __name__ == '__main__':
    app.run(debug=True)
