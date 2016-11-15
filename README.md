# SystemeDistribues

https://wiki.python.org/moin/UdpCommunication

Objectifs :

	1) Canal de communication fiable
		- Spécifications
		- Hypothèses
		- Algorithme
		- Preuve
		- Implémentation
		- Éval de perf de l'implémentation (debit en fct de la taille des messages et perfs)

	2) Détecteur de fautes parfait
		- Hypothèses
		- Algorithme
		- Implémentation
		- Validation expérimentale

Teide :

	-> Rapport
	-> Archive et readme

1) Canal plus

	Spécifications :

		Interface :
			send(message)
			receive() return message

		Propriétés :
			1) validité	: Tout message reçu est un message valide
			2) intégrité : tout message envoyé par un process correct est reçu par un processus correct

	Hypothèses :

		Pannes franches
		canal non fiable

	Algorithme :
		Phase 1 : Etablissement de la connexion
		Phase 2 : Boucle d'envoi de messages
		Phase 3 : Fin de connection ou Timeout
		
		==> Une connexion est bidirectionnelle (envoi et reception).
Overhead du message : - identifiant de la machine + identifiant du message + type de message

	Listes des types de message :

		=> message standard
		=> Acquittement + taille restante dans la fenetre
		=> réenvoi
		=> debut de connexion (bonjour, je suis machin, je commence au message n, réponse : ok, ma taille de fenetre est m).

	Format du message :
		=> num message, type + [taille fenetre disponible] + payload.

		Archi :
Interface de message qui change dépendant du type de message ?

Essayer de mettre en commun au maximum le code client et serveur.
