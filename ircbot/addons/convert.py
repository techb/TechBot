'''
Adaptation of the convert.py (for BeastBot), for TechBot in python3
this module converts units after the command !convert,
For Evilzone IRC (irc.evilzone.org)
By: Khofo

Edit: techb
fixed some errors, also cleaned the code up enough to keep OP effort
in place.
'''


'''                    START CONVERSIONS                         '''

def kg_to_lb(number):
    result = number*float(2.2046)
    return str(number) + " Kilograms = " + str(result) + " Pounds"

def lb_to_kg(number):
    result = number*float(0.453592)
    return str(number) + " Pounds = " + str(result) + " Kilograms"

def f_to_c(number):
    result = (number-32)*float(0.555)
    return str(number) + " Degrees Fahreinheit = " + str(result) + " Degrees Celsius"

def c_to_f(number):
    result = (number*float(1.8))+32
    return str(number) + " Degrees Celsius = " + str(result) + " Degrees Fahreinheit"

def m_to_ft(number):
    result = number*float(3.28084)
    return str(number) + " Meters = " + str(result)+" Feet"

def ft_to_m(number):
    result = number*float(0.3048)
    return str(number) + " Feet = " + str(result)+" Meters"

def m_to_yds(number):
    result = number*float(1.09361)
    return str(number) + " Meters = " + str(result)+" Yards"

def ft_to_yds(number):
    result = number*float(0.3333)
    return str(number) + " Feet = " + str(result)+" Yards"

def yrds_to_m(number):
    result = number*float(0.9144)
    return str(number) + " Yards = " + str(result)+" Meters"

def yrds_to_ft(number):
    result = number*float(3)
    return str(number) + " Yards = " + str(result)+" Feet"

'''               END OF CONVERSIONS                      '''

def main(nick, comargvs, chan, send):
    numArgs = comargvs.strip().split()
    print(numArgs)
    if comargvs == "help":
        send.put(("convert Usage Example: 10 ft to m", chan))
    elif len(numArgs) == 4:
        number = numArgs[0] #the number to be converted
        unit_from = numArgs[1].lower() # unit to convert from
        unit_to = numArgs[3].lower() # unit to convert to
        con = conversion(unit_from, unit_to, number, send)
        send.put((con, chan))
    else:
        send.put(("convert Usage Example: 10 ft to m", chan))

def conversion(unit_from, unit_to, number, send):
    try:
        number = float(number.strip())
    except:
        return("convert Usage Example: 10 ft to m")

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
            return(m_to_ft(number))

        elif linear[(unit_from, unit_to)] == "m_to_yds":
            return(m_to_yds(number))

        elif linear[(unit_from, unit_to)] == "ft_to_m":
            return(ft_to_m(number))

        elif linear[(unit_from, unit_to)] == "ft_to_yds":
            return(ft_to_yds(number))

        elif linear[(unit_from, unit_to)] == "yds_to_m":
            return(yrds_to_m(number))

        elif linear[(unit_from, unit_to)] == "yds_to_ft":
            return(yrds_to_ft(number))

        elif linear[(unit_from, unit_to)] == "kg_to_lb":
            return(kg_to_lb(number))

        elif linear[(unit_from, unit_to)] == "lb_to_kg":
            return(lb_to_kg(number))

        elif linear[(unit_from, unit_to)] == "f_to_c":
            return(f_to_c(number))

        elif linear[(unit_from, unit_to)] == "c_to_f":
            return(c_to_f(number))

    else:
        return("ERROR: For usage please refer to .convert help")
