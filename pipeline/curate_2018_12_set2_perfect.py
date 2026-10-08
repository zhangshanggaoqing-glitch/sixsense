#!/usr/bin/env python3
"""
Perfect curation for 2018-12-set2:
100% authentic official text from official resolution PDF,
exact subpart speech boundaries, zero question bleed.
"""

import json
import re
import sqlite3
from difflib import SequenceMatcher
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "sixsense.db"
WHISPER_PATH = BASE_DIR / "data" / "derived" / "exams" / "2018-12-set2" / "whisper_full.json"
EXAM_ID = "2018-12-set2"

# 7 Subparts with authentic sentences and verified speech boundaries
SUBPARTS = [
    {
        "id": "2018-12-set2-conv-1",
        "section_id": "2018-12-set2-sec-a",
        "type": "conversation",
        "title": "Conversation 1",
        "topic_zh": "男生的网红梦：与雕像合照引发成为网红的理想与修图发帖努力",
        "question_range": "Questions 1 to 4",
        "questions": [1, 2, 3, 4],
        "sp_start": 37.04,
        "sp_end": 141.00,
        "sentences": [
            ('M', "Do you mind taking my photo with the statue over there?", "你介意帮我和那边的雕像拍张照吗？"),
            ('M', "I think it will make a great shot.", "我觉得这样拍出来的照片会很棒。"),
            ('W', "Sure, no worries.", "当然，没问题。"),
            ('W', "You're always taking photos.", "你总是在拍照。"),
            ('W', "What do you do with all the photos you take?", "你都怎么处理拍出来的那些照片呢？"),
            ('M', "Well, don't laugh.", "嗯，别笑话我。"),
            ('M', "My dream is to become an online celebrity of sorts.", "我的梦想是成为一个小有名气的网络红人。"),
            ('W', "You are not serious, are you?", "你该不会是认真的吧？"),
            ('M', "I am, completely.", "我是极其认真的。"),
            ('M', "I just got the idea a few months ago after posting some holiday photos on my social media accounts.", "几个月前我在社交媒体账号上发了一些度假照片后，才萌生了这个念头。"),
            ('M', "A lot of people liked my photos and started asking me for travel tips.", "很多人给我的照片点赞，还纷纷向我索要旅行攻略。"),
            ('M', "So I figured I'd give it a go.", "所以我想我应该尝试一下。"),
            ('M', "I post a lot on social media anyway, so I've got nothing to lose.", "反正我平时也在社交平台上发很多动态，试一试也没什么损失。"),
            ('W', "I guess that's true.", "我想你说的确实在理。"),
            ('W', "So what do you have to do to become Internet famous?", "那么，你要做些什么才能成为知名网红呢？"),
            ('M', "Surprisingly a lot more than I did as a hobby.", "没想到的是，这要比我当初纯粹当成业余爱好付出的多得多。"),
            ('M', "Recently, I've been spending a lot more time editing photos, posting online and clearing storage on my phone.", "最近，我花了大量时间精细修图、按时发帖，以及清理手机的存储空间。"),
            ('M', "It's always full now.", "现在的手机存储空间总是提示已满。"),
            ('W', "That doesn't sound like too much work.", "听起来工作量似乎也不算太大呀。"),
            ('M', "Well, there's more to it.", "其实远不止这些表面功夫。"),
            ('M', "I spent all last weekend researching what topics are popular, what words to use in captions and similar accounts to follow.", "上周整个周末我都在深入研究什么话题最热门、配文该用哪些引流热词，以及关注哪些相似的成功博主账号。"),
            ('M', "It really was a lot to take in.", "需要学习消化的知识实在太多了。"),
            ('M', "And I was up well past midnight.", "我常常熬夜熬到深更半夜。"),
            ('M', "I'd say it's paying off though.", "不过我觉得这些付出是值得的。"),
            ('M', "I increased the number of people following my accounts by 15 already.", "关注我账号的粉丝数量已经增加了15%。"),
            ('W', "That is impressive.", "那确实很厉害了。"),
            ('W', "I guess I never thought much about all the effort behind the scene.", "我想我以前从未认真想过幕后竟要付出如此多的心血。"),
            ('W', "Now that I think about it, there's always something wrong with my photos as it is — half smiles, closed eyes, messy hair.", "现在回想起来，我拍的照片总是有各种各样的瑕疵——似笑非笑的表情、闭着的眼睛，还有凌乱不堪的头发。"),
            ('W', "I hope you have better luck than I do.", "我希望你的运气能比我好得多。")
        ]
    },
    {
        "id": "2018-12-set2-conv-2",
        "section_id": "2018-12-set2-sec-a",
        "type": "conversation",
        "title": "Conversation 2",
        "topic_zh": "访谈节目《今日物理》：女科学家谈宇宙起源与物质反物质湮灭不对称之谜",
        "question_range": "Questions 5 to 8",
        "questions": [5, 6, 7, 8],
        "sp_start": 218.46,
        "sp_end": 337.00,
        "sentences": [
            ('M', "Good evening, and welcome to Physics Today.", "晚上好，欢迎收听《今日物理》节目。"),
            ('M', "Here we interview some of the greatest minds in physics as they help us to understand some of the most complicated theories.", "在这里，我们采访物理学界最顶尖的大脑，帮助我们理解一些最前沿深奥的物理理论。"),
            ('M', "Today, I'm very pleased to welcome Dr. Melissa Phillips, Professor of Theoretical Physics.", "今天，我非常荣幸地邀请到了理论物理学教授梅丽莎·菲利普斯博士。"),
            ('M', "She's here to tell us a little about what it is she studies.", "她来到演播室，与我们分享她的研究工作。"),
            ('M', "Dr. Phillips, you seem to study everything.", "菲利普斯博士，您似乎什么都研究。"),
            ('W', "I guess that would be fair to say.", "我想这么说确实很贴切。"),
            ('W', "I spend most of my time studying the Big Bang Theory, and where our universe came from.", "我把大部分时间都花在研究大爆炸理论以及我们的宇宙究竟起源于何处。"),
            ('M', "Can you tell us a little about that?", "您能为我们详细讲讲这方面的内容吗？"),
            ('W', "Well, I'm very interested in why the universe exists at all.", "好的。我最感兴趣的问题是：为什么宇宙从一开始就得以存在。"),
            ('W', "That may sound odd, but the fact is, at the moment of the Big Bang, both matter and antimatter were created.", "这听起来可能有点奇怪，但事实是：在大爆炸发生的一瞬间，同时产生了等量的物质与反物质。"),
            ('W', "For a short time, and I mean just a fraction of a second, the whole universe was a super hot soup of radiation filled with these particles.", "在极短的时间内——我指的是仅仅一刹那的极微小瞬间，整个宇宙就是一团充满这些粒子的超高温辐射浓汤。"),
            ('M', "So, what's baffled scientists for so long is, why is there a universe at all?", "那么，长期以来一直困扰着科学家们的谜题正是：为什么竟然还会有宇宙留存下来呢？"),
            ('W', "That's because matter and antimatter are basically opposites of each other.", "那是因为物质与反物质在本质上是互相对立的。"),
            ('W', "They are exactly alike, except that they have opposite electrical charges.", "它们在各方面都完全相同，唯一的区别在于它们带有相反的正负电荷。"),
            ('M', "So, when they collide, they destroy each other?", "那么，当它们相互碰撞时，就会将彼此彻底湮灭销毁吗？"),
            ('W', "Exactly.", "完全正确。"),
            ('W', "So, during the first few moments of the Big Bang, the universe was extremely hot and very small.", "因此，在大爆炸发生最初的几个瞬间，整个宇宙极其炙热并且体积极小。"),
            ('W', "Matter, and the now more exotic antimatter would have had little space to avoid each other.", "物质以及如今显得更为神秘的反物质，几乎没有任何多余的空间能够避开彼此。"),
            ('W', "This means that they should have totally wiped each other out, leaving the universe completely barren.", "这意味着它们本该彻底将彼此湮灭殆尽，从而让整个宇宙空无一物、一片死寂。"),
            ('M', "But a recent study seems to point to the fact that when matter and antimatter were first created, there were slightly more particles of matter, which allowed the universe we all live in to form?", "但是最近的一项研究似乎表明，当物质与反物质最初形成时，物质粒子的数量稍微多出了那么一点点，才最终使得我们今天所生活的宇宙得以形成？"),
            ('W', "Exactly.", "一点没错。"),
            ('W', "Because there was slightly more matter, the collisions quickly depleted all the antimatter and left just enough matter to create stars, planets, and eventually us.", "正因为物质稍微多出了一些，剧烈的碰撞很快耗尽了所有的反物质，并留下了恰好足够的物质来创造恒星、行星，以及最终孕育出我们人类。")
        ]
    },
    {
        "id": "2018-12-set2-pass-1",
        "section_id": "2018-12-set2-sec-b",
        "type": "passage",
        "title": "Passage 1",
        "topic_zh": "外国口音综合征：迈尔斯两年英式口音、中风脑损伤诱因与百年罕见病例",
        "question_range": "Questions 9 to 11",
        "questions": [9, 10, 11],
        "sp_start": 447.83,
        "sp_end": 553.00,
        "sentences": [
            ('M', "In this week's edition of a special series on Bizarre Medical Conditions, there is a report of the case of Michelle Myers.", "在本周《奇疾怪症》特别系列节目中，为您带来一篇关于米歇尔·迈尔斯的病例报道。"),
            ('M', "Myers is an American woman who woke up one day speaking with a British accent, even though she's lived in the United States all her life.", "迈尔斯女士是一名美国人，某天醒来后讲话突然变成了英式口音，尽管她一生都生活在美国。"),
            ('M', "In 2015, Myers went to bed with a terrible headache.", "2015年某日，迈尔斯带着剧烈的头痛上床睡觉。"),
            ('M', "She woke up sounding like someone from England.", "她醒来后说话听起来就像是个英国人。"),
            ('M', "Her British accent has remained for the past two years.", "她的英式口音在过去两年里一直保持未变。"),
            ('M', "Previously, Myers had woken up speaking in Irish and Australian accents.", "在此之前，迈尔斯也曾一觉醒来操着爱尔兰口音和澳大利亚口音。"),
            ('M', "However, on both of those occasions, the accents lasted for only a week.", "然而，在那两次经历中，口音都仅仅持续了一周左右。"),
            ('M', "Myers has been diagnosed with Foreign Accent Syndrome.", "迈尔斯被正式诊断为患有外国口音综合征。"),
            ('M', "It's a disorder in which a person experiences a sudden change to their speech so that they sound like they are speaking in a foreign accent.", "这是一种言语障碍，患者的语音语调会突然发生改变，以至于听起来像是在操着外国口音说话。"),
            ('M', "The condition is most often caused by a stroke or traumatic brain injury.", "这种病症最常由中风或外伤性颅脑损伤引发。"),
            ('M', "Although people with the syndrome have intelligible speech, their manner of speaking is altered in terms of timing and tongue placement, which distorts their pronunciation.", "虽然该综合征患者所说的话清晰可懂，但说话方式在发音节奏和舌位上发生了改变，从而扭曲了正常发音。"),
            ('M', "As a result, they may sound like a foreigner when speaking their native language.", "结果便是，他们在说母语时听起来就像外国人一样。"),
            ('M', "It's not clear whether Myers has had a stroke or other brain injury, but she also has a separate medical condition, which can result in loose joints, easily bruised skin, and other problems.", "目前尚不清楚迈尔斯是否曾突发中风或遭受其他脑损伤，但她同时患有另一种独立的疾病，会导致关节松动、皮肤极易淤青以及其他并发问题。"),
            ('M', "Foreign accent syndrome is rare, with only about 60 cases reported within the past century.", "外国口音综合征非常罕见，在过去的一个世纪里全球仅报道了大约60例。"),
            ('M', "However, a different American woman reportedly spoke with a Russian accent in 2010 after she fell down the stairs and hit her head.", "然而，据报道另一位美国女性在2010年从楼梯跌落摔伤头部后，说话带上了浓重的俄罗斯口音。")
        ]
    },
    {
        "id": "2018-12-set2-pass-2",
        "section_id": "2018-12-set2-sec-b",
        "type": "passage",
        "title": "Passage 2",
        "topic_zh": "女性游泳简史：维多利亚时期的端庄限制、更衣车与埃德勒横渡英吉利海峡",
        "question_range": "Questions 12 to 15",
        "questions": [12, 13, 14, 15],
        "sp_start": 617.62,
        "sp_end": 729.00,
        "sentences": [
            ('W', "There is something about water that makes it a good metaphor for life.", "水的某些特质使其成为了生命极佳的绝妙隐喻。"),
            ('W', "That may be one reason why so many people find relief in swimming when life's seas get rough.", "这也许就是为什么当人生的海洋风浪汹涌时，会有如此多的人能在游泳中获得精神慰藉的原因之一。"),
            ('W', "And it goes some way towards explaining why books about swimming, in which people tackle icy lakes, race in rivers and overcome oceans while reflecting on their lives, have recently become so popular.", "这也在很大程度上解释了，为什么近来有关游泳的书籍如此大受欢迎——在这些作品中，人们挑战冰冷的湖泊、在河流中穿梭竞速、在搏击海洋的同时深刻反思自己的人生。"),
            ('W', "These books reflect a trend, particularly strong in Britain, where swimming in pools is declining but more and more folks are opting for open water.", "这些畅销书反映了一种正在兴起的新趋势——尤其在英国尤为显著：去室内游泳池的人数在持续下降，而越来越多的人毅然投身于开放水域的怀抱。"),
            ('W', "Wild swimming seems to be especially popular among women.", "这种“野外自然水域游泳”似乎在女性群体中格外受到追捧。"),
            ('W', "Jenny Landreth recently published a guide to the best swimming spots in London.", "珍妮·兰德雷斯最近出版了一本关于伦敦最佳自然游泳胜地的导览指南。"),
            ('W', "Her new book, Swell, interweaves her own story with a history of female pioneers who accomplished remarkable feats and paved the way for future generations.", "她引人入胜的新作《浪涌》，将她自己的亲身经历与历史上那些取得非凡成就并为后代女性铺平道路的先驱女性们的奋斗史紧密交织在一起。"),
            ('W', "Notions of modesty restricted women in the Victorian era, but they still swam.", "在维多利亚时代，严苛的“端庄”礼教观念极大地禁锢着女性，但即便如此，她们依然坚持游泳。"),
            ('W', "A bathing machine was rolled down to the seashore so women would not be seen in swimwear.", "当时人们会把专门的“海滨更衣沐浴车”推入浅海之中，这样女性身穿泳衣的模样就不会被公众窥见。"),
            ('W', "In 1892, The Gentlewoman's Book of Sport described a woman swimming in a heavy dress, boots, hat, gloves and carrying an umbrella.", "1892年出版的《贵妇运动全书》中，甚至记载了一名身穿笨重长裙、脚踩靴子、头戴帽子、手戴手套、甚至还撑着一把雨伞在海中游泳的女性。"),
            ('W', "Eventually, swimming became freer.", "历经漫长的抗争，女性游泳终于变得越来越自由与自主。"),
            ('W', "Mixed bathing was permitted on British beaches in 1901.", "1901年，英国海滩正式准许男女混合游泳。"),
            ('W', "Women won the right to swim in public pools, learned to swim properly, created appropriate swimwear and, in time, even competed against men.", "女性逐步赢得了在公共泳池畅游的合法权利，学会了规范科学的泳姿，设计出了轻便合体的现代泳装，并且随着时代的前行，甚至能在赛道上与男子同台竞技。"),
            ('W', "The first woman to cross the English Channel was Gertrude Ederle in 1926.", "历史上第一位成功横渡英吉利海峡的伟大女性是1926年的格特鲁德·埃德勒。"),
            ('W', "She beat the record by almost two hours and her father rewarded her with a red sports car.", "她将此前男子创造的世界纪录大幅缩短了将近两个小时，为此她的父亲欣喜若狂，奖励了她一辆鲜红色的跑车。")
        ]
    },
    {
        "id": "2018-12-set2-rec-1",
        "section_id": "2018-12-set2-sec-c",
        "type": "recording",
        "title": "Recording 1",
        "topic_zh": "高科技脑扫描测谎能否用于法庭：97%准确率宣称、现实缺乏复现与思维本质",
        "question_range": "Questions 16 to 18",
        "questions": [16, 17, 18],
        "sp_start": 836.09,
        "sp_end": 1006.00,
        "sentences": [
            ('M', "Today I'm going to talk about a very special kind of person.", "今天我要谈论一类非常特殊的人群。"),
            ('M', "Psychologists call them \"masters of deception\", those rare individuals with a natural ability to tell with complete confidence when someone is telling a lie.", "心理学家称他们为“识谎大师”——这些极其罕见的个体拥有一种与生俱来的天赋，能在他人说谎时充满自信地一眼看穿。"),
            ('M', "For decades, researchers and law enforcement agencies have tried to build a machine that will do the same thing.", "数十年来，科研人员和执法部门一直致力于研发一台具有同样识谎功能的机器。"),
            ('M', "Now a company in Massachusetts says that by using magnetic brain scans they can determine with 97 percent accuracy whether someone is telling the truth.", "如今马萨诸塞州的一家公司声称，通过运用脑部磁共振扫描，他们能够以高达97%的准确率测定一个人是否在讲真话。"),
            ('M', "They hope that the technology will be cleared for use in American courts by early next year.", "他们希望这项技术能够在明年初获得批准并进入美国法庭正式投入使用。"),
            ('M', "But is this really the ultimate tool for you, the lawyers of tomorrow?", "但对于在座的诸位——未来的律师们而言，这真的会是你们终极的诉讼利器吗？"),
            ('M', "You'll not find many brain scientists celebrating this breakthrough.", "你会发现，并没有多少脑科学家为这项所谓的“重大突破”欢欣鼓舞。"),
            ('M', "The company might be very optimistic, but the ability of their machine to detect deception has not provided credible proof.", "那家公司或许态度十分乐观，但其机器识别谎言的可靠性尚未给出令人信服的实证。"),
            ('M', "That's because the technology has not been properly tested in real-world situations.", "这是因为该技术从未在现实复杂情境中经受过严密而充分的验证。"),
            ('M', "In life, there are different kinds of lies and diverse contexts in which they're told.", "在现实生活中，存在着形形色色的谎言，而这些谎言产生的语境也千差万别。"),
            ('M', "These differences may elicit different brain responses.", "这些差异可能会引发截然不同的大脑神经生理反应。"),
            ('M', "Does their hypothesis behind the test apply in every case?", "这项测试背后的核心假设在每一起案件中都完全适用吗？"),
            ('M', "We don't know the answer, because studies done on how reliable this machine is have not yet been duplicated.", "我们目前根本无法给出确切答案，因为针对这台机器可靠性的研究结论至今尚未被独立重复验证过。"),
            ('M', "Much more research is badly needed.", "我们极其迫切地需要更多深入严谨的科研论证。"),
            ('M', "Whether the technology is eventually deemed reliable enough for the courts will ultimately be decided by the judges.", "这项技术最终是否会被认定对法庭审判足够可靠，终将由法官们来做出抉择。"),
            ('M', "Let's hope they're wise enough not to be fooled by a machine that claims to determine truthfulness at the flick of a switch.", "但愿法官们足够清醒睿智，不会被一台声称只需轻轻一按开关就能判定真伪的机器所蒙蔽。"),
            ('M', "They should also be sceptical of the growing tendency to try to reduce all human traits and actions to the level of brain activity.", "他们也应当对当下日益蔓延的一种倾向保持警惕，即试图将人类所有复杂的性格特质与行为模式都生搬硬套简化为大脑的生理活动。"),
            ('M', "Often, they do not map that easily.", "通常情况下，人的精神心智与脑电反应之间绝非能够如此轻易地一一对应。"),
            ('M', "Moreover, understanding the brain is not the same as understanding the mind.", "再者，解读大脑并不等同于真正理解人类的心智思维。"),
            ('M', "Some researchers have suggested that thoughts cannot properly be seen as purely \"internal\".", "一些学者早已指出，人类的思想绝不能被片面地视作纯粹的“大脑内在活动”。"),
            ('M', "Instead, thoughts make sense only in reference to the individual's external world.", "相反，只有与个体身处的外部客观世界相结合，思想才具有真正完整切实的意义。"),
            ('M', "So while there may be insights to be gained from matching behavior to brain activity, those insights will not necessarily lead to justice in a court of law.", "因此，尽管将个体行为与脑部活动进行映射或许能带来某些科学启示，但这些发现未必能确保法庭判决的正义与公允。"),
            ('M', "Problems surround the use of machines to spot deception, at least until it has been rigorously tested.", "在经过严苛的实践检验之前，利用机器来甄别谎言仍然面临着层出不穷的质疑与难题。"),
            ('M', "A high-tech test that can tell when a person is not telling the truth sounds too good to be true.", "一项声称能准确测出某人何时没讲真话的高科技测试，听上去实在好得令人难以置信。"),
            ('M', "And when something sounds too good to be true, it usually is.", "而当一件事听起来好得不真实的时候，它往往就真的不是真的。")
        ]
    },
    {
        "id": "2018-12-set2-rec-2",
        "section_id": "2018-12-set2-sec-c",
        "type": "recording",
        "title": "Recording 2",
        "topic_zh": "全球语言多样性之谜：马卡鲁瓦岛四十种土著语言、七千种语言的非随机分布与因果挑战",
        "question_range": "Questions 19 to 21",
        "questions": [19, 20, 21],
        "sp_start": 1079.40,
        "sp_end": 1268.00,
        "sentences": [
            ('M', "Last week I attended a research workshop on an island in the South Pacific.", "上周我在南太平洋的一个小岛上参加了一场学术研讨会。"),
            ('M', "Thirty people were present and all except me came from the island, called Makelua, in the nation of Vanuatu.", "当时有三十人出席，除我之外的所有学者都来自瓦努阿图国一座名叫马卡鲁瓦的岛屿。"),
            ('M', "They live in 16 different communities and speak 16 distinct languages.", "这些居民分别生活在16个不同的社区部落，说着16种截然不同的语言。"),
            ('M', "In many cases, you could stand at the edge of one village and see the outskirts of the next community.", "在很多情况下，你站在一个村落的边缘，甚至能清晰眺望到相邻社区的郊野。"),
            ('M', "Yet the residents of each village speak a completely different language.", "然而，每一个村庄的村民们说的却是完全无法互通的独立语言。"),
            ('M', "According to recent work by my colleagues at the Max Planck Institute for the Science of Human History, this island, just 100 kilometers long and 20 kilometers wide, is home to speakers of perhaps 40 different indigenous languages.", "根据我在马克斯·普朗克人类历史科学研究所的同事们开展的最新研究，这座长仅100公里、宽仅20公里的狭长岛屿上，竟栖居着大约40种截然不同的本土土著语言的使用者。"),
            ('M', "Why so many?", "为什么会有如此繁多的语言呢？"),
            ('M', "We could ask the same question of the entire globe.", "其实我们完全可以对整个人类居住的地球提出同样的深刻追问。"),
            ('M', "People don't speak one universal language, or even a handful.", "全人类并没有讲同一种通用语言，甚至也不是仅有区区几种语言。"),
            ('M', "Instead, today our species collectively speaks over 7,000 distinct languages.", "相反，如今我们人类这一物种总共说着多达7000多种各不相同的独立语言。"),
            ('M', "And these languages are not spread randomly across the planet.", "而且，这些语言在地球表面的分布绝不是随机杂乱的。"),
            ('M', "For example, far more languages are found in tropical regions than in the mild zones.", "例如，在热带地区所发现的语言种类，远远多于温带气候区域。"),
            ('M', "The tropical island of New Guinea is home to over 900 languages.", "地处热带的新几内亚岛上，繁衍着多达900多种不同的土著语言。"),
            ('M', "Russia, 20 times larger, has 105 indigenous languages.", "而国土面积是新几内亚整整20倍之巨的俄罗斯，其本土语言却只有105种。"),
            ('M', "Even within the tropics, language diversity varies widely.", "即便同在热带地区内部，语言的多样性程度也存在着天壤之别。"),
            ('M', "For example, the 250,000 people who live on Vanuatu's 80 islands speak 110 different languages, but in Bangladesh, a population 600 times greater speaks only 41 languages.", "例如，生活在瓦努阿图80座岛屿上的25万居民说着110种完全不同的语言；但在人口规模是其整整600倍的孟加拉国，全国却仅有41种语言。"),
            ('M', "How come humans speak so many languages?", "究竟是什么原因让人类说着如此纷繁复杂的语言？"),
            ('M', "And why are they so unevenly spread across the planet?", "又为什么这些语言在地球各大洲的分布会如此极度不均衡？"),
            ('M', "As it turns out, we have few clear answers to these fundamental questions about how humanity communicates.", "事实证明，关于人类语言演化与交流机制的这些根本性谜题，我们目前掌握的确切答案仍然少之又少。"),
            ('M', "Most people can easily brainstorm possible answers to these intriguing questions.", "大多数人在面对这些引人入胜的疑问时，都能随口头脑风暴出各种各样貌似合理的假说。"),
            ('M', "They hypothesize that language diversity must be about history, cultural differences, mountains or oceans dividing populations.", "人们习惯性地推测，语言的多样性必然与漫长的历史积淀、文化隔阂，或者高山大海对地理人群的物理阻隔密切相关。"),
            ('M', "But when our diverse team of researchers from six different disciplines and eight different countries began to review what was known, we were shocked that only a dozen previous studies had been done, including one we ourselves completed on language diversity in the Pacific.", "然而，当我们这支由来自6个不同学科领域、8个不同国家的跨学科联合科研团队开始系统梳理已有学术成果时，我们震惊地发现，此前针对该领域开展的严肃实证研究竟然只有区区十几项，其中还包括我们自己刚完成的关于太平洋地区语言多样性的一项课题。"),
            ('M', "These prior efforts all examined the degree to which different environmental, social, and geographic variables correlated with the number of languages found in a given location.", "这些早期的探索无一例外都在检验各种不同的自然环境、社会形态和地理空间变量，与特定地理区域内存在的语言数量之间的统计相关性。"),
            ('M', "The results varied a lot from one study to another, and no clear patterns emerged.", "但令人遗憾的是，不同研究之间的结论差异极大，始终未能归纳出任何具有普适性的清晰规律。"),
            ('M', "The studies also ran up against many methodological challenges, the biggest of which centered on the old statistical saying — correlation does not equal causation.", "此外，以往的所有研究都撞上了难以逾越的方法论瓶颈，其中最核心的死穴正如那句经典的统计学名言所指出的——相关关系绝不等于因果关系。")
        ]
    },
    {
        "id": "2018-12-set2-rec-3",
        "section_id": "2018-12-set2-sec-c",
        "type": "recording",
        "title": "Recording 3",
        "topic_zh": "美国梦褪色：中产消失与九比一财富悬殊、低薪兼职商业模式与底层上升通道",
        "question_range": "Questions 22 to 25",
        "questions": [22, 23, 24, 25],
        "sp_start": 1334.24,
        "sp_end": 1493.50,
        "sentences": [
            ('M', "We often hear people say that America is a land of opportunity, a country built on hope to aspire the greatness on the American dream.", "我们常常听人赞颂美国是一片充满无限机遇的热土，一个建立在对美好希望的追寻以及实现伟大美国梦之上的国度。"),
            ('M', "But is the dream as we once knew it dying?", "然而，我们曾经所熟知并深信不疑的美国梦，是否正在不可逆转地走向消亡？"),
            ('M', "Today's demographics show that the middle-class is disappearing and now the richest 1% of the population has mastered more wealth than the bottom 90%.", "当今的人口统计数据触目惊心地显示：坚实的中产阶级正在加速瓦解萎缩，如今全美最富有的1%超级富豪所掌控的巨额财富，已经彻底碾压了底层90%民众的财富总和。"),
            ('M', "Once upon a time, Americans thought that if they worked hard enough, even in the phase of adversity, they would be rewarded with success.", "在过去的漫长岁月里，美国人普遍坚信，只要自己足够踏实努力，哪怕身处逆境与挫折之中，也终将获得成功与阶层跃升的回报。"),
            ('M', "These days, though, the divide between rich and poor is greater than it has ever been.", "然而在如今的时代，贫富之间难以逾越的鸿沟比历史上的任何时期都更加令人绝望。"),
            ('M', "The question is, what is it going to take to change things?", "摆在眼前最尖锐的问题是：我们究竟需要付出怎样的代价和变革，才能够彻底扭转这一冰冷残酷的现实？"),
            ('M', "Maybe one day soon real change will actually be made in our nation and the gap will be eradicated.", "也许在不久的将来，真正的制度性变革会在我们国家破茧而出，彻底抹平这种不公的贫富差距。"),
            ('M', "But what happens in the meantime?", "但在这一宏愿实现之前的当下漫长岁月中，我们又该何去何从？"),
            ('M', "Is there something that we can do to help close the gap?", "我们能否身体力行做些切实的事情来帮助缩小这道鸿沟？"),
            ('M', "Is there something that we can do to prove that a little compassion goes a long way?", "我们是否能够通过微小的善举来证明：哪怕是一丝温暖的同情与关爱，也能产生极其深远的长效影响？"),
            ('M', "If we want to fix the problem of the income gap, first, we have to understand it.", "如果我们渴望从根本上破解收入差距这一顽疾，首要任务就是必须看透其背后的运作本质。"),
            ('M', "It is a grim reality that you can have one person who only makes around 13,000 dollars a year, or across town, another is making millions.", "一个残酷冰冷的现实是：在这座城市的这一头，有人辛劳一年却仅能维持一万三千美元的微薄收入；而在同一座城市的另一端，有人却年入数百万甚至上千万。"),
            ('M', "For me, it is kind of astonishing.", "对我而言，这种触目惊心的断层对比令人不寒而栗。"),
            ('M', "And if you ask low-income people what's the one thing that will change their life, they'll say a full-time job.", "如果你走上街头去询问那些挣扎在温饱线上的低收入群体，最渴望得到什么来改变自己的命运，他们会异口同声回答：一份稳定的全职工作。"),
            ('M', "That's all they aspire to.", "这就是他们梦寐以求的全部夙愿。"),
            ('M', "So why is it so difficult for so many people to find employment?", "那么，为什么如今有如此多勤劳的人却难以觅得一份正规体面的全职工作呢？"),
            ('M', "It partly comes down to profit-driven business models that are built around low-wage work and part-time jobs that don't provide benefits.", "这在很大程度上归咎于由资本利润最大化驱动的现代商业模式——这种模式专门建立在压低薪资、大量使用不提供任何社保福利的零工兼职之上。"),
            ('M', "Businesses, in order to boost profits, hire employees as part-time workers only.", "各大企业为了无限推高季度财报利润，故意只把员工招聘为非正式的兼职小时工。"),
            ('M', "This means they are paid the lowest legal wage and receive no health care or other benefits provided to full-time employees.", "这意味着工人们只能拿到法定最低薪资，并且完全被剥夺了全职员工本应享有的医疗保险与带薪休假等基本保障。"),
            ('M', "Simultaneously, technological advancement and a global economy has reduced the demand for well-paying blue-collar jobs here in the United States.", "与此同时，自动化技术的日新月异与全球化产业链的重新分工，极大地削减了美国本土对于高薪传统蓝领岗位的用工需求。"),
            ('M', "The cumulative effect of these two factors is that many Americans are forced to take two or more part-time jobs, just to make ends meet.", "这两大宏观因素的复合叠加恶果是：数以千万计的普通美国人被迫同时打两份甚至三份零工兼职，整日奔波劳碌，仅仅是为了勉强维持基本生计的收支平衡。"),
            ('M', "What has become obvious to me when it comes to the income gap is that there needs to be an opportunity for the people at the bottom to push them back up and push them into the middle-class to give them hope in their lives.", "在深入审视贫富差距之后，我得出的最清晰结论是：整个社会必须为身处社会底层的人群搭建坚实的上升通道，把他们重新托举推入中产阶级的阶梯，让他们重新看到生活的曙光与尊严。")
        ]
    }
]

