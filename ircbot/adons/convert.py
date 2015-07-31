#!/usr/bin/python

'''
Adaptation of the convert.py (for BeastBot), for TechBot in python3
this module converts units after the command !convert, 
For Evilzone IRC (irc.evilzone.org)

By: Khofo
'''


'''                    START CONVERSIONS                         '''

def kg_to_lb(number,send):
    result = number*float(2.2046)
    send(str(number) + " Kilograms = " + str(result) + " Pounds")

def lb_to_kg(number,send):
    result = number*float(0.453592)
    send(str(number) + " Pounds = " + str(result) + " Kilograms")
def f_to_c(number,send):
    result = (number-32)*float(0.555)
    send(str(number) + " Degrees Fahreinheit = " + str(result) + " Degrees Celsius")

def c_to_f(number,send):
    result = (number*float(1.8))+32
    send(str(number) + " Degrees Celsius = " + str(result) + " Degrees Fahreinheit")

def m_to_ft(number,send):
    result = number*float(3.28084)
    send(str(number) + " Meters = " + str(result)+" Feet" )

def ft_to_m(number,send):
    result = number*float(0.3048)
    send(str(number) + " Feet = " + str(result)+" Meters")

def m_to_yds(number,send):
    result = number*float(1.09361)
    send(str(number) + " Meters = " + str(result)+" Yards")

def ft_to_yds(number,send):
    result = number*float(0.3333)
    send(str(number) + " Feet = " + str(result)+" Yards")

def yrds_to_m(number,send):
    result = number*float(0.9144)
    send(str(number) + " Yards = " + str(result)+" Meters")    

def yrds_to_ft(number,send):
    result = number*float(3)
    send(str(number) + " Yards = " + str(result)+" Feet")

'''               END OF CONVERSIONS                      '''

def main(nick, comargvs, chan, send):
    try:
        numArgs = comargvs.split()
        if numArgs != '':
            if comargvs == "help":
                send("Usage Example: 10 ft to m")
            else:
                pass
            number = numArgs[0] #the number to be converted
            unit_from = numArgs[1].lower() # unit to convert from 
            unit_to = numArgs[3].lower() # unit to convert to
            send(conversion(unit_from, unit_to, number,send))
            pass
    except:
        pass

        
def conversion(unit_from, unit_to, number, send):    
        
    try:
        number = float(number.strip())
    except:
        send("Usage Example: 10 ft to m")
    
    linear = { ('m', 'ft')  : "m_to_ft",  
               ('m', 'yds') : "m_to_yds",   
               ("ft", "m")  : "ft_to_m",
               ("ft", "yds"): "ft_to_yds",
               ("yds", "m") : "yds_to_m",
               ("yds", "ft"): "yds_to_ft",
               ("kg", "lb") : "kg_to_lb",
               ("lb", "kg") : "lb_to_kg",
               ("f", "c")   : "f_to_c",
               ("c", "f")   : "c_to_f",
               }
    if (unit_from, unit_to) in linear:
        if linear[(unit_from, unit_to)] == "m_to_ft":
            send(m_to_ft(number,send))
        
        elif linear[(unit_from, unit_to)] == "m_to_yds":
            send(m_to_yds(number,send))
        
        elif linear[(unit_from, unit_to)] == "ft_to_m": 
            send(ft_to_m(number,send))
        
        elif linear[(unit_from, unit_to)] == "ft_to_yds":
            send(ft_to_yds(number, send))
        
        elif linear[(unit_from, unit_to)] == "yds_to_m":
            send(yrds_to_m(number,send))
        
        elif linear[(unit_from, unit_to)] == "yds_to_ft":
            send(yrds_to_ft(number,send))
        
        elif linear[(unit_from, unit_to)] == "kg_to_lb":
            send(kg_to_lb(number,send))
        
        elif linear[(unit_from, unit_to)] == "lb_to_kg":
            send(lb_to_kg(number,send))
        
        elif linear[(unit_from, unit_to)] == "f_to_c":
            send(f_to_c(number,send))
        
        elif linear[(unit_from, unit_to)] == "c_to_f":
            send(c_to_f(number,send))
        else:
            pass
    else:
        error = "ERROR: For usage please refer to !convert help"
        send(error)
