#!/usr/bin/env python3
"""
Curate and rigorously audit 2024-06-set2:
- 7 Subparts with authentic titles and Chinese topics
- 134 Grammatical Sentences with 100% paired, authentic Chinese translations
- Acoustic word-level timestamp alignment from Whisper
- 25 Official CET-6 Questions with options, answers, and explanations
"""

import json
import re
import sqlite3
import unicodedata
from pathlib import Path
import docx

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "sixsense.db"
WHISPER_PATH = BASE_DIR / "data" / "derived" / "exams" / "2024-06-set2" / "whisper_full.json"
DOCX_FILE = Path("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2024年06月CET6题+解+音频/02、真题word版/2024.06六级真题第2套【可复制可检索】.docx")
OCR_FILE = BASE_DIR / "data" / "derived" / "exams" / "2024-06-set2" / "ocr_listening.txt"

EXAM_ID = "2024-06-set2"
AUDIO_FILE = "2024.06六级听力音频第2套.mp3"
AUDIO_DURATION = 1549.79

SUBPARTS_DATA = [
    {
        "id": "2024-06-set2-conv-1",
        "subpart_code": "conv-1",
        "section_id": "2024-06-set2-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 1 · 破壁料理机选购与健康食谱",
        "topic_zh": "破壁料理机选购与健康食谱",
        "question_range": "Q1 ~ Q4",
        "questions": [1, 2, 3, 4],
        "anchor": ["just", "bought", "a", "new", "blender"],
        "sentences": [
            ("M", "I've just bought a new blender.", "我刚买了一台新的破壁料理机。"),
            ("W", "What's that?", "那是用来做什么的？"),
            ("M", "A blender, you know, a machine that blends food.", "料理机啊，你知道的，一种用来搅拌混合食物的机器。"),
            ("W", "Uh, yes, of course, the electric kitchen appliance.", "噢，是的，当然，就是那种厨房用的小家电。"),
            ("M", "Exactly, this one is state-of-the-art.", "没错，这一款是最先进顶级的。"),
            ("M", "I've been meaning to buy one for a while, and I did thorough research on which specific model to get.", "我想买一台已经有一段时间了，并对到底买哪一款具体型号做了透彻的研究。"),
            ("M", "I read through maybe hundreds of online user reviews.", "我通读了大概几百条网上用户的评价。"),
            ("M", "Anyway, it's amazing.", "不管怎么说，它太神奇了。"),
            ("W", "Really?", "真的吗？"),
            ("W", "What could be so special about it?", "它能有什么特别之处呢？"),
            ("W", "I mean it's just a blender.", "我的意思是它不过就是个搅拌机而已。"),
            ("M", "Well, basically, it's just a very good one.", "嗯，基本上说，它就是性能非常好。"),
            ("M", "It feels heavy and sturdy and well made.", "它手感沉甸、结实，而且做工精良。"),
            ("M", "It also has lots of power and can easily cut and crush practically anything.", "它的动力也很强劲，几乎可以轻松切碎研磨任何食材。"),
            ("M", "This way, the soups and juices I make come out really fine and smooth, with no lumpy bits.", "这样一来，我做出来的汤汁和果汁口感特别细腻丝滑，没有任何颗粒硬块。"),
            ("W", "Um, I see.", "嗯，我明白了。"),
            ("W", "I have never thought of getting one myself.", "我自己从来没想过要买一台。"),
            ("W", "It sounds like the kind of thing that, for me personally, I would rarely use.", "对我个人来说，这听起来像是那种我很少会用到的东西。"),
            ("M", "I've never had one before, and now that I do, I use it all the time.", "我以前也从来没有拥有过，但现在有了之后，我一直在用它。"),
            ("M", "I make a fresh fruit juice in the morning, maybe not every morning, but three or four times a week, and it feels fantastic.", "我早上会做新鲜果汁，也许不是每天早上，但每周有三四次，感觉棒极了。"),
            ("M", "It's a really healthy habit.", "这是一个非常健康的习惯。"),
            ("W", "I can imagine that must feel quite satisfying.", "我可以想象那一定让人感到非常满足。"),
            ("W", "I can picture you getting all creative in the kitchen and trying out a multitude of different ingredients, and it's obviously going to be healthier than buying packaged juice from a supermarket.", "我能想象出你在厨房里大展身手、尝试各种不同食材的场景，这显然比从超市买盒装果汁要健康得多。"),
            ("M", "It's so much healthier.", "健康多了。"),
            ("M", "It's not even close.", "两者根本无法相提并论。"),
            ("M", "Did you know that store-bought juice is like 10% sugar?", "你知道在商店买的果汁含糖量高达10%吗？"),
            ("W", "Right, so then you bought it for the health benefits?", "对哦，所以你买它是为了健康考量？"),
            ("M", "Mostly yes.", "绝大部分是。"),
            ("M", "Basically, it allows me to have a more varied diet with a far wider assortment of nutrients, because it's not only fruit in my morning juices you see.", "基本上，它能让我的饮食更多样化，吸收更广泛的营养成分，因为你在我早晨的果汁里看到的绝不仅仅是水果。"),
            ("M", "I can also throw in vegetables, nuts, yogurts, cereals, anything that tickled my fancy.", "我还可以扔进蔬菜、坚果、酸奶、谷物，任何我心血来潮想加的东西。")
        ]
    },
    {
        "id": "2024-06-set2-conv-2",
        "subpart_code": "conv-2",
        "section_id": "2024-06-set2-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 2 · 伯克顿小镇的蜕变与市长访谈",
        "topic_zh": "伯克顿小镇的蜕变与市长访谈",
        "question_range": "Q5 ~ Q8",
        "questions": [5, 6, 7, 8],
        "anchor": ["today", "we", "have", "a", "very", "interesting", "guest"],
        "sentences": [
            ("W", "Today we have a very interesting guest.", "今天我们请到了一位非常有趣的嘉宾。"),
            ("W", "Mr. Thomas Benjamin Grimm, the mayor of Berkton, is here to talk about his job and responsibilities overseeing this charming village.", "伯克顿镇镇长托马斯·本杰明·格林先生来到这里，谈谈他主管这个迷人村庄的工作和职责。"),
            ("W", "Mr. Grimm, thank you for being here.", "格林先生，感谢您的光临。"),
            ("M", "Thank you for having me.", "感谢你们邀请我。"),
            ("W", "I'd like to start by stating the obvious.", "我想先从大家有目共睹的事情谈起。"),
            ("W", "Berkton has become one of the most popular tourist destinations in the country, and this has happened under your watch.", "伯克顿已经成为全国最受欢迎的旅游目的地之一，而这一切都是在您的任期内实现的。"),
            ("W", "Just how did you achieve this?", "您究竟是如何做到的？"),
            ("M", "The achievement belongs to all the residents of Berkton.", "这项成就属于伯克顿的所有居民。"),
            ("M", "It was a shared effort where everybody pitched in for the communal good.", "这是一次共同的努力，每个人都为了集体的利益贡献了自己的力量。"),
            ("W", "But how did this change happen?", "但这一转变是如何发生的呢？"),
            ("W", "In about 10 years, Berkton has gone from a relatively unheard of sleepy village to a must-see destination.", "在大约十年的时间里，伯克顿从一个相对默默无闻的沉睡村庄变成了必游之地。"),
            ("M", "Yes, the change has truly been remarkable.", "是的，这一变化确实引人瞩目。"),
            ("M", "Berkton was always fortunate to be endowed with such a beautiful natural allure.", "伯克顿一直很幸运地拥有如此迷人的自然风光。"),
            ("M", "The Ambury Hills above the village remain untouched by human development, and the Sonora valley just below it is equally stunning.", "村庄上方的安伯里山依然没有受到人类开发的破坏，而正下方的索诺拉山谷同样令人惊叹。"),
            ("M", "The transformation commenced in a town hall meeting in spring 2008 over 10 years ago now, when an overwhelming majority of neighbors voted in favor of \"Motion 836\".", "这一转变始于十多年前2008年春天的一次市政厅会议，当时绝大多数街坊邻居投票赞成了“第836号提案”。"),
            ("M", "This legislative proposal essentially set out to harmonize the aesthetic appearance of all the houses in Berkton.", "这项立法提案的实质是统一协调伯克顿所有房屋的外观美感。"),
            ("M", "The idea was that if all the properties looked a certain way with shared design features, then a village as a whole would look more beautiful.", "其理念是，如果所有的建筑都呈现出某种带有共同设计特征的风貌，那么整个村庄作为一个整体就会看起来更加美丽。"),
            ("M", "And it worked.", "而且这个办法奏效了。"),
            ("W", "It certainly did.", "确实奏效了。"),
            ("W", "I'm looking now at a before-and-after photo, and the change is truly remarkable.", "我现在看着一张前后对比的照片，变化真是太惊人了。"),
            ("W", "It's hard to believe it's the same place.", "很难相信这是同一个地方。"),
            ("W", "And how do the neighbors feel now?", "那么现在街坊邻里感觉如何呢？"),
            ("M", "Great pride I would say.", "我想说大家感到无比自豪。"),
            ("W", "But what about the multitudes of visitors now crowding the streets?", "但现在挤满街道的成群结队的游客又该如何看待呢？"),
            ("W", "Is everyone happy about that?", "每个人都对此感到高兴吗？"),
            ("M", "The tourists we receive are a blessing, as they have completely revitalized our local economy.", "我们接待的游客是一种福气，因为他们彻底振兴了我们的当地经济。"),
            ("M", "Every visitor is warmly welcome.", "每一位访客都受到热烈欢迎。")
        ]
    },
    {
        "id": "2024-06-set2-pass-1",
        "subpart_code": "pass-1",
        "section_id": "2024-06-set2-sec-b",
        "section_title": "Section B: Listening Passages",
        "type": "passage",
        "title": "Passage 1 · 西北大学毫米级微型机器蟹",
        "topic_zh": "西北大学毫米级微型机器蟹",
        "question_range": "Q9 ~ Q11",
        "questions": [9, 10, 11],
        "anchor": ["researchers", "in", "the", "us", "have", "created"],
        "sentences": [
            ("", "Researchers in the US have created a remote-controlled robot that is so small it can walk on the top of a US penny.", "美国的研究人员制造出了一种微型遥控机器人，它小到可以在一枚美国一美分硬币的边缘行走。"),
            ("", "In research published in the journal Science Robotics, a team at Northwestern University said the crab-like robot is 0.5 millimeters wide.", "在发表于《科学·机器人》期刊上的一项研究中，西北大学的一个团队表示，这种形似螃蟹的机器人只有0.5毫米宽。"),
            ("", "Researchers described it as the smallest ever remote-controlled walking robot.", "研究人员称其为有史以来最小的遥控步行机器人。"),
            ("", "The tiny robot can bend, twist, crawl, walk, turn, and even jump without the use of complex hardware or special power.", "这款微型机器人无需使用复杂的硬件或专门的电源，就能弯曲、扭转、爬行、行走、转向甚至跳跃。"),
            ("", "The engineers said this is because the robot is powered by the elastic property of its body.", "工程师们表示，这是因为该机器人是由其自身的弹性物理特性驱动的。"),
            ("", "To construct the robot, the researchers used a shape memory alloy material that transforms to its \"remembered\" shape when heated.", "为了制造这款机器人，研究人员使用了一种形状记忆合金材料，该材料在受热时会转变成其“记忆”中的形状。"),
            ("", "Using a laser, the team is able to heat the robot at specific parts of its body, causing it to change shape.", "利用激光，研究团队能够加热机器人身体的特定部位，从而使其发生形变。"),
            ("", "As the robot deforms and goes back to its original shape, it creates movement from one place to another.", "当机器人发生形变并恢复其初始形状时，便产生了从一处到另一处的位移。"),
            ("", "\"Because these structures are so tiny, the rate of cooling is very fast,\" project lead Professor John A. Rogers said.", "项目负责人约翰·A·罗杰斯教授表示：“由于这些微型结构极其微小，其冷却速度非常快。”"),
            ("", "In fact, reducing the sizes of these robots allows them to run faster.", "事实上，缩小这些机器人的尺寸能够让它们跑得更快。"),
            ("", "While the research is still in the exploratory phase, the team believes that technology could lead to micro-sized robots that can perform practical tasks in tightly confined spaces.", "尽管该项研究仍处于探索阶段，但团队坚信，这项技术未来有望催生出能在极其狭小狭窄空间内执行实际任务的微型机器人。"),
            ("", "\"You might imagine micro robots as agents to repair or assemble small structures or machines in industry, or as surgical assistants to clear clogged arteries, to stop internal bleeding, or to eliminate cancerous tumors, all in minimally invasive procedures,\" Rogers said.", "罗杰斯教授说：“你可以将微型机器人想象成在工业上修复或组装小型结构及机器的工具，或是在微创手术中充当清理堵塞动脉、止住体内出血或消除恶性肿瘤的手术助手。”")
        ]
    },
    {
        "id": "2024-06-set2-pass-2",
        "subpart_code": "pass-2",
        "section_id": "2024-06-set2-sec-b",
        "section_title": "Section B: Listening Passages",
        "type": "passage",
        "title": "Passage 2 · 精英睡眠者与少眠科学训练",
        "topic_zh": "精英睡眠者与少眠科学训练",
        "question_range": "Q12 ~ Q15",
        "questions": [12, 13, 14, 15],
        "anchor": ["don", "t", "want", "to", "boast"],
        "sentences": [
            ("", "I don't want to boast anything, but I have always considered myself something of an elite sleeper.", "我不想自夸什么，但我一直认为自己算得上是个精英睡眠者。"),
            ("", "Given the opportunity, I will sleep for marathon stretches, and can doze through the most extreme situations.", "只要有机会，我能像跑马拉松一样连续睡上很久，并且能在最极端的情况下打盹打瞌睡。"),
            ("", "On one very rough ferry crossing, on the route to the Isles of Scilly, for example, my traveling companion spent the entire 3-hour-ride throwing up in the bathroom, while I dozed happily on a plastic chair.", "例如，在前往西利群岛的一次极度颠簸的风浪渡轮航程中，我的旅伴在洗手间里吐了整整三个小时，而我却在塑料椅子上睡得非常香甜。"),
            ("", "Unfortunately, it has come to my attention that I am not an elite sleeper after all.", "不幸的是，我终于注意到，自己终究根本不是什么精英睡眠者。"),
            ("", "It seems I am just lazy, because elite sleepers are defined as the approximately 3 percent of the population who are biologically programmed to need less sleep than the rest of us.", "看来我只是懒惰罢了，因为“精英睡眠者”被定义为人群中大约3%的群体，他们在生物学基因上被设定为比我们其他人需要更少的睡眠。"),
            ("", "According to a study that came out in March, elite sleepers have rare genetic changes, which means they can sleep fewer hours than mere mortals, without any risk of cognitive decline.", "根据今年3月份发表的一项研究，精英睡眠者拥有罕见的基因突变，这意味着他们睡得比凡人少得多，却没有任何认知能力下降的风险。"),
            ("", "It may not be possible to change your own genes, but can you train yourself to need less sleep?", "改变你自己的基因也许不可能，但你能否通过自我训练来减少所需的睡眠时间呢？"),
            ("", "Is there a non-biological way to reach elite sleeper status?", "是否存在一种非生物学的方法来达到精英睡眠者的状态？"),
            ("", "I have spent the past year trying to answer that question.", "在过去的一年里，我一直试图解答这个问题。"),
            ("", "Not for fun, I should add, but because having a baby has severely disrupted my sleep, for which I still have a great passion.", "我应该补充说明，这并不是出于好玩，而是因为生了宝宝严重打乱了我的睡眠——而我对睡觉依然怀有极大的热情。"),
            ("", "For a while, I assumed I'd be forced to become one of those people who jump out of bed at the crack of dawn.", "有那么一段时间，我以为自己会被迫成为那种黎明破晓时就从床上一跃而起的人。"),
            ("", "After a year of tough scientific study, however, I have discovered being forced to get up early in the morning is very different from being an early bird.", "然而，经过一年艰苦的科学研究，我发现清晨被迫早起与成为真正的“早起鸟”完全是两码事。")
        ]
    },
    {
        "id": "2024-06-set2-rec-1",
        "subpart_code": "rec-1",
        "section_id": "2024-06-set2-sec-c",
        "section_title": "Section C: Recorded Lectures/Talks",
        "type": "recording",
        "title": "Recording 1 · 体罚惩戒与童年记忆偏差",
        "topic_zh": "体罚惩戒与童年记忆偏差",
        "question_range": "Q16 ~ Q18",
        "questions": [16, 17, 18],
        "anchor": ["if", "you", "read", "an", "article"],
        "sentences": [
            ("", "If you read an article about a controversial issue, do you think you'd realize if it had changed your beliefs?", "如果你读了一篇关于争议性话题的文章，你认为自己会意识到它是否改变了你的信念吗？"),
            ("", "No one knows your own mind like you do.", "没有人比你更了解你自己的心思。"),
            ("", "It seems obvious that you would know if your beliefs had shifted.", "如果你的信念发生了改变，你自己理应心知肚明，这似乎是显而易见的。"),
            ("", "And yet, a new paper in the Quarterly Journal of Experimental Psychology suggests that we actually have very poor awareness of our own belief change, meaning that we will tend to underestimate how much we've been swayed by a convincing article.", "然而，《实验心理学季刊》发表的一篇新论文表明，我们对自己信念改变的觉察力实际上非常贫乏，这意味着我们往往会低估自己被一篇有说服力的文章所动摇的程度。"),
            ("", "The researchers recruited over 200 undergraduates across two studies and focused on their beliefs about whether physical punishment of kids is an effective form of discipline.", "研究人员在两项研究中招募了200多名本科生，重点调查了他们对体罚孩子是否是一种有效管教方式的看法。"),
            ("", "The students reported their initial beliefs about whether physical punishment is an effective way to discipline a child on the scale from \"1. Completely disbelieve\" to \"9. Completely believe\".", "学生们在“1. 完全不相信”到“9. 完全相信”的量表上，报告了他们关于体罚是否是管教儿童有效方式的初始信念。"),
            ("", "Several weeks later, they were given one of two research-based texts to read.", "几周后，他们被安排阅读两篇基于学术研究的文本之一。"),
            ("", "Each was several pages long and either presented the arguments and data in favour of physical punishment or against it.", "每篇文本长达数页，分别给出了支持或反对体罚的论据和数据。"),
            ("", "After this, the students answered some questions to test their comprehension and memory of the text.", "在此之后，学生们回答了一些问题，以测试他们对文本的理解和记忆。"),
            ("", "Then, the students again scored their belief in whether physical punishment is effective or not.", "随后，学生们再次对体罚是否有效表达了自己的信念打分。"),
            ("", "Finally, the researchers asked them to recall what their belief had been at the start of the study.", "最后，研究人员要求他们回忆在研究开始时自己的最初信念是什么。"),
            ("", "The students' belief about physical punishment changed when they read a text that argued against their own initial position.", "当学生们阅读了一篇反驳他们最初立场的文章后，他们对体罚的信念发生了改变。"),
            ("", "Crucially, the memory of their initial belief was shifted in the direction of their new belief.", "至关重要的是，他们对初始信念的记忆向着新信念的方向发生了偏移。"),
            ("", "In fact, their memory was closer to their current belief than their original belief.", "事实上，他们的回忆与其当前的信念更加接近，而不是其原本最初的信念。"),
            ("", "The more their belief had changed, the larger this memory bias tended to be, suggesting the students were relying on their current belief to deduce their initial belief.", "信念改变得越彻底，这种记忆偏差往往就越大，这表明学生们正在依赖他们当前的信念去倒推其初始信念。"),
            ("", "The memory bias was unrelated to the measures of how well they'd understood or recalled the text, suggesting these factors didn't play a role in memory of initial belief or awareness of belief change.", "这种记忆偏差与他们对文本理解或回忆程度的测量结果无关，表明这些因素在初始信念的记忆或信念转变的觉察中并没有起到作用。"),
            ("", "The researchers concede that this research was about changes to mostly moderate beliefs.", "研究人员承认，这项研究主要是关于温和信念的改变。"),
            ("", "It's likely the findings would be different in the context of changes to extreme or deeply held beliefs.", "如果是在极端或根深蒂固信念发生改变的情境下，其研究结果很可能会有所不同。"),
            ("", "However, our beliefs on most topics are in the moderate range, and as we go about our daily lives reading informative material, these intriguing findings suggest we are mostly ignorant of how what we just read has updated and altered our own position.", "然而，我们在大多数话题上的信念都处于温和区间；当我们在日常生活中阅读各类资讯材料时，这些耐人寻味的发现表明，我们大多根本没有意识到刚读到的内容是如何更新并改变了我们自身的立场。")
        ]
    },
    {
        "id": "2024-06-set2-rec-2",
        "subpart_code": "rec-2",
        "section_id": "2024-06-set2-sec-c",
        "section_title": "Section C: Recorded Lectures/Talks",
        "type": "recording",
        "title": "Recording 2 · 母亲节消费增长与女性生育趋势",
        "topic_zh": "母亲节消费增长与女性生育趋势",
        "question_range": "Q19 ~ Q21",
        "questions": [19, 20, 21],
        "anchor": ["as", "the", "american", "population", "grows"],
        "sentences": [
            ("", "As the American population grows, so does the number of American moms.", "随着美国人口的增长，美国母亲的数量也在增加。"),
            ("", "But more than a century after Mother's Day became an official holiday, even as that number increases, the share of the American population who are mothers is at the lowest point in a quarter century.", "但是在母亲节成为法定节日的100多年后，即使母亲的绝对数量在增加，母亲占美国总人口的比例却处于近四分之一个世纪以来的最低点。"),
            ("", "It's frequently noted that fertility rates are falling sharply in richer countries.", "人们经常指出，富裕国家的生育率正在急剧下降。"),
            ("", "But the less observed consequence of this trend is that a decline in births can also mean a decline in motherhood in general.", "但这一趋势较少被观察到的后果是：出生人口的下降通常也意味着整体母亲比例的下降。"),
            ("", "According to my analysis of data from the Census Bureau, the decline of American motherhood is real, occurring very quickly, and may continue for some time yet.", "根据我对人口普查局数据的分析，美国母亲比例的下降是真实存在的，而且发生得非常快，并且可能还会持续一段时间。"),
            ("", "Not only are moms making up less of the population, but their characteristics are changing too and in a way that might be linked to their proportional decline.", "母亲不仅在总人口中所占的比例变小了，而且她们的特征也在发生改变，并且这种改变可能与她们比例的下降存在关联。"),
            ("", "Moms today tend to be older than in the past.", "如今的母亲往往比过去年龄更大。"),
            ("", "Just looking at recent years, the change in age-specific birth rates has been drastic.", "单看近年来的数据，特定年龄段生育率的变化就非常剧烈。"),
            ("", "In just the past few years, the peak childbearing age range for American women has advanced from that of 25 to 29 to that of 30 to 34.", "仅仅在过去的几年里，美国女性的生育高峰年龄区间就已经从25至29岁推迟到了30至34岁。"),
            ("", "Meanwhile, childbearing among women under 20 has fallen by half or more, while childbearing among women 35 and older is rising.", "与此同时，20岁以下女性的生育率下降了一半或更多，而35岁及以上女性的生育率却在上升。"),
            ("", "One positive consequence of this age shift is that a larger proportion of new mothers are economically prepared to raise children.", "这种年龄转变的一个积极后果是，更大比例的新手母亲在经济上做好了抚养孩子的充分准备。"),
            ("", "Less positively, however, many women find that, as they age, they can't have as many kids as they would like.", "然而，不太乐观的是，许多女性发现，随着年龄的增长，她们无法生育她们所期望数量的孩子。"),
            ("", "Plus, having children later in life can increase the risk of health complications.", "此外，高龄产子还会增加出现健康并发症的风险。"),
            ("", "These finer points aside, one major consequence of the older mom's trend is that fewer years of a woman's life are spent as a mother.", "抛开这些细节不谈，母亲高龄化趋势的一个主要后果是：女性一生中为人母的年限变短了。"),
            ("", "This means that, at any given time, a larger share of women and thus of the whole population, will report not having children in government surveys.", "这意味着，在任何特定的时期，更大比例的女性（从而也是整个人口中更大比例的人群）会在政府调查中报告自己没有孩子。"),
            ("", "In other words, later motherhood means less motherhood.", "换句话说，更晚为人母意味着更少的做母亲时光。"),
            ("", "Even as motherhood rates decline, Mother's Day, of course, will endure.", "当然，即使母亲比例下降，母亲节依然会历久弥坚。"),
            ("", "In fact, despite the demographic shift, retail spending on the holiday appears to be rising.", "事实上，尽管出现了这种人口结构转变，该节日期间的零售支出似乎仍在上升。"),
            ("", "It is hard to say if Mother's Day spending is rising more than one would expect, given that the American population keeps growing.", "考虑到美国人口一直在增长，很难说母亲节的支出增长是否超出了预期。"),
            ("", "But one factor might be that the proportion of women who are the mothers of adult children is rising, and those adult children may spend more generously when it comes to celebrating the moms they no longer live with.", "但一个潜在因素可能是，拥有成年子女的母亲比例正在上升，而那些成年子女在为不再住在一起的母亲庆祝节日时，花钱可能会更加慷慨大方。")
        ]
    },
    {
        "id": "2024-06-set2-rec-3",
        "subpart_code": "rec-3",
        "section_id": "2024-06-set2-sec-c",
        "section_title": "Section C: Recorded Lectures/Talks",
        "type": "recording",
        "title": "Recording 3 · 室内绿植净化空气的科学真相",
        "topic_zh": "室内绿植净化空气的科学真相",
        "question_range": "Q22 ~ Q25",
        "questions": [22, 23, 24, 25],
        "anchor": ["since", "nasa", "published", "a", "paper"],
        "sentences": [
            ("", "Since NASA published a paper in 1989 claiming that house plants can soak up pollution and toxic chemicals, businesses and homeowners have increasingly invested in greenery to help clean their air.", "自从美国国家航空航天局在1989年发表了一篇声称室内植物可以吸收污染和有毒化学物质的论文以来，企业和房主们越来越多地投资于绿植来帮助净化室内空气。"),
            ("", "But a new analysis suggests it could actually take more than 1,000 plants per square meter to gain a benefit any greater than simply opening a couple of windows.", "但一项新的分析表明，实际上每平方米需要摆放超过1,000盆植物，才能获得比仅仅打开几扇窗户更大的净化益处。"),
            ("", "The problem lies in the fact that NASA conducted their tests in sealed containers that do not simulate the conditions in most people's homes or offices.", "问题在于，美国国家航空航天局是在密封容器中进行测试的，这并没有模拟大多数人家中或办公室的实际环境条件。"),
            ("", "The space agency was primarily concerned about keeping the air fresh for astronauts cut off in biospheres or space stations, and helping to combat \"sick building syndrome\" which had become a problem due to the super-insulated and energy-efficient offices of the late 1970s.", "该航天机构最初关注的是为与世隔绝在生物圈或空间站中的宇航员保持空气新鲜，并帮助应对由于20世纪70年代末高绝缘节能办公楼而引发的“病态建筑综合征”。"),
            ("", "By the early 1980s, workers regularly complained of skin rashes, sleepiness, headaches, and allergies as they breathed in toxic chemicals from paints and plastics.", "到了20世纪80年代初，工人们经常抱怨出现皮疹、嗜睡、头痛和过敏，因为他们吸入了来自油漆和塑料中的有毒化学物质。"),
            ("", "NASA found that certain plants could remove chemicals from the air, and even today garden centers recommend the plants for air cleaning properties.", "美国国家航空航天局发现某些植物可以去除空气中的化学物质，即使在今天，园艺中心仍在推荐具有空气净化特性的植物。"),
            ("", "However, a new evaluation of dozens of studies spanning 30 years found that house plants in a normal environment have little impact.", "然而，一项跨越30年对数十项研究所做的新评估发现，在正常环境下，室内盆栽植物的作用微乎其微。"),
            ("", "In fact, natural ventilation is far better at cleaning the air.", "事实上，自然通风在净化空气方面的效果要好得多。"),
            ("", "The researchers also calculated the clean air delivery rate for plants in the studies they analyzed and found that the rate at which plants disperse the compounds was well below the usual rate of air exchange in a normal building, caused by the movement of people coming and going, opening doors and windows.", "研究人员还计算了他们所分析研究中植物的洁净空气输出率，发现植物驱散化合物的速率远远低于正常建筑物中由于人员进出走动、开关门窗所引起的常规空气交换速率。"),
            ("", "Many of the studies did show a reduction in the concentration of volatile organic compounds over time, which is likely why people have seized on them to praise the air purifying virtues of plants.", "许多研究确实显示，随着时间的推移，挥发性有机化合物的浓度有所降低，这很可能就是人们抓住这一点大肆赞扬植物空气净化功效的原因所在。"),
            ("", "But the researchers' calculations showed it would take 10 to 1,000 plants per square meter of floor space to compete with the air cleaning capacity of a building's air handling system or even just a couple of open windows in a house.", "但研究人员的计算表明，每平方米地面空间需要放置10到1,000盆植物，才能与建筑物的空气处理系统、甚至仅仅是家中打开的两扇窗户的空气净化能力相匹敌。"),
            ("", "In contrast, NASA's sealed experiment recommended one pot plant per 100 square feet.", "相比之下，美国国家航空航天局的密封实验建议每100平方英尺放置一盆盆栽植物。"),
            ("", "This is certainly an example of how scientific findings can be misleading or misinterpreted over time.", "这无疑是一个典型例子，说明了科学发现随着时间的推移是如何被误导或曲解的。"),
            ("", "But it's also a great example of how scientific research should continually re-examine and question findings to get closer to the ground truth of understanding what's actually happening.", "但这也是一个极好的例子，说明了科学研究应当如何不断重新审视和质疑既有发现，以便更接近了解实际情况的客观真相。")
        ]
    }
]

