import logging
import re
from pathlib import Path

from mtmai.core import coreutils
from mtmai.core.config import settings
from mtmai.mtlibs import mtutils
from mtmai.mtlibs.mtutils import command_exists, is_in_gitpod, npm_patch_version
from mtmai.mtlibs.temboio import run_tmpbo_instance1
from mtmlib.github import git_commit_push
from mtmlib.mtutils import bash
from mtmlib.version_tag import patch_git_tag_version, read_tag

from . import huggingface

logger = logging.getLogger()


def get_bun_bin():
    if not command_exists("bun"):
        bash("curl -fsSL https://bun.sh/install | bash")
    return str(Path.home() / ".bun" / "bin" / "bun")


def init_project():
    if not coreutils.is_in_gitpod():
        return
    init_github_settings()
    if not mtutils.command_exists("bun"):
        bash("curl -fsSL https://bun.sh/install | bash")
    if not Path("./node_modules").exists():
        bash(f"{get_bun_bin()} i")

    if not Path(".env").exists():
        bash("cp env/dev.env .env")

    docker_config = Path.home().joinpath(".docker/config.json")
    if settings.DOCKERHUB_PASSWORD and not docker_config.exists():
        bash(
            f"(command -v docker && echo {settings.DOCKERHUB_PASSWORD} | docker login --username {settings.DOCKERHUB_USER} --password-stdin) || true"
        )

    if settings.NPM_TOKEN:
        npmrc = Path.home().joinpath(".npmrc")
        npmrc.write_text(f"//registry.npmjs.org/:_authToken={settings.NPM_TOKEN}\n")

    # if command_exists("cursor"):
    #     bash("cursor --version")
    #     bash("cursor --install-extension ms-python.vscode-pylance")
    #     bash("cursor --install-extension ms-python.python")
    #     bash("cursor --install-extension ms-toolsai.jupyter")
    #     bash("cursor --install-extension ms-toolsai.vscode-jupyter-slideshow")

    huggingface.hf_trans1_clone()


def init_github_settings():
    # 拉取所有标签, 如果仅拉起最浅层源码,会因缺少 tag 致构建失败
    bash("git fetch --tags")
    bash("(git fetch --unshallow || true)")
    bash("git config --replace-all --global pull.rebase false")
    bash(
        "git config --replace-all --global user.name a && git config --replace-all --global user.email a@a.com"
    )


def hf_trans1_commit():
    target_dir = (
        Path(settings.storage_dir)
        .joinpath(settings.gitsrc_dir)
        .joinpath(settings.HUGGINGFACEHUB_DEFAULT_WORKSPACE)
    )
    rnd_str = mtutils.gen_orm_id_key()
    Path(target_dir).joinpath("Dockerfile").write_text(f"""
# {rnd_str}
FROM docker.io/gitgit188/tmpboai
ENV DATABASE_URL={settings.DATABASE_URL}
ENV LOKI_USER={settings.LOKI_USER}
ENV GRAFANA_TOKEN={settings.GRAFANA_TOKEN}
ENV LOKI_ENDPOINT={settings.LOKI_ENDPOINT}
RUN sudo apt update

""")
    Path(target_dir).joinpath("README.md").write_text(f"""---
title: Trans1
emoji: 🏢
colorFrom: red
colorTo: gray
sdk: docker
pinned: false
license: other
app_port:  {settings.FRONT_PORT}
---""")
    bash(f"cd {target_dir} && git commit -am abccommit && git push")
    return {"ok": True}


def run_clean():
    bun_cache_dir = Path.home().joinpath(".bun/install/cache")
    bash(f"rm -rdf {bun_cache_dir}")

    if command_exists("pip"):
        logging.info("正在清理 pip 缓存")
        bash("pip cache dir && pip cache purge")
    if command_exists("docker"):
        logging.info("正在清理 docker 缓存")
        bash("docker system prune -f")

    if command_exists("pyenv"):
        bash("pyenv rehash")  # 可能不正确
    if is_in_gitpod():
        logger.info("删除 ~/.rustup")
        bash("rm -rdf ~/.rustup")
        logger.info("删除 ~/.rvm")
        dotrvm = Path.home().joinpath(".rvm")
        if dotrvm.exists():
            bash("rm -rdf ~/.rvm")


