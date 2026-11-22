"""Classify simple, complete recorded shell inputs. Never execute a recorded command."""
import re
import shlex
from pathlib import PurePosixPath


# Recognize only plain command words, quoted arguments, and visible separators.
# Leave expansion, scripts, substitutions, redirections and incomplete input to review.
TOKEN = re.compile(r'''[ \t]+|\\\n|&&|\|\||[;\n]|'(?:[^']*)'|"(?:[^"\\`$]|\$[A-Za-z_]\w*)*"|[A-Za-z0-9_./:=,@%+\-]+''')


def closure_only(command):
    """True = standalone close, False = close with another command, None = unknown."""
    if not command.strip():
        return None
    # A Codex trace can include the outer shell. Its sole -c argument is the
    # actual command text. The inner script still has to match our grammar.
    if re.match(r"^/(?:usr/)?bin/(?:zsh|bash|sh) -l?c ", command):
        try:
            argv = shlex.split(command)
        except ValueError:
            return None
        if len(argv) != 3:
            return None
        command = argv[2]
    segments, words = [], []
    pos = 0
    end = 0
    pending_rhs = False
    for token in TOKEN.finditer(command):
        if token.start() != pos:
            return None
        pos = token.end()
        value = token.group()
        if value in ("&&", "||", ";", "\n"):
            if not words and value != "\n":
                return None
            if words:
                segments.append(words)
                words = []
                pending_rhs = value in ("&&", "||")
        elif not value.isspace() and value != "\\\n":
            if words and token.start() == end:  # compound/concatenated word
                return None
            words.append(shlex.split(value)[0])
            end = pos
            pending_rhs = False
    if pos != len(command) or pending_rhs:
        return None
    if words:
        segments.append(words)
    for args in segments:
        if args[:1] == ["rtk"]:
            args = args[1:]
            if args[:1] == ["proxy"]:
                args = args[1:]
        if not args or PurePosixPath(args[0]).name not in ("python", "python3"):
            continue
        args = args[1:]
        if args[:1] == ["-B"]:
            args = args[1:]
        if not args or PurePosixPath(args[0]).name != "tasks.py":
            continue
        args = args[1:]
        if args[:1] == ["--repo"]:
            args = args[2:]
        if args[:1] == ["close"]:
            return len(segments) == 1
    return None
