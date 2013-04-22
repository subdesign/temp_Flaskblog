import sqlite3

con = sqlite3.connect('database.db')

with con:
	cur = con.cursor()
	cur.execute("DROP TABLE IF EXISTS fblog")
	cur.execute("CREATE TABLE fblog (blog_id INTEGER PRIMARY KEY AUTOINCREMENT, title STRING NOT NULL, content TEXT NOT NULL, date STRING NOT NULL, status INTEGER NOT NULL)")
	cur.execute('INSERT INTO fblog (title, content, date, status) VALUES("First post", "Lorem ipsum", "10-04-2013",1) ')
	cur.execute('INSERT INTO fblog (title, content, date, status) VALUES("Second post", "Lorem ipsum", "12-04-2013",1) ')
	cur.execute('INSERT INTO fblog (title, content, date, status) VALUES("Third post", "Lorem ipsum", "15-04-2013",1) ')

con.close()