import typer


def error_text(text: str):
    return typer.style(text, fg=typer.colors.RED)


def info_text(text: str):
    return typer.style(text, fg=typer.colors.CYAN)


def dim_text(text: str):
    return typer.style(text, dim=True)


def bold_text(text: str):
    return typer.style(text, bold=True)
