# Flask To-Do App

![](https://cdn.pixabay.com/photo/2017/01/20/19/53/productivity-1995786_960_720.jpg)

<div align="center"><i>There's not enough of these things already.</i></div>

## Motivation

A ***CRUD*** (**C**reate, **R**ead, **U**pdate, **D**elete) application is one of the smallest, non-trivial application that can be written for a language or framework. As someone who's learning **Python** and the web development framework **Flask**, I decided to practice my skills with the classic ***To-Do App***.

The ***Flask To-Do App*** uses **Flask** and **MySQL** for backend, and **Bootstrap** plus some custom *CSS* for the front end.

## Requirements

This application uses `python3` and `MySQL`

## Setup

1. Install dependencies

```
$ pip install -r requirements.txt
```

2. Setup the database

```
# Change app/__init__.py configuration if necessary.
$ mysql -u root -p
# Enter password
mysql> CREATE DATABASE flask_todo_app;
mysql> source schema.sql;
```

3. Start the server.
```
$ python3 run.py
```

## License

The contents of this repository is under the following license(s):

* MIT License