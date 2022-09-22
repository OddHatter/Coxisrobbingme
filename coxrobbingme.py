import os
import numpy as np
import pandas as pd
import mysql.connector
from datetime import datetime
from dotenv import load_dotenv
import matplotlib.pyplot as plt


load_dotenv()   # Load environment variables
b2mb = 1000000  # Bits to Megabits vice versa


# Get data from database
def get_daily_speed_data():
    mydb = mysql.connector.connect(         # Connect to database
        host=os.environ.get('DB_HOST'),     # Get DB host from env variable
        user=os.environ.get('DB_USER'),     # Get DB user from env variable
        password=os.environ.get('DB_PASS'), # Get DB password from env variable
        database=os.environ.get('DB_NAME')  # get DB name from env variable
    )
    dts_query   = mydb.cursor() 
    dts_query.execute("SELECT Download FROM daily_test_speeds")   # Query download speeds
    dts_results = dts_query.fetchall()                            # Store query results
    dts_df      = pd.DataFrame(dts_results, columns=['Download']) # Put results into a dataframe
    dts_df['Download'].replace('', np.nan, inplace=True)          # Replace empty download values with NaN
    #dts_df['Upload'].replace('', np.nan, inplace=True)           # Replace empty upload values with NaN(not enabled)   
    dts_df      = dts_df.dropna()                                 # Clear empty rows
    
    return dts_df                                                 # return the dataframe


# Calculate the average deficiency percentage of both the download and upload speeds
def calc_def(true_down):
    pkg_down  = 1000 * b2mb              # Advertised package download speed in bits
    #pkg_up    = 35 * b2mb               # Advertised package upload speed in bits
    down_def  = 1 - (true_down/pkg_down) # Calculate deficiency percentage of download speed
    # up_def   = 1 - (true_up/pkg_up)    # Calculate deficiency percentage of upload speed
    # avg_def  = (up_def + down_def)/2   # Calculate the average deficiency percentage of both download and upload speeds
    avg_def   = down_def                 # This line is only needed due to the upload speed calculation currently being disabled.

    return avg_def                       # Return average deficiency percentage


# Calculate the amount of money per second stolen by ISP
def calc_cost_def(avg_def):
    annual_act_cost   = 110 * 12                        # Calculate actual annual package cost (montly amount * 12)
    annual_fed_cost   = 140 * 12                        # Calculate FSD package cost (montly amount * 12)
    annual_full_cost  = 170 * 12                        # Calculate full annual package cost (montly amount * 12)                    
    sec_per_year      = 365 * (24 * 60 * 60)            # Calculate seconds in a year
    act_cost_per_sec  = annual_act_cost / sec_per_year  # Calculate actual cost per second
    fed_cost_per_sec  = annual_fed_cost / sec_per_year  # Calculate FSD cost per second
    full_cost_per_sec = annual_full_cost / sec_per_year # Calculate Full cost per second
    act_cost_def      = act_cost_per_sec * avg_def      # Calculate the avg actual amount "stolen"
    fed_cost_def      = fed_cost_per_sec * avg_def      # Calculate the FSD actual amount "stolen"
    full_cost_def     = full_cost_per_sec * avg_def     # Calculate the Full actual amount "stolen"

    return act_cost_def, fed_cost_def, full_cost_def    # Return amount per second stolen

# Generate caluculated lists for each cost tier
def gen_calc_lists(dts_list):
    act_calc_list  = []  # Create and empty list to hold the actual cost deficiency data
    fed_calc_list  = []  # Create and empty list to hold the FSD cost deficiency data
    full_calc_list = []  # Create and empty list to hold the Full cost deficiency data
    for spd in dts_list: # Loop through the download test speeds list to perform calculations on each test speed
        avg_def  = calc_def(float(spd[0])) # Calculate average speed deficiency percentage for all items in speedtest list (spd[1] is for upload speeds])
        cost_def = calc_cost_def(avg_def)  # Calculate the cost deficiency based on average speed deficiency
        act_calc_list.append(cost_def[0])  # Output a list of actual cost deficiency for each item in speed list
        fed_calc_list.append(cost_def[1])  # Output a list of FSD cost deficiency for each item in speed list
        full_calc_list.append(cost_def[2]) # Output a list of Full cost deficiency for each item in speed list
    
    return act_calc_list, fed_calc_list, full_calc_list # return all 3 lists as one list

