#===============================================================================
#  This class is totally optional, 
#    in case you want to trace the data back to it's corresponding cadet
#
#  Takes in 2 CSV files:
#        'Test_Results' = participant Scores by Item
#        'Growth_Stats' = participant Growth by Session
#        
#   Exports 2 CSV files:
#        'Test_Results_Unmasked'
#        'Growth_Stats_Unmasked'
#===============================================================================
import csv
    

class ReIdentify:
    """ Replaces all De-Identified participant names with their REAL names """
    
    
    def __init__(self):
        """ codeNames = map of de-identified names and real names {real_name: code_name} """
        self.codeNames = {}
    
    

    def LoadCodeNames(self):
        """ Load up the map of { De-Identified Names : Real Names} """
        
        reader = csv.reader( open('Input Files/Code_Names.csv') ) 
        
        for row in reader:
            self.codeNames.update( {row[0] : row[1]} )
            
            

    def unmask(self):
        """ Does the UnMasking for both files """
        
        print("Re-Identifying Data...", end='\n\n')
        
        self.LoadCodeNames()
        
        greader = list( csv.reader( open('Output Files/Growth_Stats.csv') ) )
        gwriter = csv.writer( open('Output Files/Growth_Stats_Unmasked.csv', 'w', newline='') )
        treader = list( csv.reader( open('Output Files/Test_Results.csv') ) )
        twriter = csv.writer( open('Output Files/Test_Results_Unmasked.csv', 'w', newline='') )
        
        
        # remap {codenames : realname}
        rev_codenames = { v: k for k, v in self.codeNames.items()}
        
        
        # check if data already de-identified
        if greader[1][0] not in rev_codenames:
            print("...Data NOT De-Identified!")
            return
        
        
        # copy over header
        gwriter.writerow(greader[0])
        twriter.writerow(treader[0])
        
        # replace De-Identified name with Code_Name
        # && rewrite to CSV file
        for row in greader[1:]:
            row[0] = rev_codenames[row[0]]
            gwriter.writerow(row)
            
        for row in treader[1:]:
            row[4] = rev_codenames[row[4]]
            twriter.writerow(row)
        
        
        print("...Data Re-Identified", end='\n\n\n')
        
        
        
        
        