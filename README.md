# trip_with_kayak

The application should then be able to recommend the best destinations and hotels based on the above variables at any given time.

1. Obtenir coordonnees GPS via nominatim.org
2. obtenir infos sur la meteo et les mettre dans un Dataframe
3. Trouver les meilleures villes pour les 7 jours a venir
4. Enregistrer les resultats dans un fichier .csv (id, city)
5. plotly carte des destinations
6. scraper Booking
7. stocker le fichier CSV dans S3
8. creer database et stocker les donnees dans la database avec SQL

## Delivery

* Un fichier .csv dans un bucket S3 contenant des informations enrichies sur la météo et les hôtels de chaque ville française

* Une base de données SQL où nous devrions pouvoir obtenir les mêmes données nettoyées de S3

* Deux cartes où vous devriez avoir un Top-5 des destinations et un Top-20 des hôtels de la région.
