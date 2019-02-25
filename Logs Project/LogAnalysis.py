#!/usr/bin/env python3
# 
# A buggy web service in need of a database.

from flask import Flask, request, redirect, url_for, render_template
from LogAnalysisDB import get_three_popular_articles,get_most_popular_author_alltime,request_lead_to_errors

app = Flask(__name__)

@app.route('/')
def index():
    news = get_three_popular_articles()
    alltime = get_most_popular_author_alltime()
    errors= request_lead_to_errors()
    return render_template("LogAnalysis.html", news = news,alltime=alltime,errors=errors)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)