#===============================================================================
#   Takes in 3 Files: 
#        'Test Data.xlsx' =  raw Tests & Surveys from the PAL3 study
#        'Pal3 Answer Key.xlsx' = answer key for tests
#        'Item Difficulty_Growth.csv' = maps test question to its corresponding KC
 
#   Exports 3 CSV Files:
#        'Test_Results' = participant Scores by Item
#        'Growth_Stats' = participant Growth by Session
#        'Item_Difficulty' = Growth per Item per Session for EXP & CNTRL
#
#   Also De-Identifies ALL participant's names (this is done only once)
#===============================================================================

import csv
import openpyxl
from operator  import itemgetter
from builtins import str
from statistics import mean
import string
import random
import os
from pathlib import Path

def print2D( arrays ):
    """ cleaner format for displaying 'list of lists' """
    for array in arrays:
        print(array)
    print()


def printdict( dictionary ):
    """ cleaner format for displaying 'dictionary' """
    for k, v in dictionary.items():
        print(k,v,sep=' : ')
    print()



class CalculateStatistics:
    """ Uses raw test data to calculate score (% correct) & growth (between sessions)
        for each participant, as well as each question on each test
    """
    
    
    def __init__(self):
        """ questionMaps = map of { test_question# : orig_question# } 
            kcMaps = { test_question_number : [ KC Source, Knowledge Component ] }
            mTests = (Test_Results.csv) 2D list of all cadet's test scores across all sessions & tests
            mGrowth = global dict that keeps track of each student's mGrowth
            mItemDifficulty = 3D List that keeps track of (2D List) Test Stats per Session per Group
            codeNames = map of de-identified names and real names {real_name: code_name}
        """
        self.questionMaps = {}
        self.kcMaps = { 'A':{}, 'B':{}, 'C':{} } 
        self.mTests = [] 
        self.mGrowth = {} 
        self.mItemDifficulty = [] 
        self.codeNames = {} 
        
    
    
    def Run(self, isMasked):
        """ MAIN 
            isMasked == boolean value to de-identify subject's names
        """
        
        print("Calculating Statistics...", end='\n\n')
        
        # import answer key data and convert to list of lists
        wb = openpyxl.load_workbook( 'Input Files/PAL3 Answer Key.xlsx' )
        correctAnswersA = self.AnswerKey( wb.get_sheet_by_name('Test A') )
        correctAnswersB = self.AnswerKey( wb.get_sheet_by_name('Test B') )
        correctAnswersC = self.AnswerKey( wb.get_sheet_by_name('Test C') )
        
        # create map of {Q : KC}
        self.MapKC()
        
        
        # import test data and convert to 2d lists
        wb = openpyxl.load_workbook( 'Input Files/Test Data.xlsx' )
        cadetAnswersA = self.FromExcelToList( wb.get_sheet_by_name('TEST A') )
        cadetAnswersB = self.FromExcelToList( wb.get_sheet_by_name('TEST B') )
        cadetAnswersC = self.FromExcelToList( wb.get_sheet_by_name('TEST C') )
        
        # create 'code names' {real name: code name} for everyone
        self.CreateCodeNames()
        
        
        # write results to a CSV file && track growth
        self.CalculateAndCombine(cadetAnswersA, correctAnswersA, 'A')
        self.CalculateAndCombine(cadetAnswersB, correctAnswersB, 'B')
        self.CalculateAndCombine(cadetAnswersC, correctAnswersC, 'C')
        
        self.SaveScores(isMasked)
        
        self.CalculateGrowth()
        
        self.SaveGrowth(isMasked)
        
        self.SaveItemDifficulty()
        
        #self.ReMapAnswers(correctAnswersA, 'A')
        
        print("...Statistics Calculated", end='\n\n\n')
    
    
    
    # This function does most the heavy lifting!
    def CalculateAndCombine( self, cadetTests, testAnswers, whichTest ):
        """ takes in: 2D list (Test Data.xlsx) and hashmap (Answer Key.xlsx)
            calculates Test_Scores & Item_Difficulty
            updates mTests, mGrowth, & mItemDifficulty
        """
    
        testStats = []
        itemDifficulty = [0]*18 # initialize with 18 zeros
        students = 0
        session = 'k'
        group_num = 1
        
        # score, add to CSV, update mGrowth dict
        for row in cadetTests:
            
            # first thing: ignore all the people who didn't take the test
            if row[2] == 'NA':
                continue
            
            # Record Item Difficulty (percent of participants who answered question correctly)
            # && reset variables, before switching to new session/group
            this_group = int(row[1])
            if this_group != group_num and this_group is not 2:
                
                if this_group is 3:
                    header = [whichTest, session, 'EXP', students]
                    testStats.append(header)
                else:
                    header = [whichTest, session, 'CNTRL', students]
                    testStats.append(header)
                
                for item in range(  len(itemDifficulty) ):
                    itemDifficulty[item] = float( "%.2f" % round( (itemDifficulty[item]/students)*100, 2 ) )
                testStats.append(itemDifficulty)    
            
                self.mItemDifficulty.append(testStats)
                #print2D(testStats)
                
                # reset stats
                testStats = []
                itemDifficulty = [0]*18 # initialize with 18 zeros
                students = 0
            
            # start initializing variables
            students += 1 
            score = 18
            gradedTest = []
            
            
            # check if cadet exists in Growth Hashmap
            cadetName = row[4] # key
            scores = [] # value
            if cadetName in self.mGrowth.keys():
                scores = self.mGrowth[cadetName] 
            else:
                scores = ['']*16 # initialize value  
            
            
            # SCORE TESTS: only iterate through test responses
            pal3KC_score = []
            nonpal3_score = []
            for col in range( 5, (len(row)-1) ): # Skip over 'Notes' column
                
                cadetAnswer = row[col]
                testAnswer = testAnswers[col - 4]   # question number = col-4
                isCorrect = 0 # initialize to false
    
                # record if answer incorrect
                if cadetAnswer != testAnswer:
                    score -= 1
                    gradedTest.append(0)
                else:
                    gradedTest.append(1)
                    itemDifficulty[col-5] += 1 # question number index = col-5
                    isCorrect = 1 # change to true
                    
                    
                # Add to KC arrays 
                if self.kcMaps[whichTest][col-4][0] != 'PAL3': # question number = col-4
                    nonpal3_score.append(isCorrect)
                else:
                    pal3KC_score.append(isCorrect)
                    
    
            # insert Test letter just before Test answers
            row.insert(5, whichTest)
            
            
            session = row[0][0] # take first letter of session string
            group_num = int(row[1])  
    
    
            # update value in Growth dictionary          
            non_pal3_grade = float("%.2f" % round(mean(nonpal3_score)*100, 2))
            pal3_kc_grade = float("%.2f" % round(mean(pal3KC_score)*100, 2))
            grade = float( "%.2f" % round((score/18)*100, 2) )
    
            if session == 'k':
                scores[0] = group_num # add group number to value of dict
                scores[1:4] = [non_pal3_grade, pal3_kc_grade, grade]
            elif session == 'm':
                scores[4:7] = [non_pal3_grade, pal3_kc_grade, grade]
            else:
                scores[7:10] = [non_pal3_grade, pal3_kc_grade, grade]
    
            self.mGrowth.update({cadetName: scores})
            
            
            # copy over KC && test scores
            gradedTest.extend(( score, non_pal3_grade, pal3_kc_grade, grade ))
            
            
            # Insert Graded_Tests before Notes
            row[24:24] = gradedTest
            self.mTests.append(row)
        
        
        # before leaving function -> record [ <test>, 'f', 3, <# of students>]
        header = [whichTest, session, 'CNTRL', students]
        testStats.append(header)
        
        for item in range(  len(itemDifficulty) ):
            itemDifficulty[item] = float( "%.2f" % round( (itemDifficulty[item]/students)*100, 2 ) )
        testStats.append(itemDifficulty)    
    
        self.mItemDifficulty.append(testStats)
        #print2D(testStats)
        
        
    
    # I could only find an overly complicated process that produced a
    # reversible short hash, so I opted for a simple random function
    def CreateCodeNames(self):
        """ Randomly generate len(8) only letters and digits for EVERYONE who 
            participated (even those who dropped out) - should only be generated once 
        """    
            
        # If code names already exist -> upload them to dictionary
        if Path(os.getcwd()+'\Input Files/Code_Names.csv').is_file():
            reader = csv.reader( open('Input Files/Code_Names.csv') ) 
            
            for row in reader:
                self.codeNames.update( {row[0] : row[1]} )
            
        # Else, generate and save
        else: 
            writer = csv.writer( open('Input Files/Code_Names.csv', 'w', newline='') )
            alphabet = string.ascii_letters + string.digits
            codes = set()
            
            # Give each participant a code_name
            for name in self.codeNames:
                
                # generate unique ID
                id = ''.join( random.choice(alphabet) for i in range(8) )
                if id in codes:
                    id = ''.join( random.choice(alphabet) for i in range(8) )
                
                # update code_base, assign code_name, & save to CSV file
                codes.add(id)
                self.codeNames.update( {name : id} )
                writer.writerow([name,id])
        
        
    
    def AnswerKey(self, worksheet ):
        """ takes in: Excel worksheet
            creates: questionMaps{}
            returns: hashmap of correct answers 
        """
        
        questions = {}
        answers = {}
        worksheetAsList = list( worksheet ) # must convert excel worksheet to 2Dlist in order to narrow iterable rows
        
        for row in worksheetAsList[1:19]: # 'for-each' through pertinent rows of excel file
            
            # first map 'new_question_number' to 'original_question_number'
            questions.update( {int(row[2].value) : int(row[1].value)} )
            
            for col in range(3, 7):  # only iterate through the four answer options (need to access by index)
                
                key = row[2].value  # question Number
                if row[col].value == 1:   # correct answer is column number containing '1'
                    answers.update( {int(key) : (col-2)} )   # col 3 is question 1 (and so on)
                    
        
        # update 
        self.questionMaps.update( {str(worksheet)[17] : questions} )
        # print answer_key 
    #     for k,v in answers.items():
    #          print(k,v)
        return answers
    
    

    def MapKC(self):
        """ Grabs orig question num and KC info from 'Item Difficulty_Growth'
            uses questionMaps{} to convert orig num to question num on tests given to participants
            creates map of { altered_num : [ KC_Source, KC ] }
            returns: rev_questionMap = { orig_question# : test_question# }
        """        
        #printdict(questionMaps)
        
        # reverse 2D map
        rev_questionMap = {}
        for key in self.questionMaps.keys():
            inv_map = { v: k for k, v in self.questionMaps[key].items()}
            rev_questionMap.update( {key : inv_map} )
        #printdict(rev_questionMap)
        
        reader = csv.reader(open('Input Files/Item Difficulty_Growth.csv')) 
        
        for row in reader:
            
            if len(row[0]) > 1: # skip header
                continue;
            
            if row[0] == '': # break when reaching end of data
                break;
    
            newNum = rev_questionMap[row[0]][int(row[4])]
                     
            self.kcMaps[row[0]].update( { newNum : [row[2],row[3]] } )
                
        #printdict(kcMaps)
        return rev_questionMap
    
        

    def FromExcelToList( self, worksheet ):
        """ takes in: an excel worksheet (Test Data.xlsx)
            returns: worksheet as a 2D list
            ignores participants who dropped out
        """
        
		# list of participants that dropped out
        removeParticipants = ['Jane Doe', 'John Smith' ]
    
        masterData = []                     # initialize 2D list
        worksheetAsList = list( worksheet ) # must convert worksheet to 2Dlist in order to narrow iterable rows
        
        for row in worksheetAsList[1:]:     # skipping the header
            
            name = row[4].value
            
            if name == None:    # break after reaching a row without content
                break                   # MUST use '.value' to access content of worksheet
            
            # add 'real_name' to database 
            if name not in self.codeNames:
                self.codeNames.update( {name : ''} )
            
            # don't copy over participants that dropped out
    #         for word in removeParticipants:
    #             if word in name:
            if any( word in name for word in removeParticipants ):
                continue
                    
            
            data = []                       # initialize 1D list
            for cell in row[:(ord('Y')-ord('A'))]:  # no pertinent info after column 'X'
                data.append(cell.value)
                
            masterData.append(data)         # add 1D list to list of lists
            
            
        return masterData
    
    
    
    def qa( self, dictionary ):
        """  check if missing any tests -> print's name of person missing test """
        
        printdict(self.mGrowth)
        
        for k,v in dictionary.items():
            count = 0
            for i in v:
                if i == '':
                    count += 1
            if count > 6:   # growth columns should be blank
                print(k, end='\n\n')
                
            
    
    def SaveScores(self, mask):
        """ De-Identifies names (from Test Data.xlsx), 
            writes all test scores to CSV, along with test stats
        """
        
        writer = csv.writer( open('Output Files/Test_Results.csv', 'w', newline='') ) # windows format for opening a writable CSV
        
        # write header
        header = ['Session', 'Group', 'Date', 'Online?', 'Name', 'Test']
        for i in range(1, 19):  # answer
            header.append('A' + str(i))         #like 'push' or 'add'
        for i in range(1, 19):  # correct?
            header.append('C' + str(i))
        header.extend(('Total Correct Answers', 'KC_NON-PAL3 (%)', 'KC_PAL3 (%)', 'Total Score (%)', 'Notes:'))   # 'push' multiple items in a single line 
        writer.writerow(header)
        
        # remove time from dates
        for row in self.mTests:
            row[2] = row[2].date()
        
        # De-Identify
        if mask is True:
            for row in self.mTests:
                
                row[4] = self.codeNames[row[4]]
        
        # sort by name, then session
        self.mTests.sort(key=itemgetter(4, 0))
        
        #save
        for row in self.mTests:
            writer.writerow(row)
            
            
    
    def CalculateGrowth(self):
        """ calculates 'growth_per_category per session' & 'overall_growth' for each student
            adds values to end of dictionary value array
        """
        
        #printdict(mGrowth)
        
        for k,v in self.mGrowth.items():
            
            # calculate mid_test growth
            # skip all the people who didn't take the test
            if v[6] is not '':
                
                for i in range(1, 4):
                    v[i+9] = float("%.2f" % round(v[i+3]-v[i], 2))
            
            else: # else replace empty test_scores & growth with 'NA'
                v[4:7] = ['NA']*3
                v[10:13] = ['NA']*3
            
            
            # calculate final_test growth
            if v[9] is not '':
                
                for i in range(1, 4):  
                    v[i+12] = float("%.2f" % round(v[i+6]-v[i], 2)) 
                
            else:
                v[7:10] = ['NA']*3
                v[13:16] = ['NA']*3
            
            # udpate dict
            self.mGrowth.update({ k : v })
            
    
    
    def SaveGrowth( self, mask ):
        """ takes in: 2D array
            De-Identifies names
            writes to CSV file
        """
        
        writer = csv.writer( open('Output Files/Growth_Stats.csv', 'w', newline='') ) # windows format for opening a writable CSV
    
        #header
        writer.writerow(['Name', 'Group', 'K_Non_PAL3 Score (%)', 'K_PAL3 Score (%)', 'K_AVG Score (%)', 
                         'M_Non_PAL3 Score (%)', 'M_PAL3 Score (%)', 'M_AVG Score (%)', 'F_Non_PAL3 Score (%)', 
                         'F_PAL3 Score (%)', 'F_AVG Score (%)', 'Mid_Growth_Non_PAL3', 'Mid_Growth_PAL3', 
                         'Mid_Growth_AVG', 'F_Growth_Non_PAL3', 'F_Growth_PAL3', 'F_Growth_AVG'])
        
        
        
        # sort by highest growth (users with same growth in descending alphabetical order)
        ##growth = sorted( mGrowth.items(), key=lambda d: ( (d[1][6], d[0]) if d[1][6] is not '' else (-float('inf'), d[0]) ), reverse=True )
        
        # first, sort by name (so users with same growth in alphabetical order) 
        growth = sorted( self.mGrowth.items() )
        
        # then, sort by highest growth magnitude
        ## if dic[1][6] is float:
        ##     return dic[1][6]
        ## else:
        ##     return -float('inf')
        growth = sorted( growth, key=lambda dic: (dic[1][15] if type(dic[1][15]) is float else -float('inf')), reverse=True )
        
        #print2D(growth)
        for row in growth:
            
            newrow = []
            if mask is True: # replace name with code_name
                newrow = [ self.codeNames[row[0]] ]
            else: # dont
                newrow = [row[0]]
                
            newrow.extend(row[1]) # combine array of values into array with name
            writer.writerow( newrow )
        
        

    def SaveItemDifficulty(self):
        """ will rearrange questions back to their original order
            and save to a CSV file
        """
        #printdict(questionMaps)
        
        # first, reorder questions to original order
        origOrder = []
        for groupResults in self.mItemDifficulty:
            
            test_letter = groupResults[0][0]
            temp = [0]*18
            
            for index in range(18):
                
                altered_num = index+1
                orig_num = self.questionMaps[test_letter][altered_num]
                #print(altered_num, ":", orig_num)
                
                temp[orig_num-1] = groupResults[1][index]
            
            temp.insert(0, str(groupResults[0]))
            origOrder.append(temp)
        
        # group by experiment/ control
        origOrder = sorted(origOrder, key=lambda a: a[0][13], reverse=True)
        
        # calculate mid, final, & avg growth per test
        allGrowths =[]
        for i in range(6):
            
            growths = [['mid growth'], ['final growth'], ['avg growth']]
            for j in range(len(origOrder[0])-1):
                mid = origOrder[(i*3)+1][j+1] - origOrder[(i*3)][j+1]
                final = origOrder[(i*3)+2][j+1] - origOrder[(i*3)][j+1]
                #print(growths[0], mid, final)
                growths[2].append(float("%.2f" % round(((mid+final)/2), 2)) )
                growths[0].append(float("%.2f" % round(mid, 2)) )
                growths[1].append(float("%.2f" % round(final, 2)) )
            allGrowths.append(growths)
        
        # add growths next to their corresponding test sets
        for i in range(1,7):
            for j in range(3):
                index = (3*i) + (3*(i-1)) +j
                origOrder.insert(index, allGrowths[i-1][j] )
                
        
        # transpose
        #print2D(origOrder)
        origOrder = list(map(list, zip(*origOrder)))
        #print2D(origOrder)
        
        # alright, now you can save it externally
        writer = csv.writer( open('Output Files/Item_Difficulty.csv', 'w', newline='') ) # windows format for opening a writable CSV
        for row in origOrder:
            writer.writerow( row )
    
    
    
    def ReMapAnswers(self, answerKey, whichTest):
        """ map correct answers back to original questions """
        
        origAnswerMap = {}
        for k,v in self.answerKey.items():
            origAnswerMap.update( {self.questionMaps[whichTest][k] : v} )  
            
        for k,v in origAnswerMap.items():
            print(k,v)
    
    
    
    
    
    
