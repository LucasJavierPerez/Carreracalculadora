from app import app, db, User

with app.app_context():
    print('Usuarios registrados:')
    print([u.username for u in User.query.all()])