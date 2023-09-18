console.log('Hello world!')

// const ws = new WebSocket('ws://localhost:8080')

const formChat = document.getElementById("formChat")
const subscribe = document.getElementById("subscribe")
const submit = document.getElementById("submit")

// formChat.addEventListener('submit', (e) => {
//   e.preventDefault()
//   ws.send(textField.value)
//   textField.value = null
// })

// ws.onopen = (e) => {
//   console.log('Hello WebSocket!')
// }

// ws.onmessage = (e) => {
//   console.log(e.data)
//   text = e.data

//   const elMsg = document.createElement('div')
//   elMsg.textContent = text
//   subscribe.appendChild(elMsg)
// }




const connect = (message) => {
  let socket = new WebSocket('ws://localhost:8080');

  socket.addEventListener('open', function (event) {
    if (message) {
      socket.send(session_id + " " + message)
    } 
  });

  socket.addEventListener('message', function (event) {
    console.log(event.data);
    text = event.data
    print_data(text)
  });

  socket.addEventListener('close', (e) => {
    console.log('Socket is closed.', e.reason);
    // print_txt(' Socket is closed.')
  })
}


function print_txt(text) {
  const elMsg = document.createElement('div')
  if (text) {
    elMsg.textContent = text
  }
  subscribe.appendChild(elMsg)
}


function print_data(text) {
  let parsed_data
  let result_txt
  if (text) {
    try {
      parsed_data = JSON.parse(text);
    } catch (e) {
    }
    if (parsed_data) {
      parsed_data.forEach((row, index) => {
        Object.entries(row).forEach(entry => {
          result_txt = ""
          const [data, courses] = entry;
          result_txt = data + " : "
          Object.entries(courses).forEach(entry => {
            const [currency, curency_data] = entry;
            result_txt += " " + currency + "(" + curency_data.sale + "/" + curency_data.purchase + ")"
          })
          print_txt(result_txt)
        })
      });
    } else {
      print_txt(text)
    }
  }
}

//connect()

// submit.addEventListener('click', (e) => {
//     connect("Click button"); 
// })

formChat.addEventListener('submit', (e) => {
  e.preventDefault()
  connect(textField.value)
  textField.value = null
})

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min) + min); 
}

session_id = Date.now() + "-" + getRandomInt(10000, 99999)
console.log("session_id",session_id)
