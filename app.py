from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect

app = Flask(__name__)

#Database path-set and initialization
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

#Database Schema
class Todo(db.Model):
   id= db.Column(db.Integer, primary_key=True)
   content= db.Column(db.String(200), nullable=False)
   date_created=db.Column(db.DateTime, default=datetime.utcnow)

   def __repr__(self):
      return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
   #Check for the type of request
   if request.method == 'POST':
      #Logic to add the task
      task_content= request.form['content']   #task_content=variable
      new_task=Todo(content=task_content)     #Added input to todo model

      #Push data to database
      try:
         db.session.add(new_task)
         db.session.commit()
         return redirect('/')
      except:
         return 'Eoor: Issue adding the string'

   else:
      #Reading DB 
      tasks = Todo.query.order_by(Todo.date_created).all()
      return render_template("index.html",tasks=tasks)

#Route for delete by id
@app.route('/delete/<int:id>')
def delete(id):
   #lookup for record w.r.t id
   task_to_delete =Todo.query.get_or_404(id)

   try:
      db.session.delete(task_to_delete)
      db.session.commit()
      return redirect('/')
   except:
      return 'There was a problem deleting'

#Rout for Symbols
@app.route('/symbol')
def symbols():
   a=('AFN','ARS','AWG','AUD','AZN','BSD','BBD','BYN','BZD','BMD','BOB','BAM','BWP','BGN','BRL','BND','KHR','CAD','KYD','CLP','CNY','COP','CRC','HRK','CUP','CZK','DKK','DOP','XCD','EGP','SVC','EUR','FKP','FJD','GHS','GIP','GTQ','GGP','GYD','HNL','HKD','HUF','ISK','INR','IDR','IRR','IMP','ILS','JMD','JPY','JEP','KZT','KPW','KRW','KGS','LAK','LBP','LRD','MKD','MYR','MUR','MXN','MNT','MZN','NAD','NPR','ANG','NZD','NIO','NGN','NOK','OMR','PKR','PAB','PYG','PEN','PHP','PLN','QAR','RON','RUB','SHP','SAR','RSD','SCR','SGD','SBD','SOS','ZAR','LKR','SEK','CHF','SRD','SYP','TWD','THB','TTD','TRY','TVD','UAH','GBP','USD','UYU','UZS','VEF','VND','YER','ZWD','Lek','؋','$','ƒ','₼','Br','BZ$','$b','KM','P','лв','R$','៛','¥','₡','kn','₱','Kč','kr','RD$','£','€','¢','Q','L','Ft','','Rp','﷼','₪','J$','₩','₭','ден','RM','₨','₮','MT','C$','₦','B/.','Gs','S/.','zł','lei','₽','Дин.','S','R','CHF','NT$','฿','TT$','₴','$U','Bs','₫','Z$')
   return '{}'.format(a)

#Route for update by id
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
   task =Todo.query.get_or_404(id)
   if request.method=='POST':
      task.content= request.form['content']

      try:
         db.session.commit()
         return redirect('/')
      except:
         return 'Error Updating'
   else:
      return render_template("update.html",task=task)

@app.route('/post',methods=['POST'])
def posting():
   input_json =request.get_json(force=True)
   dictToReturn={'stext':input_json['text']}
   return jsonify(dictToReturn)


if __name__ == "__main__":
   app.run(debug=True)