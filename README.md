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


