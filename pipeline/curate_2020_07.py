import json
import re
import sqlite3
from pathlib import Path
import docx

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = Path("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2020年07月CET6题+解+音频")
DOCX_FILE = RAW_DIR / "2020年07月六级真题（全1套）.docx"
PDF_FILE = RAW_DIR / "2020.07英语六级考试全1套解析.pdf"
DB_PATH = BASE_DIR / "data" / "sixsense.db"
WHISPER_PATH = BASE_DIR / "data" / "derived" / "exams" / "2020-07-set1" / "whisper_full.json"

def norm_word(w: str) -> str:
    return re.sub(r"[^\w']+", "", w.lower())

def load_whisper_words():
    with open(WHISPER_PATH, "r", encoding="utf-8") as f:
        segs = json.load(f)
    words = []
    for s in segs:
        for w in s["words"]:
            nw = norm_word(w["word"])
            if nw:
                words.append({
                    "word": w["word"].strip(),
                    "norm": nw,
                    "start": round(w["start"], 2),
                    "end": round(w["end"], 2)
                })
    return words

SUBPARTS_DATA = [
    {
        "id": "2020-07-set1-conv-1",
        "subpart_code": "conv-1",
        "section_id": "2020-07-set1-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 1 · 科技推动体育进步",
        "topic_zh": "科技推动体育进步",
        "question_range": "Q1 ~ Q4",
        "questions": [1, 2, 3, 4],
        "sentences": [
            ("Tonight, we have a very special guest.", "今晚我们有一位特别来宾。"),
            ("Mrs. Anna Sanchez is a three-time Olympic champion and author of the new book To the Edge.", "安娜·桑切斯女士三度获得奥运冠军，新近还写了本书，名叫《挑战极限》。"),
            ("Mrs. Sanchez, thank you for joining us.", "桑切斯女士，感谢参加我们的节目。"),
            ("Thank you for having me.", "感谢你们邀请。"),
            ("Let's start with your book.", "我们先从您的这本书聊起吧。"),
            ("What does the title To the Edge mean?", "《挑战极限》这个书名是什么意思？"),
            ("What are you referring to?", "您指什么？"),
            ("The book is about how science and technology has helped push humans to the edge of their physical abilities.", "这本书是关于科技如何帮助推动人类迫近身体极限的。"),
            ("I argue that in the past 20 years we've had the best athletes the world has ever seen.", "我认为，在过去20年里，我们见证了世界上有史以来最好的运动员。"),
            ("But is this a fair comparison?", "但这是一个公平的比较吗？"),
            ("How do you know how, say, a football player from 50 years ago would compare to one today?", "比如，你怎么知道50年前的一名足球运动员与今天的一名足球运动员相比会如何？"),
            ("Well, you're right that comparison would be perhaps impossible to make.", "嗯，你说得对，这种比较也许是不可能的。"),
            ("But the point is more about our knowledge today of human biochemistry, nutrition, and mechanics.", "但重点更多在于我们今天对人体生物化学、营养学和力学的认识。"),
            ("I believe that while our bodies have not changed in thousands of years, what has changed is the scientific knowledge.", "我相信，尽管几千年来我们的身体并没有发生改变，但发生改变的是科学知识。"),
            ("This has allowed athletes to push the limits of what was previously thought possible.", "这让运动员得以打破以前被认为可能达到的极限。"),
            ("That's interesting.", "这很有趣。"),
            ("Please tell us more about these perceived limits.", "请跟我们多讲讲这些人们曾经认定的极限。"),
            ("The world has seen sports records being broken that could only be broken with the aid of technology, whether this be the speed of a tennis serve or the fastest time in a 100-meter dash or 200-meter swimming race.", "世人见证了只有在科技助力下才能被打破的各项运动纪录，无论是网球发球的速度，还是百米短跑或200米游泳比赛的最快纪录。"),
            ("Is there any concern that technology is giving some athletes an unfair advantage over others?", "是否有人担忧科技正在让部分运动员获得对其他运动员的不公平优势？"),
            ("That is an interesting question and one that has to be considered very carefully.", "这是一个有趣的问题，必须非常谨慎地考虑。"),
            ("Skis, for example, went from being made of wood to a metal alloy, which allows for better control and faster speed.", "例如，滑雪板由木质变成金属合金，这使得操控性更好、速度更快。"),
            ("There is no stopping technological progress.", "技术进步是无法阻挡的。"),
            ("But, as I said, each situation should be considered carefully on a case-by-case basis.", "但是，正如我所说，每种情形都应该慎重考虑，具体问题具体分析。")
        ]
    },
    {
        "id": "2020-07-set1-conv-2",
        "subpart_code": "conv-2",
        "section_id": "2020-07-set1-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 2 · 外贸生意",
        "topic_zh": "外贸生意",
        "question_range": "Q5 ~ Q8",
        "questions": [5, 6, 7, 8],
        "sentences": [
            ("I've worked in international trade all my life.", "我在外贸行业干了一辈子。"),
            ("My father did so too before me.", "在我之前，我父亲也是这样。"),
            ("So I guess you could say it runs in the family.", "所以我觉得你大可说这是代代相传。"),
            ("What products have you worked with?", "你经手过哪些产品？"),
            ("All sorts, really.", "不夸张地说，什么都有。"),
            ("I've imported textiles, machinery, toys, solar panels, all kinds of things.", "这些年来我进口过纺织品、机器、玩具、太阳能电池板，各种各样的东西。"),
            ("Trends and demand come and go.", "趋势和需求变化不断。"),
            ("So one needs to be very flexible to succeed in this industry.", "所以要想在这个行业中取得成功，就必须非常灵活变通。"),
            ("I see.", "我明白。"),
            ("What goods are you trading now?", "那你现在在做什么生意呢？"),
            ("I now import furniture from China into Italy and foods from Italy into China.", "我现在把家具从中国进口到意大利，把食品从意大利进口到中国。"),
            ("I even use the same container.", "我甚至连集装箱都用同一个。"),
            ("That's a very efficient way of doing business.", "这样处理生意的效率很高。"),
            ("The same container?", "同一个集装箱？"),
            ("You mean you have one 40-foot container?", "你是说你有一个40英尺集装箱？"),
            ("Yes, that's right.", "对，没错。"),
            ("I have a warehouse in Genoa in Italy and one in Shanghai.", "我在意大利热那亚有一个仓库，上海也有一个。"),
            ("I source mid-century modern style furniture from various factories in China.", "我从中国的各个工厂搜寻中世纪现代风格家具。"),
            ("They're great value.", "它们很划算。"),
            ("I consolidate them at my warehouse and then ship them to my other warehouse in Italy.", "我把它们全都集中到我的仓库，然后运到我在意大利的另一个仓库。"),
            ("There I do the same thing, except with Italian foods like pasta, cheeses, wines, and chocolates.", "在那边我也是这么做，只不过家具换成了意大利食品，比如意大利面、奶酪、红酒和巧克力。"),
            ("I ship all of these to China in the very same cargo containers I used to bring the furniture.", "我把所有这些都运到中国的仓库，用的还是我用来运家具的货物集装箱。"),
            ("I assume you wholesale both product lines in both countries?", "我猜你的两大产品系列在两个国家都是批发出售的。"),
            ("Absolutely.", "当然了。"),
            ("I have clients and partner networks in both countries.", "我在两个国家都有客户和伙伴关系网。"),
            ("That's the best thing about working in this industry for so long.", "这就是在这个行业干了这么久的最大好处。"),
            ("I've built up quite a network of business acquaintances.", "我积累了不少生意熟人。"),
            ("How many shipments do you do?", "你会运多少批货物？"),
            ("I did 12 last year, 18 this year, and I hope to increase that to about 25 next year.", "我去年运了12批，今年运了18批，希望明年能增到差不多25批。"),
            ("That's counting both routes.", "这是算上来回两条路线的。"),
            ("Demand for authentic Italian food in China is growing rapidly.", "中国对正宗意大利食品的需求正在快速增长。"),
            ("Similarly, sales of affordable yet stylish wooden furniture are also increasing in Italy.", "同样地，价格不算贵但样式雅致的木制家具在意大利也卖得越来越好。"),
            ("Furniture is marginally more profitable, mostly because it enjoys lower customs duties.", "家具盈利稍微多些，主要是因为它享有较低的关税。")
        ]
    },
    {
        "id": "2020-07-set1-pass-1",
        "subpart_code": "pass-1",
        "section_id": "2020-07-set1-sec-b",
        "section_title": "Section B: Listening Passages",
        "type": "passage",
        "title": "Passage 1 · 职场幽默",
        "topic_zh": "职场幽默",
        "question_range": "Q9 ~ Q11",
        "questions": [9, 10, 11],
        "sentences": [
            ("Too many people view their jobs as a five-day prison from which they are paroled every Friday, says Joel Goodman, founder of the Humour Project, a humour consulting group in Saratoga Springs, New York.", "太多人将工作视为五日监禁，每周五被假释出狱。幽默计划（一家位于纽约萨拉托加斯普林斯的幽默咨询集团）的创始人乔尔·古德曼如是说。"),
            ("Humour unlocks the office prison because it lets adults bring some of their childlike spirit to the job.", "幽默打开了办公室这座监狱之门，因为它让成年人将自己孩童般的活力带到工作中。"),
            ("According to Howard Pollio, professor of psychology at the University of Tennessee, Knoxville, an office with humour breaks is an office with satisfied and productive employees.", "田纳西大学诺克斯维尔分校的心理学教授霍华德·波利奥认为，一间能够提供幽默小憩时光的办公室会是一间内部员工心满意足、工作高效的办公室。"),
            ("Pollio conducted a study that proved humour can help workers excel at routine production tasks.", "波利奥开展的一项研究证明，幽默能帮助员工出色地完成日常工作任务。"),
            ("Employees perform better when they have fun.", "当员工们开心时，他们的表现会更好。"),
            ("In large corporations with a hierarchy of power, there is often no outlet for stress.", "在权力等级森严的大公司里，员工往往没有释放压力的出口。"),
            ("Every company needs underground ways of poking fun at the organization, says Lynn M. Mark, a speaker on workplace humour for St. Mary's Health Center in St. Louis.", "每个公司都要有进行自我调侃的私密途径。圣路易斯圣玛丽健康中心的职场幽默演讲者琳恩·N·马克说。"),
            ("Kodak's Rochester, New York branch discovered a way for its 20,000 employees to uncork their bottled-up resentments.", "柯达纽约罗彻斯特分公司为其 2 万名员工找到了一种发泄内心积怨的办法。"),
            ("Their 1,000-square-foot Humour Room features a toy store.", "他们的幽默室占地面积 1000 平方英尺，玩具店是其主要特色。"),
            ("Among the room's many stress-reducing gadgets, the main attraction is a boss doll with detachable arms and legs.", "室内有众多减压小器械，其中最引人注目的是一个胳膊和腿都可以拆卸的老板娃娃。"),
            ("Employees can take the doll apart as long as they put its arms and legs back in place.", "员工们能将该老板娃娃拆解（以泄愤），只要他们之后将其胳膊和腿复位。"),
            ("Sandy Cohen, owner of a graphic print production business, created the Quote Board to document the bizarre phrases people say when under strict deadlines.", "某平面印刷制作公司的老板桑迪·科恩创建了一个引用板，用来记录人们在严苛任务期限下所说的怪诞话语。"),
            ("When you're under stress, you say stupid things, says Cohen.", "压力之下，你会说一些愚蠢的话。科恩说。"),
            ("Now we just look at each other and say, that's one for the Quote Board.", "现在，我们只是互相看着对方说，这话是说给引用板的。")
        ]
    },
    {
        "id": "2020-07-set1-pass-2",
        "subpart_code": "pass-2",
        "section_id": "2020-07-set1-sec-b",
        "section_title": "Section B: Listening Passages",
        "type": "passage",
        "title": "Passage 2 · 肥胖基因",
        "topic_zh": "肥胖基因",
        "question_range": "Q12 ~ Q15",
        "questions": [12, 13, 14, 15],
        "sentences": [
            ("Public interest was aroused by the latest discovery of a changed gene in obese mice.", "最近在肥胖小鼠身上发现的一种变异基因引起了公众关注。"),
            ("The news was made known by Rockefeller University geneticist Jeffrey Friedman.", "该消息由洛克菲勒大学遗传学家杰弗里·弗里德曼公布。"),
            ("The researchers believe this gene influences development of a hormone that tells the organism how fat or full it is.", "研究人员认为，该基因会影响某种能让机体感知自身胖瘦或饱腹程度的激素的分泌。"),
            ("Those with the changed gene may not sense when they have eaten enough or if they have sufficient fatty tissue, and thus can't tell when to stop eating.", "那些发生基因变异的小鼠可能感知不到自己什么时候吃饱或者是否已拥有足够的脂肪组织，因此也就无法判断该什么时候停止进食。"),
            ("The researchers also reported finding a gene nearly identical to the mouse obesity gene in humans.", "研究人员还报告称在人类身上发现了一种与小鼠肥胖基因近乎相同的基因。"),
            ("The operation of this gene in humans has not yet been demonstrated, however.", "然而，该基因在人类体内的运作尚未得到证实。"),
            ("Still, professionals like University of Vermont psychologist Esther Rothblum reacted enthusiastically.", "尽管如此，像佛蒙特大学心理学家埃丝特·罗斯布卢姆这样的专业人士还是作出了热烈反响。"),
            ("This research indicates that people really are born with a tendency to have a certain weight, just as they are to have a particular skin color or height.", "这项研究表明，人们确实生来就有一种达到某种特定体重的倾向，就像他们生来就拥有某种特定的肤色或身高一样。"),
            ("She believes about half of a person's total weight variation can be attributed to genetics, with the rest influenced by environmental factors.", "她认为，一个人总的体重变化中约有一半可归因于遗传，其余则受环境因素影响。"),
            ("A survey by the Center for Disease Control found a dramatic increase in obesity during the late 1980s and 1990s, highlighting the influence of environmental factors such as the abundant provision of rich foods.", "疾病控制中心的一项调查发现，在20世纪80年代末和90年代，肥胖症显著增加，这凸显了环境因素（如大量油腻食物的供应）的影响。"),
            ("The Center for Disease Control has also found that teens are far less physically active today than they were even a decade ago.", "疾病控制中心还发现，如今青少年的体育活动量远低于十年前。"),
            ("Accepting that weight is predetermined can relieve guilt and self-blame.", "接受体重是预先注定的这一事实可以减轻内疚与自责。"),
            ("But people's belief that they cannot control their weight can itself contribute to obesity.", "但人们认为自己无法控制体重的这种信念本身就可能导致肥胖。")
        ]
    },
    {
        "id": "2020-07-set1-rec-1",
        "subpart_code": "rec-1",
        "section_id": "2020-07-set1-sec-c",
        "section_title": "Section C: Recorded Lectures/Talks",
        "type": "recording",
        "title": "Recording 1 · 友谊的魅力及威胁",
        "topic_zh": "友谊的魅力及威胁",
        "question_range": "Q16 ~ Q18",
        "questions": [16, 17, 18],
        "sentences": [
            ("Qualities of a relationship, such as openness, compassion, and mental stimulation are of concern to most of us regardless of sex, but—judging from the questionnaire response—they are more important to women than to men.", "一段关系的品质，诸如坦率、同情、精神激励，对我们大多数人而言都至关重要，无关乎性别。但是，从问卷调查结果来看，女性比男性更看重这些品质。"),
            ("Asked to consider the ingredients of close friendship, women rated these qualities above all others.", "当被要求评估亲密友谊的要素时，女性把这些品质列于其他一切品质之上。"),
            ("Men assigned a lower priority to them in favor of similarity in interests—selected by 77% of men—and responsiveness in a crisis, chosen by 61% of male respondents.", "男性则将这些品质排得较低，他们更看重的是：兴趣相似性（被77%男性受访者选择）以及危机响应力（被61%男性受访者选择）。"),
            ("Mental stimulation, ranked third in popularity by men as well as women, was the only area of overlap.", "精神激励在男性和女性中均排在第三位，是唯一的重合领域。"),
            ("Among men, only 28% named openness as an important quality; caring was picked by just 23%. ", "在男性中，只有28%的人认为坦率是一项重要品质；而关怀仅被23%的人选中。"),
            ("It is evident by their selections that when women speak of close friendships they are referring to emotional factors, while men emphasize the pleasure they find in a friend's company.", "从他们的选择中可以明显看出，当女性谈及亲密友谊时，她们指的是情感因素，而男性则强调在朋友的陪伴中获得的乐趣。"),
            ("That is, when a man speaks of a friend, he is likely to be talking about someone he does things with—a teammate, a fellow hobbyist, a drinking buddy.", "也就是说，当一个男人谈论一个朋友时，他很可能指的是与他一起做事的人——队友、志同道合的爱好者、酒友。"),
            ("These activities are the fabric of the friendship.", "这些活动是友谊的交织纽带。"),
            ("It is a doing relationship in which similarity in interests is the key bond.", "这是一种“共同做事”的关系，其中兴趣的相似性是关键纽带。"),
            ("This factor was a consideration of less than 11% of women.", "只有不到11%的女性考虑了这一因素。"),
            ("Women opt for a warm, emotional atmosphere where communication flows freely; activity is mere background.", "女性偏爱温暖、充满情感的氛围，在这里交流畅通无阻；活动仅仅是背景。"),
            ("Lastly, men, as we have seen, have serious questions about each other's loyalty.", "最后，正如我们所见，男性对彼此的忠诚抱有严重的疑问。"),
            ("Perhaps this is why they placed such strong emphasis on responsiveness in a crisis—someone I can call on for help.", "也许这就是为什么他们如此强调危机响应力——一个我可以求助的人。"),
            ("Women, as their testimonies indicate, are generally more secure with each other and consequently are more likely to treat this issue lightly.", "正如她们的证词所表明的那样，女性彼此之间通常更有安全感，因此更有可能轻描淡写地对待这个问题。"),
            ("In follow-up interviews this was confirmed numerous times as woman after woman indicated that being there when needed was taken for granted.", "在后续采访中，这一点得到了无数次证实，一位又一位女性表示，在需要时给予陪伴被视为理所当然。"),
            ("As for the hazards of friendship, more than a few relationships have been shattered because of cutthroat competition and feelings of betrayal.", "至于友谊的威胁，不少关系因为激烈的竞争和被背叛的感觉而破裂。"),
            ("This applies to both men and women, but unequally.", "这适用于男性和女性，但程度不同。"),
            ("In comparison, nearly twice as many men complained about these issues as women.", "相比之下，抱怨这些问题的男性几乎是女性的两倍。"),
            ("Further, while competition and betrayal are the main thorns to female friendship, men are plagued in almost equal amounts by two additional issues: lack of frankness and a fear of appearing unmanly.", "此外，虽然竞争和背叛是女性友谊的主要刺痛，但男性在几乎同等程度上受到另外两个问题的困扰：缺乏坦率和害怕表现得没有男子气概。"),
            ("Obviously, for a man, a good friendship is hard to find.", "很明显，对男性来说，挚友难寻。")
        ]
    },
    {
        "id": "2020-07-set1-rec-2",
        "subpart_code": "rec-2",
        "section_id": "2020-07-set1-sec-c",
        "section_title": "Section C: Recorded Lectures/Talks",
        "type": "recording",
        "title": "Recording 2 · 规模最大的恐龙化石埋藏地",
        "topic_zh": "规模最大的恐龙化石埋藏地",
        "question_range": "Q19 ~ Q21",
        "questions": [19, 20, 21],
        "sentences": [
            ("The partial skeletons of more than 20 dinosaurs and the scattered bones of about 300 more have been discovered in Utah and Colorado at what is now the Dinosaur National Monument.", "在犹他州和科罗拉多州现在是美国国立恐龙公园的地方，已经发现了20多只恐龙的局部骨架和300多只恐龙的零散骨骼。"),
            ("Many of the best specimens may be seen today at museums of natural history in the larger cities of the United States and Canada.", "其中许多最好的标本如今或许能在美国和加拿大较大城市的自然历史博物馆里看到。"),
            ("This dinosaur pit is the largest and best preserved deposit of dinosaurs known today.", "这个恐龙坑是目前已知规模最大、保存最为完好的恐龙化石埋藏地。"),
            ("Many people get the idea from the mass of bones in the pit wall that some disaster such as a volcanic explosion or a sudden flood killed a whole herd of dinosaurs in this area.", "许多人看到坑壁中的大量骨头会产生一种观点：火山爆发或洪水突发等某种灾害导致了这一地区的整个恐龙群的灭亡。"),
            ("This could have happened, but it probably did not.", "这有可能发生，但很可能没有。"),
            ("The main reasons for thinking otherwise are the scattered bones and the thickness of the deposit.", "否定这种说法的两个主要原因是零散的骨骼和埋藏层的厚度。"),
            ("In other deposits where the animals were thought to have died together, the skeletons were usually complete and often all the bones were in their proper places.", "在人们认为动物集群死亡的其他矿床中，骨骼通常是完整的，并且所有的骨头通常都位于原处。"),
            ("Rounded pieces of fossil bone have been found here.", "这里发现了圆形的恐龙骨骼化石碎片。"),
            ("These fragments got their smooth round shape by rolling along the stream bottom.", "这些碎片通过沿着溪流底部滚动而获得了光滑圆润的形状。"),
            ("In a mass killing, the bones would have been left on the stream or lake bottom together at the same level.", "如果发生集体屠杀，这些骨头会被一同留在河流或湖泊底部的同一层面上。"),
            ("But in this deposit, the bones occur throughout a zone of sandstone about 12 feet thick.", "但在这一埋藏层中，骨骼分布在大约12英尺厚的整个砂岩区域内。"),
            ("The mixture of swamp dwellers and dry land types also seems to indicate that the deposit is a mixture from different places.", "沼泽生物和陆地生物化石的混合似乎也表明该沉积物是来自不同地方的混合物。"),
            ("The pit area is a large dinosaur graveyard, not a place where they died.", "恐龙坑区域是一个大型恐龙墓地，而不是它们的死亡之地。"),
            ("Most of the remains probably floated down an eastward flowing river until they were left on a shallow sandbar.", "大部分遗骸可能是顺着一条向东流动的河流漂浮而下，直到它们被留在一处浅滩沙洲上。"),
            ("Some of them may have come from far away dry land areas to the west.", "其中一些可能来自西部遥远的干旱陆地区域。"),
            ("Perhaps they drowned trying to cross a small stream or were washed away during floods.", "也许它们在试图穿过小溪流时溺水身亡，或者在洪水中被冲走。"),
            ("Some of the swamp dwellers may have got stuck in the very sandbar that became their grave; others may have floated for miles before being stranded.", "一些沼泽居民可能被困在后来成为它们坟墓的沙洲中；其他恐龙可能漂浮了数英里才搁浅。"),
            ("Even today, similar events take place when floods come in the spring.", "即使在今天，当春季洪水来临时，类似的事情也会发生。"),
            ("Sheep, cattle, and deer are often trapped by rising waters and drown.", "绵羊、牛和鹿经常被上涨的河水困住并淹死。"),
            ("Their dead bodies float downstream until the flood recedes and leaves them stranded on a bar or shore, where they lie half buried in the sand until they decay.", "它们的尸体顺流而下，直到洪水退去并将它们搁置在沙洲或岸滩上，半掩在泥沙中直至腐烂。"),
            ("Early travelers on the Missouri River reported that shores and bars were often lined with the decaying bodies of buffalo that had died during spring floods.", "密苏里河的早期旅行者反映，岸滩和沙洲上经常排列着在春季洪水中死去的水牛腐尸。")
        ]
    },
    {
        "id": "2020-07-set1-rec-3",
        "subpart_code": "rec-3",
        "section_id": "2020-07-set1-sec-c",
        "section_title": "Section C: Recorded Lectures/Talks",
        "type": "recording",
        "title": "Recording 3 · 独立自主文化使美国人孤独终老",
        "topic_zh": "独立自主文化使美国人孤独终老",
        "question_range": "Q22 ~ Q25",
        "questions": [22, 23, 24, 25],
        "sentences": [
            ("I would like particularly to talk about the need to develop a new style of aging in our own society.", "我特别想谈一谈在我们社会发展一种新的老去方式的必要性。"),
            ("Young people in this country have been accused of not caring for their parents the way they would have in the old country, and this is true.", "在我们国家，年轻人被指责不会像过去那样关心照料父母，这是事实。"),
            ("But it is also true that old people have been influenced by an American ideal of independence and autonomy.", "但另一个事实是，老年人一直以来都深受独立自主这一美国理想标准的影响。"),
            ("So we live alone, perhaps on the verge of starvation, in time without friends, but we are independent.", "为此，我们独自生活，或濒于饿死，或无友可依，但是我们独立。"),
            ("This standard American style has been forced on every ethnic group, although there are many groups for whom the ideal is not practical.", "这种典型的美国生活方式被强加给了每一个族群，尽管对许多族群来说，这种理想并不现实。"),
            ("It is a poor ideal, and pursuing it does a great deal of harm.", "这是一个糟糕的理想，追求它会带来巨大的伤害。"),
            ("This ideal of independence also contains a tremendous amount of unselfishness.", "这种独立的理想也包含着巨大的无私奉献。"),
            ("In talking to today's young mothers, I have asked them what kind of grandmothers they think they're going to be.", "在与当今年轻母亲的交谈中，我曾问她们认为自己将来会成为怎样的祖母。"),
            ("I hear devoted, loving mothers say that when they are through raising their children, they have no intention of becoming grandmothers.", "我听到全心全意爱孩子的母亲们说，当抚养完自己的孩子后，她们无意成为照顾孙辈的祖母。"),
            ("They are astonished to hear that in most of the world throughout most of its history, families have been three- or four-generation families living under the same roof.", "她们吃惊地得知，在世界上绝大多数地方和绝大多数历史时期，家庭都是三代或四代同堂住在同一个屋檐下的。"),
            ("We have overemphasized the small family unit: father, mother, small children.", "我们过度强调了核心小家庭单元：父亲、母亲和幼子。"),
            ("We think it is wonderful if grandma and grandpa, if they're still alive, can live alone.", "我们甚至认为，如果祖父母还健在，能独自生活真是太棒了。"),
            ("We have reached the point where we think the only thing we can do for our children is to stay out of their way, and the only thing we can do for our daughter-in-law is to see as little of her as possible.", "我们已经到了这样的地步：我们认为我们唯一能为子女做的事就是别碍他们的事，唯一能为儿媳做的事就是尽量少和她照面。"),
            ("Old people's nursing homes, even the best run, are filled with older people who believe the only thing they can do for their children is to look cheerful when they come to visit.", "养老院，即使是管理最好的养老院，也挤满了认为自己唯一能为孩子做的事就是在孩子来探访时表现得开开心心的老年人。"),
            ("So in the end, older people have to devote all their energies to not being a burden.", "因此到头来，老年人不得不竭尽全力让自己别成为累赘。"),
            ("We are beginning to see what a tremendous price we've paid for our emphasis on independence and autonomy.", "我们开始看到，我们为强调独立和自主付出了多么巨大的代价。"),
            ("We've isolated old people, and we've cut off the children from their grandparents.", "我们把老年人隔离开来，把孩子们和祖父母切断开来。"),
            ("One of the reasons we have as bad a generation gap today as we do is that grandparents have stepped out.", "我们今天之所以有如此严重的代沟，原因之一就是祖父母退出了家庭生活。"),
            ("Young people are being deprived of the thing they need most: perspective, to know why their parents behave so peculiarly and why their grandparents say the things they do.", "年轻人被剥夺了他们最需要的东西——客观判断能力，他们无法了解父母行事为何这般独特，祖父母为何说出那样的话。")
        ]
    }
]

