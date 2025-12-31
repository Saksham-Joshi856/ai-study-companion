async function uploadPDF() {
    const fileInput = document.getElementById("pdfFile");
    const output = document.getElementById("output");
    const loader = document.getElementById("loader");

    if (!fileInput.files.length) {
        alert("Please select a PDF file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    loader.classList.remove("hidden");
    output.innerHTML = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/summarize-pdf", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        output.innerText = data.summary;
    } catch (error) {
        output.innerText = "❌ Error summarizing PDF.";
    }

    loader.classList.add("hidden");
}
