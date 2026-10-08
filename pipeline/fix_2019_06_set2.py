#!/usr/bin/env python3
"""
Fine-tune and split all merged sentences in 2019-06-set2 into individual grammatical sentences,
each paired with its accurate Chinese translation.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from data_2019_06_set2 import SUBPARTS, QUESTIONS

# Subpart 1: C1
NEW_C1_SENTS = [
    ('W', "Wow, I would give anything to be more like Audrey Hepburn.", "哇，为了能更像奥黛丽·赫本，我愿意付出一切。"),
    ('M', "I never really understood why so many girls were such big fans of her.", "我始终没真正弄明白，为什么这么多女孩都是她的铁杆粉丝。"),
    ('M', "I mean, I've seen the famous films, Roman Holiday, Breakfast at Tiffany's and a few others, but I still don't fully get it.", "我是说，她那些著名的电影我大都看过——《罗马假日》《蒂凡尼的早餐》还有另外几部——可我还是不太明白。"),
    ('M', "Was she that great of an actress?", "她真有那么了不起吗？"),
    ('W', "Well, for me, my adoration goes beyond her movies.", "嗯，对我来说，我对她的喜爱早已超越了她演的电影。"),
    ('W', "She had such a classic elegance about her.", "她身上有一种古典的高贵优雅。"),
    ('W', "She was always so poised, in part because she spent years training as a ballet dancer before becoming an actress.", "她总是那样从容淡定，这在某种程度上是因为她在成为演员之前受过多年的芭蕾舞训练。"),
    ('M', "Why didn't she stick to dancing as a career?", "那她为什么没有把舞蹈坚持成职业呢？"),
    ('W', "It seems it was fate.", "似乎这是命运的安排。"),
    ('W', "She suffered from inadequate nutrition during the war, and therefore, a career as a professional dancer would have been too demanding on her body.", "战争时期她营养不良，因此职业舞者这一职业对她的身体来说负担太重了。"),
    ('W', "So she focused on acting instead.", "于是她转而专攻表演。"),
    ('W', "Roman Holiday was her first big break which made her a star.", "《罗马假日》让她首次大获成功，从此成为明星。"),
    ('M', "Was that the film that opened with her shopping for jewelry in New York city?", "就是那部以她在纽约挑选珠宝开场的电影吗？"),
    ('M', "You know, the scene she was wearing a black dress and dark sunglasses with a pearl necklace and long black gloves.", "你知道，就是那个她穿着黑裙子、戴着深色墨镜、佩戴珍珠项链和黑色长手套的场景。"),
    ('M', "I see the photo of her in that costume everywhere.", "那身打扮的照片我到处都看得见。"),
    ('W', "No, that one is Breakfast at Tiffany's.", "不，那一部是《蒂凡尼的早餐》。"),
    ('W', "That costume is often referred to as the most famous little black dress of all time.", "那身装束常被誉为有史以来最著名的小黑裙。"),
    ('W', "Her character in that film is very outgoing and charming, even though in real life, Audrey always described herself as shy and quiet.", "她在那部电影里饰演的角色非常外向迷人，尽管现实生活中，奥黛丽总是把自己描述为害羞而安静的。"),
    ('M', "So what did she do after her acting career?", "那她的演艺生涯结束后又做了什么呢？"),
    ('W', "She dedicated much of her life to helping children in need.", "她把大部分精力都投入到了帮助有需要的孩子上。"),
    ('W', "Her family received international aid during the war when she was growing up.", "她成长那段时间，战争期间她家里曾得到过国际援助。"),
    ('W', "I think that left a big impression on her.", "我想这件事在她心里留下了很深的印象。"),
    ('W', "That's where I got the idea to volunteer for children's charity next weekend.", "这也就是我萌生下周末去儿童慈善机构做志愿者念头的由来。"),
    ('M', "I'll join you.", "我跟你一起去。"),
    ('M', "I may not be as charming as Audrey Hepburn, but I'm all for supporting a good cause.", "我可能没奥黛丽·赫本那么有魅力，但我全力支持公益事业。")
]

# Subpart 2: C2
NEW_C2_SENTS = [
    ('W', "So, how is our presentation about the restructuring of the company coming along?", "那么，我们关于公司重组的汇报进展如何了？"),
    ('M', "Fine.", "挺好的。"),
    ('M', "I'm putting the finishing touches to it now.", "我正在做最后的润色。"),
    ('M', "But we'll have to be prepared for questions.", "不过我们得准备好应对大家的提问。"),
    ('W', "Yes, there's already a feeling that this is a top-down change.", "是的，已经有人感觉这是一次自上而下的变革了。"),
    ('W', "We really need to get everyone on board.", "我们真的需要让所有人都参与进来。"),
    ('M', "Well, there's been an extensive consultation period.", "嗯，我们已经有过一轮广泛的征询讨论了。"),
    ('W', "I know, but there's always the feeling that if it isn't broke, don't fix it.", "我明白，但总有人觉得，既然没坏就别去修。"),
    ('M', "People are worried about their jobs, too.", "人们也担心自己的工作。"),
    ('M', "I think we need to stress that while there will be some job changes, there won't be anyone getting dismissed.", "我想我们得强调，虽然会有一些职位变动，但不会有人被解雇。"),
    ('M', "In fact, we're looking to take on more staff.", "事实上，我们还打算招聘更多员工。"),
    ('W', "Agreed.", "同意。"),
    ('W', "You can hardly blame people for worrying though.", "不过人们有所担忧也是人之常情。"),
    ('W', "We need to make it clear that it's not just change for change's sake.", "我们需要讲清楚，这绝不是为变而变。"),
    ('W', "In other words, we really must make the case for why we are doing it.", "换句话说，我们确实必须把为什么要这么做这件事说清楚。"),
    ('M', "So what's the outline of the presentation?", "那么这份汇报的大纲是什么？"),
    ('M', "I'll start with a brief review of the reasons for the change that we really need to make a clean break to restart growth.", "我会先简要回顾变革的理由——我们确实需要一次彻底的了断来重启增长。"),
    ('M', "After that I'll outline the new company's structures and who's going where.", "之后我会概述新公司的组织架构，以及谁会调到哪里。"),
    ('M', "Then I'll hand it over to you to discuss the timeline and summarize and we'll take questions together at the end.", "然后我把汇报交给你，由你来讨论时间表并作总结，最后我们一起回答提问。"),
    ('M', "Anything else?", "还有别的要补充的吗？"),
    ('W', "Oh, yeah, we should let the staff know the channels of communication, you know, who they can contact or direct questions to about these changes.", "哦，对，我们应该让员工知道有哪些沟通渠道，你知道的，关于这些变动他们可以联系谁、或者把问题反映给谁。"),
    ('M', "Yes, and we can collect some frequently asked questions and present some general answers.", "对，而且我们可以收集一些常见问题，并给出一些概括性的回答。"),
    ('W', "Um, and we'll make the presentation and the questions available via the company's own computer network, right?", "嗯，我们会把汇报演示文稿和问答内容发布在公司的内部网络上，对吧？"),
    ('M', "Yes, the whole thing will be posted online.", "对，全部内容都会发到网上。"),
    ('W', "All right.", "好的。"),
    ('W', "Perhaps we should do a practice run of the presentation first.", "也许我们应该先预演一遍汇报。"),
    ('M', "Yeah, good idea.", "好，好主意。")
]

# Subpart 3: P1
NEW_P1_SENTS = [
    ('M', "Imagine walking through a busy airport and you see a miniature horse strolling down the terminal.", "想象一下，你正走在繁忙的机场里，突然看见一匹矮马在航站楼里闲庭信步。"),
    ('M', "At the Cincinnati/Northern Kentucky International Airport, miniature horses deliver a calming force two times a month.", "在辛辛那提/北肯塔基国际机场，迷你马每个月都会带来两次安抚人心的力量。"),
    ('M', "Denver and Ruby are two of the 34 therapy horses brought in from a local farm.", "丹佛和鲁比就是从当地一家农场引进的34匹治疗马中的两匹。"),
    ('M', "Their presence seems to help passengers feel more relaxed before boarding their flights.", "它们的存在似乎能帮助乘客在登机前感到更加放松。"),
    ('M', "More than 30 airports across the country now have therapy dogs.", "目前全美有30多家机场配备了治疗犬。"),
    ('M', "San Francisco has a therapy pig.", "旧金山机场还有一只治疗猪。"),
    ('M', "Cincinnati is the only airport with therapy horses.", "辛辛那提是唯一拥有治疗马的机场。"),
    ('M', "The program has proven so successful that other airports are considering introducing similar animals.", "该项目被证明非常成功，以至于其他机场也在考虑引入类似的动物。"),
    ('M', "The animals don't get startled.", "这些小动物不会受惊。"),
    ('M', "They have had hundreds of hours of airport training, so they are used to having luggage and people crowding around them.", "它们接受过数百小时的机场环境脱敏训练，因此早就习惯了行李箱和人群簇拥在它们周围。"),
    ('M', "They even wear special sneakers so they don't slip on the polished terminal floors.", "它们甚至还穿着特制的运动鞋，这样就不会在光洁如镜的航站楼地面上打滑。"),
    ('M', "The passengers often say that seeing animals makes them feel much better and helps them to calm down before a flight.", "乘客们经常表示，看到这些小动物让他们心情好多了，有助于他们在飞行前平静下来。"),
    ('M', "This little bit of support can sometimes make a big difference.", "这种小小的心理慰藉有时能发挥巨大的安抚作用。"),
    ('M', "It's amazing how a gentle nuzzle from a horse can completely erase airport stress.", "令人惊奇的是，小马轻轻蹭一下就能把在机场产生的焦虑一扫而空。"),
    ('M', "Visits to nursing homes and schools are also a regular part of the horses' schedule.", "去养老院和学校探访也是这些小马日常日程的一部分。"),
    ('M', "Their owner is already working on a new idea for a therapy animal—donkeys.", "它们的主人目前已经在构思一种全新的治疗动物——驴子。"),
    ('M', "Donkeys are gentle, patient, and very sweet.", "驴子温顺、有耐心，而且非常讨人喜欢。"),
    ('M', "Who knows, maybe soon you'll see a therapy donkey walking through the security gate!", "谁知道呢，说不定很快你就会看见一只治疗驴走过安检闸机呢！")
]

# Subpart 4: P2
NEW_P2_SENTS = [
    ('M', "Hello, viewers.", "各位观众，大家好。"),
    ('M', "Today I'm standing at the 2000-year-old Roman-era site.", "今天我正站在一处拥有两千年历史的古罗马时代遗址前。"),
    ('M', "Here in southern France, archaeologists have unearthed an extraordinary collection of ancient wall paintings.", "在法国南部这里，考古学家发掘出了一批极其珍贵的古代壁画。"),
    ('M', "They are being hailed as the most significant discovery of Roman art in France in decades.", "它们被誉为几十年来法国在古罗马艺术领域最重大的考古发现。"),
    ('M', "Patches of paint still cling to the stone walls of the bedroom and reception hall.", "在卧室和会客大厅的石墙上，依然保留着斑驳的色彩。"),
    ('M', "Some of these painted walls are preserved in places to a height of one meter.", "其中一些彩绘墙壁局部保存完好，高度可达一米。"),
    ('M', "Thousands of fragments had fallen from the upper walls and ceiling into the soil below.", "成千上万块碎片从上层墙壁和天花板脱落，掉落在了下方的泥土中。"),
    ('M', "These pieces have been put back together with great care and display a variety of images.", "这些碎片被极其悉心地拼合复原，呈现出多姿多彩的图景。"),
    ('M', "Some of these images include figures never seen before in France, such as a woman playing a stringed instrument, possibly a character from mythology.", "其中一些画面包含了在法国从未见过的生动人物，例如一名正在弹奏弦乐器的女性，可能是一位神话人物。"),
    ('M', "The paintings were done with such skill and with such expensive dyes that experts believe the artists originally came from Italy.", "这些壁画的绘制手法如此高超，所用的颜料又是如此昂贵，专家们认为画师最初很可能来自意大利本土。"),
    ('M', "They were likely hired by one of the city's elite.", "他们很可能是受聘于该城邦的一位权贵精英。"),
    ('M', "The homeowner was clearly wealthy and eager to show off his refined Roman taste to his peers.", "这位房屋主人显然家财万贯，并且渴望向同侪炫耀自己纯正考究的罗马品位。"),
    ('M', "Perhaps a Roman official wanted Pompeii-like interior to remind him of home.", "也许是一名罗马官员想要一套庞贝风格的室内装潢来寄托思乡之情。"),
    ('M', "He was probably stationed in this provincial trading port founded in 46 B.C.", "他很可能驻扎在这一建于公元前46年的行省贸易港口城市。"),
    ('M', "The luxury of the house demonstrates how rapidly Roman culture penetrated this corner of the empire.", "这处住宅的奢华充分证明了罗马文化以何等惊人的速度渗透到了帝国的这个角落。"),
    ('M', "The paintings may yield even more stunning surprises as additional sections are put together, like pieces of a puzzle.", "随着更多墙壁板块像拼图一样被拼合起来，这些壁画可能会带给我们更多惊艳的惊喜。"),
    ('M', "Whoever it was that created such magnificent pieces of art, they surely had no idea that their work would still be around thousands of years later.", "无论当年是谁创作了如此宏伟瑰丽的艺术珍品，他们肯定未曾想到自己的杰作在数千年之后依然熠熠生辉。")
]

# Subpart 5: R1
NEW_R1_SENTS = [
    ('M', "Good afternoon, class.", "同学们，下午好。"),
    ('M', "Today I want to discuss with you a new approach to empirical research.", "今天我想和大家探讨一种进行实证研究的全新方法。"),
    ('M', "In the past, scientists often worked alone.", "在过去，科学家们往往各自单打独斗。"),
    ('M', "They were confined to the university or research center where they worked.", "他们受限于自己任职的大学或科研机构。"),
    ('M', "Today, though, we are seeing mergers of some of the greatest scientific minds, regardless of their location.", "然而在今天，无论身处何地，我们正目睹着一些最伟大科学头脑的强强联合。"),
    ('M', "There has never been a better time for collaborations with foreign scientists.", "与外国科学家开展跨国合作，从来没有像今天这样迎来绝佳的黄金时代。"),
    ('M', "In fact, the European Union is taking the lead.", "事实上，欧洲联盟正走在最前列。"),
    ('M', "Spurred on by funding policies, half of European research articles had international co-authors in 2007.", "在科研资助政策的激励下，2007年欧洲半数的研究论文都拥有跨国合著者。"),
    ('M', "The United States is lagging behind, with only 30% of articles being collaborative with foreign scientists.", "相比之下美国则略显滞后，仅有30%的论文是与外国科学家合作完成的。"),
    ('M', "In China, the rate is lower, hovering at just 15%.", "而在中国，这一比例更低，徘徊在仅约15%。"),
    ('M', "Even so, the levels in these countries are also rising.", "即便如此，这些国家的跨国合作水平也都在稳步上升。"),
    ('M', "This is a sign of the continued allure of creating scientific coalitions across borders.", "这表明跨越国界组建科学联盟依然具有持久的强大吸引力。"),
    ('M', "Andrew Schubert, a researcher at the Institute for Science Policy Research, says that the rising collaboration is partly out of necessity.", "科学政策研究所的研究员安德鲁·舒伯特表示，合作的兴起在某种程度上是出于现实必然性。"),
    ('M', "This necessity comes with the rise of big science.", "这种必然性伴随着“大科学”时代的到来而产生。"),
    ('M', "Big scientific projects require enormous resources, vast datasets, and multi-disciplinary teams that no single institution can provide.", "大型科研项目需要庞大的资金资源、海量的数据集以及多学科团队，这是任何单一机构都无法独立承担的。"),
    ('M', "But he says collaborations have also emerged because of increased possibilities.", "但他同时表示，合作的激增也源于科技赋予的更多可能性。"),
    ('M', "The Internet allows like-minded scientists to find each other.", "互联网使志同道合的科学家能够轻而易举地找到彼此。"),
    ('M', "Communication is now instant and cost-free, enabling daily interactions across time zones.", "如今的跨国交流即时且零成本，使得跨时区的日常学术协作畅通无阻。"),
    ('M', "And there is a reward.", "而且这还会带来丰厚的回报。"),
    ('M', "Studies of citation counts show that internationally co-authored papers have better visibility.", "对文献引用次数的研究表明，国际合著的论文拥有更高的曝光度和学术影响力。"),
    ('M', "They receive significantly more citations than papers authored by domestic teams alone.", "它们获得的引用次数明显多于仅由国内团队独立撰写的论文。"),
    ('M', "Caroline Wagner, a research scientist at George Washington University, notes that international collaborations offer additional flexibility.", "乔治华盛顿大学的研究科学家卡罗琳·瓦格纳指出，国际合作还提供了额外的灵活性。"),
    ('M', "Whereas local collaborations sometimes persist past the point of usefulness because of social or academic obligations, international ones can be cultivated and dropped more freely.", "本地合作有时碍于人情世故或学术层级关系而在失去实际价值后依然勉强维系，而国际合作则可以更加自由地建立与解除。"),
    ('M', "The collaborative trend is true across scientific disciplines.", "这种合作趋势在各个科学门类中普遍存在。"),
    ('M', "Some fields, though, have a greater tendency for it.", "不过，某些学科领域表现出了更为强烈的合作倾向。"),
    ('M', "Particle physicists and astronomers collaborate often.", "粒子物理学家和天文学家经常开展跨国大合作。"),
    ('M', "This is because they must share expensive facilities.", "这是因为他们必须共同分摊并共享昂贵的实验设施。"),
    ('M', "No single country can afford to build a Large Hadron Collider or a giant space telescope on its own.", "没有哪一个国家能够独自承担建造大型强子对撞机或巨型太空望远镜的天文数字成本。"),
    ('M', "On the other hand, mathematicians rarely collaborate across borders.", "另一方面，数学家们却很少开展跨国合作。"),
    ('M', "Mathematics remains a largely solitary endeavor requiring little more than paper, pencil, and a quiet room.", "数学在很大程度上依然是一项孤独求索的事业，所需要的无非是纸、笔以及一间安静的书房。"),
    ('M', "The level of collaboration also varies from country to country.", "各个国家之间的国际合作程度也大相径庭。"),
    ('M', "There are historical and political reasons as to why collaborations emerge, says Wagner.", "瓦格纳表示，跨国合作之所以形成，背后有着深厚的历史与地缘政治原因。"),
    ('M', "Shared language, cultural affinity, and historical ties strongly dictate which countries partner with each other.", "共同的语言、文化认同和历史渊源，在很大程度上决定了哪些国家会彼此结为科研合作伙伴。")
]

# Subpart 6: R2
NEW_R2_SENTS = [
    ('M', "Good evening.", "晚上好。"),
    ('M', "In 1959, the year I was born, a headline in Life magazine proclaimed, Target Venus: May Be Life There!", "1959年，也就是我出生的那一年，《生活》杂志上的一则醒目标题赫然宣告：“目标金星：那里可能存在生命！”"),
    ('M', "The mid-twentieth century was a time of boundless optimism about our planetary neighbor.", "二十世纪中叶，人们对我们这颗行星邻居充满了无限的乐观遐想。"),
    ('M', "As a kid, I thrilled to tales of adventure and Isaac Asimov's juvenile science-fiction novel Lucky Starr and the Oceans of Venus.", "小时候，探险传奇故事和艾萨克·阿西莫夫的少年科幻小说《幸运斯塔尔与金星海洋》都令我无比痴迷神往。"),
    ('M', "For many of my peers, though, Venus quickly lost its romance.", "不过对我的许多同代人来说，金星很快就褪去了它的浪漫色彩。"),
    ('M', "The very first thing that scientists discovered with a mission to another planet was that Venus was not at all the Earthly paradise that fiction had portrayed.", "科学家们通过对另一颗行星执行探索任务所查明的第一件事，就是金星根本不是科幻小说里描绘的那片人间天堂。"),
    ('M', "It is nearly identical to our own planet in bulk properties such as mass, density and size.", "在质量、密度和体积等整体物理性质上，金星与我们的地球几乎一模一样。"),
    ('M', "But its surface has been cooked and dried by an ocean of carbon dioxide.", "但它的地表早已被厚达数百个大气压的二氧化碳浓云煮沸烘烤得干瘪龟裂。"),
    ('M', "Surface temperatures exceed 460 degrees Celsius, hot enough to melt lead.", "其地表温度超过460摄氏度，足以直接融化铅块。"),
    ('M', "Trapped in the burning death-grip of a runaway greenhouse effect, Venus has long been held up as a cautionary tale for everything that could go wrong on a planet like Earth.", "深陷失控温室效应造成的灼热死亡枷锁之中，金星长久以来一直被当作一面警世警钟，揭示着在类似地球的行星上一旦失衡可能引发的一切灾难。"),
    ('M', "As a possible home for alien life, it has been voted the planet least likely to succeed.", "作为外星生命的可能栖息地，它被公认为最不可能孕育生命的星球。"),
    ('M', "Scientists turned their eyes toward Mars, leaving Venus neglected for decades.", "科学家们纷纷把目光转向火星，使得金星被冷落了数十年。"),
    ('M', "But I have refused to give up on Venus, and over the years my stubborn loyalty has been justified.", "但我始终拒绝放弃对金星的信念，多年来我这份执拗的执着也被证明是极具前瞻性的。"),
    ('M', "The rocky views glimpsed by Venera 9 and other Russian landers suggested a tortured volcanic history.", "金星9号探测器和其他苏联着陆器捕捉到的岩石全景显示，这颗星球曾经历过波澜壮阔的火山喷发史。"),
    ('M', "That was confirmed in the early 1990s by the American Magellan orbiter, which used radar to peer through the planet's thick clouds and map out a rich, varied and dynamic surface.", "20世纪90年代初，美国的麦哲伦号轨道器证实了这一点，它利用合成孔径雷达穿透金星稠密的云层，绘制出了一幅丰富、多元且充满地质活力的地表全图。"),
    ('M', "The surface formed mostly in the last billion years, which makes it fresher and more recently active than any rocky planet other than Earth.", "金星表面绝大部分是在过去十亿年内重塑形成的，这使它成为除地球之外地表最年轻、地质活动最为活跃的类地行星。"),
    ('M', "Russian and American spacecraft also found hints that Venus's ancient climate was wetter, cooler and possibly even friendly to life.", "俄罗斯与美国的航天探测器还发现了蛛丝马迹：金星远古时期的气候更湿润、更凉爽，甚至可能对生命极其友好。"),
    ('M', "Measurements of Venus's density and composition show that it formed out of the same stuff as Earth, including water, and much more water than the trace found today in Venus's dense atmosphere.", "对金星密度和矿物成分的测定表明，它与地球由相同的原始星云物质凝聚而成，其中也包含了水，而且水量远比今天在金星稠密大气中检测到的微量水分多得多。"),
    ('M', "Thus our picture of Venus is of a planet with warm oceans swirled with organic molecules, lapping against shores that were lined with forests and volcanoes.", "因此，我们最新构建出的金星画卷是一颗拥有温润海洋、泛着有机分子波浪、拍打着火山与陆地边缘的温暖星球。"),
    ('M', "The sun was far dimmer back then.", "那时的太阳辐射强度远比现在要微弱暗淡。"),
    ('M', "So Venus was, in many ways, cozier than Earth.", "因此在诸多方面，远古时期的金星甚至比地球更为宜居舒适。")
]

# Subpart 7: R3
NEW_R3_SENTS = [
    ('M', "If I'm a psychology professor at the University of British Columbia, I specialize in cultural psychology, examining similarities and differences between East Asians and North Americans.", "我是不列颠哥伦比亚大学的一名心理学教授，专攻文化心理学，探究东亚人与北美人之间的心理共性与差异。"),
    ('M', "Our research team has been looking at cultural differences in self-enhancing motivations, how people have positive feelings towards not only themselves, but things connected to themselves.", "我们科研团队一直在探讨自我提升动机方面的文化差异，即人们如何不仅对自己、也对与自身相联结的事物抱有积极的情感评价。"),
    ('M', "For example, when you own something, you view it as more valuable than when you don't own it.", "举例来说，当你真正拥有某件物品时，你对它的价值评估会明显高于未曾拥有它的时候。"),
    ('M', "It's called the endowment effect.", "心理学上把这种现象称作“禀赋效应”。"),
    ('M', "The strength of that effect is stronger in Western cultures than in East Asian cultures.", "这种效应在西方文化背景下的体现，明显强于在东亚文化中的表现。"),
    ('M', "So we've been looking at other ways of seeing whether this motivation to view oneself positively is shaped by cultural experiences.", "因此我们一直在寻求其他切入点，来验证这种积极看待自我的内在动机究竟在多大程度上受到文化经验的塑造。"),
    ('M', "We've also started to look at how culture shapes sleep.", "最近我们也开始探究文化如何潜移默化地塑造人类的睡眠习惯。"),
    ('M', "We are still in the exploratory stages of this project, although what's noteworthy is that East Asians on average sleep about an hour and a half less each night than North Americans do.", "尽管该项目仍处于探索阶段，但引人注目的是，东亚人每晚的平均睡眠时间比北美人少大约一个半小时。"),
    ('M', "And it's not a more efficient sleep, not like they're compressing relatively more value out of their hours.", "而且这绝非因为他们的睡眠效率更高，并不是说他们能在更短的时间内压榨出相对更高的休息价值。"),
    ('M', "Other studies have found that even infants in East Asia sleep about an hour less than European infants.", "其他独立研究甚至发现，连东亚的婴儿每晚都比欧洲婴儿少睡约一个小时。"),
    ('M', "So we're trying to figure out how culture shapes the way you sleep.", "因此我们正试图揭开文化究竟是如何深刻塑造人们睡眠模式的面纱。"),
    ('M', "Our experiment does not take place in a sleep lab.", "我们的实验并不是在人工睡眠实验室里进行的。"),
    ('M', "Instead, we lend people motion-detecting watches, and they wear them for a week at a time.", "相反，我们向受试者借出带有运动传感监测功能的手表，让他们每次连续佩戴一整周。"),
    ('M', "Whenever they are not having a shower or swimming, they keep it on.", "除了洗澡或游泳之外，他们在日常生活中全程贴身佩戴。"),
    ('M', "These kinds of watches are used in sleep studies as a way of measuring how long people are sleeping, how efficient their sleep is, and whether they are waking up in the night.", "这类监测腕表在现代睡眠科学研究中被广泛应用，用于客观量化受试者实际睡了多久、睡眠质量效率如何，以及夜间是否存在中途惊醒。"),
    ('M', "Ideally, I'd like to take this into a controlled lab environment.", "在理想状态下，我希望能把这项研究引入设备更精密的受控实验室环境中深入开展。"),
    ('M', "We'll see where the research points us.", "我们将顺应实证数据的指引，看看科学线索会把我们引向何方。"),
    ('M', "We usually start off with the more affordable methods and if everything looks promising, then it will justify trying to build a sleep lab and study sleep across cultures that way.", "我们通常从成本可负担的方法起步探索；如果前期成果展现出广阔前景，那么就能为申请巨额经费建立专门的睡眠实验室提供充分依据，从而更加系统地开展跨文化睡眠研究。"),
    ('M', "Why do we study sleep?", "我们为什么要花大力气研究睡眠呢？"),
    ('M', "Sleep is something that has really been an unexplored topic cross-culturally.", "因为在跨文化心理学领域，睡眠长期以来一直是一个鲜有人涉足的处女地。"),
    ('M', "I'm attracted to it because culture isn't something that only shapes the way our minds operate; it shapes the way our bodies operate too, and sleep is at the intersection of those.", "我之所以对它深感着迷，是因为文化绝不仅仅塑造我们大脑思维的运转逻辑，它同样在深层次塑造着我们肉体生理的运作节律，而睡眠恰好处于心智与生理的交汇点上。")
]

new_sentences_list = [
    NEW_C1_SENTS,
    NEW_C2_SENTS,
    NEW_P1_SENTS,
    NEW_P2_SENTS,
    NEW_R1_SENTS,
    NEW_R2_SENTS,
    NEW_R3_SENTS
]

for idx, sp in enumerate(SUBPARTS):
    sp['sentences'] = new_sentences_list[idx]

import pprint
target = Path("pipeline/data_2019_06_set2.py")
with open(target, "w", encoding="utf-8") as f:
    f.write("#!/usr/bin/env python3\n")
    f.write('"""\nOfficial data for 2019-06-set2 CET-6 listening test:\n- 7 subparts with authentic titles, Chinese topics, and question ranges\n- Complete grammatical sentences with 100% paired authentic Chinese translations\n- 25 official CET-6 questions with options, answers, and explanations\n"""\n\n')
    f.write("SUBPARTS = ")
    pprint.pprint(SUBPARTS, stream=f, width=120, compact=False)
    f.write("\n\nQUESTIONS = ")
    pprint.pprint(QUESTIONS, stream=f, width=120, compact=False)
    f.write("\n")

print(f"Successfully updated {target}")
total_s = sum(len(sp['sentences']) for sp in SUBPARTS)
print(f"Total individual sentences: {total_s}")
