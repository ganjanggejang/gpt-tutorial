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
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages = [
            {'role': 'user', 'content': generate_prompt(input_text)}
          ],
          temperature=0.7,
          max_tokens=64,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
        return redirect(url_for("index", result=response['choices'][0]['message']['content']))
    
    # request.method == "GET"일 때
    result = request.args.get("result")
    return render_template("index.html", result=result) # html파일에 result 변수도 같이 전달



  
def generate_prompt(input_text):
    return """Summarize this for a high-school student: 
    {}
    """.format(input_text)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)