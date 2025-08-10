# Prompt para Gemini CLI: Calculadora de Ritmo de Running en Flask con Sistema de Login

Quiero que generes una aplicación web en **Flask** (Python) que funcione como una calculadora de ritmo de running y calcule las zonas de entrenamiento basadas en el tiempo que el usuario tarda en correr 1000 metros. La aplicación debe incluir un sistema de autenticación (registro, login y logout) ya que estará en internet, y solo los usuarios autenticados podrán usar la calculadora. La aplicación debe ser precisa, fácil de usar y cumplir con los siguientes requisitos:

## Requisitos Generales
1. **Interfaz Web**:
   - Crear una página principal con un formulario donde el usuario ingrese el tiempo de 1000 metros en el formato **MM:SS** (minutos:segundos, por ejemplo, 4:30 para 4 minutos y 30 segundos).
   - Validar que el input sea un tiempo válido (formato MM:SS, donde MM y SS son números, SS < 60).
   - Mostrar un botón para calcular el ritmo y las zonas de entrenamiento.
   - Mostrar los resultados en la misma página, incluyendo:
     - Ritmo base en minutos por kilómetro (min/km) con dos decimales.
     - Tabla con las 5 zonas de entrenamiento (Z1 a Z5) con rangos de ritmo (mínimo y máximo) en min/km.
   - Incluir un sistema de navegación con enlaces para "Login", "Registro", "Calculadora" (solo visible para usuarios autenticados) y "Logout" (solo visible para usuarios autenticados).

2. **Sistema de Autenticación**:
   - Implementar un sistema de registro y login usando **Flask-Login** o una solución similar.
   - Crear una base de datos SQLite para almacenar usuarios (campos: id, username, password_hash).
   - Durante el registro, solicitar un nombre de usuario y una contraseña (almacenar la contraseña hasheada usando **bcrypt** o **Werkzeug.security**).
   - Validar que el nombre de usuario sea único y que la contraseña tenga al menos 8 caracteres.
   - En el login, verificar las credenciales y redirigir a la página de la calculadora si es exitoso.
   - Proteger la ruta de la calculadora para que solo usuarios autenticados puedan acceder.
   - Incluir una opción de logout que cierre la sesión del usuario.
   - Mostrar mensajes de error claros para credenciales inválidas, usuario no registrado, o problemas en el registro.

3. **Cálculo del Ritmo Base**:
   - Convertir el tiempo ingresado para 1000 metros (en segundos) a un ritmo base en minutos por kilómetro.
   - Ejemplo: Si el usuario ingresa 4:30 (4 minutos y 30 segundos) para 1000 metros, el ritmo base es 4:30 min/km.
   - Asegurar que los cálculos sean precisos y se muestren en formato MM:SS con dos decimales para los segundos (por ejemplo, 4:30.00).

4. **Cálculo de Zonas de Entrenamiento**:
   - Basarse en el ritmo base (en segundos por kilómetro) para calcular las zonas de entrenamiento (Z1 a Z5) según porcentajes estándar de ritmo o velocidad.
   - Usar las siguientes zonas de entrenamiento basadas en el porcentaje de la velocidad base:
     - **Z1 (Recuperación)**: 65-75% de la velocidad base.
     - **Z2 (Aeróbica)**: 75-85% de la velocidad base.
     - **Z3 (Umbral Aeróbico)**: 85-90% de la velocidad base.
     - **Z4 (Umbral Anaeróbico)**: 90-95% de la velocidad base.
     - **Z5 (Máximo Esfuerzo)**: 95-100% de la velocidad base.
   - Convertir la velocidad base (km/h) a ritmo (min/km) para cada zona, mostrando un rango de ritmo mínimo y máximo para cada zona en formato MM:SS con dos decimales.
   - Ejemplo: Para un ritmo base de 4:30 min/km (13.33 km/h):
     - Calcular velocidad de cada zona (porcentaje de 13.33 km/h).
     - Convertir cada velocidad a ritmo (min/km) usando la fórmula: ritmo = 60 / velocidad.
     - Mostrar rangos de ritmo para cada zona (mínimo y máximo).

