const socket = new WebSocket("ws://localhost:8765");

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);

    document.getElementById("result").textContent =
        "Result: " + data.result;
};

function calculate() {

    const data = {
        a: document.getElementById("a").value,
        b: document.getElementById("b").value,
        op: document.getElementById("op").value
    };

    socket.send(JSON.stringify(data));
}
