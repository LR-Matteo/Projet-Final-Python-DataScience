WINDSPOT 

Un seul objectif : Selon un lieu donné, un rayon autour de cette localisation et un sport nautique donné, on veut trouver
le meilleur lieu pour pratiquer l'activité selon les conditions météo. Pour cela, nous utilisons les différents équipements
nautiques dispos en France.

Pour lancer le code, il suffit d'éxecuter le fichier requirement.txt en réalisant la commande suivante dans le terminal :
pip install -r requirement.txt . Ensuite, il suffit de lancer les trois notebooks en commençant par celui nommé 
"bdd_stats_desc.ipynb", puis le deuxième "acp_clustering.ipynb" et enfin le dernier "windspot.ipynb" .

Pour récupérer les données, nous avons utilisé le site gouvernement fiable "data.gouv" et notamment ce qui nous intéresse est
le recensement des équipements sportifs, espaces et sites de pratiques. Nous avons récupéré les données météo via une API 
disponibles par le site "Open-meteo.com" .

Pour le choix des variables, nous avons gardé dans la table des équipements  les colonnes suivantes : 
'equip_numero', "inst_numero", "inst_nom", "inst_adresse", "inst_cp", "dep_code", "reg_code", "dep_nom",
 "reg_nom", "lib_bdv", "equip_nom", "equip_type_name", "equip_coordonnees", "aps_name" . Autrement dit, les identifiants des
 équipements, le nom, les adresses. Nous disposons des départements, des régions, des villes, des types d'équipements,
 de ce qui est proposé par l'équipement, les coordonnées des équipements . Concernant les variables récupérées concernant la météo, nous n'avons sélectionnées que celles qui interviennent dans la construction de notre score.

 Pour commencer, nous avons débuté par quelques stats descriptives, en réalisant des représentations d'équipements sportifs par départements, par région mais aussi en regardant quels étaient les types d'équipements sportifs. Nous avons fait des cartes permettant de visualiser les résultats. Nous avons également à partir de la base initiale, crée une nouvelle base ne contenant que les équipements nautiques qui seront notre objet d'intérêt pour la fin de notre projet. Ensuite, pour le choix du modèle, nous avons fait le choix de réaliser une ACP puis un clustering sur l'ensemble des équipements de la base initiale. Cela a permis de mettre en avant des différences spatiales quant à la répartition des équipements sur le territoire. Nous obtenons différents types d'équipements (certains très ultramarins, d'autres très sports natures en extérieur, d'autres liés à une grosse population ...).
 Enfin, nous avons implémenté la finalité du projet WINDSPOT. Nous avons dans un premier temps, crée un score adéquat pour chaque sport afin d'observer les meilleures conditions climatiques possibles. Dès lors, en donnant un nom de ville, un rayon et une pratique, il est désormais possible de connaître l'équipement le plus proche ayant les meilleures conditions météo favorisant la pratique du sport. 