from cost_dict import costDict, lastUpdate, avgDown # Import data from cost_dict.py
from flask import Flask, render_template            # Import Flask data


app = Flask(__name__) # Initialize Flask


# render home page
@app.route('/') 
def index():
    #Output variables for actual, FSD, and Full cost data from cost_dict
    acps = '%.7f' % costDict[0]['act_per_sec']
    acpm = '%.5f' % costDict[0]['act_per_min']
    acph = '%.3f' % costDict[0]['act_per_hr']
    acpd = '%.2f' % costDict[0]['act_per_day']
    acpw = '%.2f' % costDict[0]['act_per_wk']
    acpmth = '%.2f' % costDict[0]['act_per_mth']
    acpy = '%.2f' % costDict[0]['act_per_yr']
    fcps = '%.7f' % costDict[1]['fed_per_sec']
    fcpm = '%.5f' % costDict[1]['fed_per_min']
    fcph = '%.3f' % costDict[1]['fed_per_hr']
    fcpd = '%.2f' % costDict[1]['fed_per_day']
    fcpw = '%.2f' % costDict[1]['fed_per_wk']
    fcpmth = '%.2f' % costDict[1]['fed_per_mth']
    fcpy = '%.2f' % costDict[1]['fed_per_yr']
    flcps = '%.7f' % costDict[2]['full_per_sec']
    flcpm = '%.5f' % costDict[2]['full_per_min']
    flcph = '%.2f' % costDict[2]['full_per_hr']
    flcpd = '%.2f' % costDict[2]['full_per_day']
    flcpw = '%.2f' % costDict[2]['full_per_wk']
    flcpmth = '%.2f' % costDict[2]['full_per_mth']
    flcpy = '%.2f' % costDict[2]['full_per_yr']
    return render_template('index.html',
                           acps=acps,
                           acpm=acpm,
                           acph=acph,
                           acpd=acpd,
                           acpw=acpw,
                           acpmth=acpmth,
                           acpy=acpy,
                           fcps=fcps,
                           fcpm=fcpm,
                           fcph=fcph,
                           fcpd=fcpd,
                           fcpw=fcpw,
                           fcpmth=fcpmth,
                           fcpy=fcpy,
                           flcps=flcps,
                           flcpm=flcpm,
                           flcph=flcph,
                           flcpd=flcpd,
                           flcpw=flcpw,
                           flcpmth=flcpmth,
                           flcpy=flcpy,
                           lastUpdate=lastUpdate,
                           avgDown=avgDown
                           )


# render about page
@app.route('/about')
def about():
    about = "About"
    return render_template("about.html", about=about)


# render disclaimer page
@app.route('/disclaimer')
def disclaimer():
    return render_template("disclaimer.html",)


# run application
if __name__ == '__main__':
    app.run()
