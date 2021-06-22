from math import nan
from flask import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

app = Flask(__name__,static_folder="static",static_url_path="/")
app.config['SECRET_KEY'] = 'ricetia'

import boto3
import base64
import boto3, botocore
import pymysql
import datetime

import os
from dotenv import load_dotenv
load_dotenv()

@app.route("/")
def index():
	return render_template("message.html")

@app.route("/userpost",methods=['GET'])
def getdata():
    signup = pymysql.connect(
        host='ricetia-mysql.cyb5eosysjkk.ap-northeast-1.rds.amazonaws.com',
        port=3306,
        user='admin',
        password=os.getenv("RDS_password"),
        db='message',
        cursorclass=pymysql.cursors.DictCursor
        )
    with signup.cursor() as cursor:
        mysqlact = "select * from msg;"
        cursor.execute(mysqlact)
        result_page = cursor.fetchall()
    signup.close()

    photovalue = {}
    for i in range(len(result_page)):
        postnub = i + 1
        postnub = str(postnub)
        photovalue["%s"%(postnub)] = result_page[i]

    return photovalue

@app.route("/userpost",methods=['POST'])
def userpost():
    filedata = json.loads(request.data)

    filename = filedata["filename"]
    filetype = filedata["filetype"]
    imgfile = filedata["imgfile"]
    posttext = filedata["posttext"]

    imgdata = base64.b64decode(imgfile)
    with open(filename, 'wb') as f:
        f.write(imgdata)
    
    # 圖片上傳S3
    s3 = boto3.client(
        "s3",
        aws_access_key_id = os.getenv("S3_keyid"),
        aws_secret_access_key = os.getenv("S3_accesskey")
    )
    file = open(filename,'rb')
    bucket_name = "wanwanbucket"
    now = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    file_name = now + "/" + filename
    acl="public-read"
    s3.upload_fileobj(
        file,
        bucket_name,
        file_name,
        ExtraArgs={
            "ACL": acl,
            "ContentType": filetype
        }
    )
    os.remove(filename)

    # 圖片網址
    fileurl = "https://d2xsmezj0utol9.cloudfront.net/" + file_name

    # 資料上傳RDS
    signup = pymysql.connect(
        host='ricetia-mysql.cyb5eosysjkk.ap-northeast-1.rds.amazonaws.com',
        port=3306,
        user='admin',
        password=os.getenv("RDS_password"),
        db='message',
        cursorclass=pymysql.cursors.DictCursor
        )
    with signup.cursor() as cursor:
        mysqlact = "INSERT INTO msg (text,photo) VALUES (%s,%s)"
        cursor.execute(mysqlact,(posttext,fileurl))
        signup.commit()
    signup.close()

    messg = {"get imgurl":fileurl}
    return messg

app.run(port=3000)
# app.run(host="0.0.0.0",port=3000)