5. **Precisión y Formato**:
   - Todos los cálculos de ritmo deben ser precisos, redondeando los segundos a dos decimales.
   - Los tiempos deben mostrarse en formato MM:SS (por ejemplo, 4:30.00).
   - Validar que el ritmo base esté en un rango realista (entre 3:00 y 10:00 min/km) para evitar errores en los cálculos.
   - Si el input es inválido, mostrar un mensaje de error claro al usuario.

6. **Estructura del Proyecto**:
   - Crear un proyecto Flask con la siguiente estructura:
     ```
     /running_calculator
     ├── app.py
     ├── templates/
     │   ├── index.html
     │   ├── login.html
     │   ├── register.html
     ├── static/
     │   └── style.css
     ├── database.db
     ```
   - **app.py**: Contiene el código Flask con las rutas (login, registro, logout, calculadora) y la lógica de cálculo.
   - **index.html**: Plantilla HTML para la calculadora con el formulario y la tabla de resultados. Usar Jinja2 para renderizar los resultados y mostrar el estado de autenticación.
   - **login.html**: Plantilla HTML para el formulario de login.
   - **register.html**: Plantilla HTML para el formulario de registro.
   - **style.css**: Estilos básicos para que la interfaz sea clara y profesional (usar un diseño limpio, con una tabla bien formateada para las zonas y formularios legibles).
   - **database.db**: Base de datos SQLite para almacenar usuarios.

7. **Detalles Técnicos**:
   - Usar Python 3.x, Flask, Flask-Login, y Werkzeug.security (o bcrypt) para autenticación.
   - Usar SQLite para la base de datos, inicializada en `app.py` con una tabla de usuarios.
   - Incluir validaciones robustas para los inputs del usuario (tanto en el formulario de la calculadora como en los formularios de login/registro).
   - Asegurar que los cálculos de las zonas sean consistentes y sigan las fórmulas indicadas.
   - Incluir comentarios detallados en el código para explicar la lógica de los cálculos y la autenticación.

8. **Interfaz de Usuario**:
   - La página principal debe tener un título claro, como "Calculadora de Ritmo de Running".
   - Incluir una barra de navegación con enlaces a "Login", "Registro", "Calculadora" (solo para usuarios autenticados) y "Logout" (solo para usuarios autenticados).
   - El formulario de la calculadora debe incluir un campo para el tiempo (MM:SS) y un botón "Calcular".
   - Los resultados deben mostrarse en una tabla con columnas: Zona, Ritmo Mínimo (MM:SS), Ritmo Máximo (MM:SS).
   - Los formularios de login y registro deben ser claros, con campos para nombre de usuario y contraseña, y un botón para enviar.
   - Usar CSS para que la interfaz sea legible (bordes, espaciado, fuente clara).
   - Mostrar mensajes de error claros para inputs inválidos o problemas de autenticación.

9. **Ejemplo de Resultado Esperado**:
   - Input: 4:30 (4 minutos y 30 segundos para 1000 metros).
   - Ritmo base: 4:30.00 min/km.
   - Zonas de entrenamiento (aproximadas):
     - Z1: 5:41.54 - 6:36.92 min/km
     - Z2: 5:01.18 - 5:41.54 min/km
     - Z3: 4:43.53 - 5:01.18 min/km
     - Z4: 4:28.42 - 4:43.53 min/km
     - Z5: 4:16.67 - 4:28.42 min/km

Por favor, genera el código completo para la aplicación Flask, incluyendo `app.py`, `index.html`, `login.html`, `register.html`, `style.css`, y la configuración de la base de datos SQLite. Asegúrate de que los cálculos sean precisos, el formato sea consistente (MM:SS con dos decimales), la autenticación sea segura, y la interfaz sea clara y funcional. Incluye comentarios detallados en el código para explicar la lógica, especialmente en los cálculos de las zonas de entrenamiento y la autenticación.