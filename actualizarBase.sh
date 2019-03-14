#primera migracion para el modelo User que se usara para el Auth
python manage.py makemigrations superadmin
python manage.py migrate superadmin
#segunda migracion de Administrador por que es necesario para crear usuario primero
python manage.py makemigrations administrador
python manage.py migrate administrador
#los ultimo modelos que necesitan del User y Administrador
python manage.py makemigrations
python manage.py migrate