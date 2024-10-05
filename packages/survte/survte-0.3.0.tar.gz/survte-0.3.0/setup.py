import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='survte',  
     version='0.3.0',
     scripts=['survte'] ,
     author="Jakob Samani",
     author_email="jakobsamani@gmail.com",
     description="A LandXML Viewer",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/samanii2/survte",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )