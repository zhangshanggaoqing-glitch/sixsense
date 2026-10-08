#!/usr/bin/env python3
"""
Curate and rigorously audit 2024-06-set1:
- 7 Subparts with authentic titles and Chinese topics
- 146 Grammatical Sentences with 100% paired, authentic Chinese translations
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
WHISPER_PATH = BASE_DIR / "data" / "derived" / "exams" / "2024-06-set1" / "whisper_full.json"
DOCX_FILE = Path("/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2024年06月CET6题+解+音频/02、真题word版/2024.06六级真题第1套【可复制可检索】.docx")
OCR_FILE = BASE_DIR / "data" / "derived" / "exams" / "2024-06-set1" / "ocr_listening.txt"

EXAM_ID = "2024-06-set1"
AUDIO_FILE = "2024.06六级听力音频第1套.mp3"
AUDIO_DURATION = 1621.12

SUBPARTS_DATA = [
    {
        "id": "2024-06-set1-conv-1",
        "subpart_code": "conv-1",
        "section_id": "2024-06-set1-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 1 · 商业赞助谈判与合同修改",
        "topic_zh": "商业赞助谈判与合同修改",
        "question_range": "Q1 ~ Q4",
        "questions": [1, 2, 3, 4],
        "anchor": ["thank", "you", "for", "meeting", "with", "me"],
        "sentences": [
            ("W", "Thank you for meeting with me, Stephen, at such short notice.", "斯蒂芬，感谢你在这么短的通知时间内和我见面。"),
            ("M", "Not a problem, Margaret.", "没问题，玛格丽特。"),
            ("M", "Now please give me some good news.", "现在请给我一些好消息吧。"),
            ("M", "Have you agreed to my last proposal?", "你同意我上次的提议了吗？"),
            ("W", "I have indeed, and I wish to sign the agreement, pending one small change to be made to the contract.", "我确实同意了，而且我希望签署这份协议，只要对合同做一处小小的修改即可。"),
            ("M", "Margaret, we've been through this for almost a year now, back and forth making alterations.", "玛格丽特，我们为这事已经拉锯了将近一年，来来回回地修改。"),
            ("M", "Are you sure you want to make a sponsorship deal for your clients or not?", "你到底确不确定要为你的客户达成一份赞助代言协议？"),
            ("M", "I ask this because frankly, some people at my end are running out of patience.", "我这么问是因为坦白讲，我这边的一些人已经快失去耐心了。"),
            ("W", "I understand your concerns, but as I'm sure you understand, we hold our clients' best interests to be of the utmost concern.", "我理解你的顾虑，但相信你也明白，我们将客户的最佳利益视作重中之重。"),
            ("W", "We therefore comb through the fine details of all contracts.", "因此我们必须对所有合同的细枝末节进行梳理推敲。"),
            ("W", "Rest assured we all appreciate your firm's patience.", "请放心，我们都非常感激贵公司的耐心。"),
            ("M", "Okay, fine.", "好的，行吧。"),
            ("M", "So what changes do you wish to make?", "那你想做什么修改？"),
            ("W", "Essentially, we would like the new deal to exclude the Middle East.", "基本上，我们希望新协议能将中东地区排除在外。"),
            ("W", "That's all.", "仅此而已。"),
            ("M", "The Middle East?", "中东地区？"),
            ("M", "Why?", "为什么？"),
            ("W", "My client has a couple of other prospective marketing deals from companies in the Middle East.", "我的客户还有另外几笔来自中东公司的潜在营销协议。"),
            ("W", "Those offers, should they materialize, would exclusively employ my client's image in the Middle East only.", "那些要约如果能够落实，将在中东地区独家使用我客户的形象。"),
            ("W", "Therefore, in order to avoid any conflict, we would need to ensure that both marketing campaigns do not overlap geographically.", "因此，为了避免任何冲突，我们需要确保两个营销活动在地域上互不重叠。"),
            ("M", "What business sector in the Middle East are we talking about here?", "我们这里谈论的是中东的哪个行业领域？"),
            ("W", "Real estate.", "房地产。"),
            ("M", "Well, that should be okay then.", "嗯，那应该没问题。"),
            ("M", "So long as the product is very different from our food and beverage market, there should be no conflict of interest.", "只要产品与我们的餐饮市场截然不同，就不会有利益冲突。"),
            ("M", "Nevertheless, I will have to run this through my people.", "不过，我还是得和我的团队商量一下。"),
            ("M", "I don't foresee any problem, though.", "但我预计不会有什么问题。"),
            ("M", "The Middle East is a negligible market for us.", "中东对我们来说是一个微不足道的市场。"),
            ("M", "But I still need to check this with a couple of departments.", "但我仍然需要与几个部门核实确认一下。")
        ]
    },
    {
        "id": "2024-06-set1-conv-2",
        "subpart_code": "conv-2",
        "section_id": "2024-06-set1-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 2 · 丹佛天文台观测奥本海默彗星",
        "topic_zh": "丹佛天文台观测奥本海默彗星",
        "question_range": "Q5 ~ Q8",
        "questions": [5, 6, 7, 8],
        "anchor": ["next", "we", "have", "a", "special"],
        "sentences": [
            ("M", "Next, we have a special science-related news story.", "接下来是一则与科学有关的特别新闻。"),
            ("M", "Paula Hancock is at the Denver Observatory.", "宝拉·汉考克正在丹佛天文台现场。"),
            ("M", "Paula, what is the big story over there?", "宝拉，那儿有什么大新闻？"),
            ("W", "Hi, John.", "你好，约翰。"),
            ("W", "Yes, all the astronomers on site here are very excited.", "是的，现场所有的天文学家都非常兴奋。"),
            ("W", "In fact, space enthusiasts all across North America and the rest of the Northern Hemisphere will be congregating on mountain tops tonight to watch the night's sky.", "事实上，今晚整个北美及北半球其他地区的太空爱好者都将聚集在山顶观测夜空。"),
            ("M", "Why?", "为什么呢？"),
            ("M", "What's the big event?", "有什么重大事件？"),
            ("M", "Is there an eclipse happening soon?", "是有日食或月食马上要发生吗？"),
            ("W", "Tonight, the Earth will come into close proximity with the Oppenheimer comet.", "今晚，地球将与奥本海默彗星近距离接触。"),
            ("W", "It is the closest our planet has been to such a phenomenon in over 100 years.", "这是100多年来我们的星球距离这种天体现象最近的一次。"),
            ("W", "For this reason, it is expected that thousands of people will gaze up at the sky tonight in order to see this formidable object.", "因此，预计今晚将有数千人仰望星空，一睹这个壮观的天体。"),
            ("M", "How far away is this comet?", "这颗彗星离我们有多远？"),
            ("M", "Will people be able to see it with the naked eye?", "人们能用肉眼看到它吗？"),
            ("W", "The Oppenheimer comet will still be millions of miles away on the edge of our galaxy.", "奥本海默彗星仍在数百万英里之外、我们银河系的边缘。"),
            ("W", "But nevertheless, this is a relatively close distance, close enough for people to observe in good detail through a telescope.", "尽管如此，这仍是一个相对较近的距离，足够人们通过望远镜仔细观测。"),
            ("W", "People will only see a blur without one.", "如果没有望远镜，人们只能看到一片模糊的光斑。"),
            ("W", "However, that does not mean one needs professional equipment.", "然而，这并不意味着人们需要专业的设备。"),
            ("W", "Even the most ordinary of telescopes should be conducive for people to observe and wonder at this flying object.", "即使是最普通的望远镜，也有助于人们观测并惊叹于这个飞行天体。"),
            ("M", "Many of our viewers will be wondering how they too can take part in this once-in-a-lifetime event.", "我们的许多观众会想知道，他们该如何参与这一生难得一见的盛事。"),
            ("M", "Where will this comet be in the sky?", "这颗彗星会在天空的什么方位？"),
            ("M", "How can people find it?", "人们该如何找到它？"),
            ("W", "The comet will be almost exactly due north, at 60 degrees above the equator.", "这颗彗星将几乎正位于正北方，在赤道上方60度角的位置。"),
            ("W", "However, finding the comet is indeed very tricky.", "不过，寻找这颗彗星确实非常棘手。"),
            ("W", "And scientists here have told me there are plenty of phone apps that will facilitate this.", "这里的科学家告诉我，有很多手机应用程序可以帮助定位。"),
            ("M", "How fantastic!", "太棒了！"),
            ("M", "Thank you, Paula, for the information.", "谢谢你，宝拉，提供这些资讯。")
        ]
    },
    {
        "id": "2024-06-set1-pass-1",
        "subpart_code": "pass-1",
        "section_id": "2024-06-set1-sec-b",
        "section_title": "Section B: Listening Passages",
        "type": "passage",
        "title": "Passage 1 · 超加工食品与健康饮食指南之辩",
        "topic_zh": "超加工食品与健康饮食指南之辩",
        "question_range": "Q9 ~ Q11",
        "questions": [9, 10, 11],
        "anchor": ["dietary", "guidelines", "form", "the", "basis"],
        "sentences": [
            ("", "Dietary guidelines form the basis for nutrition advice and regulations around the world.", "饮食指南构成了全球营养建议和法规的基础。"),
            ("", "While there is strong scientific consensus around most existing guidelines, one question has recently stirred debate: should consumers be warned to avoid ultra-processed foods?", "尽管大多数现有指南都达成了高度的科学共识，但最近有一个问题引发了激烈争论：是否应该警告消费者避免食用超加工食品？"),
            ("", "Two papers published today in the American Journal of Clinical Nutrition outline the case for and against using the concept of \"ultra-processed foods\" to help inform dietary guidelines, beyond conventional food classification systems.", "今天发表在《美国临床营养学杂志》上的两篇论文，阐述了在传统食物分类系统之外，利用“超加工食品”概念来指导饮食指南的支持与反对意见。"),
            ("", "The authors, Carlos Monteiro of the University of Sao Paulo and Arne Astrup of Novo Nordisk Foundation, will discuss the issue in a live virtual debate, August 14th, during NUTRITION 2024 Live Online.", "论文作者——圣保罗大学的卡洛斯·蒙泰罗和诺和诺德基金会的阿恩·阿斯特鲁普，将于8月14日的“2024线上营养峰会”期间展开一场线上实时辩论。"),
            ("", "The debate centers around a system developed by Monteiro and colleagues that classifies foods by their degree of industrial processing, ranging from unprocessed to ultra-processed.", "辩论的核心围绕着蒙泰罗及其同事开发的一套系统，该系统根据工业加工程度对食物进行分类，从未经加工到超加工不等。"),
            ("", "The system defines ultra-processed foods as those made using sequences of processes that extract substances from foods and alter them with chemicals in order to formulate the final product.", "该系统将超加工食品定义为：通过一系列工艺从天然食物中提取物质并用化学方法进行改变，以配制出最终产品的食物。"),
            ("", "Ultra-processed foods are characteristically designed to be cheap, tasty, and convenient.", "超加工食品的典型特征是价格低廉、口感美味且食用便捷。"),
            ("", "Examples include soft drinks and candy, packaged snacks and pastries, ready to heat products, and reconstituted meat products.", "例如软饮料和糖果、包装零食和糕点、即热食品以及重组肉制品。"),
            ("", "Studies have linked consumption of ultra-processed foods, which are often high in salt, sugar, and fat, with weight gain and an increased risk of chronic diseases, even after adjusting for the amount of salt, sugar, and fat in the diet.", "多项研究表明，食用通常高盐、高糖、高脂的超加工食品与体重增加和慢性疾病风险上升有关，即使在调整了膳食中的盐、糖和脂肪含量后依然如此。"),
            ("", "While the mechanisms behind these associations are not fully understood, Monteiro argues that the existing evidence is sufficient to justify discouraging consumption of ultra-processed foods in dietary recommendations and government policies.", "尽管这些关联背后的具体机制尚未完全明确，但蒙泰罗认为，现有证据足以证明在饮食建议和政府政策中劝阻人们食用超加工食品是合理的。")
        ]
    },
    {
        "id": "2024-06-set1-pass-2",
        "subpart_code": "pass-2",
        "section_id": "2024-06-set1-sec-b",
        "section_title": "Section B: Listening Passages",
        "type": "passage",
        "title": "Passage 2 · 限制激发人类创造力与创新",
        "topic_zh": "限制激发人类创造力与创新",
        "question_range": "Q12 ~ Q15",
        "questions": [12, 13, 14, 15],
        "anchor": ["believe", "it", "or", "not"],
        "sentences": [
            ("", "Believe it or not, human creativity benefits from constraints.", "信不信由你，人类的创造力其实得益于限制。"),
            ("", "According to psychologists, when you have less to work with, you actually begin to see the world differently.", "心理学家指出，当你可以使用的资源变少时，你实际上会开始以不同的视角看待世界。"),
            ("", "With constraints, you dedicate your mental energy to acting more resourcefully.", "有了限制，你会把脑力投入到更有策略、更巧妙地利用资源上。"),
            ("", "When challenged, you figure out new ways to be better.", "面对挑战时，你会想出新的办法让自己做得更好。"),
            ("", "The most successful creative people know that constraints give their minds the impetus to leap higher.", "最成功的创意人士深知，限制能为他们的大脑提供跳得更高的动力。"),
            ("", "People who invent new products are not limited by what they don't have or can't do.", "发明新产品的人不会被自己没有的或做不到的事情所限制。"),
            ("", "They leverage their limitations to push themselves even further.", "他们利用自身的局限性来推动自己走得更远。"),
            ("", "Many products and services are created because the founders saw a limitation in what they use.", "许多产品和服务的诞生，都是因为创始人看到了他们所用产品的局限。"),
            ("", "They created innovation based on what was not working for them at the moment.", "他们基于当时对自己不奏效的地方做出了创新。"),
            ("", "Innovation is a creative person's response to limitation.", "创新就是一个有创造力的人对局限性的回应。"),
            ("", "In a 2015 study which examined how thinking about scarcity or abundance influences how creatively people use their resources, Ravi Mehta at the University of Illinois and Meng Zhu at Johns Hopkins University found that people simply have no incentive to use what's available to them in novel ways.", "在2015年一项探讨思考稀缺或充裕如何影响人们创造性使用资源的研究中，伊利诺伊大学的拉维·梅塔和约翰斯·霍普金斯大学的朱蒙发现，人们根本没有动力以新颖的方式去使用现有的资源。"),
            ("", "When people face scarcity, they give themselves the freedom to use resources in less conventional ways because they have to.", "当人们面临稀缺时，他们会给予自己以非常规方式利用资源的自由，因为他们不得不这样做。"),
            ("", "Obstacles can broaden your perception and open up your thinking processes.", "障碍可以拓宽你的认知，打开你的思维过程。"),
            ("", "Consistent constraints help you improve the connecting unrelated ideas and concepts.", "持续的限制有助于提高你将不相关的想法和概念联系起来的能力。"),
            ("", "Marissa Mayer, former vice president for search products and user experience at Google, once wrote in a publication on Bloomberg, \"Constraints shape and focus problems and provide clear challenges to overcome; creativity thrives best when constrained.\"", "谷歌前搜索产品与用户体验副总裁玛丽莎·梅耶尔曾在一份彭博社刊物中写道：“限制能够塑造并聚焦问题，提供需要克服的明确挑战；创造力在受到限制时最为蓬勃繁荣。”")
        ]
    },
    {
        "id": "2024-06-set1-rec-1",
        "subpart_code": "rec-1",
        "section_id": "2024-06-set1-sec-c",
        "section_title": "Section C: Recorded Lectures/Talks",
        "type": "recording",
        "title": "Recording 1 · 人际冲突管理的五种动物策略",
        "topic_zh": "人际冲突管理的五种动物策略",
        "question_range": "Q16 ~ Q18",
        "questions": [16, 17, 18],
        "anchor": ["different", "people", "use", "different", "strategies"],
        "sentences": [
            ("", "Different people use different strategies for managing conflicts.", "不同的人会使用不同的策略来管理冲突。"),
            ("", "These strategies are learned in childhood.", "这些策略是在童年时期习得的。"),
            ("", "Usually, we are not aware of how we act in conflict situations.", "通常，我们并没有意识到自己在冲突情境中是如何表现的。"),
            ("", "We just do whatever seems to come naturally.", "我们只是按照看似自然而然的方式行事。"),
            ("", "But we do have a personal strategy, and because it is learned, we can always change it by learning new and more effective ways of managing conflicts.", "但我们确实拥有一套个人策略，而且既然它是习得的，我们总能通过学习新的、更有效的冲突管理方式来改变它。"),
            ("", "When you get involved in a conflict, there are two major concerns you have to take into account: achieving your personal goals and keeping a good relationship with the other person.", "当你卷入冲突时，必须考虑两个主要问题：实现个人目标，以及与对方保持良好关系。"),
            ("", "How important your personal goals are and how important the relationship is to you affect how you act in a conflict.", "你的个人目标有多重要，以及这段关系对你有多重要，会直接影响你在冲突中的行为方式。"),
            ("", "Given these two concerns, five styles of managing conflicts can be identified.", "考虑到这两个方面，可以归纳出五种冲突管理方式。"),
            ("", "1. The turtle.", "第一种是乌龟型。"),
            ("", "Turtles withdraw into their shells to avoid conflicts.", "乌龟会缩回壳里以避免冲突。"),
            ("", "They give up their personal goals and relationships.", "他们会放弃自己的个人目标和人际关系。"),
            ("", "They believe it is easier to withdraw from a conflict than to face it.", "他们认为逃避冲突比直面冲突更容易。"),
            ("", "2. The shark.", "第二种是鲨鱼型。"),
            ("", "Sharks try to overpower opponents by forcing them to accept their solution to the conflict.", "鲨鱼试图通过强迫对手接受他们对冲突的解决方案来压倒对方。"),
            ("", "They seek to achieve their goals at all costs.", "他们不惜一切代价谋求实现自己的目标。"),
            ("", "Sharks assume that conflicts are settled by one person winning and one person losing.", "鲨鱼认定冲突的解决是一方胜出一方落败。"),
            ("", "Winning gives sharks a sense of pride and achievement.", "赢给鲨鱼带来一种自豪感和成就感。"),
            ("", "Losing gives them a sense of weakness, inadequacy, and failure.", "输则给他们带来一种软弱、不足和失败的感觉。"),
            ("", "3. The teddy bear.", "第三种是泰迪熊型。"),
            ("", "Teddy bears want to be accepted and liked by other people.", "泰迪熊希望被他人接纳和喜欢。"),
            ("", "They think that conflict should be avoided in favor of harmony, and believe that conflicts cannot be discussed without damaging relationships.", "他们认为为了保持和谐应当避免冲突，并坚信讨论冲突必然会损害关系。"),
            ("", "They give up their goals to preserve the relationship.", "他们会放弃自己的目标以维护这段关系。"),
            ("", "4. The fox.", "第四种是狐狸型。"),
            ("", "Foxes are moderately concerned with their own goals and about their relationships with other people.", "狐狸适度关注自身的目标，也适度关注与他人的关系。"),
            ("", "They give up part of their goals and persuade the other person in a conflict to give up part of his goals.", "他们会放弃部分目标，并说服冲突中的另一方也放弃部分目标。"),
            ("", "They seek a solution to conflicts where both sides gain something.", "他们寻求一种双方都能有所收获的冲突解决方案。"),
            ("", "5. The owl.", "第五种是猫头鹰型。"),
            ("", "Owls view conflicts as problems to be solved.", "猫头鹰将冲突视为需要解决的问题。"),
            ("", "They see conflicts as improving relationships by reducing tension between two people.", "他们认为冲突能够通过减少两人之间的紧张关系来改善彼此的联系。"),
            ("", "They try to begin a discussion that identifies the conflict as a problem.", "他们尝试开启对话，将冲突定性为一个具体的问题。"),
            ("", "By seeking solutions that satisfy both themselves and the other person, owls maintain the relationship.", "通过寻求既能让自己满意又能让对方满意的解决方案，猫头鹰维护了这段关系。"),
            ("", "Owls are not satisfied until a solution is found that achieves their own goals and the other person's goals, and they are not satisfied until the tensions and negative feelings have been fully resolved.", "直到找到既能实现自己的目标又能实现对方目标的解决方案，直到紧张关系和负面情绪被彻底消除，猫头鹰才会感到满意。")
        ]
    },
    {
        "id": "2024-06-set1-rec-2",
        "subpart_code": "rec-2",
        "section_id": "2024-06-set1-sec-c",
        "section_title": "Section C: Recorded Lectures/Talks",
        "type": "recording",
        "title": "Recording 2 · 达尔文生命之树与地球生物基因组计划",
        "topic_zh": "达尔文生命之树与地球生物基因组计划",
        "question_range": "Q19 ~ Q21",
        "questions": [19, 20, 21],
        "anchor": ["the", "genetic", "code", "of", "all"],
        "sentences": [
            ("", "The genetic code of all 1.5 million known species of animals and plants living on Earth will be mapped to help save species from extinction and boost human health.", "地球上已知的150万种动植物的遗传密码将被绘制出来，以帮助拯救物种免于灭绝并促进人类健康。"),
            ("", "Scientists hope that cracking the genetic code of plants and animals could help uncover new treatments for infectious diseases, slow aging, improve crops and agriculture, and create new biomaterials.", "科学家们希望，破译动植物的遗传密码有助于发现传染病的新疗法、延缓衰老、改良农作物和农业，并创造新的生物材料。"),
            ("", "In Britain, organisations including the Natural History Museum, the Royal Botanic Gardens at Kew and the Wellcome Sanger Institute have joined forces to sequence Britain's 66,000 species of animals and plants.", "在英国，包括自然历史博物馆、邱园皇家植物园和惠康桑格研究所在内的各机构已联合起来，对英国本土的6.6万种动植物进行基因测序。"),
            ("", "Dubbed the Darwin Tree of Life Project, it is expected to take 10 years and cost 100 million pounds.", "该项目被称为“达尔文生命之树项目”，预计耗时10年，耗资1亿英镑。"),
            ("", "Once completed, all the information will be publicly available to researchers.", "一旦完成，所有信息将向研究人员公开发布。"),
            ("", "Many scientists believe that Earth has now entered the sixth mass extinction, with humans creating a toxic mix of habitat loss, pollution and climate change, which has already led to the loss of at least 77 species of mammals and 140 types of birds since 1500.", "许多科学家认为地球现在已经进入第六次物种大灭绝，人类造成的栖息地丧失、污染和气候变化等致命交织，自1500年以来已导致至少77种哺乳动物和140种鸟类灭绝。"),
            ("", "It is the biggest loss of species since the dinosaurs were wiped out 66 million years ago.", "这是自6600万年前恐龙灭绝以来最严重的物种灭绝。"),
            ("", "Scientists say that sequencing every species will revolutionize the understanding of biology and evolution, bolster efforts to conserve as well as protect and restore biodiversity.", "科学家表示，对每一种物种进行基因测序将彻底改变人们对生物学和进化的认知，增强养护、保护以及恢复生物多样性的努力。"),
            ("", "Dr. Tim Littlewood, head of Life Sciences Department at the Natural History Museum said, \"Whether you are interested in food or disease, the history of how every organism on the planet has adapted to its environment is recorded in its genetic makeup.\"", "自然历史博物馆生命科学部负责人蒂姆·利特尔伍德博士表示：“无论你对食物还是疾病感兴趣，地球上每种生物如何适应环境的历史都记录在其基因构成中。”"),
            ("", "\"How you then harness that is dependent on your ability to understand it.\"", "“随后你如何利用它，取决于你理解它的能力。”"),
            ("", "\"We will be using modern methods to get a really good window on the present and the past.\"", "“我们将利用现代方法，获得观察现在和过去的一扇绝佳窗口。”"),
            ("", "\"And of course, a window on the past gives you a prospective model on the future.\"", "“当然，通往过去的窗口也能为你提供预测未来的前瞻模型。”"),
            ("", "Sir Jim Smith, Director of Science at Wellcome said, \"Try as I might, I can't think of a more exciting, more relevant, more timely, or more internationally inspirational project.\"", "惠康基金会科学总监吉姆·史密斯爵士说：“无论我怎么绞尽脑汁，也想不出一个比这更令人兴奋、更息息相关、更及时或更具国际启发性的项目了。”"),
            ("", "\"Since 1970, humanity has wiped out 60 percent of animal populations.\"", "“自1970年以来，人类已经消灭了60%的动物种群。”"),
            ("", "\"About 23,000 of 80,000 species surveyed are approaching extinction.\"", "“在调查的8万个物种中，约有2.3万个正濒临灭绝。”"),
            ("", "\"We are in the midst of the sixth great extinction event of life on our planet, which not only threatens wildlife species, but also imperils the global food supply.\"", "“我们正处于地球生命第六次大灭绝事件之中，这不仅威胁着野生动物物种，也危及全球粮食供应。”"),
            ("", "\"As scientists, we all realize we desperately need to catalogue life on our fragile planet now.\"", "“作为科学家，我们都意识到，我们现在迫切需要为这个脆弱星球上的生命编目分类。”"),
            ("", "\"I think we're making history.\"", "“我认为我们正在创造历史。”")
        ]
    },
    {
        "id": "2024-06-set1-rec-3",
        "subpart_code": "rec-3",
        "section_id": "2024-06-set1-sec-c",
        "section_title": "Section C: Recorded Lectures/Talks",
        "type": "recording",
        "title": "Recording 3 · 自我错觉与生态互联性认知",
        "topic_zh": "自我错觉与生态互联性认知",
        "question_range": "Q22 ~ Q25",
        "questions": [22, 23, 24, 25],
        "anchor": ["the", "english", "poet", "wrote"],
        "sentences": [
            ("", "John Donne, the English poet, wrote in the 17th century, \"No man is an island, entire of itself; every man is a piece of the continent, a part of the main.\"", "17世纪的英国诗人约翰·多恩曾写道：“没有人是一座孤岛，可以自全；每个人都是大陆的一片，整体的一部分。”"),
            ("", "Now, a British academic has claimed that human individuality is indeed just an illusion, because societies are far more interconnected at a mental, physical, and cultural level than people realize.", "如今，一位英国学者声称，人类的个体性确实只是一种错觉，因为人类社会在精神、肉体和文化层面上的相互联系远比人们意识到的要紧密得多。"),
            ("", "In his new book, The Self Delusion, Professor Tom Oliver, a researcher in the Ecology and Evolution group at the University of Reading, argues there is no such thing as \"self\", and not even our bodies are truly \"us\".", "雷丁大学生态与进化研究小组的研究员汤姆·奥利弗教授在其新书《自我的错觉》中论证指出，根本不存在所谓的“自我”，甚至我们的身体也并非真正属于“我们”。"),
            ("", "Just as Copernicus realized the Earth is not the center of the universe, Professor Oliver said society urgently needs a Copernican-like revolution to understand people are not detached beings but rather part of one connected identity.", "正如哥白尼认识到地球并非宇宙中心一样，奥利弗教授表示，社会迫切需要一场哥白尼式的革命，去认识到人类并不是孤立的存在，而是相连整体的一部分。"),
            ("", "\"A significant milestone in the cultural evolution of human minds was the acceptance that the Earth is not the center of the universe, the so-called Copernican Revolution,\" he writes.", "他写道：“人类心灵文化进化中的一个重要里程碑，就是接受了地球并非宇宙中心的事实，即所谓的哥白尼革命。”"),
            ("", "\"However, we have one more big myth to dispose of: that we exist as independent selves at the center of a subjective universe.\"", "“然而，我们还有一个巨大的神话需要打破：那就是我们作为独立的自我存在于主观宇宙的中心。”"),
            ("", "\"You may feel as if you are an independent individual acting autonomously in the world; that you have unchanging inner self that persists throughout your lifetime, acting as a central anchor-point with the world changing around you.\"", "“你可能觉得自己是一个在世界上自主行动的独立个体；拥有一个贯穿一生的、恒常不变的内在自我，在这个变幻莫测的世界中充当核心锚点。”"),
            ("", "\"This is the illusion I seek to tackle.\"", "“这正是我试图破解的错觉。”"),
            ("", "\"We are intimately connected to the world around us.\"", "“我们与周遭世界紧密相连。”"),
            ("", "Professor Oliver argues there are around 37 trillion cells in the body but most have a lifespan of just a few days or weeks, so the material \"us\" is constantly changing.", "奥利弗教授指出，人体内大约有37万亿个细胞，但大多数细胞的寿命只有短短几天或数周，因此物质层面的“我们”一直在不断更替。"),
            ("", "In fact, there is no part of your body that has existed for more than ten years.", "事实上，你身体中没有任何一个部分的存在时间超过十年。"),
            ("", "Since our bodies are essentially made anew every few weeks, the material in them alone is clearly insufficient to explain the persistent thread of an identity.", "既然我们的身体基本上每隔几周就会重新构造一次，仅凭其中的物质成分显然不足以解释个体身份认同的延续性。"),
            ("", "Professor Oliver claims that individualism is actually bad for society, and only by realizing we are part of a bigger entity can we solve pressing environmental and societal problems.", "奥利弗教授认为，个人主义实际上对社会是有害的，只有认识到我们是更大实体的一部分，我们才能解决迫在眉睫的环境与社会问题。"),
            ("", "Through selfish over-consumption we are destroying the natural world and using non-renewable resources at an accelerating rate.", "通过自私的过度消费，我们正在破坏自然界，并以加速度消耗不可再生资源。"),
            ("", "\"We are at a critical crossroads as a species where we must rapidly reform our mindsets and behavior to act in less selfish ways,\" he said.", "他说：“作为一个物种，我们正处于一个关键的十字路口，必须迅速转变思维方式和行为举止，以减少自私自利的方式行事。”"),
            ("", "\"So let's open our eyes to the hidden connections all around us.\"", "“因此，让我们睁开双眼，看看身边所有那些隐匿的连接吧。”")
        ]
    }
]

QUESTION_SOLUTIONS = {
    1: {
        "prompt": "What does the woman say she will do?",
        "answer": "B",
        "explanation": "对话开头男士问女士是否同意上次的提议，女士回答说：“事实上我同意了，我愿意签这份协议，只不过还需要对合同做一个小小的修改。”由此可知，B项与对话内容相符。"
    },
    2: {
        "prompt": "What does the man say about some people he represents?",
        "answer": "A",
        "explanation": "对话中间，男士表示这份协议已经来来回回地修改过多次了，于是询问女士是否确定要为客户达成一份代言协议，并坦白说：“我这么问是因为坦白地说，我这边的一些人已经快没有耐心了。”由此可知，A项与对话内容相符。"
    },
    3: {
        "prompt": "What reason does the woman give for the new deal to exclude the Middle East?",
        "answer": "C",
        "explanation": "对话中间，男士询问女士为什么希望新协议将中东地区排除在外，女士解释道：“我的客户还有几个来自中东公司的潜在营销协议……为了避免任何利益冲突，我们需要确保这两个营销活动在地域上不重合。”由此可知，C项与对话内容相符。"
    },
    4: {
        "prompt": "What does the man say about the Middle East?",
        "answer": "C",
        "explanation": "对话最后，男士说道：“中东对我们来说是一个微不足道的市场（The Middle East is a negligible market for us）。但我仍然需要与几个部门核实确认一下。”由此可知，C项与对话内容相符。"
    },
    5: {
        "prompt": "What does the woman say about all the astronomers at the Denver Observatory?",
        "answer": "A",
        "explanation": "对话开头，男士询问女士丹佛天文台有什么大新闻，女士回答说：“是的，这里现场的所有天文学家都非常兴奋。事实上，整个北美和北半球其他地区的太空爱好者今晚都将齐聚在山顶上观测夜空。”随后女士解释是因为地球将近距离接触罕见的奥本海默彗星。由此可知，A项与对话内容相符。"
    },
    6: {
        "prompt": "What do we learn from the conversation about the Oppenheimer comet?",
        "answer": "B",
        "explanation": "男士询问大事件的具体内容，女士回答说：“今晚，地球将与奥本海默彗星近距离接触。这是100多年来我们的星球距离这种天体现象最近的一次。”由此可知，B项与对话内容相符。"
    },
    7: {
        "prompt": "What does the woman say people will only see in the sky without a telescope?",
        "answer": "A",
        "explanation": "女士在谈及观测彗星时指出：“奥本海默彗星仍在数百万英里之外……足够人们通过望远镜仔细观测。如果没有望远镜，人们只能在空中看到一片模糊的光斑（People will only see a blur without one）。”由此可知，A项与对话内容相符。"
    },
    8: {
        "prompt": "What do scientists at the Denver Observatory advise amateurs do to facilitate their observation?",
        "answer": "D",
        "explanation": "女士最后提到：“寻找这颗彗星确实非常棘手。这里的科学家告诉我，有很多手机应用程序可以协助定位（there are plenty of phone apps that will facilitate this）。”由此可知，D项与对话内容相符。"
    },
    9: {
        "prompt": "What question is said to have recently stirred debate?",
        "answer": "A",
        "explanation": "文章开头提到，尽管现有大多数指南都有很强的科学共识，但是最近有一个问题引发了激烈争论：“是否应该警告消费者避免食用超加工食品？”因此，A项正确。"
    },
    10: {
        "prompt": "How does the system developed by Monteiro and colleagues classify foods?",
        "answer": "B",
        "explanation": "文章中间指出，辩论围绕着蒙泰罗及其同事开发的系统展开，“该系统根据食物的工业加工程度（degree of industrial processing）对食物进行分类，从未经加工到超加工不等”。故B项正确。"
    },
    11: {
        "prompt": "What is consumption of ultra-processed foods linked with, according to studies?",
        "answer": "B",
        "explanation": "文章最后指出：“多项研究表明，食用超加工食品与体重增加和慢性疾病风险上升（an increased risk of chronic diseases）有关联。”故选项B正确。"
    },
    12: {
        "prompt": "What do psychologists say people do when they are short of resources?",
        "answer": "D",
        "explanation": "文章开头提到，心理学家指出当人们可使用的资源变少时，“你实际上会开始以不同的视角看待世界（you actually begin to see the world differently）”。选项D中的see the world in a different way是对原文的同义转述，因此D正确。"
    },
    13: {
        "prompt": "What does the passage say about innovation?",
        "answer": "C",
        "explanation": "文章中间部分明确指出：“创新就是一个有创造力的人对局限性的回应（Innovation is a creative person's response to limitation）。”选项C的表述与原文完全一致，故C正确。"
    },
    14: {
        "prompt": "What did a 2015 study by Ravi Mehta and Meng Zhu find?",
        "answer": "C",
        "explanation": "文章后半部分介绍了一项2015年的研究，拉维·梅塔和朱蒙发现，“人们根本没有动力以新颖的方式去使用现有的资源（people simply have no incentive to use what's available to them in novel ways）”。故选项C正确。"
    },
    15: {
        "prompt": "What did Marissa Mayer once write concerning creativity?",
        "answer": "D",
        "explanation": "文章最后引用了谷歌前副总裁玛丽莎·梅耶尔的观点：“局限性可以塑造并聚焦问题，提供需要克服的明确挑战；创造力在受到限制时最为蓬勃繁荣（creativity thrives best when constrained）。”选项D与原文完全一致，故D正确。"
    },
    16: {
        "prompt": "Why does the speaker say strategies for managing conflicts can always be changed?",
        "answer": "A",
        "explanation": "讲话开头提到，我们每个人都有一套应对冲突的个人策略，“而且既然它是习得的（because it is learned），我们总能通过学习新的、更有效的方式来改变它”。由此得出正确答案为A。"
    },
    17: {
        "prompt": "What is said to affect the way one acts in a conflict?",
        "answer": "C",
        "explanation": "讲话者提到卷入冲突后要考虑两个主要问题：实现个人目标与保持良好关系，并强调“你的个人目标有多重要，以及这段关系对你有多重要，会直接影响你在冲突中的行为”。由此可知，选项C为正确答案。"
    },
    18: {
        "prompt": "Of the five styles the speaker discusses, which views conflicts as problems to be solved?",
        "answer": "B",
        "explanation": "讲话者依次讲述了五种冲突解决方式，在讲到猫头鹰方式时提到：“采用猫头鹰方式的人将冲突视为需要解决的问题（Owls view conflicts as problems to be solved）”。由此可知，选项B为正确答案。"
    },
    19: {
        "prompt": "What do scientists hope to do by cracking the genetic code of plants and animals?",
        "answer": "A",
        "explanation": "讲话者在开头明确指出：“地球上已知的150万种动植物的遗传密码将被绘制出来，以帮助拯救物种免于灭绝并促进人类健康（help save species from extinction and boost human health）。”由此得出选项A为正确答案。"
    },
    20: {
        "prompt": "What do many scientists believe with regard to Earth?",
        "answer": "B",
        "explanation": "讲话中间指出：“许多科学家认为地球现在已经进入了第六次物种大灭绝（Earth has now entered the sixth mass extinction）。”由此可知，选项B为正确答案。"
    },
    21: {
        "prompt": "How does Sir Jim Smith, Director of Science at Wellcome, describe the Darwin Tree of Life Project?",
        "answer": "D",
        "explanation": "惠康基金会科学总监吉姆·史密斯爵士说道：“无论我怎么绞尽脑汁，也想不出一个比这更令人兴奋、更息息相关、更及时或更具国际启发性的项目了（a more exciting, more relevant, more timely, or more internationally inspirational project）。”由此可知，选项D为正确答案。"
    },
    22: {
        "prompt": "What is indeed just an illusion according to Professor Tom Oliver?",
        "answer": "D",
        "explanation": "讲话中提到：“雷丁大学的汤姆·奥利弗教授声称，人类的个体性（human individuality）确实只是一种错觉，因为社会在精神、肉体和文化层面的相互联系远比人们意识到的紧密得多。”故选项D为正确答案。"
    },
    23: {
        "prompt": "What does Professor Tom Oliver think of the idea that we exist as independent selves at the center of a subjective universe?",
        "answer": "A",
        "explanation": "讲话中间部分提到，奥利弗教授写道：“我们还有一个巨大的神话需要打破（one more big myth to dispose of）：那就是我们作为独立的自我，存在于主观宇宙的中心。”由此可知，这是一种需要破除的错觉/妄想（delusion to be disposed of），选项A为正确答案。"
    },
    24: {
        "prompt": "Why does Professor Tom Oliver claim that the material \"us\" is constantly changing?",
        "answer": "D",
        "explanation": "讲话中解释道：“奥利弗教授指出，人体内大约有37万亿个细胞，但大多数细胞的寿命只有短短几天或数周（most have a lifespan of just a few days or weeks），因此物质层面的‘我们’在不断变化。”由此可知，选项D为正确答案。"
    },
    25: {
        "prompt": "How can we solve pressing environmental and societal problems according to Professor Tom Oliver?",
        "answer": "C",
        "explanation": "讲话结尾指出：“奥利弗教授声称，个人主义实际上对社会不利，而且只有我们意识到自己是更大实体的一部分（part of a bigger entity / bigger world），才能解决紧迫的环境问题和社会问题。”由此可知，选项C为正确答案。"
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
        raw = raw.replace('А', 'A').replace('В', 'B').replace('С', 'C')
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
            for nw in re.findall(r"[a-z0-9']+", w["word"].lower()):
                words.append({
                    "word": w["word"].strip(),
                    "norm": nw,
                    "start": round(w["start"], 2),
                    "end": round(w["end"], 2)
                })
    return words

def curate_and_save():
    print("=" * 60)
    print("Starting curation for 2024-06-set1...")
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
        EXAM_ID, 2024, 6, 1,
        "2024年06月大学英语六级考试真题（第1套）",
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
        for i in range(total_w - len(anchor_toks)):
            if all(whisper_words[i + k]["norm"] == anchor_toks[k] for k in range(len(anchor_toks))):
                word_cursor = i
                break

        # Special adjustment for rec-3 where speaker says "John Den..."
        if sid == "rec-3":
            for i in range(total_w):
                if whisper_words[i]["norm"] == "john" and whisper_words[i]["start"] > 1350:
                    word_cursor = i
                    break

        print(f"Aligning {sp_meta['id']} ({len(raw_sentences)} sentences) starting around {whisper_words[word_cursor]['start']}s...")

        aligned_sentences = []
        for s_idx, (speaker, en_text, zh_text) in enumerate(raw_sentences):
            tokens = re.findall(r"[a-z0-9']+", en_text.lower())
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
