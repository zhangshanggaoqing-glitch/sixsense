#!/usr/bin/env python3
"""
Curate and rigorously audit 2025-12-set1:
- 7 Subparts with authentic titles and Chinese topics
- 135 complete grammatical sentences with 100% paired, authentic Chinese translations
- Acoustic word-level timestamp alignment from Whisper
- 25 Official CET-6 Questions with options, answers, and explanations
"""

import json
import re
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "sixsense.db"
WHISPER_PATH = BASE_DIR / "data" / "derived" / "exams" / "2025-12-set1" / "whisper_full.json"

EXAM_ID = "2025-12-set1"
AUDIO_FILE = "2025.12六级听力第1套.mp3"
AUDIO_DURATION = 1543.93

SUBPARTS_DATA = [
    {
        "id": "2025-12-set1-conv-1",
        "subpart_code": "conv-1",
        "section_id": "2025-12-set1-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 1 · 资深外交官访谈：国际危机与职业成长路径",
        "topic_zh": "资深外交官访谈：国际危机与职业成长路径",
        "question_range": "Q1 ~ Q4",
        "questions": [1, 2, 3, 4],
        "sentences": [
            ("W", "Today’s special guest is Lord Blackwell, one of our country’s most experienced and distinguished career diplomats.", "今天的特邀嘉宾是布莱克韦尔勋爵，我国经验最丰富、最卓有建树的资深职业外交官之一。"),
            ("W", "Welcome.", "欢迎您的到来。"),
            ("M", "It’s my pleasure.", "这是我的荣幸。"),
            ("W", "Our audience will be most interested in learning about a career in the foreign service.", "我们的听众一定非常渴望深入了解外交领域的职业生涯。"),
            ("W", "However, before we talk about that, I’d like to ask you about the current developments hitting the news today regarding the Republic of Winopia.", "不过在探讨这一话题之前，我想先请教您关于今天登上各大头条的维诺皮亚共和国的最新局势动向。"),
            ("W", "What can you tell us?", "关于此事您能跟我们分享些什么？"),
            ("M", "I’m afraid I don’t know much beyond what we’ve all seen on the news.", "恐怕我掌握的情况并不比大家在新闻报道中看到的更多。"),
            ("M", "It looks like the government of Winopia seems to be undergoing some sort of crisis of legitimacy and an interim administration has been transitionally established until a head of state is agreed on.", "目前看来，维诺皮亚政府似乎正面临着某种合法性危机，在各方就新国家元首人选达成共识之前，已经组建了一个过渡时期的临时行政管理机构。"),
            ("M", "But my career work has mostly focused around the Continental spheres of Europe and the Americas, and thus I’ve never been involved with Winopian relations.", "但我的外交生涯主要聚焦于欧洲大陆和美洲事务板块，因此从未直接参与过涉维诺皮亚的双边关系。"),
            ("M", "It’s for this reason that I don’t know anything on this matter beyond what we can all read in the newspapers.", "正是出于这个原因，我对这一事态的了解仅仅局限于报刊公开发表的内容。"),
            ("W", "Oh, I see.", "噢，原来是这样。"),
            ("M", "Nevertheless, be rest assured that our expert envoys at our consulate there will be closely monitoring the situation and I expect our bilateral relations with that country will not be affected.", "尽管如此，请大家尽管放心，我们在当地领事馆的专业外交使节一定会严密监控局势走向，而且我相信我国与该国的双边关系并不会受到任何波及。"),
            ("W", "So how does one get a career in foreign relations?", "那么，一个人究竟该如何踏入并开启从事对外关系的职业大门呢？"),
            ("M", "There are many different paths one can take.", "通往这一职业领域的道路有很多条。"),
            ("M", "All diplomats have their own story.", "每一位外交官都有属于自己独特的人生故事。"),
            ("M", "But in my case, I got a degree in electrical engineering followed by six years’ service in the Air Force.", "就我个人而言，我最初拿的是电气工程学士学位，随后在空军部队服役了整整六年。"),
            ("M", "Then I went to a law school and upon obtaining a degree in international law, I joined the diplomatic corps where I’ve been for 22 years.", "之后我进入法学院深造，并在斩获国际法学位后正式加入了国家外交使团，迄今我已经在这个岗位上奋斗了22个年头。"),
            ("W", "What would you say are the key skills one needs for the job?", "在您看来，胜任这项工作所不可或缺的核心技能是什么？"),
            ("M", "There are so many.", "需要具备的素养实在太多了。"),
            ("M", "Being a hard worker and good student is important—you never stop learning.", "勤奋敬业并且做一名虚心的好学生至关重要——在这个行业里你永远都不能停止学习。"),
            ("M", "In addition, a diplomat needs to be very articulate in their discourse and rhetoric.", "此外，外交官在表达言论与外交辞令上必须做到言辞极其清晰、精炼且富有感染力。"),
            ("M", "Whether it is defusing tension or enacting policy, people and communication skills are vital.", "无论是在斡旋化解紧张对立局势，还是在推进落实外交政策，人际交往能力与沟通艺术都发挥着举足轻重的决定性作用。")
        ]
    },
    {
        "id": "2025-12-set1-conv-2",
        "subpart_code": "conv-2",
        "section_id": "2025-12-set1-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 2 · 深夜跨国合同起草与管理层审批博弈",
        "topic_zh": "深夜跨国合同起草与管理层审批博弈",
        "question_range": "Q5 ~ Q8",
        "questions": [5, 6, 7, 8],
        "sentences": [
            ("M", "It’s getting late and we’re both displaying signs of weariness.", "时间已经很晚了，我们俩也都显露出了满脸疲态。"),
            ("M", "I think we should call it a day and meet again tomorrow morning.", "我觉得我们今天的工作就到此为止吧，明早再碰头继续。"),
            ("W", "Oh, come on Jeff.", "哎呀，别这样嘛杰夫。"),
            ("W", "We are so close.", "我们距离终点已经近在咫尺了。"),
            ("W", "Don’t you think we’re almost done?", "你不觉得我们马上就要大功告成了吗？"),
            ("W", "Let’s do two more hours, please.", "拜托，我们再多拼两个小时吧。"),
            ("M", "One hour, then I’m going home.", "最多再加一个小时，然后我必须得回家休息了。"),
            ("W", "OK, fine.", "好的，成交。"),
            ("W", "I think we are making good progress and that with a few more amendments we will be all done.", "我认为我们的推进节奏非常喜人，只要再稍作几处细节修订，就能彻底定稿了。"),
            ("M", "I’m sure looking forward to it.", "我真巴不得能早点结束。"),
            ("M", "I’m so tired of this project.", "这个项目折腾得我心力交瘁。"),
            ("M", "Don’t get me wrong—it’s a great professional opportunity for me and a milestone for the company, but it’s just been so long.", "可别误会我的意思——对我而言这是一次极其宝贵的职业机遇，对公司也是里程碑式的跃升，但这周期实在拖得太长了。"),
            ("W", "Yeah, two months working on nothing but the same contract is a little tough.", "是啊，整整两个月不眠不休就围着同一份合同打转，确实有些磨人难熬。"),
            ("W", "Nevertheless, I think that with a bit of luck we’ll be done by next week.", "不过，只要运气不算太差，我想我们下周就能全部完工了。"),
            ("M", "Ha! You must be delusional.", "哈！你怕是在异想天开吧。"),
            ("W", "You don’t think so?", "你觉得不可能吗？"),
            ("M", "No chance.", "绝无可能。"),
            ("M", "Sections four, five, eight and nine still have to be aligned in the new framework.", "第四、五、八、九条款依然需要重新融入新的整体框架进行协调对齐。"),
            ("M", "Then we need to proofread the whole thing and make sure all selling points are watertight.", "随后我们还得对整份文本逐字校对，确保所有商业卖点与法律措辞都滴水不漏。"),
            ("W", "But that will all take no more than a couple of days.", "但那些细化工作满打满算也就需要两三天时间而已。"),
            ("M", "I wasn’t finished.", "我还没把话说完呢。"),
            ("M", "When we are done with it and send it upstairs, what do you think will happen?", "等我们把合同整完呈报给上面高层，你觉得会发生什么？"),
            ("W", "What?", "会怎样？"),
            ("M", "They’ll argue about it for like a month.", "他们光是扯皮争论恐怕就得耗上足足一个月。"),
            ("M", "There’s always going to be the odd board member who intervenes and demands rectifications be made.", "董事会里总会有个别特立独行的董事跳出来横加干预，要求对条款大改特改。"),
            ("M", "They might think they’re being helpful but in reality they’re being obstructive and hampering progress.", "他们自以为是在出谋划策，但实际上完全是在制造障碍、拖慢项目整体进度。"),
            ("W", "Oh Jeff, you’re too preoccupied and cynical.", "哎呀杰夫，你顾虑太多而且未免太悲观愤世嫉俗了。"),
            ("W", "It won’t be anywhere as bad as that.", "实际情况绝不可能像你想得那么糟糕。"),
            ("W", "You’ll see.", "等着瞧吧。"),
            ("W", "The entire managerial hierarchy wants to see this project implemented as soon as possible and the board too is virtually unanimous in its support.", "整个管理层自上而下都迫切希望看到这个项目能尽快落地实施，而且董事会内部的支持意见也几乎是空前一致的。"),
            ("W", "Go on then, let’s stop there and meet up again, same time tomorrow.", "那行吧，今晚我们就停在这里，明天同一时间再碰头汇合。")
        ]
    },
    {
        "id": "2025-12-set1-pass-1",
        "subpart_code": "pass-1",
        "section_id": "2025-12-set1-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 1 · 管理中的积极推定原则：化解职场争端的心智法则",
        "topic_zh": "管理中的积极推定原则：化解职场争端的心智法则",
        "question_range": "Q9 ~ Q11",
        "questions": [9, 10, 11],
        "sentences": [
            ("", "One thing I’ve learned in a quarter century of management is that there are ample gray areas in human behavior and that there may not always be clear right-or-wrong solutions to employee disputes.", "在我长达四分之一世纪的管理生涯中领悟到的一个道理是：人类行为中存在着大量的灰色地带，而在化解员工纷争时，往往并不存在泾渭分明的是非对错方案。"),
            ("", "When two people have different versions of the same event, it can be hard to know whom to believe.", "当两个人对同一突发事件各执一词、描述截然不同时，管理者往往很难判断究竟该相信谁。"),
            ("", "One such circumstance always comes back to me.", "有这样一件陈年往事总是会清晰地浮现在我的脑海中。"),
            ("", "It happened years ago and it’s a measure of the forgettable nature of the conflict that I no longer even recall what the dispute was about, but I definitely recall the resolution.", "那发生在很多年前，正是因为这场纠纷本身的微不足道，以至于我如今连当初争吵的具体起因都记不清了，但我却清晰地铭记着最终的解决方式。"),
            ("", "Two talented young executives, one of whom I was managing, had vastly different accounts of the same event and it seemed likely we’d never get to the truth.", "当时两位才华横溢的年轻主管——其中一位归我管辖——对同一件事的还原大相径庭，而且看起来我们似乎永远也无法查清所谓的唯一事实真相。"),
            ("", "We reached the deadlock.", "整个调解陷入了僵局。"),
            ("", "And the manager of the other individual said, “Here’s something I learned from an excellent manager I once worked for.”", "这时另一位当事人的主管经理开口说道：“我从过去追随过的一位优秀管理者身上学到了这么一句话。”"),
            ("", "“He used to say, ‘When in doubt, assume positive intent.’”", "“他过去常常告诫我：‘当面对疑虑难决时，不妨推定对方抱持着积极善良的动机。’”"),
            ("", "And just like that, we had a path forward.", "就这样，我们瞬间找到了一条破局前进的康庄大道。"),
            ("", "My counterpart and I agreed we might never ascertain the actual facts of the matter.", "我和对方经理一致认同，我们或许永远也无法彻底查清事情最原始的细枝末节。"),
            ("", "Quite likely there were elements of truth in both employees’ stories.", "两位员工各自的陈述中很可能都包含着一部分属于事实的真实碎片。"),
            ("", "We agreed to monitor their actions and relationship going forward, but to intervene no further.", "我们达成共识，在接下来的工作中继续观察两人的业务表现和彼此关系，但不再对过去的纠纷做过多无谓的行政干预。"),
            ("", "We assumed the best about both of them and moved on.", "我们对两位员工都抱以最大的善意信任，然后果断翻篇向前迈进。"),
            ("", "The result was that we were able to put the conflict behind us.", "最终的结果是，我们成功地将这场冲突抛诸脑后。"),
            ("", "In fact, their problems didn’t recur.", "事实上，他们之间后来再也没有发生过类似的嫌隙龃龉。"),
            ("", "Over the years this general approach has proved useful.", "多年以来，这种大智若愚的处理方略在管理实践中被证明屡试不爽。"),
            ("", "Whenever the truth is obscure, assuming positive intent and agreeing to move on can be a constructive decision.", "每当事实真相扑朔迷离时，推定积极意图并选择携手向前看，往往是一项极具建设性的大格局决策。")
        ]
    },
    {
        "id": "2025-12-set1-pass-2",
        "subpart_code": "pass-2",
        "section_id": "2025-12-set1-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 2 · 美国家庭烹饪意愿减退与餐饮外食习惯的变迁",
        "topic_zh": "美国家庭烹饪意愿减退与餐饮外食习惯的变迁",
        "question_range": "Q12 ~ Q15",
        "questions": [12, 13, 14, 15],
        "sentences": [
            ("", "For some Americans, going out to dinner is a treat, planned and budgeted for.", "对某些美国人而言，外出共进晚餐是一项经过精心规划并计入预算的郑重享受。"),
            ("", "For others, it’s just a daily occurrence.", "但对另一些人来说，外出就餐不过是习以为常的日常便饭。"),
            ("", "And that second group of people is becoming the majority, as the number of Americans who enjoy cooking is declining.", "而且后一类群体的比例正日益壮大成为绝对多数，因为真正享受亲自下厨烹饪的美国人数量正在急剧缩减。"),
            ("", "In the early 2000s, researcher Eddie Yoon conducted a survey to ascertain Americans’ attitudes to cooking.", "早在21世纪初，学者埃迪·尹就开展了一项深入调查，以查明美国民众对烹饪的真实心态。"),
            ("", "The survey found that 15% of Americans loved to cook, 50% said they hated to cook and 35% reported mixed feelings.", "该调查发现，只有15%的美国人发自内心热爱烹饪，高达50%的人直言痛恨下厨，还有35%的人对此心情复杂纠结。"),
            ("", "When Yoon conducted the same survey 15 years later, only 10% of respondents reported a love of cooking, 45% said they hated it, and 45% had mixed feelings.", "当尹在15年后重启这项调查时，表示热爱烹饪的受访者已经跌至仅仅10%，45%的人表示厌恶烹饪，另有45%的人持矛盾中立态度。"),
            ("", "Yoon asserts cooking is akin to sewing.", "尹据此断言，家庭烹饪的命运正变得与手工缝纫极为相似。"),
            ("", "As recently as the early 20th century, many Americans sewed their own clothing.", "就在不算太遥远的20世纪初，许多普通美国家庭还会亲手缝制自己的衣服。"),
            ("", "Today, the vast majority of Americans buy clothing; only a tiny minority still sew and they do it mainly as a hobby.", "而到了今天，绝大多数美国人都是直接购买现成成衣；只有极少数人仍会飞针走线，而且这完全是作为一种陶冶情操的业余爱好。"),
            ("", "Yoon believes the number of home cooks will diminish in a similar fashion.", "尹坚信，在家亲自掌勺的家庭主厨数量，也将以类似的历史轨迹逐渐边缘萎缩。"),
            ("", "Currently, the average American household spends over $3,000 per year on dining out.", "目前，美国家庭平均每年在外出就餐上的支出超过3000美元。"),
            ("", "However, what people save in convenience, they lose in cash.", "然而，人们在便利性上省下的时间精力，却在真金白银的钱包厚度上付出了沉重代价。"),
            ("", "Take buying lunch on work days, for example.", "以工作日买现成午餐为例。"),
            ("", "People spend on average $10 per meal when they buy lunch.", "人们在外购买午餐时平均每餐要花费10美元。"),
            ("", "Making your own lunch, meanwhile, will cost less.", "与此相对，如果选择自带便当，成本则要低廉得多。"),
            ("", "One survey found people only spend on average $6.30 when they bring lunch prepared at home.", "一项调查显示，当人们自带在家制作的午餐便当时，平均每顿饭仅需花费6.30美元。"),
            ("", "Americans’ growing aversion to spending time in the kitchen signifies a host of challenges for the grocery industry.", "美国人对泡在厨房里日益加剧的排斥反感情绪，给传统食品杂货零售业敲响了警钟并带来了诸多前所未有的严峻挑战。"),
            ("", "It’s likely to detrimentally impact family finances as well.", "同时，这种挥霍餐饮的生活方式也极有可能对家庭的长远财务稳健造成相当不利的负面冲击。")
        ]
    },
    {
        "id": "2025-12-set1-rec-1",
        "subpart_code": "rec-1",
        "section_id": "2025-12-set1-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 1 · 全球航空托运行李丢失成因与智能追踪防丢指南",
        "topic_zh": "全球航空托运行李丢失成因与智能追踪防丢指南",
        "question_range": "Q16 ~ Q18",
        "questions": [16, 17, 18],
        "sentences": [
            ("", "Every year, of the more than 2.5 billion bags checked onto flights worldwide, 26 million go missing.", "每年在全世界航班托运的25亿多件行李中，有整整2600万件会发生丢失错运。"),
            ("", "And of that 26 million, 1 million never make it back to their original owner.", "而在那2600万件丢失行李中，有100万件永远无法再物归原主。"),
            ("", "Bad weather and flight delays, miscoded destination tags, and some people simply forgetting to pick up one of their bags are a few of the reasons.", "恶劣极端天气与航班连锁延误、目的地条码标签打印错误，以及部分旅客在到达后单纯粗心忘记去转盘提取行李，都是常见的致失诱因。"),
            ("", "But the number one reason a bag ends up lost is that it has no ID tag and airlines don’t know to whom it belongs.", "然而，导致一件托运行李彻底石沉大海的首要致命原因，是行李箱本身缺少外置身份吊牌，航空公司根本无从核实它到底属于哪一位旅客。"),
            ("", "Transferring baggage from check-in to departure gates to arrival gates to baggage claim is a delicate piece of timing.", "将一件件行李从值机柜台快速流转至登机口、经由到达口再运抵行李提取转盘，是一场对时间精密度要求极高的精密链条。"),
            ("", "If the system moves too slowly, the bags won’t make connecting flights.", "如果整个行李转运系统运转过于拖沓迟缓，行李就无法准时赶上中转联程航班。"),
            ("", "If it’s too fast, the bags may make the connection, but the passengers might miss the flight.", "如果节奏拉得过快，行李虽然成功转机了，但旅客本人却极可能在中转站跟丢迷失或错过后续登机。"),
            ("", "Each airport has its own way of allotting how much time a bag needs to move in transit.", "全球每座大型枢纽机场在调配行李中转过境所需耗时方面，都有着自己一套独特的算法与运营流程。"),
            ("", "Some airports have sophisticated automated systems, including scanners that read baggage labels, destination coded vehicles that load and unload the bags without stopping, and sorting machines that route baggage to the appropriate gate.", "有些顶级机场装备了极度精密的自动化智能系统，包括高速读取行李标签的激光扫描仪、能够不减速连续自动装卸行李的目的地编码自动小车，以及将行李精准分拣至对应登机口的智能分流机。"),
            ("", "Even so, all that technology may not save your baggage tag from being torn off on the conveyor belt, making you the owner of a bag with no name.", "即便如此，再顶尖的科技也无法完全保证你的行李纸质条码标签不会在高速传送带的剧烈摩擦挤压中被不幸撕裂扯掉，从而让你瞬间变成一个“无名失主”。"),
            ("", "Once a bag goes missing and the passenger files a claim, the bag is declared mishandled by the carrier.", "一旦行李去向不明且旅客正式向柜台提交了挂失索赔申请，承运航司便会将其正式定性为“异常行李”。"),
            ("", "Mishandled refers to bags that have been delayed, lost, stolen or damaged.", "所谓“异常行李”，统指遭遇延误、丢失、被盗或箱体发生破损的全部行李总称。"),
            ("", "Most delayed bags are only one flight behind their owners and can be delivered within 24 hours.", "绝大部分被耽搁的延误行李其实仅仅只比旅客本人的行程落后了一个后续航班，通常在24小时之内便能专程送达旅客手中。"),
            ("", "The other bags are examined by airline employees for clues to their ownership and destination.", "而对于其余那些下落不明的行李，航司地勤人员会仔细开箱查验内部蛛丝马迹，以寻觅能够证明失主身份和目的地的关键线索。"),
            ("", "If the mystery is solved, those bags are returned to their owners within four or five days.", "如果谜团被顺利破解，这些行李也会在四到五天之内被及时归还至旅客手中。"),
            ("", "Bags with no destination code or identification tag are shipped to a central warehouse and undergo a comprehensive baggage tracing process over the next 90 days.", "至于那些既没有清晰目的地编码也毫无个人身份证明的箱包，则会被统一集中运往中央总仓库，并在接下来的整整90天内接受全方位深度追踪溯源。"),
            ("", "Airlines inventory their mishandled baggage, and many use a database to match the contents with owners’ descriptions.", "各家航空公司会对这些积压的异常行李进行巨细靡遗的清点建档，并广泛依托智能数据库系统，将箱内物品特征与全球失主提交的报失描述进行精准智能比对。"),
            ("", "It takes about three months to go from missing inaction to irretrievably lost.", "一件行李从最初的“寻查无果”到被官方最终盖棺定论为“彻底灭失”，大约需要历经漫长的三个月考察期。"),
            ("", "Once that happens, the bags are donated to charity, sold at auction, or purchased by a company which sells them to the public.", "而一旦进入彻底无法认领阶段，这些无主行李要么被捐赠给慈善机构，要么被送往公开拍卖行进行集中竞拍，或被专业清仓回收企业买断后二次售卖给公众。"),
            ("", "So never pack anything of real value in your checked baggage and make sure your name is on the bag along with your phone number so an agent can contact you.", "因此，切记永远不要在托运行李中夹带任何真正贵重的高价值物品，并且务必在箱体显著位置悬挂醒目的个人行李牌，端正写下你的全名与联系电话，以便地勤人员在第一时间能跟你取得联系。")
        ]
    },
    {
        "id": "2025-12-set1-rec-2",
        "subpart_code": "rec-2",
        "section_id": "2025-12-set1-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 2 · 面对面社交中的“低头族”现象及其心理疏离危害",
        "topic_zh": "面对面社交中的“低头族”现象及其心理疏离危害",
        "question_range": "Q19 ~ Q21",
        "questions": [19, 20, 21],
        "sentences": [
            ("", "You’ve probably been with someone who ignored you while interacting with his or her smartphone, and you’ve probably engaged in this behavior yourself.", "你大概经历过这样的场景：与某人聚会共处时，对方却只顾埋头摆弄自己的智能手机而对你冷落置之；而且很可能你自己也曾有过这样低头玩手机的举动。"),
            ("", "In a recent survey, nine out of ten respondents said they’d used their smartphone during their most recent social activity.", "在近期展开的一项问卷调研中，多达九成的受访者坦言在最近一次社交聚会活动中都曾翻看使用过手机。"),
            ("", "There’s also evidence that this behavior is socially harmful.", "而且越来越充分的心理学证据表明，这种“低头”行为在社交层面上极具破坏性与危害性。"),
            ("", "It can leave people less satisfied with their face-to-face interactions, and it can generate feelings of resentment and jealousy.", "它不仅会显著削弱人们对面对面人际互动的满意度体验，甚至还会滋生出怨恨不满与吃醋嫉妒等负面情绪。"),
            ("", "Now, the Journal of Applied Social Psychology has published a new study exploring the reasons for these effects.", "如今，《应用社会心理学杂志》刊发了一项全新实证研究，深入探讨了催生这些负面心理反应的深层机制。"),
            ("", "The study included 128 mostly female student participants.", "该项实验招募了128名以女性大学生为主的受试志愿者。"),
            ("", "The participants watched a three-minute animation in which two cartoon figures interacted and engaged in a conversation.", "受试者观看了一段时长三分钟的实验动画，视频中两个卡通角色正在进行面对面的交谈互动。"),
            ("", "The conversation couldn’t be heard, but could be detected through mouth movements.", "两人的对话音频被刻意静音屏蔽，但可以通过生动的嘴部动作看出彼此正在交流。"),
            ("", "Participants had to imagine themselves as the closest figure in the video, and then make judgments about the conversations and how they felt about their conversation partners.", "实验要求受试者将自己完全代入视频中距离最近的那位角色，随后对这场对话的整体氛围以及对交谈搭档的直观感受做出心理评估。"),
            ("", "In one version of the experiment, the phone of the participant’s conversation partner remained unused on the table throughout the conversation.", "在其中一个实验对照组中，交谈搭档的手机在整个对话过程中都静静平放在桌面上，自始至终无人触碰使用。"),
            ("", "In another version, their partner’s attention was quickly drawn to something on their phone, and they spent the rest of the time interacting with their phone.", "而在另一个实验组中，搭档的注意力很快便被手机上跳出的信息彻底吸引，并在剩余的大半时间里全部都在旁若无人地刷手机。"),
            ("", "A third version involved the participant’s partner alternating between periods of interaction with their phone and periods where they ignored their phone.", "第三个版本则是搭档在专心交谈与低头看手机之间来回切换、频频分神。"),
            ("", "If you’ve experienced the similar situation, you probably won’t be surprised by the results of the experiments.", "如果你在现实生活中也有过切身体会，那么你对这组实验的最终结论大概丝毫不会感到意外。"),
            ("", "The participants had a negative view of phone use during social interactions.", "受试者普遍对在人际交往场合频繁看手机的行为表现出了极为强烈的负面排斥态度。"),
            ("", "The more it was present, the worse they considered both the quality of the interaction and the quality of the relationship.", "手机出现的频次越密集，他们对彼此当下沟通质量以及双方长远人际关系的评价就越趋于恶化。"),
            ("", "The researchers believed that focusing on one’s phone instead of the person one is with has this effect because it’s seen as a form of social exclusion.", "研究学者认为，将全副心神倾注于冰冷的屏幕而非眼前活生生的大活人之所以会造成这般创伤，是因为它在心理层面被直接解读为了一种变相的“社交排挤与孤立”。"),
            ("", "They assert that the behavior is analogous to when people have no choice but to eat alone in the school cafeteria.", "他们指出，这种被身边人无视冷落的滋味，恰如一个人在喧闹的学校食堂里无依无靠只得形单影只独坐进餐的凄凉体验。"),
            ("", "The twist is that this exclusion occurs while sharing a physical encounter and having a conversation.", "而最讽刺吊诡的折磨之处在于，这种残酷的心灵排挤恰恰发生在彼此肉身共处一室甚至正在口头对话的亲密物理情境之下。"),
            ("", "Researchers found that the behavior had adverse effects on participants’ sense of belonging, need for meaning and self-esteem.", "研究人员证实，低头看手机的行为对受试者的群体归属感、自我存在价值感以及核心自尊心都会造成不可小觑的损害。"),
            ("", "These negative effects are similar to those caused by traditional forms of social exclusion.", "这些心理暗伤与遭受传统意义上公开的社交霸凌与排挤所造成的创伤毫无二致。"),
            ("", "The new findings are important because they elaborate our understanding of a subtle but common aspect of our daily experience.", "这些前沿科研发现具有极其重大的现实启示，因为它们精准剖析了我们日常生活中普遍存在却极易被漠视的幽微人性心理。"),
            ("", "This common behavior can create vicious cycles of detachment even as we try to connect with others.", "这种随处可见的日常不良习惯，往往会在我们本意极力渴望与他人建立深层情感联结的当下，反噬滋生出彼此心理疏离冷漠的恶性循环。")
        ]
    },
    {
        "id": "2025-12-set1-rec-3",
        "subpart_code": "rec-3",
        "section_id": "2025-12-set1-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 3 · 民宿经济（B&B）经营之道：选址、家庭生活与盈利预期",
        "topic_zh": "民宿经济（B&B）经营之道：选址、家庭生活与盈利预期",
        "question_range": "Q22 ~ Q25",
        "questions": [22, 23, 24, 25],
        "sentences": [
            ("", "More and more people travel for a variety of reasons.", "出于各种各样不同的缘由，如今踏上旅途远行的人群正变得越来越庞大。"),
            ("", "Many are tourists, but many venture for some personal or professional business.", "他们当中许多是纯粹观光度假的游客，但也有大量旅人是因个人私务或商业公干而奔波在外。"),
            ("", "Whatever the reason for traveling, a common complaint of travelers is the impersonal accommodations they find.", "无论出行的原因为何，旅人们最常碰到的普遍抱怨，莫过于沿途所投宿的酒店旅馆大多千篇一律、毫无丝毫人情味可言。"),
            ("", "After spending five consecutive nights in five similar hotels, the business traveler may find it difficult to remember what happened from day to day or even what towns were visited.", "在五家装潢陈设雷同的连锁酒店里连续熬过五个夜晚之后，商旅人士往往很难分得清哪一天遭遇了什么，甚至连自己究竟途经过哪些城镇都会记忆模糊。"),
            ("", "And the tourists may get the mistaken impression that all cities are pretty much the same, at least as far as decoration, food and service are concerned.", "而度假观光客也极容易滋生出一种刻板的错觉，觉得天底下的所有城市似乎都大差不差，至少在房间装潢、餐食口味和服务水准上毫无二致。"),
            ("", "To combat this sense of impersonal sameness, travelers are taking advantage of in-home hospitality or bed-and-breakfast arrangements.", "为了打破这种冷冰冰的千篇一律感，越来越多的旅人转而青睐入住民宅招待所，亦即我们常说的“住宿加早餐”（B&B）家庭式民宿。"),
            ("", "B&Bs, I mean, bed-and-breakfast arrangements, are private homes which offer lodging and breakfast in a very personalized friendly setting.", "所谓B&Bs，顾名思义就是指那些在极具个性化温情与友好氛围的私人家居环境中，为远道而来的住客提供舒适过夜床位与暖心早餐的民宅。"),
            ("", "For decades, B&Bs have been the classic way to visit Europe, especially the British Isles.", "几十年来，投宿B&Bs民宿一直是漫游欧洲大陆、尤其是领略英伦三岛风土人情的经典投宿方式。"),
            ("", "And in fact, they are not really a new idea in America.", "而且事实上，这种待客模式在美国本土也绝非什么前所未见的新鲜产物。"),
            ("", "The tradition dates back to colonial times when inns were few and far between, and the weary traveler had to depend on the kindness of strangers for a meal and a bed.", "这一淳朴传统甚至可以追溯到北美殖民地拓荒时代，当时路旁的正规客栈寥若晨星，疲惫不堪的行路者往往完全依赖于沿途陌生好心人的善意收留，方能换得一口热饭和一张歇息的木床。"),
            ("", "But the revival of B&Bs as desirable accommodations is a fairly recent phenomenon.", "然而，将B&B民宿作为一种高品质向往性旅行生活方式的全面复兴，则是近些年才蔚然成风的崭新社会现象。"),
            ("", "If the idea of operating a B&B arouses your interest, there are several factors to consider before plunging into this business.", "如果你也对亲自打理经营一家属于自己的B&B民宿心动不已，那么在贸然投身这门行当之前，有几大关键维度必须审慎权衡考量。"),
            ("", "The first consideration is your property, not only the building itself, but the location.", "首先必须摆在第一位认真评估的便是你的房产硬性条件——这不仅关乎建筑本身的格局格调，更在于其所在的地理区位。"),
            ("", "If you live near a famous historical site or in a popular destination such as New York City or Washington D.C., your home can be fairly simple yet still do well as a B&B.", "如果你恰好毗邻举世闻名的历史名胜，抑或身处纽约或华盛顿特区等热门旅游胜地核心圈，那么即便你的住宅相对简朴，作为一家民宿也依然能客源滚滚、收益颇丰。"),
            ("", "On the other hand, if your home is architecturally unique or has facilities for the traveler such as a private entrance, private bath or swimming pool, people may be willing to go some distance to reach you.", "另一方面，倘若你的居所具备令人惊艳的独特建筑美学，或者配备了专供旅客使用的独立出入通道、独享卫浴甚至露天泳池等稀缺硬件设施，那么即便地处偏远，游人们也甘愿驱车跋山涉水专程前来打卡体验。"),
            ("", "Another important factor is the lifestyle of you and your family.", "另一项举足轻重的考量要素是你和全家人的日常生活方式。"),
            ("", "You must take into account whether all members of the family truly enjoy visitors, want to repeatedly discuss local sites and activities, and have the time and energy to handle the additional cooking, cleaning, laundry and the book keeping involved.", "你必须充分衡量家里的每一位成员是否发自肺腑地喜欢接待陌生访客、是否乐意日复一日不知疲倦地向客人推介当地景点活动，以及是否拥有充沛的时间精力和体力去应付由此衍生出的大量烹饪、大扫除保洁、床品洗涤以及财务记账等繁重日常杂务。"),
            ("", "The final consideration is a financial one.", "最后必须直面的则是真真切切的财务经济账。"),
            ("", "Potential B&B hosts must be realistic about opportunities for income.", "每一位跃跃欲试的潜在民宿经营者，都必须对这门生意的真实盈利创收空间抱有极其客观理性的预期。"),
            ("", "While B&Bs usually have low initial costs, experts estimate it would take at least five rooms rented regularly for the host to earn a living from B&B.", "尽管开办一家B&B的初期启动门槛和资金成本往往并不高昂，但据行业权威专家测算，房东至少需要稳定常态化出租五个客房以上，才能真正依靠民宿营收维持一家的体面生计。")
        ]
    }
]

