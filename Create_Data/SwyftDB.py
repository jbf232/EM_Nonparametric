import pymysql
import pandas as pd
import time

# Throughout this file:
# db = pymysql database connection
# q = an SQL query string

################# QUERY FUNCTIONS ###############################

# ConnectSwyftDB returns a pymysql connection the SwyftDB
def ConnectSwyftDB():
    cnx=pymysql.connect(host="analytics-sessions-replica.cxpzueixftrq.us-west-2.rds.amazonaws.com", user="reader", passwd="ZoJZeY8PvpGboy2KRoMDuRnBhTkKtcDn", db="analytics")
    return cnx

# RunQueryCursor takes in a cursor to a database a query q
# It executes the query and returns the cursor
def RunQueryCursor(q, cursor):
    cursor.execute(q)
    return cursor

# RunQueryAll takes in a database connection db and a query q 
# It returns an array containing each row in the query results
def RunQueryAll(db, q):
    cursor = db.cursor()
    cursor.execute(q)
    return cursor.fetchall()

# PrintQuery takes in a database connection db and a query q
# It prints each row in the query results
def PrintQuery(db, q):
    cursor = db.cursor()
    cursor.execute(q)
    result = cursor.fetchall()

    for row in result:
        print row
    return

################# DATA SUBFUNCTIONS ###############################

# CorrectOrders returns the card and option order for
# tapped recommended options
def CorrectOrders(name):
    if name == "trip-planner-tap-walking-recommendation":
        return 1,1
    if name == "trip-planner-tap-rideshare-recommendation":
        return 1,3
    if name == "trip-planner-tap-transit-recommendation":
        return 1,2
    return 0,0

# FindSearches returns all searches where there was exactly one tap
def FindSearches(db):
    return RunQueryAll(db, """SELECT si 
    FROM (SELECT search_id AS si, COUNT(id) AS ci FROM search_event
    WHERE name LIKE 'trip-planner-tap%' AND created_at > '2015-12-15'
    GROUP BY search_id) AS sg WHERE ci = 1""")

# FindTapEntry takes in a search id s_id and returns the tap entry
# for that search
def FindTapEntry(db, s_id):
    return RunQueryAll(db, """SELECT name, card_order, option_order 
    FROM search_event WHERE search_id = """
    +str(s_id) +""" AND name LIKE 'trip-planner-tap%'""")[0]

# FindOptTapped takes in a search id s_id, card order c_ord, and
# option order o_ord and returns the presented entry for the option tapped
def FindOptTapped(db, s_id, c_ord, o_ord):
    return RunQueryAll(db, """SELECT travel_product, travel_mode, travel_distance, 
    travel_price, travel_price_surge, travel_time 
    FROM search_event WHERE search_id = """
    + str(s_id)+""" AND NOT name LIKE 'trip-planner-tap%'
    AND card_order = """+str(c_ord)+""" AND option_order = """+str(o_ord))

# FindRec takes in a search id s_id and returns the recommended entries
def FindRec(db, s_id):
    return RunQueryAll(db, """SELECT travel_product, travel_mode, travel_distance, 
    travel_price, travel_price_surge, travel_time 
    FROM search_event WHERE search_id = """
    + str(s_id)+""" AND card_order = 1""")

# FindNonRec takes in a search id s_id and returns the nonrecommended entries
def FindNonRec(db, s_id):
    return RunQueryAll(db, """SELECT travel_product, travel_mode, travel_distance, 
    travel_price, travel_price_surge, travel_time, card_order, option_order 
    FROM search_event WHERE search_id = """
    + str(s_id)+""" AND NOT card_order = 1""")
    
# WriteRecord creates a string to record a data entry 
def WriteRecord(s_id, ind_opt, chosen, t_prod, t_dis, t_time, t_pr, t_sur):
    return str(s_id)+","+str(ind_opt)+","+str(chosen)+","+t_prod+","+str(t_dis)+","+str(t_time)+","+str(t_pr)+","+str(t_sur)+"\n"

# RecordRec creates a record string of all the recommended options and checks
# to see if they match the chosen option 
def RecordRec(db, s_id, c_prod, c_dis, c_pr, c_sur, c_time):
    rec_str = ""
    chose_rec = False

    # Go through all recommended options
    index = 0
    options = FindRec(db, s_id)
    for (t_prod, t_m, t_dis, t_pr, t_sur, t_time) in options:
        if t_prod == "n/a":
            t_prod = t_m

        # Check if it matches the chosen option
        chosen = False
        if (t_prod, t_dis, t_pr, t_sur, t_time) == (c_prod, c_dis, c_pr, c_sur, c_time):
            chosen = True
            chose_rec = True

        # Only record with nonnegative price
        if t_pr >= 0:
            rec_str += WriteRecord(s_id, index, chosen, t_prod, t_dis, t_time, t_pr, t_sur)
            index += 1
            
    return rec_str, chose_rec, options, index

