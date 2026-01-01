async function uploadPDF() {
    const fileInput = document.getElementById("pdfFile");
    const output = document.getElementById("output");
    const loader = document.getElementById("loader");
    const mode = document.getElementById("mode").value;

    if (!fileInput.files.length) {
        alert("Please select a PDF file.");
        return;
    }

    const formData = new FormData();
    formData.append("mode", mode);

    loader.classList.remove("hidden");
    output.innerHTML = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/summarize-pdf", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            const err = await response.text();
            console.error(err);
            throw new Error("Backend error");
        }

        const data = await response.json();
        output.innerText = data.summary;
    } catch (error) {
        output.innerText = "❌ Error summarizing PDF.";
    }

    loader.classList.add("hidden");
}

function formatSummary(text) {
    return text
        .replace(/OVERVIEW:/g, "<h2>Overview</h2>")
        .replace(/KEY CONCEPTS:/g, "<h2>Key Concepts</h2>")
        .replace(/FINAL TAKEAWAY:/g, "<h2>Final Takeaway</h2>")
        .replace(/- (.*)/g, "<li>$1</li>")
        .replace(/\n<li>/g, "<ul><li>")
        .replace(/<\/li>\n(?!<li>)/g, "</li></ul>")
        .replace(/\n/g, "<br>");
}
