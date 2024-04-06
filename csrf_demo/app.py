
from flask import Flask, render_template, request 
from flask_wtf import CSRFProtect 
  
app = Flask(__name__) 
app.secret_key = b'_53oi3uriq9pifpff;apl'
csrf = CSRFProtect(app) 

@app.route("/form", methods=['GET', 'POST']) 
def form(): 
    if request.method == 'POST': 
        name = request.form['Name'] 
        return (' Hello ' + name + '!!!') 
    return render_template('form.html') 

  
if __name__ == '__main__': 
    app.run(debug=True)
