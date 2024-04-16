<?php

namespace App\Controller;

use App\Entity\User;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\JsonResponse;

class SearchController extends AbstractController {
  #[Route('/search/{id}', name: 'app_search_request',)]
  public function search(User $user)
  {
    if (!$this->isGranted('ROLE_ADMIN') && $user !== $this->getUser()) 
      return $this->redirectToRoute('app_login');

    return $this->render('front/search.html.twig', [
      'user' => $user,
    ]);
  } 

  #[Route('/retreive', name: 'app_api_search', methods: ['POST', 'GET'])]
  public function retreive(Request $request): JsonResponse
  {
    $user = $this->getUser();

    if (!$user)
      return new JsonResponse(['error' => 'Authentification requise.'], Response::HTTP_UNAUTHORIZED);
    // On récupère les données JSON et on les décode pour pouvoir valider le csrf
    $data = json_decode($request->getContent(), true);
    $token = $data['_token'];

    if ($this->isCsrfTokenValid('search'.$user->getId(), $token)) {
      // Fermeture de session pour permettre l'exécution simultanée.
      session_write_close();

      $name = $data['name'];
      $email = $data['email'];
      $tel = $data['tel'];
      $address = $data['address'];
      $pseudonyme = $data['pseudonyme'];

      $userData = [];

      if($name) {
        $userData['name'] = $user->getName();
        $userData['lastname'] = $user->getSurname();
      }

      if($email) 
        $userData['email'] = $user->getEmail();


      if($address) 
        $userData['address'] = $user->getAddress();


      if($pseudonyme)
        $userData['username'] = $user->getUsername();

      // Transformer les données en chaîne de requête.
      $userQueryString = http_build_query($userData);

      $url = "http://10.16.0.5/cgi-bin/controleur_scrapper.py?".$userQueryString;

      // Initialisation de cURL
      $ch = curl_init($url);
      curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
      curl_setopt($ch, CURLOPT_TIMEOUT, 60); // Timeout après 10 secondes

      $response = curl_exec($ch);

      if (curl_errno($ch)) {
        curl_close($ch);
        return new JsonResponse('Serveur de requête indisponible.');
      }

      curl_close($ch);

      //$response = '{"instagram_scraper": [{"nickname": "lionelauroux", "Prive": "False"}], "pages_blanches_scraper": ["No result found"], "linkedin_scrapper" : [{"URL": "https://fr.linkedin.com/in/aurouxlionel/fr", "Name": "Lionel Auroux", "job": "Co-fondateur et Directeur Pédagogique chez École 2600 🏴‍☠️ ", "location": "Paris et périphérie"}]}';

      $data = json_decode($response, true);

      return new JsonResponse($data);
    }

    return new JsonResponse("Point de data.");
  }
}


