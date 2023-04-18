#Objective:- Building a Flask app for scrapping product reviews

#importing all the necessary libraries
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uopen
import logging
import pymongo
import requests

#initialising app
app = Flask(__name__)

#rendering homepage
@app.route("/",methods=['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")

#defining index page function
@app.route("/review",methods=['POST','GET'])
@cross_origin()
def index():
    if request.method=='POST':
        try:
            search_string=request.formp['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + search_string

            #getting html response
            html_response = uopen(flipkart_url)
            read_response = html_response.read()
            html_response.close()

            #beautifying page
            bs_page = bs(read_response,"html.parser")
            bigboxes = bs_page.find_all("div",{"class":"_1AtVbE col-12-12"})
            del bigboxes[0:1]
            for box in bigboxes:
                product_link = "https://www.flipkart.com" + box.div.div.div.a['href']
                prod_res = requests.get(product_link)
                prod_res.encoding='utf-8'
                prod_html = bs(prod_res.text,"html.parser")
                


                comment_boxes = prod_html.find_all('div',{'class':'_16PBlm'})


                filename = search_string+".csv"
                f = open(filename,"w")
                headers = "Products, Customer Names, Rating, Heading, Comment \n"
                f.write(headers)
                reviews = []
                for cmmt_box in comment_boxes:
                    try:
                         #name.encode(encoding='utf-8')
                        name = cmmt_box.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                    except:
                        name = 'no name'
                    try:
                        rating = cmmt_box.div.div.div.div.text
                    except:
                        rating = 'no rating'
                    try:
                        comment_head = cmmt_box.div.div.div.p.text
                    except:
                        comment_head = 'No Comment Heading'
                    try:
                        comtag = cmmt_box.div.div.find_all('div',{'class': ''})
                        custcomment = comtag[0].div.text
                    except Exception as e:
                        print("Exception while creating dictionary: ",e)

                    mydict = {"Product":search_string,
                              "Name":name,
                              "Rating":rating,
                              "CommentHead":comment_head,
                              "comments":custcomment}
                    reviews.append(mydict)
            return render_template('result.html',reviews = reviews)
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
        else:
            return render_template('index.html')
if __name__=="__main__":
    app.run(host="0.0.0.0")