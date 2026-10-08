#!/usr/bin/env python3
import json
import re
import unicodedata
import docx
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 1. Parse choices from docx
doc_path = "/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2020年09月CET6题+解+音频/02、真题word/2020年09月六级真题（第1套）.docx"
doc = docx.Document(doc_path)
paras = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
q_raw = {}
cur_q = None
for p in paras:
    m = re.match(r'^(\d+)\.\s*(.*)', p)
    if m:
        cur_q = int(m.group(1))
        q_raw[cur_q] = m.group(2)
    elif cur_q and cur_q in q_raw and cur_q <= 25:
        q_raw[cur_q] += ' ' + p

q_choices = {}
for q in range(1, 26):
    s = q_raw[q]
    parts = re.split(r'([A-D]\))', s)
    opts = {}
    for i in range(1, len(parts), 2):
        letter = parts[i][0]
        text = parts[i+1].strip()
        opts[letter] = text
    q_choices[q] = opts

# 2. Parse explanations from PDF text
with open('/tmp/2020_09_set1_all.txt', 'r', encoding='utf-8') as f:
    norm = unicodedata.normalize('NFKC', f.read())

part2_start = norm.find('Part II Listening Comprehension')
part3_start = norm.find('Part III Reading Comprehension')
listening_part = norm[part2_start:part3_start]

sections = re.split(r'三[、\s]*试题精解', listening_part)

q_exps = {}
for sec_idx, sec in enumerate(sections[1:], 1):
    t_idx = sec.find('四、全文')
    if t_idx == -1:
        t_idx = sec.find('四、 全文')
    if t_idx != -1:
        sec_content = sec[:t_idx]
    else:
        sec_content = sec
    
    q_matches = list(re.finditer(r'(?:^|\n)(\d+)\.\s*([^\n]+)', sec_content))
    for i, qm in enumerate(q_matches):
        q_num = int(qm.group(1))
        q_text = qm.group(2).strip()
        start_pos = qm.end()
        end_pos = q_matches[i+1].start() if i+1 < len(q_matches) else len(sec_content)
        block = sec_content[start_pos:end_pos]
        
        ans_m = re.search(r'(?:【答案精析】|「答案精析】)\s*([A-D])。?([\s\S]*)', block)
        if ans_m:
            ans = ans_m.group(1).strip()
            exp = ans_m.group(2).strip()
            exp = re.sub(r'淘宝店铺.*', '', exp).strip()
            exp = re.sub(r'\d+/\d+页.*', '', exp).strip()
            exp = re.sub(r'第第 \d+/\d+页.*', '', exp).strip()
            exp = re.sub(r'\s+', ' ', exp).strip()
            q_exps[q_num] = {
                'answer': ans,
                'explanation': f"【精析】{exp}"
            }

prompts = {
    1: "Why does the woman say she can be so energetic?",
    2: "What has the woman been engaged in?",
    3: "What does the woman say about the benefit teaching brings to her?",
    4: "How does the woman say new scientific breakthroughs can be made possible?",
    5: "What do both speakers think of dreams?",
    6: "Why didn't the woman's grandmother take her scheduled flight?",
    7: "What does the woman say about people's emotions?",
    8: "What did psychologist Sigmund Freud say about adults' dreams?",
    9: "What did scientists first use to discover Lake Vostok in the 1970s?",
    10: "What do scientists think about Lake Vostok?",
    11: "What do the scientists hope their discoveries will do?",
    12: "Why did James Copeland want to study the American Indian tribe, Tarahumaras?",
    13: "How did Gonzalez help James Copeland?",
    14: "What does the speaker say about James Copeland's trip to the Tarahumara village?",
    15: "What impresses James Copeland about the Tarahumara tribe?",
    16: "What usually happens when people are accused of being radical?",
    17: "What is the speaker's definition of a radical?",
    18: "What does the speaker think of most radicals in American history?",
    19: "What does the speaker say about us as human beings?",
    20: "What does the speaker say Fred should do first to improve his quality of life?",
    21: "What does the speaker say about psychiatrists?",
    22: "What does the speaker say about the American dollar bill?",
    23: "What does the speaker say about the exact composition of the American dollar bill?",
    24: "Why did the new American government mint only coins for common currency?",
    25: "What have generations of American politicians argued for?"
}

final_questions = {}
for q in range(1, 26):
    final_questions[q] = {
        'prompt': prompts[q],
        'options': q_choices[q],
        'answer': q_exps[q]['answer'],
        'explanation': q_exps[q]['explanation']
    }

