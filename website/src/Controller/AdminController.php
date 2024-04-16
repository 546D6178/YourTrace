<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Bundle\SecurityBundle\Security;
use App\Repository\UserRepository;

#[Route('/dashboard')]
class AdminController extends AbstractController {

  #[Route('/', name: 'app_dashboard',)]
  public function dashboard()
  {
    return $this->render('admin/dashboard.html.twig');
  } 

  #[Route('/users', name: 'app_user_index', methods: ['GET'])]
  public function index(UserRepository $userRepository): Response
  {
    return $this->render('user/index.html.twig', [
      'users' => $userRepository->findAll(),
    ]);
  }

  #[Route('/data-sources', name: 'app_data_sources',)]
  public function tutorial()
  {
    return $this->render('admin/data_sources.html.twig');
  } 

}


