from flask import Flask, redirect, url_for, request, render_template
import requests
import json

app = Flask(__name__, template_folder= 'templates')
context_set = ""
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return 'Error page. Use http://0.0.0.0:5000/chat in GET body with keys "message". Author: Vũ Quang Cường '

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'GET':
        val = str(request.args.get('text'))
        data = json.dumps({"sender": "Rasa","message": val})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post('http://localhost:5005/webhooks/rest/webhook', data= data, headers = headers)
        res = res.json()
        val = res[0]['text']
        val = val.replace("\n",'<br>')
        type = str(request.args.get('t'))
        if type == '1':
            return val
        else :
            return render_template('index.html', val=val)
        
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    dataBody=request.json
    for data in dataBody:
        try:
            val= data["message"]
            data = json.dumps({"sender": "Rasa","message": val})
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            res = requests.post('http://0.0.0.0:5005/webhooks/rest/webhook', data= data, headers = headers)
            res = res.json()
            val = res[0]['text']
            return val
        except Exception:
            print("An exception occurred")
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)