from peewee import *
from datetime import datetime, date
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash

# ✅ Database connection
db = SqliteDatabase('gym.db')

# ✅ Base model
class BaseModel(Model):
    class Meta:
        database = db

# ✅ User model
class User(BaseModel):
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    phone = CharField()
    address = CharField(null=True)
    city = CharField(null=True)
    state = CharField(null=True)
    zip = CharField(null=True)
    birthdate = DateField()
    gender = CharField()
    password = CharField()
    plan = CharField()
    plan_type = CharField(null=True)
    payment_method = CharField(null=True)
    api_key = CharField(null=True)  # ✅ Add this line
    registered_at = DateTimeField(default=datetime.now)

    # ✅ Password helpers
    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

# ✅ Reminder model (linked to user)
class Reminder(BaseModel):
    user = ForeignKeyField(User, backref='reminders', on_delete='CASCADE')  # ✅ FK
    category = CharField()     # workout, skincare, etc.
    task = CharField()         # e.g. Yoga, Sunscreen
    interval = IntegerField()  # e.g. 4
    unit = CharField()         # hour, day, minute

# ✅ Workout model (linked to user)
class Workout(BaseModel):
    user = ForeignKeyField(User, backref='workouts', on_delete='CASCADE')  # ✅ FK
    type = CharField()        # e.g. cardio, strength
    name = CharField()        # e.g. pushups
    sets = IntegerField()
    reps = IntegerField()
    duration = IntegerField()
    calories = IntegerField()

# ✅ Create tables (safe & smart)
if __name__ == '__main__':
    db.connect()
    db.create_tables([User, Reminder, Workout], safe=True)
    print("✅ Tables created successfully")
    db.close()
