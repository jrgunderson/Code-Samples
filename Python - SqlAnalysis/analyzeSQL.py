#=============================================================================== 
# ALL Database functions done in :memory: 
#    but, is still possible to dump database to .sql file
#===============================================================================
# Exports entire SQL Database into an excel file (w/Table of Contents) 'all_tables.xls'
#===============================================================================
# Calculates: 
#        (1) AVG Resource time/visit as 'avg_time_per_visit.csv'
#        (2) AVG Resource hits/user as 'hits_per_user.csv'
#        (3) Each User's mastery_score/resource as 'mastery_score_by_user.csv'
#        (4) Mastery scores for all users and all resources 'mastery_scores.csv'
#        (5) Passive/Active resources Attempted/Completed, total/adjusted Resource time, total Login time
#            'user_stats.csv'
#        (6) De-Identifies users from the file 'PAL3 Student Records Data.csv'
#        (7) De-Identifies user_ids from the file 'player_session_errors.csv'
#===============================================================================

import sqlite3
import csv
from xlwt import Workbook
import os
from pathlib import Path
from playerAccounts import PlayerAccounts
from logTimes import LogTimes
            

def reversedict(dic):
    """ for reversing dict that will definitely have same keys after doing so
        values for those keys will then be stored as a list
    """
    dictswap = {}
    for k,v in dic.items():
        if v not in dictswap:
            dictswap.update({v:k})
        else:
            value = dictswap[v]
            
            if type(value) is list: 
                value.append(k)
            else:
                value = [value, k]
                
            dictswap.update({v:value})
            
    return dictswap

def printdict(dic):
    """ easier to read format for dict with multiple values """
    for k,v in dic.items():
        print(k,v)
        
def numvalues(dic):
    """ count all values inside dict """
    length = 0
    for v in dic.values():
        for i in v:
            length += 1
            
    print(length)
    return length



