from flask import Flask
from flask import request
from graph import Graph
import conflictserializable as cs
from io import BytesIO
import base64
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


app = Flask(__name__)

@app.route("/")
def index():
    schedule = request.args.get("schedule", "")
    if schedule:
        if check_schedule(schedule) == 'The input schedule is invalid, please try again':
            return (
                    """<form action="" method="get">
						Input schedule: <input type="text" name="schedule">
						<input type="submit" value="Check conflict-serializable">
					</form>"""
                    + "Result: " + 'The input schedule is invalid, please try again'
            )
        else:
            schedule_result = check_schedule(schedule)
            fig = draw_graph(schedule)
            buf = BytesIO()
            fig.savefig(buf, format="png", transparent=True)
            data = base64.b64encode(buf.getbuffer()).decode("ascii")
            return (
                    """<form action="" method="get">
					Input schedule: <input type="text" name="schedule">
					<input type="submit" value="Check conflict-serializable">
				</form>"""
                    + "Result: "
                    + schedule_result
                    + f"<img src='data:image/png;base64,{data}'/>"
            )
    else:
        schedule_result = ""
        return (
                """<form action="" method="get">
                    Input schedule: <input type="text" name="schedule">
                    <input type="submit" value="Check conflict-serializable">
                </form>"""
                + "Result: "
                + schedule_result
        )
	
	
def check_schedule(schedule):
    try:
        result = cs.check_conflict_serializable(schedule)
        return result
    except ValueError:
        return "invalid input"

def draw_graph(schedule):
	return cs.draw_graph(schedule)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
	