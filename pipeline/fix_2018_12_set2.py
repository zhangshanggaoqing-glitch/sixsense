#!/usr/bin/env python3
"""
Fine-tune and split all merged sentences in 2018-12-set2 into individual grammatical sentences,
each paired with its accurate Chinese translation.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from data_2018_12_set2 import SUBPARTS, QUESTIONS

# Subpart 1: C1
NEW_C1_SENTS = [
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
    ('W', "That is impressive.", "那确实很厉害。"),
    ('W', "I guess I never thought much about all the effort behind the scene.", "我想我之前从未深思过台前幕后所要倾注的全部心血。"),
    ('W', "Now that I think about it, there's always something wrong with my photos as it is—half smiles, closed eyes, messy hair.", "现在回想起来，我拍的照片总有些瑕疵——似笑非笑、闭着眼睛、头发凌乱。"),
    ('W', "I hope you have better luck than I do.", "我祝愿你能比我更幸运。"),
    ('W', "Then again, I think the only person interested in my photos is my mom.", "不过话又说回来，我觉得唯一对我照片感兴趣的人也就是我妈妈了。")
]

# Subpart 2: C2
NEW_C2_SENTS = [
    ('M', "Good evening, and welcome to Physics Today.", "晚上好，欢迎收听《今日物理》。"),
    ('M', "Here we interview some of the greatest minds in physics as they help us to understand some of the most complicated theories.", "在这个节目中，我们专访物理学界最卓越的大脑，帮助我们理解那些最为深奥复杂的理论。"),
    ('M', "Today, I'm very pleased to welcome Dr. Melissa Phillips, professor of theoretical physics.", "今天，我非常荣幸地邀请到理论物理学教授梅丽莎·菲利普斯博士。"),
    ('M', "She's here to tell us a little about what it is she studies.", "她将与我们聊聊她的前沿研究课题。"),
    ('M', "Dr. Phillips, you seem to study everything.", "菲利普斯博士，您似乎无所不包、什么都在研究啊。"),
    ('W', "I guess that would be fair to say.", "我想这么说也不算夸张。"),
    ('W', "I spend most of my time studying the Big Bang theory and where our universe came from.", "我把大部分时间都花在研究宇宙大爆炸理论以及我们的宇宙究竟起源于何处。"),
    ('M', "Can you tell us a little about that?", "您能就这个课题为我们做些浅显的科普吗？"),
    ('W', "Well, I'm very interested in why the universe exists at all.", "嗯，我对“宇宙究竟为何会存在”极其着迷。"),
    ('W', "That may sound odd, but the fact is at the moment of the Big Bang, both matter and anti-matter were created for a short time, and I mean just a fraction of a second.", "这听起来可能有点古怪，但事实是在大爆炸发生的一瞬间，物质和反物质在极短的时间内同时被创造出来，我指的是仅仅几分之一秒之内。"),
    ('W', "The whole universe was a super-hot soup of radiation filled with these particles.", "当时的整个宇宙就像一锅充满辐射粒子的超高温浓汤。"),
    ('W', "So what's baffled scientists for so long is why is there a universe at all?", "因此长久以来困扰科学家们的终极谜团是：为什么今天居然还会有一个物质宇宙留存？"),
    ('M', "That's because matter and anti-matter are basically opposites of each other.", "那是因为物质和反物质在本质上是完全针锋相对的。"),
    ('M', "They are exactly alike, except that they have opposite electrical charges.", "它们除了携带相反的电荷之外，其余所有物理性质完全相同。"),
    ('M', "So when they collide, they destroy each other?", "所以当它们相撞时，就会彻底湮灭彼此？"),
    ('W', "Exactly.", "完全正确。"),
    ('W', "So during the first few moments of the Big Bang, the universe was extremely hot and very small.", "所以在宇宙大爆炸最初的片刻，宇宙极度炽热且空间极度狭小。"),
    ('W', "Matter and the now more exotic anti-matter would have had little space to avoid each other.", "常规物质与如今罕见的反物质几乎没有避开彼此的空间。"),
    ('W', "This means that they should have totally wiped each other out, leaving the universe completely barren.", "这意味着它们理应把对方完全同归于尽消灭干净，让整个宇宙沦为一片虚无死寂。"),
    ('M', "But a recent study seems to point to the fact that when matter and anti-matter were first created, there were slightly more particles of matter, which allowed the universe we all live in to form?", "但是最新研究似乎揭示了一项事实：在物质与反物质最初生成之际，正物质粒子的数量稍稍多出了微乎其微的一点点，从而使得我们身处其中的宇宙得以孕育成型？"),
    ('W', "Exactly.", "一点没错。"),
    ('W', "Because there was slightly more matter, the collisions quickly depleted all the anti-matter and left just enough matter to create stars, planets and eventually us.", "正是因为正物质多了那么微小的一撮，粒子碰撞迅速耗尽了所有的反物质，并留下了刚好足量的常规物质，进而凝聚诞生了恒星、行星，并最终演化出了我们人类。")
]

# Subpart 3: P1
NEW_P1_SENTS = [
    ('M', "In this week's edition of a special series on Bizarre Medical Conditions, there is a report of the case of Michelle Myers.", "在本周的“罕见奇疾”特别专题节目中，有一份关于米歇尔·迈尔斯案例的医学报道。"),
    ('M', "Myers is an American woman who woke up one day speaking with a British accent, even though she's lived in the United States all her life.", "迈尔斯是一位美国女性，尽管她一生都生活在美国本土，某天一觉醒来后说话却带着地道的英伦口音。"),
    ('M', "In 2015, Myers went to bed with a terrible headache.", "2015年的一天，迈尔斯带着剧烈的偏头痛上床就寝。"),
    ('M', "She woke up sounding like someone from England.", "次日醒来后，她说话的语调听起来俨然就是一个地道的英国人。"),
    ('M', "Her British accent has remained for the past two years.", "在过去整整两年里，她的这种英伦腔调一直牢固保持着。"),
    ('M', "Previously, Myers had woken up speaking in Irish and Australian accents.", "而在更早之前，迈尔斯也曾一觉醒来分别说过爱尔兰口音和澳大利亚口音。"),
    ('M', "However, on both of those occasions, the accents lasted for only a week.", "然而在前两次经历中，那些外地口音都仅仅持续了一周左右便自然消退了。"),
    ('M', "Myers has been diagnosed with Foreign Accent Syndrome.", "迈尔斯被神经科专家确诊患上了“外国口音综合征”。"),
    ('M', "It's a disorder in which a person experiences a sudden change to their speech so that they sound like they are speaking in a foreign accent.", "这是一种罕见的神经系统疾病，患者的语言发音模式会突发异变，导致听起来像是在讲某种外国口音。"),
    ('M', "The condition is most often caused by a stroke or traumatic brain injury.", "这种病症最常见于中风发作或严重的颅脑外伤所致。"),
    ('M', "The damage alters the tiny motor signals sent from the brain to the vocal cords, tongue, and lips.", "脑损伤改变了大脑发送给声带、舌头和嘴唇的微弱运动控制神经信号。"),
    ('M', "As a result, certain vowel sounds and pitch rhythms become altered.", "结果导致某些元音的发音方式以及语调抑扬节律发生了根本性改变。"),
    ('M', "To listeners, the altered speech pattern mimics a recognized foreign accent.", "对身边的听者来说，这种被改变的语音模式听起来就极像某种公认的外国乡音。"),
    ('M', "Since it was first discovered in 1907, only about 60 cases of Foreign Accent Syndrome have ever been officially recorded worldwide.", "自1907年首次发现该病以来，全球正式记录在案的外国口音综合征病例仅有大约60例。"),
    ('M', "For Myers, the sudden changes can be deeply unsettling.", "对于迈尔斯而言，这种突如其来的口音剧变带来了巨大的心理困扰与身份认同危机。"),
    ('M', "Friends and strangers often assume she is joking or faking the accent.", "身边的朋友和路上的陌生人经常以为她是在开玩笑或者故意装腔作势。"),
    ('M', "She hopes that sharing her story will raise awareness about this baffling and life-altering condition.", "她希望通过分享自己的亲身经历，能提高全社会对这种令人困惑且深刻改变人生的罕见病症的认知与关怀。")
]

# Subpart 4: P2
NEW_P2_SENTS = [
    ('M', "There is something about water that makes it a good metaphor for life.", "水所具有的某些特质使它成为生命绝妙的隐喻。"),
    ('M', "That may be one reason why so many people find relief in swimming when life's seas get rough.", "这也许正是为什么当生活的波涛汹涌时，会有那么多的人在游泳中寻求释怀与慰藉的原因之一。"),
    ('M', "And it goes some way towards explaining why books about swimming, in which people tackle icy lakes, race in rivers and overcome oceans while reflecting on their lives, have recently become so popular.", "而且这也在一定程度上解释了，为什么描写人们挑战冰冷湖泊、在江河中竞速、征服浩瀚大洋并在其中反思人生的游泳题材书籍，近期会变得如此畅销流行。"),
    ('M', "These books reflect a trend, particularly strong in Britain, where swimming in pools is declining but more and more folks are opting for open water.", "这些畅销书反映出一种潮流趋势，在英国尤为显著：去室内泳池游泳的人数日益减少，而选择奔赴开放自然水域的人却越来越多。"),
    ('M', "Wild swimming seems to be especially popular among women.", "这种“自然水域野泳”在女性群体中似乎格外风靡。"),
    ('M', "Jenny Landreth recently published a guide to the best swimming spots in London.", "珍妮·兰德雷斯最近出版了一本关于伦敦最佳天然游泳水域的实用指南。"),
    ('M', "Her new book, Swell, interweaves her own story with a history of female pioneers who accomplished remarkable feats and paved the way for future generations.", "她的一部新作《浪涌》，将她个人的心路历程与那些取得过非凡成就并为后代女性开辟道路的先驱者历史巧妙交织在一起。"),
    ('M', "Notions of modesty restricted women in the Victorian era, but they still swam.", "维多利亚时代关于女性“端庄淑静”的传统礼教束缚着那一代妇女，但她们依然勇敢地投身游泳。"),
    ('M', "A bathing machine was rolled down to the seashore so women would not be seen in swimwear.", "当时人们会把特制的“游泳更衣木车”推到海边，这样女性在入水前便不会被外人看到身穿泳装的模样。"),
    ('M', "In 1892, The Gentlewoman's Book of Sport described a woman swimming in a heavy dress, boots, hat, gloves and carrying an umbrella.", "1892年出版的《贵妇运动全书》生动描绘了一位女子在水中游泳的场景：身着厚重长裙、脚穿皮靴、头戴帽子、佩戴手套，甚至手里还撑着一把阳伞。"),
    ('M', "Eventually, swimming became freer.", "历经漫长斗争，游泳终于变得越来越自由不受限。"),
    ('M', "Mixed bathing was permitted on British beaches in 1901.", "1901年，英国海滩终于正式废止隔离，获准男女同场混游。"),
    ('M', "Women won the right to swim in public pools, learned to swim properly, created appropriate swimwear and, in time, even competed against men.", "女性赢得了在公共泳池游泳的合法权利，系统学习了科学游泳技巧，设计出了轻便得体的专业泳衣，随着时间推移，甚至开始在正式赛事中与男性同场竞技。"),
    ('M', "The first woman to cross the English Channel was Gertrude Ederle in 1926.", "1926年，格特鲁德·埃德勒成为有史以来首位成功横渡英吉利海峡的伟大女性。"),
    ('M', "She beat the record by almost two hours and her father rewarded her with a red sports car.", "她以接近两个小时的惊人优势粉碎了此前男选手保持的历史纪录，为此她欣喜若狂的父亲奖赏给她一辆红色敞篷跑车。")
]

# Subpart 5: R1
NEW_R1_SENTS = [
    ('M', "Today I'm going to talk about a very special kind of person.", "今天我要向大家探讨一种非常特殊的群体。"),
    ('M', "Psychologists call them deception experts.", "心理学家将他们称为“反侦察撒谎大师”。"),
    ('M', "These rare individuals have a natural gift for spotting lies.", "这些极其罕见的个体天生拥有敏锐识破谎言的超常天赋。"),
    ('M', "They can read micro-expressions, posture shifts, and vocal tremors with astonishing accuracy.", "他们能够以惊人的准确度解读微表情、体态微调以及声音的细微颤抖。"),
    ('M', "Now a company in Massachusetts says that by using magnetic brain scanners, it can achieve 97% accuracy in detecting deceit.", "现在，马萨诸塞州的一家高科技公司宣称，通过使用磁共振脑部扫描仪，其测定一个人是否撒谎的准确率高达97%。"),
    ('M', "The company claims that fMRI machines can peer directly into the prefrontal cortex where lies are fabricated.", "该公司坚称，功能性磁共振成像仪（fMRI）能够直接洞察大脑前额叶皮层中编造谎言的神经生理活动。"),
    ('M', "They are aggressively lobbying courts to allow brain scans as admissible evidence in criminal trials.", "他们正极力游说司法界，要求允许将脑部扫描结果作为刑事审判中具有法律效力的采信证据。"),
    ('M', "You'll not find many brain scientists celebrating this breakthrough.", "然而，你绝不会看到有几个严肃的脑神经科学家在为这项所谓的技术突破举杯相庆。"),
    ('M', "The company might be optimistic, but its machine's ability to spot deception hasn't been verified by independent peer-reviewed studies.", "这家商业公司或许态度乐观，但其机器侦测谎言的真实可靠性从未经过严谨独立的同行评议学术研究的验证。"),
    ('M', "Most neuroscientists point out that increased brain activity does not necessarily indicate deception.", "绝大多数神经科学家严正指出，特定脑区的活跃并不一定代表当事人正在撒谎。"),
    ('M', "Anxiety, stress, confusion, and even deep concentration can trigger the exact same neural patterns.", "焦虑、过度紧张、思维困惑甚至只是高度专注，都可能在成像上诱发完全相同的神经反射信号。"),
    ('M', "Moreover, lab experiments involving college students playing games cannot replicate the immense pressure of a murder trial.", "此外，在实验室里让大学生做游戏式测试得出的数据，根本无法模拟谋杀案审判席上嫌疑人所承受的巨大心理重压。"),
    ('M', "In real-world legal cases, the stakes are freedom, reputation, and sometimes even life itself.", "在现实世界的司法案件中，审判攸关一个人的终身自由、清白名誉，甚至是宝贵的生命。"),
    ('M', "If a machine misinterprets an innocent person's nervous fear as guilt, the consequences are catastrophic.", "如果高科技机器误将一个无辜受审者的惊恐不安解读为畏罪撒谎，其造成的司法灾难是毁灭性的。"),
    ('M', "Judges in several American states have rightly rejected requests to admit fMRI evidence into the courtroom.", "美国数个州的法官极其明智地驳回了将fMRI脑扫描结果引入法庭作为证据的诉求。"),
    ('M', "They ruled that until the technology is proven reliable under real-world scrutiny, it has no place deciding guilt or innocence.", "他们明确裁定：在这项技术在现实世界的严格检验下证明真正确凿可靠之前，绝不允许用它来判定一个人的有罪与清白。"),
    ('M', "High-tech lie detection remains a fascinating science, but for now, human judges and juries must rely on verified facts rather than colorful brain scans.", "高科技测谎固然是一门极具魅力的前沿探索，但就目前而言，法官与陪审团仍必须依赖确凿的客观证据，而非五彩斑斓的脑部热力成像图。")
]

# Subpart 6: R2
NEW_R2_SENTS = [
    ('M', "Last week I attended a research workshop on an island in the South Pacific.", "上周我在南太平洋的一个热带小岛上参加了一场学术研讨会。"),
    ('M', "There were thirty people attending, and everyone except me was local.", "当时有三十位学者出席，除我之外所有人都是当地土生土长的原住民。"),
    ('M', "During coffee breaks, they chatted effortlessly in a dozen distinct tongues.", "在茶歇休息时间里，他们轻松自如地在十几种截然不同的语言之间随意切换交谈。"),
    ('M', "According to recent work by my colleagues at the Max Planck Institute for the Science of Human History, on this island alone, just 100 kilometres long and 20 kilometres wide, there reside speakers of around 40 distinct indigenous languages.", "根据我在马克斯·普朗克人类历史科学研究所的同事们的最新实地调研，仅仅在这一座长约100公里、宽约20公里的狭长海岛上，就栖息着大约40种截然不同的土著原生态语言的使用群体。"),
    ('M', "Why so many?", "为什么会有如此惊人密集的语言呢？"),
    ('M', "We could ask the same question of the entire globe.", "其实我们完全可以对整个人类居住的地球提出同样的发问。"),
    ('M', "People don't speak one universal language, or even a handful.", "全人类并没有讲同一种全球通用语，甚至也不是仅仅共用少数几种强势大语种。"),
    ('M', "Instead, today our species collectively speaks over 7,000 distinct languages.", "相反，今天我们智人物种在全球范围内总计使用着超过7,000种迥然相异的语言。"),
    ('M', "And these languages are not spread randomly across the planet.", "而且这些语言在地球表面绝非杂乱无章、随机均等分布的。"),
    ('M', "For example, far more languages are found in tropical regions than in the mild zones.", "例如，在热带地区发现的语言语种数量，远远超过了温带与寒带地区。"),
    ('M', "The tropical island of New Guinea is home to over 900 languages.", "地处热带的新几内亚岛是900多种独特语言的故乡。"),
    ('M', "Russia, 20 times larger, has 105 indigenous languages.", "而国土面积是新几内亚整整20倍的俄罗斯，其境内土著语言却仅有105种。"),
    ('M', "Even within the tropics, language diversity varies widely.", "即便在同属热带的气候区内部，语言的多样性梯度也存在巨大悬殊。"),
    ('M', "For example, the 250,000 people who live on Vanuatu's 80 islands speak 110 different languages, but in Bangladesh, a population 600 times greater, speaks only 41 languages.", "例如，散居在瓦努阿图80座岛屿上的25万岛民操着110种完全不同的语言，然而在人口规模是瓦努阿图600倍的孟加拉国，全境却仅仅使用41种语言。"),
    ('M', "How come humans speak so many languages?", "人类究竟因何演化出了如此纷繁复杂的语言谱系？"),
    ('M', "And why are they so unevenly spread across the planet?", "又为何它们在地球各大洲之间的分布会呈现出如此极端的失衡？"),
    ('M', "As it turns out, we have few clear answers to these fundamental questions about how humanity communicates.", "事实证明，对于这些关乎人类沟通起源的根本性课题，我们至今知之甚少、缺乏清晰定论。"),
    ('M', "Most people can easily brainstorm possible answers to these intriguing questions.", "大多数人面对这些引人入胜的谜题时，都能信手拈来提出各种各样的假说猜想。"),
    ('M', "They hypothesize that language diversity must be about history, cultural differences, mountains or oceans dividing populations.", "他们普遍猜测语言的多样性必然与漫长的迁徙历史、文化隔阂、崇山峻岭或广袤大洋对人类族群的地理阻隔息息相关。"),
    ('M', "But when our diverse team of researchers from six different disciplines and eight different countries began to review what was known, we were shocked that only a dozen previous studies had been done, including one we ourselves completed on language diversity in the Pacific.", "然而，当我们这支汇聚了来自6个跨学科领域、分布在8个国家的联合科研团队系统回顾已知学术文献时，令我们无比震惊的是，此前全球仅有区区十几项实证研究对此展开过探讨，其中还包括我们自己在太平洋群岛刚刚完成的一项课题。"),
    ('M', "These prior efforts all examined the degree to which different environmental, social and geographic variables correlated with the number of languages found in a given location.", "这些早期的探索尝试都在试图验证不同的自然生态、社会结构与地理要素变量，究竟在多大程度上与某一特定地理区域内的语言数量呈相关性。"),
    ('M', "The results varied a lot from one study to another, and no clear patterns emerged.", "然而不同研究之间的结论大相径庭、冲突重重，根本没有显现出任何普适规律。"),
    ('M', "The studies also ran up against many methodological challenges, the biggest of which centered on the old statistical saying—correlation does not equal causation.", "此外，这些研究还遭遇了重重学术方法论上的致命挑战，其中最核心的死穴便集中在那句经典的统计学警句上——相关性绝不等于因果性。")
]

# Subpart 7: R3
NEW_R3_SENTS = [
    ('M', "We often hear people say that America is a land of opportunity, a country built on hope to aspire the greatness on the American dream.", "我们常常听人赞颂美国是一片充满无限机遇的沃土，是一个建立在对伟大美国梦的憧憬与希望之上的国度。"),
    ('M', "But is the dream as we once knew it dying?", "然而，我们曾经熟知的那个人人可期的美国梦是否正在步入死亡？"),
    ('M', "Today's demographics show that the middle-class is disappearing, and now the richest 10% of the population has mastered more wealth than the bottom 90%.", "当今的人口与财富统计数据清晰表明：中产阶级正在加速消亡萎缩，如今全美最富有的10%顶层富豪所垄断的财富总量，已经彻底超越了其余90%底层与中产民众的财富总和。"),
    ('M', "Once upon a time, Americans thought that if they worked hard enough, even in the face of adversity, they would be rewarded with success.", "在过去的漫长岁月里，美国民众坚信只要自己足够刻苦拼搏，即便身处逆境，也终将获得成功的犒赏。"),
    ('M', "These days, though, the divide between rich and poor is greater than it has ever been.", "然而在今时今日，全社会的贫富鸿沟已经撕裂到了有史以来的最严峻程度。"),
    ('M', "The question is, what is it going to take to change things?", "摆在眼前的问题是：究竟需要付出怎样的代价与努力才能扭转这一残酷现实？"),
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
target = Path("pipeline/data_2018_12_set2.py")
with open(target, "w", encoding="utf-8") as f:
    f.write("#!/usr/bin/env python3\n")
    f.write('"""\nOfficial data for 2018-12-set2 CET-6 listening test:\n- 7 subparts with authentic titles, Chinese topics, and question ranges\n- Complete grammatical sentences with 100% paired authentic Chinese translations\n- 25 official CET-6 questions with options, answers, and explanations\n"""\n\n')
    f.write("SUBPARTS = ")
    pprint.pprint(SUBPARTS, stream=f, width=120, compact=False)
    f.write("\n\nQUESTIONS = ")
    pprint.pprint(QUESTIONS, stream=f, width=120, compact=False)
    f.write("\n")

print(f"Successfully updated {target}")
total_s = sum(len(sp['sentences']) for sp in SUBPARTS)
print(f"Total individual sentences: {total_s}")
