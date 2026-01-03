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
    formData.append("file", fileInput.files[0]);
    formData.append("mode", mode); // ✅ backend expects this

    loader.classList.remove("hidden");
    loader.innerText = "Analyzing PDF...";
    output.innerHTML = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/summarize-pdf", {
            method: "POST",
            body: formData,
        });

        // 🔍 show backend error clearly
        if (!response.ok) {
            const errText = await response.text();
            console.error("Backend error:", errText);
            throw new Error(errText);
        }

        const data = await response.json();
        loader.innerText = "Generating summary...";
        console.log("Backend response:", data); // 👈 DEBUG LINE

        // ✅ FIX: backend returns `summary`
        output.innerHTML = formatSummary(data.summary);

    } catch (error) {
        console.error("Frontend error:", error);
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
