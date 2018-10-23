# Script d'envoi d'emails pour les correspondances

## Installing

#### Installation 

Sur Linux :
```commandline
pip install jinja2
git clone https://github.com/HadrienRenaud/corres-inscription
cd corres-inscription
cp config-template.py config.py
```
Ensuite éditer `config.py` pour y mettre la bonne configuration.

## How to

L'envoi d'un mail passe par plusieurs étapes :
 - écrire le template (le + dur)
 - exécuter l'application (le + facile, si tu dois pas la réparer après)

### Écrire un template

`corres-inscription` utilise [Jinja](http://jinja.pocoo.org/docs/2.10/) pour générer le contenu des mails.

Pour plus d'informations sur comment faire un template `Jinja`, voir [ici](http://jinja.pocoo.org/docs/2.10/templates/).

Pour résumer Jinja transforme votre fichier en un autre, en remplaçant ce qui est contenu dans des balises par des valeurs données par Python. Rien de plus parlant qu'un petit exemple :

#### Un petit exemple

Imaginons que les variables suivantes sont définies dans Python :

```python
titre = "Mon super document"

auteur = "Hadrien Renaud"

class Lecteur:
    est_intelligent = False
    sait_lire = True
    nom = None
    
mon_lecteur = Lecteur()
mon_lecteur.est_intelligent = True
mon_lecteur.nom = "Ada Lovelace"

petit_dictionnaire = {
    'mon': 'my',
    'nom': 'name',
    'est': 'is',
}

ma_liste = [2, 3, 5, 7, 11, 13, 17, 19]
```

Et le template suivant :

```jinja2
# {{ titre }}

__by {{ auteur }}__

Mon très cher lecteur,

Je t'écris aujourd'hui pour t'affirmer que tu 
{% if mon_lecteur.est_intelligent %}
est
{% else %}
n'est pas
{% end %}
intelligent. Cela me désole mais je ne puis rien y faire, ta lecture est indépendante de ma volonté.

{% set phrase = ['mon', 'nom', 'est', 'Hadrien'] %}
Même si je sais que tu ne le comprends pas, toi, {{ mon_lecteur.nom }}, je t'écris en français. Pour te le faire comprendre, voici comment on dit {{ ' '.join(phrase) }} en anglais : {{ ' '.join([petit_dictionnaire[w] if w in petit_dictionnaire else w for w in phrase]) }}.

Je voudrais aussi te faire part de ma découverte, voici les nombres premiers entre 2 et 20 : 
{% for i in ma_liste %}
 - {{ i }}
 {% endfor %}
 
 Bonne soirée,
 
 {{ auteur }}

```

Permet de retrouver le message suivant :

```markdown
# Mon super document

__by Hadrien Renaud__

Mon très cher lecteur,

Je t'écris aujourd'hui pour t'affirmer que tu 
es intelligent. Cela me désole mais je ne puis rien y faire, ta lecture est indépendante de ma volonté.

Même si je sais que tu ne le comprends pas, toi, Ada Lovelace, je t'écris en français. Pour te le faire comprendre, voici comment on dit mon nom est Hadrien en anglais : my name is Hadrien.

Je voudrais aussi te faire part de ma découverte, voici les nombres premiers entre 2 et 20 : 
  - 2
  - 3
  - 5
  - 7
  - 11
  - 13
  - 17
  - 19
 
 Bonne soirée,
 
Hadrien Renaud
```

### Variables définies ici

 - `team`
 - `teams`

#### team

`team` est la variable qui contient les données de l'équipe en question (généralement celle à qui vous écrivez).
C'est un objet de la classe `Team` qui est construit dynamiquement en fonction des colonnes du document `.csv` qui contient les données des équipes, avec une traduction possible pour certains caractères.

Par exemple, si le document `csv` contient :

| identifiant | mail                     | nom | questions | reponses | idopposition |   | 
|-------------|--------------------------------|-----------|-----------|----------|--------------|---| 
| 11          | hadrien.renaudlebret@gmail.com | equipe1   |           |          | 12           |   | 
| 12          | hadrien.renaudlebret@gmail.com | equipe2   |           |          | 11           |   | 

Alors la classe `Team` aura pour attributs :
 - `id_` ~ identifiant
 - `mail`
 - `nom`
 - `questions`
 - `reponses`
 - `idopposition`

#### teams

`teams` est la variable qui contient toutes les données de toutes les équipes. Elle a un attribut `teams` qui est la liste des équipes, et une méthode ̀`get_by_id(i)` qui retourne la variable team numéro `i`. 
Par exemple, pour avoir accès aux informations de l'équipe opposée dans la variable `opp`, on utilisera : 
```jinja2
{% set opp = teams.get_by_id(team.idopposition %}
``` 

### Exécuter le programme

```commandline
python3 main.py file.csv file.jinja
```

Pour plus d'infos, regarder `python3 main.py -h`.