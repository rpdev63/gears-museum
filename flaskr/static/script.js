const toggleElt = document.getElementById("toggle");
const navbarElt = document.getElementById("navbar");
const headerElt = document.getElementById("header");

navbarElt.classList.toggle('active');
alert("Ca marche");
toggleElt.addEventListener("click", function changeToggle() {
    toggleElt.classList.toggle('active');
    navbarElt.classList.toggle('active');
});

document.onclick = function (e) {
    if (e.target.id !== 'header' && e.target.id !== 'navbar' && e.target.id !== 'toggle') {
        toggleElt.classList.remove('active');
        navbarElt.classList.remove('active');
    }
}