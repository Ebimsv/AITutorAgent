import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any

class TutorialDatabase:
    """Simple SQLite database for storing tutorial conversations."""
    
    def __init__(self, db_path: str = "database/tutorial_agent.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                message_type TEXT DEFAULT 'chat',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_conversation(self, session_id: str, subject: str) -> int:
        """Create a new conversation and return its ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (session_id, subject)
            VALUES (?, ?)
        ''', (session_id, subject))
        
        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return conversation_id
    
    def add_message(self, conversation_id: int, role: str, content: str, message_type: str = "chat"):
        """Add a message to the conversation."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO messages (conversation_id, role, content, message_type)
            VALUES (?, ?, ?, ?)
        ''', (conversation_id, role, content, message_type))
        
        conn.commit()
        conn.close()
    
    def get_conversation_history(self, conversation_id: int) -> List[Dict[str, Any]]:
        """Get all messages for a conversation."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT role, content, message_type, timestamp
            FROM messages
            WHERE conversation_id = ?
            ORDER BY timestamp ASC
        ''', (conversation_id,))
        
        messages = []
        for row in cursor.fetchall():
            messages.append({
                "role": row[0],
                "content": row[1],
                "message_type": row[2],
                "timestamp": row[3]
            })
        
        conn.close()
        return messages
    
    def get_conversations_by_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all conversations for a session."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, subject, created_at
            FROM conversations
            WHERE session_id = ?
            ORDER BY created_at DESC
        ''', (session_id,))
        
        conversations = []
        for row in cursor.fetchall():
            conversations.append({
                "id": row[0],
                "subject": row[1],
                "created_at": row[2]
            })
        
        conn.close()
        return conversations 