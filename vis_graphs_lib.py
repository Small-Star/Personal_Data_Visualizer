'''
Created on Jul 23, 2015

'''
import pylab

def moving_avg(series,n=5,use_float=False):
    '''Takes an input list of ints and returns an input list of same length; values are the n point moving average of the input. Initial values are padded out.'''
    
    if not use_float:
        ma = [0 for i in range(len(series))]
    if use_float:
        ma = [0*1.0 for i in range(len(series))]
        
    for i in range(len(ma) - n):
        #Do the bulk
        for j in range(n):    
            ma[i+n] += series[i-j+n]
        ma[i+n] = ma[i+n]/n
        
    for i in range(n):
        #Do the edge cases at the beginning
        for j in range(0,i + 1): 
            ma[i] += series[j]
        ma[i] = ma[i]/(j + 1)

    return ma
    
def create_bg_rects(nodes,height,bottom=0.0):
    '''Takes a list of input nodes and returns rects colored based on FIC, with the height passed in'''
        
    print "BGR" + str(type(nodes))
    rect_array = []
    
    dates =[nodes[node].get_date() for node in nodes]
    fics = [nodes[node].get_fic() for node in nodes]
    
    #print dates
    #Set up BG ranges for FICs
    lbound = 0
    last_ubound = 0
    
    for f in range(len(fics)):
        if fics[f] != fics[lbound]: #if tested fic is different than the fic at the beginning of the range, there is a change
            if fics[lbound] == 'M':
                color = '#b8b8b8'
            elif fics[lbound] == 'C':
                color = '#86cecb'
            elif fics[lbound] == 'B':
                color = '#7a7aff'

            #Weird data error - seemed to be reading input file correctly, but was getting an off by one error when drawing this particular rect
            #NOTE: Sorting the nodelist seems to have fixed this
            #if dates[lbound].__str__()=="2014-08-10":
            #    rect = pylab.Rectangle((dates[lbound], bottom), 63, height - bottom,facecolor = color)
            #    rect_array.append(rect)
            #    lbound = f
            #else:
            rect = pylab.Rectangle((dates[lbound], bottom), f - lbound, height - bottom,facecolor = color)
            rect_array.append(rect)
            last_ubound = f
            #print "rect created at " + str(lbound) + " to " + str(f) + " for " + str(fics[lbound])
            lbound = f
    
    #Create final rect
    if fics[lbound] == 'M':
        color = '#b8b8b8'
    elif fics[lbound] == 'C':
        color = '#86cecb'
    elif fics[lbound] == 'B':
        color = '#7a7aff'
        
    rect = pylab.Rectangle((dates[last_ubound], bottom), len(fics) - last_ubound, height - bottom,facecolor = color)
    rect_array.append(rect)
    
    return rect_array
    