def extract_docx_questions():
    doc = docx.Document(DOCX_FILE)
    in_listening = False
    q_blocks = {}
    curr_q = None

    for p in doc.paragraphs:
        txt = p.text.strip()
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
        clean = re.sub(r'(Section [A-C]|Directions.*?heard\.|Questions \d+ to \d+.*?heard\.)', '', raw, flags=re.DOTALL)
        opts = {}
        matches = list(re.finditer(r'([A-D])\)\s*', clean))
        for i, m in enumerate(matches):
            letter = m.group(1)
            start = m.end()
            end = matches[i+1].start() if i + 1 < len(matches) else len(clean)
            opt_text = clean[start:end].strip()
            opts[letter] = opt_text
        questions[q] = opts
    return questions

def extract_pdf_solutions():
    prompts = {
        1: "What do we learn about Anna Sanchez?",
        2: "What is the woman's book mainly about?",
        3: "What has changed in the past thousands of years?",
        4: "What is the man's concern about the use of technology in sports competitions?",
        5: "What does the woman think is required to be successful in international trade?",
        6: "What does the woman say is special about her way of doing business?",
        7: "What does the woman have in both Italy and China?",
        8: "What does the woman say makes furniture marginally more profitable?",
        9: "What does the passage say about humor in the workplace?",
        10: "What does the study by Howard Polio show?",
        11: "What can Kodak's employees do in the humor room?",
        12: "What does the speaker say has aroused public interest?",
        13: "What do we learn about the changed gene?",
        14: "What does University of Vermont psychologist Esther Rothblum say?",
        15: "What accounts for Americans' obesity according to a survey by the Center for Disease Control?",
        16: "What quality do men value most concerning friendship according to a questionnaire response?",
        17: "What do women refer to when speaking of close friendships?",
        18: "What may threaten a friendship for both men and women?",
        19: "Where can many of the best dinosaur specimens be seen today?",
        20: "What occurs to many people when they see the massive bones in the pit wall?",
        21: "What does the speaker suggest about the large number of dinosaur bones in the pit?",
        22: "What ideal influences American aging style?",
        23: "What does the speaker say about old people in the United States?",
        24: "What is astonishing to the young mothers interviewed by the speaker?",
        25: "What does the speaker say older people try their best to do?"
    }

    answers = {
        1: "A", 2: "D", 3: "B", 4: "C",
        5: "B", 6: "D", 7: "A", 8: "C",
        9: "A", 10: "D", 11: "B",
        12: "A", 13: "D", 14: "C", 15: "B",
        16: "A", 17: "D", 18: "C",
        19: "D", 20: "B", 21: "A",
        22: "B", 23: "D", 24: "B", 25: "B"
    }

    explanations = {
        1: "首段男士介绍女士身份：三度获得奥运冠军（three-time Olympic champion），故选 A。",
        2: "女士介绍新书主要观点：科技如何帮助人类挑战身体极限（push humans to the edge of their physical abilities），故选 D。",
        3: "女士指出：几千年来人类身体没有改变，改变的是科学知识（scientific knowledge），故选 B。",
        4: "男士提出担忧：科技是否会给予某些运动员不公平优势（unfair advantage），故选 C。",
        5: "女士谈到外贸行业：趋势与需求变化不断，成功需要非常灵活变通（flexible），故选 B。",
        6: "女士介绍商业模式：往返使用同一个40英尺集装箱进行双向物流，效率极高，故选 D。",
        7: "女士提到：自己在意大利热那亚和中国上海各拥有一个仓库（warehouse），故选 A。",
        8: "女士解释家具盈利稍高原因：享有较低的进口关税（lower customs duties），故选 C。",
        9: "文章首段指出：幽默打破办公室桎梏，帮助员工减轻压力（reduce their stress），故选 A。",
        10: "霍华德·波利奥教授研究表明：幽默能帮助员工出色完成日常工作任务（excel at routine tasks），故选 D。",
        11: "柯达公司幽默室规定：只要员工把胳膊和腿复位，就可以拆解老板娃娃，故选 B。",
        12: "文章开篇指出：在肥胖小鼠身上发现的变异基因（changed gene in obese mice）引起公众关注，故选 A。",
        13: "细节说明：变异小鼠感知不到吃饱或脂肪组织，无法判断何时停止进食（stop eating），故选 D。",
        14: "心理学家指出：人们生来就具有达到某种特定体重的遗传倾向（born with a tendency），故选 C。",
        15: "疾控中心调查指出：除基因外，大量油腻食物的供应（abundant provision of rich foods）等环境因素也是主因，故选 B。",
        16: "问卷显示：77%男性将兴趣相似性（similarity in interests）作为首选要素，故选 A。",
        17: "女性认为：当谈及亲密友谊时，她们主要指的是情感因素（emotional factors），故选 D。",
        18: "文章指出：激烈的竞争和感受到背叛（feelings of betrayal）是危害友谊的主要因素，故选 C。",
        19: "讲话指出：公园出土的许多最好标本如今在美加各大城市的自然历史博物馆展出，故选 D。",
        20: "众人看到大量骨骼往往产生猜想：某些自然灾害（natural disaster）导致了恐龙集体灭绝，故选 B。",
        21: "讲话人指出：大部分恐龙遗骸是随向东流淌的河流漂下并留在浅滩上的，故选 A。",
        22: "讲话指出：美国老年人深受独立与自主（independence and autonomy）的理想标准影响，故选 B。",
        23: "老年人选择独自生活，追求独立与自主的意识，故选 D。",
        24: "年轻母亲震惊于：在人类大部分历史和世界大部分地方，大家庭同堂居住是常态，故选 B。",
        25: "老年人竭尽全力做的事情是：努力不成为子女的负担（avoid being a burden），故选 B。"
    }

    return prompts, answers, explanations