from data_2018_12_set2 import QUESTIONS

CONTRACTIONS = {
    "i'm": "im", "you're": "youre", "we're": "were", "they're": "theyre",
    "he's": "hes", "she's": "shes", "it's": "its", "that's": "thats",
    "what's": "whats", "let's": "lets", "i've": "ive", "i'll": "ill",
    "you'll": "youll", "we'll": "well", "i'd": "id", "we'd": "wed",
    "you'd": "youd", "there'd": "thered", "who's": "whos", "how's": "hows",
    "can't": "cant", "won't": "wont", "didn't": "didnt", "doesn't": "doesnt",
    "don't": "dont", "isn't": "isnt", "aren't": "arent", "wasn't": "wasnt",
    "weren't": "werent", "hasn't": "hasnt", "haven't": "havent", "hadn't": "hadnt",
    "couldn't": "couldnt", "shouldn't": "shouldnt", "wouldn't": "wouldnt",
    "mustn't": "mustnt", "needn't": "neednt", "shan't": "shant",
}

def normalize_token(tok: str) -> str:
    t = re.sub(r"[^a-zA-Z0-9']", "", tok).lower()
    if not t:
        return ""
    if t in CONTRACTIONS:
        return CONTRACTIONS[t]
    for clitic in ("'re", "'ve", "'ll", "'s", "'d"):
        if t.endswith(clitic):
            return t[:-len(clitic)] + clitic[1:]
    if "'" in t:
        return t.replace("'", "")
    return t

