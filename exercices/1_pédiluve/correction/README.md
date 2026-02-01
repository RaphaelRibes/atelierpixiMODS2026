# Le Pédiluve
Parce que oui, il faut bien commencer quelque part !

## Objectif
Le but est de faire tourner et d'automatiser le script main.py avec pixi.
Cet exercice a pour but de vous faire comprendre les bases de pixi en créant un simple environnement et une tache simple.


## Instructions
1. Initisalisez un environnement pixi.
```shell
pixi init
```

2. Ajouter python 3.9 dans votre environnement par défaut.
```shell
pixi add python=3.9
```

3. Ajouter la library `cowpy` a votre environement. 
```shell
pixi add --pypi cowpy
```

4. Faire tourner le script main.py avec pixi.
```shell
pixi run python main.py
```

5. Automatiser le lancement du script avec une tache pixi
```shell
pixi task add start "python main.py"
```

6. Lancer la tache pixi
```shell
pixi run start
```

## Pour aller plus loin
- Modifie le script main.py pour afficher un message donné en argument de la ligne de commande.

7. Il suffit juste de modifier le script main.py pour récupérer l'argument et l'afficher avec cowpy.

Pixi va se charger de parser l'argument et de le passer au script.

```shell
pixi run start "Hey !"
✨ Pixi task (start): python main.py Hey !
 _______ 
< Hey ! >
 ------- 
     \   ^__^
      \  (oo)\_______
         (__)\       )\/\
           ||----w |
           ||     ||
```