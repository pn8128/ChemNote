[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)

# ChemNote

ChemNote is jupyter extention to execute physical calculation with unit.

## Installation
### Pip

```sh
pip install ChemNote
```

## How to Use

demo is [here](notebook/demo.ipynb)

### 基本的な使い方
```python
x=cn.define(数値,単位)
```
で定義。四則演算と累乗が扱える。
```python
x.show(有効数字)
```
で数式として表示。ただし、jupyter notebook上では、最終行に
```
x
```
とあるだけで数式として表示される。
```python
print(x)
```
とした場合、コピーしやすいtexのテキストとして表示される。(両端を\$で囲うとマークダウン下で数式表示される。)
