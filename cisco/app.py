# create a simple flask based todo api with add, list and delete endpoints
from flask import Flask, request, jsonify
app = Flask(__name__)
todos = []
current_id = 1
@app.route('/todos', methods=['GET'])
def list_todos():
    return jsonify(todos)
# generate code for adding a todo item
@app.route('/todos', methods=['POST'])
def add_todo():
    global current_id
    data = request.get_json()
    todo_item = {
        'id': current_id,
        'title': data.get('title'),
        'status': data.get('completed', 'pending')
    }
    todos.append(todo_item)
    current_id += 1
    return jsonify({'message': 'Todo added', 'todo': todo_item}), 201

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    for todo in todos:
        if todo['id'] == todo_id:
            todos.remove(todo)
            return jsonify({'message': 'Todo deleted', 'todo': todo}), 200
    return jsonify({'message': 'Todo not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)