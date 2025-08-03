document.getElementById("uploadForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    let fileInput = document.getElementById("resumeInput").files[0];

    if (!fileInput) {
        showError("⚠️ Please upload a file first!");
        return;
    }

    let formData = new FormData();
    formData.append("resume", fileInput);

    try {
        let response = await fetch("/", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        let result = await response.json();
        showResult(result.result);
    } catch (error) {
        console.error("Error:", error);
        showError(`⚠️ ${error.message}`);
    }
});

function showResult(result) {
    let resultBox = document.getElementById("result");
    resultBox.innerHTML = `<div class="highlighted-text">${result.replace(/\n/g, "<br>")}</div>`;
}

function showError(message) {
    let resultBox = document.getElementById("result");
    resultBox.innerHTML = `<div class="error-text">${message}</div>`;
}


 
 
 