from flask import Flask, render_template, request
import pandas as pd
import json

app = Flask(__name__)

# 加载字典数据
dict_data = pd.read_csv('D:\\【名義等查詢】\\字典數據.csv', encoding='utf-8')

# 加载异体字数据
with open('D:\\【名義等查詢】\\異體字數據.json', encoding='utf-8') as f:
    variant_chars = json.load(f)


# 首页
@app.route('/')
def index():
    return render_template('index.html')


# 查询字的释义和异体字的释义
@app.route('/search', methods=['POST'])
def search():
    char = request.form['char']
    meanings, variant_meanings = get_meanings(char)
    return render_template('search.html', char=char, meanings=meanings, variant_meanings=variant_meanings)


# 获取字的释义和异体字的释义
def get_meanings(char):
    meanings = dict_data.loc[
        dict_data['字'].str.contains(char, na=False), ['字', '書名', '部件', '注文', '備註']].to_dict(orient='records')

    # 找到包含目标字的异体字组
    variant_group = []
    for v in variant_chars.values():
        if char in v:
            variant_group = v
            break

    variant_group = set(variant_group) - {char}

    # 获取异体字的释义
    variant_meanings = dict_data[dict_data['字'].isin(variant_group)][['字', '書名', '部件', '注文', '備註']].to_dict(
        orient='records')

    return meanings, variant_meanings


if __name__ == '__main__':
    app.run(debug=True, port=5004)
