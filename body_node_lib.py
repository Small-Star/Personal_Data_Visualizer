'''
Created on Aug 16, 2015

@author: Administrator
'''

import datetime

class body_node(object):
    def __init__(self,creation_date = datetime.date(1,1,1)):
        self.creation_date = creation_date
        
        self.workout = workout_node()                    #Workout_node describing the day's workout, if any
        
        self.weight = 0
        self.bodyfat = 0
        
        self.calorie_intake = 0
        self.protein_intake = 0
        self.tdee = 0

    def set_creation_date(self,creation_date):
        self.creation_date = creation_date
        
    def worked_out(self):
        if (len(self.get_workout().cardio) != 0 or len(self.get_workout().lifts) != 0):
            return True
        else: 
            return False
        
    def get_workout(self):
        return self.workout
    
    def get_weight(self):
        return self.weight
    
    def get_bodyfat(self):
        return self.bodyfat
    
    def set_weight(self, weight):
        self.weight = weight
        
    def set_bodyfat(self, bodyfat):
        self.bodyfat = bodyfat
        
    def text_rep(self):
        pass
        #return 'Goal (' + self.desc_string + ') created on ' + str(self.creation_date) + ' is ' + str(self.status)

    def __str__(self):
        return self.creation_date.__str__() + str(self.worked_out())
        #return self.creation_date.__str__() + ' ' + self.desc_string + ':' + self.status + '\n'
        
class workout_node(object):
    def __init__(self):
        
        self.start_time = datetime.datetime(1,1,1,1,1)
        self.end_time = datetime.datetime(1,1,1,1,2)
        
        self.cardio = []                             #List of tuples; Each tuple is (cardio_name,duration)
        self.lifts = []                              #List of lists of tuples; List of lifts; One list per lift, and each lift is a list of tuples, which represent a set. Tuple format is (Lift Name, weightxrep)
  
        #self.workout_duration                      #A tuple consisting of (beginning_time,end_time) of workout
        self.lift_notes = ''                         #String of the notes for the day's lift
        self.rating = 0                               #Value from 1 to 5 indicating how good the workout was
        self.workout_type = 'NA'                       #String indicating which workout it was
        
    def text_rep(self):
        pass
        #return 'Goal (' + self.desc_string + ') created on ' + str(self.creation_date) + ' is ' + str(self.status)
    
    def get_cardio(self):
        return self.cardio
    
    def add_cardio(self, cardio):
        self.cardio.append(cardio)
        
    def set_start_time(self, st):
        self.start_time = st
            
    def set_end_time(self, et):
        self.end_time = et
                
    def add_lift(self,lift):
        fl = False
        if not self.lifts:
            l = list()
            l.append(lift)
            self.lifts.append(l)
            fl = True
        for li in range(len(self.lifts)):
            if self.lifts[li][0][0] == lift[0]:
                self.lifts[li].append(lift)
                fl = True
                break
        if fl == False:
            l = list()
            l.append(lift)
            self.lifts.append(l)
            
    def get_lifts(self):
        return self.lifts
    
    def get_lift(self,lift_name):
        return [l for l in self.lifts if l[0][0] == lift_name]
    
    def get_workout_duration(self):
        return self.end_time - self.start_time
    
    def get_start_time(self):
        return self.start_time
        
    def get_end_time(self):
        return self.end_time
    
    def get_lift_notes(self):
        return self.lift_notes
    
    def set_lift_notes(self, lift_notes):
        self.lift_notes = lift_notes  
        
    def get_rating(self):
        return self.rating
    
    def set_rating(self, rating):
        self.rating = rating
    
    def get_workout_type(self):
        return self.workout_type
    
    def set_workout_type(self, workout_type):
        self.workout_type = workout_type  
        
    def __str__(self):
        pass
        #return self.creation_date.__str__() + ' ' + self.desc_string + ':' + self.status + '\n'