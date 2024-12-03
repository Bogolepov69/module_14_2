import sqlite3

try:
    # Подключение к базе данных
    conn = sqlite3.connect('not_telegram.db')
    # Создание объекта курсора
    cursor = conn.cursor()
    # Создание таблицы Users, если её нет
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER,
            balance INTEGER NOT NULL
        )
    ''')

    # Заполнение таблицы 10 записями
    users = [
        ('User1', 'example1@gmail.com', 10, 1000),
        ('User2', 'example2@gmail.com', 20, 1000),
        ('User3', 'example3@gmail.com', 30, 1000),
        ('User4', 'example4@gmail.com', 40, 1000),
        ('User5', 'example5@gmail.com', 50, 1000),
        ('User6', 'example6@gmail.com', 60, 1000),
        ('User7', 'example7@gmail.com', 70, 1000),
        ('User8', 'example8@gmail.com', 80, 1000),
        ('User9', 'example9@gmail.com', 90, 1000),
        ('User10', 'example10@gmail.com', 100, 1000)
    ]
    cursor.executemany('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)', users)

    # Обновление баланса каждой второй записи
    cursor.execute('''
        UPDATE Users
        SET balance = 500
        WHERE id IN (
            SELECT id
            FROM Users
            WHERE id % 2 = 1
        )
    ''')

    # Удаление каждой третьей записи
    cursor.execute('''
        DELETE FROM Users
        WHERE id IN (
            SELECT id
            FROM Users
            WHERE id % 3 = 1
        )
    ''')

    # Выборка всех записей, где возраст не равен 60
    cursor.execute('''
        SELECT username, email, age, balance
        FROM Users
        WHERE age <> 60
    ''')
    rows = cursor.fetchall()

    # Вывод результатов
    for row in rows:
        print(f"Имя: {row[0]} | Почта: {row[1]} | Возраст: {row[2]} | Баланс: {row[3]}")

    # Расчет среднего баланса (добавлено)
    cursor.execute("SELECT COUNT(*) FROM Users")
    total_users = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(balance) FROM Users")
    all_balances = cursor.fetchone()[0]
    if total_users > 0:
        average_balance = all_balances / total_users
        print(f"Средний баланс: {average_balance}")
    else:
        print("Таблица пользователей пуста")

    conn.commit()

except sqlite3.Error as e:
    print(f"Ошибка базы данных: {e}")

finally:
    if conn:
        conn.close()


