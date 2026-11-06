
import sqlite3
from datetime import date

DB_NAME = "expenses.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            expense_date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            monthly_budget REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS savings_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_name TEXT NOT NULL,
            target_amount REAL NOT NULL,
            saved_amount REAL NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS no_spend_challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            challenge_name TEXT NOT NULL,
            duration INTEGER NOT NULL,
            start_date TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Active'
        )
    """)

    conn.commit()
    conn.close()


# Expense functions

def add_expense(amount, category, description):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (amount, category, description, expense_date)
        VALUES (?, ?, ?, ?)
    """, (amount, category, description, date.today().isoformat()))

    conn.commit()
    conn.close()


def get_expenses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, amount, category, description, expense_date
        FROM expenses
        ORDER BY expense_date DESC, id DESC
    """)

    expenses = cursor.fetchall()
    conn.close()

    return expenses


def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()


# Budget functions

def set_monthly_budget(amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM budgets")

    cursor.execute(
        "INSERT INTO budgets (monthly_budget) VALUES (?)",
        (amount,)
    )

    conn.commit()
    conn.close()


def get_monthly_budget():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT monthly_budget FROM budgets LIMIT 1")

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else 0


# Savings goal functions

def add_savings_goal(goal_name, target_amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO savings_goals
        (goal_name, target_amount, saved_amount)
        VALUES (?, ?, 0)
    """, (goal_name, target_amount))

    conn.commit()
    conn.close()


def get_savings_goals():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, goal_name, target_amount, saved_amount
        FROM savings_goals
        ORDER BY id DESC
    """)

    goals = cursor.fetchall()
    conn.close()

    return goals


def update_savings(goal_id, amount):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE savings_goals
        SET saved_amount = saved_amount + ?
        WHERE id = ?
    """, (amount, goal_id))

    conn.commit()
    conn.close()


def delete_savings_goal(goal_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM savings_goals WHERE id = ?",
        (goal_id,)
    )

    conn.commit()
    conn.close()


# No-Spend Challenge functions

def create_challenge(challenge_name, duration):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO no_spend_challenges
        (challenge_name, duration, start_date, status)
        VALUES (?, ?, ?, 'Active')
    """, (challenge_name, duration, date.today().isoformat()))

    conn.commit()
    conn.close()


def get_challenges():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, challenge_name, duration, start_date, status
        FROM no_spend_challenges
        ORDER BY id DESC
    """)

    challenges = cursor.fetchall()
    conn.close()

    return challenges


def complete_challenge(challenge_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE no_spend_challenges
        SET status = 'Completed'
        WHERE id = ?
    """, (challenge_id,))

    conn.commit()
    conn.close()


def delete_challenge(challenge_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM no_spend_challenges WHERE id = ?",
        (challenge_id,)
    )

    conn.commit()
    conn.close()
