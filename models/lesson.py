from .database import get_db

class Lesson:
    def __init__(self, id, title, filepath, module, order_index):
        self.id = id
        self.title = title
        self.filepath = filepath
        self.module = module
        self.order_index = order_index
        
    @staticmethod
    def get_all():
        db = get_db()
        lessons = db.execute('SELECT * FROM lessons ORDER BY module ASC, order_index ASC').fetchall()
        return [Lesson(l['id'], l['title'], l['filepath'], l['module'], l['order_index']) for l in lessons]

    @staticmethod
    def get(lesson_id):
        db = get_db()
        lesson = db.execute('SELECT * FROM lessons WHERE id = ?', (lesson_id,)).fetchone()
        if not lesson:
            return None
        return Lesson(lesson['id'], lesson['title'], lesson['filepath'], lesson['module'], lesson['order_index'])
