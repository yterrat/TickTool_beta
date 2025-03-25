console.log("PDF export script loaded");

function printToPDF() {
    console.log("Print to PDF function called");
    window.print();
}

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM content loaded, adding event listener");
    document.getElementById('print-button').addEventListener('click', printToPDF);
});
