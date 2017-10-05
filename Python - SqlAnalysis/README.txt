This program produces statistics on tables pulled from a database.

Since the SQL dump from the Database is in MySQL format, if you want to use an updated SQL dump you MUST convert the MySQL File to an SQLite Database file (since python uses sqlite3 library to pull data from a database). 

I've already converted the database, but for your reference...

	(1) download the script from: https://github.com/dumblob/mysql2sqlite
	(2) download cygwin: 
		- (VERY IMPORTANT) during installing make sure to type "sqlite3" from 
		  the 'Select Packages' screen and click on all ( because cygwin MUST use it's version of sqlite )
	(3) use sqlite from cygwin
		- change directory: (run Cygwin.bat): "cd /cygdrive/c/ "
		- "./mysql2sqlite <db_name>.sql | sqlite3 <your_name>.db"


*To retain anonymity all input/output files are not included, other information inside the program may also be censored as well.