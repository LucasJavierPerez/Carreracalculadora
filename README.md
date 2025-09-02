# Calculadora de Ritmos de Running

Esta es una aplicación web para calcular ritmos de running y generar tablas de entrenamiento personalizadas.

## Características

- Calculadora de ritmos por zona de entrenamiento
- Tabla de tiempos por distancias parciales
- Sistema de autenticación de usuarios
- Compatible con dispositivos móviles (PWA)

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual: `python -m venv venv`
3. Activar el entorno virtual: `source venv/bin/activate` (Linux/Mac) o `venv\Scripts\activate` (Windows)
4. Instalar dependencias: `pip install -r requirements.txt`
5. Ejecutar la aplicación: `python app.py`

## Despliegue en Railway

La aplicación está configurada para desplegarse en Railway. Simplemente conecta el repositorio a Railway y se desplegará automáticamente.

## Uso

1. Registra una cuenta o inicia sesión
2. Ingresa tu tiempo en 1000m en formato MM:SS
3. Obtén tus ritmos de entrenamiento personalizados por zona
4. Usa la tabla de entrenamiento detallada para planificar tus sesiones

## PWA (Progressive Web App)

La aplicación puede instalarse en dispositivos móviles como una aplicación nativa:

### En Android:
1. Abre la aplicación en un navegador móvil (Chrome/Safari)
2. Busca la opción de "Agregar a pantalla de inicio" o "Instalar aplicación"
3. Sigue las instrucciones del navegador

### En iOS:
1. Abre la aplicación en Safari
2. Presiona el botón de compartir (cuadrado con flecha hacia arriba)
3. Selecciona "Agregar a pantalla de inicio"
4. Sigue las instrucciones para agregar la aplicación

**Nota:** En iOS, la instalación funciona a través de la opción "Agregar a pantalla de inicio" en Safari. La aplicación funcionará como una PWA aunque no aparezca un botón de instalación específico como en Android.

## Compatibilidad

- Android: Compatible con Chrome y navegadores que soportan PWA
- iOS: Compatible con Safari (a través de "Agregar a pantalla de inicio")
- Desktop: Compatible con Chrome, Firefox, Edge y Safari
