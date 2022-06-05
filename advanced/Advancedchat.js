name = window.prompt("Enter your name");
document.getElementById("loginname").innerText = name
let messages = document.getElementById("messages")

var mymessage = document.getElementById("my-msg")

let mywebsocket = new WebSocket("ws://localhost:7000")

mywebsocket.onopen = function (){
    data_to_sent = {
        username:name,
        type: "login"
    }
    mywebsocket.send(JSON.stringify(data_to_sent))
}

// when the server receives messages
mywebsocket.onmessage = function (event){
    console.log(event.data)
    console.log(JSON.parse(event.data))
    messages.innerHTML +=event.data
}

mywebsocket.close=function (){
    console.log("Socket closed")
     data = {
           "type":"left",
           "msg":"",
           "username":name
       }
       // we need to send the data using the websocket
       // lets create websocket and use it to send the message
       mywebsocket.send(JSON.stringify(data))

}

mywebsocket.onerror = function (){
    console.log(`error happened ${name}`)
}
mymessage.addEventListener("keyup", function (ev){
    console.log(ev)
   if (ev.code==="Enter"){
       msg= mymessage.value
       data = {
           "type":"msg",
           "msg":msg,
           "username":name
       }
       messages.innerHTML+=`${name}:${msg}\n`;
       mymessage.value = "";
       // we need to send the data using the websocket
       // lets create websocket and use it to send the message
       mywebsocket.send(JSON.stringify(data))  // this asynchronous ---> so this will send error
       // as it will try to send the data before the connection opened.
    }

});