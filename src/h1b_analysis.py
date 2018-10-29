# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:59:03 2018

@author: Siva
"""
import sys


class ReadRecord: #reading and parsing each record
    def __init__(self,recordstring,case_number_idx,status_idx,soc_name_idx,state_idx):
        self.parse_record(recordstring,case_number_idx,status_idx,soc_name_idx,state_idx)
    def parse_record(self,recordstring,case_number_idx,status_idx,soc_name_idx,state_idx):
        splits = recordstring.split(";")
        self.occupation = splits[soc_name_idx].strip().strip('\"')
        self.state = splits[state_idx].strip()
        if splits[status_idx] == "CERTIFIED":
            self.certified = True
        else:
            self.certified = False
            
            
        

class Solution(object):
    def __init__(self):
        self.state_summary = {}
        self.occupation_summary = {}
        self.certified_count = 0
        
    
    def record_summary(self,input_record): #creating dictionaries with occupation and state counts.
    
        if input_record.occupation in self.occupation_summary: #incrementing occupation count if at is already seen
            self.occupation_summary[input_record.occupation] += 1
        else:
            self.occupation_summary[input_record.occupation] = 1 #creating new occupation record in dictionary 
                                   
        if input_record.state in self.state_summary: #incrementing state count if at is already seen
            self.state_summary[input_record.state] += 1
        else:
            self.state_summary[input_record.state] = 1 #creating new state record in dictionary 
        self.certified_count += 1
    
    def write_top_occupations(self,occ_path):
        #sorting the occupations by count descending order and  name ascending order
        top_occupations = sorted(self.occupation_summary.items(), key = lambda x: (-x[1],x[0]), reverse = False)[:10] #taking only top 10
        occ_optxt=open(occ_path,"w")#open output occupation file
        occ_header = "TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE"              
        occ_optxt.write(occ_header+"\n") #writing header
        
        for x in top_occupations: #writing data
            occ_op_row = "{};{};{}{}".format(x[0], str(x[1]), str(round(float(x[1]*100/self.certified_count),1)),"%") #formatting output
            occ_optxt.write(occ_op_row+"\n")
        occ_optxt.close()
        
    def write_top_states(self,state_path):
        #sorting the states by count descending order and  name ascending order
        top_states = sorted(self.state_summary.items(), key = lambda x: (-x[1],x[0]), reverse = False)[:10] #taking top 10
        state_optxt=open(state_path,"w") #open output stats file
        state_header = "TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE"              
        state_optxt.write(state_header+"\n") #writing header
        
        for x in top_states: #writing data
            state_op_row = "{};{};{}{}".format(x[0], str(x[1]), str(round(float(x[1]*100/self.certified_count),1)),"%") #formmating state data
            state_optxt.write(state_op_row+"\n")
        state_optxt.close()

    def run(self):
        argv = sys.argv #reading input arguments
        
        try: #validating input arguments
            h1b_file_path = argv[1]
            occ_file_path = argv[2]
            state_file_path = argv[3]
        except:
            print("Wrong input arguments passed")
            return    
        
        
        try: #validating input file
            with open(h1b_file_path,encoding="utf8",mode = "r") as f:#Read each line of i/p  file
                header = f.readline().split(";") #reading  header
                for i,value in enumerate(header): #finding index for interested columns. 
                    if (value == "LCA_CASE_NUMBER" or value == "CASE_NUMBER"):
                        case_number_idx = i
                    if (value == "STATUS" or value == "CASE_STATUS"):
                        status_idx = i
                    if (value == "LCA_CASE_SOC_NAME" or value =="SOC_NAME" ):
                        soc_name_idx = i
                    if (value == "WORKSITE_STATE" or value == "LCA_CASE_WORKLOC1_STATE"):
                        state_idx = i
                        
                for line in f: 
                    #reading and parsing input row
                    input_record = ReadRecord(line,case_number_idx,status_idx,soc_name_idx,state_idx)
                    if input_record.certified: #processing only certified applications
                        self.record_summary(input_record)
        except: #validating input file
            print("Error reading file " + h1b_file_path)
            return                              

        self.write_top_occupations(occ_file_path) #creating ouput file with top 10 occupations
        self.write_top_states(state_file_path) #creating ouput file with top 10 states
                

if __name__ == '__main__':
    Solution().run()
    