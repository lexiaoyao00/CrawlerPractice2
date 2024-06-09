from .spider_baidu import BaiDu
from .spider_danbooru import Danbooru,PostInfo

##### 动态导入1 #############

# import os
# import importlib

# # 获取当前文件所在的目录路径
# package_dir = os.path.dirname(__file__)

# # 遍历目录下的所有文件
# for file in os.listdir(package_dir):
#     if file.endswith('.py') and file != '__init__.py':
#         module_name = file[:-3]  # 去掉文件扩展名.py
#         module = importlib.import_module(f'spiders.{module_name}')
#         globals().update({name: getattr(module, name) for name in dir(module) if not name.startswith('_')})


##### 动态导入2 #############

# import pkgutil
# import importlib
# import inspect

# __all__ = []

# def is_local_class(obj):
#     """
#     检查一个对象是否是当前包中定义的类
#     """
#     if inspect.isclass(obj):
#         module = inspect.getmodule(obj)
#         if module:
#             return module.__name__.startswith(__name__ + ".")
#     return False

# for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
#     module = importlib.import_module(f".{module_name}", package=__name__)
#     for name, obj in vars(module).items():
#         if is_local_class(obj):
#             setattr(__import__(__name__), name, obj)
#             __all__.append(name)

# print(__all__)
