from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

def mark_attendance(name, app):
    from models import Person
    if not name or name.lower() == "unknown":
        return 
    
    with app.app_context():
        personexist = Person.query.filter_by(name=name).all()
        for p in personexist:
            if p.date_time.date() == date.today():
                return
            
        newperson = Person(
            name = name,
            date_time = datetime.now()
        )
        db.session.add(newperson)
        db.session.commit()


def daily_total_count():
    from models import Person

    today = date.today()
    count = 0
    for person in Person.query.all():
        if person.date_time.date() == today:
            count += 1
    return count
