async function sendMessage() {
    let userMessageInput = document.getElementById("userMessage");
    let userMessage = userMessageInput.value.trim();
    if (!userMessage) return; // Prevent empty messages

    let chatBox = document.getElementById("chatBox");

    // ✅ Prevent duplicate messages by disabling the input temporarily
    userMessageInput.disabled = true;

    // Append user message once
    chatBox.innerHTML += `<p><b>You:</b> ${userMessage}</p>`;

    try {
        // ✅ Use relative path to avoid cross-origin issues
        let response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userMessage })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        let responseData = await response.json();

        if (!responseData.response) {
            throw new Error("No response received from chatbot.");
        }

        chatBox.innerHTML += `<p><b>Bot:</b> ${responseData.response}</p>`;

    } catch (error) {
        console.error("Error:", error);
        chatBox.innerHTML += `<p style="color: red;"><b>Error:</b> Chatbot is not responding.</p>`;
    }

    // ✅ Re-enable input field after message is sent
    userMessageInput.value = "";
    userMessageInput.disabled = false;
}

// ✅ Ensure only one event listener is attached
document.getElementById("userMessage").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();  // ✅ Prevents form submission and duplicate messages
        sendMessage();
    }
});
