<?php

namespace App\Form;

use App\Entity\User;
use Symfony\Component\Form\AbstractType;
use Symfony\Component\Form\Extension\Core\Type\CheckboxType;
use Symfony\Component\Form\Extension\Core\Type\EmailType;
use Symfony\Component\Form\Extension\Core\Type\TextareaType;
use Symfony\Component\Form\Extension\Core\Type\DateType;
use Symfony\Component\Form\Extension\Core\Type\TextType;
use Symfony\Component\Form\Extension\Core\Type\PasswordType;
use Symfony\Component\Form\FormBuilderInterface;
use Symfony\Component\OptionsResolver\OptionsResolver;
use Symfony\Component\Validator\Constraints\IsTrue;
use Symfony\Component\Validator\Constraints\Length;
use Symfony\Component\Validator\Constraints\NotBlank;

class RegistrationFormType extends AbstractType
{
  public function buildForm(FormBuilderInterface $builder, array $options): void
  {
    $builder
      ->add('email', EmailType::class, [
        'label' => 'Adresse mail :' 
      ])
      ->add('birthdate', DateType::class, [
        'required' => false,
        'label' => 'Date de naissance : (facultatif)',
        'attr' => ['class' => 'date_select'],
        'widget' => 'single_text',
      ])
      ->add('name', TextType::class, [
        'label' => 'Prénom :' 
      ])
      ->add('surname', TextType::class, [
        'label' => 'Nom :' 
      ])
      ->add('username', TextType::class, [
        'label' => 'Pseudonyme :',
        'required' => false,
      ])
      ->add('phone_number', TextType::class, [
        'label' => 'Téléphone :',
        'required' => false,
      ])
      ->add('address', TextAreaType::class, [
        'required' => false,
        'label' => 'Adresse postale : (facultatif)',
      ])
      ->add('plainPassword', PasswordType::class, [
        // instead of being set onto the object directly,
        // this is read and encoded in the controller
        'label' => 'Mot de passe :',
        'mapped' => false,
        'attr' => ['autocomplete' => 'nouveau mot-de-passe'],
        'constraints' => [
          new NotBlank([
            'message' => 'Veuillez entrer un mot de passe',
          ]),
          new Length([
            'min' => 6,
            'minMessage' => 'Votre mot de passe doit faire au moins {{ limit }} caractères',
            // max length allowed by Symfony for security reasons
            'max' => 4096,
          ]),
        ],
      ])
      ->add('agreeTerms', CheckboxType::class, [
        'label' => 'J\'accèpte les termes :',
        'mapped' => false,
        'constraints' => [
          new IsTrue([
            'message' => 'Veuillez accepter les termes',
          ]),
        ],
      ])

      ;
  }

  public function configureOptions(OptionsResolver $resolver): void
  {
    $resolver->setDefaults([
      'data_class' => User::class,
    ]);
  }
}
