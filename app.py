from flask import Flask , render_template , request


import pickle

import math

from pycricbuzz import Cricbuzz

from datetime import datetime

import psycopg2

teamm = open('team_decoder.pkl',"rb")

team_decoder = pickle.load(teamm)

reg = pickle.load(open('reg.pkl',"rb"))

c = Cricbuzz()

livetime = "19:40"

endtime = "24:00"

matches = c.matches()

x = datetime.now()

c_time = x.strftime("%H:%M")
    

#Getting the MAtch id

def mid():
    for ma in matches:
        if "Indian Premier League 2020" in ma["srs"]:
            return (ma["id"])
        else :
            return "None"

#livescore
def livescore():
    global id
    id = mid()
    if id == "None":
        return "No Score"
    else :
        lscore = c.livescore(id)
        return lscore
    
#Scorecard
def scorecard():
    lscore = livescore()
    if c_time > livetime and lscore != "No Score":
        overs1 = float(lscore["batting"]["score"][0]["overs"])
        return overs1
    else :
        return 0

overs1 = scorecard()


def team_de(team):
    code =  team_decoder.transform([team])
    return code[0]
    
def PS(Runs,Overs):
    a = math.modf(Overs)
    RR = Runs/(a[1] + (a[0]/0.6))
    RR = round(RR,2)
    RO = (20 - Overs) - 0.4
    RO = round(RO,1)
    ab = math.modf(RO)
    ROA = ab[1]  + ab[0]/0.6
    PS = Runs + (ROA*RR)
    PS = round(PS)
    return PS


def Check(score,wickets,overs,striker,non_Striker):
    if score <= 220 and wickets < 10 and  overs  < 20 and  math.modf(overs)[0] <= 0.5 and (striker + non_Striker) <= score and score >= 0 and wickets >= 0 and  overs  >= 0 and  striker  >= 0 and  non_Striker >= 0:
        return "good"
    else:
        return "bad"
    
def Check1(Overs,Runs):
    if Overs <= 20 and Runs < 300 and Overs >= 0 and Runs >= 0:
        return "good"
    else:
        return "bad"


application = app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST" and "overs" in request.form:
        overs = float(request.form.get("overs"))
        bat = str(request.form.get("batting_team"))
        score = float(request.form.get("score"))
        striker = float(request.form.get("striker"))
        non_Striker = float(request.form.get("non_Striker"))
        wickets = float(request.form.get("wickets"))        
        bat1 = team_de(bat)
        che = Check(score,wickets,overs,striker,non_Striker)
        if che == "good":
            score = reg.predict([[bat1,score,wickets,overs,striker,non_Striker]])
            score = round(score[0],0)
            Score2 = f'Predicted Score : {score}'
            #data_entry_D(score,wickets,overs,bat,striker,non_Striker,score)
            return render_template("index.html", bmi = Score2)
        else:
            Score3 = "Recheck the info entered"
            return render_template("index.html", bmi = Score3)        
    if request.method == "POST" and "Overs_1" in request.form:
        Over = float(request.form.get("Overs_1"))
        runs = float(request.form.get("Runs_1"))
        chec = Check1(Over,runs)
        if chec == "good":
            Score = PS(runs,Over)
            Score1 = f'Predicted Score : {Score}'
            #data_entry_RR(runs,Over,Score)
            return render_template("index.html", bmi = Score1)
        else:
            Score4 = "Recheck the info entered"
            return render_template("index.html", bmi = Score4)
        
    return render_template("index.html")

@app.route("/livescore", methods=['GET', 'POST'])
def home1():
    if overs1 < 20 and overs1 >= 0 and c_time >= livetime and c_time < endtime:
        lscore = livescore()
        overs2 = float(lscore["batting"]["score"][0]["overs"])
        score1 = float(lscore["batting"]["score"][0]["runs"])
        wickets1 = float(lscore["batting"]["score"][0]["wickets"])
        bat2 = lscore["batting"]["team"]
        bowl2 = lscore["bowling"]["team"]
        bat22 = team_de(bat2)
        stiker_score1 = float(lscore["batting"]["batsman"][0]["runs"])
        try:
            non_stiker_score1 = float(lscore["batting"]["batsman"][1]["runs"])
        except:
            non_stiker_score1 = 0
        PS_R = PS(score1,overs2)
        PS_D = reg.predict([[bat22,score1,wickets1,overs2,stiker_score1,non_stiker_score1]])
        PS_D = int(round(PS_D[0],0))
        return render_template("index1.html",bat2 = str(bat2),bowl2 = str(bowl2), score = int(score1), overs = overs2, wickets = int(wickets1), non_stiker_score= int( non_stiker_score1),stiker_score=int(stiker_score1), PS_D = PS_D, PS_R = PS_R)
    elif c_time > "20:50" and c_time < "21:50":
        lscore = livescore()
        overs2 = float(lscore["batting"]["score"][0]["overs"])
        score1 = float(lscore["batting"]["score"][0]["runs"])
        wickets1 = float(lscore["batting"]["score"][0]["wickets"])
        return render_template("index1.html", score = score1, overs = overs2, wickets = wickets1)
    else:
        return render_template("nol.html")

@app.errorhandler(ValueError)
def page(e):
    return render_template("error.html") 

if __name__ == '__main__':
    app.run(debug=True)