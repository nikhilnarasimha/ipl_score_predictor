# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 21:30:17 2020

@author: malat
"""


from flask import Flask , render_template

from pycricbuzz import Cricbuzz

from datetime import datetime

c = Cricbuzz()

matches = c.matches()

x = datetime.now()

hours = x.strftime("%H")

hours = int(hours)

def mid():
    for ma in matches:
        if "Indian Premier League 2020" in ma["srs"]:
            return (ma["id"])

id = mid()

lscore = c.livescore(id)

score = lscore["batting"]["score"][0]["runs"]
wickets = lscore["batting"]["score"][0]["wickets"]
overs = int(lscore["batting"]["score"][0]["overs"])


stiker_score = lscore["batting"]["batsman"][0]["runs"]
try:
    non_stiker_score = lscore["batting"]["batsman"][1]["runs"]
except:
    non_stiker_score = 0

application = app = Flask(__name__)

@app.route("/livescore", methods=['GET', 'POST'])
def home():
    if overs < 20 and hours > 19 and hours < 24:
        
    
        return render_template("index1.html", score = score, overs = overs, wickets = wickets,non_stiker_score=non_stiker_score,stiker_score=stiker_score)

if __name__ == '__main__':
    app.run(debug=True)