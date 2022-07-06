from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)
playerlist = []
file = pd.read_csv("nba.csv")
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        p1 = request.form["p1"]
        p2 = request.form["p2"]
        if p1 == "" or p2 == "" or p1 == p2:
            return render_template("index.html", playerlist=get_playerlist())
        else:
            return redirect(url_for("compare", p1=p1, p2=p2))
    else:
        return render_template("index.html", playerlist=get_playerlist())
@app.route("/<p1>/<p2>")
def compare(p1, p2):
    fname1 = "images/" + p1.split()[0] + "_" + p1.split()[1] + ".png"
    src1 = url_for('static', filename=fname1)
    fname2 = "images/" + p2.split()[0] + "_" + p2.split()[1] + ".png"
    src2 = url_for('static', filename=fname2)
    p1 = file.loc[file['Name'] == p1]
    p2 = file.loc[file['Name'] == p2]
    return render_template("compare.html", p1=p1, p2=p2, src1=src1, src2=src2)
def get_playerlist():
    if playerlist == []:
        file.sort_values(by=['PTS'], axis=0, ascending=[False], inplace=True)
        for index, row in file.iterrows():
            playerlist.append(row[1])
    return playerlist
if __name__ == "__main__":
    app.run(debug=True)