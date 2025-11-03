from flask import Flask, request, jsonify
from habit_manager import get_user_habits_with_quote, create_user_habit
from database import mark_habit_done, create_table
import os

app = Flask(__name__)
create_table()

@app.route("/habits/<username>", methods=["GET"])
def list_habits(username):
    return jsonify(get_user_habits_with_quote(username))

@app.route("/habits/<username>", methods=["POST"])
def create_habit(username):
    data = request.get_json()
    habit_name = data.get("habit")
    frequency = data.get("frequency")
    response, status = create_user_habit(username, habit_name, frequency)
    return jsonify(response), status


@app.route("/a2a/habits", methods=["POST"])
def a2a_habits():
    try:
        # Get the JSON-RPC payload
        body = request.get_json()

        if not body or body.get("jsonrpc") != "2.0" or "id" not in body or "method" not in body:
            return jsonify({
                "jsonrpc": "2.0",
                "id": body.get("id") if body else None,
                "error": {
                    "code": -32600,
                    "message": "Invalid Request: jsonrpc must be '2.0', id and method are required"
                }
            }), 200  # Note: JSON-RPC spec expects 200 even for errors

        rpc_id = body["id"]
        method = body["method"]
        params = body.get("params", {})

        username = params.get("username")
        if not username:
            return jsonify({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32602, "message": "Missing 'username' parameter"}
            }), 200

        if method == "habits/get":
            result = get_user_habits_with_quote(username)

        elif method == "habits/add":
            habit_name = params.get("habit")
            frequency = params.get("frequency")
            if not habit_name or not frequency:
                return jsonify({
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "error": {"code": -32602, "message": "Missing 'habit' or 'frequency' parameter"}
                }), 200
            result, _ = create_user_habit(username, habit_name, frequency)

        elif method == "habits/mark_done":
            habit_name = params.get("habit")
            if not habit_name:
                return jsonify({
                    "jsonrpc": "2.0",
                    "id": rpc_id,
                    "error": {"code": -32602, "message": "Missing 'habit' parameter"}
                }), 200
            message = mark_habit_done(username, habit_name)
            result = {"message": message}

        else:
            return jsonify({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            }), 200

        return jsonify({
            "jsonrpc": "2.0",
            "id": rpc_id,
            "result": result
        })

    except Exception as e:
        return jsonify({
            "jsonrpc": "2.0",
            "id": body.get("id") if "body" in locals() else None,
            "error": {"code": -32603, "message": "Internal error", "data": str(e)}
        }), 200

@app.route("/habits/<username>/mark_done", methods=["POST"])
def mark_done(username):
    data = request.get_json()
    habit = data.get("habit")

    if not habit:
        return jsonify({"error": "Please provide what you saved habit as."}), 400

    message = mark_habit_done(username, habit)
    return jsonify({"message": message})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
