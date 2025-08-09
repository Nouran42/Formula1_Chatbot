const response = await fetch("http://127.0.0.1:8000/ask", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify({ question: userQuestion }),
});
const data = await response.json();
setAnswer(data.answer);
