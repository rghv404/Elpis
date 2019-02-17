const chatBox = document.getElementById("chat-box");
const messageBox = document.getElementById('message-box');
const agentResponseBox = document.getElementsByClassName("row agent-response")[0];
const userResponseBox = document.getElementsByClassName("row user-response")[0];
const agentWritingMessage = document.getElementById("agent-writing-response");
const ipBox = document.getElementById("chat-input-box");
let connection;
let agentWritingBox;

window.onbeforeunload = function(){ 
  return 'Are you sure you want to leave?';
};

const onStart = () => {
    connection = new WebSocket('ws://localhost:8000');
    // When the connection is open, send some data to the server
    connection.onopen = function () {
        console.log("Opened websocket");
        connection.send('hi');
    };

    // Log errors
    connection.onerror = function (error) {
        console.error('WebSocket Error ' + error);
    };

    // Log messages from the server
    connection.onmessage = function (e) {
        const   message = checkConversationEnd(e);   
        console.log('Server: ' + message);
        // Artificial timeout to simulate loading
        setTimeout(() => {
            addAgentResponseBox(message);
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
            connection.send(message.trim());
            addUserResponse(message);
            addAgentTypingBox();
        }
    }, 200);
};

function checkConversationEnd(e){
    let msg = undefined;
    if(e.data.includes('Thank you for taking the evaluation.')) {
        ipBox.style.display = "none";
        agentWritingBox.style.display = "none";
        console.log("Conversation finished - Depression Question Survey Complete.")
        msg = "Based on your case, we are forwarding your request to the concerned authority with HIGH priory. Please "
        + "click on the link to be redirected to the local agent.";
    } else if(e.data.includes('If you seek professional help please dial Helpline')) {
        ipBox.style.display = "none";
        agentWritingBox.style.display = "none";
        console.log("Conversation finished - Helpline.")
    }
    else if(e.data === "EndOfChat") {
        ipBox.style.display = "none";
        agentWritingBox.style.display = "none";
        console.log("Conversation finished - Depression Question Survey Complete.");
        msg = "Based on your case, we are forwarding your request to the concerned authority with HIGHEST priory. Please "
        + "click on the link to be redirected to the local agent."; 
    }
    return msg || e.data;
}
const addAgentResponseBox = (text = Math.random()) => {
    const clone = agentResponseBox.cloneNode(true);
    const msg = clone.children[1].children[1];
    if (msg) {
        msg.innerHTML = text.toString();
    }
    clone.style.display = '';
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
