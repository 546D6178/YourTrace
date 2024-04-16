<?php

namespace App\Entity;

use App\Repository\UserRepository;
use Doctrine\DBAL\Types\Types;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Bridge\Doctrine\Validator\Constraints\UniqueEntity;
use Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface;
use Symfony\Component\Security\Core\User\UserInterface;
use Symfony\Component\Validator\Constraints as Assert;

#[ORM\Entity(repositoryClass: UserRepository::class)]
#[UniqueEntity(fields: ['email'], message: 'Un compte existe déjà avec cette adresse email.')]
class User implements UserInterface, PasswordAuthenticatedUserInterface
{
  #[ORM\Id]
  #[ORM\GeneratedValue]
  #[ORM\Column]
  private ?int $id = null;

  #[Assert\Email] 
  #[ORM\Column(length: 180, unique: true)]
  private ?string $email = null;

  #[ORM\Column]
  private array $roles = [];

  /**
* @var string The hashed password
     */
  #[ORM\Column]
  private ?string $password = null;

  #[ORM\Column(type: 'boolean')]
  private $isVerified = false;

  #[ORM\Column(type: Types::DATE_MUTABLE, nullable: true)]
  private ?\DateTimeInterface $birthdate = null;

  #[Assert\NoSuspiciousCharacters]
  #[ORM\Column(length: 255, nullable: true)]
  private ?string $address = null;

  #[Assert\NoSuspiciousCharacters]
  #[ORM\Column(length: 255)]
  private ?string $name = null;

  #[Assert\NoSuspiciousCharacters]
  #[ORM\Column(length: 255)]
  private ?string $surname = null;

  #[ORM\Column(length: 25, nullable: true)]
  private ?string $phone_number = null;

  #[Assert\NoSuspiciousCharacters]
  #[ORM\Column(length: 255, nullable: true)]
  private ?string $username = null;

  public function getId(): ?int
  {
    return $this->id;
  }

  public function getEmail(): ?string
  {
    return $this->email;
  }

  public function setEmail(string $email): self
  {

    if ($email) {
      $this->email = $email;
    } 

    return $this;
  }

  /**
     * A visual identifier that represents this user.
     *
     * @see UserInterface
     */
  public function getUserIdentifier(): string
  {
    return (string) $this->email;
  }

  /**
     * @see UserInterface
     */
  public function getRoles(): array
  {
    $roles = $this->roles;
    // guarantee every user at least has ROLE_USER
    $roles[] = 'ROLE_USER';

    return array_unique($roles);
  }

  public function setRoles(array $roles): self
  {
    $this->roles = $roles;

    return $this;
  }

  /**
     * @see PasswordAuthenticatedUserInterface
     */
  public function getPassword(): string
  {
    return $this->password;
  }

  public function setPassword(string $password): self
  {
    $this->password = $password;

    return $this;
  }

  /**
     * @see UserInterface
     */
  public function eraseCredentials(): void
  {
    // If you store any temporary, sensitive data on the user, clear it here
    // $this->plainPassword = null;
  }

  public function isVerified(): bool
  {
    return $this->isVerified;
  }

  public function setIsVerified(bool $isVerified): self
  {
    $this->isVerified = $isVerified;

    return $this;
  }

  public function getBirthdate(): ?\DateTimeInterface
  {
    return $this->birthdate;
  }

  public function setBirthdate(?\DateTimeInterface $birthdate): self
  {
    $this->birthdate = $birthdate;

    return $this;
  }

  public function getAddress(): ?string
  {
    return $this->address;
  }

  public function setAddress(?string $address): self
  {
    $this->address = $address;

    return $this;
  }

  public function getName(): ?string
  {
    return $this->name;
  }

  public function setName(?string $name): self
  {
    $this->name = $name;

    return $this;
  }

  public function getSurname(): ?string
  {
    return $this->surname;
  }

  public function setSurname(string $surname): self
  {
    $this->surname = $surname;

    return $this;
  }

  public function getPhoneNumber(): ?string
  {
    return $this->phone_number;
  }

  public function setPhoneNumber(?string $phone_number): static
  {
    $this->phone_number = $phone_number;

    return $this;
  }

  public function getUsername(): ?string
  {
    return $this->username;
  }

  public function setUsername(?string $username): static
  {
    $this->username = $username;

    return $this;
  }
}
