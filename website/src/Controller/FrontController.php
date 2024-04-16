<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\HttpFoundation\Request;

class FrontController extends AbstractController {
  #[Route('/', name: 'app_index', methods: ['GET'])]
  public function index(Request $request)
  {
      return $this->render('front/home.html.twig');
  } 

  #[Route('/didacticiel', name: 'tutorial', methods: ['GET'])]
  public function tutorial()
  {
      return $this->render('front/tutorial.html.twig');
  } 

  #[Route('/a-propos', name: 'about', methods: ['GET'])]
  public function about()
  {
      return $this->render('front/about.html.twig');
  } 


  #[Route('/mentions-legales', name: 'legals', methods: ['GET'])]
  public function legals()
  {
      return $this->render('front/legals.html.twig');
  } 
}


