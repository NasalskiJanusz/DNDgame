from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import *
import sqlite3

app = Flask(__name__)
app.secret_key = 'cipka'  # Ustaw klucz tajny dla sesji
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Zwiększa bezpieczeństwo ciasteczek
app.config['SESSION_COOKIE_SECURE'] = False  # Zmień na True, jeśli używasz HTTPS


# Inicjalizacja bazy danych użytkowników
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

    def get_id(self):
        return str(self.id)  # Musi zwrócić identyfikator jako string

@login_manager.user_loader
def load_user(user_id):
    user_data = get_user(user_id)  # Fetch user by ID
    if user_data:
        return User(user_data[0], user_data[1], user_data[2], user_data[3])
    return None


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = get_user(username)  # Pobierz dane użytkownika z bazy

        if user_data and check_password_hash(user_data[2], password):  # Sprawdź, czy hasło się zgadza
            user = User(user_data[0], user_data[1], user_data[2], user_data[3])  # Utwórz obiekt User
            login_user(user)  # Zaloguj użytkownika
                
            next_page = request.args.get('next')  # Pobierz stronę, na którą użytkownik chciał przejść
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Nieprawidłowa nazwa użytkownika lub hasło')
    
    return render_template('login.html')


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
        ''', ('admin', generate_password_hash('admin'), 'game_master'))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Admin user already exists")
    finally:
        conn.close()


# dodaj spella
@app.route('/add_spell', methods=['GET', 'POST'])
@login_required
def handle_add_spell():
    print(f"Current user: {current_user.username}, role: {current_user.role}")
    if request.method == 'POST':
        # Pobieranie danych z formularza
        name = request.form['name']
        level = request.form['level']
        damage_formula = request.form['damage_formula']
        mana_cost = request.form['mana_cost']
        action_points = request.form['action_points']
        spell_range = request.form['range']
        element = request.form['element']
        description = request.form['description']

        # Dodaj zaklęcie do bazy danych
        add_spell(name, level, damage_formula, mana_cost, action_points, spell_range, element, description)
        flash('Zaklęcie zostało pomyślnie dodane!')
        return redirect(url_for('handle_add_spell'))

    spells = get_all_spells()
    return render_template('add_spell.html', spells=spells)




@app.route('/delete_spell/<int:spell_id>', methods=['POST'])
def delete_spell(spell_id):
    delete_spell_by_id(spell_id)
    flash('Zaklęcie zostało pomyślnie usunięte!')
    return redirect(url_for('handle_add_spell'))

def get_all_spells():
    conn = sqlite3.connect('spells.db')
    conn.row_factory = sqlite3.Row  # Ustawienie, aby wyniki były zwracane jako słowniki
    c = conn.cursor()
    c.execute('SELECT * FROM spells')
    spells = c.fetchall()
    conn.close()
    return spells


def delete_spell_by_id(spell_id):
    conn = sqlite3.connect('spells.db')
    c = conn.cursor()
    c.execute('DELETE FROM spells WHERE id = ?', (spell_id,))
    conn.commit()
    conn.close()

@app.route('/delete_item/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    conn = sqlite3.connect('items.db')
    c = conn.cursor()
    c.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    flash('Przedmiot został pomyślnie usunięty!')
    return redirect(url_for('new_item'))




@app.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    if request.method == 'POST':
        item_type = request.form['type']
        str_value = request.form['str']
        dex_value = request.form['dex']
        stm_value = request.form['stm']
        intelligence_value = request.form['intelligence']
        charisma_value = request.form['charisma']
        hp_value = request.form.get('hp', 0)  # Użyj wartości domyślnej 0, jeśli nie podano
        mp_value = request.form.get('mp', 0)  # Użyj wartości domyślnej 0, jeśli nie podano
        ac_value = request.form.get('ac', 0)  # Użyj wartości domyślnej 0, jeśli nie podano
        mr_value = request.form.get('mr', 0)  # Użyj wartości domyślnej 0, jeśli nie podano
        spd_value = request.form.get('spd', 0)  # Użyj wartości domyślnej 0, jeśli nie podano
        luck_value = request.form.get('luck',0)
        rarity_value = request.form.get('rar')
        desc_value = request.form.get('desc')

        # Dodawanie przedmiotu do bazy danych items.db
        conn = sqlite3.connect('items.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO items (type, str, dex,stm, int, cha, hp, mp, ac, mr, spd,luck,rar,desc)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)
        ''', (item_type, str_value, dex_value, stm_value, intelligence_value,
              charisma_value, hp_value, mp_value, ac_value, mr_value, spd_value,luck_value,rarity_value,desc_value))
        conn.commit()
        conn.close()

        flash('Przedmiot został pomyślnie dodany!')
        return redirect(url_for('new_item'))

    items = get_all_items()  # Pobierz wszystkie przedmioty
    return render_template('new_item.html', items=items)


