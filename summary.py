import MeCab
import re
from sklearn.feature_extraction.text import CountVectorizer


count_vect = CountVectorizer()
TAGGER = MeCab.Tagger("-Owakati")


def analysis(text):
    return TAGGER.parse(text).replace("\n", "").split()
    

def create_summary(text, sentences_count=3):
    for x in re.finditer(r"「.*?」", text):
        if x:
            parentheses_text = x.group()
            if "。" in parentheses_text:
                text = text.replace(
                    parentheses_text, 
                    parentheses_text.replace("。", " ")
                )

    text = text.strip().split("。")
    top = text[0]
    text.remove(top)
    
    if len(text) <= sentences_count:
        return False
    else:
        text = {
            count: dict(sentence=sentence.strip(), analyzed_sentence=analysis(sentence.strip()))
            for count, sentence in enumerate(text)
            if sentence != ""
        }

        for count in text:
            if text[count]["analyzed_sentence"] and text[count]["sentence"]:
                sentence = text[count]["analyzed_sentence"]
                try:
                    feature = count_vect.fit_transform(sentence).toarray()
                except:
                    severity = 0
                else:
                    severity = float(sum(sum(feature))/len(feature))
                finally:
                    text[count]["severity"] = severity

        data = {
            x[0]+1: x[1]["sentence"]+"。"
            for (count, x) in enumerate(sorted(text.items(), key=lambda x:x[1]["severity"], reverse=True))
            if count < sentences_count
        }

        data[0] = top+"。"

        return data


if __name__ == "__main__":
    text = """
妊婦に対する暴力や、座席に堂々と放尿をする立ちション男など、最近、韓国における電車内でのモラル低下が問題視されている。しかし、こうした乗客によるトラブルが多発しているのは、電車だけではない。
　10月末に仁川（インチョン）の市内の路線バス車内で起きた騒動は、大きな物議を醸している。なんと、泥酔した乗客の男（46）が突然、ズボンのチャックを下ろすと、その場で自慰行為を始めたのだ。男は、ほかの乗客の通報によって、現行犯逮捕された。
　驚いたのは、この男の職業だ。なんとは、同市の住民センターで働くベテラン公務員だったのだ。彼の処遇はまだ明らかになっていないが、バスの車内で自慰行為をして逮捕という前科は、以降の公務にも支障が出ることは間違いない。
　ネット民の間では、「こんな奴が公務員とは、この国が心配だ……」「酒をバカみたいに飲むから、犬野郎になるんだ。何事も、ほどほどがいい」などと、公務員という肩書も相まって、激しいバッシングにつながっている。
　一方、運転手自身が引き起こすトラブルも多々ある。中でも、運転中の携帯電話の使用は大きな問題だ。　
　なんと、ここ3年間だけで、携帯使用による前方不注意が原因のバス事故が4,000件余り発生、400人近い人命が損なわれているという。最近、日本では、トラック運転手が「ポケモンGO」に夢中になり、歩行者をはねるという事件があったが、韓国では乗客を乗せるバス運転手の多くが“ながら運転”をしているわけだ。
　乗客トラブルに始まり、運転手のながら運転など、何かと問題の絶えない韓国バス業界。最近では、特定の乗客に対して露骨な乗車拒否を行うバスまであるという。電車もダメ、バスも危険となれば、かの国での移動手段は、どうすればいいのだろうか？

"""

    result = create_summary(text=text, sentences_count=3)
    print(result[0])
    del result[0]
    for x in result:
        print(x, result[x])
