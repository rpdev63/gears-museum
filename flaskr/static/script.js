const toggleElt = document.getElementById("toggle");
const navbarElt = document.getElementById("navbar");
const headerElt = document.getElementById("header");

let active = false
if (window.innerWidth > 991) {
    navbarElt.classList.toggle("active");
    active = true;
}

window.addEventListener("resize", () => {


    if (window.innerWidth > 991 && !active) {

        navbarElt.classList.add('active');
        active = true;
    }
    if (window.innerWidth < 991 && active) {
        navbarElt.classList.remove('active');
        toggleElt.classList.remove('active');
        active = false;
    }
});

toggleElt.addEventListener("click", function changeToggle() {
    toggleElt.classList.toggle('active');
    navbarElt.classList.toggle('active');
});