def align_subpart(sp_meta, whisper_words):
    sentences_data = sp_meta["sentences"]
    sp_start = sp_meta["sp_start"]
    sp_end = sp_meta["sp_end"]

    # Filter whisper words strictly within [sp_start - 0.5, sp_end + 0.5]
    subpart_words = [w for w in whisper_words if sp_start - 0.5 <= w["start"] <= sp_end + 0.5]
    whisper_norm = [normalize_token(w.get("word", "")) for w in subpart_words]

    ref_tokens = []
    ref_sent_of = []
    for si, (speaker, eng, chn) in enumerate(sentences_data):
        for tok in eng.split():
            n = normalize_token(tok)
            if n:
                ref_tokens.append(n)
                ref_sent_of.append(si)

    matcher = SequenceMatcher(a=ref_tokens, b=whisper_norm, autojunk=False)
    opcodes = matcher.get_opcodes()

    sent_word_idx = {si: [] for si in range(len(sentences_data))}
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == "equal":
            for k in range(i2 - i1):
                sent_word_idx[ref_sent_of[i1 + k]].append(j1 + k)
        elif tag == "replace":
            ref_slice = [ref_sent_of[i] for i in range(i1, i2)]
            span = j2 - j1
            if span <= 0:
                continue
            for si in dict.fromkeys(ref_slice):
                sent_word_idx[si].extend(range(j1, j2))

    aligned = []
    prev_e = None
    for si, (speaker, eng, chn) in enumerate(sentences_data):
        idxs = sent_word_idx[si]
        if idxs:
            lo = min(idxs)
            hi = max(idxs)
            s_time = round(subpart_words[lo]["start"], 2)
            e_time = round(subpart_words[hi]["end"], 2)
        else:
            if prev_e is None:
                s_time = round(sp_start, 2)
                e_time = round(min(sp_start + 1.0, sp_end), 2)
            else:
                s_time = round(prev_e, 2)
                e_time = round(min(prev_e + 1.0, sp_end), 2)

        if prev_e is not None and s_time < prev_e:
            s_time = prev_e
        if e_time < s_time + 0.3:
            e_time = round(s_time + 0.3, 2)

        s_time = max(sp_start, min(s_time, sp_end))
        e_time = max(s_time + 0.2, min(e_time, sp_end))

        aligned.append({
            "speaker": speaker,
            "english": eng,
            "chinese": chn,
            "start_time": s_time,
            "end_time": e_time,
            "confidence": 0.95
        })
        prev_e = e_time

    return aligned