subparts_info = [
    {
        'id': '2020-09-set1-conv-1',
        'subpart_code': 'conv-1',
        'section_id': '2020-09-set1-sec-a',
        'section_title': 'Section A: Long Conversations',
        'type': 'conversation',
        'title': 'Conversation 1 · 教学与科研相长、科学普及与火星数据分析',
        'topic_zh': '教学与科研相长、科学普及与火星数据分析',
        'question_range': 'Q1 ~ Q4',
        'questions': [1, 2, 3, 4],
        'sp_start': 34.0,
        'sp_end': 235.0,
        'sentences': [
            ("M", "You are a professor of physics at the University of Oxford.", "您是牛津大学的物理学教授。"),
            ("M", "You're a senior advisor at the European Organization for Nuclear Research.", "担任着欧洲核子研究中心的高级顾问。"),
            ("M", "You also seem to tour the globe tirelessly, giving talks.", "似乎还在世界各地不知疲倦地做演讲。"),
            ("M", "And in addition, you have your own weekly TV show on science.", "此外，您每周还有自己的科普电视节目。"),
            ("M", "Where do you get the energy?", "您怎么会有这么多精力呢？"),
            ("W", "Oh, well, I just love what I do.", "呃，唔，我真的热爱我所做的一切。"),
            ("W", "I'm extremely fortunate to have this life, doing what I love doing.", "能过这样的生活，做我热爱做的事，我非常幸运。"),
            ("M", "Professor, what exactly is your goal?", "教授，您的目标到底是什么？"),
            ("M", "Why do you do all of this?", "您为什么要做这些事情？"),
            ("W", "Well, as you said, I do have different things going on, but these, I think, can be divided into two groups.", "嗯，正如你所说，我确实在做很多不同的事情，但我认为这些事情可以分为两类。"),
            ("W", "The education of science, and the further understanding of science.", "科学教育和对科学的进一步了解。"),
            ("M", "Don't these two things get in the way of each other?", "这两件事难道不会互相妨碍吗？"),
            ("M", "What I mean is, doesn't giving lectures take time away from the lab?", "我的意思是，讲课不会占用做实验的时间吗？"),
            ("W", "Not really, no.", "不会的，不会。"),
            ("W", "I love teaching, and I don't mind spending more time doing that now than in the past.", "我喜欢教学，我不介意现在比过去花更多的时间去做这件事。"),
            ("W", "Also, what I will say is that teaching a subject helps me comprehend it better myself.", "另外，我想说的是，教授一门学科有助于我更好地理解这门学科。"),
            ("W", "I find that it furthers my own knowledge when I have to explain something clearly.", "我发现，当我不得不解释清楚某事物时，教学能帮我进一步加深对它的理解。"),
            ("W", "When I have to aid others in understanding it, and when I have to answer questions about it, teaching at a high level can be very stimulating for anyone, no matter how much expertise they may already have in the field they are instructing.", "当我不得不帮助别人理解它、回答关于它的问题时，高阶段的教学对任何人来讲都是非常具有启发性的，不论他们在自己所教授的领域已有多少专业知识。"),
            ("M", "Are there any scientific breakthroughs that you see on the near horizon?", "您认为近期会有什么科学突破吗？"),
            ("M", "A significant discovery or invention we can expect soon?", "或者说我们很快就能盼来的重大发现或发明？"),
            ("W", "The world is always conducting science, and there are constantly new things being discovered.", "全世界一直都在开展科学研究，新事物不断地被发现。"),
            ("W", "In fact, right now we have too much data sitting in computers.", "事实上，我们当前有太多的数据存放在电脑里。"),
            ("W", "For example, we have thousands of photos of planet Mars taken by telescopes that nobody has ever seen.", "例如，我们有成千上万张用望远镜拍摄的火星照片，却没人看过它们。"),
            ("W", "We have them, yet nobody has had time to look at them with their own eyes, let alone analyze them.", "我们有这些照片，却没人有时间用自己的眼睛去看一眼，更不用说去分析它们了。")
        ]
    },
    {
        'id': '2020-09-set1-conv-2',
        'subpart_code': 'conv-2',
        'section_id': '2020-09-set1-sec-a',
        'section_title': 'Section A: Long Conversations',
        'type': 'conversation',
        'title': 'Conversation 2 · 梦境与迷信认知、理性与非理性情感、弗洛伊德心理学',
        'topic_zh': '梦境与迷信认知、理性与非理性情感、弗洛伊德心理学',
        'question_range': 'Q5 ~ Q8',
        'questions': [5, 6, 7, 8],
        'sp_start': 235.0,
        'sp_end': 431.6,
        'sentences': [
            ("M", "Do you think dreams have special meanings?", "你觉得梦有特殊含义吗？"),
            ("W", "No, I don't think they do.", "不，我不觉得它们有什么特殊含义。"),
            ("M", "I don't either, but some people do.", "我也不觉得，但有些人确实这么认为。"),
            ("M", "I would say people who believe that dreams have special meanings are superstitious, especially nowadays.", "我不得不说那些相信梦有特殊含义的人太迷信了，尤其是现在还这么认为的。"),
            ("M", "In the past, during the times of ancient Egypt, Greece or China, people used to believe that dreams could foresee the future.", "过去，在古埃及、古希腊和古中国时代，人们往往相信梦境可以预见未来。"),
            ("M", "But today, with all the scientific knowledge that we have, I think it's much harder to believe in these sorts of things.", "但今天，我们已掌握了如此多的科学知识，我觉得很难再相信这些说法。"),
            ("W", "My grandmother is superstitious, and she thinks dreams can predict the future.", "我祖母就很迷信，而且她认为梦可以预测未来。"),
            ("W", "Once, she dreamed that the flight she was due to take the following day crashed.", "有一次她梦到第二天自己要乘坐的飞机失事了。"),
            ("W", "Can you guess what she did?", "你能猜到她做了什么吗？"),
            ("W", "She didn't take that flight.", "她没去搭乘那趟航班。"),
            ("W", "She didn't even bother to go to the airport the following day.", "甚至第二天连机场都不愿去。"),
            ("W", "Instead, she took the same flight, but a week later.", "她转而乘坐了一周之后的同一航班。"),
            ("W", "And everything was fine, of course.", "当然，什么事都没发生。"),
            ("W", "No plane ever crashed.", "没有飞机坠毁。"),
            ("M", "How funny!", "真滑稽！"),
            ("M", "Did you know that flying is actually safer than any other mode of transport?", "你知道乘坐飞机实际上要比其他任何交通方式都安全吗？"),
            ("M", "It's been statistically proven.", "这是经过数据证实的。"),
            ("M", "People can be so irrational sometimes.", "人们有时候竟然可以荒唐至此。"),
            ("W", "Yes, absolutely.", "是啊，就是这样。"),
            ("W", "But even if we think they're ridiculous, emotions can be just as powerful as rational thinking.", "但即便我们认为他们很离谱，情感也确实会和理性思维一样影响强大。"),
            ("M", "Exactly.", "正是如此。"),
            ("M", "People do all sorts of crazy things because of their irrational feelings.", "人们会因为不理性的感受而做出各种疯狂的事情。"),
            ("M", "But in fact, some psychologists believe that our dreams are the result of our emotions and memories from that day.", "但其实，一些心理学家认为我们的梦来自于当天的情感和记忆。"),
            ("M", "I think it was Sigmund Freud who said that children's dreams were usually simple representations of their wishes.", "我想是西格蒙德·弗洛伊德曾说过，儿童的梦境通常是他们愿望的直接展现。"),
            ("M", "Things they wished would happen.", "即他们所希望发生之事。"),
            ("M", "But in adults, dreams are much more complicated reflections of their more sophisticated sentiments.", "但对于成年人，梦境则是对他们更丰富情感的更复杂的反映。"),
            ("W", "Isn't it interesting how psychologists try to understand, using the scientific method, something as bizarre as dreams?", "心理学家试图用科学的方法来理解梦境这么古怪的东西，这难道不是很有趣吗？"),
            ("W", "Psychology is like the rational study of irrational feelings.", "心理学就像是对非理性情感进行理性的研究。")
        ]
    },
    {
        'id': '2020-09-set1-pass-1',
        'subpart_code': 'pass-1',
        'section_id': '2020-09-set1-sec-b',
        'section_title': 'Section B: Passages',
        'type': 'passage',
        'title': 'Passage 1 · 南极冰下沃斯托克湖探测、极端微生物与地外生命探索',
        'topic_zh': '南极冰下沃斯托克湖探测、极端微生物与地外生命探索',
        'question_range': 'Q9 ~ Q11',
        'questions': [9, 10, 11],
        'sp_start': 431.6,
        'sp_end': 633.88,
        'sentences': [
            ("Speaker", "While some scientists explore the surface of Antarctica, others are learning more about a giant body of water four kilometers beneath the ice pack.", "当一些科学家在探索南极洲表面时，另一些科学家正在研究南极洲冰层下4千米处的巨大水体。"),
            ("Speaker", "Scientists first discovered Lake Vostok in the 1970s by using radio waves that penetrate the ice.", "20世纪70年代，科学家们使用可透过冰层的无线电波首次发现了沃斯托克湖。"),
            ("Speaker", "Since then, they have used sound waves and even satellites to map this massive body of water.", "自那以后，他们曾使用声波甚至卫星来测绘这片巨大的水域。"),
            ("Speaker", "How does the water in Lake Vostok remain liquid beneath an ice sheet?", "沃斯托克湖中的水是如何在冰盖下保持液态的？"),
            ("Speaker", "The thick glacier above acts like an insulating blanket and keeps the water from freezing, says Martin Siegert, a glaciologist from the University of Wales.", "威尔士大学的冰川学家马丁·西格特说：“上面这层厚厚的冰盖就像一条隔热毯一样防止水结冰。”"),
            ("Speaker", "In addition, geothermal heat from deep within the earth may warm the hidden lake.", "此外，来自地下深处的地热可能暖化了这个隐蔽的湖。"),
            ("Speaker", "The scientists suspect that microorganisms may be living in Lake Vostok, closed off from the outside world for more than two million years.", "科学家们猜测可能有微生物生活在沃斯托克湖，从而与外界隔绝了200多万年。"),
            ("Speaker", "Anything found there will be totally alien to what's on the surface of the earth, says Siegert.", "西格特说，在那里发现的一切都将与地表上的生物截然不同。"),
            ("Speaker", "Scientists are trying to find a way to drill into the ice and draw water samples without causing contamination.", "科学家们正试图找到一种方法，可以在不造成污染的情况下钻入冰层提取水样。"),
            ("Speaker", "Again, robots might be the solution.", "又一次，机器人成了可能的解决方案。"),
            ("Speaker", "If all goes as planned, a drill-shaped robot will melt through the surface ice.", "倘若一切按计划进行，一个钻头形状的机器人将熔化穿透地表冰层。"),
            ("Speaker", "When it reaches the lake, it will release another robot that can swim in the lake, take pictures and look for signs of life.", "当它到达湖面时，会释放出另一个能在湖中游泳、拍照并寻找生命迹象的机器人。"),
            ("Speaker", "The scientists hope their discoveries will shed light on life in outer space, which might exist in similar dark and airless conditions.", "科学家们希望他们的发现能为外太空的生命带来启示，外太空的生命可能存在于类似的黑暗和无空气环境中。"),
            ("Speaker", "Recently, close-up pictures of Jupiter's moon Europa showed signs of water beneath its icy surface.", "最近，木星的卫星“木卫二”的特写照片显示其冰冷表面下存在水迹象。"),
            ("Speaker", "Once tested in Antarctica, robots could be sent to Europa to search for life there, too.", "一旦在南极洲完成测试，机器人也可以被送往木卫二去寻找那里的生命。")
        ]
    },
    {
        'id': '2020-09-set1-pass-2',
        'subpart_code': 'pass-2',
        'section_id': '2020-09-set1-sec-b',
        'section_title': 'Section B: Passages',
        'type': 'passage',
        'title': 'Passage 2 · 美洲塔拉乌马拉语言研究、传统纯朴生活与文明反思',
        'topic_zh': '美洲塔拉乌马拉语言研究、传统纯朴生活与文明反思',
        'question_range': 'Q12 ~ Q15',
        'questions': [12, 13, 14, 15],
        'sp_start': 633.88,
        'sp_end': 826.47,
        'sentences': [
            ("Speaker", "The idea to study the American Indian tribe, Tarahumaras, came to James Copeland in 1984 when he discovered that very little research had been done on their language.", "1984年，詹姆斯·科普兰发现有关美洲印第安部落塔拉乌马拉语言的研究少之又少，便萌生了研究该部落的想法。"),
            ("Speaker", "He contacted a tribe member through a social worker who worked with the tribesmen in Mexico.", "他通过一名在墨西哥做部落成员工作的社工联系到了一位部落成员。"),
            ("Speaker", "At first, the tribe member, named Gonzalez, was very reluctant to cooperate.", "起初，这位名叫冈萨雷斯的部落成员非常不愿意配合。"),
            ("Speaker", "He told Copeland that no amount of money could buy his language.", "他告诉科普兰，再多的钱也买不到他的语言。"),
            ("Speaker", "But after Copeland explained to him what he intended to do with his research and how it would benefit the Tarahumaras, Gonzalez agreed to help.", "不过，在科普兰向他解释了“自己打算用这项研究做些什么”以及“这项研究将如何使塔拉乌马拉受益”之后，冈萨雷斯就答应帮忙了。"),
            ("Speaker", "He took Copeland to his village and served as an intermediary.", "他把科普兰带到自己的村庄，充当起了中间人。"),
            ("Speaker", "Copeland says, \"Thanks to him, the Tarahumaras understood what our mission was and started trusting us.\"", "科普兰说：“多亏了他，塔拉乌马拉人才明白了我们的使命是什么，而后开始信任我们。”"),
            ("Speaker", "Entering the world of the Tarahumaras has been a laborious project for Copeland.", "于科普兰而言，进入塔拉乌马拉人的世界是个艰辛的任务。"),
            ("Speaker", "To reach their homeland, he must drive two and a half days from Houston, Texas.", "他必须从德克萨斯州休斯顿出发，开两天半的车才能抵达他们的家乡。"),
            ("Speaker", "He loads up his vehicle with goods that the tribesmen can't easily get, and gives the goods to them as a gesture of friendship.", "他把部落成员无法轻易获得的东西装上车，再将这些东西送给他们以示友谊。"),
            ("Speaker", "The Tarahumaras, who don't believe in accumulating wealth, take the food and share it among themselves.", "不崇尚积累财富的塔拉乌马拉人接受了这些食物，并在彼此之间分享。"),
            ("Speaker", "For Copeland, the experience has not only been academically satisfying, but also has enriched his life in several ways.", "对科普兰来说，这一经历不仅在学术上令人满意，而且在很多方面丰富了他的生活。"),
            ("Speaker", "\"I see people rejecting technology and living a very hard, traditional life, which offers me another notion about the meaning of progress in the Western tradition,\" he says.", "他说：“我看到人们抗拒科技，过着非常艰苦的传统生活，这为我提供了另一种关于西方传统中进步意义的见解。”"),
            ("Speaker", "\"I experience the simplicity of living in nature that I would otherwise only be able to read about.\"", "“我体验到了大自然生活的简单纯朴，而这种简单原本我只能在书本上读到。”"),
            ("Speaker", "\"I see a lot of beauty in their sense of sharing and concern for each other.\"", "“在他们彼此分享和关心的意识中，我看到了许多美好。”")
        ]
    },
    {
        'id': '2020-09-set1-rec-1',
        'subpart_code': 'rec-1',
        'section_id': '2020-09-set1-sec-c',
        'section_title': 'Section C: Recordings',
        'type': 'recording',
        'title': 'Recording 1 · 激进分子的污名化、社会权力结构与历史进步推动力',
        'topic_zh': '激进分子的污名化、社会权力结构与历史进步推动力',
        'question_range': 'Q16 ~ Q18',
        'questions': [16, 17, 18],
        'sp_start': 826.47,
        'sp_end': 1090.56,
        'sentences': [
            ("Speaker", "What is a radical?", "什么是“激进分子”？"),
            ("Speaker", "It seems today that people are terrified of the term, particularly of having the label attached to them.", "如今，人们似乎很害怕这个词，特别是害怕被贴上这个标签。"),
            ("Speaker", "Accusing individuals or groups of being radical often serves to silence them into submission, thereby maintaining the existing state of affairs and, more important, preserving the power of a select minority who are mostly wealthy white males in Western society.", "指责个人或团体激进往往会压制他们的声音，进而使他们屈服，从而维持事态现状，更重要的是，这样会维护少部分精英人士的权力，而这些人在西方社会中大多是富有的白人男性。"),
            ("Speaker", "Feminism is a perfect example of this phenomenon.", "女权主义就是这种现象的一个典型例子。"),
            ("Speaker", "The women's movement has been plagued by stereotypes, misrepresentations by the media, and accusations of man-hating and radicalism.", "女性运动一直困扰于人们的刻板印象、媒体的歪曲以及外界对其厌男和激进主义的指责。"),
            ("Speaker", "When the basic foundation of feminism is simply that women deserve equal rights in all facets of life.", "尽管女权主义的基本诉求仅仅是女性在生活的各个方面享有平等的权利。"),
            ("Speaker", "When faced with the threat of being labeled radical, women back down from their worthy cause and consequently participate in their own oppression.", "当面临被贴上激进分子标签的威胁时，女性就会放弃呼吁自己应有的权益，从而加入到对自己的压迫中去。"),
            ("Speaker", "It has gotten to the point that many women are afraid to call themselves feminists because of the stigma attached to the word.", "现在已经到了许多女性不敢自称女权主义者的地步，因为这个词自带污名。"),
            ("Speaker", "If people refuse to be controlled and intimidated by stigmas, the stigmas lose all their power.", "如果人们拒绝被污名控制和恐吓，污名就会失去其所有的影响力。"),
            ("Speaker", "Without fear on which to feed, such stigmas can only die.", "没有了赖以生存的恐惧，这些污名就只能消亡。"),
            ("Speaker", "To me, a radical is simply someone who rebels against the norm or advocates a change in the existing state of affairs.", "对我来说，激进分子就是那些反抗常态或主张改变事态现状的人。"),
            ("Speaker", "On closer inspection, it becomes clear that the norm is constantly evolving and therefore is not a constant entity.", "仔细观察就会发现，常态很明显是在不断演变的，因此，它不是一个恒定的存在。"),
            ("Speaker", "So why then is deviation from the present situation such a threat when the state of affairs itself is unstable and subject to relentless transformation?", "那么，为什么在事态本身状况就不稳定、会不断变化的情况下，背离现状是一种威胁呢？"),
            ("Speaker", "It all goes back to maintaining the power of those who have it and preventing the rise of those who don't.", "这一切都源于要维护那些拥有权力的人的权力，阻止那些没有权力的人崛起。"),
            ("Speaker", "In fact, when we look at the word radical in a historical context, nearly every figure we now hold up as a hero was considered a radical in his or her time.", "事实上，当我们在历史背景下看“激进分子”这个词时，几乎每一个我们现在视为英雄的人物在他或她的时代都被认为是激进分子。"),
            ("Speaker", "Radicals are people who affect change.", "激进分子是那些推动变革的人。"),
            ("Speaker", "They are the people about whom history is written.", "他们是历史书写的对象。"),
            ("Speaker", "Abolitionists were radicals.", "废奴主义者是激进分子。"),
            ("Speaker", "Civil rights activists were radicals.", "民权活动家是激进分子。"),
            ("Speaker", "Even the founders of our country in their fight to win independence from England were radicals.", "甚至我们国家的开国元勋在争取脱离英国、赢得独立时也是激进分子。"),
            ("Speaker", "Their presence in history has changed the way our society functions, mainly by shifting the balance of power that previously existed.", "他们在历史上的存在改变了我们社会的运作方式，主要通过改变先前存在的权力平衡。"),
            ("Speaker", "Of course, there are some radicals who have made a negative impact on humanity, but undeniably there would simply be no progress without radicals.", "当然，也有一些激进分子对人类造成了负面影响，但不可否认的是，没有激进分子就没有进步。"),
            ("Speaker", "That being said, next time someone calls me a radical, I will accept that label with pride.", "话虽如此，如果下次有人叫我激进分子，我会骄傲地接受这个称呼。")
        ]
    },
    {
        'id': '2020-09-set1-rec-2',
        'subpart_code': 'rec-2',
        'section_id': '2020-09-set1-sec-c',
        'section_title': 'Section C: Recordings',
        'type': 'recording',
        'title': 'Recording 2 · 人际社交环境同化、心态悄然蜕变与主动选择人生伴侣',
        'topic_zh': '人际社交环境同化、心态悄然蜕变与主动选择人生伴侣',
        'question_range': 'Q19 ~ Q21',
        'questions': [19, 20, 21],
        'sp_start': 1090.56,
        'sp_end': 1313.56,
        'sentences': [
            ("Speaker", "We are very susceptible to the influence of the people around us.", "我们很容易受到周围人的影响。"),
            ("Speaker", "For instance, you may have known somebody who has gone overseas for a year or so, and has returned with an accent perhaps.", "举个例子，你或许认识一个出国一年左右的人，这个人回国后说话可能会带着异国腔调。"),
            ("Speaker", "We become part of our immediate environment.", "我们会融入我们当下所处的环境。"),
            ("Speaker", "None of us are immune to the influences of our own world and let us not kid ourselves that we are untouched by the things and the people in our life.", "没有人能免受自身所处世界的影响，所以不要自欺欺人地认为“自己没有受到生活中的事与人的影响”。"),
            ("Speaker", "Fred goes off to his new job at a factory.", "弗雷德到一个新工厂工作。"),
            ("Speaker", "Fred takes his 10-minute coffee break, but the other workers take a half an hour.", "他一般会花10分钟喝咖啡休息，但其余工人却会花上半个小时。"),
            ("Speaker", "Fred says, \"What's the matter with you guys?\"", "弗雷德说：“你们这帮人怎么回事？”"),
            ("Speaker", "Two weeks later, Fred is taking 20-minute breaks.", "两周后，弗雷德花20分钟休息。"),
            ("Speaker", "A month later, Fred takes his half hour.", "一个月后，他也花半个小时休息了。"),
            ("Speaker", "Fred is saying, \"If you can't beat them, join them.\"", "他说：“如果你没办法改变别人，就加入他们。”"),
            ("Speaker", "\"Why should I work any harder than the next guy?\"", "“我为什么要比其他人更卖力干活呢？”"),
            ("Speaker", "The fascinating thing about being human is that generally we are unaware that there are changes taking place in our mentality.", "人类的奇妙之处在于，我们通常无法意识到自己的心态正在发生转变。"),
            ("Speaker", "It is like returning to the city's smog after some weeks in the fresh air.", "这就像是在新鲜空气中待了数周之后，重新回到城市弥漫的烟雾中。"),
            ("Speaker", "Only then do we realize that we have become accustomed to the nasty smells.", "只有到了那时，我们才会意识到自己已经习惯了那些难闻的气味。"),
            ("Speaker", "Mix with critical people and we learn to criticize.", "与爱挑剔的人在一起，我们学会挑剔。"),
            ("Speaker", "Mix with happy people and we learn about happiness.", "与快乐的人在一起，我们懂得快乐。"),
            ("Speaker", "What this means is that we need to decide what we want from life and then choose our company accordingly.", "这意味着我们需要明确自己想要从生活中得到什么，然后相应地选择与谁交往。"),
            ("Speaker", "You may well say, \"That is going to take some effort.\"", "你很可能会说：“那需要付出一些努力。”"),
            ("Speaker", "\"It may not be comfortable.\"", "“可能不太舒服。”"),
            ("Speaker", "\"I may offend some of my present company.\"", "“可能会得罪我目前的一些朋友。”"),
            ("Speaker", "Right, but it is your life.", "没错，但这关乎你的人生。"),
            ("Speaker", "Fred may say, \"I'm always broke, frequently depressed.\"", "弗雷德可能会说：“我总是身无分文，经常感到沮丧。”"),
            ("Speaker", "\"I'm going nowhere and I never do anything exciting.\"", "“我一事无成，从不做任何刺激有趣的事情。”"),
            ("Speaker", "Then we discover that Fred's best friends are always broke, frequently depressed, going nowhere and wishing that life was more exciting.", "然后我们发现，弗雷德最好的朋友们也总是身无分文，经常感到沮丧，一事无成，而且希望生活能更刺激有趣。"),
            ("Speaker", "This is not coincidence.", "这绝非巧合。"),
            ("Speaker", "Nor is it our business to stand in judgment of Fred.", "对弗雷德指指点点也不是我们的分内之事。"),
            ("Speaker", "However, if Fred ever wants to improve his quality of life, the first thing he'll need to do is recognize what has been going on all these years.", "然而，如果弗雷德想要提高生活品质，首先要做的就是认清自己这些年都经历了什么。"),
            ("Speaker", "It's no surprise that doctors as a profession suffer a lot of ill health because they spend their lives around sick people.", "医生作为一个职业群体，身体状况经常欠佳，这不足为奇，因为他们整日与病人相处。"),
            ("Speaker", "Psychiatrists have a higher incidence of suicide in their profession for related reasons.", "出于类似的原因，精神病医生在这一职业中的自杀发生率更高。"),
            ("Speaker", "Traditionally, nine out of ten children whose parents smoke, smoke themselves.", "传统上，父母吸烟的孩子中有十分之九自己也吸烟。"),
            ("Speaker", "Obesity is in part an environmental problem.", "肥胖在一定程度上是一种环境问题。"),
            ("Speaker", "Successful people have successful friends and so the story goes on.", "成功人士结交成功的朋友，诸如此类的例子不胜枚举。")
        ]
    },
    {
        'id': '2020-09-set1-rec-3',
        'subpart_code': 'rec-3',
        'section_id': '2020-09-set1-sec-c',
        'section_title': 'Section C: Recordings',
        'type': 'recording',
        'title': 'Recording 3 · 美钞的历史演变、防伪工艺与美国货币体系沿革',
        'topic_zh': '美钞的历史演变、防伪工艺与美国货币体系沿革',
        'question_range': 'Q22 ~ Q25',
        'questions': [22, 23, 24, 25],
        'sp_start': 1313.56,
        'sp_end': 1576.10,
        'sentences': [
            ("Speaker", "Virtually every American can recognize a dollar bill at a mere glance.", "几乎每个美国人都能一眼认出美钞。"),
            ("Speaker", "Many can identify it by its sound or texture.", "许多人可以通过声音或质地将其识别。"),
            ("Speaker", "But few people indeed can accurately describe the world's most powerful, important currency.", "但实际上，几乎没有人能够准确描述这种世上最强大、最重要的货币。"),
            ("Speaker", "The American dollar bill is colored with black ink on one side and green on the other.", "美钞一面用黑墨着色，另一面用绿墨着色。"),
            ("Speaker", "The exact composition of the paper and ink is a closely guarded government secret.", "纸张和墨水的确切成分是政府严守的秘密。"),
            ("Speaker", "Despite its weighty importance, the dollar bill actually weighs little.", "尽管美钞的重要性非常重，但实际上它的重量却很轻。"),
            ("Speaker", "It requires nearly 500 bills to tip the scales at a pound.", "达到一磅需要近500张钞票。"),
            ("Speaker", "Not only is the dollar bill lightweight, but it also has a brief lifespan.", "美钞不仅重量轻，而且寿命短。"),
            ("Speaker", "Few dollar bills survive longer than 18 months.", "很少有美钞能使用18个月以上。"),
            ("Speaker", "The word \"dollar\" is taken from the German word \"thaler\", the name for the world's most important currency in the 16th century.", "“dollar”一词取自德语单词“thaler”，后者是16世纪世界上最重要货币的名称。"),
            ("Speaker", "The thaler was a silver coin first minted in 1518 under the reign of Charles V, Emperor of Germany.", "thaler是一种银币，于1518年德国皇帝查理五世统治时期首次铸造。"),
            ("Speaker", "The concept of paper money is a relatively recent innovation in the history of American currency.", "纸币的概念在美国货币史上是相对较晚的创新。"),
            ("Speaker", "When the Constitution was signed, people had little regard for paper money because of its steadily decreasing value during the colonial era.", "签署《宪法》时，人们对纸币几乎没有信心，因为在殖民时代纸币一直在不断贬值。"),
            ("Speaker", "Because of this lack of faith, the new American government minted only coins for common currency.", "由于缺乏信心，美国新政府仅铸造硬币作为通用货币。"),
            ("Speaker", "Interest-bearing banknotes were issued at the same time, but their purpose was limited to providing money for urgent government crises, such as American involvement in the War of 1812.", "当时也发行了带息纸币，但其目的仅限于为紧急的政府危机提供资金，例如美国卷入1812年战争。"),
            ("Speaker", "The first non-interest-bearing paper currency was authorized by Congress in 1862 at the height of the Civil War.", "第一种不带息纸币于1862年内战高潮时由国会批准发行。"),
            ("Speaker", "At this point, citizens' old fears of devalued paper currency had calmed, and the dollar bill was born.", "此时，公众对纸币贬值的旧有担忧已经平息，美钞由此诞生。"),
            ("Speaker", "The new green-colored paper money quickly earned the nickname \"Greenback\".", "这种新型的绿色纸币很快获得了“绿背纸币”的绰号。"),
            ("Speaker", "Today, the American dollar bill is a product of the Federal Reserve and is issued from the 12 Federal Reserve banks around the United States.", "今天，美钞是联邦储备系统的产物，由全美12家联邦储备银行发行。"),
            ("Speaker", "The government keeps a steady supply of approximately two billion bills in circulation at all times.", "政府始终保持约20亿张钞票在市场上稳定流通。"),
            ("Speaker", "Controversy continues to surround the true value of the dollar bill.", "围绕美钞真实价值的争论仍在继续。"),
            ("Speaker", "American history has seen generations of politicians argue in favor of a gold standard for American currency.", "美国历史上曾有数代政治家主张美国货币实行金本位制。"),
            ("Speaker", "However, for the present, the American dollar bill holds the value that is printed on it and little more.", "然而，目前美钞的价值仅限于其票面所印的面值，仅此而已。"),
            ("Speaker", "The only other guarantee on the bill is a Federal Reserve pledge as a confirmation in the form of government securities.", "该纸币的唯一其他保障是联邦储备银行以政府证券形式确认的承诺。")
        ]
    }
]

out_py = BASE_DIR / "pipeline" / "data_2020_09_set1.py"
with open(out_py, "w", encoding="utf-8") as f:
    f.write("#!/usr/bin/env python3\n")
    f.write('"""\n')
    f.write("Official data for 2020-09-set1 CET-6 listening test:\n")
    f.write("- 7 subparts with authentic titles, Chinese topics, and question ranges\n")
    f.write("- Complete grammatical sentences with 100% paired authentic Chinese translations\n")
    f.write("- 25 official CET-6 questions with options, answers, and explanations\n")
    f.write('"""\n\n')
    f.write("SUBPARTS = " + repr(subparts_info) + "\n\n")
    f.write("QUESTIONS = " + repr(final_questions) + "\n")

print(f"Successfully generated {out_py}!")
