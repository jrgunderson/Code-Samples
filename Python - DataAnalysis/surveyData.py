#===============================================================================
#   Takes in Excel File 'Test Data'
#   Exports CSV File 'Survey_Results', 'Post_Surveys', & 'Pre_Surveys'
#===============================================================================

import csv
import openpyxl
from collections import Counter
from nltk import WordNetLemmatizer
from nltk import SnowballStemmer
import string
#from PyDictionary import PyDictionary


def print2D( arrays ):
    """ cleaner format for displaying 'list of lists' """
    
    for array in arrays:
        print(array)
    print()



class SurveyData:
    """ Calculates Avg Score & Word Counts from Surveys 
        filled out by 'PAL3 users'
    """
    
    def __init__(self):
        """ mResults = avg scores and word counts derived from raw survey data
            codeNames = map of de-identified names and real names {real_name: code_name}
            rawData = All Post Survey answers
        """
        self.mResults = []
        self.codeNames = {}
        self.rawData = []
        


    def Run(self):
        """ MAIN """
        
        print("Analyzing Survey Data...", end='\n\n')
    
        wb = openpyxl.load_workbook( 'Input Files/Test Data.xlsx' )
        surveys = self.FromExcelToList( wb.get_sheet_by_name('POST-SURVEY') )
        
        self.combineSurveys(wb.get_sheet_by_name('POST-SURVEY CONTROL'))
        self.savePostSurveys()
        
        self.preSurveys(wb.get_sheet_by_name('PRE-SURVEY'))
        
        # print2D(surveys)
        # print2D(map(list, zip(*surveys))) # print a transposed 2D List
        self.analyze(surveys)
        
        #print2D(self.mResults)
        self.save2CSV(self.mResults)
        
        print("...Survey Data Analyzed", end='\n\n\n')
        
    
    
    def preSurveys(self, worksheet):
        """ takes in: excel worksheet of pre-surveys
            de-identifies && saves externally to csv
        """
        writer = csv.writer( open('Output Files/Pre_Surveys.csv', 'w', newline='') )
        worksheetAsList = list(worksheet)
        
        for row in worksheetAsList:
            
            if row[0].value == None:
                break  
            
            
            if row is not worksheetAsList[0]:
                row[0].value = self.codeNames[row[0].value] # replace Real_Name with De_Identified_Name
                
            data = []                       
            for cell in row:
                data.append(cell.value)
                
            #print(data)
            try:
                writer.writerow(data)
            # some joker put in the pi symbol
            except UnicodeEncodeError:
                data[len(data)-1] = 'pi' 
                writer.writerow(data) 
        
        
    
    def combineSurveys(self, worksheet):
        """ takes in: Post-Survey data from Control
            combines Post-Survey data from PAL3 Users && Control
        """
        worksheetAsList = list( worksheet )
        
        for row in worksheetAsList[1:]:
            
            if row[0].value == None:
                break                   
            
            if row[8].value == 'NA': # skip over people who dropped out
                continue
    
            data = []           
            # copy over name && group            
            for cell in row[:2]:
                data.append(cell.value)
                
            data.append(0) # everyone who filled out this survey is in CNTRL group   
            data.extend(['']*67) # skip over questions CNTRL didn't have on survey 
            
            # copy over quantitative survey data
            for cell in row[2:8]:
                data.append(cell.value)
            
            data.extend(['']*2) # skip over questions CNTRL didn't have on survey
            
            # copy over qualitative survey data
            for cell in row[8:]:
                data.append(cell.value)
            
            self.rawData.append(data)
        #print2D(self.rawData)  
        
    
     
    def savePostSurveys(self):
        """ De-Identify and save Raw survey data to 'Post_Surveys.csv'
        """
        
        writer = csv.writer( open('Output Files/Post_Surveys.csv', 'w', newline='') )
        
        self.LoadCodeNames()
        
        for row in self.rawData[1:]: # no code-name in header
            row[0] = self.codeNames[row[0]] # replace Real_Name with De_Identified_Name
        
        
        # replace some header titles
        self.rawData[0][70] = self.rawData[0][70] +" / I prefer to study on a tablet."
        self.rawData[0][71] = self.rawData[0][71] +" / I prefer to study on a PC or laptop, if available."
        self.rawData[0][72] = self.rawData[0][72] +" / I studied alone, such as in my room."
        self.rawData[0][73] = self.rawData[0][73] +" / I studied in common areas."
        self.rawData[0][78] = self.rawData[0][78] +" / When and where do you typically study (e.g., after class during ATT/A-school, a refresher between A-School and C-School, in study groups, alone in your dorm, in common areas)?"
        
        #save
        for row in self.rawData:
            writer.writerow(row)
        
         
        
    def FromExcelToList( self, worksheet ):
        """ takes in: an excel worksheet
            *starts building 'rawData'
            returns: worksheet (without group# and participant name) as a 2D list
        """
    
        masterData = []                     # initialize 2D list
        worksheetAsList = list( worksheet ) # must convert worksheet to 2Dlist in order to narrow iterable rows
        
        # copy over header row to Master Results 2D List
        temp = []
        for cell in worksheetAsList[0][2:]: # only iterate through 1st row after 2nd cell
            temp.append(cell.value) # need to grab each cell by value
        self.mResults.append(temp)
        
        
        # copy over header to 'rawData'
        temp = []
        for cell in worksheetAsList[0]:
            temp.append(cell.value)
        temp.insert(2, 'Is EXP ?')
        self.rawData.append(temp)  
            
        
        # copy contents of worksheet into a seperate 2D List
        for row in worksheetAsList[1:]:     # skipping the header
            
            if row[0].value == None:    # break after reaching a row without content
                break                   
            
            if row[2].value == 'NA':    # skip over people who didn't fill it out
                continue
    
            # access data in worksheet and add to 2D list
            data = []                       
            for cell in row[2:]:            # Skip name & Group#
                data.append(cell.value)
                
            masterData.append(data) # add another list to 2D list
            
            
        # now do a slightly modified version for the 'rawData'
        exceptions = ["Smith, John", "Doe, Jane"]
        for row in worksheetAsList[1:]:
            
            if row[0].value == None:
                break                   
            
            # skip over people who dropped out... unless they just didn't fill out the survey
            if row[2].value == 'NA':
                if not any( row[0].value in name for name in exceptions ):
                    continue
    
            data = []                       
            for cell in row:
                data.append(cell.value)
            data.insert(2, 1) # everyone who filled out this survey is in EXP group   
            self.rawData.append(data)
        
        #print2D(self.rawData)    
        return masterData
    
    
    
    def analyze(self,surveys):
        """ This function counts the word frequency of the survey responses.
            input: 2D List of all survey data
            output: 2D List of calculated survey data results
        """
        
        # for stemming
        noPunctuation = str.maketrans('','', string.punctuation)
        unimportant = {'', 'na', 'a', 'i', 'of', 'to', 'the', 'and', 'but', 'as', 'it', 'or', 'in', 'wa',
                       'would', 'when', 'that', 'then', 'was', 'an'}
        
        # iterate through columns
        content = 0
        avgValues = []
        for column in map(list, zip(*surveys)): # transpose 2D List
            
            participants = avg = 0
            words = []
            
            try:
                content = int(column[0]) # to test which columns contain qualitative data
                
                # function to calculate avg score
                for cell in column:
                    if cell != 'NA':
                        participants += 1
                        avg += cell
                avg /= participants
                avgValues.append( float("%.2f" % round(avg,1)) )
            
            
            # if not numerical value
            except ValueError:
                
                # split all sentences into words  
                # -> add to array with all other words for that question
                for cell in column:
                    words.extend(cell.split())
                 
                # remove punctuation, convert to lower case, & stem each word
                for i in range(len(words)):
                    #print(words[i])
                    words[i] = words[i].lower().translate(noPunctuation)
                    words[i] = WordNetLemmatizer().lemmatize( words[i] )
                    words[i] = SnowballStemmer('english').stem( words[i] )
                    #print(words[i])
                
                    # combine similar words
    #                 if words[i] != 'na':
    #                     try:
    #                         synonym = PyDictionary().synonym( words[i] )
    #                         for s in synonym:
    #                             if s in words:
    #                                 print(words[i], s)
    #                                 words[i] = s
    #                     except (ValueError, TypeError):
    #                             print()
                
                # count frequency
                wordcount = Counter(words)
                
                # remove 'non_important' words
                for word in list(wordcount):
                    if word in unimportant:
                        del wordcount[word]
                
                avgValues.append(wordcount) 
                
        self.mResults.append(avgValues)
    
    
    
    def save2CSV(self,twoDlist):
        """ input: 2D list
            output: CSV file
        """
        writer = csv.writer( open('Output Files/Survey_Results.csv', 'w', newline='') ) # windows format for opening a writable CSV
        
        for row in twoDlist:
            writer.writerow(row)
        
    

    def LoadCodeNames(self):
        """  load codenames """
        
        reader = csv.reader( open('Input Files/Code_Names.csv') ) 
        
        for row in reader:
            self.codeNames.update( {row[0] : row[1]} )



