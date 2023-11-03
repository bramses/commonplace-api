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

    messages.push({ role: "system", content: "The highlight is: The greatest use of a life is to spend it on something that will outlast it. by William James." });

    /*
Certainly! Let's integrate the previous topics we discussed into the new margin note. "The greatest use of a life is to spend it on something that will outlast it" by William James. This highlights the transience of human existence and the significance of making our limited time count. It aligns with the concept of "working hard for your garden" by investing in endeavors with long-lasting impact, such as planting trees you may never see the fruit of or writing code that may not gain immediate popularity. Additionally, being a caregiver to younger individuals reflects this idea of dedicating oneself to meaningful endeavors that leave a lasting impact. By nurturing and guiding the younger generation, we contribute to shaping future lives and creating a legacy that extends beyond our own lifetime. Furthermore, the concept of cura, the appreciation of care due to our awareness of mortality, emphasizes the importance of valuing and engaging in acts of compassion and support. Recognizing the brevity of life can inspire us to cherish and make the most of our time, leaving behind a legacy of care and meaningful connections.
    */


    messages.push({ role: "user", content: "Ask me a question about this margin note they provided: 'work hard for your garden'" });


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
    let assistant_message = "";

    // Read the response stream as chunks and append them to the chat log
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      chunks += decoder.decode(value);
      chatlog.innerHTML = chunks;
      assistant_message = chunks;
    }

    // add assistant message to the chat log
    messages.push({ role: "assistant", content: assistant_message });
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

  let assistant_message = "";
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
    assistant_message = chunks;
  }

  // add assistant message to the chat log
  // chatlog.innerHTML += `<div class="message assistant">${assistant_message}</div>`;
  chatlog.scrollTop = chatlog.scrollHeight;
  messages.push({ role: "assistant", content: assistant_message });
});