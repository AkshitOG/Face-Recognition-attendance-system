from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def mark_attendance(name, app):
    from models import Person
    if not name or name.lower() == "unknown":
        return 
    
    with app.app_context():
        personexist = Person.query.filter_by(name=name).first()

        if personexist:
            return
        else:
            newperson = Person(
                name = name,
                date_time = datetime.now()
            )
            db.session.add(newperson)
            db.session.commit()
