'''
Created on Jul 19, 2015

'''
from vis_diet import *
from vis_goals import *
from vis_records import *
from vis_weightlifting import *
import datetime

#if __name__ == '__main__':

print "Init"
day_nodes = {}
print "Reading diet info..."
day_nodes = read_data_diet(day_nodes)
print "Reading goals info..."
day_nodes = read_data_goals(day_nodes = day_nodes)
print "Reading records info..."
day_nodes = read_data_records(day_nodes = day_nodes)
print "Reading weightlifting info..."
day_nodes = read_weightlifting_records(day_nodes = day_nodes)

# print str(day_nodes[datetime.date(2015,3,24).toordinal()].get_bnode().get_workout().get_start_time()), str(day_nodes[datetime.date(2015,3,24).toordinal()].get_bnode().get_workout().get_end_time()), day_nodes[datetime.date(2015,3,24).toordinal()].get_bnode().get_workout().get_workout_duration()
# print str(day_nodes[datetime.date(2015,3,24).toordinal()].get_bnode().get_weight())
# print str(day_nodes[datetime.date(2015,3,24).toordinal()].get_bnode().get_bodyfat())
# print str(day_nodes[datetime.date(2015,3,24).toordinal()].get_bnode().get_workout().get_rating())
# print str(day_nodes[datetime.date(2015,3,24).toordinal()].get_bnode().get_workout().get_workout_type())
# print str(day_nodes[datetime.date(2015,3,24).toordinal()].get_bnode().get_workout().get_cardio())
# print str(day_nodes[datetime.date(2015,8,14).toordinal()].get_bnode().get_workout().get_lifts())

print "Graphing diet info..."
graph_diet(day_nodes, 7)
print "Graphing goal info..."
graph_goals_stacked_bar(dict((k, v) for k, v in day_nodes.iteritems() if datetime.date(2014,03,22).toordinal() <= k),7) #cut out the dates with no goals

graph_single_lift(day_nodes,'Bench Press',5)

print "Graphing body info..."
graph_body(day_nodes, 7)

pylab.show()

