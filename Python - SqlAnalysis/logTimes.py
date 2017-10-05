#===============================================================================
# This class generates the debug files:
#    (1) resource_sessions.csv
#    (2) player_session_errors.csv
#===============================================================================

import csv
from datetime import datetime


def print3Dict(dic):
    """ easier to read format for dict with multiple values """
    for k,v in dic.items():
        print(k)
        for i,j in v.items():
            print(i,j)
            
            
            
class LogTimes(object):
    '''
        Class used to return total login times for each user
        based on their session login/logout times && resource activity times
    '''


    def __init__(self, cursor, userstats):
        '''
        user_stats = {} #{ actor_id : [ #passive_attempts, #active_attempts, #total_attempts, 
                         #passive_completed, #active_completed, #total_completed,
                         total_resource_time, adjusted_resource_time, total_login_time ] }
        user_times = { user_id : {day : [times]} }
        '''
        self.cursor = cursor
        self.user_stats = userstats
        self.user_times = {}
    
    
    def getResourceTimes(self):
        """
            Grabs resource activity from SQL DB
            Also formats date/times to datetime format
        """
        
        # grab resource sessions
        self.cursor.execute(" SELECT actor_id, revision FROM lrs_resource_records WHERE actor_id >= 11470 AND actor_id <=11545 ")
        for row in self.cursor.fetchall():
            
            user_id = row[0]
            
            # skip duplicate accounts
            if user_id in (11471, 11482, 11498):
                continue
            
            
            # parse out the date/time
            date_time = row[1].split('-')[2:]
            
            
            # convert date to format from 'player_sessions'
            day = date_time[0].split('/')
            
            # add preceeding zero to month and day (if applicable)
            if len(day[0]) == 1:
                day[0] = '0'+ day[0]
            if len(day[1]) == 1:
                day[1] = '0'+ day[1]
                
            day = day[2] + '-' + day[0] + '-' + day[1]
            
            
            # convert to military time
            mtime = ''
            time = date_time[1].split(':')
            
            if date_time[2] == 'PM': # if PM
                
                if time[0] == '12': # if noon
                    mtime = date_time[1]
                    
                else:
                    mtime = int(time[0]) + 12
                    mtime = str(mtime) + ":" + time[1] + ":" + time[2]
                
            else: # if AM
                
                if time[0] == '12': # if midnight
                    mtime = int(time[0]) + 12
                    mtime = str(mtime) + ":" + time[1] + ":" + time[2]
                    
                else:
                    mtime = date_time[1]
                    
                    
            date_time = day + ' '+ mtime
            
            # if dictionary key already created
            if user_id in self.user_times:
            
                # if day already in dictionary
                if day in self.user_times[user_id]:
                    self.user_times[user_id][day].append(date_time) 
                    
                # else insert day
                else:
                    self.user_times[user_id].update({ day : [date_time] })
                
            # else insert key
            else:
                self.user_times.update({ user_id : { day : [date_time] } })
    
        self.saveResourceSessions()
        
    
    def saveResourceSessions(self):
        """
            save consolidated resource sessions to CSV 
            NOT DeIdentified -> Used for debugging purposes
        """
        
        #print3Dict(self.user_times)
        writer = csv.writer( open( 'Debugging/resource_sessions.csv', 'w', newline='' ) )
        writer.writerow(['player_id', 'session_date(s)', 'session_time(s)'])
        
        # convert dictionary to sorted 3-D array
        user_resource_activity = []
        row = 0
        for user,values in self.user_times.items():
            
            user_resource_activity.append([user])

            for date,date_times in values.items():
                
                just_times = []
                for date_time in date_times:
                    
                    just_times.append(date_time.split(' ')[1])
                    
                user_resource_activity[row].append([date,just_times])
                
            row += 1
            
        sorted_times = sorted(user_resource_activity)
        
        
        # actual writing
        for date in range( len( sorted_times ) ):
            
            # write user_id
            writer.writerow([ sorted_times[date][0] ])
            
            for date_times in range( 1, len(sorted_times[date]) ):
                
                # write session_date
                writer.writerow([ '', sorted_times[date][date_times][0] ])
                
                for user in range( 1, len(sorted_times[date][date_times]) ):
                    # write resource just_times for that date
                    writer.writerow([ '', '', sorted_times[date][date_times][user] ])
                    
                    
    # NOTE: not using this function
    #       keeping for future reference
    def formatDateTime(self, date_time):
        """
            takes in: string of date && time
            converts: date format of YYYY-mm-dd to mm/dd/YYYY
            returns: as array of [date, time]
        """
        
        this_login = date_time.split(' ')
        this_login[0] = datetime.strptime(this_login[0], '%Y-%m-%d').strftime('%m/%d/%Y')
        
        # remove preceding zeros from both Date && Time
        for i in range(2):
            
            # first check if day position contains zero
            # Do NOT do this for the minute position
            if i == 0:
                if this_login[i][3] == '0':
                    this_login[i] = this_login[i][:3] + this_login[i][4:]
                    
            # then check if month/hour position contains zero
            if this_login[i][0] == '0':
                this_login[i] = this_login[i][1:]
                
        return this_login
        
        
        
    def days_between(self, d1, d2):
        """ Helper function to subtract # of days between 2 dates """
        
        d1 = datetime.strptime(d1, '%Y-%m-%d %H:%M:%S').date()
        d2 = datetime.strptime(d2, '%Y-%m-%d %H:%M:%S').date()
        
        return (d2 - d1).days
    
    def time_between(self, t1, t2):
        """ Helper function to subtract seconds between 2 string times """
        
        t1 = datetime.strptime(t1, '%Y-%m-%d %H:%M:%S')
        t2 = datetime.strptime(t2, '%Y-%m-%d %H:%M:%S')
        
        return (t2 -t1).total_seconds()
    
        

    def calculateLoginTime(self):
        """ calculates: Total Login Time
            based on session_lengths from player_sessions
                -> lrs_resource_records referenced for resource activity
            writes conflicts to CSV
                -> any logout_time == -1: means no resource activity for login date
                -> logout_time == None: means no resource activity between login time and next login time
        """
        self.getResourceTimes()
        
        # login time typically doesn't last longer than 1.5 hours
        TIMEOUT = 5400
        logout_time = None
        
        # create error file
        #f = open( 'Debugging/player_session_errors.csv', 'w', newline='' )
        #csv.writer( f ).writerow(['player_id', 'login_time', 'logout_time', 'session_length'])
        #f.close()
        writer = csv.writer( open('Debugging/player_session_errors.csv', 'w', newline='') )
        writer.writerow(['player_id', 'login_time', 'logout_time', 'session_length'])
        
        
        # retrieve resource session times from sql
        i = 0
        self.cursor.execute(" SELECT player_id, login_time, logout_time, session_length FROM player_sessions WHERE player_id >= 11470 AND player_id <=11545 ")
        player_sessions = sorted(self.cursor.fetchall())
        
        for row in player_sessions:
            
            user_id = row[0]
            
            # skip duplicate accounts
            if user_id in (11471, 11482, 11498):
                i += 1
                continue
            
            this_login = row[1] # aka login_time
            
            
            # (A) first need to check if resource_activity BEFORE login_time
            if i > 0:
                
                login_day = row[1].split(' ')[0]
                possible_login = None
                session_times = []
                
                # grab the resource times for the login_day
                try:
                    session_times = self.user_times[user_id][login_day]
                
                # return -1 if no resource activity for that day
                except:
                    session_times = -1
                    
                
                
                # if sessions exist for login_day
                if session_times != -1:
                    
                    prev_user = player_sessions[i-1][0]
                    prev_day = player_sessions[i-1][1].split(' ')[0]
                    
                    # (1) if no previous logout_time                    
                    if logout_time == -1 or logout_time == None:
                        
                        # but belongs to same user && same day
                        if prev_user == user_id and prev_day == login_day:
                            
                            # grab prev login
                            possible_login = row[1]
                            
                        
                        # simply grab earliest resource_time in day
                        else:
                            possible_login = session_times[0]
                    
                    
                    # (2) check if activity between prev_logout and current_login
                    # else there is logout, so check if logout_time from same_user and same_day
                    elif prev_user == user_id and prev_day == login_day:
                        
 
                        # find logout_time < Smallest_Time < login_time
                        for time in session_times:
                            
                            # ignore activities after login_time
                            # MUST subtract ( comparator DOES NOT work properly )
                            if self.time_between(this_login, time) > 0:
                                break
                            
                            # ignore activities before logout_time
                            if self.time_between(logout_time, time) <= 0:
                                continue
                            
                            # break after grabbing earliest time
                            possible_login = time
                            break
                    
                    # (3) else there is a logout, but it does not associate with same user_id/date
                    else:   
                        # grab earliest resource_time in day
                        possible_login = session_times[0]
                        
                        
                    # now see if logout_time is before this_login
                    if possible_login != None:
                        
                        # if it is, change it
                        if self.time_between(this_login, possible_login) < 0:
                            
                            this_login = possible_login
                            
                
                #ELSE NO ACTIVITY BEFORE LOGIN TIME thus CURRENT LOGIN TIME IS VALID
                
        
            
            # (B) need to ALWAYS CHECK if activity after "logout"
                
            # convert date/time to format that matches 
            next_row = None
            next_login = '9999-12-31 23:59:59' # default assumes no next login
            logout_time = None # reset initialization
            session_length = row[3]
            
            
            # (1) get next_login
            # error check for 'index out of bounds'
            if i+1 < len(player_sessions):
                
                next_row = player_sessions[i+1]
                
                # if user_id of this_row matches user_id of next_row
                if next_row[0] == user_id:
                    next_login = next_row[1]

            
            
            # (2) get logout_time
            # check difference in days  
            days = self.days_between( this_login, next_login)
            
            # if next_login IS NOT next (or same) day
            if days > 1:
                
                # simply get last time of day
                logout_time = self.getLogoutTimes(row)[-1]

                # check if logout_time < login_time
                if logout_time != -1:
                    if self.time_between(this_login, logout_time) < 0:
                        logout_time = None
                
        
            # if IS same day         
            elif days == 0:
                
                session_times = self.getLogoutTimes(row)
                
                
                # and if resource_session(s) exists for that day
                if session_times[0] != -1:
                    
                    
                    # ignore duplicate login times
                    if this_login == next_login:
                        i += 1
                        continue
                    
                    # return this_time < Greatest_Time < next_login_time
                    for time in session_times:
                        
                        # ignore activities after next_login_time
                        # MUST subtract ( comparator DOES NOT work properly )
                        if self.time_between(next_login, time) > 0:
                            break
                        
                        logout_time = time
                        
                
                    # check if logout_time < login_time
                    if logout_time != None:
                        if self.time_between(this_login, logout_time) < 0:
                                
                            logout_time = None
                              
                    
                # if session_times[0] is == -1
                else:
                    logout_time = session_times[0]
                        
            
            
            # check if login session wraps over to next day
            # if it does not, treat as inactivity
            elif days == 1:
                 
                # (a) first grab last session of login_day
                # remember logout_time == -1 means no resource activity during day of login
                #          logout_time == None means no resource activity between login of this day and next day
                logout_time = self.getLogoutTimes(row)[-1]
                
                # check if logout_time < login_time
                if logout_time != -1:
                    if self.time_between(this_login, logout_time) < 0:
                        logout_time = None
                 
                     
                # (b) check if resource_sessions before login of next day
                next_session_times = self.getLogoutTimes(next_row)
                times_b4_next_login = []
                                    
                
                # if resource activity exists
                if next_session_times[0] != -1:
                    
                    for time in next_session_times:
                         
                        # break if no resource_times before next_login_time
                        if self.time_between(next_login, time) > 0:
                            break
                         
                        # else, add to next_session_times
                        times_b4_next_login.append(time)
                
                
                
                # (c) check if resource activity between logins
                if (len(times_b4_next_login) > 0) and (logout_time != -1):
                     
                    # if reasonable amount_of_time between times
                    # else: logout_time remains unchanged
                    if logout_time != None:
                        if self.time_between(logout_time, times_b4_next_login[0]) < TIMEOUT:
                            
                            # grab this_time < Greatest_Time < next_login_time
                            # which is last resource time of next day before next login
                            logout_time = times_b4_next_login[-1]
                
                # if no resource activity between logins   
                elif (len(times_b4_next_login) == 0) and (logout_time == -1 or logout_time == None):
                    
                    session_length = -1 # a variable to denote extra info to be added to error log
                
                elif next_session_times == -1:
                    session_length = -2
            
            
            
            # (3) check calculated logout_time vs actual logout_time (if it exists)
            player_logout = row[2]
            
            # if logout time exists
            if player_logout[0] != '0':
                        
                # if logout_time represents a reasonable login length
                if self.time_between(this_login, player_logout) < TIMEOUT:
                    
                    # if logout_time exists
                    if type(logout_time) == 'str':
                            
                        # if  player_logout > logout_time 
                        if self.time_between(logout_time, player_logout) > 0:
                             
                            logout_time = player_logout
                            
                    # or if logout_time does not exist
                    else:
                        logout_time = player_logout
            
            
            # (4) if no resource_times exist between login_times 
            # && days with a login_time but no resource activity for that day
            #     treat as user inactivity and ignore those instances
            #     SAVE TO ERROR LOG
            if logout_time == -1 or logout_time == None:

