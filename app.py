from flask import Flask,render_template,url_for,request,redirect,session,render_template_string,flash
import mysql.connector
import bcrypt
db_config = {
    'user': 'root',       # replace with your MySQL username
    'password': 'affagk',   # replace with your MySQL password
    'host': 'localhost',
    'database': 'login'}
def add_user(username, password, user_type):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    query = "INSERT INTO users (username, password_hash, user_type) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, password_hash, user_type))
    conn.commit()
    cursor.close()
    conn.close()


# Example users
add_user('basit', 'password123', 'local_user')
add_user('ali', 'password456', 'it_user')
add_user('awais', 'password789', 'administrator')

app = Flask(__name__)
app.secret_key = 'supersecretkey' 
db_config = {
    'user': 'root',       # replace with your MySQL username
    'password': 'fkgfkgfk',   # replace with your MySQL password
    'host': 'localhost',
    'database': 'login'}
templates = {
    "local_user": "<h1>Welcome Local User!</h1>",
    "it_user": "<h1>Welcome IT User!</h1>",
    "administrator": "<h1>Welcome Administrator!</h1>",
    "home": '''
        <form action="/login" method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br>
            <button type="submit">Login</button>
        </form>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <ul>
                {% for category, message in messages %}
                    <li class="{{ category }}">{{ message }}</li>
                {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
    '''
}

@app.route('/')
def home():
    return render_template_string(templates["home"])

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    
    query = "SELECT password_hash, user_type FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    

    if result:
        stored_password_hash, user_type = result
        if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
            if user_type == 'local_user':
                return redirect(url_for('local_user'))
            elif user_type == 'it_user':
                return redirect(url_for('it_user'))
            elif user_type == 'administrator':
                return redirect(url_for('administrator'))
            else:
                return "Invalid user type"
        else:
            flash('Incorrect password', 'error')
            return redirect(url_for('home'))
    else:
        flash('User not found', 'error')
        return redirect(url_for('home'))
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/local_user')
def local_user():
    return render_template_string(templates["local_user"])

@app.route('/it_user')
def it_user():
    return render_template_string(templates["it_user"])

@app.route('/administrator')
def administrator():
    return render_template_string(templates["administrator"])

if __name__ == '__main__':
    app.run(debug=True)