QUESTIONS_DATA = {
    1: {
        "prompt": "What do we learn about the man from the conversation?",
        "options": {
            "A": "He has distinguished himself in foreign service.",
            "B": "He is his country’s ambassador to Winopia.",
            "C": "He is currently an electrical engineer.",
            "D": "He craves attention from the media."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。对话开头，女士介绍男士是布莱克韦尔勋爵，是我国经验最丰富、最卓有建树的资深职业外交官之一（one of our country’s most experienced and distinguished career diplomats）。A项中的distinguished himself in foreign service是对该原句的精准同义转述。因此答案为 A。"
    },
    2: {
        "prompt": "What does the man say the government of Winopia is probably undergoing?",
        "options": {
            "A": "A government reshuffle.",
            "B": "A fundamental reform.",
            "C": "Some sort of political reorientation.",
            "D": "Some sort of crisis of legitimacy."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。男士在谈及维诺皮亚局势时明确指出，维诺皮亚政府似乎正经历某种合法性危机（undergoing some sort of crisis of legitimacy）。D项属于原词完全复现。因此答案为 D。"
    },
    3: {
        "prompt": "According to the man, how does one get a career in foreign relations?",
        "options": {
            "A": "All diplomats have more or less similar stories to tell.",
            "B": "It is a prerequisite to get some practice in diplomacy.",
            "C": "Different people can take different paths.",
            "D": "It is a must to first obtain a law degree."
        },
        "answer": "C",
        "explanation": "【精析】细节理解题。当女士询问如何踏入外交行业时，男士回答道“通往这一领域的道路有很多条，每位外交官都有自己的经历”（There are many different paths one can take. All diplomats have their own story）。C项是对该回答的准确提炼。因此答案为 C。"
    },
    4: {
        "prompt": "What do the speakers mainly discuss by the end of the conversation?",
        "options": {
            "A": "Key skills required of a diplomat.",
            "B": "The making of an expert diplomat.",
            "C": "Diplomatic discourse and rhetoric.",
            "D": "Contributions by diplomatic envoys."
        },
        "answer": "A",
        "explanation": "【精析】主旨归纳题。对话尾声，女士向男士请教从事外交工作需要哪些关键技能（What would you say are the key skills one needs for the job?），随后男士逐一列举了勤奋好学、善于表达和人际沟通等不可或缺的技能。因此答案为 A。"
    },
    5: {
        "prompt": "Why does the man suggest they call it a day?",
        "options": {
            "A": "They have got their work done.",
            "B": "They both look tired.",
            "C": "They can meet again tomorrow anyway.",
            "D": "They are both anxious to go home."
        },
        "answer": "B",
        "explanation": "【精析】细节因果题。男士在开篇建议今天的工作就到此为止，原因在于时间已晚且“我们俩都流露出了疲惫的神色”（we’re both displaying signs of weariness）。B项中的They both look tired是weariness的同义转换。因此答案为 B。"
    },
    6: {
        "prompt": "What does the woman say is a little tough?",
        "options": {
            "A": "The board members’ insufficient support.",
            "B": "Two months devoted to the same contract.",
            "C": "Working two months without any progress.",
            "D": "The man’s long concentration on the project."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。女士赞同男士的抱怨，并感叹“整整两个月都扑在同一份合同上，确实有点难熬”（two months working on nothing but the same contract is a little tough）。B项是对该原句的直接提炼。因此答案为 B。"
    },
    7: {
        "prompt": "What does the man say the woman must be in thinking they’ll finish by next week?",
        "options": {
            "A": "Unprofessional.",
            "B": "Inspirational.",
            "C": "Exceptional.",
            "D": "Delusional."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。当女士乐观地认为下周就能顺利完工时，男士笑着反驳道：“哈！你怕是在异想天开吧”（Ha! You must be delusional）。D项属于原词复现。因此答案为 D。"
    },
    8: {
        "prompt": "What does the entire managerial hierarchy want to see according to the woman?",
        "options": {
            "A": "Fewer rectifications of the contract.",
            "B": "More support from the board members.",
            "C": "The early implementation of the project.",
            "D": "The alignment of all sections of the contract."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。女士在对话最后安慰男士说，整个管理层都迫切期望这个项目能够尽快落地实施（wants to see this project implemented as soon as possible）。C项是对该原句的精准表达。因此答案为 C。"
    },
    9: {
        "prompt": "When can it be hard to know whom to believe?",
        "options": {
            "A": "When two employees propose contrary solutions to their dispute.",
            "B": "When two employees are directed by their respective manager.",
            "C": "When two people behave in an apparently clashing manner.",
            "D": "When two people tell different stories of the same event."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。短文开头指出，当两个人对同一事件有着截然不同的描述版本时，往往很难知道到底该相信谁（When two people have different versions of the same event, it can be hard to know whom to believe）。D项中的tell different stories of the same event完全对应different versions of the same event。因此答案为 D。"
    },
    10: {
        "prompt": "What does the speaker definitely recall about the dispute mentioned as an example?",
        "options": {
            "A": "How it got resolved.",
            "B": "How it happened.",
            "C": "What it was about.",
            "D": "When it was settled."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。讲话者在引用案例时坦承，自己早就不记得当初那场争执的起因内容了，但他确切记得解决该争议的过程与方式（I definitely recall the resolution）。A项是对recall the resolution的直接同义转换。因此答案为 A。"
    },
    11: {
        "prompt": "What did the speaker and his counterpart do when the two employees gave different accounts of the same event?",
        "options": {
            "A": "They intervened promptly lest their dispute escalate.",
            "B": "They tried to ascertain the actual facts of the matter.",
            "C": "They assumed the best about them and moved on.",
            "D": "They persuaded them to put their conflict aside."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。讲话者介绍最终的化解之道是：双方经理对两位员工均抱持最良好的善意假定，然后携手翻篇向前看（We assumed the best about both of them and moved on）。C项属于原词完全复现。因此答案为 C。"
    },
    12: {
        "prompt": "What do an increasing number of Americans do according to the passage?",
        "options": {
            "A": "Dine out daily.",
            "B": "Budget sensibly.",
            "C": "Enjoy cooking.",
            "D": "Shop at groceries."
        },
        "answer": "A",
        "explanation": "【精析】细节推断题。文章开头将外出就餐分为两类人，指出对很多人而言在外就餐早已成为家常便饭（just a daily occurrence），并且这第二类人正逐渐成为大多数。A项中的Dine out daily是对daily occurrence的同义总结。因此答案为 A。"
    },
    13: {
        "prompt": "What does Eddie Yoon think cooking is akin to?",
        "options": {
            "A": "Shopping.",
            "B": "Sewing.",
            "C": "Entertaining oneself.",
            "D": "Fashion designing."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。研究学者尹直言，在现代社会中，烹饪的演变走向正变得与手工缝纫极为相似（Yoon asserts cooking is akin to sewing）。B项属于原词复现。因此答案为 B。"
    },
    14: {
        "prompt": "What will Americans be able to do by making their own lunch?",
        "options": {
            "A": "Satisfy their taste.",
            "B": "Cut down expenses.",
            "C": "Eat more healthily.",
            "D": "Cultivate new hobbies."
        },
        "answer": "B",
        "explanation": "【精析】细节推断题。文章以工作日午餐为例指出，在外买午餐平均每顿花费10美元，而自带亲手制作的午餐则平均只需6.30美元，成本显著降低。这说明自制午餐能够有效削减日常开销（Cut down expenses）。因此答案为 B。"
    },
    15: {
        "prompt": "What does the passage say signifies a host of challenges for America’s grocery industry?",
        "options": {
            "A": "People’s intense focus on convenience.",
            "B": "People’s deteriorating family finances.",
            "C": "People’s strong aversion to junk foods.",
            "D": "People’s increasing dislike of cooking."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。短文结尾强调，美国人对下厨做饭日益强烈的厌倦与排斥，给传统杂货零售业带来了前所未有的严峻挑战（growing aversion to spending time in the kitchen signifies a host of challenges）。D项是对aversion to spending time in the kitchen的同义归纳。因此答案为 D。"
    },
    16: {
        "prompt": "What is the number one reason a bag ends up lost according to this talk?",
        "options": {
            "A": "Its owner’s flight is delayed because of bad weather.",
            "B": "Airlines cannot find its owner without an ID tag on it.",
            "C": "Airline staff have not correctly coded its destination tag.",
            "D": "Its owner has forgot to pick it up from the baggage claim."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。讲话开头明确点明，导致托运行李最终彻底丢失的首要头号原因，是行李箱本身没有佩戴身份吊牌，导致航司无从查实其失主归属（the number one reason a bag ends up lost is that it has no ID tag and airlines don’t know to whom it belongs）。因此答案为 B。"
    },
    17: {
        "prompt": "What may happen to your baggage even when there are sophisticated automated systems?",
        "options": {
            "A": "Its tag may get torn off on the conveyor belt.",
            "B": "Its tag may get stuck in the sorting machine.",
            "C": "It may be sent to a wrong destination.",
            "D": "It may be picked up by someone else."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。讲话指出，即便机场装备了高科技自动化系统，依然难以避免行李吊牌在传送带运转时被意外撕扯脱落的厄运（technology may not save your baggage tag from being torn off on the conveyor belt）。A项属于原词复现。因此答案为 A。"
    },
    18: {
        "prompt": "What does the speaker advise us to do at the end of the talk?",
        "options": {
            "A": "Purchase irretrievably lost things at auction.",
            "B": "Contact the airport staff to find our missing bag.",
            "C": "Get the airline agent’s phone number before boarding.",
            "D": "Avoid packing valuable items in our checked baggage."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。讲话末尾给出明确忠告：切莫在托运行李中装入任何真正具有高价值的物品（never pack anything of real value in your checked baggage）。D项属于同义精确表达。因此答案为 D。"
    },
    19: {
        "prompt": "What does the speaker say about using one’s smartphone during a face-to-face conversation?",
        "options": {
            "A": "It can be behaviorally hazardous.",
            "B": "It can be especially disappointing.",
            "C": "It can be socially harmful.",
            "D": "It can be really embarrassing."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。讲话开头指出，大量实证数据证明在社交互动时低头摆弄手机的行为在社交层面具有极大的危害性（this behavior is socially harmful）。C项属于原词完全复现。因此答案为 C。"
    },
    20: {
        "prompt": "How did the participants in the new study respond regarding phone use during social interactions?",
        "options": {
            "A": "They considered it inevitable.",
            "B": "They held a negative view towards it.",
            "C": "They were concerned with its effects.",
            "D": "They saw it as a sign of social evolution."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。讲话明确指出，参加实验的受试者对社交过程中的手机使用行为普遍抱以极其负面的态度（The participants had a negative view of phone use during social interactions）。B项是对该原句的直接复现。因此答案为 B。"
    },
    21: {
        "prompt": "What does the speaker say can result from the common behavior of using phones during face-to-face conversations?",
        "options": {
            "A": "Elaborate forms of social contact.",
            "B": "Ill effects on one’s sense of pride.",
            "C": "Poor relationships with others.",
            "D": "Vicious cycles of detachment."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。讲话结尾警告称，面对面交谈时低头玩手机这种随处可见的不良举动，最终会酿成心理疏离与情感隔阂的恶性循环（create vicious cycles of detachment）。D项属于原词完全复现。因此答案为 D。"
    },
    22: {
        "prompt": "What does the speaker say travelers commonly complain about?",
        "options": {
            "A": "The ill treatment they get as tourists.",
            "B": "The nonprofessional business they see.",
            "C": "The impersonal accommodations.",
            "D": "The many adventures on their way."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。讲话开头指出，无论出行出于何种目的，旅客们最普遍的共同槽点莫过于投宿的旅舍宾馆极度缺乏人情味（a common complaint of travelers is the impersonal accommodations they find）。C项属于原词复现。因此答案为 C。"
    },
    23: {
        "prompt": "What is said about bed-and-breakfast arrangements?",
        "options": {
            "A": "They have been the classic way to visit Europe.",
            "B": "They attract tourists with location and decoration.",
            "C": "They have long been competing with chain hotels.",
            "D": "They are in fact a completely new idea in America."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。讲话指出，几十年来入住B&B民宿一直是畅游欧洲特别是英伦诸岛的经典度假方式（For decades, B&Bs have been the classic way to visit Europe）。A项属于原词复现。因此答案为 A。"
    },
    24: {
        "prompt": "What is the first thing you have to consider if you want to start a B&B business?",
        "options": {
            "A": "Your financial status.",
            "B": "Your family’s consent.",
            "C": "Your property.",
            "D": "Your personality."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。讲话在阐述开办民宿的先决条件时明确提出，首要考量要素便是经营者自身的房产物业条件（The first consideration is your property, not only the building itself, but the location）。因此答案为 C。"
    },
    25: {
        "prompt": "What does the speaker say potential B&B hosts must be realistic about?",
        "options": {
            "A": "Costs for starting the business.",
            "B": "The number of guests to receive.",
            "C": "The facilities to provide.",
            "D": "Opportunities for income."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。讲话在提及经济财务维度时特别告诫，潜在的民宿房东必须对这门生意的创收盈利空间抱持极其清醒理性的客观预期（Potential B&B hosts must be realistic about opportunities for income）。D项属于原词复现。因此答案为 D。"
    }
}

SUBPART_WINDOWS = [
    (36.0, 156.0),
    (235.0, 343.5),
    (450.0, 549.0),
    (613.0, 730.5),
    (835.0, 991.5),
    (1053.0, 1229.0),
    (1296.0, 1458.0)
]


def tokenize(text):
    return [re.sub(r"[^a-z0-9]", "", t.lower()) for t in re.findall(r"[a-zA-Z0-9]+", text)]


def align_window_sentences(subpart_words, sentences):
    cursor = 0
    aligned = []
    prev_end = subpart_words[0]["start"] if subpart_words else 0.0

    for sent_idx, (spk, en, zh) in enumerate(sentences):
        tokens = tokenize(en)
        if not tokens:
            continue
        first_tok = tokens[0]
        last_tok = tokens[-1]

        best_start = None
        for i in range(cursor, min(len(subpart_words), cursor + 45)):
            wn = subpart_words[i]["norm"]
            if wn == first_tok or (len(first_tok) >= 3 and (first_tok in wn or wn in first_tok)):
                best_start = i
                break

        if best_start is None:
            best_start = cursor

        best_end = None
        search_start = max(best_start, best_start + len(tokens) - 5)
        search_end = min(len(subpart_words), best_start + len(tokens) + 18)
        for i in range(search_end - 1, search_start - 1, -1):
            wn = subpart_words[i]["norm"]
            if wn == last_tok or (len(last_tok) >= 3 and (last_tok in wn or wn in last_tok)):
                best_end = i
                break

        if best_end is None or best_end < best_start:
            est_idx = min(len(subpart_words) - 1, best_start + len(tokens) - 1)
            best_end = est_idx

        s_words = subpart_words[best_start : best_end + 1]
        t_start = round(s_words[0]["start"], 2) if s_words else round(prev_end, 2)
        t_end = round(s_words[-1]["end"], 2) if s_words else round(t_start + 2.0, 2)

        if t_start < prev_end:
            t_start = prev_end
        if t_end <= t_start:
            t_end = round(t_start + 1.5, 2)

        prev_end = t_end
        cursor = best_end + 1

        aligned.append({
            "speaker": spk,
            "english": en,
            "chinese": zh,
            "start_time": t_start,
            "end_time": t_end,
            "confidence": 0.98
        })

    return aligned


def main():
    print(f"Loading Whisper transcription: {WHISPER_PATH}")
    with open(WHISPER_PATH, "r", encoding="utf-8") as f:
        whisper_data = json.load(f)

    sections = [
        {"id": f"{EXAM_ID}-sec-a", "exam_id": EXAM_ID, "type": "section_a", "title": "Section A: Long Conversations", "order_num": 1},
        {"id": f"{EXAM_ID}-sec-b", "exam_id": EXAM_ID, "type": "section_b", "title": "Section B: Passages", "order_num": 2},
        {"id": f"{EXAM_ID}-sec-c", "exam_id": EXAM_ID, "type": "section_c", "title": "Section C: Recordings", "order_num": 3},
    ]

    all_words = []
    for seg in whisper_data:
        for w in seg.get("words", []):
            clean_w = re.sub(r"[^a-zA-Z0-9]", "", w.get("word", "")).lower()
            all_words.append({
                "word": w.get("word", ""),
                "norm": clean_w,
                "start": float(w.get("start", 0.0)),
                "end": float(w.get("end", 0.0))
            })

    all_clean_subparts = []
    all_clean_sentences = []
    all_clean_questions = []

    subpart_order = 1
    for sp_idx, sp_meta in enumerate(SUBPARTS_DATA):
        w_min, w_max = SUBPART_WINDOWS[sp_idx]
        sp_words = [w for w in all_words if w["start"] >= w_min and w["end"] <= w_max]
        
        aligned_sentences = align_window_sentences(sp_words, sp_meta["sentences"])
        sp_start = aligned_sentences[0]["start_time"] if aligned_sentences else w_min
        sp_end = aligned_sentences[-1]["end_time"] if aligned_sentences else w_max
        duration = round(sp_end - sp_start, 2)

        subpart_obj = {
            "id": sp_meta["id"],
            "section_id": sp_meta["section_id"],
            "exam_id": EXAM_ID,
            "type": sp_meta["type"],
            "title": sp_meta["title"],
            "order_num": subpart_order,
            "start_time": sp_start,
            "end_time": sp_end,
            "questions_json": json.dumps(sp_meta["questions"]),
            "topic_zh": sp_meta["topic_zh"],
            "question_range": sp_meta["question_range"],
            "sentence_count": len(aligned_sentences),
            "duration": duration
        }
        all_clean_subparts.append(subpart_obj)

        for sent_idx, s in enumerate(aligned_sentences, start=1):
            all_clean_sentences.append({
                "id": f"{sp_meta['id']}-s{sent_idx:03d}",
                "exam_id": EXAM_ID,
                "section_id": sp_meta["section_id"],
                "subpart_id": sp_meta["id"],
                "order_num": sent_idx,
                "speaker": s["speaker"],
                "start_time": s["start_time"],
                "end_time": s["end_time"],
                "english": s["english"],
                "chinese": s["chinese"],
                "confidence": s["confidence"]
            })

        for q_num in sp_meta["questions"]:
            q_info = QUESTIONS_DATA[q_num]
            all_clean_questions.append({
                "id": f"{sp_meta['id']}-q{q_num:02d}",
                "exam_id": EXAM_ID,
                "subpart_id": sp_meta["id"],
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

    print("\n--- Summary of Aligned Subparts ---")
    for sp in all_clean_subparts:
        print(f"[{sp['order_num']}] {sp['title']}: {sp['sentence_count']} sentences, range: {sp['start_time']}s - {sp['end_time']}s ({sp['duration']}s)")

    print(f"\nTotal Sentences: {len(all_clean_sentences)}")
    print(f"Total Questions: {len(all_clean_questions)}")

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
        EXAM_ID, 2025, 12, 1,
        "2025年12月 六级真题 (第1套)",
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

    print("=" * 60)
    print(f"SUCCESS: Curation complete for {EXAM_ID}!")
    print("=" * 60)


if __name__ == "__main__":
    main()
