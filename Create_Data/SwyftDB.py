import pymysql
import pandas as pd
import time

# This function returns a pymysql connection the SwyftDB
def ConnectSwyftDB():
    cnx=pymysql.connect(host="analytics-sessions-replica.cxpzueixftrq.us-west-2.rds.amazonaws.com", user="reader", passwd="ZoJZeY8PvpGboy2KRoMDuRnBhTkKtcDn", db="analytics")
    return cnx

# is function takes in a cursor to a database and a SQL query string q
# It executes the query and returns the cursor
def RunQueryCursor(q, cursor):
    cursor.execute(q)
    return cursor

# This function takes in a database connection db and a SQl query string q 
# It returns an array containing each row in the query results
def RunQueryAll(db, q):
    cursor = db.cursor()
    cursor.execute(q)
    return cursor.fetchall()

# This function takes in a database connection db and a SQL query string q
# It prints each row in the query results
def PrintQuery(db, q):
    cursor = db.cursor()
    cursor.execute(q)
    result = cursor.fetchall()

    for row in result:
        print row
    return

if __name__ == "__main__":
    cnx = ConnectSwyftDB()
    potential_searches = RunQueryAll(cnx, """SELECT si 
    FROM (SELECT search_id AS si, COUNT(id) AS ci FROM search_event
    WHERE name LIKE 'trip-planner-tap%'
    GROUP BY search_id) AS sg WHERE ci = 1""")
   
    # Open files to write to
    f1 = open('search_options.txt','w')
    f2 = open('search_extra_info.txt','w')

    print "Total Potential Searches to Record:"
    print len(potential_searches) 
    
    # Go through all searches 
    num_data = 0
    skip_events = 0
    skip_events_nontaxi = 0
    skip_searches = 0
    for x in potential_searches:
        print num_data
        s_id = x[0]

        # Find the chosen product:
        name, p_card, p_ord = RunQueryAll(cnx, """SELECT name, card_order, option_order 
        FROM search_event WHERE search_id = """
        +str(s_id) +""" AND name LIKE 'trip-planner-tap%'""")[0]
        
        # Give correct card if not already listed
        if p_card == None:
            if name == "trip-planner-tap-walking-recommendation":
                p_card, p_ord = 1,1
            if name == "trip-planner-tap-rideshare-recommendation":
                p_card, p_ord = 1,3
            if name == "trip-planner-tap-transit-recommendation":
                p_card, p_ord = 1,2
        
        # Index options and create table string
        search_event_str = ""
        ind_opt = 0
        chose_neg = False
        found_match = False
        mult_matches = False

        options = RunQueryAll(cnx, """SELECT travel_product, travel_mode, travel_distance, 
        travel_price, travel_price_surge, travel_time, card_order, option_order 
        FROM search_event WHERE search_id = """
        + str(s_id)+""" AND NOT name LIKE 'trip-planner-tap%'""")

        # Ignore negative priced options
        for (t_prod, t_m, t_dis, t_pr, t_sur, t_time, c_ord, o_ord) in options:
            # Correct walking options with no product listing
            if t_prod == "n/a":
                t_prod = t_m

            # Find if it was the chosen option 
            chosen = (c_ord == p_card and o_ord == p_ord)
            if chosen and t_pr < 0:
                chose_neg = True
            if chosen and found_match == True:
                mult_matches = True
                print s_id
            if chosen and found_match == False:
                found_match = True
            
            # Add to list of options if price is not negative
            if t_pr >= 0:
                search_event_str += str(s_id)+","+str(ind_opt)+","+str(chosen)+","+t_prod+","+str(t_dis)+","+str(t_time)+","+str(t_pr)+","+str(t_sur)+"\n"
                ind_opt += 1
            elif t_prod != "ubertaxi":
                skip_events += 1
                skip_events_nontaxi += 1
            else:
                skip_events += 1

        if chose_neg == False and found_match == True and mult_matches == False:
            # print search_event_str
            f1.write(search_event_str)
            _, uuid, date, s_lat, s_lon, e_lat, e_lon = RunQueryAll(cnx, """SELECT 
            id, uuid, created_at, start_lat, start_lon, end_lat, end_lon 
            FROM search WHERE id = """+str(s_id))[0]
            f2.write(str(s_id)+","+str(uuid)+","+str(date)+","+str(s_lat)+","+str(s_lon)+","+str(e_lat)+","+str(e_lon)+"\n")
            num_data += 1
            print search_event_str
        else:
            skip_searches += 1
        if num_data > 10:
            break 
    print "Recorded Searches: "+str(num_data) 
    print "Skipped Searches: "+str(skip_searches)
    print "Skipped Event Entries: "+str(skip_events)
    print "Skipped Non-Taxi Event Entries: "+str(skip_events_nontaxi)
    f1.close()
    f2.close()
