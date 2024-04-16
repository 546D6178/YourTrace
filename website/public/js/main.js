// Ice berg feature

const iceberg = document.getElementById("yourtrace_info");

let scrolling = window.pageYOffset;

function parallaxeImg(scrolling) {
  iceberg.style.transform ="translateY("+ scrolling / 2 +"px)"
}

if (window.innerWidth > 768 && iceberg !== null) {


  parallaxeImg(scrolling); //Actualisation des positions au chargement de la page

  //Ecouteur d'events pour tous les effets au scroll

  document.addEventListener('scroll', (e) => {
    window.requestAnimationFrame(function () {
      scrolling = window.pageYOffset;
      parallaxeImg(scrolling)
    });
  });

}

// Others

/* Fonction qui permet de fermer les fenêtres de notifications avec un fondu */
function fadeOutElement(element) {
  element.classList.add("fade-out");
  setTimeout(function() {
      element.style.display = 'none';
  }, 500);
}
