import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class Database:
    """SQLite 데이터베이스 관리 클래스"""

    def __init__(self, db_path: str = "chat.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        """데이터베이스 연결 반환"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # 딕셔너리 형태로 결과 반환
        return conn

    def init_db(self):
        """데이터베이스 초기화 및 테이블 생성"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 메시지 테이블 생성
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def save_message(self, username: str, message: str) -> Dict:
        """메시지 저장"""
        conn = self.get_connection()
        cursor = conn.cursor()

        timestamp = datetime.now().isoformat()

        cursor.execute(
            "INSERT INTO messages (username, message, timestamp) VALUES (?, ?, ?)",
            (username, message, timestamp)
        )

        message_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return {
            "id": message_id,
            "username": username,
            "message": message,
            "timestamp": timestamp
        }

    def get_recent_messages(self, limit: int = 50) -> List[Dict]:
        """최근 메시지 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, username, message, timestamp FROM messages ORDER BY id DESC LIMIT ?",
            (limit,)
        )

        messages = []
        for row in cursor.fetchall():
            messages.append({
                "id": row["id"],
                "username": row["username"],
                "message": row["message"],
                "timestamp": row["timestamp"]
            })

        conn.close()

        # 오래된 순서로 반환
        return list(reversed(messages))

    def clear_old_messages(self, days: int = 30):
        """오래된 메시지 삭제"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM messages WHERE created_at < datetime('now', '-' || ? || ' days')",
            (days,)
        )

        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()

        return deleted_count


# 싱글톤 인스턴스
db = Database()
