#===============================================================================
#   Takes in 2 CSV files:
#        'Item_Difficulty' = Growth per Item per Session for EXP & CNTR
#        'Item Difficulty_Growth' = same as Item_Difficulty, just different format
#        
#   Exports 3 CSV files:
#        'Item Difficulty_Growth' = updated if values changed from 'calculateStatistics' class
#        'Category_Growth' = overall Growth per 'KC' per Session for EXP, CNTRL, & BOTH
#        'KC_Difficulty_Question_Mappings' = maps difficulty for each KC
#===============================================================================

import csv
import statistics
import openpyxl
from calculateStatistics import CalculateStatistics as cs
from operator import itemgetter


def print2D( arrays ):
    """ cleaner format for displaying 'list of lists' """
    for array in arrays:
        print(array)
    print()


def print4Ddict( dictionary ):
    """ cleaner format for displaying multi-layered maps """
    for k, v in dictionary.items():
        print(k)
        for kc in v.items():
            print(kc)
    print()
    

def print4D( arrays ):
    """ cleaner format for displaying multi-layered lists """
    for array in arrays:
        print(array[0])
        
        for aa in array[1:]:
            for a in aa:
                print(a)
    print()



class CategoryStats:
    """ Uses data calculated from 'caclulatteStatistics.py' to calculate 
        Growth for each KC
    """
    
    def __init__(self):
        """ mCategories = { Group : (KC, [#items, Score, StdDev, Growth]) } 
            rquestionMaps = map of { orig_question# : new_question# } 
            kcDiffMaps = multi-Dimensional array to hold data for 'KC_Difficulty_Question_Mappings.csv'
        """
        self.mCategories = {}
        self.rquestionMaps = {}
        self.kcDiffMaps = []



    def Run(self):
        """ Main """
        
        print("Analyzing Categories...", end='\n\n')
        
        self.updateItemDifficulty()
        
        self.createQuestionMaps()
        self.calculateKCdifficulty()
        self.saveKCdifficulty()
        
        self.calculateRawData( csv.reader(open('Input Files/Item Difficulty_Growth.csv')) )
        
        self.calculateStats()
        
        self.saveStats()
        
        
        print("...Categories Analysed", end='\n\n\n')
        
        
    
    def createQuestionMaps(self):
        """ creates map of { orig_question# : new_question# } 
            by using methods from calculateStatistics.py
            purpose: helper method for creating 'KC_Difficulty_Question_Mappings.csv'
        """
        wb = openpyxl.load_workbook( 'Input Files/PAL3 Answer Key.xlsx' )
        x = cs()
        x.AnswerKey( wb.get_sheet_by_name('Test A') )
        x.AnswerKey( wb.get_sheet_by_name('Test B') )
        x.AnswerKey( wb.get_sheet_by_name('Test C') )
        self.rquestionMaps = x.MapKC()
        
        
    
    def calculateKCdifficulty(self):
        """ creates 'kcDiffMaps' from updated 'Item_Difficulty_Growth.csv' """
        
        reader = list(csv.reader(open('Input Files/Item Difficulty_Growth.csv')))
        
        
        for row in reader[1:]:
            
            del row[10:13] # del growth for EXP
            del row[13:16] # del growth for CNTRL
            
            # calculate KC difficulty across ALL groups
            for i in range(3):
                mean = ( float(row[7+i])+float(row[10+i]) )/2
                row.append( "%.2f" % round(mean,2) )
            
            # insert test_question_num
            row.insert(1, self.rquestionMaps[row[0]][int(row[4])]) 
            
            self.kcDiffMaps.append(row)
        
        
    
    def saveKCdifficulty(self):
        """ save to external CSV file"""
        
        writer = csv.writer( open('Output Files/KC_Difficulty_Question_Mappings.csv', 'w', newline='') )
        
        writer.writerow([ 'Test Letter', 'Test Question #', 'Question (text)', 'Source', 
                  'KC', 'Original Question #', 'Answer #', 'Answer (text)', 
                  "['k', 'EXP'] (%)", "['m', 'EXP']  (%)", "['f', 'EXP']  (%)", 
                  "['k', 'CNTRL']  (%)", "['m', 'CNTRL']  (%)", "['f', 'CNTRL']  (%)", 
                  "['k', 'ALL']  (%)", "['m', 'ALL']  (%)", "['f', 'ALL']  (%)"])
        
        
        self.kcDiffMaps.sort(key=itemgetter(0,1))
        
        for row in self.kcDiffMaps:
            writer.writerow(row)
            
        
    
    def updateItemDifficulty(self):
        """ updates growth stats per category from item_difficulty.csv to item difficulty_growth.csv
        """
        
        orig_reader = list(csv.reader(open('Input Files/Item Difficulty_Growth.csv')))
        update_reader = list(csv.reader(open('Output Files/Item_Difficulty.csv')))[1:]
        
        updated = orig_reader[:1] # initialize with header
        
        
        # copy over KC data
        for row in orig_reader[1:]:
            updated.append(row[:7])
        
        
        # copy over updated growth
        # in the original format of 'item Difficulty_growth.csv'
        for i in range(3):
            for j in range(len(update_reader)): #len(update_reader) == 18 rows
                it = 6*i
                updated[(18*i+1)+j].extend( update_reader[j][(0+it):(6+it)] + update_reader[j][(18+it):(24+it)] )
                
        
        # save updated data
        writer = csv.writer( open('Input Files/Item Difficulty_Growth.csv', 'w', newline='') )
        for row in updated:
            writer.writerow(row)
            
        
    
    def calculateRawData(self, reader):
        """ takes in: CSV file
            calculates raw scores for each category
            updates 'mCategories' dictionary
        """
    
        # initialize Master_Category_Data
        categories = ['All_Categories', 'All_PAL3', 'Non-PAL3 (NEET/CET/Other)', 'Capacitor Behavior', 
                      'Diode Behavior-Reverse', 'Full Wave Rectifier Behavior', 
                      'Inductor Behavior', "Kirchoff's Current Law", "Ohm’s Law: Voltage", 
                      'RC Input Filter Behavior', 'Transistor Behavior', 'Zener Diode Behavior']
        for i in range(3):
            dic = {}
            for cat in categories:
                dic.update( { cat :[0,[],[],[],0,0,0,0,0,0,0,0,0] } )
            if i is 0:
                self.mCategories.update( { 'EXP' : dic } )
            elif i is 1:
                self.mCategories.update( { 'CNTRL' : dic } )
            else:
                self.mCategories.update( { 'TOTAL' : dic } )
        
    
        
        # Fill dictionary values
        for row in list(reader)[1:]: # skip header
            
            # Break when reaches row without data
            if row[0] is '': 
                break
                
    
            for key in self.mCategories.keys(): # for each group  
                
                # gather all info into their corresponding dictionary values
                kC = ''
                if row[2] != 'PAL3':
                    kC = 'Non-PAL3 (NEET/CET/Other)'
                else:
                    kC = row[3]
                    self.mCategories[key]['All_PAL3'][0] += 1
                
                # n_items count
                self.mCategories[key][kC][0] += 1 # update KC
                self.mCategories[key]['All_Categories'][0] += 1 # update ALL
                
                
                # Iterate through EXP & CNTRL values simultaneously
                for i in range(1,4):
                    
                    
                    # Update EXP 
                    if key is 'EXP':
                        self.mCategories[key][kC][i].append( float(row[6+i]) )  # update KC
                        
                        self.mCategories[key]['All_Categories'][i].append( float(row[6+i]) ) # update ALL
                        
                        if kC is not 'Non-PAL3 (NEET/CET/Other)':
                            self.mCategories[key]['All_PAL3'][i].append( float(row[6+i]) ) # update ALL_PAL3
                    
                    # Update CNTRL
                    elif key is 'CNTRL':
                        
                        self.mCategories[key][kC][i].append( float(row[12+i]) ) # update KC
                        
                        self.mCategories[key]['All_Categories'][i].append( float(row[12+i]) ) # update ALL
                        
                        if kC is not 'Non-PAL3 (NEET/CET/Other)':
                            self.mCategories[key]['All_PAL3'][i].append( float(row[12+i]) ) # update ALL_PAL3
                           
                    # Update TOTAL
                    else:
                        self.mCategories[key][kC][i].extend(( float(row[6+i]), float(row[12+i]) ))  # update KC
                        
                        self.mCategories[key]['All_Categories'][i].extend(( float(row[6+i]), float(row[12+i]) )) # update ALL
                        
                        if kC is not 'Non-PAL3 (NEET/CET/Other)':
                            self.mCategories[key]['All_PAL3'][i].extend(( float(row[6+i]), float(row[12+i]) )) # update ALL_PAL3
                    
