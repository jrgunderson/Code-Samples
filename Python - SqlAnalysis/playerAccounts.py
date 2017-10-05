#===============================================================================
# This class is used for:
#    (A) loading CodeNames from file
#    (B) de-identifying or re-identifying real_names from a file
#    (C) de-identifying user_id's from file
#===============================================================================


import csv
from difflib import get_close_matches


class PlayerAccounts(object):
    ''' de-identify or re-identify data 
    '''
    
    def __init__(self, cursor, user2mask=None):
        '''
            curser = database cursor NEEDS to be passed in!
            user_id2mask = defaulted to None if not being used
        '''
        self.cursor = cursor
        self.user_id2mask = user2mask
        
        
    
    def loadCoadeNames(self):
        """ loads from file 'Input Files/Code_Names.csv' 
        """

        reader = csv.reader( open('Input Files/Code_Names.csv') ) 
        
        code_names = {} # { real_name :  hash_code }
        for row in reader:
            code_names.update( {row[0].replace(' ','') : row[1]} ) # remove spaces, otherwise retrieving full names 
                                                                            # from cursor gets a little complicated
        
        
        # load user_id and real_name from database
        self.cursor.execute(" SELECT id, last_name, first_name FROM player_accounts WHERE id >= 11470 AND id <=11545 ")
        
        qa = [] # to ensure no key is used twice
        user_2_code = {} # {user_id : hash_code}
        
        for row in self.cursor.fetchall():
            
            # skip over the accounts that didn't work
            if row[0] in (11471, 11482, 11498):
                continue
            
            name = (row[1] + ',' + row[2])
            key = ''
            
            # return if 74% match 
            # to offset names that are off by a few letters  or variance in first name
            # && ensures people with same last name treated separately
            
            # handle exceptions first
            if name.split(',')[0] == 'Smith':
                name = 'Smith, John'
            
            if name.split(',')[1] == 'Jane':
                name = 'Doe, Jane'
            
            try:
                key = get_close_matches(name, code_names.keys(), cutoff=.74 )[0]
                qa.append(key)
                
            except IndexError:
                print("NO MATCH: ", name)
            
            
            user_2_code.update({ row[0] : code_names[key] })
            
        
        qa = sorted(qa)
        for i in range(len(qa)-1):
            if qa[i] == qa[i+1]:
                print("ERROR: ", qa[i], " ENTERED TWICE")
                
        return user_2_code
    
    
    
    def deIdentify(self, file_in, row, column):
        """ 
            takes in:
                (1) (CSV) file to be de-idnetified
                (2) the (zero indexed) row the real_names begin
                (3) the (zero indexed) column the real_names are in
        """
        # load up { real_name : hash_code }
        reader = csv.reader( open('Input Files/Code_Names.csv') ) 
        codenames = {}
        for entry in reader:
            codenames.update( {entry[0].lower() : entry[1]} )
        
        
        file_out = file_in.replace("In", "Out") + '_DeIdentified.csv'
        file_in += '.csv'
        reader = list( csv.reader( open(file_in) ) )
        writer = csv.writer( open(file_out, 'w', newline='') )
        
        
        # check if data already de-identified
        try:
            get_close_matches(reader[row][column].lower(), codenames.keys(), cutoff=.9 )[0] # 90% match
            
        except IndexError:
            print("...Data Does NOT need to be De-Identified!")
            return
        
        
        # copy over header(s)
        for entry in reader[:row]:
            writer.writerow(entry)
        
        # this is to ensure no entry is incorrectly duplicated
        qa = []
        
        # replace Real_Names with Code_Names
        # && rewrite to CSV file
        for entry in reader[row:]:
            
            key = get_close_matches(entry[column].lower(), codenames.keys(), cutoff=.9 ) # 90% match
            
            # if name exists, replace it with code name
            # if name does not exits, then ignore them
            if len(key) > 0:
                #print(entry[column], codenames[key[0]])
                qa.append(entry[column])
                
                entry[column] = codenames[key[0]]
                writer.writerow(entry)
                
            else:
                if entry[column] is not '':
                    print("NO MATCH: ", entry[column])
        
        qa = sorted(qa)
        for i in range(len(qa)-1):
            if qa[i] == qa[i+1]:
                print("ERROR: ", qa[i], " ENTERED TWICE")
                
    
    
    def reIdentify(self, file_in, row, column):
        """ takes in:
                (1) (CSV) file to be re-identified
                (2) the (zero indexed) column the code_names are in
        """
        
        reader = csv.reader( open('Code_Names.csv') ) 
        rev_codenames = {} # { hash_code : real_name }
        for entry in reader:
            rev_codenames.update( {entry[1] : entry[0]} )
        
        
        file_out = file_in.replace("In", "Out") + '_unmasked.csv'
        file_in += '.csv'
        
        reader = list( csv.reader( open(file_in) ) )
        writer = csv.writer( open(file_out, 'w', newline='') )
        
        
        # check if data already re-identified
        if reader[row][column] not in rev_codenames:
            print("...Data NOT De-Identified!")
            return
        
        # copy over header(s)
        for entry in reader[:row]:
            writer.writerow(entry)
        
        # replace De-Identified name with Code_Name
        # && rewrite to CSV file
        for entry in reader[row:]:
            entry[column] = rev_codenames[entry[column]]
            writer.writerow(entry)



    def deIdentifyUsers(self, file_in, row, column):
        """ 
            takes in:
                (1) (CSV) file to be de-idnetified
                (2) the (zero indexed) column the real_names are in
        """
        
        # first check if dictionary exists
        if self.user_id2mask == None:
            print("ERROR: Need dictionary that maps user_id's to hash_codes first!")
            return 
        
        
        file_out = file_in.replace("Debugging", "Output Files") + '_DeIdentified.csv'
        file_in += '.csv'
        reader = list( csv.reader( open(file_in) ) )
        writer = csv.writer( open(file_out, 'w', newline='') )
        
        
        # quick make sure file qualifies to be de-identified
        try:
            # do this by trying to convert the 'str' type user_id (which is a numerical value) to an 'int'
            int(reader[row][column])
            
        except ValueError:
            print("...Data Does NOT need to be De-Identified!")
            return
        
        
        # copy over header(s)
        for entry in reader[:row]:
            writer.writerow(entry)
        
        
        # replace Real_Names with Code_Names
        # && rewrite to CSV file
        for entry in reader[row:]:
            
            # keep in empty rows
            if len(entry) == 0:
                writer.writerow('')
                continue
            
            # to distinguish if user_id in that cell or not
            codename = None
            try: 
                codename = self.user_id2mask[ int(entry[column]) ]
                
            # if error converting to int, then cell must not contain user_id 
            except ValueError:
                writer.writerow(entry) # but you still need to copy over the data
                continue
            

            # replace user_id with code name
            entry[column] = codename
            writer.writerow(entry)
                
                
                
                
                
                        
        
        