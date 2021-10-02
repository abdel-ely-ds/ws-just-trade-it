import nox
from nox.sessions import Session

locations = "src", "tests", "noxfile.py"
nox.options.sessions = "tests", "lint", "build", "blacken"
nox.options.stop_on_first_error = True


@nox.session(python=["3.9", "3.8"], reuse_venv=True)
def blacken(session: Session) -> None:
    """
    Run black code formatter
    """
    args = session.posargs or locations
    session.install("black==20.8b1", "isort==5.6.4")
    session.run("isort", *args)
    session.run("black", *args)


@nox.session(python=["3.9", "3.8"], reuse_venv=True)
def lint(session: Session) -> None:
    """
    Lint using flake8
    """
    args = session.posargs or locations

    session.install(
        "toml==0.10.2",
        "flake8==3.8.4",
        "flake8-black==0.2.1",
        "flake8-bugbear==20.1.4",
        "flake8-isort==4.0.0",
    )

    session.run("flake8", *args)


@nox.session(python=["3.9", "3.8"], reuse_venv=True)
def tests(session: Session) -> None:
    """
    Test code
    """
    session.install("pip", "install", ".[test]")
    session.run("pytest")
