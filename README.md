Docker-shell is a small utility to shell into a running Docker container by name or ID.

This uses Typer, which itself uses Click.

# Requirements

If you can use [pipx](https://github.com/pipxproject/pipx), then just that and it'll handle it. Otherwise, You'll need:

- Python 3.8+
- Poetry

# Installation

You can either install directly from the release (using version 0.1.0 as an example) via:

```sh
pipx install https://github.com/ewdicus/docker-shell/archive/docker_shell-0.1.0-py3-none-any.whl
```

or, you can download the wheel from the releases and then follow step 4 below in [From source](#from-source).

## From source

This is still in development and I don't think building this and installing it yourself is bad. If you want to try that, the steps should be:

1. Clone this repo
2. `poetry install`
3. `poetry build`
4. `pipx install <wherever this is>/docker_shell-0.1.0-py3-none-any.whl`

> Note: If you install via pip rather than pipx make sure to use `pip install --user ...` so this installs in your user's directory.

# Usage

If you just run `docker-shell` you'll get a nice little table of running containers:

```sh
$ docker-shell

| ID         | Name              | Image Tags                 |
|------------|-------------------|----------------------------|
| d1e5dab390 | aminoweb_nginx_1  | ['aminoweb_nginx:latest']  |
| c817abb130 | aminoweb_www_1    | ['aminoweb_www:latest']    |
| 1020d0c04f | aminoweb_www_js_1 | ['aminoweb_www_js:latest'] |
```

If you type `docker-shell` and then hit tab, it should autocomplete running container names:

```sh
$ docker-shell aminoweb_
aminoweb_nginx_1   aminoweb_www_1     aminoweb_www_js_1
```

Running `docker-shell` with either a container name or ID will open a bash shell into that container (with a fallback to sh).

```sh
$ docker-shell aminoweb_www_1
amino@c817abb1309e:/data/app$
```

> Note: You can customize the command that's executed on the running container with the -c/--command option, or by setting a `DOCKER_SHELL_COMMAND` env var.

And just for the sake of being complete here's the help:

```sh
$ docker-shell --help
Usage: docker-shell [OPTIONS] [CONTAINER]

Shell into a running Docker container by name or ID.

If run with no arguments, will display running containers. Change the
shell command with --command, -c, or by setting an env var called
DOCKER_SHELL_COMMAND.

Arguments:
[CONTAINER] This can be a container name or ID.

Options:
-c, --command TEXT The shell command to run in the container. [env var:
DOCKER_SHELL_COMMAND; default: /bin/sh -c "[ -e
/bin/bash ] && /bin/bash || /bin/sh"]

--install-completion Install completion for the current shell.
--show-completion Show completion for the current shell, to copy it or
customize the installation.

--help Show this message and exit.
```
