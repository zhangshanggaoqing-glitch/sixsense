#!/usr/bin/env python3
"""
Generate pipeline/data_2018_06_set1.py with 100% golden standard:
- 7 Subparts with authentic titles, Chinese topics, and question ranges
- Complete grammatical sentences with 100% paired authentic Chinese translations
- 25 Official CET-6 questions with full options, verified answers, and detailed explanations
"""

import pprint
from pathlib import Path

EXAM_ID = "2018-06-set1"

SUBPARTS = [
    {
        "id": f"{EXAM_ID}-conv-1",
        "subpart_code": "conv-1",
        "section_id": f"{EXAM_ID}-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 1 · 西班牙凉菜汤与腌火腿：原料构成、口感作用与腌制工艺",
        "topic_zh": "西班牙美食介绍：gazpacho 冷汤原料与夏季清爽缘由、陈面包增稠作用与腌火腿工艺及价格",
        "question_range": "Q1 ~ Q4",
        "questions": [1, 2, 3, 4],
        "sp_start": 0.0,
        "sp_end": 0.0,
        "sentences": [
            ("M", "What's all that? Are you going to make a salad?", "那是什么？你要做沙拉吗？"),
            ("W", "No. I'm going to make a gazpacho.", "不。我要做一道 gazpacho。"),
            ("M", "What's that?", "那是什么？"),
            ("W", "Gazpacho is a cold soup from Spain. It's mostly vegetables. I guess you can call it a liquid salad.",
             "gazpacho 是一种来自西班牙的冷汤，它主要是蔬菜。你也可以叫它液体沙拉。"),
            ("M", "Cold soup? Sounds weird.", "冷汤？听起来怪怪的。"),
            ("W", "It's delicious. Trust me. I tried it for the first time during my summer vacation in Spain. You see, in the south of Spain it gets very hot in the summer, up to 42 degrees Celsius. So a cold gazpacho is very refreshing. The main ingredients are tomato, cucumber, bell peppers, olive oil and stale bread.",
             "很好吃的。相信我。我在西班牙度假的时候第一次吃。你看，在西班牙南部，夏天很热，气温高达 42 摄氏度。所以冷的 gazpacho 非常清爽。它的主要原料是西红柿、黄瓜、柿子椒、橄榄油和陈面包。"),
            ("M", "Stale bread? Surely you mean bread for dipping into the soup?",
             "陈面包？你 Surely 是说用来蘸着吃汤的面包吧？"),
            ("W", "No. Bread is crushed and blended in like everything else. It adds texture and thickness to the soup.",
             "不。面包是像其他所有东西一样被压碎、加入汤中的。它增加了汤的口感和浓度。"),
            ("M", "Mm. And is it healthy?", "嗯。那它健康吗？"),
            ("W", "Sure. As I said earlier, it's mostly vegetables. You can also add different things if you like, such as half-boiled eggs or cured ham.",
             "当然了。就像我刚才所说的，它主要是蔬菜。如果你喜欢的话，也可以加入不同的东西，比如半熟的鸡蛋或腌制火腿。"),
            ("M", "Cured ham? What's that?", "腌制火腿？那是什么？"),
            ("W", "That's another Spanish delicacy. Have you never heard of it? It's quite famous.",
             "那是另一种西班牙美食。你没听说过吗？它很有名的。"),
            ("M", "No. Is it good too?", "没有。这也很好吃吗？"),
            ("W", "Oh, yeah, definitely. It's amazing. It's a little dry and salty, and it's very expensive because it comes from a special type of pig that only eats a special type of food. The ham is covered in salt to dry and preserve it, and left to hang for up to two years. It has a very distinct flavor.",
             "噢，是的，当然。它味道很棒。它有一点干和咸，而且很贵，因为它取自一种特殊品种的猪，这种猪只吃一种特殊的饲料。火腿用盐覆盖以干燥和防腐，然后悬挂长达两年。它有非常独特的味道。"),
            ("M", "Mm. Sounds interesting. Where can I find some?",
             "嗯。听起来很有趣。在哪里能找到呢？"),
            ("W", "It used to be difficult to get Spanish produce here. But it's now a lot more common. Most large supermarket chains have cured ham in little packets, but in Spain you can buy a whole leg.",
             "以前很难在这里买到西班牙产品，但现在常见多了。大多数大型连锁超市都有小包装的腌火腿，但在西班牙你能买到一整条火腿。"),
            ("M", "A whole pig leg? Why would anybody want so much ham?",
             "一整条猪腿？为什么有人要这么多火腿？"),
            ("W", "In Spain, many people buy a whole leg for special group events such as Christmas. They cut it themselves into very thin slices with a long flat knife.",
             "在西班牙，许多人会为圣诞节之类的特殊集体活动买一整条火腿。他们会自己用一把又长又平的刀把它切成很薄的片。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-conv-2",
        "subpart_code": "conv-2",
        "section_id": f"{EXAM_ID}-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 2 · 生日礼物选酒：预算区间、红酒推荐与基安蒂和仙粉黛的对比",
        "topic_zh": "为老板挑选生日葡萄酒：佐餐酒不宜送礼、中档价位三十至六十美元、红酒易配餐及两种意大利红酒比较",
        "question_range": "Q5 ~ Q8",
        "questions": [5, 6, 7, 8],
        "sp_start": 0.0,
        "sp_end": 0.0,
        "sentences": [
            ("M", "Hello, I wish to buy a bottle of wine.", "你好，我想买一瓶葡萄酒。"),
            ("W", "Hi. Yes. What kind of wine would you like?", "你好，是的。您想要哪种葡萄酒？"),
            ("M", "I don't know. Sorry, I don't know much about wine.", "我不知道。抱歉，我对葡萄酒了解不多。"),
            ("W", "That's no problem at all. What's the occasion and how much would you like to spend?",
             "完全不成问题。请问是什么场合，您的预算是多少呢？"),
            ("M", "It's for my boss. It's his birthday. I know he likes wine, but I don't know what type. I also do not want anything too expensive, maybe mid-range. How much would you say is a mid-range bottle of wine approximately?",
             "是送给我的老板，他过生日。我知道他喜欢葡萄酒，但我不知道他喜欢什么类型。我也不想买太贵的，中档的就可以。一瓶中档的葡萄酒大约多少钱？"),
            ("W", "Well, it varies greatly. Our lowest prices are around $6 a bottle, but those are table wines. They are not very special, and I would not suggest them as a gift. On the other hand, our most expensive bottles are over $150. If you are looking for something priced in the middle, I would say anything between $30 and $60 would make a decent gift. How does that sound?",
             "嗯，价格差别很大。我们这里最低的价格大约是每瓶 6 美元，但那些是佐餐酒，并没有什么很特别的，我不建议把它们当作礼物。另一方面，我们这里最贵的酒超过 150 美元。如果您在找中间价位的酒，我觉得 30 到 60 美元的酒用来送人很体面。您觉得可以吗？"),
            ("M", "Mm, yeah. I guess something in the vicinity of 30 or 40 would be good. Which type would you recommend?",
             "嗯，行。我想 30 或 40 美元左右的酒会比较合适。你推荐哪种酒？"),
            ("W", "I would say the safest option is always a red wine. They are generally more popular than whites, and they can usually be paired with food more easily. Our specialty here are Italian wines, and these tend to be fruity with medium acidity. This one here is a Chianti, which is perhaps Italy's most famous type of red wine. Alternatively, you may wish to try and surprise your boss with something less common, such as this Zinfandel. The grapes are originally native to Croatia, but this winery is in eastern Italy and it has a more spicy and peppery flavor. So to summarize, the Chianti is more classical and the Zinfandel more exciting. Both are similarly priced at just under $40.",
             "我想说最保险的选择永远都是红葡萄酒。它整体上比白葡萄酒更受欢迎，也更容易和食物搭配。我们这里的特色是意大利葡萄酒，这些酒果味较浓、酸度中等。这瓶是 Chianti（基安蒂），它可能是意大利最著名的红酒种类。或者，您要是想给老板来个惊喜，可以试试这种没那么常见的，比如这瓶 Zinfandel（仙粉黛）。它所用葡萄原产于克罗地亚，酒庄位于意大利东部，味道更为辛辣，带有较多胡椒味。总而言之，基安蒂更经典，仙粉黛更令人兴奋。两者价格相近，都不到 40 美元。"),
            ("M", "I will go with Chianti then. Thanks.", "那我就选基安蒂了。谢谢。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-pass-1",
        "subpart_code": "pass-1",
        "section_id": f"{EXAM_ID}-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 1 · 纳瓦霍密码通讯员：二战从未被破译的口头密码与最成功战时密码",
        "topic_zh": "二战纳瓦霍口头密码：基于难懂母语与暗语、通讯员的战场作用及战后获得的政府表彰",
        "question_range": "Q9 ~ Q11",
        "questions": [9, 10, 11],
        "sp_start": 0.0,
        "sp_end": 0.0,
        "sentences": [
            ("M", "Many people enjoy secret codes. The harder the code, the more some people will try to figure it out. In wartime, codes are especially important. They help armies send news about battles and the size of enemy forces. Neither side wants its codes broken by the other.",
             "许多人喜欢密码。密码越难，越会有人想要破解它。在战时，密码尤其重要。它们帮助军队传送战斗和敌军规模的相关情报。任何一方都不希望自己的密码遭到另一方破解。"),
            ("M", "One very important code was never broken. It was used during World War II by the Americans. It was a spoken code never written down. And it was developed and used by Navajo Indians. They were called the Navajo code talkers. The Navajos created the code in their own language. Navajo is hard to learn and only a few people know it, so it was pretty certain that the enemy would not be able to understand the code talkers.",
             "有一种极为重要的密码从未被破解。它在二战期间由美国人使用。它是一种从未写下来的口头密码。它由纳瓦霍印第安人发明和使用，而他们就被称为纳瓦霍密码通讯员。纳瓦霍人用他们自己的语言创建了密码。纳瓦霍语很难学，懂的人很少，因此敌人肯定听不懂密码通讯员说的话。"),
            ("M", "In addition, the talkers used code words. They called a submarine an iron fish and a small bomb thrown by hand a potato. If they wanted to spell something, they used code words for letters of the alphabet. For instance, the letter A was ant or apple or ax.",
             "此外，密码通讯员用的是暗语。他们把潜艇叫作铁鱼，把手榴弹叫作土豆。要是他们想拼什么单词，他们会用暗语来表示字母表中的字母。例如，字母 A 就是 ant（蚂蚁）或 apple（苹果）或 ax（斧子）。"),
            ("M", "The code talkers worked mostly in the islands in the Pacific. One or two would be assigned to a group of soldiers. They would send messages by field telephone to the code talker in the next group, and he would relay the information to his commander. The code talkers played an important part in several battles. They helped troops coordinate their movements and attacks. After the war, the U.S. government honored them for what they had accomplished. Theirs was the most successful wartime code ever used.",
             "密码通讯员主要在太平洋岛屿工作。每队士兵配有一到两名密码通讯员。他们通过野战电话给另一队的密码通讯员发送消息，然后再由他把情报转给指挥官。密码通讯员在数场战役中发挥了重要作用，他们帮助部队协调行动和进攻。战后，美国政府对他们的成就进行了表彰。他们的密码是有史以来最成功的战时密码。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-pass-2",
        "subpart_code": "pass-2",
        "section_id": f"{EXAM_ID}-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 2 · 技术冲击高薪岗位：教育医疗被替代、私人护理难取代与经济重组之问",
        "topic_zh": "技术对传统高薪工作的冲击：未来二十年知识密集岗位被替代、难以被智能技术复制的私人护理及经济重组问题",
        "question_range": "Q12 ~ Q15",
        "questions": [12, 13, 14, 15],
        "sp_start": 0.0,
        "sp_end": 0.0,
        "sentences": [
            ("M", "If you are young and thinking about your career, you'll want to know where you can make a living.",
             "如果你还年轻，正在思索自己的职业，那么你会想知道可以在哪里谋生。"),
            ("M", "Well, there's going to be a technological replacement of a lot of knowledge-intensive jobs in the next 20 years, particularly in the two largest sectors of the labor force with professional skills. One is teaching and the other healthcare. You have so many applications and software and platforms that are going to come in and provide information and service in these two fields, which means a lot of healthcare and education sectors will be radically changed and a lot of jobs will be lost.",
             "未来二十年，许多知识密集型工作将被技术所取代，特别是在最大的两个需要专业技能的劳动力行业：一个是教育，另一个是医疗。现在的许多应用、软件和平台都将进入这两个领域，为之提供信息和服务，这意味着许多医疗和教育行业将经历剧烈的变革，许多岗位将消失。"),
            ("M", "Now, where will the new jobs be found? Well, the one sector of the economy that can't be easily duplicated by even smart technologies is the caring sector, the personal care sector. That is, you can't really get a robot to do a great massage or physical therapy, or you can't get the kind of personal attention you need with regard to therapy or any other personal service. There could be very high-end personal services. Therapists do charge a lot of money. I think there's no limit to the amount of personal attention and personal care people would like if they could afford it.",
             "那么，新岗位会在哪里出现呢？有一种经济部门，即便智能技术也不容易复制，那就是护理业——私人护理业。更确切地说，你不可能真正让机器人提供舒适的按摩或理疗，也不可能得到那种你在治疗或其他私人服务中需要的私人关怀。未来可能出现非常高端的私人服务。治疗师收费的确很高。但我认为只要支付得起，人们对私人关怀和私人护理数量的要求是没有上限的。"),
            ("M", "But the real question in the future is how come people afford these things if they don't have money, because they can't get a job that pays enough. That's why I wrote this book which is about how to reorganize the economy for the future, when technology brings about destructive changes to what we used to consider high-income work.",
             "不过，未来真正的问题在于，如果人们因找不到工资足够多的工作而挣不到钱，他们怎样支付得起这些服务。这就是我写这本书的原因，讲的是在技术给我们曾经视作高薪的工作带来毁灭性转变时，我们应如何面向未来重组经济。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-rec-1",
        "subpart_code": "rec-1",
        "section_id": f"{EXAM_ID}-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 1 · 埃及最古老的人工铺就道路：采石场到航道的连接、石锯证据与洪水驳船运输",
        "topic_zh": "四千六百年历史的埃及人工道路考古：连接采石场与水运航道、首现石锯证据及驳船借洪水运石",
        "question_range": "Q16 ~ Q18",
        "questions": [16, 17, 18],
        "sp_start": 0.0,
        "sp_end": 0.0,
        "sentences": [
            ("M", "American researchers have discovered the world's oldest paved road, a 4,600-year-old highway. It linked a stone pit in the Egyptian desert to waterways that carried blocks to monument sites along the Nile. The 8-mile road is at least 500 years older than any previously discovered road. It is the only paved road discovered in ancient Egypt, said geologist Thomas Bown of the United States Geological Survey. He reported the discovery on Friday.",
             "美国研究人员发现了世界上最古老的人工铺就道路，一条 4600 年前修建的公路。它将埃及沙漠中的一个采石场和沿尼罗河运送石块到纪念碑工地的航道连接了起来。这条八英里的路比先前发现的任意一条路都要古老至少五百年。美国地质调查局的地质学家托马斯·鲍恩说，这是古埃及已发现的唯一一条人工铺就的道路。他于周五报告了这一发现。"),
            ("M", "The road probably doesn't rank with the pyramids as a construction feat, but it is a major engineering achievement, said his colleague, geologist James Harrell of the University of Toledo. Not only is the road earlier than we thought possible, we didn't even think they built roads. The researchers also made a discovery in the stone pit at the northern end of the road: the first evidence that the Egyptians used rock saws. This is the oldest example of saws being used for cutting stone, said Bown's colleague James Hoffmeier of Wheaton College in Illinois.",
             "他的同事、托莱多大学的地质学家詹姆斯·哈雷尔说：“这条道路也许无法和金字塔相媲美，算不上建筑成就，但它是一项重大的工程成就。不仅仅是这条道路比我们所想象的要古老，我们甚至都没想到他们修建了道路。”研究人员还在这条道路北部尽头的采石场有所发现：埃及人使用石锯的首个证据。鲍恩的同事、伊利诺伊州惠顿学院的詹姆斯·霍夫迈尔说：“这是人们使用锯来切割石头的最古老的例子。”"),
            ("M", "That's two technologies we didn't know they had, Harrell said. And we don't know why they were both abandoned. The road was discovered in the Faiyum Depression, about 45 miles southwest of Cairo. Short segments of the road had been observed by earlier explorers, Bown said, but they failed to realize its significance or follow up on their observations. Bown and his colleagues stumbled across it while they were doing geological mapping in the region.",
             "哈雷尔说：“这是两项我们不知道他们已拥有的技术。”他还说：“并且我们不知道它们为何都被废弃。”这条道路是在法尤姆洼地中被发现的，位于开罗西南方向大约 45 英里。鲍恩说，早期探险家已观察到了这条路的一小部分，但他们未能意识到其重要性，也未跟进其观察。鲍恩和他的同事在这片区域进行地质填图时偶然发现了这条道路。"),
            ("M", "The road was clearly built to provide services for the newly discovered stone pit. Bown and Harrell have found the camp that housed workers at the stone pit. The road appears today to go nowhere, ending in the middle of the desert. When it was built, its terminal was a dock on the shore of Lake Moeris, which had an elevation of about 66 feet above sea level, the same as the dock. Lake Moeris received its water from the annual floods of the Nile.",
             "这条路显然是为了给新近发现的采石场提供服务而修建的。鲍恩和哈雷尔在采石场发现了供工人居住的营地。今天这条路似乎不知所终，止于沙漠的中间。在其被修建时，它的终点是莫里斯湖岸边的一个码头，莫里斯湖高于海平面约 66 英尺，与码头高度一样。莫里斯湖中的水来自每年尼罗河的洪水。"),
            ("M", "At the time of the floods, the river and lake were at the same level and connected through a gap in the hills near the modern villages of el-Lahun and Hawara. Harrell and Bown believe that blocks were loaded onto barges during the dry season, then floated over to the Nile during the floods to be shipped off to the monument sites at Giza and Saqqara.",
             "在洪水期，尼罗河和莫里斯湖处于同一水平面，通过靠近拉洪和哈瓦拉的现代村庄的山谷内的一个缺口相连。哈雷尔和鲍恩认为，这些石块是在旱季被装入驳船，然后在洪水期漂到尼罗河上，并被运往吉萨和塞卡拉的纪念碑工地。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-rec-2",
        "subpart_code": "rec-2",
        "section_id": f"{EXAM_ID}-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 2 · 中医针灸亲历记：左臂久痛的城市求医路、龚医生扎针与流行背后的机理未明",
        "topic_zh": "针灸疗法的个人体验与观察：常规检查无法诊断而转向针灸、扎针无痛及患者需求推动普及",
        "question_range": "Q19 ~ Q21",
        "questions": [19, 20, 21],
        "sp_start": 0.0,
        "sp_end": 0.0,
        "sentences": [
            ("M", "The thin, extremely sharp needles didn't hurt at all going in. Dr. Gong pierced them into my left arm, around the elbow that had been bothering me. Other needles were slipped into my left wrist and, strangely, into my right arm, and then into both my closed eyelids.",
             "那一根根纤细而又极其尖锐的针扎进去时一点也不疼。龚医生将这些针刺入我的左臂，环绕在困扰我很久的手肘周围。其他一些针插入了我的左手腕，还有很不可思议的地方——我的右臂和我闭着的双眼眼皮。"),
            ("M", "There wasn't any discomfort, just a mild warming sensation. However, I did begin to wonder what had driven me here, to the office of Dr. James Gong in New York's Chinatown. Then I remembered the torturing pain in that left elbow. Several trips to a hospital and two expensive, uncomfortable medical tests had failed to produce even a diagnosis. Maybe you lean on your left arm too much, the doctor concluded, suggesting I see a bone doctor. During the hours spent waiting in vain to see a bone doctor, I decided to take another track and try acupuncture. A Chinese-American friend recommended Dr. Gong. I took the subway to Gong's second-floor office, marked with a hand-painted sign.",
             "没有任何不适，只有轻微的温热感。但是，我确实开始疑惑，是什么让我来到这里，来到詹姆斯·龚医生位于纽约唐人街的办公室。随后我记起来了——是我左手肘那折磨人的疼痛。几趟去医院、两次昂贵而不舒服的医疗检查，甚至连个诊断都做不出来。医生总结道：“也许你靠左臂支撑得过多了”，并建议我去看骨科大夫。在徒劳地等着看骨科医生的时间里，我决定试试另外一条路——针灸。一个美籍华人朋友推荐了龚医生。我坐地铁去了龚医生坐落在二楼、以手绘招牌为标志的办公室。"),
            ("M", "Dr. Gong speaks English, but not often. Most of my questions to him were greeted with a friendly laugh, but I managed to let him know where my arm hurt. He asked me to go into a room, had me lie down on a bed, and went to work. In the next room, I learned, a woman dancer was also getting a treatment. As I lay there a while, I drifted into a dream-like state and fantasized about what she looked like.",
             "龚医生说英语，但不经常说。对我的大多数问题，他都报以友善的一笑，但我设法让他知道我的手臂哪里疼。他让我进了一间屋子，躺在床上，然后开始施治。我得知，在隔壁的房间里，一位女舞者也在接受治疗。我在床上躺了一会儿，就渐渐进入了一种做梦般的状态，幻想着那位女舞者长什么样子。"),
            ("M", "Acupuncturists today are as likely to be found on Park Avenue as on Mott Street. In all there are an estimated 10,000 acupuncturists in the country. Nowadays, a lot of medical doctors have learned acupuncture techniques; so have a number of dentists. Reason? Patient demand. Few, though, can adequately explain how acupuncture works. Acupuncturists may say that the body has more than 800 acupuncture points. A life force called qi circulates through the body. Points on the skin are energetically connected to specific organs, body structures and systems. Acupuncture points are stimulated to balance the circulation of qi. The truth is, though acupuncture is at least 2,200 years old, nobody really knows what's happening, says Paul Zmiewski, a Ph.D. in Chinese studies who practices acupuncture in Philadelphia.",
             "如今，你在派克大街上找到针灸师的概率，跟在唐人街的勿街上找到针灸师的概率没什么两样。据估计，在美国总共有上万名针灸师。如今，许多医疗医生都学了针灸技法，连许多牙医也学了针灸技法。原因是什么？患者需求。不过，几乎没人能充分解释针灸是如何奏效的。针灸师可能会说，人体有不下 800 个穴位，一种被称之为「气」的生命之力在体内循环流通。肌肤上的穴位与特定器官、人体结构和系统相联系，通过刺激穴位来平衡气的循环。真实情况是，尽管针灸至少有 2200 年的历史，「没有人真正知道这到底是怎么一回事」，在费城执业针灸的汉学博士保罗·兹米夫斯基说道。"),
            ("M", "After five treatments, there has been dramatic improvement in my arm, and the pain is a fraction of what it was. The mainly silent Dr. Gong finally even offered a diagnosis for what troubled me. Pinched nerve, he said.",
             "经过五次治疗之后，我的手臂有了明显的改善，疼痛只剩下原来的一点点了。大多沉默不语的龚医生最后甚至还对我的病症给出了诊断。他说：「是神经受到压迫。」"),
        ],
    },
    {
        "id": f"{EXAM_ID}-rec-3",
        "subpart_code": "rec-3",
        "section_id": f"{EXAM_ID}-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 3 · 出生排行对婚配的影响：独生子女难付出、长子女强势与各排行最佳配偶搭配",
        "topic_zh": "出生次序与婚姻匹配研究：长子女、么子女、中间孩与独生子女的性格特点及其最佳与最差婚配",
        "question_range": "Q22 ~ Q25",
        "questions": [22, 23, 24, 25],
        "sp_start": 0.0,
        "sp_end": 0.0,
        "sentences": [
            ("M", "Ronald and Lois, married for two decades, consider themselves a happy couple. But in the early years of their marriage, both were disturbed by persistent arguments that seem to fade away without ever being truly resolved. They uncovered clues to what was going wrong by researching a fascinating subject: how birth order affects not only your personality, but also how compatible you are with your mate.",
             "结婚二十年的罗纳德和罗伊斯夫妇认为自己是幸福的一对。但在早期婚姻生活中，两人都被持续反复的争执所困扰，这些争执虽然似乎已慢慢消失，却从未真正得到解决。他们通过研究一个极具吸引力的课题发现了两人之间出问题的线索，这个课题是：出生次序如何不但影响你的性格，还影响你与配偶的匹配程度。"),
            ("M", "Ronald and Lois are only children, and onlies grow up accustomed to being the apple of their parents' eyes. Match two onlies and you have partners who subconsciously expect each other to continue fulfilling this expectation, while neither has much experience in the giving end.",
             "罗纳德和罗伊斯都是独生子女，独生子女在成长过程中已经习惯被父母视为珍宝。如果两个独生子女结婚，两人潜意识里都希望对方继续满足这一期待，而都没有多少作为「付出」一方的经验。"),
            ("M", "Here's a list of common birth-order characteristics, and some thoughts on the best and worst marital matches for each. The oldest tends to be self-assured, responsible, a high achiever and relatively serious and reserved. He may be slow to make friends, perhaps content with only one companion. The best matches are with a youngest, an only, or a mate raised in a large family. The worst match is with another oldest, since the two will be too sovereign to share a household comfortably.",
             "下面是不同出生次序对应的一些常见性格特征，以及关于各自最佳和最差婚配的一些想法。长子女往往自信、有责任感，是成就很高的人，并且相对严谨和保守。他可能不会轻易结交朋友，或许满足于只有一个同伴。最佳婚配对象是么子女、独生子女或在大家庭中长大的配偶。最差婚配对象是另一个长子女，因为两人都过于强势，无法在同一屋檐下舒适共处。"),
            ("M", "The youngest child of the family thrives on attention and tends to be outgoing, optimistic, creative and less ambitious than others in the family. He may lack self-discipline and have difficulty making decisions on his own. A youngest brother of brothers, often unpredictable and romantic, will match best with an oldest sister of brothers. The youngest sister of brothers is best matched with an oldest brother of sisters, who will happily indulge these traits.",
             "家中的么子女在关注中长大，往往是外向、有冒险精神、乐观、有创造力的，不如家中其他人那么雄心勃勃。他可能缺乏自律精神，难以自主做决定。兄弟中最小的一位往往善变且浪漫，与有若干弟弟的长姐最配。有若干哥哥的么妹和有若干妹妹的长兄最配，后者会很乐意纵容前者的这些特点。"),
            ("M", "The middle child is influenced by many variables; however, middles are less likely to take initiative and more anxious and self-critical than others. Middles often successfully marry other middles, since both are strong on tact, not so strong on the aggressiveness and tend to crave affection.",
             "排行中间的孩子受许多变量的影响；但是，他们不像其他人那样倾向于采取主动，而是更为焦虑，比别人更多地自我批判。中间孩往往相互匹配、成功结合，因为双方都机敏过人，攻击性不强，且都倾向于渴求感情。"),
            ("M", "The only child is often most comfortable when alone. But since an only tends to be a well-adjusted individual, she'll eventually learn to relate to any chosen spouse. The male only child expects his wife to make life easier without getting much in return. He is sometimes best matched with a younger sister of brothers. The female only child, who tends to be slightly more flexible, is well matched with an older man, who will indulge her tendency to test his love. Her worst match? Another only, of course.",
             "独生子女通常在独处时最自在，但因为独生子女往往是一个适应性强的人，她最终会学着与所选择的任何一位配偶相处。男性独生子女盼望妻子改善他的生活而不向他索取太多回报，他有时与有若干哥哥的妹妹最配。独生子女中的女性往往稍微灵活一些，与较年长的男子相配，这样的男子会纵容她常常测试他的爱。她的最差婚配对象呢？当然就是另一个独生子女了。"),
        ],
    },
]

QUESTIONS = {
    1: {
        "prompt": "What do we learn about gazpacho?",
        "options": {
            "A": "It is a typical salad.",
            "B": "It is a Spanish soup.",
            "C": "It is a weird vegetable.",
            "D": "It is a kind of spicy food.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为文章开头处兼新事物引出处。女士说：“Gazpacho is a cold soup from Spain.”与 B) 同义改写。因此答案为 B)。A) 源自开篇男士问话中的 salad，但女士随即回答 No, I'm going to make a gazpacho，下文虽提到可看作「液体沙拉」，那只是为便于男士理解，不可等同于沙拉；C) 将 vegetables 与 weird 杂糅，vegetables 是主要原料，weird 是男士的主观评价；D) 根据 bell peppers 臆测其辛辣，文中并未提到该信息。",
    },
    2: {
        "prompt": "For what purpose is stale bread mixed into gazpacho?",
        "options": {
            "A": "To make it thicker.",
            "B": "To make it more nutritious.",
            "C": "To add to its appeal.",
            "D": "To replace an ingredient.",
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。设题要点为疑问句提示重点信息处。女士说：“Bread is crushed and blended in like everything else. It adds texture and thickness to the soup.”其中 thickness 即「浓度」，A) 为其同义改写。因此答案为 A)。B)、C)、D) 均属于对题干的主观臆测，文中并未涉及这三项内容。",
    },
    3: {
        "prompt": "Why does the woman think gazpacho is healthy?",
        "options": {
            "A": "It contains very little fat.",
            "B": "It uses olive oil in cooking.",
            "C": "It uses no artificial additives.",
            "D": "It is mainly made of vegetables.",
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。设题要点为疑问句提示重点信息处。男士问及 gazpacho 是否健康，女士明确回答 “Sure. As I said earlier, it's mostly vegetables.”，即其有益健康主要由于食材为蔬菜。因此答案为 D)。A) 由「主要原料为蔬菜」臆测出脂肪含量少，文中并未提及；B) 利用主要原料之一的 olive oil 干扰，文中并未说明其健康作用来自橄榄油；C) 的「人造添加剂」在文中并未提及。",
    },
    4: {
        "prompt": "What does the woman say about cured ham?",
        "options": {
            "A": "It does not go stale for two years.",
            "B": "It takes no special skill to prepare.",
            "C": "It comes from a special kind of pig.",
            "D": "It is a delicacy blended with bread.",
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。设题要点为疑问句提示重点信息处。女士说：“it's very expensive because it comes from a special type of pig that only eats a special type of food.”C) 原义复现这一信息。因此答案为 C)。A) 源自 left to hang for up to two years，但文中指的是制作时需要悬挂两年，其保质时长并未提及；B) 反向篡改原文，制作工艺涉及盐腌、风干与悬挂两年，并不需要特殊技巧之说并不成立；D) 将与面包相混合的 gazpacho 篡改为腌制火腿。",
    },
    5: {
        "prompt": "What does the woman think of table wines?",
        "options": {
            "A": "They come in a great variety.",
            "B": "They do not make decent gifts.",
            "C": "They do not vary much in price.",
            "D": "They go well with Italian food.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为语义转折处。女士说：“our lowest prices are around $6 a bottle, but those are table wines. They are not very special, and I would not suggest them as a gift.”them 指代 table wines，B) 是对其看法（不宜作礼物）的正确概括与推理。因此答案为 B)。A) 将 it varies greatly 所指的「葡萄酒价格多样」错改为「佐餐酒种类多样」；C)、D) 均属对价格差异与配餐建议的曲解，与「佐餐酒是否宜作礼物」无关。",
    },
    6: {
        "prompt": "What is the price range of wine the man will consider?",
        "options": {
            "A": "$30-$40.",
            "B": "$40-$50.",
            "C": "$50-$60.",
            "D": "Around $150.",
        },
        "answer": "A",
        "explanation": "【精析】细节推断题。设题要点为人物观点信息。男士说：“I guess something in the vicinity of 30 or 40 would be good.”A) 是对其同义改写。因此答案为 A)。B)、C) 属张冠李戴——原文女士推荐的中档价位是 30 至 60 美元，但男士将愿意接受的价位进一步缩小到 30 至 40 美元；D) 属于女士提到的高档价位（150 美元以上），并非男士愿意考虑的价位。",
    },
    7: {
        "prompt": "Why does the woman recommend red wines?",
        "options": {
            "A": "They are a healthy choice for elderly people.",
            "B": "They are especially popular among Italians.",
            "C": "They symbolize good health and longevity.",
            "D": "They go well with different kinds of food.",
        },
        "answer": "D",
        "explanation": "【精析】细节推断题。设题要点为最高级表达处兼对比处。女士说：“the safest option is always a red wine. They are generally more popular than whites, and they can usually be paired with food more easily.”D) 是题干与选项合并信息对这一建议的同义转述。因此答案为 D)。A)、C) 利用原文未提及的常识「红酒有利于健康」捏造干扰；B) 将 more popular 与 Italian 等个别词汇杂糅曲解为「红酒很受意大利人欢迎」，原文本意为「红酒比白葡萄酒更受欢迎，意大利红酒是店内特色」。",
    },
    8: {
        "prompt": "What do we learn about the wine the man finally bought?",
        "options": {
            "A": "It is a wine imported from California.",
            "B": "It is less spicy than all other red wines.",
            "C": "It is far more expensive than he expected.",
            "D": "It is Italy's most famous type of red wine.",
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。设题要点为事物对比处兼最高级表达处。对话末尾男士说 “I will go with Chianti”，即选择了基安蒂；女士介绍它时说过 “a Chianti, which is perhaps Italy's most famous type of red wine.”因此答案为 D)。A) 将原文的 Croatia（葡萄原产地）混淆为读音相近的 California，且原产的是葡萄而非红酒；B) 将「仙粉黛比基安蒂更辛辣」的二者比较，误解为「在所有红酒中基安蒂更淡」；C) 与原文「男士期望 30 至 40 美元、基安蒂低于 40 美元（即符合其预期）」相悖。",
    },
    9: {
        "prompt": "What does the speaker say many people enjoy doing?",
        "options": {
            "A": "Learning others' secrets.",
            "B": "Searching for information.",
            "C": "Decoding secret messages.",
            "D": "Spreading sensational news.",
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。设题要点为文章开头处兼特殊句式处。首段说：“Many people enjoy secret codes. The harder the code, the more some people will try to figure it out.”it 即指 the code，C) 的 Decoding secret messages 与之对应。因此答案为 C)。A) 中 secrets 源自首句 secret codes，但该短语表示「密码」而非「秘密」；B)、D) 中的 information 与 news 复现首段末 news 一词，但原文此处指「密码在战时发送情报的作用」，而非「人们的爱好」。",
    },
    10: {
        "prompt": "What do we learn about Navajo code talkers?",
        "options": {
            "A": "They helped the U.S. army in World War II.",
            "B": "They could write down spoken codes promptly.",
            "C": "They were assigned to decode enemy messages.",
            "D": "They were good at breaking enemy secret codes.",
        },
        "answer": "A",
        "explanation": "【精析】细节推断题。设题要点为新话题引出处与评价处。第二段提到该密码 was used during World War II by the Americans，末段又提到 “The code talkers played an important part in several battles. They helped troops coordinate their movements and attacks.”，可知他们在二战中帮助了美军。因此答案为 A)。B) 与「It was a spoken code never written down」直接相悖；C)、D) 干扰方式相似，均将通讯员的工作「协调己方部队的行动和进攻」篡改为「破解敌方讯息」。",
    },
    11: {
        "prompt": "What is the speaker mainly talking about?",
        "options": {
            "A": "Important battles fought in the Pacific War.",
            "B": "Decoding of secret messages in war times.",
            "C": "A military code that was never broken.",
            "D": "Navajo Indians' contribution to code breaking.",
        },
        "answer": "C",
        "explanation": "【精析】主旨归纳题。解题信息位于新话题开启处与文章收尾处。文章既抓住「纳瓦霍密码的发明和使用」，又高度概括核心信息「从未被破解」（never broken / the most successful wartime code ever used）。因此答案为 C)。A) 源自末段 the islands in the Pacific、several battles；B) 源自第二段 army...codes broken 的改写，但两项均不足以概括全文；D) 虽复现关键词 Navajo Indians，但原文用 the most successful wartime code 强调的是「因从未被破解而成为最成功的战时密码」，而非「对密码破解的贡献」。",
    },
    12: {
        "prompt": "What does the speaker say will happen in the next 20 years?",
        "options": {
            "A": "All services will be personalized.",
            "B": "A lot of knowledge-intensive jobs will be replaced.",
            "C": "Technology will revolutionize all sectors of industry.",
            "D": "More information will be available.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为预测未来现象处。第二段说：“there's going to be a technological replacement of a lot of knowledge-intensive jobs in the next 20 years.”B) 中 a lot of knowledge-intensive jobs 与 will be replaced 对应 replacement。因此答案为 B)。A) 由「私人护理难以被取代」臆断出「所有服务都会被私人化」；C) 将「教育和医疗许多部门会经历变革」扩大为「所有行业」；D) 由「许多应用与平台进入教育和医疗行业提供信息和服务」臆断出「可供使用的信息会增多」。",
    },
    13: {
        "prompt": "Where will young people have more chances to find jobs?",
        "options": {
            "A": "In the robotics industry.",
            "B": "In the information service.",
            "C": "In the personal care sector.",
            "D": "In high-end manufacturing.",
        },
        "answer": "C",
        "explanation": "【精析】细节推断题。设题要点为设问—回答处。第三段开头先设问 “where will the new jobs be found”，继而指出「私人护理业即便智能技术也难以复制」，暗示在该行业找到工作的几率更大。因此答案为 C)。A) 由细节 a robot 捏造，该处是以「机器人难以提供优质服务」说明私人护理业难以被取代，并未谈及机器人行业；B) 由 information and service 捏造，该处描述的是技术对教育医疗的变革作用；D) 利用 high-end services 捏造出「高端制造业」，本文出现的是高端私人服务。",
    },
    14: {
        "prompt": "What does the speaker say about therapists?",
        "options": {
            "A": "They charge high prices.",
            "B": "They need lots of training.",
            "C": "They cater to the needs of young people.",
            "D": "They focus on customers' specific needs.",
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。设题要点为事实信息强调处。第三段说：“Therapists do charge a lot of money.”其中 charge 复现原词，high prices 同义替换 a lot of money。因此答案为 A)。B) 将「教育与医疗从业者需要专业技能」偷换成治疗师必备的素质；C) 由演讲受众「年轻人」捏造，文中并未谈及治疗师迎合年轻人需求；D) 由顾客客观需求「从治疗中得到关怀」过度推理出治疗师的主观态度，原文并未明确提及。",
    },
    15: {
        "prompt": "What is the speaker's book about?",
        "options": {
            "A": "The rising demand in education and healthcare in the next 20 years.",
            "B": "The disruption caused by technology in traditionally well-paid jobs.",
            "C": "The tremendous changes new technology will bring to people's lives.",
            "D": "The amazing amount of personal attention people would like to have.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为定语从句解释说明处。末段说：“I wrote this book which is about how to reorganize the economy for the future, when technology brings about destructive changes to what we used to consider high-income work.”disruption 对应 destructive changes，traditionally well-paid jobs 同义替换 what we used to consider high-income work。因此答案为 B)。A) 由分析对象「教育业和医疗业」捏造出「需求增长」；C) 将「技术冲击传统高薪岗位」的影响对象改为「日常生活」；D) 将次要细节「人们对关怀的需求很高」当成作者关注重点，由 But the real question is... 可知其后的内容才是重点。",
    },
    16: {
        "prompt": "What do we learn from the lecture about the world's oldest paved road in Egypt?",
        "options": {
            "A": "It was the longest road in ancient Egypt.",
            "B": "It was constructed some 500 years ago.",
            "C": "It lay 8 miles from the monument sites.",
            "D": "It linked a stone pit to some waterways.",
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。设题要点为首段对该道路的描述。首段说：“It linked a stone pit in the Egyptian desert to waterways that carried blocks to monument sites along the Nile.”与 D) 直接对应。因此答案为 D)。A) 与文中「唯一一条已发现的人工铺就道路」相悖；B) 将「比先前发现的道路早至少五百年」与「已有 4600 年历史」杂糅得出；C) 由 8-mile 与 monument sites 杂糅而来，原文为「这条路长 8 英里」。",
    },
    17: {
        "prompt": "What did the researchers discover in the stone pit?",
        "options": {
            "A": "Saws used for cutting stone.",
            "B": "Traces left by early explorers.",
            "C": "An ancient geographical map.",
            "D": "Some stone tool segments.",
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。设题要点为并列处与新发现引出处。第二段说：“The researchers also made a discovery in the stone pit... the first evidence that the Egyptians used rock saws. This is the oldest example of saws being used for cutting stone.”与 A) 复现。因此答案为 A)。B) 由「早期探险家已观察到这条路的一小部分」臆断；C) 由研究人员进行地质填图时发现道路，臆断出「发现了一张古老的地理图」；D) 将原文 stone 与 segments 杂糅，segments 指的是「路段」，并非石器片段。",
    },
    18: {
        "prompt": "For what purpose was the paved road built?",
        "options": {
            "A": "To transport stones to block floods.",
            "B": "To provide services for the stone pit.",
            "C": "To link the various monument sites.",
            "D": "To connect the villages along the Nile.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为强调处 clearly。末段说：“The road was clearly built to provide services for the newly discovered stone pit.”与 B) 复现。因此答案为 B)。A) 将 blocks 误解为动作用途，原文意在说明「载有石块的驳船借洪水漂到尼罗河上」，而非「用石块拦截洪水」；C)、D) 将 monument sites、villages、the Nile 与 linked 杂糅，目的是采石场与码头，而非金字塔工地或尼罗河沿岸村庄。",
    },
    19: {
        "prompt": "What does the speaker find especially strange?",
        "options": {
            "A": "Dr. Gong didn't give him any conventional tests.",
            "B": "Dr. Gong marked his office with a hand-painted sign.",
            "C": "Dr. Gong didn't ask him any questions about his pain.",
            "D": "Dr. Gong slipped in needles where he felt no pain.",
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。设题要点为异乎寻常情况的提示词 strangely。首段说：“Other needles were slipped into my left wrist and, strangely, into my right arm, and then into both my closed eyelids.”即在没有疼痛感的地方扎针，发言者对此感到不可思议。因此答案为 D)。A)、C) 涉及问诊与检查，但并非发言者觉得「特别不可思议」之处；B) 复现 hand-painted sign，但这一细节并不与 strangely 对应。",
    },
    20: {
        "prompt": "Why did the speaker go see Dr. Gong?",
        "options": {
            "A": "He had heard of the wonders acupuncture could work.",
            "B": "Dr. Gong was very famous in New York's Chinatown.",
            "C": "Previous medical treatments failed to relieve his pain.",
            "D": "He found the expensive medical tests unaffordable.",
        },
        "answer": "C",
        "explanation": "【精析】细节概括题。设题要点为原因引出处。第二段说：“Several trips to a hospital and two expensive, uncomfortable medical tests had failed to produce even a diagnosis.”即此前的治疗甚至连诊断都无法做出，未能缓解其病痛，因此转向针灸。因此答案为 C)。A) 借开篇 wonder 一词干扰，但该词为动词，意为「想知道」；B) 由「一位华人朋友推荐龚医生」过度推断，并不意味着他在整个唐人街名气很大；D) 与原文「检查昂贵而不舒服」相悖，文中并未说付不起。",
    },
    21: {
        "prompt": "What accounts for the growing popularity of acupuncture in the United States, according to the speaker?",
        "options": {
            "A": "More and more patients ask for the treatment.",
            "B": "Acupuncture techniques have been perfected.",
            "C": "It doesn't need the conventional medical tests.",
            "D": "It does not have any negative side effects.",
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。设题要点为原因引出处。第四段说：“Nowadays, a lot of medical doctors have learned acupuncture techniques; so have a number of dentists. Reason? Patient demand.”A) 与 patient demand 构成同义改写。因此答案为 A)。B) 由医生纷纷学习针灸技法臆测「针灸技术已完善」，且与「几乎无人能充分揭示针灸如何奏效、没人真正知道这到底是怎么一回事」相悖；C) 在龚医生的治疗流程与「不需要医疗检查」之间强加因果；D) 表述过于绝对，且「针灸副作用」文中并未提及。",
    },
    22: {
        "prompt": "What does the speaker say about Ronald and Lois's early years of married life?",
        "options": {
            "A": "They were on the verge of breaking up.",
            "B": "They were compatible despite differences.",
            "C": "They quarreled a lot and never resolved their arguments.",
            "D": "They argued persistently about whether to have children.",
        },
        "answer": "C",
        "explanation": "【精析】细节概括题。设题要点为用于引出话题的事例处。首段说：“in the early years of their marriage, both were disturbed by persistent arguments that seem to fade away without ever being truly resolved.”quarreled a lot 对应 persistent arguments，never resolved 与 without ever being truly resolved 同义。因此答案为 C)。A) 由 persistent arguments 与 without ever being truly resolved 过度引申出濒临分手，夸大了矛盾；B) 概括的是这对夫妇迄今二十年的婚姻生活（以前争吵不断、现在相处融洽），与题干所问「早期」不符；D) 中 children 在文中指代的是夫妇二人，原文并未提及有关孕育下一代的内容。",
    },
    23: {
        "prompt": "What do we learn about Ronald and Lois?",
        "options": {
            "A": "Neither of them has any brothers or sisters.",
            "B": "Neither of them won their parents' favor.",
            "C": "They weren't spoiled in their childhood.",
            "D": "They didn't like to be the apple of their parents' eyes.",
        },
        "answer": "A",
        "explanation": "【精析】细节推断题。设题要点为用于引出话题的事例处。第二段说：“Ronald and Lois are only children.”A) 虽未直接复现原文，但实际是对 only children 的解释说明。因此答案为 A)。B)、C) 均与「他们被父母视为珍宝（the apple of their parents' eyes）」相悖；D) 与 expect each other to continue fulfilling this expectation（他们期待配偶继续像父母般珍视宠爱他们）含义相悖。",
    },
    24: {
        "prompt": "What does the speaker say about the oldest child in the family?",
        "options": {
            "A": "They are usually good at making friends.",
            "B": "They tend to be adventurous and creative.",
            "C": "They are often content with what they have.",
            "D": "They tend to be self-assured and responsible.",
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。设题要点为分类介绍处。原文说：“The oldest tends to be self-assured, responsible, a high achiever and relatively serious and reserved.”D) 复现了长子女的两大特点。因此答案为 D)。A) 与「他可能不会轻易结交朋友（slow to make friends）」相悖；B) 中 adventurous、creative 实为么子女的特点；C) 中 content 虽复现，但原文指「或许满足于只有一个同伴」，选项将其引申至生活方方面面。",
    },
    25: {
        "prompt": "What does the speaker say about the only children?",
        "options": {
            "A": "They enjoy making friends.",
            "B": "They tend to be well adjusted.",
            "C": "They are least likely to take initiative.",
            "D": "They usually have successful marriages.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为分类介绍处。末段说：“since an only tends to be a well-adjusted individual, she'll eventually learn to relate to any chosen spouse.”与 B) 复现。因此答案为 B)。A) 与末段 often most comfortable when alone（最自在于独处）相悖；C) 虽复现 less likely to take initiative，但那是排行中间孩子的特点；D) 由 well-adjusted、relate to any chosen spouse 过度引申，原文并未提到婚姻是否成功。",
    },
}


def main():
    out = Path(__file__).resolve().parent / f"data_{EXAM_ID.replace('-', '_')}.py"
    with open(out, "w", encoding="utf-8") as f:
        f.write("#!/usr/bin/env python3\n")
        f.write('"""\n')
        f.write(f"Official data for {EXAM_ID} CET-6 listening test:\n")
        f.write("- 7 subparts with authentic titles, Chinese topics, and question ranges\n")
        f.write("- Complete grammatical sentences with 100% paired authentic Chinese translations\n")
        f.write("- 25 official CET-6 questions with options, answers, and explanations\n")
        f.write('"""\n\n')
        f.write("SUBPARTS = ")
        f.write(pprint.pformat(SUBPARTS, width=100, sort_dicts=False))
        f.write("\n\nQUESTIONS = ")
        f.write(pprint.pformat(QUESTIONS, width=100, sort_dicts=False))
        f.write("\n")
    total_sent = sum(len(sp["sentences"]) for sp in SUBPARTS)
    print(f"Wrote {out}")
    print(f"Subparts: {len(SUBPARTS)}  Sentences: {total_sent}  Questions: {len(QUESTIONS)}")


if __name__ == "__main__":
    main()