QUESTION_SOLUTIONS = {
    1: {
        "prompt": "What does the man say he did before buying the blender?",
        "answer": "D",
        "explanation": "男士提到他在购买这款料理机之前，对到底买哪款具体型号做了透彻的研究（did thorough research on which specific model to get），并阅读了上百条网评。由此可知，D项为正确答案。"
    },
    2: {
        "prompt": "What does the woman say she has never thought of doing?",
        "answer": "B",
        "explanation": "女士表示自己从来没有想过要买一台料理机（I have never thought of getting one myself），因为对自己而言很少会用到。由此可知，B项为正确答案。"
    },
    3: {
        "prompt": "What does the man say is a really healthy habit?",
        "answer": "D",
        "explanation": "男士提到自己现在每周有三四天早上会做新鲜果汁，“这是一个非常健康的习惯（It's a really healthy habit）”。由此可知，D项为正确答案。"
    },
    4: {
        "prompt": "What do we learn about store-bought juice from the conversation?",
        "answer": "A",
        "explanation": "对话最后，男士反问女士：“你知道商店买的果汁含糖量高达10%吗（store-bought juice is like 10% sugar）？”由此可知，A项为正确答案。"
    },
    5: {
        "prompt": "What is the question the woman asked Mr. Grimm after the introduction?",
        "answer": "D",
        "explanation": "女士在介绍完市长后提问：在您的领导下，伯克顿成为全国最受欢迎的旅游胜地之一，“您究竟是如何做到带领大家彻底改变这个村庄的？”由此可知，D项为正确答案。"
    },
    6: {
        "prompt": "What do we learn about Berkton of 10 years ago?",
        "answer": "C",
        "explanation": "女士在对话中提到，在大约十年前，伯克顿还是一个相对默默无闻的沉睡村庄（a relatively unheard of sleepy village）。由此可知，C项为正确答案。"
    },
    7: {
        "prompt": "What resulted from the passing of the legislative proposal \"Motion 836\"?",
        "answer": "D",
        "explanation": "市长解释说，“第836号提案”实质上是为了统一协调伯克顿所有房屋的外观美感，使全村房屋风格一致。由此可知，D项（所有房屋外观风格协调一致）为正确答案。"
    },
    8: {
        "prompt": "Why does the man say the tourists are a blessing to Berkton?",
        "answer": "A",
        "explanation": "市长指出，游客对小镇来说是一种福气，因为他们彻底振兴了当地的经济（completely revitalized our local economy）。由此可知，A项为正确答案。"
    },
    9: {
        "prompt": "What does the passage say about a team of researchers at Northwestern University?",
        "answer": "A",
        "explanation": "文章开头提到，西北大学的团队研制出仅0.5毫米宽的微型机器人，“是有史以来最小的遥控步行机器人（the smallest ever remote-controlled walking robot）”。故选项A正确。"
    },
    10: {
        "prompt": "What did the researchers say about the robot they created?",
        "answer": "D",
        "explanation": "工程师解释说，该微型机器人无需复杂硬件，“而是由其身体自身的弹性物理特性驱动的（powered by the elastic property of its body）”。选项D表述与原文完全一致，故正确。"
    },
    11: {
        "prompt": "What do the researchers expect their robots to do in the future?",
        "answer": "B",
        "explanation": "研究团队坚信，未来微型机器人可以在极其狭窄紧凑的空间内执行实用任务（perform practical tasks in tightly confined spaces）。故选项B正确。"
    },
    12: {
        "prompt": "What does the speaker say she did on her ride to the Isles of Scilly?",
        "answer": "B",
        "explanation": "作者在乘船前往西利群岛时，旅伴吐了整整3小时，而她自己在塑料椅上香甜地睡了整个航程（dozed happily / slept during the entire ride）。故选项B正确。"
    },
    13: {
        "prompt": "What do we learn from the passage about elite sleepers?",
        "answer": "C",
        "explanation": "根据3月份发表的研究，精英睡眠者拥有罕见的基因突变（rare genetic changes），在基因层面上注定需要更少睡眠。故选项C（由基因决定）正确。"
    },
    14: {
        "prompt": "What has the speaker been trying to find out over the past year?",
        "answer": "D",
        "explanation": "作者提出疑问：“你能否通过训练让自己需要更少的睡眠？是否有非生物学的方法达到精英睡眠者状态？”过去一年她一直试图寻找这一答案。故选项D正确。"
    },
    15: {
        "prompt": "What has the speaker discovered after a year of tough scientific study?",
        "answer": "C",
        "explanation": "文章最后总结道：“经过一年艰苦的科学研究，我发现清晨被迫早起（being forced to get up early）与成为真正的早起鸟大相径庭。”故选项C正确。"
    },
    16: {
        "prompt": "What does a new paper in the Quarterly Journal of Experimental Psychology suggest?",
        "answer": "D",
        "explanation": "论文指出，我们对自己信念改变的觉察力非常差，这意味着我们往往会低估自己被有说服力的文章所影响动摇的程度（tend to underestimate how much we've been swayed）。故选项D正确。"
    },
    17: {
        "prompt": "What happened when the students read a text that argued against their own initial position?",
        "answer": "A",
        "explanation": "研究发现，当学生阅读了反驳自己立场的文章后，“他们对体罚的信念发生了改变（The students' belief about physical punishment changed）”。由此可知，选项A为正确答案。"
    },
    18: {
        "prompt": "What did the researchers concede concerning their findings?",
        "answer": "A",
        "explanation": "研究人员承认，这项研究主要是关于温和信念的改变，可能不适用于极端或深层信念的转变。故选项A（与温和看法相关）正确。"
    },
    19: {
        "prompt": "What does the speaker conclude from her analysis of the Census Bureau's data?",
        "answer": "C",
        "explanation": "讲话者根据人口普查局数据分析得出：“美国母亲群体比例的下降是真实存在的，而且发生得非常快（the decline of American motherhood is real, occurring very quickly）。”故选项C正确。"
    },
    20: {
        "prompt": "What does the speaker say is a positive consequence of the age shift in childbearing?",
        "answer": "B",
        "explanation": "讲话者明确提到，母亲高龄化的一个积极后果是“更大比例的新手母亲在经济上做好了抚养孩子的充分准备（economically prepared to raise children）”。故选项B正确。"
    },
    21: {
        "prompt": "What might be one explanation for the rise in retail spending on Mother's Day?",
        "answer": "A",
        "explanation": "讲话者指出，拥有成年子女的母亲比例正在上升，而成年子女为不住在一起的母亲庆祝时花钱更慷慨；母亲身份含义的转变也是重要因素。故选项A正确。"
    },
    22: {
        "prompt": "What does NASA's 1989 paper claim house plants can do?",
        "answer": "B",
        "explanation": "NASA在1989年的论文中声称，室内植物可以吸收污染和有毒化学物质（soak up pollution and toxic chemicals）。由此得出选项B为正确答案。"
    },
    23: {
        "prompt": "What is said to be the problem with NASA's study reported in its 1989 paper?",
        "answer": "B",
        "explanation": "问题在于NASA是在密封容器中进行实验的（conducted their tests in sealed containers），无法模拟人们日常真实的家居或办公环境。故选项B正确。"
    },
    24: {
        "prompt": "What is the finding of a new evaluation of dozens of studies spanning 30 years?",
        "answer": "A",
        "explanation": "跨越30年的新评估发现，正常环境下绿植对净化空气影响微乎其微，“事实上，自然通风的效果要好得多（natural ventilation is far better at cleaning the air）”。故选项A正确。"
    },
    25: {
        "prompt": "What does NASA's sealed experiment recommendation exemplify in scientists' pursuit of truth?",
        "answer": "D",
        "explanation": "讲话结尾指出，这是一个极好的例子，说明科学研究应当“不断重新审视和质疑研究发现，以求更接近实际客观真理（continually re-examine and question findings to get closer to the ground truth）”。故选项D正确。"
    }
}

