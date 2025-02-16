from flask import Flask, render_template
import requests
app = Flask(__name__)
def fetch_contests():
    contests = []
    try:
        cf_response = requests.get("https://codeforces.com/api/contest.list").json()
        if cf_response["status"] == "OK":
            for contest in cf_response["result"]:
                if contest["phase"] == "BEFORE":
                    contests.append({
                        "name": contest["name"],
                        "date": "Codeforces - " + str(contest["startTimeSeconds"])
                    })
    except Exception as e:
        print("Error fetching Codeforces data:", e)
    try:
        atcoder_response = requests.get("https://kenkoooo.com/atcoder/resources/contests.json").json()
        for contest in atcoder_response:
            contests.append({
                "name": contest["title"],
                "date": "AtCoder - " + str(contest["start_epoch_second"])
            })
    except Exception as e:
        print("Error fetching AtCoder data:", e)
    try:
        cc_response = requests.get("https://www.codechef.com/api/list/contests/all").json()
        for contest in cc_response["future_contests"]:
            contests.append({
                "name": contest["contest_name"],
                "date": "CodeChef - " + contest["contest_start_date"]
            })
    except Exception as e:
        print("Error fetching CodeChef data:", e)
    return contests
@app.route('/')
def index():
    contests = fetch_contests()
    return render_template('index.html', contests=contests)
if __name__ == '__main__':
    app.run(debug=True)