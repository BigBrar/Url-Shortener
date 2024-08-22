import random
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# class create_link():
#     def __init__():

def string_shuffler():
    random_string = ['a','v','d','c','t','r','q']
    final_string = ''
    random.shuffle(random_string)
    while True:
        for things in random_string:
            final_string+=things
        string_already_exist = check_short_string(final_string)
        if string_already_exist:
            continue
        else:
            break
    return final_string


def check_short_string(short_string):
    found_status = False
    with open('long_url.json','r') as file:
        json_file = json.load(file)
        if short_string in json_file:
            return True
        else:
            return found_status


def check_long_url(long_url):
    short_url = None
    with open('long_url.json','r') as file:
        json_file = json.load(file)
        for url in json_file:
            if url['long_url'] == long_url:
                short_url = url['short_string']
    return short_url


def do_json(long_url, short_string):
    url_already_exist = check_long_url(long_url)
    if url_already_exist:
        print('found_em')
        return url_already_exist
    else:
        try:
            print("not found_em")
            with open('long_url.json','r') as file:
                data = json.load(file)
                json_url = {"long_url":long_url,"short_string":short_string}
                data.append(json_url)
            with open('long_url.json','w') as file:
                json.dump(data,file)
            return True
        except Exception as e:
            return "Something went wrong !!!"
        



@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/shortened",methods=['GET','POST'])
def shortened_url():
    if request.method == 'POST':
        long_url = request.form['long_url']
        if long_url:
            pass
        else:
            return "Hey, you. You are supposed to give the url that needs to be shortened !!!"
        short_string = string_shuffler()
        json_write = do_json(long_url,short_string)
        if json_write == True:
            pass
        else:
            print(json_write)
            return render_template("shortened.html", short_string=json_write)
        return render_template("shortened.html", short_string=short_string)
    return "You haven't given the url !!!"

@app.route("/<short_url>",methods=['GET'])
def test_function(short_url):
    if short_url == "favicon.ico":
        return ""
    long_url = ''
    short_string = str(short_url)
    print("Short_string - ",short_string)
    with open('long_url.json','r') as file:
        json_file = json.load(file)
        # print(json_file)
        for short_url in json_file:
            # print(short_url == short_string)
            if short_url['short_string'] == short_string:
                long_url = short_url['long_url']
                print(long_url)
            else:
                # print("nothing")
                continue
        return redirect(long_url)



if __name__ == ("__main__"):
    app.run(debug=True)