const chatBox = document.getElementById("chat-box");
const messageBox = document.getElementById('message-box');
const agentResponseBox = document.getElementsByClassName("row agent-response")[0];
const userResponseBox = document.getElementsByClassName("row user-response")[0];
const agentWritingMessage = document.getElementById("agent-writing-response");

let connection;
let agentWritingBox;

const onStart = () => {
    connection = new WebSocket('ws://localhost:8000');
    // When the connection is open, send some data to the server
    connection.onopen = function () {
        console.log("Opened websocket");
    };

    // Log errors
    connection.onerror = function (error) {
        console.error('WebSocket Error ' + error);
    };

    // Log messages from the server
    connection.onmessage = function (e) {
        console.log('Server: ' + e.data);
        // Artificial timeout to simulate loading
        setTimeout(() => {
            addAgentResponseBox(e.data);
            if (agentWritingBox) {
                chatBox.removeChild(agentWritingBox);
                agentWritingBox = undefined;
            }

        }, 2000);
    };

    connection.onclose = function () {
        console.log("Closing websocket");
    }
};

const onEnterPress = (event) => {
    if (!event) event = window.event;
    const e = event.keyCode || event.which;
    if (e === 13) {
        sendMessage();
        return false;
    }
};
const sendMessage = () => {
    const message = messageBox.value;
    messageBox.value = "";
    console.log("Sending message to server", message);
    // Allow enough time for the WS to open again
    setTimeout(() => {
        if (connection.OPEN) {
            connection.send(message);
            addUserResponse(message);
            addAgentTypingBox();
        }
    }, 200);
};

const addAgentResponseBox = (text = Math.random()) => {
    const clone = agentResponseBox.cloneNode(true);
    const msg = clone.children[1].children[1];
    if (msg) {
        msg.innerHTML = text.toString();
    }
    chatBox.appendChild(clone);
};

const addUserResponse = (text = Math.random()) => {
    const clone = userResponseBox.cloneNode(true);
    const msg = clone.children[0].children[1];
    if (msg) {
        msg.innerHTML = text.toString();
    }
    clone.style.display = '';
    chatBox.appendChild(clone);
};

const addAgentTypingBox = () => {
    const clone = agentWritingMessage.cloneNode(true);
    clone.style.display = "";
    chatBox.appendChild(clone);
    agentWritingBox = clone;
};
