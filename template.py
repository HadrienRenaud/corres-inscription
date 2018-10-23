# -*- coding: utf-8 -*-
import re
import jinja2


class ParsingError(Exception):
    pass


def _render_file(file, attribute):
    """Render the file"""

    with open(file, "r") as opened_file:
        content = opened_file.read()

    templ = jinja2.Template(content)

    return templ.render(attribute)


RE_HEADER = re.compile(r"Content:\s*\n+")
RE_HEADER_CONTENT = re.compile(r"(?P<key>\w+): (?P<value>.*(?:\n\s+.*\S)*)")
RE_UNIDENT = re.compile(r"\n\s*(?P<content>.*)")
RE_UNIDENT_SUBST = r"\n\g<content>"  # type: str
ARG_TRANSLATION = {
    "from": "sender",
    "to": "receivers",
    "subject": "subject",
}


def _parse_header(string):
    res = {}
    for match in RE_HEADER_CONTENT.finditer(string):
        value = RE_UNIDENT.sub(RE_UNIDENT_SUBST, match.group("value"), re.MULTILINE)
        key = match.group('key')
        if key.lower() in ARG_TRANSLATION:
            key = ARG_TRANSLATION[key.lower()]
        res[key] = value
    return res


def _parse_mail(content):
    match = RE_HEADER.search(content)
    if match is None:
        raise ParsingError("Wrong template format : " + content)
    header = content[:match.start()]
    res = _parse_header(header)
    res["content"] = content[match.end():]
    return res


def render(file, attribute):
    return _parse_mail(_render_file(file, attribute))

