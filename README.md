<!DOCTYPE html>
<html lang="en" xmlns:background-color="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="UTF-8">
    </head>
<body>
<h1>Инструкция по настройке проекта django на Ubuntu 21.10 Nginx и Gunicorn + Postgres</h1>
<p>
<h2>Содержание: </h2>
  <h3>  0. Версии приложений<br>
    1. Настройка droplet на digitalocean<br>
    2. Настройка проекта django. Подготовка команд для ввода<br>
    3. Настройка на сервере<br>
    4. Ссылки на источники<br></h3>
<hr>
  <h3> 0. Версии приложений<br></h3>

asgiref==3.4.1<br>
Django==4.0<br>
sqlparse==0.4.2<br>
tzdata==2021.5<br>
Ubuntu 21.10 x64<br>
python3.9<br>
psycopg2-binary-2.9.3<br><br>
<hr>

<h3>1. Настройка droplet на digitalocean<br></h3>
Требуется регистрация на сайте <a href='https://www.digitalocean.com/'>digitalocean.com</a><br>
    <ul>
    <li>Create/Droplets<br>
    <li>Ubuntu 21.10 x64<br>
    <li>Basic<br>
    <li>Regular Intel with SSD<br>
    <li>$5/mo<br>
    <li>Frankfurt<br>
    <li>Authentication - Password <br>
    <li>Create root password - вводим свожный пароль и записываем в блокнот<br>
    <li>Choose a hostname - стандартное заменяем на более короткое и подходящее<br>
    <li>Create Droplet<br>
    <li>Копируем IP в виде 64.227.126.18 в блокнот, он нам пригодится в дальнейшем.<br><br>
    </ul>
<hr>

<h3>2. Настройка проекта django<br> </h3>
<ol>
<li> Создаем копию файла <code>settings.py - local_settings.py.</code>
Открываем <code>settings.py</code><br><br>
<li> Добавляем:<br>
<h7><code>import os</code></h7><br><br>
<li>Заменяем <br>
<h7><code>BASE_DIR = Path(__file__).resolve().parent.parent</code></h7><br>
на<br>
<h7><code>BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))</code></h7><br><br>
<li>Создаем файл <code>secret_file.txt</code>. Cкопируем туда наш ключ, например:
<h7><code>SECRET_KEY='django-insecure-j=3s&a9*(s)-ex$z0s1o&)xeosea8k8#-tpl29ybc6wq$%zz!3'</code></h7><br>
и изменим имеющийся на <h7><code>SECRET_KEY = 'pu35hg2b5[q'egjq=h1=gebbvqpbdvhkevev'</code></h7><br><br>
<li>Изменим <h7><code>DEBUG = True</code></h7> на <h7><code>DEBUG = False</code></h7><br><br>
<li>В <h7><code>ALLOWED_HOSTS = []</code></h7> пропиcываем наш IP и localhost <br>
<h7><code>ALLOWED_HOSTS = ['64.227.126.18', 'localhost']</code></h7><br><br>
<li>Меняем настройки базы данных с sqlite на Postgres<br>
Вводим для БД имя, юзер и в файле <code>secret_file.txt</code> добавляем пароль сложный пароль, например:
<h7><code>'PASSWORD': "kdhbfvlkdvbavflakhvbafa65dbdgbg"</h7></code><br><br>
<h7><code>
DATABASES = {  

        'default': {  
        
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  
        
        'NAME': 'djangodb',  
        
        'USER': 'django',  
        
        'PASSWORD': 'superhardpassword'  
        
        'HOST': 'localhost',  
        
        'PORT': '5432',  
        
    }
    }
</h7></code>
<small>* Для удобного копипаста используйте соответствующие файлы проекта</small><br><br>
<li>Ниже <h7><code>STATIC_URL = 'static/'</h7></code> добавляем
<h7><code>STATIC_ROOT = os.path.join(BASE_DIR, 'static/')</h7></code><br><hr>
Остальное не обязательно, делаем для удобства<br><br>
<li>Создаем <code>setup.txt</code> и запишем код, который нужно вводить при настройке Nginx и Gunicorn.
Внесем данные которые уже известны IP, названия файлов, директорий и  пользователя,
которого планируем создать. Назовем его ivan. <br><br>

<b>gunicorn.socket</b><br><br>
<h7><code>
[Unit] 

Description=gunicorn socket  

[Socket]  

ListenStream=/run/gunicorn.sock  

[Install]

WantedBy=sockets.target
</h7></code><br><br>  


<b>gunicorn.service</b><br><br>
<h7><code>[Unit]  

Description=gunicorn daemon  

Requires=gunicorn.socket  

After=network.target  

[Service]  

User=ivan  

Group=ivan  

WorkingDirectory=/home/ivan/mysite  

ExecStart=/home/ivan/env/bin/gunicorn \  

--access-logfile - \  

