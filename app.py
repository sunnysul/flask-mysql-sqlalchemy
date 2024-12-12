"""
pip install flask
pip install Flask-Cors
pip install flask_sqlalchemy
pip install mysql-connector-python
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:%40HitechComputer15@localhost/todoappflask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


db = SQLAlchemy(app)


class TodoModel(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    done = db.Column(db.Boolean)


with app.app_context():
    db.create_all()


@app.route('/todos', methods=['GET'])
def get_todos():
    todos = TodoModel.query.all()

    keys = ['id', 'title', 'done']
    values = []
    for todo in todos:
        values.append([todo.id, todo.title, todo.done])

    todos = []
    for value in values:
        todos.append(dict(zip(keys, value)))
    return jsonify(todos)


@app.route('/todos', methods=['POST'])
def create_todo():
    request_data = request.get_json()

    todo = TodoModel(title=request_data['title'], done=False)
    db.session.add(todo)
    db.session.commit()

    return jsonify({'id': todo.id})


@app.route('/todos/<id>', methods=['PUT'])
def update_todo(id):
    todo = TodoModel.query.filter_by(id=id).first()

    request_data = request.get_json()
    todo.title = request_data['title']
    todo.done = request_data['done']

    db.session.commit()
    return jsonify({'id': todo.id})


@app.route('/todos/<id>', methods=['DELETE'])
def delete_todo(id):
    todo = TodoModel.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'id': todo.id})


if __name__ == '__main__':
    app.run(debug=True)



#.gitignore