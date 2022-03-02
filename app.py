
from flask import Flask,render_template,url_for,request,redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_restful import Resource, Api


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
api = Api(app)
db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(200), nullable=False)
    completed=db.Column(db.Integer, default=0)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return '<Task %r>' % self.id

@app.route('/',methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        task_content=request.form['content']
        new_task=Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There is an issue"
    else:
        try:
            tasks=Todo.query.order_by(Todo.date_created).all()
        except:
            tasks=None
        return render_template('index.html',tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There is an issue"
    
@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    task_to_update=Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_to_update.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There is an issue"
    else:
        return render_template('update.html',task=task_to_update)
        
class Hello(Resource):
  
    # corresponds to the GET request.
    # this function is called whenever there
    # is a GET request for this resource
    def get(self):
  
        return jsonify({'message': 'hello world'})
  
    # Corresponds to POST request
    def post(self):
          
        data = request.get_json()     # status code
        return jsonify({'data': data}), 201
  
  
# another resource to calculate the square of a number
class Square(Resource):
  
    def get(self, num):

        return jsonify({'square': num**2})
  
api.add_resource(Hello, '/')
api.add_resource(Square, '/square/<int:num>')
  

if __name__ == '__main__':
    app.run(debug=True)