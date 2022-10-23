# 載入 pymongo 套件
from gc import collect
from operator import methodcaller
from tkinter.messagebox import NO
from unittest import result
import pymongo
# 連線到 MngoDB 雲端資料庫
client = pymongo.MongoClient("mongodb+srv://owner:owner123@mydatabase.icgmoth.mongodb.net/?retryWrites=true&w=majority")


# client = pymongo.MongoClient("mongodb+srv://owner:<password>@mydatabase.icgmoth.mongodb.net/?retryWrites=true&w=majority")
db = client.memberSystem

# 選擇操作 member_system 資料庫
# db = client.member_system
print("資料庫連線建立成功")



# 初始化伺服器
from flask import *
app=Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)
app.secret_key="secretKey"
# 處理路由
@app.route("/")
def index():
    return render_template("index.html")

# 進入會員頁
@app.route("/member")
def member():
    if "nickname" in session:
        nickname=session["nickname"]
        if nickname!="":
            nickname=nickname+"，"
            print(nickname)
        return render_template("member.html",nic=nickname)
    else:
        return redirect("/")

# /error?msg=錯誤訊息
@app.route("/error")
def error():
    message=request.args.get("msg","發生錯誤，請聯繫克服")
    return render_template("error.html",msa=message)

# 進入註冊頁面
@app.route("/register")
def register():
    return render_template("register.html")

# 註冊帳號，與資料庫互動
@app.route("/signup",methods=["POST"])
def signup():
    # 從前端接收資料
    nickname=request.form["nickname"]
    email=request.form["email"]
    password=request.form["password"]

    # 根據接收到的資料，和資料庫互動
    collection=db.user  #user為資料庫中集合的名稱

    # 檢查是否有相同email的資料
    result = collection.find_one({
        "email":email
    })
    if result != None:
        return redirect("/error?msg=信箱已經被註冊")
    collection.insert_one({
        "nickname":nickname,
        "email":email,
        "password":password
    })
    return redirect("/")


    # 登入
@app.route("/signin",methods=["POST"])
def signin():
    email=request.form["email"]
    password=request.form["password"]
    #和資料庫互動、比對
    collection=db.user
    result=collection.find_one({
        "$and":[
            {"email":email},
            {"password":password}
        ]
    })
    # 帳號密碼錯誤，跳轉至錯誤頁面
    if result==None:
        return redirect("/error?msg=帳號或密碼輸入錯誤")
    # 登入成功，在session 紀錄會員資訊，導向會員頁面
    session["nickname"]=result["nickname"]
    return redirect("/member")


# 登出，清除session資料
@app.route("/signout")
def signout():
    del session["nickname"]
    return redirect("/")

# 計算
@app.route("/count")
def count():
    number=request.args.get("number",None)
    result=int(number)*int(number)
    print(result)
    return render_template("countResult.html",res=result)


app.run(port=3000)