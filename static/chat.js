const form = document.querySelector("#chat-form");
const chatlog = document.querySelector("#chat-log");

const messages = [];
// run on async app load

const app = async () => {
  if (l_messages.length > 0 ) {
    // put l_messages as first messages of messages
    for (let i = 0; i < l_messages.length; i++) {
      messages.push(l_messages[i]);
    }

    messages.push({ role: "user", content: "The highlight is: The greatest use of a life is to spend it on something that will outlast it. by William James. The margin note provided was 'work hard for your garden" });

    const response = await fetch("/ingest/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ messages: messages }),
    });

    // Create a new TextDecoder to decode the streamed response text
    const decoder = new TextDecoder();

    // Set up a new ReadableStream to read the response body
    const reader = response.body.getReader();
    let chunks = "";

    // Read the response stream as chunks and append them to the chat log
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      chunks += decoder.decode(value);
      chatlog.innerHTML = chunks;
    }
  }
}

app();

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  // Get the user's message from the form
  const message = form.elements.message.value;

  // add user message to the chat log
  chatlog.innerHTML += `<div class="message user">${message}</div>`;
  chatlog.scrollTop = chatlog.scrollHeight;

  // add user message to the messages array
  messages.push({ role: "user", content: message });


  // TODO dont delete messages as new ones stream in
  // TODO assistant messages not appending correctly

  // Send a request to the Flask server with the user's message
  const response = await fetch("/ingest/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ messages: messages }),
  });

  // Create a new TextDecoder to decode the streamed response text
  const decoder = new TextDecoder();

  // Set up a new ReadableStream to read the response body
  const reader = response.body.getReader();
  let chunks = "";

  // Read the response stream as chunks and append them to the chat log
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks += decoder.decode(value);
    chatlog.innerHTML = chunks;
  }
});