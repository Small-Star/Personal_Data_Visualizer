import datetime
from goal_node_lib import *
from body_node_lib import *


class day_node():
    def __init__(self, date=datetime.date(1001,1,1)):
        self.date = date
        self.calorie_intake = 0
        self.protein_intake = 0
        self.tdee = 0
        self.weight = 0
                
        self.fic = 'N'  #Food Intake Cycle (i.e. bulk, cut, maintainence)
        
        self.goals = [] #List of goal nodes
        
        self.records = [] #List of strings (i.e. records)
        
        self.bnode = body_node()
        
        self.mood = (('','',''),('','',''))   #((AL,AH,AS),(VL,VH,VS))

        
    def get_date(self):
        return self.date #Datetime format
    def get_calorie_intake(self):
        return self.calorie_intake
    def get_protein_intake(self):
        return self.protein_intake
    def get_tdee(self):
        return self.tdee
    def get_weight(self):
        return self.weight
    def get_fic(self):
        return self.fic
    def get_bnode(self):
        return self.bnode
    def get_goals(self):
        return self.goals
    def get_num_goals(self):
        return len(self.goals)
    def get_goals_of_status(self,status):
        g_list = []
        for g in self.goals:
            if g.get_status() == status:
                g_list.append(g)
        return g_list                
    def get_mood(self):
        return self.mood
    
    def set_date(self,date):
        self.date = date
    def set_calorie_intake(self, calorie_intake):
        self.calorie_intake = calorie_intake
    def set_protein_intake(self, protein_intake):
        self.protein_intake = protein_intake
    def set_tdee(self, tdee):
        self.tdee = tdee
    def set_weight(self, weight):
        self.weight = weight
    def set_fic(self, fic):
        self.fic = fic
    def set_bnode(self, bnode):
        self.bnode = bnode
    def add_goal(self, goal):
        self.goals.append(goal)
    def add_record(self, record):
        self.records.append(record)
    def set_mood(self, mood):
        self.mood = mood
        
    def text_rep(self):
        s =  "Date: " + str(self.date) + "\n" + \
            "Calories: " + str(self.calorie_intake) + "\n" + \
            "Protein : " + str(self.protein_intake) + "\n" + \
            "TDEE : " + str(self.tdee) + "\n" + \
            "FIC: " + str(self.fic) + "\n" + \
            "Weight: " + str(self.weight) + "\n" + \
            "-----------------------------\n"
            
        for g in self.goals:
            s += g.__str__()
            
        s += "-----------------------------\n"
            
        for r in self.records:
            s += r + "\n"
            
        return s
            
            