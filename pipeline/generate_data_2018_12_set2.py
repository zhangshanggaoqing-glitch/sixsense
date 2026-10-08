#!/usr/bin/env python3
"""
Generate pipeline/data_2018_12_set2.py with 100% golden standard:
- 7 Subparts with authentic titles, Chinese topics, and question ranges
- Complete grammatical sentences with 100% paired authentic Chinese translations
- 25 Official CET-6 questions with full options, verified answers, and detailed explanations
"""

import pprint
from pathlib import Path

EXAM_ID = "2018-12-set2"

SUBPARTS = [
    {
        "id": f"{EXAM_ID}-conv-1",
        "subpart_code": "conv-1",
        "section_id": f"{EXAM_ID}-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 1 · 男生的网红梦：与雕像合照引发成为网红的理想与修图运营的幕后付出",
        "topic_zh": "业余拍照爱好者追逐网络红人梦：发帖获赞起步、修图选题与涨粉运营、以及女士对自身照片的不满",
        "question_range": "Q1 ~ Q4",
        "questions": [1, 2, 3, 4],
        "sp_start": 34.64,
        "sp_end": 215.00,
        "sentences": [
            ("M", "Do you mind taking my photo with the statue over there? I think it will make a great shot.",
             "你介意帮我和那边的雕像拍张照吗？我觉得这样拍出来的照片会很棒。"),
            ("W", "Sure, no worries. You're always taking photos. What do you do with all the photos you take?",
             "当然，没问题。你一直在拍照。你都怎么处理拍出来的那些照片呢？"),
            ("M", "Well, don't laugh. My dream is to become an online celebrity of sorts.",
             "嗯，别笑我。我的梦想是成为一个小有名气的网红。"),
            ("W", "You are not serious, are you?", "你该不会是认真的吧？"),
            ("M", "I am, completely. I just got the idea a few months ago after posting some holiday photos on my social media accounts. A lot of people liked my photos and started asking me for travel tips. So I figured I'd give it a go. I post a lot on social media anyway, so I've got nothing to lose.",
             "我非常认真。几个月前我在自己的社交媒体账号上发了一些度假照片，才有了这个想法。很多人给我的照片点赞，还向我索要旅行攻略。所以我想我应该试试。反正我平时也在社交媒体上发很多东西，也没什么损失。"),
            ("W", "I guess that's true. So what do you have to do to become Internet famous?",
             "我想你说的对。那么，你要怎么做才能成为网红呢？"),
            ("M", "Surprisingly a lot more than I did as a hobby. Recently, I've been spending a lot more time editing photos, posting online and clearing storage on my phone. It's always full now.",
             "没想到的是，这比我当初只把它当业余爱好要多做很多。最近，我花了大量时间修图、发帖，以及清理手机存储空间，我的手机现在存储总是占满。"),
            ("W", "That doesn't sound like too much work.", "听起来工作量并不大呀。"),
            ("M", "Well, there's more to it. I spent all last weekend researching what topics are popular, what words to use in captions and similar accounts to follow. It really was a lot to take in. And I was up well past midnight. I'd say it's paying off though. I increased the number of people following my accounts by 15 already.",
             "当然远不止这些。上周整个周末我都在研究什么话题热门、什么词可用作标题，以及要关注哪些相似账号。的确有很多东西要领会。而且我过了半夜都还没睡。不过我得说这是值得的。我已经把关注我账号的人数提升了 15%。"),
            ("W", "That is impressive. I guess I never thought much about all the effort behind the scene. Now that I think about it, there's always something wrong with my photos as it is—half smiles, closed eyes, messy hair. I hope you have better luck than I do. Then again, I think the only person interested in my photos is my mom.",
             "真了不起。我想我从未考虑过需要这么多的幕后努力。现在回想起来，我的照片里总有些瑕疵——似笑非笑、闭着眼睛、头发凌乱。我希望你运气比我好。不过话又说回来，我觉得唯一对我的照片感兴趣的人就是我妈妈。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-conv-2",
        "subpart_code": "conv-2",
        "section_id": f"{EXAM_ID}-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 2 · 访谈节目《今日物理》：女科学家谈宇宙起源与物质反物质的对撞湮灭",
        "topic_zh": "理论物理学家解读宇宙起源：大爆炸瞬间物质与反物质生成、本应彼此湮灭却因物质略多而留存宇宙",
        "question_range": "Q5 ~ Q8",
        "questions": [5, 6, 7, 8],
        "sp_start": 215.00,
        "sp_end": 413.50,
        "sentences": [
            ("M", "Good evening, and welcome to Physics Today. Here we interview some of the greatest minds in physics as they help us to understand some of the most complicated theories. Today, I'm very pleased to welcome Dr. Melissa Phillips, professor of theoretical physics. She's here to tell us a little about what it is she studies. Dr. Phillips, you seem to study everything.",
             "晚上好，欢迎来到《今日物理》。节目中我们采访一些物理学界首屈一指的学者，帮助我们理解一些最复杂的理论。今天我十分高兴地欢迎理论物理学教授梅丽莎·菲利普斯博士，她来到这里是为和我们聊聊她的研究。菲利普斯博士，您似乎什么都研究啊。"),
            ("W", "I guess that would be fair to say. I spend most of my time studying the Big Bang theory and where our universe came from.",
             "我想这么说会比较恰当——我大部分时间都在研究宇宙大爆炸理论以及我们的宇宙从何而来。"),
            ("M", "Can you tell us a little about that?", "您能就此问题跟我们谈谈吗？"),
            ("W", "Well, I'm very interested in why the universe exists at all. That may sound odd, but the fact is at the moment of the Big Bang, both matter and anti-matter were created for a short time, and I mean just a fraction of a second. The whole universe was a super-hot soup of radiation filled with these particles. So what's baffled scientists for so long is why is there a universe at all?",
             "嗯，我对「宇宙究竟为何存在」很感兴趣。这可能听着奇怪，但事实上，在大爆炸的那一刻，物质和反物质在短时间内同时生成，我是说仅在几分之一秒的功夫里。整个宇宙当时就是一盆超高温的放射物浓汤，里面充满了这些放射物粒子。所以长久以来困扰科学家的是「到底为什么会有宇宙」。"),
            ("M", "That's because matter and anti-matter are basically opposites of each other. They are exactly alike, except that they have opposite electrical charges. So when they collide, they destroy each other?",
             "这是因为物质和反物质从根本上是相反的。它们除了带有相反的电荷之外完全一样。所以当它们碰撞时，会摧毁彼此？"),
            ("W", "Exactly. So during the first few moments of the Big Bang, the universe was extremely hot and very small. Matter and the now more exotic anti-matter would have had little space to avoid each other. This means that they should have totally wiped each other out, leaving the universe completely barren.",
             "没错。所以大爆炸之初的刹那间，整个宇宙温度极高，空间极其狭小。物质和如今更显奇异的反物质本没有什么空间能避开对方。也就是说，它们本应完全湮灭彼此，徒留一片荒凉世界。"),
            ("M", "But a recent study seems to point to the fact that when matter and anti-matter were first created, there were slightly more particles of matter, which allowed the universe we all live in to form?",
             "但是一项新研究似乎指出一项事实：物质和反物质最初生成之时，物质粒子稍稍多了一些，这就让我们所生存的宇宙得以形成？"),
            ("W", "Exactly. Because there was slightly more matter, the collisions quickly depleted all the anti-matter and left just enough matter to create stars, planets and eventually us.",
             "没错。因为物质多了那么一点点，碰撞很快把所有的反物质清除一空，留下刚好足量的物质，生成了恒星、行星，并最终造就了我们。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-pass-1",
        "subpart_code": "pass-1",
        "section_id": f"{EXAM_ID}-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 1 · 外国口音综合征：迈尔斯两年英式口音、中风脑损伤诱因与百年仅约六十例",
        "topic_zh": "罕见疾病Foreign Accent Syndrome：口音突变案例、致因与发音扭曲机制、极低发病率与后续研究缺口",
        "question_range": "Q9 ~ Q11",
        "questions": [9, 10, 11],
        "sp_start": 445.50,
        "sp_end": 600.00,
        "sentences": [
            ("M", "In this week's edition of a special series on Bizarre Medical Conditions, there is a report of the case of Michelle Myers. Myers is an American woman who woke up one day speaking with a British accent, even though she's lived in the United States all her life.",
             "本周「奇疾怪症」特别系列为您带来一篇关于米歇尔·迈尔斯的报道。迈尔斯女士是一名美国人，某天醒来后讲话突然变成了英式口音，尽管她一直生活在美国。"),
            ("M", "In 2015, Myers went to bed with a terrible headache. She woke up sounding like someone from England. Her British accent has remained for the past two years. Previously, Myers had woken up speaking in Irish and Australian accents. However, on both of those occasions, the accents lasted for only a week.",
             "2015 年某日，迈尔斯带着严重头痛上床睡觉。她醒来后说话听起来便像是英国人。她的英式口音在过去两年里一直保持未变。在此之前，迈尔斯曾一觉醒来变成爱尔兰腔和澳大利亚腔。然而那两次口音突变都只持续了一周。"),
            ("M", "Myers has been diagnosed with Foreign Accent Syndrome. It's a disorder in which a person experiences a sudden change to their speech so that they sound like they are speaking in a foreign accent. The condition is most often caused by a stroke or traumatic brain injury.",
             "迈尔斯被诊断出患有外国口音综合征。这是一种疾病，患有这种疾病的人说话方式会突然大变，听起来就像是外国口音。这种病症通常由中风或颅脑损伤引起。"),
            ("M", "Although people with the syndrome have intelligible speech, their manner of speaking is altered in terms of timing and tongue placement, which may distort their pronunciation. The result is that they may sound foreign when speaking their native language. It's not clear whether Myers has experienced a stroke or other brain damage, but she also has a separate medical condition, which can result in loose joints, easily bruised skin and other problems.",
             "虽然这种综合征患者的讲话内容可以理解，但其说话方式（包括说话的节奏以及舌头的位置）发生了改变，这会扭曲他们的发音，结果便是他们说母语时可能听起来像外国人。目前还不清楚迈尔斯是否曾经中风或有其他脑损伤，但她有另外的病症，这种病症可能导致关节松动、皮肤容易擦伤和其他问题。"),
            ("M", "Foreign Accent Syndrome is rare, with only about 60 cases reported within the past century. However, a different American woman reportedly spoke with a Russian accent in 2010 after she fell down the stairs and hit her head.",
             "外国口音综合征非常罕见，上个世纪只出现约 60 例报道。然而据报道，2010 年另一名美国女性从楼梯上摔下撞到头部后，说话就带上了俄罗斯口音。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-pass-2",
        "subpart_code": "pass-2",
        "section_id": f"{EXAM_ID}-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 2 · 女性游泳简史：维多利亚时期的端庄限制、更衣车与埃德勒横渡英吉利海峡",
        "topic_zh": "女性游泳百年演变：从端庄观念下全副武装下海，到泳装革新与首位横渡英吉利海峡的女英雄",
        "question_range": "Q12 ~ Q15",
        "questions": [12, 13, 14, 15],
        "sp_start": 616.00,
        "sp_end": 805.50,
        "sentences": [
            ("M", "There is something about water that makes it a good metaphor for life. That may be one reason why so many people find relief in swimming when life's seas get rough. And it goes some way towards explaining why books about swimming, in which people tackle icy lakes, race in rivers and overcome oceans while reflecting on their lives, have recently become so popular.",
             "水的某些特质使它成为生命的恰当隐喻。这也许就是为什么当生活的海洋变得处境艰难时，会有那么多的人在游泳中得到宽慰的原因之一。它还在某种程度上解释了为什么关于游泳的书籍最近越来越受欢迎——这些书的主题为：人们挑战冰冷的湖泊、在河流中比赛、征服海洋，同时反思自己的人生。"),
            ("M", "These books reflect a trend, particularly strong in Britain, where swimming in pools is declining but more and more folks are opting for open water. Wild swimming seems to be especially popular among women. Jenny Landreth recently published a guide to the best swimming spots in London. Her new book, Swell, interweaves her own story with a history of female pioneers who accomplished remarkable feats and paved the way for future generations.",
             "这些书反映了一种趋势——在英国尤为明显，去泳池游泳的人越来越少，而选择开放水域的人越来越多，「野泳」似乎特别受女性欢迎。珍妮·兰德雷斯最近出版了一本伦敦最佳游泳场所指南。她的新作《浪涌》将她自己的故事与那些取得了非凡成就、并为后代铺平道路的女性先驱的历史交织在一起。"),
            ("M", "Notions of modesty restricted women in the Victorian era, but they still swam. A bathing machine was rolled down to the seashore so women would not be seen in swimwear. In 1892, The Gentlewoman's Book of Sport described a woman swimming in a heavy dress, boots, hat, gloves and carrying an umbrella.",
             "在维多利亚时代，「端庄」的观念限制着当时的女性，但她们依然游泳。「游泳更衣车」会被推到海边，使女性不被看到身着泳衣的样子。1892 年，《淑女运动指南》描述了一位女性游泳时的形象：身着厚重的裙子、靴子，戴着帽子和手套，手里还撑把雨伞。"),
            ("M", "Eventually, swimming became freer. Mixed bathing was permitted on British beaches in 1901. Women won the right to swim in public pools, learned to swim properly, created appropriate swimwear and, in time, even competed against men. The first woman to cross the English Channel was Gertrude Ederle in 1926. She beat the record by almost two hours and her father rewarded her with a red sports car.",
             "终于，游泳变得不那么受限了。1901 年，英国海滩开始允许男女混泳。女性赢得了在公共泳池游泳的权利，学习了游泳技巧，设计出了得体的泳衣，最后甚至与男性竞赛。1926 年，格特鲁德·埃德勒成为首位横渡英吉利海峡的女性。她以近两小时的优势打破纪录，父亲奖励了她一辆红色跑车。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-rec-1",
        "subpart_code": "rec-1",
        "section_id": f"{EXAM_ID}-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 1 · 高科技测谎能否用于庭审：脑扫描公司宣称九成七准确、脑科学家质疑与法官决策",
        "topic_zh": "磁扫描测谎技术的可靠性争议：缺乏真实情境验证、心智不等同于大脑与法庭应用应审慎",
        "question_range": "Q16 ~ Q18",
        "questions": [16, 17, 18],
        "sp_start": 829.50,
        "sp_end": 1078.00,
        "sentences": [
            ("M", "Today I'm going to talk about a very special kind of person. Psychologists call them masters of deception—those rare individuals with a natural ability to tell with complete confidence when someone is telling a lie. For decades, researchers and law enforcement agencies have tried to build a machine that will do the same thing.",
             "今天我要谈论一类非常特殊的人。心理学家称其为「骗术大师」——这些罕见的个体有一种天赋：若有人说谎，他们能够相当自信地识破。几十年来，研究人员和执法机构一直致力于建造一台具有同样功能的机器。"),
            ("M", "Now a company in Massachusetts says that by using magnetic brain scans they can determine with 97% accuracy whether someone is telling the truth. They hope that the technology will be cleared for use in American courts by early next year. But is this really the ultimate tool for you, the lawyers of tomorrow?",
             "现在马萨诸塞州的一家公司表示，他们能通过脑部磁扫描以 97% 的准确率测定一个人是否在说实话。他们希望该技术能够于明年初在美国法庭获准投入使用。但这真的是你的终极工具吗，也就是明日律师的终极工具？"),
            ("M", "You'll not find many brain scientists celebrating this breakthrough. The company might be very optimistic, but the ability of their machine to detect deception has not provided credible proof. That's because the technology has not been properly tested in real-world situations. In life, there are different kinds of lies and diverse context in which they're told. These differences may elicit different brain responses. Does their hypothesis behind the test apply in every case? We don't know the answer, because studies done on how reliable this machine is have not yet been duplicated. Much more research is badly needed.",
             "你会发现，没有多少脑科学家在赞美这项突破。该公司也许相当乐观，但是其机器的识骗能力并未提供可信性证明。这是因为该技术尚未在现实情境中进行充分测试。生活中有形形色色的谎言，而这些谎言又有着各式各样的生成语境。这些区别可能引起大脑的不同反应。他们试验背后的假设能应用于每一个案件吗？我们并不知道答案，因为关于这台机器可信度如何的研究尚未被复制。急需更多的研究。"),
            ("M", "Whether the technology is eventually deemed reliable enough for the courts will ultimately be decided by the judges. Let's hope they're wise enough not to be fooled by a machine that claims to determine truthfulness at the flick of a switch. They should also be sceptical of the growing tendency to try to reduce all human traits and actions to a low level of brain activity. Often, they do not map that easily.",
             "此项技术最后是否会被视为对法庭足够可靠，最终将由法官决定。但愿法官们足够明智，别被一个声称只须轻按开关便能确定诚实与否的机器愚弄。他们也应该对「将人类所有性格特性和行为简化为大脑活动水平」的渐强趋势保持怀疑。通常来说，性格行为和大脑活动水平并不能轻易匹配。"),
            ("M", "Moreover, understanding the brain is not the same as understanding the mind. Some researchers have suggested that thoughts cannot properly be seen as purely internal. Instead, thoughts make sense only in reference to the individual's external world. So while there may be insights to be gained from matching behavior to brain activity, those insights will not necessarily lead to justice in a court of law. Problems surround the use of machines to spot deception, at least until it has been rigorously tested.",
             "再者，理解大脑和理解思维是两码事。一些研究人员已指出，不能将思想完全视为纯粹「内部的」。相反，只有和个体的外部世界相联系，思想才有意义。因此，尽管将行为和大脑活动进行匹配可能会获得一些洞见，但这些见解未必能实现法庭上的公正。至少在严格测试前，使用机器识骗还存在诸多问题。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-rec-2",
        "subpart_code": "rec-2",
        "section_id": f"{EXAM_ID}-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 2 · 全球语言多样性之谜：马卡鲁瓦岛四十种土著语言、七千种语言与既往研究的空白",
        "topic_zh": "语言地理分布研究：太平洋小岛的语言奇迹、热带远多于温带、既往研究未发现明确模式",
        "question_range": "Q19 ~ Q21",
        "questions": [19, 20, 21],
        "sp_start": 1078.00,
        "sp_end": 1330.00,
        "sentences": [
            ("M", "Last week I attended a research workshop on an island in the South Pacific. Thirty people were present and all except me came from the island, called Makelua, in the nation of Vanuatu. They live in 16 different communities and speak 16 distinct languages. In many cases, you could stand at the edge of one village and see the outskirts of the next community. Yet the residents of each village speak a completely different language.",
             "上周我在南太平洋一个小岛上参加了一场研讨会。当时有三十人出席，除我之外的所有人都来自瓦努阿图国一个叫作马卡鲁瓦的岛屿。他们生活在 16 个不同的社群，说 16 种不同的语言。在许多情况下，站在一个村庄的村头，你能看到另一个社群的郊野。然而，每个村庄的居民都说着完全不同的语言。"),
            ("M", "According to recent work by my colleagues at the Max Planck Institute for the Science of Human History, this island, just 100 kilometers long and 20 kilometers wide, is home to speakers of perhaps 40 different indigenous languages.",
             "根据我在马克斯·普朗克人类历史科学研究所的同事们的最新研究，在这座仅 100 公里长、20 公里宽的岛屿上，栖居着大概 40 种不同土著语言的使用者。"),
            ("M", "Why so many? We could ask the same question of the entire globe. People don't speak one universal language, or even a handful. Instead, today our species collectively speaks over 7,000 distinct languages. And these languages are not spread randomly across the planet. For example, far more languages are found in tropical regions than in the mild zones. The tropical island of New Guinea is home to over 900 languages. Russia, 20 times larger, has 105 indigenous languages. Even within the tropics, language diversity varies widely. For example, the 250,000 people who live on Vanuatu's 80 islands speak 110 different languages, but in Bangladesh, a population 600 times greater, speaks only 41 languages.",
             "为什么有这么多种语言呢？我们可以对全世界提出同样的问题。人们没有一种通用语言，甚至也不是只说几种语言。相反，今天我们人类一共有 7000 多种不同的语言。而这些语言在地球上并不是随意分布的。例如，在热带地区发现的语言种类远多于温带地区。热带岛屿新几内亚有 900 多种语言。而面积是新几内亚 20 倍的俄罗斯则只有 105 种土著语言。甚至在热带地区内部，语言多样性也有很大差异。例如，生活在瓦努阿图 80 个岛屿上的 25 万人讲着 110 种不同的语言，但在人口是瓦努阿图 600 倍的孟加拉国，却只有 41 种语言。"),
            ("M", "How come humans speak so many languages? And why are they so unevenly spread across the planet? As it turns out, we have few clear answers to these fundamental questions about how humanity communicates. Most people can easily brainstorm possible answers to these intriguing questions. They hypothesize that language diversity must be about history, cultural differences, mountains or oceans dividing populations. But when our diverse team of researchers from six different disciplines and eight different countries began to review what was known, we were shocked that only a dozen previous studies had been done, including one we ourselves completed on language diversity in the Pacific.",
             "为什么人类会有这么多种语言？为什么这些语言在地球上的分布如此不均衡？事实证明，我们对人类是如何交流这类基本问题尚无明确的答案。大多数人能轻松地通过头脑风暴对这些有趣的问题做出可能的解释。他们假定语言的多样性一定与历史、文化差异、山川或海洋分隔人口有关。但是，当来自 6 个不同学科、8 个不同国家的研究人员组成的多元化团队开始回顾已知内容时，我们震惊地发现，在此之前只有 12 项相关研究，其中还包括一项我们自己完成的关于太平洋地区语言多样性的研究。"),
            ("M", "These prior efforts all examined the degree to which different environmental, social and geographic variables correlated with the number of languages found in a given location. The results varied a lot from one study to another, and no clear patterns emerged. The studies also ran up against many methodological challenges, the biggest of which centered on the old statistical saying—correlation does not equal causation.",
             "这些研究都是在检验不同环境、社会和地理变量与某既定地区所发现的语言数量之间的相关程度。不同研究的结果各不相同，并未发现明确的模式。这些研究还遭遇了许多方法论上的挑战，其中最大的挑战集中在那句古老的统计学箴言上——相关关系并不等于因果关系。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-rec-3",
        "subpart_code": "rec-3",
        "section_id": f"{EXAM_ID}-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 3 · 美国梦褪色：中产消失与九比一的财富悬殊、低薪兼职商业模式与全职渴望",
        "topic_zh": "美国贫富差距扩大的现实：中产阶级消失、收入分配失衡、企业仅用兼职与底层群体全职就业的渴望",
        "question_range": "Q22 ~ Q25",
        "questions": [22, 23, 24, 25],
        "sp_start": 1330.00,
        "sp_end": 1490.00,
        "sentences": [
            ("M", "We often hear people say that America is a land of opportunity, a country built on hope to aspire the greatness on the American dream. But is the dream as we once knew it dying? Today's demographics show that the middle-class is disappearing, and now the richest 10% of the population has mastered more wealth than the bottom 90%.",
             "我们常听人说美国是一个机遇之地，一个建立在追求伟大美国梦希望之上的国家。但我们曾经的梦想是否正在破灭？当今的人口统计资料显示，中产阶级正在消失，现在 10% 的富裕人口的财富量超过 90% 底层人口的总和。"),
            ("M", "Once upon a time, Americans thought that if they worked hard enough, even in the face of adversity, they would be rewarded with success. These days, though, the divide between rich and poor is greater than it has ever been. The question is, what is it going to take to change things? Maybe one day soon real change will actually be made in our nation and the gap will be eradicated. But what happens in the meantime? Is there something that we can do to help close the gap? Is there something that we can do to prove that a little compassion goes a long way?",
             "过去，美国人认为只要他们足够努力，即便是在困境中也能收获成功。然而现如今，贫富差距比以往任何时候都大。问题是，怎么做才能改变现状？也许在不久后的某一天，我们的国家将真正发生改变，贫富差距将会被消除。但在此期间呢？我们能否做些什么来帮助缩小差距、来证明些许同情心能产生深远的影响呢？"),
            ("M", "If we want to fix the problem of the income gap, first, we have to understand it. It is a grim reality that you can have one person who only makes around 13,000 dollars a year, or across town, another is making millions. For me, it is kind of astonishing. And if you ask low-income people what's the one thing that will change their life, they'll say a full-time job. That's all they aspire to. So why is it so difficult for so many people to find employment?",
             "如果我们想要解决收入差距问题，首先得理解这些问题。一个残酷的现实是，有人一年只能挣大约 1.3 万美金，而在城镇的另一边，有人正挣着几百万。对我来说，这有些令人吃惊。如果你问低收入群体，什么会改变他们的生活，他们会说要一份「全职工作」。这就是他们所渴望的全部。那么，为什么这么多人都难以找到工作呢？"),
            ("M", "It partly comes down to profit-driven business models that are built around low-wage work and part-time jobs that don't provide benefits. Businesses, in order to boost profits, hire employees as part-time workers only. This means they are paid the lowest legal wage and receive no health care or other benefits provided to full-time employees.",
             "这部分归因于利润驱动的商业模式，它基于低薪工作和不提供福利的兼职工作而建立。企业为了增加利润，只雇用兼职员工，这意味着他们只能领到法定最低工资，也没有全职员工所享有的医疗保健或其他福利。"),
            ("M", "Simultaneously, technological advancement and a global economy has reduced the demand for well-paying blue-collar jobs here in the United States. The cumulative effect of these two factors is that many Americans are forced to take two or more part-time jobs, just to make ends meet. What has become obvious to me when it comes to the income gap is that there needs to be an opportunity for the people at the bottom to push them back up and push them into the middle-class to give them hope in their lives.",
             "与此同时，技术进步和全球化经济减少了美国对高薪蓝领工作的需求。这两个因素的累加效应就是，许多美国人被迫从事两份或两份以上兼职工作，而这仅仅能维持收支平衡。在收入差距问题上，我认为显而易见的一点是，底层群体需要有机会将自己重新推回上一阶层、挤入中产阶层，以此获得生活的希望。"),
        ],
    },
]

QUESTIONS = {
    1: {
        "prompt": "What does the man ask the woman to do?",
        "options": {
            "A": "Stop worrying about him.",
            "B": "Keep away from the statue.",
            "C": "Take a picture of him.",
            "D": "Put on a smile for the photo.",
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。设题要点为提出请求处。男士说：“Do you mind taking my photo with the statue over there?”即请女士为自己拍照，C) 同义复现这一请求。因此答案为 C)。A) 将女士同意拍照的答复（Sure, no worries）曲解为「男士请求女士停止对他的担忧」；B) 利用拍照取景处的 statue 杜撰出「请女士离雕塑远点」；D) 利用片段信息 taking my photo 捏造，对话中并未提及「微笑」，且是男士请女士为自己拍照，而非男士给女士拍照。",
    },
    2: {
        "prompt": "What does the man dream of?",
        "options": {
            "A": "Gaining great fame on the Internet.",
            "B": "Publishing a collection of his photos.",
            "C": "Collecting the best photos in the world.",
            "D": "Becoming a professional photographer.",
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。设题要点为细节介绍处。男士说：“My dream is to become an online celebrity of sorts.”Gaining great fame 即 become a celebrity 所指，on the Internet 与 online 同义。因此答案为 A)。B) 把男士提到的「将照片发布在社交媒体上」窜改为「出版照片集」；C) 中「收集」与「全世界最好的照片」在对话中均未提及；D) 由对话中大量信息涉及拍照而主观认为男士想成为专业摄影师，但拍照只是服务于其「成为网红」的理想。",
    },
    3: {
        "prompt": "What has the man been busy doing recently?",
        "options": {
            "A": "Surfing various websites and collecting photos.",
            "B": "Editing his pictures and posting them online.",
            "C": "Following similar accounts to compare notes.",
            "D": "Studying the pictures in popular social media.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为细节介绍处。男士说：“Recently, I've been spending a lot more time editing photos, posting online and clearing storage on my phone.”B) 精准复现这一表述。因此答案为 B)。A) 中 Surfing various websites 虽属男士所忙之事，但 collecting photos 体现的是「从网上下载」，与 posting online「把照片发布在网上」相悖；C) 中 Following similar accounts 复现第 9 段所述上周末之事，但 compare notes 在文中无迹可寻；D) 将研究对象「哪些是热门话题」曲解为「流行社交媒体上的图片」。",
    },
    4: {
        "prompt": "What does the woman say about her photos?",
        "options": {
            "A": "They are far from satisfactory.",
            "B": "They are mostly taken by her mom.",
            "C": "They make an impressive album.",
            "D": "They record her fond memories.",
        },
        "answer": "A",
        "explanation": "【精析】细节概括题。设题要点为观点表达处。女士说：“there's always something wrong with my photos as it is—half smiles, closed eyes, messy hair.”即她的照片总有些瑕疵，A) 是对其准确概括。因此答案为 A)。B) 将「唯一对她照片感兴趣的人是她妈妈」窜改为「照片主要由她妈妈拍摄」；C) 将女士对男士所言的 That is impressive 当作对自己照片的评价，且未提及「影集」相关信息；D) 利用「照片记录美好瞬间」的常识干扰，对话中并未提及。",
    },
    5: {
        "prompt": "What does the man say is Physics Today?",
        "options": {
            "A": "A journal reporting the latest progress in physics.",
            "B": "An introductory course of modern physics.",
            "C": "An occasion for physicists to exchange ideas.",
            "D": "A series of interviews with outstanding physicists.",
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。设题要点为开篇背景介绍处。男士说：“Good evening, and welcome to Physics Today. Here we interview some of the greatest minds in physics...”，题干与 D) 共同构成对 Here we interview...in physics 的正确解读。因此答案为 D)。A) 利用新研究干扰，但「今日物理」出现于开篇，是对话发生的场景；B) 中 introductory course 在文中无对应；C) 利用「一些最杰出的物理学家」干扰，但后文 help us to understand、She's here to tell us 明确这是访谈节目邀请物理学家与观众交流，而非物理学家之间的交流。",
    },
    6: {
        "prompt": "What is the woman physicist's main research area?",
        "options": {
            "A": "The future of the physical world.",
            "B": "The origin of the universe.",
            "C": "Sources of radiation.",
            "D": "Particle theory.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为新话题引出处。女士说：“I spend most of my time studying the Big Bang theory and where our universe came from.”「宇宙大爆炸」与「宇宙从何而来」均属宇宙起源问题，B) 正确概括了这一研究领域。因此答案为 B)。A) 利用开篇碎片信息干扰，对话并未探及「物质世界的未来」；C) 利用 super-hot soup of radiation 干扰，但该信息也服务于「宇宙如何产生」，并未提及这些放射物的来源；D) 利用 these particles 干扰，女士通篇未再深入解释粒子相关知识。",
    },
    7: {
        "prompt": "What is the woman interested in?",
        "options": {
            "A": "How matter collides with anti-matter.",
            "B": "Whether the universe will turn barren.",
            "C": "Why there exists anti-matter.",
            "D": "Why there is a universe at all.",
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。设题要点为提问具体内容处。女士说：“I'm very interested in why the universe exists at all.”其中 exists 义同选项中的 there is，与题干共同契合这一表述。因此答案为 D)。A)「物质与反物质碰撞」属男士的回应，文中并未说明女士是否对此感兴趣；B) 将「物质与反物质本该完全抵消从而导致宇宙空无一物」这一铺垫，偷换为「宇宙未来的走向」；C) 张冠李戴，将女士感兴趣的「宇宙为何存在」窜改为「反物质为何存在」。",
    },
    8: {
        "prompt": "What seems to be the finding of the recent study?",
        "options": {
            "A": "Matter and anti-matter are opposites of each other.",
            "B": "Anti-matter allowed humans to come into existence.",
            "C": "The universe formed due to a sufficient amount of matter.",
            "D": "Anti-matter exists in very high-temperature environments.",
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。设题要点为话题转换兼新信息引出处。男士说：“But a recent study seems to point to the fact that when matter and anti-matter were first created, there were slightly more particles of matter, which allowed the universe we all live in to form.”C) 同义改写这一结论，选项中的 due to 复现文中 which allowed 标识的因果关联。因此答案为 C)。A) 源自男士话语，但属已知知识，并非新研究的发现；B) 将「碰撞所剩的足量物质造就了宇宙和人类」窜改为「反物质造就了人类」；D) 源自女士描述大爆炸之初的情形，但同样属已有发现。",
    },
    9: {
        "prompt": "What happened to Michelle Myers one day?",
        "options": {
            "A": "She found herself speaking a foreign language.",
            "B": "She woke up speaking with a different accent.",
            "C": "She found some symptoms of her illness gone.",
            "D": "She woke up finding herself in another country.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为事例详情处。首段说：“Myers is an American woman who woke up one day speaking with a British accent, even though she's lived in the United States all her life.”由 lived in the United States all her life 与 speaking with a British accent 可推知，她身处的国家未变、所讲的语言未变，变的只是讲英语的口音。因此答案为 B)。A)、D) 均利用 British、England、Irish、Australian 等碎片信息捏造，原文均指口音的变化，而非「语言」或「国家」的变化；C) 由 went to bed with a terrible headache 过度推断而来，文章并未提及该病症是否消失。",
    },
    10: {
        "prompt": "What does the passage say about Foreign Accent Syndrome?",
        "options": {
            "A": "It is usually caused by a stroke or brain injury.",
            "B": "It has not yet found any effective treatment.",
            "C": "It leaves the patient with a distorted memory.",
            "D": "It often happens to people with speech defects.",
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。设题要点为原因处。第二段说：“The condition is most often caused by a stroke or traumatic brain injury.”其中 The condition 回指 Foreign Accent Syndrome，A) 是其同义转述。因此答案为 A)。B) 源自 It's not clear，但原文指「迈尔斯的发病原因不清楚」，并未谈及该综合征的治疗；C) 源自 distort，但综合征扭曲的是发音（pronunciation）而非记忆；D) 源自 speech，但原文是在指出该病影响「导致说话方式改变、说话内容仍可理解」，并未提及易发病对象。",
    },
    11: {
        "prompt": "What accent did another American woman speak with after a head injury?",
        "options": {
            "A": "British.",
            "B": "Irish.",
            "C": "Russian.",
            "D": "Australian.",
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。设题要点为转折处。末句说：“a different American woman reportedly spoke with a Russian accent in 2010 after she fell down the stairs and hit her head.”与 C) 相符。因此答案为 C)。A)、B)、D) 均为迈尔斯女士一觉醒来后说话的口音，与题干所问的「另一名女性头部受伤后的口音变化」不符。",
    },
    12: {
        "prompt": "What has become so popular recently?",
        "options": {
            "A": "Water sports.",
            "B": "Racing in rivers.",
            "C": "Stories about women swimmers.",
            "D": "Books about swimming.",
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。设题要点为因果关系兼细节介绍处。首段说：“And it goes some way towards explaining why books about swimming...have recently become so popular.”题干与 D) 共同精准复现这一表述。因此答案为 D)。A)、B) 利用全文话题 swimming 与书中内容（race in rivers）干扰，但均非题干所问「最近变得流行的事物」；C) 利用 women、swimming 及 her own story 杜撰出「女性游泳相关的故事很流行」。",
    },
    13: {
        "prompt": "What did Jenny Landreth do recently?",
        "options": {
            "A": "She succeeded in swimming across the English Channel.",
            "B": "She published a guide to London's best swimming spots.",
            "C": "She told her story of adventures to some young swimmers.",
            "D": "She wrote a book about the history of swimwear in the UK.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为细节介绍处。第二段说：“Jenny Landreth recently published a guide to the best swimming spots in London.”B) 精准复现这一信息。因此答案为 B)。A) 张冠李戴，成功横渡英吉利海峡的是格特鲁德·埃德勒；C) 将「她的新书中交织着自己的故事」歪曲为「她给年轻游泳者讲自己的冒险故事」；D) 利用第三、四段的个别词汇 swimwear 干扰，将其书中内容由「自己和女性先驱的故事」窜改为「英国泳衣历史」。",
    },
    14: {
        "prompt": "What do we learn about women in the Victorian era?",
        "options": {
            "A": "They loved vacationing on the seashore.",
            "B": "They had a unique notion of modesty.",
            "C": "They were prohibited from swimming.",
            "D": "They were fully dressed when swimming.",
        },
        "answer": "D",
        "explanation": "【精析】细节推断题。设题要点为特定时期细节介绍处。第三段末句描述女性游泳时的形象为「身着厚重的裙子、靴子，戴着帽子和手套，手里还撑把雨伞」，D) 是基于此做出的合理推断。因此答案为 D)。A) 利用个别词汇 seashore 杜撰出「喜欢在海边度假」；B) 将「端庄的观念对女性有诸多限制」曲解为「女性对端庄的认识独特」；C) 与首句后半部分「但她们仍然游泳」相悖。",
    },
    15: {
        "prompt": "What does the passage say about Gertrude Ederle?",
        "options": {
            "A": "She designed lots of appropriate swimwear for women.",
            "B": "She once successfully competed against men in swimming.",
            "C": "She was the first woman to swim across the English Channel.",
            "D": "She was an advocate of women's right to swim in public pools.",
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。设题要点为人物细节介绍处。末段说：“The first woman to cross the English Channel was Gertrude Ederle in 1926.”与 C) 精准对应。因此答案为 C)。A)、B)、D) 分别利用末段「女性设计出了得体的泳衣」「女性与男性进行游泳比赛」「女性有了在公共泳池游泳的权利」干扰，这些内容均与题干所问人物无关。",
    },
    16: {
        "prompt": "What have researchers and law enforcement agencies tried to do?",
        "options": {
            "A": "Build a machine that can detect lies.",
            "B": "Develop a magnetic brain scanner.",
            "C": "Test the credibility of court evidence.",
            "D": "Win people's complete trust in them.",
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。设题要点为主体举措引出处。首段末句说：“researchers and law enforcement agencies have tried to build a machine that will do the same thing.”其中 the same thing 回指上句 tell with complete confidence when someone is telling a lie，义同选项中的 detect lies。因此答案为 A)。B) 借马萨诸塞州一家公司使用 magnetic brain scans 干扰，但那是该公司的行为，并非题干所问；C) 用 use in courts、credible proof 捏造，且「法庭证据」涵盖面过广；D) 利用 complete、telling the truth 干扰，文章通篇聚焦「如何分辨谎言」，未提及赢取他人信任。",
    },
    17: {
        "prompt": "How do many brain scientists respond to the Massachusetts company's so-called technological breakthrough?",
        "options": {
            "A": "They are optimistic about its potential.",
            "B": "They are sceptical of its reliability.",
            "C": "They think it is but business promotion.",
            "D": "They celebrate it with great enthusiasm.",
        },
        "answer": "B",
        "explanation": "【精析】细节概括题。设题要点为引出多个主体态度处。第三段说：“You'll not find many brain scientists celebrating this breakthrough...the ability of their machine to detect deception has not provided credible proof.”B) 概括了脑科学家不认同该突破、因其缺乏可靠证据的态度。因此答案为 B)。A) 借 optimistic 干扰，但这是马萨诸塞州公司的态度；C) 从脑科学家不认可的态度过度推断而来，文中并无信息支撑；D) 与「赞美这项突破的脑科学家不多」直接相悖。",
    },
    18: {
        "prompt": "What does the speaker think of using a high-tech test to determine whether a person is telling the truth?",
        "options": {
            "A": "It is not to be trusted at all.",
            "B": "It does not sound economical.",
            "C": "It may intrude into people's privacy.",
            "D": "It may lead to overuse in court trials.",
        },
        "answer": "A",
        "explanation": "【精析】细节推断题。设题要点为结尾发表观点处。演讲者说：“A high-tech test that can tell when a person is not telling the truth sounds too good to be true. And when something sounds too good to be true, it usually is.”并在末段指出使用机器识骗存在诸多问题，A) 正确概括了这一立场。因此答案为 A)。B)「测谎技术是否经济」在文中没有提及；C) 利用 brain scans 与 matching behavior to brain activity 干扰，文中焦点不在「隐私问题」；D) 从演讲者质疑测谎技术的态度中臆断「技术一引进便会被滥用」，文中并无信息支撑。",
    },
    19: {
        "prompt": "What does the speaker say about the island of Makelua?",
        "options": {
            "A": "Most of its residents speak several languages.",
            "B": "Some of its indigenous languages are dying out.",
            "C": "Each village there speaks a totally different language.",
            "D": "Its languages have interested researchers the world over.",
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。设题要点为语义转折处。首段说：“Yet the residents of each village speak a completely different language.”C) 与之同义复现。因此答案为 C)。A) 从「所有参会者都是该岛岛民、说 16 种语言」过度推出「大部分岛民每个人都会说几种语言」；B) 利用 indigenous languages 臆断「一些土著语言正在消亡」，原文并未谈及该信息；D) 将「我们也可以对全球提出同样的问题」中的研究对象「全球语言状况」偷换为「全球研究者」，臆断出所有人都对岛上语言感兴趣。",
    },
    20: {
        "prompt": "What do we learn from the talk about languages in the world?",
        "options": {
            "A": "They are spread randomly across the world.",
            "B": "Some are more difficult to learn than others.",
            "C": "More are found in tropical regions than in the mild zones.",
            "D": "They enrich and impact each other in more ways than one.",
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。设题要点为举例处。第二段说：“far more languages are found in tropical regions than in the mild zones.”C) 复现这一表述。因此答案为 C)。A) 与「这些语言并非随意分布在地球上」相悖；B) 对热带与温带语言种类的比较偷换概念，原文意在说明分布不均衡，与语言难易度无关；D) 利用惯常认知「不同语言会相互影响」干扰，但文中无信息支撑。",
    },
    21: {
        "prompt": "What have the diverse team of researchers found about the previous studies on language diversity?",
        "options": {
            "A": "They used different methods to collect and analyze data.",
            "B": "They identified distinct patterns of language distribution.",
            "C": "Their conclusions do not correspond to their original hypotheses.",
            "D": "There is no conclusive account for the cause of language diversity.",
        },
        "answer": "D",
        "explanation": "【精析】细节概括题。设题要点为研究结果引出处。末段说：“The results varied a lot from one study to another, and no clear patterns emerged.”D) 是对研究内容与研究发现的合理概括，其中 no conclusive account 对应 The results varied a lot 与 no clear patterns。因此答案为 D)。A) 利用个别词汇 different、methodological 与「收集和分析数据」的常识捏造而来；B) 利用 language、distinct、patterns 干扰，与「没有清晰的模式出现」相悖；C) 属张冠李戴——作出该假定（假定语言多样性与历史、文化差异等有关）的并非该多元化研究团队，而是「大多数人」。",
    },
    22: {
        "prompt": "What do the surveys show about America according to the speaker?",
        "options": {
            "A": "Its middle-class is disappearing.",
            "B": "Its wealth is rationally distributed.",
            "C": "Its population is rapidly growing.",
            "D": "Its cherished dream is coming true.",
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。设题要点为调查结果说明处。首段说：“Today's demographics show that the middle-class is disappearing.”A) 与之同义复现。因此答案为 A)。B) 与「现如今贫富差距比以往任何时候都大」所传递的「财富分配不合理」相悖；C) 利用 population 与数据对比 1% VS 90% 干扰，该数据实际用于说明贫富比例悬殊；D) 与反问句所暗示的「梦想正在破灭」及调查结果相悖。",
    },
    23: {
        "prompt": "What did Americans use to believe?",
        "options": {
            "A": "Success was but a dream without conscientious effort.",
            "B": "They could realize their dreams through hard work.",
            "C": "A few dollars could go a long way.",
            "D": "Wealth was shared by all citizens.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为今昔对比处。首段末说：“Once upon a time, Americans thought that if they worked hard enough...they would be rewarded with success.”B) 是其同义表述。因此答案为 B)。A) 虽包含「成功、努力」要素，但强调「未必努力了就一定成功」，与美国梦的核心「有付出就一定有回报」不符；C) 将「些许同情心能产生深远影响」窜改为「少量钱可以大有作为」，且这属于讲话者的呼吁而非美国人过去的观点；D) 由文中提及的现状「贫富/收入差距问题」臆测而来，文中并无支撑信息。",
    },
    24: {
        "prompt": "What do low-income people aspire to?",
        "options": {
            "A": "Better working conditions.",
            "B": "Better-paying jobs.",
            "C": "High social status.",
            "D": "Full employment.",
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。设题要点为设问处。演讲者说：“if you ask low-income people what's the one thing that will change their life, they'll say a full-time job. That's all they aspire to.”D) 精准复现这一表述。因此答案为 D)。A)、B) 由「兼职人员只能领到法定最低工资、无医疗保健及其他福利」分别臆测对应措辞，但演讲者明确转述的是「一份全职工作」；C) 由全篇的社会地位议题臆断，原文并未提及低收入群体对更高社会地位的追求。",
    },
    25: {
        "prompt": "What do businesses do to increase their revenues?",
        "options": {
            "A": "Reduce the administrative costs.",
            "B": "Adopt effective business models.",
            "C": "Hire part-time employees only.",
            "D": "Make use of the latest technology.",
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。设题要点为因果说明处。第三段说：“Businesses, in order to boost profits, hire employees as part-time workers only.”C) 精准复现这一做法。因此答案为 C)。A)、B)、D) 均属企业在提高效率方面的常见做法，但本段并未将其与增加收入相联系，原文所明确给出的企业盈利手段只有「仅雇用兼职员工」这一项。",
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