def docker_build_base():
    logger.info("🚀 build docker image_base")
    image_tag = f"{settings.DOCKERHUB_USER}/base"
    bash(
        f"docker build --progress=plain -t {image_tag} -f Dockerfile.base . && docker push {image_tag}"
    )
    logger.info("✅ build docker image_base")


async def run_deploy():
    await dp_vercel_mtmaiadmin()
    await run_tmpbo_instance1()
    logger.info("✅ tembo io pushed")
    hf_trans1_commit()
    logger.info("✅ hf_space_commit")
    git_commit_push()
    logger.info("✅ git_commit_push")


py_projects = [
    "mtmai",
    "mtmdb",
    "mtmlib",
    "mtmtrain",
    "mtmai-client",
    "mtmscreentocode",
    "mtmflow",
]


def run_testing():
    for project in py_projects:
        if Path(f"{project}/{project}/tests").exists():
            bash(f"cd {project} && coverage run -m pytest ")
            logger.info("✅ testing ok!")


def release_py():
    version_tag = read_tag()
    logger.info("version tag: %s", version_tag)
    # run_testing()
    for project in py_projects:
        dist_dir = Path(f"{project}/dist")
        if dist_dir.exists():
            bash(f"rm -rdf {dist_dir}")
        bash(f"cd {project} && poetry build")

    for project in py_projects:
        try:
            bash(f"cd {project} && poetry publish")
        except Exception as e:  # noqa: BLE001
            logger.info("⚠ pypi %s 发布失败 %s", project, e)

    for project in py_projects:
        mtutils.pyproject_patch_version(project)

    release_npm()
    next_version = patch_git_tag_version()
    logger.info("✅ patch_git_tag_version ok!,next version tag: %s", next_version)


def release_npm():
    npm_packages = [
        "apps/mtmaiweb",
        "apps/mtmaiadmin",
        "packages/mtmeditor",
        "packages/mtmscreentocode",
        "packages/mtxuilib",
        "packages/mtxlib",
        "packages/mtmaiapi",
    ]

    bash(f"{get_bun_bin()} run turbo build")

    for package in npm_packages:
        npm_patch_version(package)
    bash(f"{get_bun_bin()} run changeset publish --no-git-tag")
    logger.info("✅ release_npm ok!")


async def dp_cfpage():
    logger.info("🚀 正在部署 cfpage")
    from mtmlib import vercel

    pages = ["apps/mtmaiweb/src/app/(web)/layout.tsx"]
    pre_content = Path(pages[0]).read_text()
    # Check if the current runtime is nodejs before replacing
    if re.search(r'runtime\s*=\s*["\']nodejs["\']', pre_content):
        new_content = re.sub(r'runtime\s*=\s*"nodejs"', r'runtime="edge"', pre_content)
        Path(pages[0]).write_text(new_content)
        logger.info("✅ 替换layout 源码中的 runtime 为 edge")
    else:
        new_content = pre_content

    vercel.deploy_vercel(
        project_dir="apps/mtmaiweb",
        is_cfpage=True,
        project_name="mtmaiweb",
        vercel_token=settings.vercel_token,
    )

    # 恢复
    Path(pages[0]).write_text(pre_content)
    logger.info("✅ 恢复layout 源码中的 runtime 为原来的值")
    git_commit_push()


async def dp_vercel_mtmaiadmin():
    logger.info("🚀 正在部署到 vercel")
    from mtmlib import vercel

    vercel.deploy_vercel(
        project_dir="apps/mtmaiadmin",
        is_cfpage=False,
        project_name="mtmaiadmin",
        vercel_token=settings.vercel_token,
        deploy_to_vercel=True,
        build_local=False,
    )
    git_commit_push()
