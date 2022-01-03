from flask import Flask,render_template,request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route('/product',methods=['POST','GET'])
@cross_origin()
def reviewScrapper():
    if request.method == 'POST':
        try:
            search = request.form['content'].replace(" " , '')
            url="https://www.flipkart.com/search?q=" + search
            req=uReq(url)
            url_page=req.read()
            req.close()
            url_html=bs(url_page, 'html.parser')
            bigboxes=url_html.findAll('div',{'class': "_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box=bigboxes[0]
            productLink="https://www.flipkart.com"+box.div.div.div.a['href']
            prodReq=requests.get(productLink)
            prodReq.encoding='utf-8'
            prod_html=bs(prodReq.text,"html.parser")
            commentboxes=prod_html.findAll('div',{'class',"_16PBlm"})
            print(commentboxes)
            filename = search + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []
            for commentbox in commentboxes:
                try:
                    name=commentbox.div.div.findAll('p',{'class','_2sc7ZR _2V5EHH'})[0].text
                except:
                    name="No Name Found"

                try:
                    Rating=commentbox.div.div.div.div.text
                except:
                    Rating="No Rating found"

                try:
                    heading=commentbox.div.div.div.p.text
                except:
                    heading="No heading found"

                try:
                    comment=commentbox.div.div.findAll('div',{'class',''})[0].text
                except:
                    comment="No comment found"
                mydict={
                    "Product":search,
                    "Name":name,
                    "Rating":Rating,
                    "CommentHead":heading,
                    "Comment":comment
                }
                print(mydict)
                print("           ")
                reviews.append(mydict)
            return render_template('result.html', reviews=reviews[0:(len(reviews) - 1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


