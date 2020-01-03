from flask import Flask, request, url_for, Response
import json
from solver import solvePuzzle, solverWrapper
from heuristicSolver import solvePuzzleHeuristic
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=["POST", "OPTIONS"])
def result():
    if request.method == "OPTIONS":
        return makeResp("")
    if request.method == "POST":
        data = json.loads(request.data.decode("utf-8"))
        w = data.get("w", None)
        if not w:
            return makeResp("No w given")
        w = int(w)

        h = data.get("h", None)
        if not h:
            return makeResp("No h given")
        h = int(h)

        x = data.get("x", None)
        if not x:
            return makeResp("No x given")

        y = data.get("y", None)
        if not y:
            return makeResp("No y given")

        solver = data.get("solver", None)
        if not solver:
            return makeResp("No Solver given")

        animation = data.get("animation", None)

        if solver == "DFS":
            if not animation:
                puzzle = solvePuzzle(w, h, x, y, 0, None, [])
                if puzzle is not None:
                    return makeResp(str(puzzle.tolist()))
                else:
                    return makeResp("No Solution")
            else:
                puzzle, temp_puzzles = solverWrapper(w, h, x, y, 0, None)
                out_puzzles = []
                if puzzle is not None:
                    for temp_puzzle in temp_puzzles:
                        out_puzzles.append(temp_puzzle.tolist())
                    return makeResp(str(out_puzzles))
                else:
                    return makeResp("No Solution")
        if solver == "heuristic":
            puzzle, temp_puzzles = solvePuzzleHeuristic(w, h, x, y)
            if puzzle is not None:
                return makeResp("No Solution")
            else:
                if not animation:
                    return makeResp(str(puzzle))
                else:
                    return temp_puzzles


def makeResp(body):
    resp = Response(body)
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = ["POST", "OPTIONS"]
    resp.headers["Access-Control-Allow-Headers"] = [
        "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"]

    return resp


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
