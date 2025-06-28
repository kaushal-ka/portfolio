/* static/main.js 
    Handles:
    - AJAX POST to /sumit_contact
    - Shows flash box in center-top
    - Auto-hide after 5 s OR click "OK"
---------------------------------------------------- */
const form = document.getElementById("contactForm");
const flash = document.getElementById("flash-message");
form.addEventListener("submit", async(e) =>{
e.preventDefault(); // stop normal page reload
const formData = new FormData(form);
try {
    const res = await fetch("/submit_contact", {
        method: "POST",
        body: formData
    });
    const data = await res.json();
    // Show flash
    if (data.status === "success") form.reset(); // clear fields
}    
catch (err) {
    showFlash("Unexpected error occurred!", "error");
}
});
// Display flash, auto-hide, allow dismiss
function showFlash(msg, status = "success") {
    // Reset content & class
    flash.innerHTML = "";
    flash.textContent = msg;
    flash.className = "flash-message show" + (status === "error" ? "error" : "");
    // Add "ok" dismiss button
    const btn = document.createElement("button");
    btn.textContent = "OK";
    btn.onclick = hideFlash;
    flash.appendChild(btn);
    flash.style.display = "flex";
    // Auto hide after 5 seconds
    setTimeout(hideFlash, 5000);
}

function hideFlash(){
    flash.classList.remove("show"); // fades out (opacity transition)
    // Wait for CSS transition then hide fully
    setTimeout(() => { flash.style.display = "none"; }, 400);
    

}
