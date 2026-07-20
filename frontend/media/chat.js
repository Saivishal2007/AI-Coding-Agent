const vscode = acquireVsCodeApi();

const chat = document.getElementById("chat");
const prompt = document.getElementById("prompt");
const send = document.getElementById("send");

let thinkingMessage = null;

// =========================
// Send Prompt
// =========================

async function sendPrompt() {

    const text = prompt.value.trim();

    if (!text)
        return;

    addMessage(text, "user");

    prompt.value = "";

    autoResize();

    // Disable UI while AI is working
    send.disabled = true;

    prompt.disabled = true;

    send.textContent = "Thinking...";

    showThinking();

    vscode.postMessage({

        command: "sendPrompt",

        prompt: text

    });

}

send.addEventListener("click", sendPrompt);

// Ctrl + Enter

prompt.addEventListener("keydown", (e) => {

    if (e.key === "Enter" && e.ctrlKey) {

        e.preventDefault();

        sendPrompt();

    }

});

// Auto resize textarea

prompt.addEventListener("input", autoResize);

function autoResize() {

    prompt.style.height = "0px";

    prompt.style.height = prompt.scrollHeight + "px";

}

// =========================
// Receive Backend Messages
// =========================

window.addEventListener("message", (event) => {

    const message = event.data;

    hideThinking();

    // Re-enable UI

    send.disabled = false;

    prompt.disabled = false;

    send.textContent = "Send";

    prompt.focus();

    switch (message.type) {

        case "response":

            addAIMessage(message.response);

            break;

        case "edit_preview":

            addEditPreview(

                message.preview,

                message.editId

            );

            break;

        case "edit_files_preview":

            addMultiplePreview(

                message.previews,

                message.editId

            );

            break;

        case "apply_success":

            document.querySelectorAll(".edit-card").forEach(card => {

                card.remove();

            });

            addAIMessage("✅ Edit applied successfully.");

            break;

        default:

            addAIMessage(

                message.response ||

                "Unknown response."

            );

    }

});

// =========================
// Message Rendering
// =========================

function addMessage(text, type) {

    const wrapper = document.createElement("div");

    wrapper.className = "message " + type;

    const avatar = document.createElement("div");

    avatar.className = "avatar";

    avatar.textContent =
        type === "user"
            ? "👤"
            : "🤖";

    const bubble = document.createElement("div");

    bubble.className = "bubble";

    bubble.textContent = text;

    const footer = document.createElement("div");

    footer.className = "message-footer";

    footer.textContent = getCurrentTime();

    wrapper.appendChild(avatar);

    wrapper.appendChild(bubble);

    chat.appendChild(wrapper);

    chat.appendChild(footer);

    scrollBottom();

}

function addAIMessage(text) {

    const wrapper = document.createElement("div");

    wrapper.className = "message ai";

    const avatar = document.createElement("div");

    avatar.className = "avatar";

    avatar.textContent = "🤖";

    const bubble = document.createElement("div");

    bubble.className = "bubble";

    bubble.textContent = text;

    wrapper.appendChild(avatar);

    wrapper.appendChild(bubble);

    chat.appendChild(wrapper);

    const footer = document.createElement("div");

    footer.className = "message-footer";

    footer.textContent = getCurrentTime();

    chat.appendChild(footer);

    addCopyButtons();

    highlightAll();

    scrollBottom();

}

// =========================
// Thinking Message
// =========================

function showThinking() {

    thinkingMessage = document.createElement("div");

    thinkingMessage.className = "message ai";

    thinkingMessage.id = "thinking";

    const avatar = document.createElement("div");

    avatar.className = "avatar";

    avatar.textContent = "🤖";

    const bubble = document.createElement("div");

    bubble.className = "bubble thinking";

    bubble.innerHTML = `

        <div class="thinking-text">

            Thinking...

        </div>

        <div class="thinking-sub">

            Analyzing your repository

        </div>

    `;

    thinkingMessage.appendChild(avatar);

    thinkingMessage.appendChild(bubble);

    chat.appendChild(thinkingMessage);

    scrollBottom();

}

function hideThinking() {

    if (thinkingMessage) {

        thinkingMessage.remove();

        thinkingMessage = null;

    }

}

// =========================
// Code Block Buttons
// =========================

