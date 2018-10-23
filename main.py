#!/usr/bin/python3

import sys
import argparse
import functools

import team
import template
import mail


def _file_exists(string: str, arg=None) -> str:
    try:
        open(string, "r")
    except FileNotFoundError as e:
        msg = f"File not found {e.filename}"
        raise argparse.ArgumentError(arg, msg)
    except OSError as e:
        msg = f"File {e.filename} cannot be opened"
        raise argparse.ArgumentError(arg, msg)
    except ValueError as e:
        msg = f"File {e.filename} has an encoding problem."
        raise argparse.ArgumentError(arg, msg)
    except Exception as e:
        msg = f"File cannot be opened. ({type(e)} : {e.args})"
        raise argparse.ArgumentError(arg, msg)
    return string


def _get_parser(*args, **kwargs):
    parser = argparse.ArgumentParser(
        description="Send mails with jinja2 templates.",
        epilog="For any question or remark, please contact "
               "Hadrien Renaud <hadrien.renaud@polytechnique.edu>",
    )
    parser.add_argument(
        "csv_file",
        help="The csv file with the teams in it.",
        type=_file_exists,
    )
    parser.add_argument(
        "template",
        help="The jinja template for the mail.",
        type=_file_exists,
    )
    parser.add_argument(
        "--send",
        help="If present, send mails",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--yes", "-y",
        help="Answer yes to 'Do you really want to send mails ?'",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "--verbose", "-v",
        help="Verbose level",
        action="store_true",
        default=False,
    )

    args = parser.parse_args(*args, **kwargs)
    return args.csv_file, args.template, args.send, args.yes, args.verbose


def printif(test: bool):
    """Wrapper around print to control output based on a boolean."""
    @functools.wraps(print)
    def null(*args, **kwargs):
        pass

    if test:
        return print
    else:
        return null


def main():
    """Fonction d'entrée du programme."""

    csv_file, jinja_file, send, yes, verbose = _get_parser()

    printv = printif(verbose)
    printn = printif(not yes and verbose)

    printv("Parsing teams ... ", end="")

    teams = team.Teams(csv_file)

    printv(f"Done : {len(teams.teams)} teams found.\n")
    printv("Parsing template ... ", end="")

    content = [
        template.render(jinja_file,
                        {"teams": teams, "team": t,
                         "opp": teams.get_by_id(t.id_opp)})
        for t in teams.teams]

    printv("Done.\n")

    printn("### First mail :")
    printn(mail.send(send=False, **content[0]))

    if send and not yes:
        send = input("Do you really want to send mails ? [y/N] : ")
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False, "": False, "oui": True,
                 "o": True, "non": False}
        if send in valid:
            send = valid[send]
        else:
            send = False
    else:
        send = send or yes

    if send:
        for c in content:
            mail.send(send=send, **c)

    return 0


if __name__ == '__main__':
    sys.exit(main())
