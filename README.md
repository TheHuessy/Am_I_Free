# Am_I_Free
A python script that scrapes my google calendar from the API, judges events, and returns days that I don't have anything booked after 6PM. The goal of this project is to create an automated email system that contacts various comedy clubs in Boston and sends my availability for the next X months.

## Methods

### Google Calendar API

The script first goes out to the google calendar API, provides the credential file generated from my google developer account, and pulls in all events from my personal calendar between the day of the run and 4 months into the future.

### Evaluation of Events

Once the API delievers the list of events info, the script extracts and cleans the start and end datetimes for each event. As it does this, it evaluates whether or not the event is after 6 PM. If it is, then that date is added to an array of 'busy' dates. If the event starts before 6 PM, it is assumed that the rest of the evening is free. 

If the script encounters a full day event (sometimes I will put travel as a multi-all day event), it will take each date in the range from first to last day of the event and add those dates to the array of 'busy' dates

### Comparing to Desired Days

The function in the script allows a relative degree of freedom for the user to compare their free days to busy ones. The function has several, hard coded day patterns that it will look for within the given date range depending on the person being contacted for dates. These do not have to be utilized and the user can put in days of the week and even weeks of the month. As is common in the entertainment world, sometimes shows happen once a month on the Xth Y day of the week each month. 

The function allows for one or more values to be passed to both the day of the week argument as well as the week of the month argument. This allows the user to generate every free second and forth Wednesday and Thursday that they are free on within the date range, for instance.

### Result

Once all the evaluation is completed, the function returns an array of dates which can either be passed to another function/script section or copied and pasted into an email.

### Coming Next

As mentioned in the introduction, the goal of this project is to automate emails to send my available dates to bookers in Boston. This is the first half, which generates the list of free dates and the next part will be the automated email piece. I plan to use the gmail API, similarly to the google calendar API and set up a monthly cronjob on my home storage server.