--workers 3 \  

--bind unix:/run/gunicorn.sock \  

example.wsgi:application  

[Install]  

WantedBy=multi-user.target</h7></code><br>

<b>nginx for mysite</b><br><br>

<h7><code>server {  

listen 80;  

server_name 64.227.126.18;  

location = /favicon.ico { access_log off; log_not_found off; }  

location /static/ {  

root /home/ivan/mysite;  

}  

location / {  

include proxy_params;  

proxy_pass http://unix:/run/gunicorn.sock;  

}  

}</h7></code><br><br>
Вносим <code>local_settings.py</code>, <code>secret_file.txt</code> и <code>setup.txt</code>
в файл <code>.gitignore</code><br>
Делаем commit и push проекта на github<br><br></ol>
<hr>
<h3>3. Настройка на сервере</h3>
<ol>
<li>Открываем командную строку и вводим <h7><code>ssh root@64.227.126.18</code></h7> (root@наш_IP),
<h7><code>yes</code></h7>, пароль.<br>
<br>
<li>Создаем пользователя:<br>
<h7><code>adduser ivan</code></h7><br>
вводим пароль<br>
<h7><code>usermod -aG sudo ivan  

su ivan</code></h7><br><br>

<li>Устанавливаем пакеты:<br><br>
<h7><code>sudo apt update  

sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl</code></h7><br><br>

<li>Настраиваем БД postgresql:<br><br>
<h7><code>sudo -u postgres psql  

CREATE DATABASE djangodb;  

CREATE USER django WITH PASSWORD 'kdhbfvlkdvbavflakhvbafa65dbdgbg';  

ALTER ROLE django SET client_encoding TO 'utf8';  

ALTER ROLE django SET default_transaction_isolation TO 'read committed';  

ALTER ROLE django SET timezone TO 'UTC';  

GRANT ALL PRIVILEGES ON DATABASE djangodb TO django;  

\q</code></h7><br><br>

<li>Клонируем проект:<br><br>
<h7><code>cd ..  

cd /home/ivan  

git clone https://github.com/MGZV/mysite.git</code></h7><br><br>

<li>Ставим виртуальное окружение:<br><br>
<h7><code>sudo -H pip3 install --upgrade pip  

sudo -H pip3 install virtualenv  

virtualenv env  

source env/bin/activate</code></h7><br><br>

<li>Перемещаем файлы на дирректорию выше:<br><br>
<h7><code>cd mysite  

mv example/* ..  

cd ..  

rm -rf example/</code></h7><br><br>

<li>Устанавливаем пакеты:<br><br>
<h7><code>pip install -r requirements.txt  

pip install gunicorn  

pip install psycopg2-binary</code></h7><br><br>

<li>Собираем static файлы:<br><br>
<h7><code>cd ..  

python manage.py collectstatic  

deactivate</code></h7><br><br>

<li>Записываем подготовленный код в файлы gunicorn:<br><br>
<h7><code>sudo vim /etc/systemd/system/gunicorn.socket  

sudo vim /etc/systemd/system/gunicorn.service</code></h7><br><br>

<li>Вводим команды, смотрим исполнение:<br><br>
<h7><code>sudo systemctl enable gunicorn.socket  

sudo systemctl start gunicorn.socket  

sudo systemctl status gunicorn.socket  

curl --unix-socket /run/gunicorn.sock localhost  

file /run/gunicorn.sock  

sudo systemctl status gunicorn</code></h7>  

CTRL +C<br><br>

<li>Настраиваем nginx<br><br>
<h7><code>sudo vim /etc/nginx/sites-available/mysite  

sudo ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled  

sudo nginx -t  

sudo systemctl restart nginx</code></h7></ol><br><br>
<hr>
При редактировании файлов повторить:<br><br>
<h7><code>python manage.py collectstatic  

sudo service gunicorn restart  </code></h7> <br><br>

Переходим в браузере по IP. Радуемся!<br><br>
<hr>
<h3> 4. Ссылки на источники<br></h3>
<ol>
<li> Туториал на русском на сайте
<a href='https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04-ru'>digitalocean.com</a>
<br><br>
<li> Видео от канала <a href='https://www.youtube.com/watch?v=US9BkvzuIxw'>DigitalOcean</a><br><br>
<li> Видео на Ютубе от канала  <a href='https://www.youtube.com/watch?v=mp4rwP7Ny_A&t=3917s'>Django School</a><br><br>
<li> Курс от Senior Pomidor Developer
<a href='https://www.youtube.com/watch?v=GThTUNEJ0Y0&list=PLyaCd9XYVI9BQXrJU3zw3PGs_vcWw7_CD'>Django сервер на Linux</a><br><br></ol>
<hr>P.S. Это мой подход настройки сервера, если есть замечания или исправления обязательно напишите: anr.mgzv@gmail.com<br><br>
<br>

</body>
</html>
