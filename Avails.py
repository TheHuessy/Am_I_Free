from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import datetime
import re
from pprint import pprint
from calendar import monthcalendar as mc



def get_the_date(week_of_month, day_of_week, year, month_num):
    days_dict = {"Monday": 0,
                 "Tuesday":1,
                 "Wednesday": 2,
                 "Thursday": 3,
                 "Friday": 4,
                 "Saturday": 5,
                 "Sunday": 6}
    possible_dates =[]
    
    for week_num in week_of_month:    
        # Get week arrays
        may = mc(year, month_num)
    
        # Narrow down to the week we're looking for
        dt = may[week_num-1]
        
        for dys in day_of_week:
            # Get the date of the day of the week we're looking for
            day_dt = dt[days_dict[dys]]
            
    
            # Combine the info into one date object
            try:
                result = datetime.date(year, month_num, day_dt)
            except:
                ## If that didn't work, then the date is probably not in range so skip it
                continue
            else:
                possible_dates += [result]
    
    
    # Send the sucker back
    return(possible_dates)




## If monthly_week: look for dates that fall on the 'days' values but also that appear in X week

def free_dates(days_var=[], months_forward=4, booker_show=None, monthly_week=None):

    
    known_shows = {"Laugh": ["Thursday", "Friday", "Saturday"],
                  "Nicks": ["Friday", "Saturday"],
                  "Hideout": ["Thursday","Friday", "Saturday"],
                  "McGreevys": ["Monday", "Tuesday"],
                  "Capo": ["Monday"],
                  "Comedy Studio": ["Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                  "Cott": ["Monday", "Thursday", "Friday", "Saturday"],
                  "Comedy Party": ["Thursday", "Saturday"]}
    
    day_dict = {0: "Monday",
                1: "Tuesday",
                2: "Wednesday",
                3: "Thursday",
                4: "Friday",
                5: "Saturday",
                6: "Sunday"}
    
    if booker_show:
        if booker_show not in known_shows.keys():
            print("The booker specified is not known\nBookers Known: {}".format(known_shows.keys()))
            return(None)
        else:
            days = known_shows[booker_show]
            
    else:
        days = days_var
    
    ####################################
    #########GETTTING GOOGLE DATA#######
    ####################################
    
    ## SCOPES AND CREDENTIAL LOCATION CODING
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = '/home/james/Documents/PythonNotebooks/Calendar API/calendar.json'

    ## BUILDING CREDENTIAL OBJECT
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    ## CREATING API SERVICE INSTANCE
    service = build('calendar', 'v3', credentials=credentials)

    ## CALLING ALL EVENTS FOR THE CALENDAR FOR JAMESHUESSY@GMAIL.COM
    t_now = datetime.datetime.utcnow()
    
    if t_now.month+months_forward > 12:
        end_year = t_now.year + 1
        end_month = (t_now.month+months_forward)-12
    elif t_now.month+months_forward <= 12:
        end_year = t_now.year
        end_month = t_now.month+months_forward
        
    t_end = datetime.datetime(end_year, end_month, 1, *t_now.timetuple()[3:-2])

    d = service.events().list(calendarId='jameshuessy@gmail.com', 
                              timeMin=t_now.isoformat()+'Z',
                              timeMax=t_end.isoformat()+'Z')
    ### Calling 'execute()' is how you make the api call
    dd = d.execute()


    try:
        events = pd.DataFrame(dd['items'])
    except Exception as err:
        print("Couldn't get items into the dataframe\nError: {}".format(err))

    #print("Done")
    
    ####################################
    #########PULLING EVENTS DATES#######
    ####################################

    termine = []

    for i in range(len(events)):   
        if events['status'][i] == 'cancelled':            
            continue
            
        f = events['start'][i]
        gi = events['summary'][i]
        
        try:
            tme = f['dateTime']
        except:
            try:
                tme = events['start'][i]
                tme = tme['date']
                tme = datetime.datetime.strptime(tme, '%Y-%m-%d')
            
                tmedn = events['end'][i]
                tmedn = tmedn['date']
                tmedn = datetime.datetime.strptime(tmedn, '%Y-%m-%d')
            
                tme = datetime.datetime.date(tme)
                tmedn = datetime.datetime.date(tmedn)
            except:
                print("Couldn't parse an all day event: {}".format(gi))
        
            else:
                all_day_range = list(pd.date_range(start=tme, end=tmedn))
        
                ### Add date range dates to termine
                for i in range(len(all_day_range)-1):
                    dte = datetime.datetime.date(all_day_range[i])
                    termine += [dte]
        
        else:
            tme = re.sub(pattern='-04:00', repl="", string=tme)
            tme = re.sub(pattern='-05:00', repl="", string=tme)
        
            tme = re.sub(pattern='T', repl=" ", string=tme)
        
            tme = datetime.datetime.strptime(tme, '%Y-%m-%d %H:%M:%S')
        
            tmed = datetime.datetime.date(tme)
            try:
                tmet = datetime.datetime.time(tme)
            except:
                print("{} appears to be an all dayer".format(gi))
            else:        
                uhr19 = datetime.datetime.time(datetime.datetime.strptime("2019-05-21 18:00:00", '%Y-%m-%d %H:%M:%S'))
                if tmet > uhr19:
                    termine += [tmed]
    
    

    ####################################
    #########PULLING EVENTS DATES#######
    ####################################
    
    
    # Beginning Date (today)
    t_now = datetime.datetime.utcnow()

    # End Date (the first day of the 4th month from today)
    # fatetime.datetime() is expecting year, month, day, time, etc. which you either pass from t_now.timetupple or fill in yourself
    
    if t_now.month + months_forward > 12:
        t_year = t_now.year+1
        t_month = (t_now.month + months_forward)-12
    else:
        t_year = t_now.year
        t_month = t_now.month + months_forward
    
    t_end = datetime.datetime(t_year, t_month, 1, *t_now.timetuple()[3:-2])

    
    if monthly_week:
        t_range = []
        if t_end.month < t_now.month:
            for mnths in range(t_now.month, 12):
                # Start with the first month through december
                t_r = get_the_date(week_of_month=monthly_week,
                                   day_of_week=days,
                                   year=t_now.year, 
                                   month_num=mnths)
                t_range += [t_r]
                # Go to January through the end month of the following year
            for mnths in range(1, t_end.month):                
                t_r = get_the_date(week_of_month=monthly_week,
                                   day_of_week=days,
                                   year=t_end.year, 
                                   month_num=mnths)
                t_range += [t_r]
            
        else:
            for mnths in range(t_now.month, t_end.month):                
                t_r = get_the_date(week_of_month=monthly_week,
                                   day_of_week=days,
                                   year=t_year, 
                                   month_num=mnths)
                t_range += [t_r]
        
    
    else:
        # Date range generated
        t_range = list(pd.date_range(start=t_now, end=t_end))
        
    
    # Getting everything formatted as just the date
    for i in range(len(t_range)):
        nt = datetime.datetime.date(t_range[i])        
        t_range[i] = nt        
    
    kill = []
    for e in t_range:
        if e in termine:
            kill += [e]
    
    # If you try to kill off the dates you're already booked, you screw up the loop
    # This way you grab all the date values and then perform the remove without affecting
    # the array you're looping through. I imagine that when you got rid of an iteration,
    # it's calling it as (t_range[x]) and when you get rid of x the list moves down one.
    
    for death in kill:
        t_range.remove(death)
    
    fin = []
    for l in t_range:
        ddw = datetime.datetime.weekday(l)
        ddn = day_dict[ddw]
        if ddn in days:
            fin += [re.sub(pattern="[0-9]{4}-", repl="", string=l.isoformat())]    
    
    return([x for x in fin])
