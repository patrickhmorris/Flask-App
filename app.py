from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Use a list of dictionaries to manage tasks with unique IDs
tasks = []
next_id = 1


@app.route('/')
def home():
    return redirect(url_for('show_tasks'))


@app.route('/tasks', methods=['GET', 'POST'])
def show_tasks():
    global next_id
    if request.method == 'POST':
        task_content = request.form['content']
        if task_content:
            tasks.append({'id': next_id, 'content': task_content, 'is_important': False})
            next_id += 1
        return redirect(url_for('show_tasks'))
    else:
        # Sort tasks to bring important tasks to the top
        sorted_tasks = sorted(tasks, key=lambda x: x['is_important'], reverse=True)
        return render_template('tasks.html', tasks=sorted_tasks)


@app.route('/mark_important/<int:task_id>')
def mark_important(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['is_important'] = not task['is_important']
            break
    return redirect(url_for('show_tasks'))


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return redirect(url_for('show_tasks'))


@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if request.method == 'POST':
        task['content'] = request.form['content']
        return redirect(url_for('show_tasks'))
    return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
