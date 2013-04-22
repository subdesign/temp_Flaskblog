from flask import *
import sqlite3
from forms import ArticleForm
from datetime import datetime

USERNAME = 'admin'
PASSWORD = 'password'
DATABASE = 'database.db'

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = '86i94Pox4MyHJy0s3wC4E51KR6H1C7hv'

# DATABASE 

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

# FRONTEND METHODS

@app.route('/')
def blog():
	g.db = connect_db()
	cur = g.db.execute('SELECT * FROM fblog WHERE status=1 ORDER BY date DESC')
	posts = [dict(title=row[1], content=row[2], date=row[3]) for row in cur.fetchall()]
	g.db.close()
	return render_template('blog.html', posts=posts)


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])	
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
			error = 'Invalid username or password'
		else:
			session['logged_in'] = True
			return redirect(url_for('admin'))

	return render_template('login.html', error=error)


@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	return redirect( url_for('login'))

# ADMIN METHODS

@app.route('/admin')
def admin():
	if not session.get('logged_in'):
		abort(404)
	else:
		g.db = connect_db()
		cur = g.db.execute('SELECT blog_id, title, date, status FROM fblog ORDER BY blog_id ASC')
		posts = [dict(blog_id=row[0], title=row[1], date=row[2], status=row[3]) for row in cur.fetchall()]
		g.db.close()
		return render_template('admin.html', posts=posts)


@app.route('/status/<int:blog_id>',)
def status(blog_id):
	if not session.get('logged_in'):
		abort(404)
	else:
		g.db = connect_db()		

		cur = g.db.execute('SELECT status FROM fblog WHERE blog_id=' + str(blog_id) )		

		status = cur.fetchone()[0]

		if status == 1:				
			cur = g.db.execute('UPDATE fblog SET status = 0 WHERE blog_id=' + str(blog_id))
		elif status == 0:			
			cur = g.db.execute('UPDATE fblog SET status = 1 WHERE blog_id=' + str(blog_id))
		
		g.db.commit()
		g.db.close()		
		flash('Status set successfully')
		return redirect( url_for('admin'))


@app.route('/add', methods=['GET', 'POST'])		
def add():
	if not session.get('logged_in'):
		abort(404)
	else:
		form = ArticleForm()		
		if request.method == 'POST':
			if form.validate() == False:				
				return render_template('add.html', form=form)
			else:
				d = datetime.now().strftime('%d-%m-%Y')
				g.db = connect_db()
				cur = g.db.execute('INSERT INTO fblog (title, content, date, status) VALUES (?, ?, ?, 1)', [form.title.data, form.content.data, d])
				g.db.commit()
				g.db.close()
				return redirect( url_for('admin') )

		elif request.method == 'GET':
			return render_template('add.html', form=form)


@app.route('/update/<int:blog_id>', methods=['GET', 'POST'])
def update(blog_id):
	if not session.get('logged_in'):
		abort(404)
	else:
		form = ArticleForm()		
		if request.method == 'POST':
			if form.validate() == False:				
				return render_template('add.html', form=form)
			else:
				
				g.db = connect_db()
				cur = g.db.execute('UPDATE fblog SET title =' + form.title.data + ', content =' + form.content.data + ' WHERE blog_id=' + str(blog_id))
				g.db.commit()
				g.db.close()
				flash('Article updated successfully')
				return redirect( url_for('admin') )

		elif request.method == 'GET':			
			g.db = connect_db()
			article = query_db('SELECT blog_id, title, content FROM fblog WHERE blog_id = ?', [blog_id], one=True)
			form.title.data = article['title']
			form.content.data = article['content']			
			return render_template('edit.html', form=form, article=article)


@app.route('/delete/<int:blog_id>', methods=['GET'])
def delete(blog_id):
	if not session.get('logged_in'):
		abort(404)
	else:
		g.db = connect_db()
		cur = g.db.execute('DELETE FROM fblog WHERE blog_id=' + str(blog_id))
		g.db.commit()
		g.db.close()
		flash('Article deleted successfully')
		return redirect( url_for('admin'))

# RUN APP

if __name__ == '__main__':
	app.run(debug=True)