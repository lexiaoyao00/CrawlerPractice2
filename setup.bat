@echo off

REM 创建虚拟环境
python -m venv venv

REM 激活虚拟环境
call venv\Scripts\activate

REM 安装项目依赖
pip install -r requirements.txt

REM 退出虚拟环境
deactivate