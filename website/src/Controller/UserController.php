<?php

namespace App\Controller;

use App\Entity\User;
use App\Form\UserType;
use App\Repository\UserRepository;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Validator\Validator\ValidatorInterface;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

#[Route('/user')]
class UserController extends AbstractController
{
  // Les nouveaux utilisateurs sont généralement créés depuis le RegistrationController()
  #[Route('/new', name: 'app_user_new', methods: ['GET', 'POST'])]
  public function new(Request $request, UserRepository $userRepository, UserPasswordHasherInterface $userPasswordHasher, ValidatorInterface $validator): Response
  {
    $user = new User();
    $form = $this->createForm(UserType::class, $user);
    $form->handleRequest($request);

    if ($form->isSubmitted() && $form->isValid()) {
      
      $errors = $validator->validate($user);
      if (count($errors) > 0)
            return new Response('Invalid user properties. You naughty hacker.', Response::HTTP_BAD_REQUEST);
      
      $user->setPassword(
                $userPasswordHasher->hashPassword(
                    $user,
                    $form->get('plainPassword')->getData()
                )
            );

      $userRepository->save($user, true);

      return $this->redirectToRoute('app_user_index', [], Response::HTTP_SEE_OTHER);
    }

    return $this->render('user/new.html.twig', [
      'user' => $user,
      'form' => $form->CreateView(),
    ]);
  }

  #[Route('/{id}', name: 'app_user_show', methods: ['GET'])]
  public function show(User $user): Response
  {
    if (!$this->isGranted('ROLE_ADMIN') && $user !== $this->getUser()) 
      return $this->redirectToRoute('app_login');

    return $this->render('user/show.html.twig', [
      'user' => $user,
    ]);
  }

  #[Route('/{id}/edit', name: 'app_user_edit', methods: ['GET', 'POST'])]
  public function edit(Request $request, User $user, UserRepository $userRepository,ValidatorInterface $validator): Response
  {
    if (!$this->isGranted('ROLE_ADMIN') && $user !== $this->getUser()) 
      return $this->redirectToRoute('app_login');
    
    $form = $this->createForm(UserType::class, $user);
    $form->handleRequest($request);

    if ($form->isSubmitted() && $form->isValid()) {
      
      $errors = $validator->validate($user);
      if (count($errors) > 0)
            return new Response('Invalid user properties. You naughty hacker.', Response::HTTP_BAD_REQUEST);

      $userRepository->save($user, true);

      if ($this->isGranted('ROLE_ADMIN'))
        return $this->redirectToRoute('app_user_index', [], Response::HTTP_SEE_OTHER);

      return $this->redirectToRoute('app_user_show', ['id' => $user->getId()]);
    }

    return $this->render('user/edit.html.twig', [
      'user' => $user,
      'form' => $form->CreateView(),
    ]);
  }

  #[Route('/{id}', name: 'app_user_delete', methods: ['POST'])]
  public function delete(Request $request, User $user, UserRepository $userRepository): Response
  {
    $isAdmin = $this->isGranted("ROLE_ADMIN");

    if ($this->isCsrfTokenValid('delete'.$user->getId(), $request->request->get('_token')))
      $userRepository->remove($user, true);

    if ($isAdmin)
    {
      $this->addFlash("success", "L'utilisateur " . $user->getName() . " à bien été supprimé !");
      return $this->redirectToRoute('app_user_index', [], Response::HTTP_SEE_OTHER);
    }
    else
    {
      $request->getSession()->invalidate();
      $this->container->get('security.token_storage')->setToken(null);

      $this->addFlash("success", "L'utilisateur " . $user->getName() . " à bien été supprimé !");
      return $this->redirectToRoute('app_login');
    }
  }
}
