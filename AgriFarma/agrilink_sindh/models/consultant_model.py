from db import get_db


def list_consultants(limit=100):
	db = get_db()
	cur = db.execute('SELECT * FROM consultant ORDER BY id DESC LIMIT ?', (limit,))
	return cur.fetchall()


def get_consultant(cid):
	db = get_db()
	cur = db.execute('SELECT * FROM consultant WHERE id = ?', (cid,))
	return cur.fetchone()


def create_consultant(name: str, expertise: str = '', contact: str = ''):
	db = get_db()
	cur = db.execute('INSERT INTO consultant (name, expertise, contact) VALUES (?,?,?)', (name, expertise, contact))
	db.commit()
	return cur.lastrowid
