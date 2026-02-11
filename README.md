

# 📄 FastAPI WebSocket Chat App Documentation

## 💬 Real-Time 2-Person Chat Using FastAPI + WebSockets

This is a simple real-time chat application built using:

* **FastAPI**
* **WebSockets**
* **HTML + JavaScript frontend**
* Optional **Ngrok** for public access

---

---

# ✅ Features

* Two or more users can chat in real time
* Messages are broadcast instantly
* Works on:

  * Same machine (localhost)
  * Same Wi-Fi network
  * Any device globally using ngrok

---

---

# 📦 Requirements

Make sure you have:

* Python 3.8+
* pip installed

---

---

# ⚙️ Setup Instructions

## Step 1: Clone or Copy Project

Create a folder:

```bash
mkdir fastapi-chat
cd fastapi-chat
```

Create a file:

```
main.py
```

Paste the full chat code inside.

---

---

## Step 2: Install Dependencies

Run:

```bash
pip install fastapi uvicorn
```

---

---

# ▶️ Running the Chat App Locally

## Step 3: Start FastAPI Server

Run:

```bash
uvicorn main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## Step 4: Open Chat Page

Open browser and visit:

```
http://localhost:8000/chat
```

---

## Step 5: Chat With Yourself (Testing)

Open the same link in two tabs:

* Tab 1 = Person A
* Tab 2 = Person B

Type messages and chat instantly.

---

---

# 🌐 Running Chat Across Devices (Same Wi-Fi)

## Step 6: Run Server for Network Access

Start server like this:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Step 7: Find Your Local IP Address

### Linux / Ubuntu:

```bash
ip a
```

Look for something like:

```
192.168.1.10
```

---

## Step 8: Open Chat From Other Device

On another phone/laptop connected to same Wi-Fi, open:

```
http://192.168.1.10:8000/chat
```

Now both devices can chat.

---

---

# 🌍 Running Chat From Anywhere Using Ngrok

Ngrok exposes your local server publicly.

---

## Step 9: Install Ngrok

### Linux:

```bash
sudo snap install ngrok
```

Or download from [https://ngrok.com](https://ngrok.com)

---

## Step 10: Login to Ngrok (One-Time)

```bash
ngrok config add-authtoken YOUR_TOKEN
```

---

## Step 11: Start FastAPI Server

Run:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Step 12: Start Ngrok Tunnel

Open a new terminal and run:

```bash
ngrok http 8000
```

You will see:

```
Forwarding https://xxxx.ngrok-free.dev -> http://localhost:8000
```

---

## Step 13: Share Public Chat Link

Now anyone can open:

```
https://xxxx.ngrok-free.dev/chat
```

And chat from anywhere 🌍💬

---

---

# ⚠️ Important WebSocket Fix for HTTPS

The JavaScript code automatically chooses correct protocol:

```javascript
let protocol = location.protocol === "https:" ? "wss" : "ws";
let ws = new WebSocket(`${protocol}://${location.host}/ws`);
```

This ensures:

* Localhost → ws://
* Ngrok HTTPS → wss://

---

---

# 📌 Notes

* This project stores messages in memory (no database)
* If server stops, chat stops
* Ngrok free link changes every restart

---

---

# 🚀 Future Improvements

You can extend this project by adding:

* User join/leave notifications
* Private rooms
* Message history (PostgreSQL)
* Authentication (JWT)
* React frontend UI

---

---

# ✅ Quick Commands Summary

| Task               | Command                                       |
| ------------------ | --------------------------------------------- |
| Install packages   | `pip install fastapi uvicorn`                 |
| Run locally        | `uvicorn main:app --reload`                   |
| Run on Wi-Fi       | `uvicorn main:app --host 0.0.0.0 --port 8000` |
| Start ngrok tunnel | `ngrok http 8000`                             |



