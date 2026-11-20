"""Local Git operations for an explicitly authorized parallel Engineer run."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], stdout=subprocess.PIPE, check=True).stdout


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def path_summary(entries):
    names = [ascii(os.fsdecode(entry)) for entry in entries[:8]]
    if len(entries) > 8:
        names.append(f"(+{len(entries) - 8} more)")
    return ", ".join(names)


def checkout(path):
    path = Path(path).resolve(strict=True)
    require(Path(os.fsdecode(git(path, "rev-parse", "--show-toplevel")).strip()).resolve() == path,
            "Expected exact checkout root")
    return path


def common(root):
    return (root / os.fsdecode(git(root, "rev-parse", "--git-common-dir")).strip()).resolve()


def head(root):
    return git(root, "rev-parse", "HEAD").decode().strip()


def admin_dir(root):
    return (root / os.fsdecode(git(root, "rev-parse", "--git-dir")).strip()).resolve()


def ref(root):
    return git(root, "rev-parse", "--symbolic-full-name", "HEAD").decode().strip()


def record(root, data):
    with (admin_dir(root) / "lean-run.json").open("x") as stream:
        json.dump(data, stream)


def ownership(root):
    data = json.loads((admin_dir(root) / "lean-run.json").read_text())
    require(data["path"] == str(root) and data["ref"] == ref(root), "Checkout identity changed")
    return data


def clean(root, ignored=False):
    admin = admin_dir(root)
    for marker in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD", "rebase-apply", "rebase-merge", "sequencer", "index.lock"):
        require(not (admin / marker).exists(), f"Unfinished Git operation: {root}")
    options = ["--ignored"] if ignored else []
    entries = git(root, "ls-files", "-v", "-z").split(b"\0")
    require(not any(entry[:1].islower() or entry.startswith(b"S ") for entry in entries),
            f"Index flags can hide changes: {root}")
    status = git(root, "-c", "core.fsmonitor=false", "status", "--porcelain=v1", "--no-renames", "-z",
                 "--untracked-files=normal", "--ignore-submodules=none", *options)
    if status:
        kinds = {b"!!": b"ignored: ", b"??": b"untracked: "}
        entries = [kinds.get(item[:2], b"tracked: ") + item[3:] for item in status.split(b"\0")[:-1]]
        raise ValueError(f"Preserved changes in {root}: {path_summary(entries)}")


def check_integration(root):
    require((root / ".git").is_file(), "Integration needs a linked worktree")
    name = git(root, "symbolic-ref", "--short", "HEAD").decode().strip()
    require(name.startswith("lean-integrate/"), "Expected a run integration branch")
    return name


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    begin = commands.add_parser("begin")
    begin.add_argument("repository")
    begin.add_argument("run")
    accept = commands.add_parser("accept")
    accept.add_argument("integration")
    accept.add_argument("worker")
    accept.add_argument("base")
    accept.add_argument("checkpoint")
    accept.add_argument("paths", nargs="+", help="Exact owned changed files, relative to the repository")
    finish = commands.add_parser("land")
    finish.add_argument("repository")
    finish.add_argument("integration")
    finish.add_argument("branch")
    finish.add_argument("base")
    finish.add_argument("verified")
    finish.add_argument("--commit", action="store_true", help="Fast-forward only with commit authority")
    retire = commands.add_parser("retire")
    retire.add_argument("keeper", help="Checkout retaining the accepted checkpoint")
    retire.add_argument("temporary", help="Exact run-created checkout from the host or begin")
    retire.add_argument("checkpoint")
    args = parser.parse_args(argv)
    if args.command == "begin":
        repo = checkout(args.repository)
        git(repo, "symbolic-ref", "--quiet", "HEAD")
        clean(repo)
        require(re.fullmatch(r"[A-Za-z0-9_-]+", args.run), "Invalid run name")
        previous = [os.fsdecode(f[9:]) for f in git(repo, "worktree", "list", "--porcelain", "-z").split(b"\0")
                    if f.startswith(b"worktree ")]
        path = Path(tempfile.mkdtemp(prefix="lean-integrate-")).resolve()
        try:
            git(repo, "worktree", "add", "-b", "lean-integrate/" + args.run, path, head(repo))
            record(path, dict(path=str(path), ref=ref(path), repo=str(repo), original_ref=ref(repo),
                              base=head(path), previous=previous))
        except subprocess.CalledProcessError:
            if not os.listdir(path):
                os.rmdir(path)
            raise
        print(path)
        return
    if args.command == "retire":
        keeper, temporary = checkout(args.keeper), checkout(args.temporary)
        require(keeper != temporary and common(keeper) == common(temporary), "Wrong checkout")
        # A primary checkout has no linked-worktree administration directory.
        require((temporary / ".git").is_file() and
                (temporary / os.fsdecode(git(temporary, "rev-parse", "--git-dir")).strip()).resolve().parent
                == common(keeper) / "worktrees", "Not a linked worktree")
        require(head(temporary) == args.checkpoint, "Checkpoint changed")
        data = ownership(temporary)
        require(str(keeper) in (data["repo"], data.get("integration")), "Keeper belongs to another run")
        if "accepted" in data:
            require(data["accepted"] == args.checkpoint, "Not the accepted worker checkpoint")
        git(keeper, "symbolic-ref", "--quiet", "HEAD")
        git(keeper, "merge-base", "--is-ancestor", args.checkpoint, "HEAD")
        clean(temporary, ignored=True)
        git(keeper, "worktree", "remove", str(temporary))
        return
    integration = checkout(args.integration)
    check_integration(integration)
    run = ownership(integration)
    clean(integration)
    if args.command == "accept":
        worker = checkout(args.worker)
        require(worker != integration and common(worker) == common(integration), "Wrong Engineer checkout")
        require((worker / ".git").is_file(), "Engineer needs a linked worktree")
        require(str(worker) not in run["previous"] and not (admin_dir(worker) / "lean-run.json").exists(),
                "Not a new, unassigned Engineer checkout")
        clean(worker)
        require(head(worker) == args.checkpoint, "Engineer checkpoint changed")
        require(git(worker, "rev-list", "--parents", "-n1", "HEAD").decode().split()[1:] == [args.base],
                "Expected one task commit on its assigned base")
        git(integration, "merge-base", "--is-ancestor", args.base, "HEAD")
        changed = git(worker, "diff", "--no-renames", "--name-only", "-z", args.base, "HEAD").split(b"\0")[:-1]
        require(bool(changed) and set(map(os.fsdecode, changed)) <= set(args.paths), "Changes outside assignment or empty checkpoint")
        try:
            git(integration, "-c", "rerere.enabled=false", "merge", "--no-overwrite-ignore",
                "--no-ff", "--no-edit", args.checkpoint)
        except subprocess.CalledProcessError as error:
            conflicts = git(integration, "diff", "--name-only", "--diff-filter=U", "-z").split(b"\0")[:-1]
            if not conflicts:
                raise
            raise ValueError(f"Conflicts in {integration}: {path_summary(conflicts)}. "
                             "Resolve and commit in integration, verify the result, then rerun accept before retire.") from error
        record(worker, dict(path=str(worker), ref=ref(worker), repo=run["repo"],
                            integration=str(integration), accepted=args.checkpoint))
    else:
        repo = checkout(args.repository)
        require(repo != integration and common(repo) == common(integration), "Wrong destination")
        require(run["repo"] == str(repo) and run["original_ref"] == ref(repo) and run["base"] == args.base,
                "Destination differs from run start")
        require(git(repo, "symbolic-ref", "--short", "HEAD").decode().strip() == args.branch,
                "Destination branch changed")
        require(head(repo) == args.base and head(integration) == args.verified, "Destination or verified revision changed")
        git(repo, "merge-base", "--is-ancestor", args.base, args.verified)
        clean(repo)
        git(repo, "merge", "--no-overwrite-ignore", "--ff-only" if args.commit else "--squash", args.verified)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        sys.exit(f"Parallel operation stopped: {error}")
