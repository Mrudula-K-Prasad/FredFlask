from fredapi import Fred
from flask import Flask, render_template, request
import re
from datetime import date
import pandas as pd
global start_date, end_date

api_key = "f9aaecd910d743d83207db70c1e90204"
fred = Fred(api_key=api_key)

            

def get_fred_data(phrase):
    data = fred.search(phrase)
    series_ids = list(data.iloc[:10].index)
    # desc = list(data.iloc[:10]['notes'])
    
    title = [fred.get_series_info(i)['title'] for i in series_ids]


    data_dict = {}
    for i in range (len(series_ids)):
        data_dict[series_ids[i]] = title[i]
    return data_dict


app = Flask('Fred data')


@app.route('/fred_data', methods=['GET', 'POST'])
def get_desc():
    global start_date, end_date
    top_10_dict = {}
    if request.method == "POST":
        desc = request.form.get('desc')
        start = request.form.get('start_date')
        y, m, d = start.split('-')
        start_date = date(int(y),int(m), int(d))
        end = request.form.get('end_date')
        y_e, m_e, d_e = end.split('-')
        end_date = date(int(y_e),int(m_e), int(d_e))
        top_10_dict = get_fred_data(desc)
    
    return render_template('res_list.html', data = top_10_dict)


@app.route('/data/', methods=['GET', 'POST'])
def get_data():
    global start_date, end_date
    url = request.args.get('id')
    df = pd.DataFrame(fred.get_series(str(url), observation_start=start_date, observation_end=end_date), columns=['data'])
    da = [d.date() for d in df['data'].index]
    data = list(df['data'])
    dict_res = {}
    for i in range(len(data)):
        dict_res[da[i]] = data[i]
    return render_template('data.html', d = dict_res)
@app.route('/')
def home():
    return render_template('fred.html')