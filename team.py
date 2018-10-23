from typing import List
import csvinteract

__translate_dict = {
    "identifiant": "id_",
    "mailequipe": "mail",
    "nomequipe": "name",
    "réponses": "reponses",
    "idopposition": "id_opp",
}


def _translate(header: List[str]) -> List[str]:
    """Translate headers into args for Team constructing."""
    return [__translate_dict.setdefault(h, h) for h in header]


class Team:
    id_: str = None

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            self.__setattr__(key, val)


class Teams:
    def __init__(self, file):
        rows, headers = csvinteract.extract(file)
        headers = _translate(headers)
        self.teams = [Team(**dict(zip(headers, row))) for row in rows]
        self.id_to_team = {t.id_: t for t in self.teams}

    def get_by_id(self, id_):
        return self.id_to_team[id_]
