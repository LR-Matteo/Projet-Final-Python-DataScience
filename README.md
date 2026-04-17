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
 de ce qui est proposé par l'équipement, les coordonnées des équipements .