#         print("///  RAW DATA  ///")
#         print4Ddict(self.mCategories)
        
        
    
    def calculateStats(self):
        """ Iterates through Master_Dictionary
            Calculates Std-Dev & Growth
        """
        
        for key in self.mCategories.keys():
            
            for category in self.mCategories[key].keys():
                
                # Calculate Avg Score && Std Dev
                for i in range(1,4):
                    self.mCategories[key][category][i+3] = float( "%.2f" % round( statistics.mean(self.mCategories[key][category][i]), 2))
                    self.mCategories[key][category][i+6] = float( "%.2f" % round( statistics.pstdev(self.mCategories[key][category][i]), 2))
                      
                # Delete list of item_difficulties after stats calculated 
                del self.mCategories[key][category][1:4] 
                
                
                # Calculate Growth
                for i in range(7,9):
                    k_score = self.mCategories[key][category][1]
                    self.mCategories[key][category][i] =  float( "%.2f" % round( (self.mCategories[key][category][i-5] - k_score), 2))
                    
                # Calculate Avg Growth
                self.mCategories[key][category][9] = float( "%.2f" % round( statistics.mean(self.mCategories[key][category][7:9]), 2))
        
#         print("///  STATS CALCULATED  ///")
#         print4Ddict(self.mCategories)
    
    
    
    def convert(self):
        """ converts 4-D nested dictionary to multi-dimentional list """
        
        sortedMaster = []
        # sort by 'n_items'
        for key in self.mCategories.keys():
            sortedInner = [key]
            sortedInner.append(sorted( self.mCategories[key].items(), key=lambda d: d[1][0], reverse=True ))
            sortedMaster.append(sortedInner)
        
        # then sort by 'group'
        ssMaster = sorted( sortedMaster, key=lambda m: (len(m[0]), m[0]) ) 
    
#         print("///  SORTED DATA  ///")
#         print4D(ssMaster)
        return(ssMaster)
            
            
    
    def saveStats(self):
        """ Saves the global dictionary to CSV file """
        
        writer = csv.writer( open('Output Files/Category_Growth.csv', 'w', newline='') )
        
        # HEADER
        writer.writerow(['Category', "'n' items", 'Kickoff Score (%)', 'Mid Score (%)', 'Final Score (%)', 
                         'StdDev_k (%)', 'StdDev_m (%)', 'StdDev_f (%)', 'growth_M', 'growth_F', 'growth_AVG'])
        
        
        # sort by 'group' -> then by 'n_items'
        mc = self.convert()
        
        # for every group
        for group in mc:
            
            writer.writerow( [group[0]] ) # record group
            
            # for every tuple (kc, stats)
            for kc in group[1]:
                
                # combine into single array
                list = [kc[0]]
                list.extend(kc[1])
                
                writer.writerow(list) # and record
                    
        
    
    
    
    
    
