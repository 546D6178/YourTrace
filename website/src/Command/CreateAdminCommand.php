<?php
namespace App\Command;

use Symfony\Component\Console\Attribute\AsCommand;
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;
use Doctrine\ORM\EntityManagerInterface;
use App\Entity\User;

#[AsCommand(name: 'app:create-admin')]
class CreateAdminCommand extends Command
{
    protected static $defaultName = 'app:create-admin';

    private $passwordHasher;
    private $entityManager;

    public function __construct(UserPasswordHasherInterface $passwordHasher, EntityManagerInterface $entityManager)
    {
        $this->passwordHasher = $passwordHasher;
        $this->entityManager = $entityManager;

        parent::__construct();
    }

    protected function configure(): void
    {
        $this->setDescription('Crée un utilisateur admin');
    }

    protected function execute(InputInterface $input, OutputInterface $output): int{
        $user = new User();
        $user->setEmail('admin@yourtrace.com');
        $user->setRoles(['ROLE_ADMIN']);
        $user->setName('Admin');
        $user->setSurname('User');
        $user->setIsVerified(true);

        $user->setPassword($this->passwordHasher->hashPassword(
            $user,
            'il_faudra_songer_a_changer_cette_passphrase_par_defaut'
        ));

        $this->entityManager->persist($user);
        $this->entityManager->flush();

        $output->writeln('Admin user created!');

        return Command::SUCCESS;
    }
}
