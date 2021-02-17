import os
import shutil

from invoke import task


def copy(from_path: str, to_path: str):
    if os.path.isdir(from_path):
        shutil.copytree(from_path, to_path)
    elif os.path.isfile(from_path):
        shutil.copy(from_path, to_path)


@task
def clean(c):
    c.run("pyclean .")


@task
def format(c):
    c.run("isort MODULE_NAME")
    c.run("black MODULE_NAME")


@task
def lint(c):
    c.run("flake8 MODULE_NAME --max-line-length 119 --extend-ignore 'E203, W503'")


@task
def type_check(c):
    c.run("mypy MODULE_NAME --ignore-missing-imports")


@task
def test(c):
    c.run("pytest MODULE_NAME/test")


@task
def docs(c):
    os.makedirs("docs", exist_ok=True)
    c.run("pydoc-markdown -p MODULE_NAME > docs/api.md")
    copy("README.md", "docs/")
    c.run("mkdocs build --clean")


@task
def build(c):
    c.run("poetry build")


@task
def publish(c):
    c.run("mkdocs gh-deploy")
    c.run("poetry publish")

    version = c.run("poetry version -s").stdout

    c.run(f'git commit -m "v{version}"')
    c.run(f"git tag v{version}")
    c.run(f"git push origin v{version}")
