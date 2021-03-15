import os
import time
import logging

logging.basicConfig(format="%(asctime)s-%(levelname)s-%(message)s", level=logging.INFO)


def auto_deploy():
    # git pull
    try:
        logging.info("执行 git pull ...")
        os.system("git pull")
        logging.info("执行编译...")
        os.system("mkdocs build")
        logging.info("git commit ...")
        os.system("git add *")
        os.system("git commit -m \"{}\"".format(int(time.time())))
        logging.info("git push ...")
        os.system("git push")
    except Exception as e:
        logging.error(e)


if __name__ == "__main__":
    auto_deploy()