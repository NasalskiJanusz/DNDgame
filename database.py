import os
import sqlite3

# Funkcja do tworzenia bazy danych users
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Funkcja do tworzenia bazy danych spells (jeśli nie istnieje)
def init_spells_db():
    # Sprawdzamy, czy plik bazy danych istnieje
    if not os.path.exists('spells.db'):
        print("Tworzenie bazy danych zaklęć...")
        conn = sqlite3.connect('spells.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS spells (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                level INTEGER NOT NULL,
                damage_formula TEXT NOT NULL,
                mana_cost INTEGER NOT NULL,
                action_points INTEGER NOT NULL,
                range INTEGER NOT NULL,
                element TEXT NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()
        conn.close()
    else:
        print("Baza danych zaklęć już istnieje.")

# Funkcja do dodawania zaklęć do bazy spells
def add_spell(name, level, damage_formula, mana_cost, action_points, spell_range, element, description):
    conn = sqlite3.connect('spells.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO spells (name, level, damage_formula, mana_cost, action_points, range, element, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, level, damage_formula, mana_cost, action_points, spell_range, element, description))
    conn.commit()
    conn.close()


# Funkcja do dodawania nowego użytkownika do bazy users
def add_user(username, password, role):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO users (username, password, role) VALUES (?, ?, ?)
    ''', (username, password, role))
    conn.commit()
    conn.close()

def get_user(identifier):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    # Check if the identifier is numeric (likely a user_id), otherwise treat it as a username
    if identifier.isdigit():
        c.execute('SELECT * FROM users WHERE id = ?', (identifier,))
    else:
        c.execute('SELECT * FROM users WHERE username = ?', (identifier,))

    user = c.fetchone()
    conn.close()
    return user



def init_items_db():
    conn = sqlite3.connect('items.db')
    cursor = conn.cursor()
    
    # Tworzenie tabeli items, jeśli nie istnieje
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        str INTEGER NOT NULL,
        dex INTEGER NOT NULL,
        stm INTEGER NOT NULL,
        int INTEGER NOT NULL,
        cha INTEGER NOT NULL,
        hp INTEGER NOT NULL,
        mp INTEGER NOT NULL,
        ac INTEGER NOT NULL,
        mr INTEGER NOT NULL,
        spd INTEGER NOT NULL,
        luck INTEGER NOT NULL,
        rarity TEXT,
        desc TEXT,
        where_item TEXT
    )''')

    conn.commit()
    conn.close()







# Funkcja do inicjalizacji bazy danych bohaterów
def init_heroes_db():
    if not os.path.exists('heroes.db'):
        print("Tworzenie bazy danych bohaterów...")
        conn = sqlite3.connect('heroes.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS heroes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                class TEXT NOT NULL,
                race TEXT,
                strength INTEGER,
                dexterity INTEGER,
                stm INTEGER,
                intelligence INTEGER,
                charisma INTEGER,
                magic_resistance INTEGER,
                hp INTEGER,
                mp INTEGER,
                armor INTEGER,
                speed INTEGER,
                luck INTEGER
            )
        ''')
        conn.commit()
        conn.close()
    else:
        print("Baza danych bohaterów już istnieje.")


# Funkcja do dodawania bohatera do bazy danych
def add_hero(name, hero_class, race, strength, dexterity, stm, intelligence, charisma, magic_resistance, hp, mp, armor, speed, luck, items, spells):
    conn = sqlite3.connect('heroes.db')
    c = conn.cursor()

    # Dodanie bohatera do heroes.db (wszyscy bohaterowie)
    c.execute(''' 
        INSERT INTO heroes (name, class, race, strength, dexterity, stm, intelligence, charisma, magic_resistance, hp, mp, armor, speed, luck)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, hero_class, race, strength, dexterity, stm, intelligence, charisma, magic_resistance, hp, mp, armor, speed, luck))
    conn.commit()
    conn.close()
    
    # -----------------Druga część funkcji-------------------------
    
    conn = sqlite3.connect(f"{name}_baza.db")
    c = conn.cursor()
    
    # Wpisz staty do jego osobistej bazy danych
    c.execute(''' 
        INSERT INTO staty_herosa (name, class, race, strength, dexterity, stm, intelligence, charisma, magic_resistance, hp, mp, armor, speed, luck)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, hero_class, race, strength, dexterity, stm, intelligence, charisma, magic_resistance, hp, mp, armor, speed, luck))
    
    # Insert spelli i itemów do bazy danych bohatera (plecak i spelle)
    for item_id in items:
        c.execute("INSERT INTO plecak (item_id) VALUES (?)",(item_id)) 
    for spell_id in spells:
        c.execute("INSERT INTO spells (spell_id) VALUES (?)",(spell_id))   
    
  
    conn.commit()
    conn.close()



    
# Funkcja tworząca osobne bazy danych na przedmioty i zaklęcia
def create_hero_equipment_spells_databases(hero_name):
    # Tworzenie bazy danych dla bohatera
    conn = sqlite3.connect(f"{hero_name}_baza.db")
    c = conn.cursor()
    
    # Staty do modyfikacji w obliczeniach
    c.execute('''
            CREATE TABLE IF NOT EXISTS staty_herosa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                class TEXT NOT NULL,
                race TEXT,
                strength INTEGER,
                dexterity INTEGER,
                stm INTEGER,
                intelligence INTEGER,
                charisma INTEGER,
                magic_resistance INTEGER,
                hp INTEGER,
                mp INTEGER,
                armor INTEGER,
                speed INTEGER,
                luck INTEGER
            )
        ''')
    
    # Eq postaci czyli to co nosi na sobie
    c.execute('''
              CREATE TABLE IF NOT EXISTS ekwipunek(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  item_id INTEGER,
                  where_item TEXT
              )
              ''')
    
    # Spelle które już umie
    c.execute('''
              CREATE TABLE IF NOT EXISTS spells(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  spell_id INTEGER
              )
              ''')
    
    # Plecak
    c.execute('''
              CREATE TABLE IF NOT EXISTS plecak(
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  item_id INTEGER
              )
              ''')
    conn.commit()
    conn.close()

# Funkcja do pobierania wszystkich przedmiotów z bazy danych items.db
def get_all_items():
    if not os.path.exists('items.db'):
        print("Baza danych przedmiotów nie istnieje.")
        return []
    conn = sqlite3.connect('items.db')
    conn.row_factory = sqlite3.Row  # Zwraca wyniki jako słowniki
    c = conn.cursor()
    c.execute('SELECT * FROM items')
    items = c.fetchall()
    conn.close()
    return items

# Funkcja do pobierania wszystkich przedmiotów z bazy danych items.db
def get_all_spells():
    if not os.path.exists('spells.db'):
        print("Baza danych przedmiotów nie istnieje.")
        return []
    conn = sqlite3.connect('spells.db')
    conn.row_factory = sqlite3.Row  # Zwraca wyniki jako słowniki
    c = conn.cursor()
    c.execute('SELECT * FROM spells')
    items = c.fetchall()
    conn.close()
    return items





