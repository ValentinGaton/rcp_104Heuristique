#!/usr/bin/env python3
# coding: utf-8
"""


   :platform: Unix, Windows
   :synopsis: Probleme donné : surveillez un terrain en entier avec des capteurs et minimiser la consomation d'energie
    Les ont une zone de surveillance la totalité du terrain doit être surveillez des obstacle peuvent être placé sur le terrain

:Authors:
        Lin Jian
        Gaton Valentin


:Version: 1.0
"""


def main():
    import math

    def fieldCreator(y, x, *args):
        """
        Création du terrain sous forme de list
        :param x: taille en x
        :param y: taille en y
        :param args: les differents obstacle du terrain de la forme suivante [x, y]
        :return: listes avec y listes de x elements initialisé à 0 si vide 2 si obstacle
        """
        field = [[0 for i in range(x)] for j in range(y)]
        if (args):
            for arg in args[0]:
                field[arg[0]][arg[1]] = 2
        return field

    def isWithinRange(radius, origin, point):
        """
        Permet de savoir si un point (couple de position [y,x] fait parti du cercle de rayon donné et de position d'origine ([y, x])
        :param radius: rayon d'action du capteur
        :return: True si le point est dans la porté du cercle
        """
        differenceY = point[0] - origin[0]
        differenceX = point[1] - origin[1]
        if ((differenceX * differenceX) + (differenceY * differenceY) <= radius * radius):
            return True
        else:
            return False

    def correctRange(Y, X, MAX_Y, MAX_X, MAX_L):
        """
        Correction de la distance de placement du point permet d'eviter les out of bound
        :param Y: param Y du point
        :param X: param X du point
        :param MAX_X: bordure X
        :param MAX_Y: bordure en Y
        :param MAX_L: distance maximale ateignable
        :return:
        """
        if ((Y + MAX_L) > MAX_Y):
            correctY = MAX_Y
        else:
            correctY = Y + MAX_L
        if ((X + MAX_L) > MAX_X):
            correctX = MAX_X
        else:
            correctX = X + MAX_L
        return [correctY, correctX]

    def fillFieldWithRadius(field, radius):
        """
        Permet de remplir le terrain avec un cercle de rayon donné
        :param field: liste representant le terrain
        :param radius: radius des capteurs
        :return: le terrain rempli et le nombre de capteur pour chaque type
        """
        # Indice de switch des taille de capteur
        radIndice = 0
        # nombre de capteur par type
        cptC1 = 0
        cptC2 = 0
        cptC3 = 0
        # valeur des bordure de terrain
        MAX_Y = len(field) - 1
        MAX_X = len(field[0]) - 1
        # suivit des iterations
        Y = 0
        X = 0
        Yi = 0
        Xi = 0
        # debut algo de placement
        for y in field:
            for x in y:
                radIndice = 0
                if (x == 0):
                    for radIndice in range(3):
                        MAX_L = math.floor(float(radius[radIndice]) / math.sqrt(2))
                        correctXY = correctRange(Y, X, MAX_Y, MAX_X, MAX_L)
                        if ((correctXY[1] == MAX_X) or (correctXY[0] == MAX_Y)):
                            pass
                        elif (field[correctXY[0]][correctXY[1]] == 0):
                            break
                    if (field[correctXY[0]][correctXY[1]] == 1):
                        correctXY[0] = Y
                        correctXY[1] = X
                    if (field[correctXY[0]][correctXY[1]] == 0):
                        if (radIndice == 0):
                            cptC1 += 1
                            print('big one')
                        if (radIndice == 1):
                            cptC2 += 1
                            print('mid one')
                        if (radIndice == 2):
                            cptC3 += 1
                            print('little one')
                        for yi in field:
                            for xi in yi:
                                if (isWithinRange(radius[radIndice], correctXY, [Yi, Xi])):
                                    if (xi == 2):
                                        field[Yi][Xi] = 2
                                    else:
                                        field[Yi][Xi] = 1
                                Xi += 1
                            Xi = 0
                            Yi += 1
                        Yi = 0
                        Xi = 0
                        # affichage du terrain rempls à chaque capteur placé
                        fieldString = str(field)
                        fieldString2 = fieldString.replace("[[", "[")
                        fieldString2 = fieldString2.replace("]]", "]")
                        fieldString2 = fieldString2.replace("], ", "] \n")
                        print('MATCH = ', cptC1 + cptC2 + cptC3, '\n' + fieldString2)
                X += 1
            X = 0
            Y += 1
        return (field, cptC1, cptC2, cptC3)

    def sortValues(*args):
        """
        Range des valeur dans l'ordre decroissant
        :param args: valeurs à ranger du plus grand au plus petit
        :return: valeur rangé dans l'odre decroissant
        """
        lst = []

        for arg in args:
            lst.append(arg)
        lst.sort(reverse=True)
        return lst

    def checkEmptyZone(field):
        """
        methode de test pour verifier si il y a des cases non rempli de maniere automatique
        :param field: liste de liste representant le terrain
        """
        for y in field:
            for x in y:
                if (x == 0):
                    print("erreur Y X : ", [y, x])
                if (x == 1):
                    pass

    def powerCalculation(nbCapteur, radius):
        """
        calucul de la puissance simplement radius * le nombre de capteur
        :param nbCapteur:  nombre de capteur d'un type
        :param radius: radius du capteur
        :return:
        """
        energie = 0
        for i, j in zip(nbCapteur, radius):
            energie += int(i) * int(j)
        return energie

    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################
    obstacle = []
    # VALEURS MODIFIABLE
    # ZONE D'INPUT
    # TAILLE DU TERRAIN
    X = int(input('nombre de colonnes : '))
    Y = int(input('nombre de lignes : '))
    # OBSTACLES
    # creez ici les obstacles que vous voulez placer
    f = input("nombre d'obstacle : ")
    for q in range(int(f)):
        input_raw = input('position des obstacle Y,X (séparé par une virgule): ')
        y, x = input_raw.split(',')
        obstacle.append([int(y), int(x)])
    print(obstacle)
    # RAYON DES CAPTEURS ET PUISSANCE
    # rentrez ici les tailles de rayon des capteur entrez 3 valeurs SVP
    A = float(input('rayon du capteur 1 : '))
    B = float(input('rayon du capteur 2 : '))
    C = float(input('rayon du capteur 3 : '))
    radius = sortValues(A, B, C)
    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################
    # DEBUT DES TRAITEMENT
    # creation du terrain en liste de liste avec les obstacle
    field = (fieldCreator(X, Y, obstacle))
    # affichage terrain de base
    fieldString = str(field)
    fieldString2 = fieldString.replace("[[", "[")
    fieldString2 = fieldString2.replace("]]", "]")
    fieldString2 = fieldString2.replace("], ", "] \n")
    print('terrain de base\n' + fieldString2)

    # remplissage de la grille en partant de [0,0]
    (fieldDone, nombreCapteur1, nombreCapteur2, nombreCapteur3) = fillFieldWithRadius(field, radius)

    # affichage de resultat
    # création de la string du terrain de maniere plus lisible
    fieldString = str(fieldDone)
    fieldString2 = fieldString.replace("[[", "[")
    fieldString2 = fieldString2.replace("]]", "]")
    fieldString2 = fieldString2.replace("], ", "] \n")
    # FIN DES TRAITEMENT
    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################
    print('\n\n\nGrille Finale\n' + fieldString2)
    print('##################')
    print("#####RESULTAT#####")
    print('##################')
    print("|| Il y a ", nombreCapteur1, "capteur de taille ", radius[0], "|| Il y a ", nombreCapteur2,
          "capteur de taille ", radius[1], "|| Il y a ", nombreCapteur3, "capteur de taille ", radius[2], " ||")
    print("l'energie totale est de ", powerCalculation([nombreCapteur1, nombreCapteur2, nombreCapteur3], radius))

    print("le resultat suivant se lit de la maniere suivante : \n"
          "les 1 sont les zones couvertes par les capteur\n"
          "les 2 sont les obstacles\n"
          "les 0 sont des zones non couvertes si tout c'est bien passé il n'y en a pas\n"
          "Il est possible de voir les iterations faites plus haut et chaques capteurs placé")


if __name__ == '__main__':
    main()