function addCopyButtons() {

    const blocks = document.querySelectorAll("pre");

    blocks.forEach(pre => {

        if (pre.querySelector(".copy-btn"))
            return;

        const button = document.createElement("button");

        button.className = "copy-btn";

        button.textContent = "📋 Copy";

        button.onclick = () => {

            navigator.clipboard.writeText(pre.innerText);

            button.textContent = "✅ Copied";

            setTimeout(() => {

                button.textContent = "📋 Copy";

            }, 1500);

        };

        pre.style.position = "relative";

        pre.appendChild(button);

    });

}

// =========================
// Highlight.js
// =========================

function highlightAll() {

    if (typeof hljs === "undefined")
        return;

    document
        .querySelectorAll("pre code")
        .forEach((block) => {

            hljs.highlightElement(block);

        });

}

// =========================
// Edit Preview Card
// =========================

function addEditPreview(preview, editId) {

    const wrapper = document.createElement("div");

    wrapper.className = "edit-card";

    wrapper.innerHTML = `

        <div class="edit-title">
            📝 Proposed Changes
        </div>

        <div class="file-name">
            📄 ${preview.path}
        </div>

        <pre>${preview.diff}</pre>

    `;

    const actions = document.createElement("div");

    actions.className = "edit-actions";

    const applyButton = document.createElement("button");

    applyButton.className = "apply-btn";

    applyButton.textContent = "✅ Apply";

    applyButton.onclick = () => {

        applyButton.disabled = true;

        applyButton.textContent = "Applying...";

        vscode.postMessage({

            command: "applyEdit",

            editId

        });

    };

    const cancelButton = document.createElement("button");

    cancelButton.className = "cancel-btn";

    cancelButton.textContent = "❌ Cancel";

    cancelButton.onclick = () => {

        wrapper.remove();

    };

    actions.appendChild(applyButton);

    actions.appendChild(cancelButton);

    wrapper.appendChild(actions);

    chat.appendChild(wrapper);

    scrollBottom();

}

// =========================
// Welcome Screen
// =========================

if (chat.children.length === 0) {

    const welcome = document.createElement("div");

    welcome.className = "welcome";

    welcome.innerHTML = `

        <h2>👋 Welcome</h2>

        <p>

            Ask me anything about your repository.

        </p>

        <div class="suggestions">

            <button onclick="quickPrompt('Explain this project')">

                Explain Project

            </button>

            <button onclick="quickPrompt('Review the architecture')">

                Review Architecture

            </button>

            <button onclick="quickPrompt('Find bugs')">

                Find Bugs

            </button>

            <button onclick="quickPrompt('Optimize this code')">

                Optimize

            </button>

        </div>

    `;

    chat.appendChild(welcome);

}

window.quickPrompt = function(text) {

    prompt.value = text;

    prompt.focus();

};

// =========================
// Helpers
// =========================

function scrollBottom() {

    requestAnimationFrame(() => {

        chat.scrollTo({

            top: chat.scrollHeight,

            behavior: "smooth"

        });

    });

}

function getCurrentTime() {

    return new Date().toLocaleTimeString([], {

        hour: "2-digit",

        minute: "2-digit"

    });

}

// =========================
// Multiple File Preview
// =========================

function addMultiplePreview(previews, editId) {

    const wrapper = document.createElement("div");

    wrapper.className = "edit-card";

    wrapper.innerHTML = `

        <div class="edit-title">

            📝 Multiple File Changes

        </div>

    `;

    previews.forEach(preview => {

        const file = document.createElement("div");

        file.className = "multi-file";

        file.innerHTML = `

            <div class="file-name">

                📄 ${preview.path}

            </div>

            <pre>${preview.diff}</pre>

        `;

        wrapper.appendChild(file);

    });

    const actions = document.createElement("div");

    actions.className = "edit-actions";

    const apply = document.createElement("button");

    apply.className = "apply-btn";

    apply.textContent = "✅ Apply All";

    apply.onclick = () => {

        apply.disabled = true;

        apply.textContent = "Applying...";

        vscode.postMessage({

            command: "applyEdit",

            editId

        });

    };

    const cancel = document.createElement("button");

    cancel.className = "cancel-btn";

    cancel.textContent = "❌ Cancel";

    cancel.onclick = () => {

        wrapper.remove();

    };

    actions.appendChild(apply);

    actions.appendChild(cancel);

    wrapper.appendChild(actions);

    chat.appendChild(wrapper);

    scrollBottom();

}