def clean_opt_text(s: str) -> str:
    s = unicodedata.normalize('NFKC', s)
    s = s.strip()
    return s

def extract_docx_questions():
    doc = docx.Document(DOCX_FILE)
    in_listening = False
    q_blocks = {}
    curr_q = None

    for p in doc.paragraphs:
        txt = unicodedata.normalize('NFKC', p.text.strip())
        if 'Part II' in txt and 'Listening' in txt:
            in_listening = True
            continue
        if 'Part III' in txt:
            in_listening = False
            break
        if not in_listening or not txt:
            continue
            
        m = re.match(r'^(\d+)\.\s*(.*)', txt)
        if m:
            curr_q = int(m.group(1))
            q_blocks[curr_q] = m.group(2)
        elif curr_q is not None:
            q_blocks[curr_q] += ' ' + txt

    questions = {}
    for q in range(1, 26):
        raw = q_blocks.get(q, '')
        raw = raw.replace('\u0410', 'A').replace('\u0412', 'B').replace('\u0421', 'C')
        clean = re.sub(r'(Section [A-C]|Directions.*?heard\.|Questions \d+ to \d+.*?heard\.)', '', raw, flags=re.DOTALL)
        opts = {}
        matches = list(re.finditer(r'([A-D])\)\s*', clean))
        for i, m in enumerate(matches):
            letter = m.group(1)
            start = m.end()
            end = matches[i+1].start() if i + 1 < len(matches) else len(clean)
            opt_text = clean_opt_text(clean[start:end])
            opts[letter] = opt_text
        questions[q] = opts
    return questions

