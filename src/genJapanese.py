import re
import markovify
import MeCab

def loadFiles(paths):
    text = ''
    for path in paths:
        #pythonのwithはスコープを生成しない
        with open(path) as f:
            text =  text + f.read()
    return text
        


def splitForMarkov(text):
    tagger = MeCab.Tagger()
    splitText = ''

    #https://github.com/jsvine/markovify/issues/84
    brokenStrings = [
        '(',
        ')',
        '[',
        ']',
        '"',
        "'",
    ]
    ##改行は基本的に文末にのみ現れること、文中に余計な空白が現れないことを想定している
    ##mecabでbrokenStringsに含まれる括弧などはそれぞれ1文字ずつ出てくる
    for line in text.split():
        parsed = tagger.parseToNode(line)
        while parsed:
            unit = parsed.surface
            if unit in brokenStrings: 
                unit = re.sub('[\[\(]', '「', unit)
                unit = re.sub('[\]\)]', '」', unit)
                unit = re.sub('[\'\"]', '', unit)
            splitText = splitText + unit
            if unit != '、' and unit != '。':
                splitText = splitText + ' '
            if unit == '。':
                splitText = splitText + '\n'
            parsed = parsed.next
        splitText = splitText + '\n'
    return splitText


def main():
    paths = ['./texts/matsuoka1.txt', './texts/matsuoka1_5.txt']
    text = loadFiles(paths)
    #wakati = MeCab.Tagger('-Owakati')
    #print(wakati.parse(text).split())
    splitText = splitForMarkov(text)
    textModel = markovify.NewlineText(splitText, state_size=2)
    for i in range(5):
        generated = textModel.make_short_sentence(50)
        if generated:
            generated = re.sub(' ','' , generated)
        print(generated)

if __name__ == '__main__':
    main()
