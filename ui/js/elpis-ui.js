const chatBox = document.getElementById("chat-box");
const messageBox = document.getElementById('message-box');
const agentResponseBox = document.getElementsByClassName("row agent-response")[0];
const userResponseBox = document.getElementsByClassName("row user-response")[0];

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
    console.log(message);
    setTimeout(addAgentResponseBox, 200);
    setTimeout(() => addUserResponse(message), 400);
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
    chatBox.appendChild(clone);
};
