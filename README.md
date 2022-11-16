Merci de bien lire ce fichier avant de commencer à utiliser le projet.

/!\/!\/!\ Pour le bon fonctionnement du projet, merci de créer en avance un fichier output.json, contenant des crochets
exemple contenu de output.json : 
<output.json>

[

]

</output.json>
le fichier sur mon github est au bon format
/!\/!\/!\

Une première liste de 6 vidéos est inclue dans le projet, la dernière vidéo ne contient pas de commentaire, le terminal le signalera.

Pour la partie commentaire, je n'ai pas réussi à le faire sans le module selenium.
Il est dans requirements.txt, il faut donc l'installer avec pip.

Néanmoins, je ne savais pas si on avait droit ou non, à utiliser d'autres technos que celles notées dans les slides de l'énoncé.
Si ce n'est pas le cas, il vous suffit de modifier la variable globale tryWithTheComments (ligne 15 de scrapper.py), afin de la passer de 'True' à 'False'.
De plus, lancer un driver web prend beaucoup de temps (jusqu'à 10 secondes par video), donc avec une liste d'environ 1000 ids de videos, cela risque de prendre du temps
Il arrive parfois que la fonction n'arrive pas à retrouver les commentaires, mais je ne sais pas d'où vient ce problème
Pour les vidéos sans commentaire, le programme ne fait rien, il attend 10 secondes et passe à la vidéo suivante
Les vidéos avec les commentaires bloqués n'ont pas de compteur de like. Je l'ai donc initialisé à 0

J'ai fais attention à essayer de rendre le code le plus lisible possible, suivant les bonnes pratiques du livre CleanCode.

------------------------------------------------------------------------------------------------------------------------------

Venv :
python3.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

------------------------------------------------------------------------------------------------------------------------------

Pour lancer le script :
python scrapper.py --input input.json --output output.json

------------------------------------------------------------------------------------------------------------------------------

Pour lancer les tests :
python -m pytest tests/test_scrapper.py OR coverage run -m pytest tests/test_scrapper.py

------------------------------------------------------------------------------------------------------------------------------

Lecture de output.json :
Le code est indenté sur une seule ligne.
Vous pouvez le réindenter avec votre IDE
