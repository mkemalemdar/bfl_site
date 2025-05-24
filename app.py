import json
import os
from flask import Flask, render_template, request, redirect, url_for

APP = Flask(__name__)
DATA_FILE = 'posts.json'

def load_posts():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_posts(posts):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

@APP.route('/')
def index():
    posts = load_posts()
    # ensure comments key exists for all posts
    for p in posts:
        p.setdefault('comments', [])
    return render_template('index.html', posts=posts)

@APP.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title'].strip()
        content = request.form['content'].strip()
        if title and content:
            posts = load_posts()
            new_id = (posts[-1]['id'] + 1) if posts else 1
            posts.append({'id': new_id, 'title': title, 'content': content, 'comments': []})
            save_posts(posts)
            return redirect(url_for('show_post', post_id=new_id))
    return render_template('create.html')

@APP.route('/post/<int:post_id>', methods=('GET', 'POST'))
def show_post(post_id):
    posts = load_posts()
    post = next((p for p in posts if p['id'] == post_id), None)
    if not post:
        return "Post not found", 404
    post.setdefault('comments', [])
    if request.method == 'POST':
        author = request.form.get('author', 'Anonymous').strip() or 'Anonymous'
        text = request.form['text'].strip()
        if text:
            post['comments'].append({'author': author, 'text': text})
            save_posts(posts)
        return redirect(url_for('show_post', post_id=post_id))
    return render_template('post.html', post=post)

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
