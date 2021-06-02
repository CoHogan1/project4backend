how to set up a virtual environment.
set packages to local directory.

check version of pip
```
python3 -m pip --version

```
for linux'
set up env. end of command name is whatever I want to name it.
```
$ python3 -m venv env

```

no response in teminal, check directory for file.


activate vir env

```
$ source env/bin/activate

```

<!-- (env) conner@conner-ThinkPad-X1-Carbon-3rd:~/Desktop/sei-monstera/PYTHON3/flask$  -->


deactivate

```
$ deactivate
```
always .gitignore the env folder.




installing flask:
only when inside the vir env.

touch requirements.txt

```
$ pip3 install flask
```
```
$ pip3 freeze > requirements.txt

```
req. lists our dependencies. just like package.json


take a look at the terminal output.
if I go to local host 8000, i will see cannot get./ Not found. error 404

access sever http:localhost:8000 (localhost is the same as 127.0.0.1)s


install dotenv.

```
$ pip3 install python-dotenv
```

console shows
* Serving Flask app "app" (lazy loading) *****
* Environment: development *****
* Debug mode: on
* Running on http://127.0.0.1:8000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 269-295-309


To install packages from the requirements file and tell pip to install all of the packages in this file using the -r flag:

```
$ pip3 freeze > requirements.txt

```
When building my sever i must have my models sorted out first.
need two modules.

```
$ pip3 install psycopg2
```

```
$ pip3 install peewee
```


running your app should now create your db and tables.  
**here's how to check:**
1. run `python3 app.py` and you should see the "created tables" print in your terminal

2. quit your app and `ls` — there should be a `dogs.sqlite` file

3. connect to `dogs.sqlite` by running `sqlite3 dogs.sqlite`

4. in sqlite, type `.tables` and you should see `dog`, type `.schema dog`
and you should see an SQL create table statement that appears to be based
on your `Dog` model in `models.py`


```
$ pip3 install -U flask-cors
```



user login.

```
$ pip3 install flask-bcrypt flask_login

```



```
$ pip3 freeze > requirements.txt

```


create relationships between two models. "One to many"