def curate_all():
    whisper_words = load_whisper_words()
    total_w = len(whisper_words)
    docx_questions = extract_docx_questions()
    prompts, answers, explanations = extract_pdf_solutions()

    subpart_anchors = {
        "conv-1": ["tonight", "we", "have"],
        "conv-2": ["worked", "in", "international"],
        "pass-1": ["too", "many", "people"],
        "pass-2": ["public", "interest", "was"],
        "rec-1": ["qualities", "of", "a"],
        "rec-2": ["partial", "skeletons", "of"],
        "rec-3": ["would", "like", "particularly"]
    }

    all_clean_subparts = []
    all_clean_questions = []

    for sp_meta in SUBPARTS_DATA:
        sid = sp_meta["subpart_code"]
        raw_sentences = sp_meta["sentences"]

        # Jump cursor to anchor
        anchor_toks = subpart_anchors[sid]
        for i in range(len(whisper_words) - len(anchor_toks)):
            if all(whisper_words[i + k]["norm"] == anchor_toks[k] for k in range(len(anchor_toks))):
                word_cursor = i
                break

        aligned_sentences = []
        for s_idx, (en_text, zh_text) in enumerate(raw_sentences):
            tokens = [norm_word(w) for w in en_text.split() if norm_word(w)]
            if not tokens:
                continue

            start_idx = None
            window = min(120, total_w - word_cursor)
            for off in range(window):
                cur = word_cursor + off
                if whisper_words[cur]["norm"] == tokens[0]:
                    if len(tokens) > 1 and cur + 1 < total_w:
                        if whisper_words[cur + 1]["norm"] == tokens[1]:
                            start_idx = cur
                            break
                    else:
                        start_idx = cur
                        break

            if start_idx is not None:
                st_time = whisper_words[start_idx]["start"]
                last_tok = tokens[-1]
                end_idx = min(start_idx + len(tokens), total_w - 1)
                for off in range(max(0, len(tokens) - 6), min(len(tokens) + 12, total_w - start_idx)):
                    cur = start_idx + off
                    if cur < total_w and whisper_words[cur]["norm"] == last_tok:
                        end_idx = cur
                        break
                end_time = max(whisper_words[end_idx]["end"], st_time + 0.8)
                word_cursor = end_idx + 1
            else:
                cur_time = whisper_words[min(word_cursor, total_w - 1)]["start"]
                st_time = cur_time
                end_time = cur_time + max(1.5, len(tokens) * 0.35)

            aligned_sentences.append({
                "id": f"{sp_meta['id']}-s{s_idx+1:03d}",
                "order_num": s_idx + 1,
                "speaker": "M" if "conv" in sid and s_idx % 2 == 0 else "W" if "conv" in sid else "",
                "start_time": round(st_time, 2),
                "end_time": round(end_time, 2),
                "english": en_text,
                "chinese": zh_text,
                "confidence": 0.98 if start_idx is not None else 0.85
            })

        duration = round(aligned_sentences[-1]["end_time"] - aligned_sentences[0]["start_time"], 1) if aligned_sentences else 0.0

        subpart_obj = {
            "id": sp_meta["id"],
            "subpart_code": sid,
            "section_id": sp_meta["section_id"],
            "type": sp_meta["type"],
            "title": sp_meta["title"],
            "topic_zh": sp_meta["topic_zh"],
            "question_range": sp_meta["question_range"],
            "order_num": len(all_clean_subparts) + 1,
            "start_time": aligned_sentences[0]["start_time"],
            "end_time": aligned_sentences[-1]["end_time"],
            "duration": duration,
            "sentence_count": len(aligned_sentences),
            "sentences": aligned_sentences
        }
        all_clean_subparts.append(subpart_obj)

        print(f"Subpart {sid} ({sp_meta['title']}): {len(aligned_sentences)} sentences, {subpart_obj['start_time']}s -> {subpart_obj['end_time']}s ({duration}s)")

        for q_num in sp_meta["questions"]:
            opts = docx_questions.get(q_num, {})
            all_clean_questions.append({
                "id": f"2020-07-q{q_num:02d}",
                "exam_id": "2020-07-set1",
                "subpart_id": sp_meta["id"],
                "question_num": q_num,
                "prompt": prompts.get(q_num, f"Question {q_num}"),
                "option_a": opts.get("A", ""),
                "option_b": opts.get("B", ""),
                "option_c": opts.get("C", ""),
                "option_d": opts.get("D", ""),
                "correct_answer": answers.get(q_num, "A"),
                "explanation": explanations.get(q_num, "")
            })

    derived_dir = BASE_DIR / "data" / "derived" / "exams" / "2020-07-set1"
    derived_dir.mkdir(parents=True, exist_ok=True)

    with open(derived_dir / "alignment.json", "w", encoding="utf-8") as f:
        json.dump({
            "exam_id": "2020-07-set1",
            "title": "2020年07月大学英语六级考试真题（全国单套卷）",
            "audio_file": "202007-CET6 听力.mp3",
            "audio_duration": 1611.15,
            "subparts": all_clean_subparts
        }, f, ensure_ascii=False, indent=2)

    with open(derived_dir / "questions.json", "w", encoding="utf-8") as f:
        json.dump(all_clean_questions, f, ensure_ascii=False, indent=2)

    print(f"\nSaved alignment.json & questions.json successfully.")

    # SQLite Database Update
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS questions")
    cur.execute("""
        CREATE TABLE questions (
            id TEXT PRIMARY KEY,
            exam_id TEXT NOT NULL,
            subpart_id TEXT NOT NULL,
            question_num INTEGER NOT NULL,
            prompt TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            explanation TEXT
        )
    """)

    cur.execute("PRAGMA table_info(subparts)")
    cols = [r[1] for r in cur.fetchall()]
    if "topic_zh" not in cols:
        cur.execute("ALTER TABLE subparts ADD COLUMN topic_zh TEXT DEFAULT ''")
    if "question_range" not in cols:
        cur.execute("ALTER TABLE subparts ADD COLUMN question_range TEXT DEFAULT ''")
    if "sentence_count" not in cols:
        cur.execute("ALTER TABLE subparts ADD COLUMN sentence_count INTEGER DEFAULT 0")
    if "duration" not in cols:
        cur.execute("ALTER TABLE subparts ADD COLUMN duration REAL DEFAULT 0.0")

    cur.execute("DELETE FROM subparts WHERE exam_id = '2020-07-set1'")
    for sp in all_clean_subparts:
        cur.execute("""
            INSERT INTO subparts (id, exam_id, section_id, type, title, topic_zh, question_range, order_num, start_time, end_time, sentence_count, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sp["id"], "2020-07-set1", sp["section_id"], sp["type"], sp["title"], sp["topic_zh"], sp["question_range"],
            sp["order_num"], sp["start_time"], sp["end_time"], sp["sentence_count"], sp["duration"]
        ))

    cur.execute("DELETE FROM sentences WHERE exam_id = '2020-07-set1'")
    total_s = 0
    for sp in all_clean_subparts:
        for s in sp["sentences"]:
            cur.execute("""
                INSERT INTO sentences (id, exam_id, section_id, subpart_id, order_num, speaker, start_time, end_time, english, chinese, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                s["id"], "2020-07-set1", sp["section_id"], sp["id"], s["order_num"],
                s["speaker"], s["start_time"], s["end_time"], s["english"], s["chinese"], s["confidence"]
            ))
            total_s += 1

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

    print(f"\nSQLite sixsense.db refreshed with {len(all_clean_subparts)} subparts, {total_s} sentences, {len(all_clean_questions)} questions.")

if __name__ == "__main__":
    curate_all()
