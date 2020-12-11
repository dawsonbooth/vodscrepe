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
def lint(c):
    c.run("pylint vodscrepe")


@task
def test(c):
    c.run("pytest vodscrepe/test")


@task
def docs(c):
    c.run("pydoc-markdown -p vodscrepe > docs/documentation.md")
    copy("README.md", "docs/README.md")
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