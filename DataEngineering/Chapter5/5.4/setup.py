from setuptools import setup, find_packages # 將程式碼打包為套件
from os import path
from io import open

#抓取檔案所在路徑
here = path.abspath(path.dirname(__file__)) # dirname 是抓取檔案前面的路徑、abspath 是將目前路徑和 dirname 抓的路徑合併

with open(path.join(here, "README.md"), encoding="utf-8") as f: # 透過 with 讀檔案會自動關閉檔案
    long_description = f.read() # 讀取檔案內容

# 套件資訊
setup( 
    name="financialdata",  # Required
    version="1.0.1",  # Required
    description="financial mining",  # Optional
    long_description=long_description,  # Optional
    long_description_content_type="text/markdown",  
    # Optional (see note above)
    url="https://github.com/linsamtw",  # Optional
    author="linsam",  # Optional
    author_email="samlin266118@gmail.com",  # Optional
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="financial, python",  # Optional
    project_urls={  # Optional
        "documentation": "https://linsamtw.github.io/FinMindDoc/",
        "Source": "https://github.com/linsamtw/FinMind",
    },
)
