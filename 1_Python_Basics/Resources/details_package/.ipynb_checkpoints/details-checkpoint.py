import os,sys
from os.path import abspath,join,dirname
sys.path.insert(0,abspath(join(dirname(__file__),'..')))

from payment_package import payment_details
def details():
    print("this is my details file")

payment_details.payment()