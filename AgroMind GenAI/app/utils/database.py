

# import sqlite3
# from datetime import datetime

# DB_PATH = "agromind.db"


# # =========================================
# # DATABASE CONNECTION
# # =========================================
# def get_connection():
#     return sqlite3.connect(DB_PATH, check_same_thread=False)


# # =========================================
# # INITIALIZE DATABASE
# # =========================================
# def init_db():

#     conn = get_connection()
#     cursor = conn.cursor()

#     # Users table
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         phone_number TEXT PRIMARY KEY,
#         created_at TEXT
#     )
#     """)

#     # Predictions table
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS predictions (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         phone_number TEXT,
#         image_name TEXT,
#         predicted_class TEXT,
#         confidence REAL,
#         timestamp TEXT
#     )
#     """)

#     # Chats table
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS chats (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         phone_number TEXT,
#         disease_name TEXT,
#         predicted_section TEXT,
#         user_message TEXT,
#         bot_response TEXT,
#         feedback TEXT,
#         timestamp TEXT
#     )
#     """)

#     conn.commit()
#     conn.close()


# # =========================================
# # USER FUNCTIONS
# # =========================================
# def save_user(phone_number):

#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#     INSERT OR IGNORE INTO users (phone_number, created_at)
#     VALUES (?, ?)
#     """, (phone_number, datetime.now().isoformat()))

#     conn.commit()
#     conn.close()


# # =========================================
# # PREDICTION FUNCTIONS
# # =========================================
# def save_prediction(phone_number, image_name, predicted_class, confidence):

#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#     INSERT INTO predictions
#     (phone_number, image_name, predicted_class, confidence, timestamp)
#     VALUES (?, ?, ?, ?, ?)
#     """, (
#         phone_number,
#         image_name,
#         predicted_class,
#         confidence,
#         datetime.now().isoformat()
#     ))

#     conn.commit()
#     conn.close()


# def get_latest_prediction(phone_number):

#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#     SELECT predicted_class
#     FROM predictions
#     WHERE phone_number=?
#     ORDER BY id DESC
#     LIMIT 1
#     """, (phone_number,))

#     result = cursor.fetchone()

#     conn.close()

#     return result[0] if result else None


# # =========================================
# # CHAT FUNCTIONS
# # =========================================
# def save_chat(phone_number, disease_name, predicted_section, user_message, bot_response):

#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#     INSERT INTO chats
#     (phone_number, disease_name, predicted_section, user_message, bot_response, timestamp)
#     VALUES (?, ?, ?, ?, ?, ?)
#     """, (
#         phone_number,
#         disease_name,
#         predicted_section,
#         user_message,
#         bot_response,
#         datetime.now().isoformat()
#     ))

#     conn.commit()
#     conn.close()


# # =========================================
# # FEEDBACK FUNCTION
# # =========================================
# def save_feedback(phone_number, feedback):

#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#     UPDATE chats
#     SET feedback=?
#     WHERE id = (
#         SELECT id
#         FROM chats
#         WHERE phone_number=?
#         ORDER BY id DESC
#         LIMIT 1
#     )
#     """, (feedback, phone_number))

#     conn.commit()
#     conn.close()


# # =========================================
# # GET CHAT HISTORY
# # =========================================
# def get_chat_history(phone_number, limit=10):

#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#     SELECT user_message, bot_response
#     FROM chats
#     WHERE phone_number=?
#     ORDER BY id DESC
#     LIMIT ?
#     """, (phone_number, limit))

#     rows = cursor.fetchall()

#     conn.close()

#     return rows[::-1]


import sqlite3
from datetime import datetime

DB_PATH = "agromind.db"


# =========================================
# DATABASE CONNECTION
# =========================================
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# =========================================
# INITIALIZE DATABASE
# =========================================
def init_db():

    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        phone_number TEXT PRIMARY KEY,
        created_at TEXT
    )
    """)

    # Predictions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_number TEXT,
        image_name TEXT,
        predicted_class TEXT,
        confidence REAL,
        timestamp TEXT
    )
    """)

    # Chats table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_number TEXT,
        disease_name TEXT,
        predicted_section TEXT,
        user_message TEXT,
        bot_response TEXT,
        feedback TEXT,
        feedback_comment TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


# =========================================
# USER FUNCTIONS
# =========================================
def save_user(phone_number):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO users (phone_number, created_at)
    VALUES (?, ?)
    """, (phone_number, datetime.now().isoformat()))

    conn.commit()
    conn.close()


# =========================================
# PREDICTION FUNCTIONS
# =========================================
def save_prediction(phone_number, image_name, predicted_class, confidence):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO predictions
    (phone_number, image_name, predicted_class, confidence, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (
        phone_number,
        image_name,
        predicted_class,
        confidence,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_latest_prediction(phone_number):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT predicted_class
    FROM predictions
    WHERE phone_number=?
    ORDER BY id DESC
    LIMIT 1
    """, (phone_number,))

    result = cursor.fetchone()

    conn.close()

    return result[0] if result else None


# =========================================
# CHAT FUNCTIONS
# =========================================
def save_chat(phone_number, disease_name, predicted_section, user_message, bot_response):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO chats
    (phone_number, disease_name, predicted_section, user_message, bot_response, timestamp)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        phone_number,
        disease_name,
        predicted_section,
        user_message,
        bot_response,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


# =========================================
# SAVE FEEDBACK
# =========================================
def save_feedback(phone_number, feedback, comment=None):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE chats
    SET feedback=?, feedback_comment=?
    WHERE id = (
        SELECT id
        FROM chats
        WHERE phone_number=?
        ORDER BY id DESC
        LIMIT 1
    )
    """, (feedback, comment, phone_number))

    conn.commit()
    conn.close()


# =========================================
# GET TOTAL CHAT COUNT
# =========================================
def get_chat_count(phone_number):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM chats
    WHERE phone_number=?
    """, (phone_number,))

    count = cursor.fetchone()[0]

    conn.close()

    return count