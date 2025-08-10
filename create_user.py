from app import app, db, User

with app.app_context():
    # Verificar si el usuario ya existe
    username = 'test'
    existing_user = User.query.filter_by(username=username).first()
    
    if existing_user:
        print(f'El usuario {username} ya existe')
    else:
        # Crear un nuevo usuario
        new_user = User(username=username)
        new_user.set_password('password123')
        db.session.add(new_user)
        db.session.commit()
        print(f'Usuario {username} creado con éxito')