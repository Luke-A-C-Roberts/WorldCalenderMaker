colours = {
    "none"          : "\033[0m",
    "black"         : "\033[30m",
    "red"           : "\033[31m",
    "green"         : "\033[32m",
    "yellow"        : "\033[33m",
    "blue"          : "\033[34m",
    "magenta"       : "\033[35m",
    "cyan"          : "\033[36m",
    "light Grey"    : "\033[37m",
    "dark Grey"     : "\033[30;1m",
    "bright red"    : "\033[31;1m",
    "bright green"  : "\033[32;1m",
    "bright yellow" : "\033[33;1m",
    "bright blue"   : "\033[34;1m",
    "bright magenta": "\033[35;1m",
    "bright cyan"   : "\033[36;1m",
    "white"         : "\033[37;1m",
}


def colourise(string: str, colour: str) -> str:
    return f"{colours[colour]}{string}\033[0m"