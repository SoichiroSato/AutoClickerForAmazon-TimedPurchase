import stdiomask
from OperateAmazon import OperateAmazon 
from NTPClient import NTPClient
from TimeUtiltys import TimeUtiltys 
from CheckUtiltys import CheckUtiltys
from datetime import datetime,date,timedelta
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import messagebox,Tk
from sys import exit

#Amazonの自動購入プログラム
def main():
    
    Tk().withdraw()
    if not messagebox.askokcancel("確認", "このプログラムはGoogleChromeを使用します。\r\nインストール済みの方は「OK｝を押してください。\r\nまだの方は「キャンセル」を押してください。"):
        return
        
    print("★プログラムの説明★")
    print("・購入予定時刻の2分前に自動でログイン処理を行ない、購入予定時刻に自動で購入するツールです。")
    print("・このツールは購入時刻に「今すぐ買う」ボタンが表示できるページのみ使えます。")
    print("・あらかじめカートの中身は空にしておいてください。")
    print("・あらかじめ購入決済方法は一つにしておいてください。「クレジットカード」を推奨します。")
    print("・各入力項目は入力後に「Enter」キーを押してください。")
    print("・[*]がある入力項目は必須です。ないものは任意で設定してください。")
    print("　")

    while True:  
        print("高速版を使用しますか？")
        print("初回起動は通常版をオススメします。")
        headless= input("*y/n>")
        if headless == "y" or headless == "n":
            break
        else:
            print("yかnを入力してください")

    while True:   
        login = input("*ログインID(半角)>")
        if login != "":
            if CheckUtiltys.CheckMailAddress(login):
                break
            elif CheckUtiltys.CheckPhoneNumber(login):
                break
            else:
                print("ログインIDが不正です。")
        else:
            print("ログインID(半角)は必須です。")
            
    while True:  
        password = stdiomask.getpass("*ログインPassWord(半角)>")
        if password != "":
            if CheckUtiltys.CheckHankakuEisuziKigou(password):
                break
            else:
                print("ログインpasswordが不正です。")
        else:
            print("ログインPassWord(半角)は必須です。")
    
    while True:
        purchaseGoodsUrl = input("*買いたい商品のURL>")
        if purchaseGoodsUrl != "":
            if CheckUtiltys.CheckURL(purchaseGoodsUrl,"www.amazon.co.jp"):
                break
            else:
                print("AmazonのURLを入力してください。")
        else:
            print("買いたい商品のURLは必須です。")

    checkColor = input("カラーを選択する場合は左または上から順に0から半角数値で入力してください。未入力可。(例)一番左を選択の場合「0」>")
    checkSize = input("サイズを選択する場合は左または上から順に0から半角数値で入力してください。未入力可。(例)一番上を選択の場合「0」>")
    quantity = input("2つ以上購入する場合は購入個数を入力してください。1つの場合は未入力。>")

    while True:
        try:
            start = datetime.strptime(input("*購入時間(hh:mm)>") + ":00","%H:%M:%S").time()
            before2Minites = datetime.combine(date.today(), start) - timedelta(minutes=2)
            loginTime = datetime.combine(date.today(), before2Minites.time()) #購入予定時刻の2分前
            before1Seconds = datetime.combine(date.today(), start) - timedelta(seconds=1)
            purchaseTime = datetime.combine(date.today(), before1Seconds.time()) #購入予定時刻の1秒前
            break
        except Exception as e:
            print("[error]開始時刻が不正です。もう一度入力してください")
            continue

    print("ログイン処理実行時刻："+str(loginTime))
    print("購入処理実行時刻："+str(purchaseTime))

    ntpClient = NTPClient("ntp.nict.jp")
    
    #chromeのバージョンに合せたドライバーをインストールする
    #まぁまぁ重いから先にやっておく
    driverPath = ChromeDriverManager().install()
    
    #シークレットブラウザ/画面サイズ最大/画像を読み込まない
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito') 
    options.add_argument('--start-maximized')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--lang=ja')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    #高速版の場合はヘッダーレス
    if headless =="y":
        options.add_argument("--headless")

    #ログイン処理実行時刻まで待機
    TimeUtiltys.MakeSleep(TimeUtiltys.FindTheTimeDifference(loginTime,ntpClient))

    driver = webdriver.Chrome(driverPath,chrome_options=options)
   
    #指定したdriverに対して最大で10秒間待つように設定する
    driver.implicitly_wait(10)
   
    #ログイン処理
    OperateAmazon.Login(driver,login,password,headless)
    
    #購入処理実行時刻まで待機
    TimeUtiltys.MakeSleep(TimeUtiltys.FindTheTimeDifference(purchaseTime,ntpClient))

    OperateAmazon.Purchase(driver,purchaseGoodsUrl,checkColor,checkSize,quantity)

    while True:
        finish = input("終了するにはEnterキーを押してください")
        if not finish:
            break
    exit()

if __name__=='__main__':       
    main()
