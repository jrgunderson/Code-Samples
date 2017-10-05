#=============================================================================== 
#
# SETUP: Convert MySQL dump to SQLite DB (MUST BE DONE BEFORE RUNNING QUERIES)
# Note: I've already done this conversion, but for your reference... 
#    (1) download the script from: https://github.com/dumblob/mysql2sqlite
#    (2) download cygwin: 
#        - (VERY IMPORTANT) during installing make sure to type "sqlite3" from 
#        the 'Select Packages' screen and click on all ( because cygwin MUST use it's version of sqlite )
#    (3) use sqlite from cygwin
#        - change directory: (run Cygwin.bat): "cd /cygdrive/c/ "
#        - "./mysql2sqlite pal3db.sql | sqlite3 pal3db.db"
#
#=============================================================================== 

from analyzeSQL import AnalyzeSQL

if __name__ == '__main__':
    
    AnalyzeSQL().run()
    