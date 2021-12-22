import conflictserializable as cs

fig = cs.draw_graph('R1(A), W2(B), R3(C), W3(A), R4(D), R4(B), W1(D), W2(C)')
fig.show()


def index():
    schedule = request.args.get("schedule", "")
    if schedule:
        if check_schedule(schedule) == 'The input schedule is invalid, please try again':
            return (
                    """<form action="" method="get">
						Input schedule: <input type="text" name="schedule">
						<input type="submit" value="Check conflict-serializable">
					</form>"""
                    + "Result: "
            )
        else:
            schedule_result = check_schedule(schedule)
            fig = draw_graph(schedule)
            buf = BytesIO()
            fig.savefig(buf, format="png")
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
