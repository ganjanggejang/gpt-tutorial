import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# main page
@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        input_text = request.form["input_text"]
        response_summarize = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages = [
            {'role': 'user', 'content': generate_prompt_1(input_text)}
          ],
          temperature=0.7,
          max_tokens=64,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
        response_keyword = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages = [
            {'role': 'user', 'content': generate_prompt_2(input_text)}
          ],
          temperature=0.7,
          max_tokens=128,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
        return redirect(url_for("index", result=response_summarize['choices'][0]['message']['content'], keyword=response_keyword['choices'][0]['message']['content']))
    
    # request.method == "GET"일 때
    result = request.args.get("result")
    keyword = request.args.get("keyword")
    return render_template("index.html", result=result, keyword=keyword) # html파일에 result 변수도 같이 전달




def generate_prompt_1(input_text):
    return """Summarize this for a high-school student: 
    {}
    """.format(input_text)


def generate_prompt_2(input_text):
    return """Pick 5 or so difficult keywords that require deeper learning of this text.:
    {}
    """.format(input_text)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)