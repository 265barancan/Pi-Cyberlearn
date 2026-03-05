from .database import get_db

class Progress:
    @staticmethod
    def get_completed_lessons(user_id):
        db = get_db()
        progress = db.execute('SELECT lesson_id FROM progress WHERE user_id = ?', (user_id,)).fetchall()
        return [p['lesson_id'] for p in progress]

    @staticmethod
    def mark_completed(user_id, lesson_id):
        db = get_db()
        try:
            db.execute(
                'INSERT INTO progress (user_id, lesson_id) VALUES (?, ?)',
                (user_id, lesson_id)
            )
            db.commit()
            return True
        except db.IntegrityError:
            return False  # Already completed
