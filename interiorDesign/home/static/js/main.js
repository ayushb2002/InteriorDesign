 
    window.setTimeout(function(){
        var loader = document.getElementById('shown');
        var body = document.getElementById('hidden');
        loader.style.display = 'none';
        body.style.display = 'block';
    }, 3000);


    // When the user scrolls the page, execute myFunction
window.onscroll = function() {myFunction()};
// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function myFunction() {

    var navbar = document.getElementById("navbar");
    var sticky = navbar.offsetTop;

  if (window.pageYOffset > sticky) {
    navbar.classList.add("fixed-top")
  } else {
    navbar.classList.remove("fixed-top");
  }
}