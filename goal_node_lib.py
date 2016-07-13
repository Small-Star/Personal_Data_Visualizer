#Goal Visualizer Library v.01

#03/05/2015

class goal(object):
    def __init__(self,status,creation_date,desc_string):
        self.status = status
        self.creation_date = creation_date
        self.desc_string = desc_string
        
        self.action_date = ''
        self.action_string = ''

    def text_rep(self):
        return 'Goal (' + self.desc_string + ') created on ' + str(self.creation_date) + ' is ' + str(self.status)

    def get_status(self):
        return self.status

    def get_creation_date(self):
        return self.creation_date

    def get_desc_string(self):
        return self.desc_string

    def get_action_date(self):
        return self.action_date

    def get_action_string(self):
        return self.action_string

    def set_action_date(self, action_date):
        self.action_date = action_date

    def set_action_string(self, action_string):
        self.action_string = action_string

    def __str__(self):
        return self.creation_date.__str__() + ' ' + self.desc_string + ':' + self.status + '\n'