#                 f = open( 'player_session_errors.csv', 'a', newline='' )
#                 writer = csv.writer( f )
                
                if logout_time == -1:
                    
                    
                    writer.writerow('')
                    writer.writerow(row)
                    
                    newrow = ['resource days:']
                    dates = sorted(self.user_times[user_id].keys(), key=lambda x: datetime.strptime(x, '%Y-%m-%d'))
                    newrow.extend(dates)          
                    writer.writerow(newrow)
                    
                    
                    
                    # log resource activity of next day
                    if session_length == -1:
                        newrow = ['next resource times:']
                        newrow.extend(self.user_times[ user_id ][ next_login.split(' ')[0] ])
                        writer.writerow(newrow)
                
                
                else:
                    writer.writerow('')
                    writer.writerow(row)
                    
                    if next_login[0] == '9':
                        next_login = "NO NEXT LOGIN"
                    writer.writerow([ 'next login:', next_login ])
                    
                    newrow = ['resource times:']
                    newrow.extend( self.user_times[ user_id ][ this_login.split(' ')[0] ] )
                    writer.writerow(newrow)
                    
                    # log no activity after login and no activity on next login of consecutive day
                    if session_length == -2:
                        newrow = ['resource days:']
                        dates = sorted(self.user_times[user_id].keys(), key=lambda x: datetime.strptime(x, '%Y-%m-%d'))
                        newrow.extend(dates)          
                        writer.writerow(newrow)
                        
                    # log no activity after login and no activity before next login
                    elif session_length == -1:
                        newrow = ['next resource times:']
                        newrow.extend( self.user_times[ user_id ][ next_login.split(' ')[0] ] )
                        writer.writerow(newrow)
                
#                 f.close()
                
                # reset session_length to reflect actual session_length
                # in stead of error_code
                session_length = 0
                
            
            # (4.b) else, calculate session_length
            else:
                
                # but first need to check if a logout already existed
                if row[2][0] != '0':
                    time_diff = self.time_between(logout_time, row[2])
                    
                    # if exisiting logout later, then use it 
                    if time_diff > 0 and time_diff < TIMEOUT:
                        logout_time = row[2]
                
                session_length = self.time_between(this_login, logout_time)
            

            # (C) !! finally can update user's total_login_time !!
            if session_length > 0:
                self.user_stats[user_id][8] += session_length

            
            # to access by index
            i += 1 
        
        return self.user_stats
        
    
    def getLogoutTimes(self, entry):
        """ returns: array of all logout_times for a user on a given day 
                     or -1 if no activity
        """
        user = entry[0]
        day = entry[1].split(' ')[0]
        
        try:
            session_times = self.user_times[user][day] 
            return session_times 
            
        # log all login_times that DO NOT have a session_time   
        except:
            return [-1]



  