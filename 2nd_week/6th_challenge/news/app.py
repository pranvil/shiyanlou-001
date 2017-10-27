#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from flask import Flask, render_template
import os

app = Flask(__name__)
app.run(port=3000)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    article=[]
    file_list = os.listdir('/home/pranvil/test/files')
    for i in file_list:
        path = '/home/pranvil/test/files/'+i
        with open(path,'r') as file:
            for line in file:
                if 'title' in line:
                    line = line.split(':')
                    article.append(line[1])
    return render_template('index.html',article=article)


@app.route('/files/<filename>')
def file(filename):
    try:
        content=[]
        path = '/home/pranvil/test/files/'+filename+'.json'
        with open(path,'r') as file:
            for line in file:
                if 'title' in line or 'created_time' in line or 'content' in line:
                    content.append(line)
        return render_template('file.html',txt=content)
    except:
        return render_template('404.html'),404

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404


