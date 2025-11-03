# HNG 13 Backend Wizards - Stage  Task
## Habit Tracker AI Agent
A motivational habit-tracking backend built with **Flask**, **SQLite**, and **ZENQuotes API**.  
Users can add, view, and mark habits as done — and get random motivational quotes every time they check their progress.

___
## Features
- Add new habits with frequency (daily, weekly, etc.)
- Get all habits with automatic motivational quotes
- Mark habits as done ✅
- Simple JSON-RPC (A2A) API for Telex integration

___
## ⚙️ Setup Instructions
```bash
# 1. Clone this repo
git clone https://github.com/Richardeze/HNG_Stage_3.git
cd HNG_Stage_3

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # on macOS/Linux
venv\Scripts\activate      # on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python database.py

# 5. Run server
python main.py
```
Then open in your browser:
http://127.0.0.1:5000/habits/&lt;username>

___
## 🔗 API ENDPOINT
**REST Endpoints**

| Method   | Endpoint             | Description |
|:----------|:---------------------|:-------------|
| **POST** | `/habits/<username>` | Add a new habit for a specific user (requires `habit` and `frequency` in JSON body). |
| **GET**  | `/habits/<username>` | Get all habits for a specific user along with a random motivational quote. |
**A2A (JSON-RPC) Endpoints for Telex**

| Method   | Endpoint           | Method Name        | Description |
|:----------|:------------------|:-------------------|:-------------|
| **POST** | `/a2a/habits`      | `habits/get`       | Fetch all habits for a given user and return them with a motivational quote. |
| **POST** | `/a2a/habits`      | `habits/add`       | Add a new habit for a user by passing `username`, `habit`, and `frequency` in `params`. |
| **POST** | `/a2a/habits`      | `habits/mark_done` | Mark a specific habit as completed for the user. |
___
## Example Requests and Responses
**Add a new Habit**  
```curl -X POST http://127.0.0.1:5000/habits/richard \
-H "Content-Type: application/json" \
-d '{"habit": "Exercise", "frequency": "daily"}'
```
**Response**
``` 
{
  "message": "Habit 'Exercise' added for user richard."
}
```
**Get All Habits**
```
curl http://127.0.0.1:5000/habits/richard
```
**Response**
```
{
  "habits": [
    {
      "habit": "Exercise",
      "frequency": "daily",
      "created_at": "2025-11-02 18:42:10",
      "reminder": "✅ You're on track!"
    }
  ],
  "motivational_quote": "\"The journey of a thousand miles begins with one step.\" - Lao Tzu"
}
```
**Telex (A2A) Example**
```
curl -X POST http://127.0.0.1:5000/a2a/habits \
-H "Content-Type: application/json" \
-d '{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "habits/get",
  "params": { "username": "richard" }
}'
```
**Response**
```
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "habits": [
      {
        "habit": "Exercise",
        "frequency": "daily",
        "reminder": "⏰ Reminder: It's time to do your 'Exercise' habit (daily)."
      }
    ],
    "motivational_quote": "\"Keep pushing forward!\" - Unknown"
  }
}
```
___
## Live API URL
You can access the deployed API here:  
https://web-production-635a.up.railway.app/habits/richard
