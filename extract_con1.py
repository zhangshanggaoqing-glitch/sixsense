import subprocess
import unicodedata

p = "/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2020年07月CET6题+解+音频/2020.07英语六级考试全1套解析.pdf"
res = subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True)
txt = unicodedata.normalize("NFKC", res.stdout)

pos_con1 = txt.find("Conversation One")
pos_con2 = txt.find("Conversation Two")
print("=== Conversation One English & Notes ===")
print(txt[pos_con1:pos_con2])

pos_trans1 = txt.find("全文翻译")
print("=== Translation snippet ===")
print(txt[pos_trans1:pos_trans1+1200])
