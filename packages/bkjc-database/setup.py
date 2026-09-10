import sys

if __name__=="__main__":
    if len(sys.argv)<=1:
        sys.argv.append("install")


from setuptools import setup
setup()
