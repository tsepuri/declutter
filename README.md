# declutter
The python file easily and intuitively reorganizes messy folders into four major subfolders: Docs, Media, Programming and Unknown, and several more inner subfolders based around similarities of file names and file types. It also gets rid of unnecessary and duplicate files and finally moves the content to a new folder. 
Note: This version has been built for MacOS only. 

## Getting started

These instructions will tell you how to get all of the code up and running on your local machine for development and testing, see deployment for notes on how to deploy it on a live server. 

### Prerequisites

You will need to have [pip](https://pip.pypa.io/en/stable/installing/) on your local machine, a command-line interface, a version of Python > 3.7 and an IDE that can run Python and .env. You will need to use MacOS for the current build.

### Installing

To install the required packages, use
```
pip install -r requirements.txt
```
You will need to replace the .env_sample file with a .env file that specifies the folders on your machine that you want to work with.

## Deployment

To deploy the code, you can use
```
python declutter.py
```
or 
```
python3 declutter.py
```
depending on where the version of Python > 3.7 is stored.

## Built with
* [Python](https://www.python.org/) - Everything

## Author
* **Tarun Sepuri**

## Acknowledgements

* I thank Kalle Hallden for the inspiration for the idea

 
