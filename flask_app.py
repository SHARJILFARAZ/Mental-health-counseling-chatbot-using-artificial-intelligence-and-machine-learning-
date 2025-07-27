from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database connection
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

def get_comments_html(post_id):
    cursor.execute("SELECT username, comment, timestamp FROM comments WHERE post_id = ? ORDER BY timestamp DESC", (post_id,))
    comments = cursor.fetchall()
    comments_html = ""
    for comment_username, comment, comment_timestamp in comments:
        comments_html += f"""
        <div class="comment">
            <div class="comment-header">
                <div class="username">{comment_username}</div>
                <div class="timestamp">{comment_timestamp}</div>
            </div>
            <div class="comment-content">{comment}</div>
        </div>
        """
    return comments_html

@app.route('/like_post', methods=['POST'])
def like_post():
    post_id = request.json.get('post_id')
    cursor.execute("UPDATE forum_posts SET likes = likes + 1 WHERE id = ?", (post_id,))
    conn.commit()
    cursor.execute("SELECT likes FROM forum_posts WHERE id = ?", (post_id,))
    likes = cursor.fetchone()[0]
    return jsonify({"success": True, "likes": likes})

@app.route('/add_comment', methods=['POST'])
def add_comment():
    post_id = request.json.get('post_id')
    comment = request.json.get('comment')
    username = request.json.get('username')
    cursor.execute("INSERT INTO comments (post_id, username, comment) VALUES (?, ?, ?)", (post_id, username, comment))
    conn.commit()
    comments_html = get_comments_html(post_id)
    return jsonify({"success": True, "comments_html": comments_html})

if __name__ == '__main__':
    app.run(port=5000)
