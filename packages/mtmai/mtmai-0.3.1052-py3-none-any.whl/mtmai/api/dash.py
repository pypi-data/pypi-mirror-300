import logging

from fastapi import APIRouter

from mtmai.models.dash import CmdkItem, DashConfig
# from mtmai.models.models import DocCollsPublic

router = APIRouter()

logger = logging.getLogger()


@router.get("/config", response_model=DashConfig)
async def config(
    # db: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
):
    """获取后台配置"""

    base_path = "/dash"
    dashConfig = DashConfig(
        navMenus=[
            {
                "title": "站点",
                "icon": "site",
                "variant": "ghost",
                "url": base_path + "/site",
            },
            {
                "title": "文章",
                "icon": "article",
                "variant": "ghost",
                "url": base_path + "/post",
            },
            # {
            #     "title": "搜索",
            #     "icon": "search",
            #     "variant": "ghost",
            #     "url": "/search",
            # },
            {
                "title": "任务",
                "icon": "boxes",
                "variant": "ghost",
                "url": "/site",
            },
            # {
            #     "title": "设置",
            #     "icon": "settings",
            #     "variant": "ghost",
            #     "url": "/settings",
            # },
        ]
    )
    return dashConfig


# @router.get("/user_menus", response_model=DocCollsPublic)
# async def user_menus(
#     # db: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
# ):
#     """获取用户菜单"""
#     user_cmdks = [
#         CmdkItem(label="数据管理", icon="", url=""),
#         CmdkItem(label="settings", icon="settings", url=""),
#         CmdkItem(label="退出", icon="logout", url=""),
#     ]
#     return user_cmdks
