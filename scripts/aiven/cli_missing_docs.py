"""
Script to help find missing related devportal command documentation
for Aiven client

Notes:

  1. Just run this script to use it: `python cli_missing_docs.py`
  2. Since the script uses docutils to parse the `.rst` files, and not sphinx,
     it is normal to get `(ERROR/3) Unknown interpreted text role` messages,
     as docutils doesn't understand sphinx extensions. These don't affect the
     accuracy of the `MISSING` output.
"""
import os
from aiven.client import argx, cli
from docutils.core import publish_doctree
from pathlib import Path

p = os.path.abspath(os.path.join(__file__, "../../.."))
os.chdir(p)


def find_cli_docs() -> None:
    """
    Parses the CLI document folder and retrieves
    all the titles that matchs with the aiven command.
    """
    list_of_commands = []
    dirname = os.path.dirname(__file__).replace("scripts/aiven", "") + "docs/tools/cli"
    print(dirname)
    for dirpath, dirnames, filenames in os.walk(dirname):
        for name in filenames:
            with open(os.path.join(dirpath, name)) as f:
                text = f.read()
                titles = publish_doctree(text).traverse(condition=section_title)
                for t in titles:
                    list_of_commands.append(t.astext())
    # Remove from the titles the avn prefix to match it with the functions
    list_of_commands = list(map(lambda x: x.replace("avn ", ""), list_of_commands))

    return sorted(list_of_commands)


def find_cli_commands():
    """This function parses the CLI and returns all its functions.

    Each `avn` command is implemented by a method annotated with `@arg`
    Those are listed in `argx.ARG_LIST_PROP`.

    Today (27.08.2022), they're only on the AivenCLI class, so this
    is used to parse the commands.

    Info: https://github.com/aiven/aiven-client/blob/main/aiven/client/cli.py
    """
    cmds = []
    for prop_name in dir(cli.AivenCLI):
        # Ignore private values/methods
        if prop_name.startswith("_"):
            continue
        # Get the value/method with that name
        prop = getattr(cli.AivenCLI, prop_name)
        # And see if it has an argument list defined on it
        arg_list = getattr(prop, argx.ARG_LIST_PROP, None)
        # If it doesn't, then it's not a command and we can ignore it
        if arg_list is None:
            continue
        # Replace double underscores with spaces, single underscores with hyphens,
        # to get the actual command
        cmd = prop_name.replace("__", " ").replace("_", "-")
        cmds.append(cmd)
    return cmds


# This function retrieves the section titles from a doc
def section_title(node):
    """Whether `node` is a section title.

    Note: it DOES NOT include document title!
    """
    try:
        return node.parent.tagname == "section" and node.tagname == "title"
    except AttributeError:
        return None  # not a section title


def main():
    list_of_cli = find_cli_commands()
    list_of_docs = find_cli_docs()

    # Uncomment the below to find the matches between doc and cli

    # print("FOUND")
    # intersection = sorted(set(list_of_cli).intersection(list_of_docs))
    # print(intersection)

    print("---------- MISSING -------------")
    difference = sorted(set(list_of_cli).difference(list_of_docs))
    for i in difference:
        print(i)


if __name__ == "__main__":
    main()