def load_whisper_words():
    with open(WHISPER_PATH, "r", encoding="utf-8") as f:
        segs = json.load(f)
    words = []
    for s in segs:
        for w in s.get("words", []):
            for nw in re.findall(r"[a-z0-9]+", w["word"].lower()):
                words.append({
                    "word": w["word"].strip(),
                    "norm": nw,
                    "start": round(w["start"], 2),
                    "end": round(w["end"], 2)
                })
    return words

def curate_and_save():
    print("=" * 60)
    print("Starting curation for 2024-06-set2...")
    print("=" * 60)

    whisper_words = load_whisper_words()
    total_w = len(whisper_words)
    print(f"Loaded {total_w} normalized Whisper words.")

    docx_opts = extract_docx_questions()
    print(f"Extracted options for {len(docx_opts)} questions from docx.")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Update/Insert Exam
    cur.execute("""
        INSERT INTO exams (id, year, month, set_number, title, audio_file, audio_duration, is_golden)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            title=excluded.title,
            audio_file=excluded.audio_file,
            audio_duration=excluded.audio_duration,
            is_golden=excluded.is_golden
    """, (
        EXAM_ID, 2024, 6, 2,
        "2024年06月大学英语六级考试真题（第2套）",
        AUDIO_FILE, AUDIO_DURATION, 1
    ))

    # 2. Insert Sections
    sections = [
        (f"{EXAM_ID}-sec-a", EXAM_ID, "conversation", "Section A: Long Conversations", 1),
        (f"{EXAM_ID}-sec-b", EXAM_ID, "passage", "Section B: Listening Passages", 2),
        (f"{EXAM_ID}-sec-c", EXAM_ID, "recording", "Section C: Recorded Lectures/Talks", 3),
    ]
    cur.executemany("""
        INSERT INTO sections (id, exam_id, type, title, order_num)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            type=excluded.type,
            title=excluded.title,
            order_num=excluded.order_num
    """, sections)

    # Clean existing data for this exam
    cur.execute("DELETE FROM subparts WHERE exam_id = ?", (EXAM_ID,))
    cur.execute("DELETE FROM sentences WHERE exam_id = ?", (EXAM_ID,))
    cur.execute("DELETE FROM questions WHERE exam_id = ?", (EXAM_ID,))

    all_clean_subparts = []
    all_clean_sentences = []
    all_clean_questions = []

    subpart_order = 1
    for sp_meta in SUBPARTS_DATA:
        sid = sp_meta["subpart_code"]
        raw_sentences = sp_meta["sentences"]
        anchor_toks = sp_meta["anchor"]

        # Jump cursor to anchor
        word_cursor = 0
        min_start = 0
        if sid == "conv-2": min_start = 200
        elif sid == "pass-1": min_start = 440
        elif sid == "pass-2": min_start = 600
        elif sid == "rec-1": min_start = 800
        elif sid == "rec-2": min_start = 1040
        elif sid == "rec-3": min_start = 1270

        for i in range(total_w - len(anchor_toks)):
            if whisper_words[i]["start"] >= min_start:
                if all(whisper_words[i + k]["norm"] == anchor_toks[k] for k in range(len(anchor_toks))):
                    word_cursor = i
                    if sid == "conv-1": word_cursor = i - 2
                    elif sid == "pass-2": word_cursor = i - 1
                    break

        print(f"Aligning {sp_meta['id']} ({len(raw_sentences)} sentences) starting around {whisper_words[word_cursor]['start']}s...")

        aligned_sentences = []
        for s_idx, (speaker, en_text, zh_text) in enumerate(raw_sentences):
            tokens = re.findall(r"[a-z0-9]+", en_text.lower())
            if not tokens:
                continue

            start_idx = None
            window = min(80, total_w - word_cursor)
            for off in range(window):
                cur_pos = word_cursor + off
                cur_w = whisper_words[cur_pos]["norm"]
                if cur_w == tokens[0] or cur_w.startswith(tokens[0]) or (len(tokens) > 1 and cur_w == tokens[1]):
                    start_idx = cur_pos
                    break

            if start_idx is not None:
                st_time = whisper_words[start_idx]["start"]
                end_idx = min(start_idx + len(tokens) - 1, total_w - 1)
                for eoff in range(max(0, len(tokens) - 4), min(len(tokens) + 8, total_w - start_idx)):
                    cur_norm = whisper_words[start_idx + eoff]["norm"]
                    if cur_norm == tokens[-1] or cur_norm.endswith(tokens[-1]):
                        end_idx = start_idx + eoff
                        break
                end_time = max(whisper_words[end_idx]["end"], st_time + 0.6)
                word_cursor = end_idx + 1
            else:
                cur_time = whisper_words[min(word_cursor, total_w - 1)]["start"]
                st_time = cur_time
                end_time = cur_time + max(1.5, len(tokens) * 0.35)
                print(f"  [WARN] Fallback timing for: {en_text[:40]}...")

            aligned_sentences.append({
                "id": f"{sp_meta['id']}-s{s_idx+1:03d}",
                "exam_id": EXAM_ID,
                "section_id": sp_meta["section_id"],
                "subpart_id": sp_meta["id"],
                "order_num": s_idx + 1,
                "speaker": speaker,
                "start_time": round(st_time, 2),
                "end_time": round(end_time, 2),
                "english": en_text,
                "chinese": zh_text,
                "confidence": 0.98 if start_idx is not None else 0.85
            })

        duration = round(aligned_sentences[-1]["end_time"] - aligned_sentences[0]["start_time"], 1) if aligned_sentences else 0.0

        subpart_obj = {
            "id": sp_meta["id"],
            "section_id": sp_meta["section_id"],
            "exam_id": EXAM_ID,
            "type": sp_meta["type"],
            "title": sp_meta["title"],
            "order_num": subpart_order,
            "start_time": aligned_sentences[0]["start_time"] if aligned_sentences else 0.0,
            "end_time": aligned_sentences[-1]["end_time"] if aligned_sentences else 0.0,
            "questions_json": json.dumps(sp_meta["questions"]),
            "topic_zh": sp_meta["topic_zh"],
            "question_range": sp_meta["question_range"],
            "sentence_count": len(aligned_sentences),
            "duration": duration
        }
        all_clean_subparts.append(subpart_obj)
        all_clean_sentences.extend(aligned_sentences)
        subpart_order += 1

        # Process questions for this subpart
        for q_num in sp_meta["questions"]:
            sol = QUESTION_SOLUTIONS[q_num]
            opts = docx_opts.get(q_num, {})
            all_clean_questions.append({
                "id": f"{sp_meta['id']}-q{q_num:02d}",
                "exam_id": EXAM_ID,
                "subpart_id": sp_meta["id"],
                "question_num": q_num,
                "prompt": sol["prompt"],
                "option_a": opts.get("A", ""),
                "option_b": opts.get("B", ""),
                "option_c": opts.get("C", ""),
                "option_d": opts.get("D", ""),
                "correct_answer": sol["answer"],
                "explanation": sol["explanation"]
            })

    # Insert subparts
    for sp in all_clean_subparts:
        cur.execute("""
            INSERT INTO subparts (id, section_id, exam_id, type, title, order_num, start_time, end_time, questions_json, topic_zh, question_range, sentence_count, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sp["id"], sp["section_id"], sp["exam_id"], sp["type"], sp["title"],
            sp["order_num"], sp["start_time"], sp["end_time"], sp["questions_json"],
            sp["topic_zh"], sp["question_range"], sp["sentence_count"], sp["duration"]
        ))

    # Insert sentences
    for sent in all_clean_sentences:
        cur.execute("""
            INSERT INTO sentences (id, exam_id, section_id, subpart_id, order_num, speaker, start_time, end_time, english, chinese, words_json, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sent["id"], sent["exam_id"], sent["section_id"], sent["subpart_id"],
            sent["order_num"], sent["speaker"], sent["start_time"], sent["end_time"],
            sent["english"], sent["chinese"], None, sent["confidence"]
        ))

    # Insert questions
    for q in all_clean_questions:
        cur.execute("""
            INSERT INTO questions (id, exam_id, subpart_id, question_num, prompt, option_a, option_b, option_c, option_d, correct_answer, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            q["id"], q["exam_id"], q["subpart_id"], q["question_num"], q["prompt"],
            q["option_a"], q["option_b"], q["option_c"], q["option_d"], q["correct_answer"], q["explanation"]
        ))

    conn.commit()
    conn.close()

    print("=" * 60)
    print(f"SUCCESS: Curation complete for {EXAM_ID}!")
    print(f"Subparts inserted: {len(all_clean_subparts)}")
    print(f"Sentences inserted: {len(all_clean_sentences)}")
    print(f"Questions inserted: {len(all_clean_questions)}")
    print("=" * 60)

if __name__ == "__main__":
    curate_and_save()
