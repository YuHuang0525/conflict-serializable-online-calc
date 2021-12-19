from flask import Flask
from flask import request
from graph import Graph
import conflictserializable as cs

app = Flask(__name__)

@app.route("/")
def index():
    schedule = request.args.get("schedule", "")
    if schedule:
        schedule = check_schedule(schedule)
    else:
        schedule = ""
    return (
        """<form action="" method="get">
                Input schedule: <input type="text" name="schedule">
                <input type="submit" value="Check conflict-serializable">
            </form>"""
        + "Result: "
        + schedule
    )

def check_schedule(schedule):
    try:
        result = cs.check_conflict_serializable(schedule)
        return result
    except ValueError:
        return "invalid input"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
	
	