
import os
import re
import csv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# App setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_secret_key'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return redirect(url_for('calculator'))

@app.route('/training_table', methods=['GET', 'POST'])
@login_required
def training_table():
    distance_headers = ['1000', '1200', '1500', '2000', '3000', '4000', '5000']
    table_data = []
    highlighted_row = None
    vo2_max = None
    time_input = None
    velocity_ms = None
    velocity_kmh = None
    
    # Definir las zonas de entrenamiento y sus porcentajes de VO2 max
    training_zones = [
        {'name': 'Regenerativo', 'percentages': [40, 45, 50]},
        {'name': 'Umbral Aeróbico', 'percentages': [55, 60, 65, 70]},
        {'name': 'Umbral anaeróbico', 'percentages': [75, 80, 85]},
        {'name': 'Vo2 Max', 'percentages': [90, 95, 100]},
        {'name': 'Tolerancia Lactica', 'percentages': [105, 110, 115]}
    ]
    
    # Obtener tiempo del formulario POST o de la URL GET
    if request.method == 'POST':
        time_input = request.form.get('time')
    elif request.args.get('time'):
        time_input = request.args.get('time')
    
    if time_input:
        if not re.match(r'^\d{1,2}:\d{2}$', time_input):
            flash('Formato de tiempo inválido. Por favor use MM:SS.', 'danger')
            return redirect(url_for('training_table'))

        minutes, seconds = map(int, time_input.split(':'))
        if seconds >= 60:
            flash('Los segundos deben ser menos de 60.', 'danger')
            return redirect(url_for('training_table'))

        total_seconds = minutes * 60 + seconds
        
        # Calcular velocidad en m/s
        distance = 1000  # metros
        velocity_ms = distance / total_seconds
        velocity_kmh = velocity_ms * 3.6
        
        # Estimar VO2 max basado en la velocidad (velocidad × 3.5)
        vo2_max = round(velocity_kmh * 3.5, 2)
        
        # Generar los datos de la tabla basándose en el tiempo del usuario
        row_index = 0
        for zone in training_zones:
            for percentage in zone['percentages']:
                # Calcular la velocidad para este porcentaje de VO2 max
                zone_velocity_ms = velocity_ms * (percentage / 100)
                zone_velocity_str = f"{zone_velocity_ms:.2f}".replace('.', ',')
                
                # Calcular tiempos para cada distancia
                times = []
                for i, distance in enumerate(distance_headers):
                    distance_m = int(distance)
                    
                    # Para distancias 4000m y 5000m, solo mostrar datos hasta 85% VO2 max
                    if distance_m >= 4000 and percentage > 85:
                        times.append('')  # Celda vacía
                    else:
                        time_seconds = distance_m / zone_velocity_ms
                        
                        # Formatear tiempo como MM:SS o HH:MM:SS
                        if time_seconds < 3600:  # Menos de 1 hora
                            minutes = int(time_seconds // 60)
                            seconds = int(time_seconds % 60)
                            time_str = f"{minutes}:{seconds:02d}"
                        else:  # 1 hora o más
                            hours = int(time_seconds // 3600)
                            minutes = int((time_seconds % 3600) // 60)
                            seconds = int(time_seconds % 60)
                            time_str = f"{hours}:{minutes:02d}:{seconds:02d}"
                        
                        times.append(time_str)
                
                # Añadir fila a la tabla
                table_data.append({
                    'zone': zone['name'],
                    'vo2_percent': f"{percentage}%",
                    'velocity': zone_velocity_str,
                    'times': times
                })
                
                # Verificar si esta es la fila más cercana al ritmo del usuario (100% VO2 max)
                if percentage == 100:
                    highlighted_row = row_index
                
                row_index += 1
    
    return render_template('training_table.html', 
                           distance_headers=distance_headers, 
                           table_data=table_data, 
                           highlighted_row=highlighted_row,
                           vo2_max=vo2_max, 
                           velocity_ms=velocity_ms,
                           velocity_kmh=velocity_kmh,
                           time_input=time_input)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return redirect(url_for('register'))

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('calculator'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/calculator', methods=['GET', 'POST'])
@login_required
def calculator():
    if request.method == 'POST':
        time_input = request.form.get('time')
        if not re.match(r'^\d{1,2}:\d{2}$', time_input):
            flash('Invalid time format. Please use MM:SS.', 'danger')
            return redirect(url_for('calculator'))

        minutes, seconds = map(int, time_input.split(':'))
        if seconds >= 60:
            flash('Seconds must be less than 60.', 'danger')
            return redirect(url_for('calculator'))

        total_seconds = minutes * 60 + seconds
        base_pace_min_km = total_seconds

        if not (180 <= base_pace_min_km <= 600):
            flash('Pace must be between 3:00 and 10:00 min/km.', 'danger')
            return redirect(url_for('calculator'))

        base_speed_kmh = 3600 / base_pace_min_km

        zones = {
            'Zona 1 (Regenerativo) % 50 al 60': (0.50, 0.60),
            'Zona 2 (Umbral Aeróbico) % 65 al 70': (0.65, 0.70),
            'Zona 3 (Umbral Anaeróbico) % 75 al 85': (0.75, 0.85),
            'Zona 4 (Vo2 Max) % 90 al 100': (0.90, 1.00),
            'Zona 5 (Tolerancia Láctica) % 105 al 115': (1.05, 1.15)
        }

        results = {}
        for zone, (max_perc, min_perc) in zones.items():
            min_speed = base_speed_kmh * min_perc
            max_speed = base_speed_kmh * max_perc
            min_pace = 60 / max_speed
            max_pace = 60 / min_speed
            results[zone] = {
                'min_pace': f'{int(min_pace)}:{int((min_pace * 60) % 60):02d}',
                'max_pace': f'{int(max_pace)}:{int((max_pace * 60) % 60):02d}'
            }
        
        base_pace_formatted = f'{minutes}:{seconds:02d}'

        return render_template('index.html', results=results, base_pace=base_pace_formatted, original_time=time_input)

    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # Use Railway's PORT environment variable or default to 5001 for local testing
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
