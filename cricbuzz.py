# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 20:00:29 2020

@author: malat
"""


from pycricbuzz import Cricbuzz

c = Cricbuzz()

import json

matches = c.matches()
print (json.dumps(matches,indent=4)) #for pretty prinitng

lscore = c.livescore("30409")
print(json.dumps(lscore, indent=4, sort_keys=True))







def mid():
    for ma in matches:
        if "Indian Premier League 2020" in ma["srs"]:
            return (ma["id"])
        
mid = mid()
lscore = c.livescore(mid)
lscore["batting"]["score"][0]["runs"]
lscore["batting"]["score"][0]["wickets"]
lscore["batting"]["score"][0]["overs"]
bat2 = lscore["batting"]["team"]

stiker_score = lscore["batting"]["batsman"][0]["runs"]
non_stiker_score = lscore["batting"]["batsman"][1]["runs"]

float(overs)








