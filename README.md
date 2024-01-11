# Letterboxd To Trakt.tv Data Transfer

This script takes exported data from Letterboxd in the form of a CSV file and transfers either diary or watched data to Trakt.tv. There are some problems with it but it *mostly* works.
The main problem is that shows (limited series) logged on Letterboxd do not transfer to Trakt. This is because the data is being sent to Trakt specified as a movie, so Trakt looks for a movie with the title
of the show. This typically results in a movie of the same title as the show being logged on Trakt. Also, this was my first time working with Oauth, so use at you're own risk. I'm *pretty sure* that it is secure
enough at least. Finally, some movies are logged wrong if there are other films released in the same year with the same title. I'm not sure if this can be avoided as exporting from Letterboxd does not give any
other form of database ID to specify the specific movie. 

I have added functionality to add a **last entered** date, a feature I wanted that many other scripts made to transfer data between these services don't have. This lets you add movies to Trakt in bulk
so you can continue to log movies on Letterboxd and then occassionally run this script to add all movies logged since you last made the transfer. 

## How to use:
1. Export and unzip your Letterboxd data at https://letterboxd.com/settings/data/
2. Install any dependencies I used yada yada
3. Drag the diary or watched file into the same directory as the scripts
4. Run python3 boxd_to_trakt.py csv_type
5. A web browser will open and you will have to log in to Trakt.tv


## Examples
* python3 boxd_to_trakt.py diary
* python3 boxd_to_trakt.py diary --last_entered 12-03-2023

## Notes
* When using "last entered", the script only transfers movies *after* this date. Hence, if you have two movies logged on the same last transfered date, but you ran the transfer before logging the
second on Letterboxd, the program will skip that second one.
* There is no date associated with watched data from Letterboxd so I think Trakt just marks them as having been watched on the current date or the release date. 
