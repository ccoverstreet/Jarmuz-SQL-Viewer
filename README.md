# Jarmuż SQL Viewer


Jarmuż SQL Viewer is a PyQt5-based MySQL/MariaDB (Only ones I have tested with) viewer. It uses Python Version 3.7.4 and uses the mysql-connector python module. 


___
# Installation

There are two ways of downloading Jarmuż SQL Viewer (second way still in progress). The first is to use git to clone the repository and run Python with all the necessary dependencies or use a platform specfic frozen executable. 

## Git

### Prerequisites
1. Install PyQt5 on your system (varies based on platform)
2. Install mysql-connector using the command `pip install mysql-connector`

### Installation

1. Run `git clone https://github.com/ccoverstreet/Jarmuz-SQL-Viewer.git`
2. Change into cloned directory with `cd Jarmuz-SQL-Viewer`
3. Run `python jarmuz_sql.py` to start the viewer.


___
# Using Jarmuż

To use Jarmuż, first login to your database user by clicking on the "File" menu and clicking the login option or by pressing "Ctrl + L". This will bring up a prompt that asks for a username and password. After entering your credentials, you should see that the databases table has been updated with all the available databases for the user. The bottom window is the SQL terminal, which allows you to run your own SQL commands. The output shows what user and database is selected. You can also navigate through databases and tables by clicking on the database/table you want in the left two table viewers. KEEP IN MIND when you click on a database, it also switches your SQL terminals active database to the selected one. I will be updating the program in a few days to show user and database on the entry line.