# Generate cost deficiency dictionaries for use on website
def gen_def_dict(dts_list):
    minute = 60        # Variable for minute in seconds
    hour   = 3600      # Variable for hour in seconds
    day    = 86400     # Variable for day in seconds
    week   = 604800    # Variable for week in seconds
    month  = 2592000   # Variable for month in seconds
    year   = 31536000  # Variable for year in seconds
    
    act_def_dict     = {} # Initialize actual cost dictionary
    fed_def_dict     = {} # Initialize FDS cost dictionary
    full_def_dict    = {} # Initialize Full cost dictionary
    
    calc_list        = gen_calc_lists(dts_list) # Get calculated deficiency lists
    act_per_sec_def  = np.average(calc_list[0]) # Calculate actual cost deficiency average from list
    fed_per_sec_def  = np.average(calc_list[1]) # Calculate FDS cost deficiency average from list
    full_per_sec_def = np.average(calc_list[2]) # Calculate Full cost deficiency average from list
    
    act_def_dict["act_per_sec"]   = act_per_sec_def           # Actual cost per second
    act_def_dict["act_per_min"]   = act_per_sec_def * minute  # Actual cost per minute
    act_def_dict["act_per_hr"]    = act_per_sec_def * hour    # Actual cost per hour
    act_def_dict["act_per_day"]   = act_per_sec_def * day     # Actual cost per day
    act_def_dict["act_per_wk"]    = act_per_sec_def * week    # Actual cost per week
    act_def_dict["act_per_mth"]   = act_per_sec_def * month   # Actual cost per month
    act_def_dict["act_per_yr"]    = act_per_sec_def * year    # Actual cost per year
    fed_def_dict["fed_per_sec"]   = fed_per_sec_def           # FDS cost per second
    fed_def_dict["fed_per_min"]   = fed_per_sec_def * minute  # FDS cost per minute
    fed_def_dict["fed_per_hr"]    = fed_per_sec_def * hour    # FDS cost per hour
    fed_def_dict["fed_per_day"]   = fed_per_sec_def * day     # FDS cost per day
    fed_def_dict["fed_per_wk"]    = fed_per_sec_def * week    # FDS cost per week
    fed_def_dict["fed_per_mth"]   = fed_per_sec_def * month   # FDS cost per month
    fed_def_dict["fed_per_yr"]    = fed_per_sec_def * year    # FDS cost per year
    full_def_dict["full_per_sec"] = full_per_sec_def          # Full cost per second
    full_def_dict["full_per_min"] = full_per_sec_def * minute # Full cost per minute
    full_def_dict["full_per_hr"]  = full_per_sec_def * hour   # Full cost per hour
    full_def_dict["full_per_day"] = full_per_sec_def * day    # Full cost per day
    full_def_dict["full_per_wk"]  = full_per_sec_def * week   # Full cost per week
    full_def_dict["full_per_mth"] = full_per_sec_def * month  # Full cost per month
    full_def_dict["full_per_yr"]  = full_per_sec_def * year   # Full cost per year
    
    return act_def_dict, fed_def_dict, full_def_dict          # return cost dictionaries. 

# Save data for site output into .py file to be imported into flask application
def save_static_data(cost_dict, dts_list):
    dlist              = [float(i) for i in dts_list]         # Convert each item in download list to float
    avg_down           = np.average(dlist)/b2mb               # Calculate avaerage download speed for site output 
    now                = datetime.now()                       # Get current time
    dt_string          = now.strftime("%m-%d-%Y %I:%M:%S %p") # Output current time in 12HR format
    cost_dict_filename = 'cost_dict.py'                       # Set output file name
    cost_dict_file     = open(cost_dict_filename, 'w')        # Open output file
    cost_dict_file.write(f"costDict = {cost_dict}")           # Write cost dictionary to line in output file
    cost_dict_file.write(f"\nlastUpdate = '{dt_string}'")     # Write timestamp as variable on new line in output file
    cost_dict_file.write(f"\navgDown = {'%.2f' % avg_down}")  # Write average download speed as variable on new line as output file
    cost_dict_file.close()                                    # close output file


def plot_data(dts_df):
    dlist     = [] # Create empty list to convert download speeds to float values                          
    pkdlist   = [] # Create empty list to store package download speed for plotting
    time_list = [] # Create empty list to store time data for plotting
    #pkulist  = [] # Create empty list to stor package upload speed for plotting(currently not enabled)
    dwnlist  = dts_df[['Download']].values     # Get list of download speeds to use as string
    avglist  = dts_df[['Download']].values     # Get list of download speeds for use in averaging download speeds(and upload speeds when enabled)
    alist    = [float(i) for i in avglist]     # Convert avglist data to float
    avg_down = np.average(alist)/b2mb          # Calculate average download speed for output to plot
    for spd in dwnlist:                        # Get each speed in dwnlist
        dlist.append(float(spd) / b2mb)        # Divide download speed by 1000 to convert from bps to Mbps
    dlist     = dlist[-72:]                    # Create a list of the last 72 speed tests
    #uplist   = dts_df[['Upload']].values/b2mb # Divide upload speed by 1000 to cohvert from bps to Mbps(not enabled)
    xrange    = len(dlist)                     # Create range from length of dlist
    for i in range(xrange):                    # Create a list of package speeds for plotting
        time_list.append((i*20)/60)            # Create x axis(time)list
        pkdlist.append(1000)                   # Create y axis (download speeds) list
        # pkulist.append(35)                   # Create x axix (upload speeds) list (not enabled)
    
    # The following code just formats and plots the above data and saves the image as a png for use in a flask-app
    plt.style.use('seaborn-v0_8-dark')
    plt.title("Speed Test Results: Last 24 hours")
    plt.text(11, 0, f'Average Download Speed: {"%.2f" % avg_down}Mbps', bbox={
             'facecolor': 'orange', 'alpha': .3}, fontsize=10, fontweight='bold', verticalalignment='bottom', horizontalalignment='left')
    plt.xlabel("Time in Hours")
    plt.ylabel("Download Speed in Mbps")
    plt.plot(time_list, dlist, label="Actual Download Speeds")
    #plt.plot(time_list, uplist, label="Actual Up Speeds")
    plt.plot(time_list, pkdlist, label="Package Download Speeds")
    #plt.plot(time_list,pkulist, label="Package Up Speeds")
    plt.legend(loc='upper left')
    plt.savefig('static/speeds.png')


# Run the application 
if __name__ == "__main__":
    dts_df    = get_daily_speed_data()      # Get data from the server
    dts_list  = dts_df[['Download']].values # Put data in a list
    cost_dict = gen_def_dict(dts_list)      # Calculate data and output dictionaries
    save_static_data(cost_dict, dts_list)   # Save date to static file
    plot_data(dts_df)                       # Create and save graph image
