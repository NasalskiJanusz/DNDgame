from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, add_user, get_user
import sqlite3
app = Flask(__name__)
app.secret_key = 'cipa'  # Ustaw swój klucz sekretu

# Inicjalizacja bazy danych
init_db()

# Konfiguracja Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Upewnij się, że ta linia jest dodana

class User(UserMixin):
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    user_data = get_user(user_id)
    if user_data:
        return User(user_data[0], user_data[1], user_data[2], user_data[3])
    return None
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = get_user(username)

        print(f"Próba logowania użytkownika: {username}")
        if user_data:
            print(f"Znaleziono użytkownika: {user_data}")
            if check_password_hash(user_data[2], password):
                user = User(user_data[0], user_data[1], user_data[2], user_data[3])
                login_user(user)
                print(f"Użytkownik {username} zalogowany pomyślnie. Przekierowywanie do dashboardu.")
                return render_template('index.html')
            else:
                print("Hasło nie zgadza się")
        else:
            print("Użytkownik nie znaleziony")

        flash('Nieprawidłowa nazwa użytkownika lub hasło')
    return render_template('login.html')
print("settings")
# Upewnij się, że ta linia jest dodana
login_manager.login_view = 'login'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        try:
            add_user(username, password, role)
            flash('Registration successful! You can now log in.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists. Please choose another one.')
    return render_template('register.html')

def create_default_user():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO users (username, password, role) VALUES (?, ?, ?)
        ''', ('admin', generate_password_hash('admin'), 'gracz'))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Admin user already exists")
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    create_default_user()  # Create the default admin user
    app.run(debug=True)
