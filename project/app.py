from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

tasks = []  # In a real app, use a database!

@app.route('/api/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if request.method == 'POST':
        data = request.get_json()
        task_name = data.get('name')
        due_date_str = data.get('dueDate') # Get due date from request
        subject = data.get('subject')

        try:
            due_date = datetime.datetime.strptime(due_date_str, "%Y-%m-%d").date()
            new_task = {"name": task_name, "dueDate": str(due_date), "subject": subject, "completed": False} # Store date as string
            tasks.append(new_task)
            return jsonify({"message": "Task added"})
        except (ValueError, TypeError): # Handle errors
            return jsonify({"error": "Invalid data"}), 400  # Return error with code 400

    elif request.method == 'GET':
        return jsonify(tasks)  # Send tasks to frontend

@app.route('/api/tasks/<int:task_id>', methods=['PUT']) # Update task
def update_task(task_id):
    if 0 <= task_id < len(tasks):
        data = request.get_json()
        tasks[task_id]['completed'] = data.get('completed', False) # Update completed status
        return jsonify({"message": "Task updated"})
    else:
        return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
