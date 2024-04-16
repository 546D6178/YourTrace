// Déclaration de l'AbortController en dehors de la fonction de soumission
let abortController;

document.getElementById('osint_search').addEventListener('submit', function(e) {
  e.preventDefault();

  // Réinitialisation de l'AbortController à chaque soumission du formulaire
  abortController = new AbortController();

  let resultContent = document.getElementById("results_content");
  resultContent.style.opacity = "1"

  let loader = document.getElementById("loader");
  loader.style.display = "block";
  loader.style.opacity = "1";
  loader.style.animation = "animloader 1s linear infinite";

  let formData = new FormData(e.target);
  let object = {};
  formData.forEach(function(value, key){
    object[key] = value;
  });

  let checkboxElements = document.querySelectorAll('.toggle-checkbox');
  checkboxElements.forEach(checkbox => {
    object[checkbox.id] = checkbox.checked;
  });

  let json = JSON.stringify(object);
  let cancel_button = document.getElementById('cancel_button');

  cancel_button.style.opacity = "1";
  cancel_button.style.display = "inline-block";

  // Envoie le token CSRF en tant que paramètre de l'URL avec le signal d'annulation
  fetch(e.target.action + '?_token=' + object._token, {
    method: 'POST',
    body: json,
    headers: {
      "Content-Type": "application/json"
    },
    signal: abortController.signal
  })
  .then(response => response.json())
  .then(data => {
    cancel_button.style.opacity = "0";
    cancel_button.style.display = "none";
    
    console.log(data);

    let delay = 0;
    let decal = 200;
    let resultArea = document.getElementById('results'); 
    resultArea.innerHTML = "";

    if (data == "Point de data." || data == "Serveur de requête indisponible.") {
      resultArea.innerHTML += `<li style="animation : slide-in .4s ${delay}ms ease-in-out forwards"><a>${data}</a></li>`;

    } else if (data.length == 0) {
      resultArea.innerHTML += `<li style="animation : slide-in .4s ${delay}ms ease-in-out forwards"><a>Aucun résultat. Nous n'avons rien trouvé sur vous !</a></li>`;

    } else {
      Object.keys(data).forEach((key) => {
        let listHTML = "";

        data[key].forEach((item) => {
          listHTML += `<li class="major" style="animation : slide-in .4s ${delay}ms ease-in-out forwards"><a href="">${key}</a><ul>`;
          delay += decal;

          if (typeof item == "object"){
            Object.keys(item).forEach((subkey) => {
              if(subkey.toLowerCase() == "url"){
                listHTML += `<li class="minor" style="animation : slide-in .4s ${delay}ms ease-in-out forwards"><a href="${item[subkey]}" target="_blank">${subkey} : ${item[subkey]}</a></li>`;

              } else if (key === "Holehe"){
                listHTML += `<li class="minor" style="animation : slide-in .4s ${delay}ms ease-in-out forwards"><a href="https://${subkey}" target="_blank">${subkey} : ${item[subkey]}</a></li>`;
                } else {
                  listHTML += `<li class="minor" style="animation : slide-in .4s ${delay}ms ease-in-out forwards"><a href="">${subkey} : ${item[subkey]}</a></li>`;
              }
              delay += 100;
            });
          } else {
            listHTML += `<li class="minor" style="animation : slide-in .4s ${delay}ms ease-in-out forwards"><a href="">${item}</a></li>`;
            delay += decal;
          }

          listHTML += "</ul></li>";
        });

        resultArea.innerHTML += listHTML;
      });
    }
    loader.style.display = "none";
  }).catch(error => {
    if (error.name === 'AbortError') {
      console.log('Fetch aborted');
    } else {
      console.error('Fetch error:', error);
    }
    loader.style.display = "none";
  });
}); 

// Bouton ou action pour annuler la requête
document.getElementById('cancel_button').addEventListener('click', (e) => {
  console.log("Interrupted");
  e.preventDefault();
  if (abortController) {
    abortController.abort();
    cancel_button.style.opacity = "0";
    cancel_button.style.display = "none";
  }
});

