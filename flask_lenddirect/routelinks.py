from flask_lenddirect.models import User, Todos
from flask import Flask, render_template,url_for,request,redirect,flash
from flask_lenddirect.forms import UserRegisterForm,UserLoginForm,UserUpdateForm,TaskForm,UpdateTaskForm
from flask_lenddirect import app, database, crypt
from flask_login import login_user, current_user, logout_user, login_required

# STATICFILES_FINDERS = [
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# ]

# STATICFILES_DIRS = [
#     path.join(TOP_DIR, 'static'),
# ]

# STATIC_ROOT = path.join(TOP_DIR, 'staticfiles')
# STATIC_URL = '/static/'

@app.route('/home')
@login_required
def home():
	page = request.args.get('page', 1, type=int)
	todos= Todos.query.filter_by(owner=current_user).paginate(page=page,per_page=5)
	return render_template('home.html',todos=todos)

@app.route('/about')
def about():
	return 'About Page'

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = UserRegisterForm()
	if form.validate_on_submit():
		 password_hash = crypt.generate_password_hash(form.password.data).decode('utf-8')
		 user = User(userName=form.userName.data, emailId=form.emailId.data, password=password_hash)
		 database.session.add(user)
		 database.session.commit()
		 flash('Successfully Registered. Please Login to continue', 'success')
		 return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = UserLoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(emailId=form.emailId.data).first()
		if user and crypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			return redirect(url_for('home'))
			
		else:
			flash('Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
	form = UserUpdateForm()
	if form.validate_on_submit():
		current_user.userName = form.userName.data
		current_user.emailId  = form.emailId.data
		database.session.commit()
		flash('Account successfully updated!', 'success')
		return redirect(url_for('profile'))
	elif request.method =='GET':
		form.userName.data = current_user.userName
		form.emailId.data  = current_user.emailId
	return render_template('profile.html', title='Profile',form=form)

@app.route('/addTodo', methods=['GET', 'POST'])
@login_required
def addTodo():
	form = TaskForm()
	if form.validate_on_submit():
		todo = Todos(name=form.name.data, description=form.description.data, completed=form.completed.data, priority=form.priority.data, owner=current_user)
		database.session.add(todo)
		database.session.commit()
		flash('Todo Item successfully added!', 'success')
		return redirect(url_for('home'))
	return render_template('create_todos.html', title='CreateTodo', form=form)

@app.route('/sort')
def sort():
	flash('sorted todos by priority', 'success')
	page = request.args.get('page', 1, type=int)
	todos= Todos.query.filter_by(owner=current_user).order_by(Todos.priority.asc()).paginate(page=page,per_page=5)
	return render_template('task_sorted.html', title='Home',todos=todos)

@app.route('/<int:todo_id>')
def getTodo(todo_id):
    todo = Todos.query.get_or_404(todo_id)
    return render_template('todo.html', title='Todo', todo=todo)

@app.route('/<todo_id>/update', methods=['GET', 'POST'])
@login_required
def update(todo_id):
    todo = Todos.query.get_or_404(todo_id)
    if todo.owner != current_user:
        abort(403)
    form = UpdateTaskForm()
    if form.validate_on_submit():
        todo.name = form.name.data
        todo.description = form.description.data
        todo.priority = form.priority.data
        todo.completed = form.completed.data
        database.session.commit()
        flash('Todo updated successfully', 'success')
        return redirect(url_for('getTodo', todo_id=todo.id))
    elif request.method == 'GET':
        form.name.data = todo.name
        form.description.data = todo.description
        form.priority.data = todo.priority
        form.completed.data = todo.completed
    return render_template('update_todos.html', title='Update',
                           form=form)


@app.route("/delete/<int:todo_id>", methods=['GET','POST'])
@login_required
def deleteTodo(todo_id):
    todo = Todos.query.get_or_404(todo_id)
    if todo.owner != current_user:
        abort(403)
    database.session.delete(todo)
    database.session.commit()
    flash('Your Todo Item is deleted!', 'success')
    return redirect(url_for('home'))


@app.route('/user1', methods=['GET', 'POST'])
def loginUser1():
    user = User.query.filter_by(emailId='user1@gmail.com').first()
    if user:
    	login_user(user)
    	return redirect(url_for('home'))
    else:
    	flash('Please check email and password', 'danger')
    	return render_template('login.html', title='Login', form=form)



@app.route('/user2', methods=['GET', 'POST'])
def loginUser2():
    user = User.query.filter_by(emailId='user2@gmail.com').first()
    if user:
    	login_user(user)
    	return redirect(url_for('home'))
    else:
    	flash('Please check email and password', 'danger')
    	return render_template('login.html', title='Login', form=form)