# RecordNonRec creates a record string of all nonrecommended options and
# checks whether they match a recommended option or the chosen option
# (skipping in both these cases)
# Option indices start from index
def RecordNonRec(db, s_id, card, opt, recommended, index):
    opt_str = ""

    # Go through all nonrecommended options
    options = FindNonRec(db, s_id)
    for (t_prod, t_m, t_dis, t_pr, t_sur, t_time, c_ord, o_ord) in options:
        rec = True
        # Check if it matches the chosen option
        if card == c_ord and opt == o_ord:
            rec = False
        # Check if it has a negative price
        if t_pr < 0:
            rec = False
        # Check if it matches a recommended option
        for (r_prod, r_m, r_dis, r_pr, r_sur, r_time) in recommended:
            if (r_prod, r_m, r_dis, r_pr, r_sur, r_time) == (t_prod, t_m, t_dis, t_pr, t_sur, t_time):
                rec = False
                break

        # Only record with nonnegative price
        if rec:
            if t_prod == "n/a":
                t_prod = t_m
            opt_str += WriteRecord(s_id, index, False, t_prod, t_dis, t_time, t_pr, t_sur)
            index += 1
            
    return opt_str

# RecordOptions records all the options for a given search
# and will return True if no catch cases (chose neg prod, mult or no matches
# for clicked option) are found and the appropriate string
def RecordOptions(db, s_id):
    search_str = ""
    print s_id
    
    # Find the click entry:
    name, c_ord, o_ord = FindTapEntry(db, s_id)

    # Correct card if not already listed
    if c_ord == None:
        c_ord, o_ord = CorrectOrders(name)
        # If still not found then don't record
        if c_ord != 1:
            return False, ""

    # Find the corresponding listed option
    tapped = FindOptTapped(db, s_id, c_ord, o_ord)

    # If we didn't get exactly one match return, don't record
    if len(tapped) != 1:
        return False, ""

    c_prod, c_m, c_dis, c_pr, c_sur, c_time = tapped[0]
    # If we chose a negative priced option, don't record
    if c_pr < 0:
        return False, ""

    if c_prod == "n/a":
         c_prod = c_m
    
    # Record Recommended Options
    rec_str, chose_rec, recommended, index = RecordRec(db, s_id, c_prod, c_dis, c_pr, c_sur, c_time)
    search_str += rec_str
    if chose_rec == False:
        search_str += WriteRecord(s_id, index, True, c_prod, c_dis, c_time, c_pr, c_sur)
        index += 1

    # Record Nonrecommended Options (skip repeats)
    search_str += RecordNonRec(db, s_id, c_ord, o_ord, recommended, index)
    return True, search_str
        


################# MAIN FUNCTION ###############################
    
if __name__ == "__main__":
    db = ConnectSwyftDB()
    potential_searches = FindSearches(db)
   
    # Open files to write to
    f1 = open('search_options.txt','w')
    f2 = open('search_extra_info.txt','w')

    print "Total Potential Searches to Record:"
    print len(potential_searches) 
    
    # Go through all searches 
    num_data = 0
    skip_searches = 0
    for x in potential_searches:
        print num_data
        s_id = x[0]
        met_constr, search_event_str = RecordOptions(db, s_id)

        if met_constr:
            #PrintQuery(db, """SELECT name, travel_product, travel_mode, travel_distance, 
    #travel_price, travel_price_surge, travel_time, card_order, option_order FROM search_event WHERE search_id = """+str(s_id))
            f1.write(search_event_str)
            _, uuid, date, s_lat, s_lon, e_lat, e_lon = RunQueryAll(db, """SELECT 
            id, uuid, created_at, start_lat, start_lon, end_lat, end_lon 
            FROM search WHERE id = """+str(s_id))[0]
            f2.write(str(s_id)+","+str(uuid)+","+str(date)+","+str(s_lat)+","+str(s_lon)+","+str(e_lat)+","+str(e_lon)+"\n")
            num_data += 1
            #print search_event_str
        else:
            #PrintQuery(db, """SELECT name, travel_product, travel_mode, travel_distance, 
    #travel_price, travel_price_surge, travel_time, card_order, option_order FROM search_event WHERE search_id = """+str(s_id))
            skip_searches += 1
        if num_data > 10:
            break 
    print "Recorded Searches: "+str(num_data) 
    print "Skipped Searches: "+str(skip_searches)

    f1.close()
    f2.close()
