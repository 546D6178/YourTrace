<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;
use Symfony\Component\Security\Http\Authentication\AuthenticationUtils;

class SecurityController extends AbstractController
{
    #[Route(path: '/login', name: 'app_login')]
    public function login(AuthenticationUtils $authenticationUtils): Response
    {
        // get the login error if there is one
        $error = $authenticationUtils->getLastAuthenticationError();
        // last username entered by the user
        $lastUsername = $authenticationUtils->getLastUsername();

        if ($this->getUser())
            $this->addFlash("success", "Tu es déjà connecté en tant que " . $this->getUser()->getUserIdentifier());

        if (isset($error))
        {
            $messageKey = $error->getMessageKey();
            $this->addFlash("error", $messageKey);
        }

        return $this->render('security/login.html.twig', ['last_username' => $lastUsername]);
    }

    #[Route(path: '/logout', name: 'app_logout')]
    public function logout(): void
    {
        $this->addFlash("success", "Tu es bien déconnecté " . $this->getUser()->getName());
        throw new \LogicException('This method can be blank - it will be intercepted by the logout key on your firewall.');
    }
}
