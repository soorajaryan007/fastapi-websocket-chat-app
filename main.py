from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

clients = []

# =======================
# FULL HTML + CSS + JS UI
# =======================
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat App</title>

    <style>
        body {
            margin: 0;
            font-family: "Segoe UI", sans-serif;
            background: linear-gradient(to right, #f8f9fa, #e9ecef);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        .chat-container {
            width: 95%;
            max-width: 500px;
            height: 92vh;
            background: white;
            border-radius: 18px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .chat-header {
            background: #343a40;
            color: white;
            padding: 15px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
        }

        .chat-body {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            background: #f1f3f5;
        }

        .chat-body li {
            list-style: none;
            background: white;
            margin: 10px 0;
            padding: 10px 14px;
            border-radius: 12px;
            max-width: 85%;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            font-size: 15px;
            word-wrap: break-word;
        }

        img {
            max-width: 220px;
            border-radius: 12px;
            margin-top: 6px;
        }

        .chat-footer {
            padding: 12px;
            background: white;
            display: flex;
            flex-direction: column;
            gap: 10px;
            border-top: 1px solid #ddd;
        }

        input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 10px;
            font-size: 15px;
            outline: none;
        }

        input:focus {
            border-color: #007bff;
        }

        .send-row {
            display: flex;
            gap: 10px;
        }

        button {
            flex-shrink: 0;
            padding: 12px 18px;
            border: none;
            border-radius: 10px;
            background: #007bff;
            color: white;
            font-size: 15px;
            cursor: pointer;
            transition: 0.2s;
        }

        button:hover {
            background: #0056b3;
        }

        @media (max-width: 500px) {
            .chat-container {
                height: 100vh;
                border-radius: 0;
            }
        }
    </style>
</head>

<body>

<div class="chat-container">

    <!-- HEADER -->
    <div class="chat-header">
        💬 FastAPI WebSocket Chat (Text + Image)
    </div>

    <!-- CHAT AREA -->
    <ul class="chat-body" id="chat"></ul>

    <!-- INPUT AREA -->
    <div class="chat-footer">

        <input id="username" type="text" placeholder="Enter your name..." />

        <div class="send-row">
            <input id="msg" type="text" placeholder="Type message..." />
            <button onclick="sendMessage()">Send</button>
        </div>

        <input type="file" id="imageInput" accept="image/*" />
        <button onclick="sendImage()">Send Image</button>

    </div>
</div>

<script>
    let protocol = location.protocol === "https:" ? "wss" : "ws";
    let ws = new WebSocket(`${protocol}://${location.host}/ws`);

    // ==========================
    // RECEIVE MESSAGE
    // ==========================
    ws.onmessage = function(event) {

        let chat = document.getElementById("chat");
        let message = JSON.parse(event.data);

        let item = document.createElement("li");

        // TEXT MESSAGE
        if (message.type === "text") {
            item.textContent = message.user + ": " + message.data;
        }

        // IMAGE MESSAGE
        if (message.type === "image") {
            item.innerHTML = `
                <b>${message.user}:</b><br>
                <img src="${message.data}">
            `;
        }

        chat.appendChild(item);

        // Auto Scroll
        chat.scrollTop = chat.scrollHeight;
    };

    // ==========================
    // SEND TEXT MESSAGE
    // ==========================
    function sendMessage() {

        let user = document.getElementById("username").value;
        let msg = document.getElementById("msg").value;

        if (user.trim() === "" || msg.trim() === "") return;

        ws.send(JSON.stringify({
            type: "text",
            user: user,
            data: msg
        }));

        document.getElementById("msg").value = "";
    }

    // ==========================
    // SEND IMAGE MESSAGE
    // ==========================
    function sendImage() {

        let user = document.getElementById("username").value;
        let fileInput = document.getElementById("imageInput");

        if (user.trim() === "") {
            alert("Enter your name first!");
            return;
        }

        if (fileInput.files.length === 0) return;

        let file = fileInput.files[0];
        let reader = new FileReader();

        reader.onload = function() {

            ws.send(JSON.stringify({
                type: "image",
                user: user,
                data: reader.result
            }));
        };

        reader.readAsDataURL(file);

        fileInput.value = "";
    }
</script>

</body>
</html>
"""

# =======================
# ROUTE TO OPEN CHAT PAGE
# =======================
@app.get("/chat")
def chat_page():
    return HTMLResponse(html)


# =======================
# WEBSOCKET CONNECTION
# =======================
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    clients.append(ws)

    try:
        while True:
            data = await ws.receive_text()

            # Broadcast to all clients
            for client in clients:
                await client.send_text(data)

    except WebSocketDisconnect:
        clients.remove(ws)
        print("Client disconnected")