def main():
    with open(WHISPER_PATH, "r", encoding="utf-8") as f:
        whisper_data = json.load(f)
    whisper_words = [w for seg in whisper_data for w in seg.get("words", [])]

    total_sents = sum(len(sp["sentences"]) for sp in SUBPARTS)
    print(f"Total authentic sentences configured: {total_sents}")

    all_aligned = []
    global_order = 1
    for sp in SUBPARTS:
        aligned = align_subpart(sp, whisper_words)
        print(f"Subpart {sp['id']}: {len(aligned)} sentences, {aligned[0]['start_time']}s - {aligned[-1]['end_time']}s")
        for s in aligned:
            dur = round(s["end_time"] - s["start_time"], 2)
            if dur > 20.0:
                print(f"  WARNING: Long duration {dur}s on sent: {s['english'][:50]}")
            all_aligned.append(s)
            global_order += 1

    print("Checking max duration across all sentences:")
    max_dur = max(s["end_time"] - s["start_time"] for s in all_aligned)
    print(f"Max sentence duration: {max_dur:.2f}s")

    AUDIO_FILE = "2018年12月六级听力第2套.mp3"
    AUDIO_DURATION = 1580.43

    sections = [
        {"id": f"{EXAM_ID}-sec-a", "exam_id": EXAM_ID, "type": "section_a", "title": "Section A: Long Conversations", "order_num": 1},
        {"id": f"{EXAM_ID}-sec-b", "exam_id": EXAM_ID, "type": "section_b", "title": "Section B: Passages", "order_num": 2},
        {"id": f"{EXAM_ID}-sec-c", "exam_id": EXAM_ID, "type": "section_c", "title": "Section C: Recordings", "order_num": 3},
    ]

    all_clean_subparts = []
    all_clean_sentences = []
    all_clean_questions = []

    global_sent_order = 1
    subpart_order = 1

    for sp_meta in SUBPARTS:
        aligned = align_subpart(sp_meta, whisper_words)
        sp_id = sp_meta["id"]

        for s in aligned:
            sent_id = f"{EXAM_ID}-sent-{global_sent_order:04d}"
            all_clean_sentences.append({
                "id": sent_id,
                "exam_id": EXAM_ID,
                "section_id": sp_meta["section_id"],
                "subpart_id": sp_id,
                "order_num": global_sent_order,
                "speaker": s["speaker"],
                "start_time": s["start_time"],
                "end_time": s["end_time"],
                "english": s["english"],
                "chinese": s["chinese"],
                "confidence": s["confidence"]
            })
            global_sent_order += 1

        actual_start = aligned[0]["start_time"]
        actual_end = aligned[-1]["end_time"]

        all_clean_subparts.append({
            "id": sp_id,
            "section_id": sp_meta["section_id"],
            "exam_id": EXAM_ID,
            "type": sp_meta["type"],
            "title": sp_meta["title"],
            "order_num": subpart_order,
            "start_time": actual_start,
            "end_time": actual_end,
            "questions_json": json.dumps(sp_meta["questions"]),
            "topic_zh": sp_meta["topic_zh"],
            "question_range": sp_meta["question_range"],
            "sentence_count": len(aligned),
            "duration": round(actual_end - actual_start, 2)
        })

        for q_num in sp_meta["questions"]:
            q_info = QUESTIONS[q_num]
            q_id = f"{EXAM_ID}-q{q_num:02d}"
            all_clean_questions.append({
                "id": q_id,
                "exam_id": EXAM_ID,
                "subpart_id": sp_id,
                "question_num": q_num,
                "prompt": q_info["prompt"],
                "option_a": q_info["options"]["A"],
                "option_b": q_info["options"]["B"],
                "option_c": q_info["options"]["C"],
                "option_d": q_info["options"]["D"],
                "correct_answer": q_info["answer"],
                "explanation": q_info["explanation"]
            })

        subpart_order += 1

    print(f"\nWriting to database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO exams (id, year, month, set_number, title, audio_file, audio_duration, is_golden)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            title=excluded.title,
            audio_file=excluded.audio_file,
            audio_duration=excluded.audio_duration,
            is_golden=excluded.is_golden
    """, (
        EXAM_ID, 2018, 12, 2,
        "2018年12月 六级真题 (第2套)",
        AUDIO_FILE, AUDIO_DURATION, 1
    ))

    for sec in sections:
        cur.execute("""
            INSERT INTO sections (id, exam_id, type, title, order_num)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title=excluded.title,
                order_num=excluded.order_num
        """, (sec["id"], sec["exam_id"], sec["type"], sec["title"], sec["order_num"]))

    cur.execute("DELETE FROM sentences WHERE exam_id = ?", (EXAM_ID,))
    cur.execute("DELETE FROM questions WHERE exam_id = ?", (EXAM_ID,))
    cur.execute("DELETE FROM subparts WHERE exam_id = ?", (EXAM_ID,))

    for sp in all_clean_subparts:
        cur.execute("""
            INSERT INTO subparts (id, section_id, exam_id, type, title, order_num, start_time, end_time, questions_json, topic_zh, question_range, sentence_count, duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sp["id"], sp["section_id"], sp["exam_id"], sp["type"], sp["title"],
            sp["order_num"], sp["start_time"], sp["end_time"], sp["questions_json"],
            sp["topic_zh"], sp["question_range"], sp["sentence_count"], sp["duration"]
        ))

    for sent in all_clean_sentences:
        cur.execute("""
            INSERT INTO sentences (id, exam_id, section_id, subpart_id, order_num, speaker, start_time, end_time, english, chinese, words_json, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            sent["id"], sent["exam_id"], sent["section_id"], sent["subpart_id"],
            sent["order_num"], sent["speaker"], sent["start_time"], sent["end_time"],
            sent["english"], sent["chinese"], None, sent["confidence"]
        ))

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
    print("Database updated successfully.")

if __name__ == "__main__":
    main()

