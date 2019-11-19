from flask import Flask, render_template, request, session
import random
import time
import pickle

app = Flask(__name__)


@app.route("/")
def landing_page():
    curNum = random.randint(1, 1000)
    session["randomNum"] = curNum
    session["gameH2"] = "Enter Number"
    session["starttime"] = time.perf_counter()
    session["numOfTries"] = 0
    return render_template(
        "game.html", the_title="Guessing Game", data=session["gameH2"]
    )


@app.route("/guessnum", methods=["POST"])
def check_num():
    guess = int(request.form["guessed"])
    if guess == session["randomNum"]:
        session["numOfTries"] += 1
        session["endtime"] = time.perf_counter()
        session["time_taken"] = round(session["endtime"] - session["starttime"])
        return render_template(
            "winner.html",
            the_title="Well Done",
            data=session["randomNum"],
            data2=session["time_taken"],
            data3=session["numOfTries"],
        )
    elif guess < session["randomNum"]:
        session["numOfTries"] += 1
        session["gameH2"] = "Too Low"
        return render_template(
            "game.html", the_title="Try Again", data=session["gameH2"]
        )
    elif guess > session["randomNum"]:
        session["numOfTries"] += 1
        session["gameH2"] = "Too High"
        return render_template(
            "game.html", the_title="Try Again", data=session["gameH2"]
        )


@app.route("/nameentered", methods=["POST"])
def name_entered():
    namef = request.form["name"]
    timetaken = session["time_taken"]
    numoftries = session["numOfTries"]
    winnerlist = [namef, numoftries, timetaken]

    pickle_in = open("scores.pickle", "rb")
    currlist = pickle.load(pickle_in)
    pickle_in.close()
    currlist.append(winnerlist)
    pickle_out = open("scores.pickle", "wb")
    pickle.dump(currlist, pickle_out)
    pickle_out.close()
    return render_template("results.html", The_title="Results")


@app.route("/displayscores")
def display_scores():
    pickle_in = open("scores.pickle", "rb")
    currlist = pickle.load(pickle_in)
    pickle_in.close()

    def sortsecond(val):
        return val[1], val[2]

    currlist = sorted(currlist, key=sortsecond)
    return render_template("highscores.html", The_title="High Scores", data=currlist)


app.secret_key = "asdu90vdaf87v932hiurhyuasdfoysad8uf7t3g2"

if __name__ == "__main__":
    app.run(debug=True)
