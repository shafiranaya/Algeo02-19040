const fileBtn = document.querySelector('#file-btn');

fileBtn.addEventListener('click', directToFile);

function directToFile(e){
    e.preventDefault();
    window.location.href = "addfile.html";
}