###### Dev установка
Установка пакетного менеджера:

(установка nodejs: `sudo apt-get install nodejs`)

(установка npm: `sudo apt-get install npm`)

(установка bower: `sudo npm install -g bower`)
> NOTE: возможна ошибка, связанная с конфликтом между node и nodejs, установите: `sudo apt-get install nodejs-legacy`

Установка виртуальной среды
```
virtualenv ~/Envs/grissli
source ~/Envs/grissli/bin/activate
```

Установка компонентов и статики
```
pip install -r requirements.txt
bower install
```

Запуск приложения
```
python run.py
celery worker -A page_parse.app.celery -P eventlet --loglevel=info
```
