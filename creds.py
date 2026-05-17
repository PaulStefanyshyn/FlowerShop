from app import app, Admin
from database.db import db

@app.cli.command('create-admin')
def create_admin():
    username = "KurvaBober"
    password = "NeoPass15243"
    admin = Admin(username=username)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print(f'Admin {username} created!')