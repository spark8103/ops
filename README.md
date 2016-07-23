# ops
web ops system

Quick start
===========

> * You need a mysql instance running locally or remotely to connect. 
> * ops runs on Python 2.7
> * install virtualenv pip python-dev

### 0. install pip

download https://pypi.python.org/pypi/pip#downloads

```bash
# tar zxvf pip-*.tar.gz && cd pip*
# python setup.py install  #required python-setuptools python-devel
```

vi ~/.pip/pip.conf
```bash
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
```

```bash
# pip install virtualenv
```


### 1. Get ops

```bash
# git clone https://github.com/spark8103/ops.git
# cd ops
# virtualenv env
# ./env/bin/pip install -r requirements.txt
```

### 2. setting Mysql 

```bash
yum install mysql mysql-devel
docker run -d --restart=always --name mysql -v /home/mysql:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456 -e TZ="Asia/Shanghai" mysql:5.6.30

mysql -uroot -p123456 -h localhost
mysql> CREATE DATABASE IF NOT EXISTS ops COLLATE utf8_general_ci;
mysql> GRANT all privileges on ops.* to ops@'%' identified by '123456';
mysql> flush privileges;

# cat ops/settings.py
```

### 3. Run

```bash
# ./env/bin/python manage.py collectstatic
# ./env/bin/python manage.py makemigrations
# ./env/bin/python manage.py migrate
# ./env/bin/python manage.py runserver 0.0.0.0:80
# ./env/bin/python manage.py createsuperuser
```

## License
This project is licensed under the [Apache-2.0 license](https://opensource.org/licenses/Apache-2.0).
