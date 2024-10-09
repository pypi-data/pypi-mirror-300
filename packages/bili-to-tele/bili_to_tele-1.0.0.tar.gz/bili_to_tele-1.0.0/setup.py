from setuptools import setup, find_packages

# 读取 README 文件作为长描述
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bili_to_tele",  # 项目名称
    version="1.0.0",  # 版本号，根据需要更新
    author="aiko",  # 您的名字或组织名
    author_email="hideonbushplease774@gmail.com",  # 您的邮箱
    description="A tool to push Bilibili live and dynamic updates to Telegram",  # 简短描述
    long_description=long_description,  # 长描述，通常是 README 文件的内容
    long_description_content_type="text/markdown",  # 说明长描述的内容类型
    url="https://github.com/YourUsername/bili_to_tele",  # 项目的主页（如 GitHub 仓库）
    packages=find_packages(),  # 自动发现所有包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # 选择合适的许可证
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # 指定 Python 版本
    install_requires=[
        "httpx>=0.23.0",
        "loguru>=0.5.3",
        "pydantic>=1.10.2",
        "aiomysql>=0.1.1",
        "pymysql>=1.0.2",
        "aiohttp>=3.8.1",
        "brotli>=1.0.9",
        "creart>=0.1.4",
        "graia-ariadne>=2.0.3",
        "graia-saya>=0.2.22",
        # 添加其他必要的依赖
    ],
    entry_points={
        "console_scripts": [
            "bili_to_tele=bili_to_tele.core.bot:StarBot.run",  # 更新为新的包名
        ],
    },
    include_package_data=True,  # 包含包内数据文件
    package_data={
        "bili_to_tele": ["data/*.json", "painter/*.ttf"],  # 根据需要调整
    },
    keywords="bilibili telegram push notifications",  # 相关关键词
    license="MIT",  # 项目许可证
)