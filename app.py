from flask import Flask, render_template, request
from model import recommend_gifts

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/finder")
def finder():
    return render_template("finder.html")


@app.route("/result", methods=["GET"])
def result():

    relation = request.args.get("relation")
    age = request.args.get("age")
    occasion = request.args.get("occasion")
    budget = request.args.get("budget")
    interest = request.args.get("interest")

    recommendations = recommend_gifts(
        relation,
        occasion,
        interest,
        budget,
        age
    )

    return render_template(
        "result.html",
        recommendations=recommendations.to_dict("records")
    )


if __name__ == "__main__":
    app.run(debug=True)