# Endpoint do formularza tworzenia nowego bohatera
@app.route('/new_hero', methods=['GET', 'POST'])
def new_hero():
    if request.method == 'POST':
        # Pobranie danych z formularza
        name = request.form['name']
        hero_class = request.form['class']
        race = request.form['race']
        strength = int(request.form['strength'])
        dexterity = int(request.form['dexterity'])
        stm = int(request.form['stm'])
        intelligence = int(request.form['intelligence'])
        charisma = int(request.form['charisma'])
        magic_resistance = int(request.form['magic_resistance'])
        hp = int(request.form['hp'])
        mp = int(request.form['mp'])
        armor = int(request.form['armor'])
        speed = int(request.form['speed'])
        luck = int(request.form['luck'])
        # Dodanie bohatera do bazy danych
        try:
            # Tworzenie bazy danych dla bohatera (jego staty, ekwipunek, plecak oraz spelle które umie)
            create_hero_equipment_spells_databases(name)
            
            # Zaklęcia i przedmioty (można zaznaczyć kilka, dlatego użyjemy request.form.getlist)
            selected_spells = request.form.getlist('spells')
            selected_items = request.form.getlist('items')
            
            # ID aktualnie zalogowanego użytkownika
            user_id = current_user.id
            
            # Dodanie nowego bohatera
            add_hero(name, hero_class, race, strength, dexterity, stm, intelligence, charisma, magic_resistance, hp, mp, armor, speed, luck, selected_items, selected_spells, user_id)
            
            return redirect(url_for('new_hero'))
        except Exception as e:
            print(f'Wystąpił błąd podczas dodawania bohatera: {e}')

            return redirect(url_for('new_hero'))

    spells = get_all_spells()  # Pobierz zaklęcia
    items = get_all_items()  # Pobierz przedmioty

    return render_template('new_hero.html', spells=spells, items=items)



@app.route('/index')
@login_required  # Upewnij się, że tylko zalogowani użytkownicy mają dostęp
def index():
    print(f"Zalogowany użytkownik: {current_user.username}, rola: {current_user.role}")  # Debugowanie
    # Sprawdź rolę użytkownika i renderuj odpowiedni szablon
    if current_user.role == 'gracz':
        return render_template('index_player.html')
    elif current_user.role == 'game_master':
        return render_template('index.html')
    else:
        # W razie nieznanej roli możesz przekierować do strony błędu lub powiadomić o braku uprawnień
        flash('Nieznana rola użytkownika!')
        return redirect(url_for('login'))
    
@app.route('/game')

def game():
    print(f"Zalogowany użytkownik: {current_user.username}, rola: {current_user.role}")  # Debugowanie
    
    # Sprawdź rolę użytkownika i renderuj odpowiedni szablon
    if current_user.role == 'gracz':
        return render_template('game_player.html')
    elif current_user.role == 'game_master':
        return render_template('game_master.html')
    else:
        # W razie nieznanej roli możesz przekierować do strony błędu lub powiadomić o braku uprawnień
        flash('Nieznana rola użytkownika!')
        return redirect(url_for('login'))
    


if __name__ == '__main__':
    init_db()  # Inicjalizacja bazy danych użytkowników
    init_spells_db()  # Inicjalizacja bazy danych zaklęć
    init_heroes_db()  # Inicjalizacja bazy danych bohaterów
    create_default_user()  # Tworzenie domyślnego użytkownika
    init_items_db()
    app.run(debug=True)