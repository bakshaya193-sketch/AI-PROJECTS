"""
Database initialization and connection management.
Creates all tables needed for v2: users, conversations, messages, tickets, config.
"""
import sqlite3
from datetime import datetime

DATABASE_PATH = "support_agent.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table for authentication
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'agent',
            email TEXT,
            created_date TEXT NOT NULL
        )
    """)

    # Conversations table - one per chat session
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            status TEXT DEFAULT 'active',
            language TEXT DEFAULT 'en',
            agent_active INTEGER DEFAULT 0,
            agent_name TEXT,
            agent_joined_at TEXT,
            customer_last_active TEXT,
            created_date TEXT NOT NULL,
            updated_date TEXT NOT NULL
        )
    """)

    # Messages table - every chat message stored here
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            sender TEXT NOT NULL,
            content TEXT NOT NULL,
            original_content TEXT,
            language TEXT DEFAULT 'en',
            sentiment TEXT DEFAULT 'neutral',
            sentiment_score REAL DEFAULT 0.0,
            created_date TEXT NOT NULL,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    """)

    # Tickets table - linked to conversations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            question TEXT NOT NULL,
            summary TEXT,
            status TEXT DEFAULT 'unresolved',
            priority TEXT DEFAULT 'normal',
            created_date TEXT NOT NULL,
            resolved_date TEXT,
            agent_id INTEGER,
            FOREIGN KEY (conversation_id) REFERENCES conversations(id)
        )
    """)

    # Documents table - tracks every uploaded file
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT UNIQUE NOT NULL,
            file_type TEXT NOT NULL,
            chunks_count INTEGER DEFAULT 0,
            file_size INTEGER DEFAULT 0,
            uploaded_date TEXT NOT NULL
        )
    """)

    # Config table for branding and notification settings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL
        )
    """)

    # Insert default config values
    defaults = [
        ("primary_color", "#2563eb"),
        ("company_name", "AI Support"),
        ("logo_url", ""),
        ("notification_email", ""),
        ("slack_webhook", ""),
        ("font_family", "Inter, sans-serif"),
    ]
    for key, value in defaults:
        cursor.execute("INSERT OR IGNORE INTO config (key, value) VALUES (?, ?)", (key, value))

    # Create default admin and agent users
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        # Admin user
        admin_hash = pwd_context.hash("admin123")
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, password_hash, role, email, created_date)
            VALUES (?, ?, ?, ?, ?)
        """, ("admin", admin_hash, "admin", "admin@company.com", datetime.now().isoformat()))

        # Agent user
        agent_hash = pwd_context.hash("agent123")
        cursor.execute("""
            INSERT OR IGNORE INTO users (username, password_hash, role, email, created_date)
            VALUES (?, ?, ?, ?, ?)
        """, ("agent", agent_hash, "agent", "agent@company.com", datetime.now().isoformat()))

        # Customer users
        for uname, pwd, email in [
            ("customer1", "customer123", "customer1@email.com"),
            ("customer2", "customer456", "customer2@email.com"),
        ]:
            h = pwd_context.hash(pwd)
            cursor.execute("""
                INSERT OR IGNORE INTO users (username, password_hash, role, email, created_date)
                VALUES (?, ?, ?, ?, ?)
            """, (uname, h, "customer", email, datetime.now().isoformat()))

    except Exception as e:
        print(f"Could not create default users: {e}")

    conn.commit()
    conn.close()
    print("✓ Database initialized")
