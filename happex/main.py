import json
from flask import render_template
from happex import app
import matplotlib
import io

matplotlib.use("agg")

from matplotlib import pyplot


def best_fit(X, Y):
    xbar = sum(X) / len(X)
    ybar = sum(Y) / len(Y)
    n = len(X)  # or len(Y)
    numer = sum([xi * yi for xi, yi in zip(X, Y)]) - n * xbar * ybar
    denum = sum([xi ** 2 for xi in X]) - n * xbar ** 2
    b = numer / denum
    a = ybar - b * xbar
    return a, b


def line_plot(query, xlabel, ylabel):
    data = io.BytesIO()

    x, y = app.db.get_graph(query)
    a, b = best_fit(x, y)

    pyplot.scatter(x, y)
    yfit = [a + b * xi for xi in x]

    pyplot.plot(x, yfit)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)
    pyplot.savefig(data, format="png")
    pyplot.clf()
    return data


@app.route("/")
def index():
    scores = [[x[0], float(x[1])] for x in app.db.get_all_scores()]
    return render_template("index.html", data=scores)


@app.route("/social_ladder")
def social_ladder():
    return render_template("social_ladder.html")


@app.route("/social_ladder/graph.png")
def get_ladder_graph():
    data = line_plot(
        "select lifeladder, socialsupport from happy where lifeladder is not null and socialsupport is not null;",
        "Social Support",
        "Life Ladder",
    )
    return data.getvalue(), 200, {"Content-Type": "image/png"}


@app.route("/confidence")
def confidence():
    return render_template("confidence.html")


@app.route("/confidence/graph.png")
def get_conf_graph():
    data = line_plot(
        "select lifeladder, confidence from happy where lifeladder is not null and confidence is not null;",
        "Confidence in Government",
        "Life Ladder",
    )
    return data.getvalue(), 200, {"Content-Type": "image/png"}


@app.route("/democracy")
def democracy():
    return render_template("democracy.html")


@app.route("/democracy/graph.png")
def get_dem_graph():
    data = line_plot(
        "select lifeladder, democraticquality from happy where lifeladder is not null and democraticquality is not null;",
        "Democratic Quality",
        "Life Ladder",
    )
    return data.getvalue(), 200, {"Content-Type": "image/png"}


@app.route("/generosity")
def generosity():
    return render_template("generosity.html")


@app.route("/generosity/graph.png")
def get_gen_graph():
    data = line_plot(
        "select paffect, generosity from happy where paffect is not null and generosity is not null;",
        "Positive Affect",
        "Generosity",
    )
    return data.getvalue(), 200, {"Content-Type": "image/png"}


@app.route("/naffect")
def naffect():
    return render_template("naffect.html")


@app.route("/naffect/graph.png")
def get_naffect_graph():
    data = line_plot(
        "select naffect, generosity from happy where naffect is not null and generosity is not null;",
        "Negative Affect",
        "Generosity",
    )
    return data.getvalue(), 200, {"Content-Type": "image/png"}


@app.route("/country/<ctry>")
def get_country(ctry):
    rows = app.db.get_country(ctry)

    if not rows:
        return f"<h1>No data available</h1>"

    average = lambda i: round(
        sum([x[i] for x in rows if x[i] is not None])
        / len([x[i] for x in rows if x[i] is not None]),
        2,
    )

    name = rows[0][0]

    # Add world averages for context?
    ladder = average(2)
    lifeexpect = average(3)
    socialsupport = average(4)
    generosity = average(5)
    paffect = average(6)
    delivery = average(7)
    corruption = average(8)

    return render_template(
        "country.html",
        code=ctry,
        name=name,
        ladder=ladder,
        lifeexpect=lifeexpect,
        socialsupport=socialsupport,
        generosity=generosity,
        paffect=paffect,
        deliveryquality=delivery,
        corruption=corruption,
    )


@app.route("/country/<ctry>/graph.png")
def get_country_graph(ctry):
    rows = app.db.get_country(ctry)

    data = io.BytesIO()

    pyplot.plot([x[1] for x in rows], [float(x[2]) for x in rows])
    pyplot.axis([2005, 2018, 0, 10])
    pyplot.savefig(data, format="png")
    pyplot.clf()

    return data.getvalue(), 200, {"Content-Type": "image/png"}
