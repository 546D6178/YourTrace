# Introduction 

Petit bout de code qui peut être utilisé pour requêter l'API d'AWS pour connaître l'IP pubique qui rend accessible le gitlab. 
Ici nous aborderons la création d'un utilisateur, puis d'une politique qui lui sera attribué et enfin la création d'un token d'accès

# Paramétrage sur AWS

Créer un utilisateur IAM sur AWS 

*Un utilisateur IAM est une identité avec des informations d'identification à long terme utilisées pour interagir avec AWS dans un compte.*

https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey_CLIAPI

## Créer un politique sur AWS 

*Une politique est un objet dans AWS qui définit les autorisations*

- RTFM déjà. 

> Création politique : Read-only access

```

{
   "Version": "2012-10-17",
   "Statement": [{
      "Effect": "Allow",
      "Action": [
         "ec2:DescribeInstances", 
         "ec2:DescribeImages",
         "ec2:DescribeTags", 
         "ec2:DescribeSnapshots"
      ],
      "Resource": "*"
   }
   ]
}
```

## Créer le token d'accès 
*Utilisez les clés d'accès pour effectuer des appels par programmation vers AWS à partir d'AWS CLI*

- Ajouter un "Clés d'accè" depuis le dashboard AWS "IAM management" sous Gestions des accès > Utilisateurs

# Paramétrage côté client 

## Installation du CLI AWS

- Installation : 

`curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"`

`unzip awscliv2.zip`

`sudo ./aws/install`

- Paramétrer notre cli avec nos données d'identifications : 

`aws configure`
```
AWS Access Key ID [None]: AKIATLWY6OSRE4HYQO6E
AWS Secret Access Key [None]: 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
Default region name [None]: us-east-1
Default output format [None]: json
```

Récupérer l'IP publique souhaitée : 

`aws ec2 describe-instances --instance-ids i-038007881685e8f80 --query=Reservations[].Instances[].PublicIpAddress |  grep -oP '(?<=").*?(?=")'`