class AnalyzeSQL():
    """ Analyzes data from SQL Database of PAL3 Users
    """
    

    def __init__(self):
        """ creates db connection in :memory:
            creates db cursor
            user_id2mask = { actor_id : code_name } 
            resource2index = { resource_id : index }
            result2resource = { result_id : resource_id }
            result2actor = { result_id : actor_id }
            raw_data = # [ result_id, is_passive, is_completion, score, duration ] }
            r_max_time = { resource_id : [name, max_duration] }
            resource_time_visit = { resource_id : [num_visits, total_time, avg_time per/visit] }
            resource_hits_per_user = { actor_id : [count for each resource] }
            player_mastery = { player_id : [topic mastery scores] }
            user_stats = {} #{ actor_id : [ #passive_attempts, #active_attempts, #total_attempts, 
                             #passive_completed, #active_completed, #total_completed,
                             total_resource_time, adjusted_resource_time, total_login_time ] }
        """
        self.connection = sqlite3.connect(':memory:')
        self.cursor = self.connection.cursor() 
        self.user_id2mask = {}
        self.resource2index = {}
        self.result2resource = {}
        self.result2actor = {} 
        self.raw_data = []
        self.r_max_time = {}
        self.resource_time_visit = {}
        self.resource_hits_per_user = {}
        self.player_mastery = {}
        self.user_stats = {}
    
    
    def db2sqlite(self):
        """ CONVERTS (original converted) .db to .sqlite """
        
        c = sqlite3.connect('Original DB\pal3db.db')
        with open('Original DB\pal3db.sqlite', 'w', encoding="utf8") as f:
            for line in c.iterdump():
                f.write('%s\n' % line)
        f.close()
        c.close()
        print('original .db file converted to .sqlite file')
        
        
    def buildDB(self):
        """ BUILD db into working :memory: from sqlite file """
        
        # convert db to sqlite file (if not done so already)
        if not Path(os.getcwd()+'\Original DB/pal3db.sqlite').is_file():
            self.db2sqlite()
            print("SQLite file created!")
        
        # build the database!
        sql_file = open('Original DB\pal3db.sqlite', 'r', encoding="utf8").read()
        self.connection.executescript(sql_file)
        print('.sqlite file loaded')
    
    
    # DUMP database - will be empty if you've: 
    # (1) have never run db2sqlite() 
    # (2) and didn't use buildDB() during this instance
    def dump(self):
        """ creates a .sql file of working database from :memory: """
        
        with open('Output Files/dump.sql', 'w', encoding="utf8") as f:
            for line in self.connection.iterdump():
                f.write('%s\n' % line)
        f.close()
        print("Database Dumped!")
        
    
    
    def saveaASexcel(self):
        """ saves database into a single excel workbook
            each table has it's own worksheet tab
                * 'dmis' is the only table that info was lost in conversion
        """
        wb = Workbook()
        
        # lookup & save 'index' of tables
        self.cursor.execute(" SELECT * FROM pal3db.sqlite_master ")
        self.save_sheet( wb.add_sheet('index') )
        
        
        # create array of table names
        tables = self.getAsColumn('name', 'pal3db.sqlite_master', "type = 'table'")
        
        # save all tables
        for table in tables:  
            
            command = 'SELECT * FROM ' + table
            self.cursor.execute(command)
            
            self.save_sheet( wb.add_sheet(table) )
    
        wb.save('Debugging/all_tables.xls')
        print('Excel file created!')
        
    
    def save_sheet(self, sheet):
        """ HELPER FUNCTION for saveASexcel()
            pass in: sheet you want to save 
        """
        
        # copy over header
        for i in range(len(self.cursor.description)):
            sheet.write(0, i, self.cursor.description[i][0])
        
        # copy over table contents (cell by cell)
        c = list(self.cursor)
        for i in range(len(c)):
            for j in range(len(c[i])):
                sheet.write(i+1, j, c[i][j])
    
        
    
    def table2csv(self, table_name):
        """ creates csv from db table """
        
        # filename == table_name
        filename = 'Tables/' + table_name + '.csv'
        writer = csv.writer( open( filename, 'w', encoding="utf8", newline='' ) )
        
        # cursor.execute('SELECT * FROM <table_name>')
        command = 'SELECT * FROM '+ table_name
        self.cursor.execute(command)
    
        writer.writerow([i[0] for i in self.cursor.description]) # write headers
        writer.writerows(self.cursor)
        
    
    
    # even when getting a single row from table it is returned as an array of tuples
    # so this function fixes that
    def getAsColumn( self, column_name, table_name, constraint= None ):
        """ returns a single column from table as an array """
        
        command = 'SELECT ' + column_name + ' FROM ' + table_name
        
        if constraint is not None:
            command += ' WHERE ' + constraint
        
        self.cursor.execute(command)
        
        column = []
        for row in self.cursor:
            for item in row:
                column.append(item)
        
        return column
    
    
    def initStuff(self):
        """ creates content for instance variables: 
                result2resource, result2actor, r_max_time, resource2index, 
                resource_hits_per_user, user_stats, player_mastery
        """
                
        
        # map {result_id : resource_id } -> ONLY FOR RESOURCES ACCESSED DURING TRIALS
        self.cursor.execute(" SELECT result_id, resource_id FROM lrs_resource_records WHERE actor_id >= 11470 AND actor_id <=11545 ORDER BY actor_id ASC")
        self.result2resource = dict(self.cursor.fetchall())
        
        
        # map {result_id : actor_id } -> ONLY FOR RESOURCES ACCESSED DURING TRIALS
        # BUT HAS NO WAY OF KNOWING IF RESOURCE CONSIDERED COMPLETE YET
        self.cursor.execute(" SELECT result_id, actor_id FROM lrs_resource_records WHERE actor_id >= 11470 AND actor_id <=11545 ")
        self.result2actor = dict(self.cursor.fetchall())
        
        
        # create map of { resource_id : [name, max_duration] } 
        self.cursor.execute(" SELECT id, name, duration FROM resources ")
        temp = self.cursor.fetchall()
        for row in temp:
            self.r_max_time.update({row[0]:[row[1:]]})
        
        
        # give an index to each resource_id
        index = 0
        for id in self.r_max_time.keys():
            self.resource2index.update({ id : index })
            index += 1
        
        # initialize dict (no users for id's 11488, 11513, 11534 || 11471, 11482, 11498 are accounts that didn't work)
        resources = len(self.resource2index)
        for actor in range(11470,11546):
            
            if actor in (11488, 11513, 11534, 11471, 11482, 11498):
                continue
            
            self.resource_hits_per_user.update({ actor : [0]*resources })
            self.user_stats.update({ actor : [0]*9})
            self.player_mastery.update({ actor : [0]*15 })  # { actor : [num_of_topics +1] }
                    
    
    
    def resourceTimePerVisit(self):
        """ fills the 'r_max_time' && 'resource_time_visit dictionaries'
        """
        result_times = {} # { result_id: resource_duration }

                    
        # Create map of { result_id: resource_duration }
        # IGNORE users who did NOT participate in TRIALS
        self.cursor.execute(" SELECT id, passive, success, completion, score, duration  FROM lrs_resource_results ")
        temp = self.cursor.fetchall()
        for row in temp:
            
            # if result_id from TRIAL
            if row[0] in self.result2resource:
                
                # if resource considered completed
                if self.isComplete(row):
                    result_times.update({row[0]:row[5]})
                
                # all raw_data
                self.raw_data.append(list(row))
        
        
        
        # create avg_time_per_visit dictionary
        for k,v in result_times.items():
            
            resource_id = self.result2resource[k]
            max_time = self.r_max_time[resource_id][0][1] # get second index of tuple inside array
            
            # log raw time
            self.user_stats[self.result2actor[k]][6] += v
            
            # cap maximum amount of time allowed in resource
            this_time = 0
            if v > max_time:
                this_time = max_time
                self.user_stats[self.result2actor[k]][7] += max_time # log adjusted time
            else:
                this_time = v
            
            # if resource_id already logged in dictionary...
            if resource_id in self.resource_time_visit:
                
                hits = self.resource_time_visit[resource_id][0] + 1
                total_time = self.resource_time_visit[resource_id][1] + this_time
                
                self.resource_time_visit.update({ resource_id : [hits, total_time, ''] })
                
            # else, create dictionary entry   
            else:
                # resource_time_visit = { resource_id : [num_visits, total_time, avg_time per/visit] } 
                self.resource_time_visit.update({ resource_id : [ 1, this_time, '' ] })   
        
        
        # cacluate avg time per visit / update dict
        for k,v in self.resource_time_visit.items():
            avg_time = float( "%.2f" % round( v[1]/v[0], 1 ) )
            
            self.resource_time_visit.update( {k: [v[0], float( "%.2f" % round(v[1],1)), avg_time ]} )
        
        self.saveTimePerVisit()
    

    
    def isComplete(self, resource_record):
        """ calculates if resource_record was completed 
            resource_record = [result_id, passive, success, completion, score, duration]
        """
        # if NON-passive resource
        if resource_record[1] == 0:
            if resource_record[3] == 1:
                return True
            else:
                return False
        # if PASSIVE resource
        else:
            # '.2' predetermined as a 'completed' score for 'passive' resources
            if resource_record[4] > .2:
                return True
            else:
                return False
    
    
    
    def saveTimePerVisit(self):
        """ exports dict to CSV (injects actual Resource Name) 
            #also saves the pertinent raw data from 'lrs_resource_results'
        """
        
        # save avg time per resourece visit
        writer = csv.writer( open( 'Output Files/avg_time_per_visit.csv', 'w', newline='' ) )
        writer.writerow(['id', 'name', 'num_visits', 'total_time (s)', 'avg_time_per_vist (s)', 'max_duration (s)'])
        
        for k,v in self.resource_time_visit.items():
            row = [k]
            row.extend(v)
            row.insert(1, self.r_max_time[k][0][0])
            row.append(self.r_max_time[k][0][1])
            writer.writerow(row)
            
        # save raw data
        writer = csv.writer( open( 'raw_data.csv', 'w', newline='' ) )
        writer.writerow(['id', 'resource_id', 'passive', 'success', 'completion', 'score', 'duration'])
         
        for row in self.raw_data:    
            row.insert(1, self.result2resource[row[0]])
            writer.writerow(row)
    
    
    
    def calculateHitsPerUser(self):
        """ uses: result2resources, & r_max_time
            to: generate resource_hits_per_user { actor_id : [ count for each resource ]
        """
        
        # start counting!
        # raw_data = [result_id, is_passive, did_attempt, is_completion, score, duration ] 
        for row in self.raw_data:
            
            resource = self.result2resource[row[0]]
            index = self.resource2index[resource]
            actor = self.result2actor[row[0]]
            
            # increment attempts
            if row[2] is not 0:
                
                self.user_stats[actor][2] += 1 # total_attempts
                
                if row[1] is 1:
                    self.user_stats[actor][0] += 1 # passive_attempts
                
                else:
                    self.user_stats[actor][1] += 1 # active_attempts
                
            # increment completed
            if self.isComplete(row):
                
                self.resource_hits_per_user[actor][index] += 1 # hits_per_user count 
                
                self.user_stats[actor][5] += 1 # total_completed
                
                if row[1] is 1:
                    self.user_stats[actor][3] += 1 # passive_completed
                
                else:
                    self.user_stats[actor][4] += 1 # active_completed
                
            
        # verify total hit count
        count = 0
        for v in self.resource_hits_per_user.values():
            for i in v:
                count += i
        print(count)

        self.saveHitsPerUser()



    def saveHitsPerUser(self):
        """ saves hits per user to csv """
        
        # save to csv
        writer = csv.writer( open( 'Output Files/hits_per_user.csv', 'w', newline='' ) )
        
        # create and write header
        header = ['user_id']
        for k in self.resource2index.keys():
            header.append('resource_' + str(k))
        writer.writerow(header)
          
        # save hits per user
        for k,v in self.resource_hits_per_user.items():
            
            row = [self.user_id2mask[k]] # de-identify
            row.extend(v)
            writer.writerow(row)
    
    
    
    def saveUserStats(self):
        """ saves user stats to csv """
        
        # save to csv
        writer = csv.writer( open( 'Output Files/user_stats.csv', 'w', newline='' ) )
        
        # create and write header
        header = [ 'user_id', '#_passive_attempts', '#_active_attempts', '#_total_attempts', 
                '#_passive_completed', '#_active_completed', '#_total_completed',
                'total_resource_time', 'adjusted_resource_time', 'total_login_time' ]
        writer.writerow(header)
          
        # save hits per user
        for k,v in self.user_stats.items():
            
            row = [self.user_id2mask[k]] # de-identify
            row.extend(v)
            writer.writerow(row)
        
    
    
    def calculateMastery(self):
        """ calculates most recent mastery score per topic for each participant
            ** indices of the self.player_mastery array is the topic_id
        """
        self.cursor.execute(" SELECT player_id, topic_id, date, mastery FROM player_topic_masteries WHERE player_id >= 11470 AND player_id <=11545")
        
        # sorted by player_id, topic, date
        all_masteries = sorted( self.cursor.fetchall() )
        
        for entry in all_masteries:
            
            # skip over duplicates
            if entry[0] in ( 11471, 11482, 11498 ):
                continue
            
            # just keep overwriting and most recent mastery score will be final overwrite 
            self.player_mastery[entry[0]][entry[1]] = entry[3]
                
        
        
    def saveMasteries(self):
        """ Save As (De-Identified):  
                (1) Player ID | Topic ID | Last Score
                (2) Player ID | Topic_ID_1_Score |...| Topic_ID_14_Score
        """
        writer1 = csv.writer( open( 'Output Files/mastery_score_by_user.csv', 'w', newline='' ) )
        writer1.writerow([ 'player_id', 'topic', 'recent_score' ])
        
        writer2 = csv.writer( open( 'Output Files/mastery_scores.csv', 'w', newline='' ) )
        header = ['player_id']
        self.cursor.execute(" SELECT id, name FROM topics ")
        topics = self.cursor.fetchall()
        for entry in topics:
            topic = str(entry[0]) + " : " + entry[1]
            header.append(topic)
        writer2.writerow(header)
        
        
        for entry in self.player_mastery.items():
            
            user = self.user_id2mask[entry[0]]
            row = [ user ]
            
            for topic in topics:
                
                score = entry[1][topic[0]]
                
                # 'mastery_score_by_user.csv'
                if score > 0:
                    writer1.writerow([ user, topic[0], score ])
                
                # 'mastery_scores.csv'
                row.append( score )
            writer2.writerow(row)
    
    
    
    def run(self):
        """ MAIN """
        
        print("Analyzing Database...")
        
        
        # LOAD pal3db into working :memory:
        #self.buildDB()
        self.cursor.execute(" ATTACH DATABASE 'Original DB\pal3db.db' AS pal3db ")
        
        # Visually display data inside tables
        #self.saveaASexcel()
        
        self.user_id2mask = PlayerAccounts(self.cursor).loadCoadeNames() # { user_id : hash_code }
        PlayerAccounts(self.cursor).deIdentify('Input Files/PAL3 Student Record Data', 3, 0)
        
        self.initStuff()
        self.resourceTimePerVisit()
        self.calculateHitsPerUser()
        self.user_stats = LogTimes(self.cursor, self.user_stats).calculateLoginTime()
        self.saveUserStats()
        
        PlayerAccounts(self.cursor, self.user_id2mask).deIdentifyUsers('Debugging/player_session_errors', 2, 0)
        
        self.calculateMastery()
        self.saveMasteries()
        
        
        
        # Clean up
        #self.dump()
        self.cursor.close()
        self.connection.close()
        
        print("...Database Analyzed")
        
    
     
