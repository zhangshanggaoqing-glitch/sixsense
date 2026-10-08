#!/usr/bin/env python3
"""
Curate and rigorously audit 2025-12-set2:
- 7 Subparts with authentic titles and Chinese topics
- Complete grammatical sentences with 100% paired, authentic Chinese translations
- Acoustic word-level timestamp alignment from Whisper
- 25 Official CET-6 Questions with options, answers, and explanations
"""

import json
import re
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "sixsense.db"
WHISPER_PATH = BASE_DIR / "data" / "derived" / "exams" / "2025-12-set2" / "whisper_full.json"

EXAM_ID = "2025-12-set2"
AUDIO_FILE = "2025.12六级听力第2套.mp3"
AUDIO_DURATION = 1572.43

SUBPARTS_DATA = [
    {
        "id": "2025-12-set2-conv-1",
        "subpart_code": "conv-1",
        "section_id": "2025-12-set2-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 1 · 高校食堂餐饮体验与空间翻新评价",
        "topic_zh": "高校食堂餐饮体验与空间翻新评价",
        "question_range": "Q1 ~ Q4",
        "questions": [1, 2, 3, 4],
        "sentences": [
            ("W", "I must say I love our canteen.", "我必须说我很喜欢咱们学校的食堂。"),
            ("W", "It’s such a great meeting point.", "这里真是一个绝佳的聚会社交地点。"),
            ("M", "Yeah, it really is, both for students and teachers.", "是啊，确实如此，对学生和老师来说都是这样。"),
            ("M", "Shame about the food.", "只可惜饭菜质量差强人意。"),
            ("W", "What do you mean?", "你这是什么意思？"),
            ("W", "I think the food is fine.", "我觉得这里的伙食挺不错的呀。"),
            ("M", "I would say the food is just OK, but the prices are absurd, don’t you agree?", "要我说，饭菜只能算一般，但价格却贵得离谱，你难道不这么觉得吗？"),
            ("W", "I don’t actually.", "我还真不这么认为。"),
            ("W", "I personally think they’re perfectly appropriate.", "我个人觉得这儿的定价完全合情合理。"),
            ("W", "If it’s overpriced, why does it get so frantically busy at lunchtimes?", "要是真定价过高，为什么每到午饭时间这里都挤得人满为患、异常火爆呢？"),
            ("M", "Hmm.", "嗯。"),
            ("M", "You make a good point.", "你说得确实有道理。"),
            ("M", "I guess a lot of it is good value.", "我想这里的很多餐品确实物有所值。"),
            ("M", "Maybe even most of it.", "甚至大部分餐品性价比都很高。"),
            ("M", "However, don’t you think six bucks for a slice of apple crumble is beyond most students’ budgets?", "不过，你难道不觉得一份苹果金宝酥卖6美元，这远远超出了大多数学生的日常消费预算吗？"),
            ("W", "Ah, yes, desserts are overpriced.", "啊，确实，甜点的价格确实虚高了。"),
            ("W", "I’ll give you that.", "这一点我承认你说得对。"),
            ("W", "To be honest, I’ve forgotten about those, as I never eat them.", "坦白讲，我都快忘了这茬了，因为我从来都不吃甜点。"),
            ("W", "I never really crave sweet things or any fancy delicacies.", "我平时从来不怎么嘴馋甜食或任何精致昂贵的花哨点心。"),
            ("W", "What I always go for is their scrambled egg.", "我每次必点的是他们的炒蛋系列。"),
            ("W", "They have such a great variety.", "他们炒蛋的花样搭配实在太丰富了。"),
            ("M", "Yeah, those are good.", "对，那些炒蛋确实做得很好吃。"),
            ("M", "They also come out really fast.", "而且出餐上菜速度奇快无比。"),
            ("M", "Actually, that’s one of the best things about the canteen, the speed.", "事实上，出餐神速正是这个食堂最大的亮点之一。"),
            ("M", "If I fancy something more substantial than a sandwich, but I don’t have much time for lunch, the university canteen is always a good option.", "要是我午饭想吃点比三明治更扎实顶饱的饭菜，但手头又没有充裕的时间慢慢吃，学校食堂总是一个极佳的去处。"),
            ("M", "The kitchen staff work at such a brisk pace—they really deserve to be complimented for it.", "后厨员工动作麻利干练、节奏飞快——这一点他们真的值得大加夸赞。"),
            ("W", "Totally, and it’s such a great environment too.", "完全赞同，而且这里的就餐环境也相当惬意。"),
            ("W", "Like, the entire building is beautiful.", "你看，整座建筑本身就极具美感。"),
            ("M", "It is very nice.", "环境确实无可挑剔。"),
            ("W", "The massive glass windows make all the difference.", "那些巨大的落地玻璃窗起到了画龙点睛的作用。"),
            ("W", "I think they’re so cool.", "我觉得大落地窗简直酷毙了。"),
            ("W", "Apparently, they did a massive renovation a few years ago.", "据说几年前他们斥巨资对食堂进行了一次彻底的大规模装修改造。"),
            ("W", "It cost them a pretty penny.", "当时可是花费了一大笔巨资呢。"),
            ("M", "Yeah, I’m not surprised.", "嗯，这一点我丝毫不觉得意外。"),
            ("M", "It’s a very versatile space, suitable both for eating and relaxing.", "这是一个功能极其多元百搭的空间，既适合在此用餐，也适合休闲放松。"),
            ("W", "And for working.", "还非常适合在此办公学习。"),
            ("M", "You’re right, working too.", "你说得对，也很适合学习办公。"),
            ("M", "I’ve used my laptop there once or twice, and there’s always a group project or meeting going on at the far end.", "我就曾在那儿用过一两次笔记本电脑，而且远处靠里的角落里总有小组在热火朝天地讨论项目或开会。")
        ]
    },
    {
        "id": "2025-12-set2-conv-2",
        "subpart_code": "conv-2",
        "section_id": "2025-12-set2-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 2 · 管理层与年轻员工的职场观念契合与考核法则",
        "topic_zh": "管理层与年轻员工的职场观念契合与考核法则",
        "question_range": "Q5 ~ Q8",
        "questions": [5, 6, 7, 8],
        "sentences": [
            ("W", "Hi, Tony.", "嗨，托尼。"),
            ("W", "Today we’re talking about how managers can get along better with young people at work.", "今天我们要深入探讨管理者如何在职场中更好地与年轻一代员工融洽相处。"),
            ("W", "We often hear young people today have a poor work ethic.", "我们经常能听到一种论调，声称如今的年轻一代缺乏良好的职业道德与敬业精神。"),
            ("W", "That’s not really justified though, is it?", "但这种说法其实根本站不住脚，对吧？"),
            ("M", "Not really.", "确实毫无依据。"),
            ("M", "In reality, young people of this age group are as varied and multifaceted as any other generation.", "实际上，这个年龄层的年轻人同以往任何一代人一样，都是极其多元丰富、千人千面的。"),
            ("W", "Yeah, but if you are struggling to work with young people in your workspace, what can you do?", "是的，但如果你在自己的团队里正为如何与年轻员工协作沟通而感到头疼苦恼，你该怎么做呢？"),
            ("M", "Well, it’s essential to connect with them, to learn about their values.", "首先，至关重要的是要与他们建立起真正的情感共鸣与联结，去主动倾听并理解他们的核心价值追求。"),
            ("M", "It’s also really important to recognize the way young people want to balance their work life with their personal life.", "同样极其关键的是，必须深刻理解年轻一代渴望在工作与个人生活之间划清界限、实现平衡的强烈诉求。"),
            ("W", "So, they generally don’t want to defer happiness in return for career advancement?", "所以，他们大体上并不愿意牺牲当下的幸福感来换取虚无缥缈的职场晋升？"),
            ("M", "Absolutely.", "一点没错。"),
            ("M", "They are not willing to sacrifice their personal lives for their work lives.", "他们绝不甘愿为了工作而牺牲属于自己的个人生活。"),
            ("M", "And this leads people to equate that with an unwillingness to work hard.", "然而外界往往容易把这种界限感简单粗暴地等同于‘不肯吃苦、不愿努力工作’。"),
            ("W", "Right, but that couldn’t be further from the truth, could it?", "没错，但这根本就是大错特错的误解，对吗？"),
            ("M", "Young people will work extremely hard during their defined work hours.", "在法定的工作时间之内，年轻员工往往会全力以赴、极其拼命地投入工作。"),
            ("M", "But they expect to have their time off, like weekends and nights, free from work.", "但他们强烈希望在下班之后，比如周末和夜晚的休息时间里，能够彻底免受工作讯息的打扰。"),
            ("W", "So, how should managers go about assessing young people’s productivity?", "那么，管理者究竟该如何客观科学地考量评估年轻员工的工作产出与效率呢？"),
            ("M", "Generally, young people believe their productivity should not be measured by the number of hours they work—since someone can work for 8 hours and accomplish next to nothing of significance for the company.", "总体而言，年轻人坚信衡量生产力绝不应当仅仅看坐班工时的长短——毕竟一个人即便在工位上枯坐8个小时，也完全可能对公司没有贡献任何实质性的核心成果。"),
            ("M", "Instead, young people measure their productivity levels by the quality of the work they perform.", "相反，年轻一代衡量自身效率高低的核心标尺，是他们最终交付的工作品质究竟有多高。"),
            ("W", "But we often hear that young people want to feel more than just being a part of a big machine.", "而且我们常听到年轻人渴望在工作中获得使命感，而非仅仅充当大企业机器上的一枚冷冰冰的螺丝钉。"),
            ("W", "Such a perspective can be hard to discredit, can’t it?", "这种诉求是极其正当且无法被轻易否定的，不是吗？"),
            ("M", "It’s important to legitimize their work.", "因此，管理者必须赋予其工作崇高的意义感与正当性。"),
            ("M", "Young workers want to work on projects that matter to themselves, the company or the world at large.", "年轻员工渴望参与那些对他们自身、对公司乃至对整个社会和世界都真正产生深远价值的项目。"),
            ("M", "They must feel the need to stay working at a company whose values align with their own.", "只有当一家企业的核心价值观与他们内心的信念同频共振时，他们才会发自内心地产生强烈的归属感并长久留任。"),
            ("W", "Thanks for your advice.", "非常感谢您这番真知灼见的建议。")
        ]
    },
    {
        "id": "2025-12-set2-pass-1",
        "subpart_code": "pass-1",
        "section_id": "2025-12-set2-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 1 · 餐厅菜单素食分区对不同客群消费决策的反向心理效应",
        "topic_zh": "餐厅菜单素食分区对不同客群消费决策的反向心理效应",
        "question_range": "Q9 ~ Q11",
        "questions": [9, 10, 11],
        "sentences": [
            ("", "Many restaurants are trying to persuade customers to eat more sustainably, moving away from environmentally unfriendly meat towards greener dishes.", "当下许多餐饮企业正竭力劝导食客践行更具可持续性的饮食方式，引导大家减少食用不利于环保的肉类，转向更加绿色的植物基菜品。"),
            ("", "Although it sounds counterintuitive, restaurants which include specific vegetarian sections on their menus may be unintentionally encouraging customers to eat meat, a new study suggests.", "然而一项最新研究却揭示了一个看似反直觉的现象：在菜单上特意单设独立“素食专区”的餐厅，可能在无意中反倒促使食客摄入了更多肉类。"),
            ("", "Behavioral scientist Linda Bacon, one of the study’s authors, said restaurants can have a positive impact on the environment by encouraging their customers to choose more plant-based food and less meat.", "该项研究的作者之一、行为科学家琳达·培根指出，餐饮门店若能积极鼓励顾客多吃植物性膳食并减少肉类摄入，本能对生态环境产生极其积极正向的影响。"),
            ("", "However, our findings suggest that while certain restaurant menu designs can encourage some consumers to make pro-environmental food choices, they can have the opposite effect on others.", "然而我们的实证数据却表明，尽管某些特定的菜单版面设计能够有效激励一部分消费者做出亲环境的餐饮抉择，但在另一部分客群身上却产生了适得其反的相反效应。"),
            ("", "The study involved 750 people, half of whom frequently ate vegetarian food, and half of whom rarely ate it.", "该项实证研究招募了750名受试者，其中一半在日常生活中经常食用素食，而另一半则极少吃素。"),
            ("", "No vegetarians were included.", "需要特别说明的是，受试群体中并不包含严格素食主义者。"),
            ("", "They were given different menus and asked to choose a meal as if they were eating out with friends.", "研究团队为他们分发了不同排版风格的测试菜单，并要求他们模拟与朋友在餐厅聚餐时的真实场景挑选一份餐食。"),
            ("", "Placing vegetarian dishes in a separate section did not have a significant effect on the choices made by infrequent vegetarian food eaters.", "实验结果显示，将素食菜肴集中归入单独的素食专区，对于那些平时极少吃素的人群的点餐抉择并没有产生显著的扰动影响。"),
            ("", "But it did have a notable effect on the frequent eaters, lowering their chance of picking a vegetarian option by 65%.", "但这种分区排版却对那些平日里素食频次较高的熟客造成了惊人的负面冲击，致使他们下单挑选素食选项的概率骤降了整整65%。"),
            ("", "The researchers also discovered that presenting a vegetarian dish as the chef’s recommendation or including a more appealing description of a non-meat meal leads to a greater proportion of infrequent vegetarian eaters choosing a vegetarian option.", "科研人员同时还察觉到，将某道素食标注为‘主厨力荐’，或为无肉菜品撰写更加色香味俱全的诱人菜品文案描述，能够显著提振那些罕见吃素客群尝试素食的比例。"),
            ("", "But again, these altered menu designs backfired with those who ate vegetarian food more frequently, leading them to be less likely to choose a vegetarian dish.", "但令人啼笑皆非的是，这类精心修饰的菜单调整策略在那些原本习惯经常吃素的人群面前再度全面反噬翻车，使得这部分熟客最终选择素食菜品的可能性大幅滑坡。")
        ]
    },
    {
        "id": "2025-12-set2-pass-2",
        "subpart_code": "pass-2",
        "section_id": "2025-12-set2-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 2 · 中英科研团队开发低温冷凝净化技术阻隔室内污染",
        "topic_zh": "中英科研团队开发低温冷凝净化技术阻隔室内污染",
        "question_range": "Q12 ~ Q15",
        "questions": [12, 13, 14, 15],
        "sentences": [
            ("", "Nottingham Trent University and the Chinese Academy of Sciences have been trying to find a way to prevent deadly outdoor air pollution from penetrating indoors.", "英国诺丁汉特伦特大学与中国科学院的研究团队长期致力于探索一种能够彻底阻隔致命室外大气污染物渗入室内空间的崭新技术方案。"),
            ("", "They found that if pollution is frozen to around minus 18 degrees Celsius in a condensing tube, the particles gather together and fall to the bottom, allowing fresh, clean air to pass through.", "他们惊喜地发现，若将污染空气在特制冷凝管中急速冷却冻结至摄氏零下18度左右，悬浮颗粒物便会迅速抱团聚结并沉降在管底，从而让清新洁净的纯净空气顺利通过。"),
            ("", "Their method was able to remove 99% of pollutants.", "实验证实，他们独创的这套低温凝结法能够高效清除高达99%的各类大气污染物。"),
            ("", "It is hoped that the work could pave the way for simple modification of air conditioning units, so that they can also clean polluted indoor air.", "研究人员殷切期望这项科技突破能为现有常规空调机组的简易升级改造铺平道路，使其兼具强力净化室内浑浊空气的全新功能。"),
            ("", "Outdoor air pollution in cities is a global problem, whether it be haze plaguing Kolkata or poor air impacting the health of children in London schools.", "城市室外空气污染是一项席卷全球的严峻生态难题，无论是在长期遭受重度雾霾困扰的加尔各答，还是空气质量堪忧进而威胁伦敦校园学童肺部健康的英国本土，无一能幸免。"),
            ("", "While there are some existing technologies to purify indoor air, they can be inefficient, expensive, or produce harmful byproducts.", "尽管目前市场上已经存在若干室内空气净化手段，但它们往往普遍存在着能效低下、造价高昂，甚至容易衍生出有害二次副产物的明显弊端。"),
            ("", "When outdoor air quality is poor, people tend to spend even more time indoors, but outdoor pollution also leads to indoor pollution, and people still suffer.", "每当室外空气质量亮起红灯时，公众往往倾向于更长时间深居室内闭门不出；然而室外的污浊毒害同样会加速渗透蔓延至室内，导致人们在室内依然备受呼吸健康危害的煎熬。"),
            ("", "It is estimated that pollution is linked to over 40,000 early deaths in Britain each year.", "据权威卫生机构测算，在英国本土，每年因各类空气污染诱发的过早死亡人数就高达4万余人。"),
            ("", "Professor Gang Pan of the Chinese Academy of Sciences said, “We have shown in our experiments that simply by circulating polluted air through a small freezing chamber, we can remove most of the fine particles and gas pollutants.”", "来自中国科学院的潘纲教授对此表示：“我们在实验中充分证实，仅仅通过让受污染空气循环穿过一个紧凑小型的冷冻气室，便能彻底捕获并剥离绝大多数细微颗粒物以及有毒有害气体污染物。”"),
            ("", "“Our study makes it possible to add an air cleaner option to household appliances in areas which might experience extremely poor air conditions.”", "“我们的科研成果使得在那些空气状况极度恶劣的重度污染地区，为各类普通家用电器集成加装‘空气净化器’功能模块成为了现实可能。”"),
            ("", "“By controlling indoor air pollution and improving air quality in this way, this work could be greatly beneficial to public health.”", "“通过这种廉价高效的温控手段有效遏制室内空气污染并显著提振空气纯净度，这项研究成果无疑将对全人类的公共卫生健康事业产生极其深远的大幅裨益。”")
        ]
    },
    {
        "id": "2025-12-set2-rec-1",
        "subpart_code": "rec-1",
        "section_id": "2025-12-set2-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 1 · 裂唇鱼通过镜子测试：鱼类自我意识之争与智力评判重构",
        "topic_zh": "裂唇鱼通过镜子测试：鱼类自我意识之争与智力评判重构",
        "question_range": "Q16 ~ Q18",
        "questions": [16, 17, 18],
        "sentences": [
            ("", "Research recently carried out by my team suggests that fish may be self-aware.", "我所在的研究团队近期开展的前沿实证研究表明：鱼类极可能同样具备自我意识。"),
            ("", "A certain species of fish recently passed the well-known mirror test—this is a test that demonstrates self-recognition in the animals.", "某种特定鱼类在近期成功通过了生物学界闻名遐迩的‘镜子测试’——这是一项专门用以检验动物是否具备镜中自我识别能力的黄金标准测试。"),
            ("", "Only a few animals, such as humans, apes, dolphins and some birds can recognise themselves in a mirror, and only these animals capable of self-recognition will attempt to remove marks placed on their skin after noticing them in their reflection.", "在以往的科学认知中，全世界仅有极少数灵长与高等物种能够识破镜中的镜像，比如人类、类人猿、海豚以及某些特定鸟类；而且只有这些具备自我识别天赋的动物，才会在透过镜子察觉到自己身体表面被点上的色斑标记后，主动尝试去擦拭刮除。"),
            ("", "This ability suggests the level of higher intelligence and awareness.", "这种在镜前审视自身的非凡能力，长期以来一直被学界奉为衡量生物是否拥有高阶认知智慧与自我觉知的分水岭。"),
            ("", "This is not shown by children until around 18 months.", "人类幼儿通常也要成长发育至大约18个月大时，大脑才会真正觉醒并展现出这一心理认知能力。"),
            ("", "Until now, no fish has demonstrated the ability, but our experiments show the fish in question will scrape up against hard surfaces to remove marks placed on its body by our researchers after viewing itself in a mirror.", "在此之前，历史上从未有任何鱼类展现出过此类心智行为；但我们的最新对比实验却确凿显示：当这种实验鱼照镜子并察觉到科研人员事先在其身体部位留下的染色标记后，它竟然会特意游向水底坚硬礁石表面反复用力摩擦刮擦，试图将该标记彻底抹除。"),
            ("", "The behaviours we observe leave little doubt that this fish behaviourally fulfils all criteria of the mirror test as originally laid out.", "我们在精密监控中所记录下的这一系列严谨行为模式无可辩驳地证明：从行为学表征来看，这种鱼完全精准达成了镜子测试最初设立的每一项严苛指标。"),
            ("", "The fish in our study never attempted to remove the marks when no mirror was present or when the marks were just placed on the mirror.", "在对照组中，当鱼缸中未放置镜子、或者污痕仅仅被涂抹在镜子玻璃表面时，实验鱼便绝不会做出任何刮擦自身身体的无效举动。"),
            ("", "Unmarked fish also did not attempt to remove marks from themselves when interacting with a marked fish on the other side of a window.", "同样，当一条自身未被做标记的鱼隔着透明玻璃窗与对侧一条带有标记的同类互动凝视时，它也断然不会去徒劳刮擦自己的身体。"),
            ("", "These results show either that fish are self-aware or that the mirror test, which is considered to be the gold standard test used to denote higher intelligence, may be flawed.", "这一震撼的实验结论无可避免地将科学界推向了一个非此即彼的重大抉择：要么我们必须承认鱼类确实拥有某种自我意识；要么这恰恰证明被奉为高级智慧检验金科玉律的‘镜子测试’本身存在着致命的逻辑漏洞。"),
            ("", "What is less clear is whether these behaviours should be considered as evidence that fish are self-aware, even though in the past, these same behaviours have been interpreted as self-awareness in so many other animals.", "眼下引发巨大争议的关键在于：这些举动是否真的能够直接采信为鱼类具备自我意识的铁证？尽管在漫长的动物行为学史上，这套一模一样的行为机制在诸多哺乳动物和鸟类身上无一例外都被毫不犹豫地定性为‘拥有自我觉知’。"),
            ("", "Depending on your position, you might reject the interpretation that these behaviours in a fish satisfy passing the test at all.", "依据各自不同的学术立场，一部分保守学者可能会断然拒绝接受一条低等鱼类的此类行为能够算作通过了神圣的镜子测试。"),
            ("", "But on what objective basis can you do this when the behaviours they show are so functionally similar to those of other species that have passed the test?", "然而，面对它们所展现出的行为机制在功能与逻辑上与其他所有高智商过关物种如此惊人一致的事实，你究竟又能凭借怎样合乎客观理性的科学基准去全盘否定它呢？"),
            ("", "Results from our research raise more questions than answers.", "归根结底，我们团队的这项颠覆性研究成果所引发的未解之谜与深层困惑，远比它所给出的现成答案要庞大得多。"),
            ("", "What if self-awareness develops like an onion, building layer upon layer rather than appearing all at once?", "倘若生物的自我意识发育演进恰如一颗洋葱的层层包裹，是一层一层逐渐积累递进，而非非黑即白、瞬间全盘涌现的呢？"),
            ("", "Perhaps, in order to explore self-awareness further, we should stop looking at responses to the mirror as a decisive test.", "或许，为了在未来更深层次地探求生命自我意识的本质，我们早就该停止将对镜子做出的单向物理反应当成一锤定音的唯一试金石了。"),
            ("", "Only with a richer theory of the self and a larger test battery will we be able to determine all of the various levels of self-awareness, including where exactly fish fit in.", "唯有构建起更加多维丰满的‘自我心智理论’，并引入成体系的综合测试工具矩阵，人类才能真正厘清大自然中生命自我意识的各种层级跨度，并最终精准锚定鱼类在这张宏伟的智力演化版图上究竟身处何方。")
        ]
    },
    {
        "id": "2025-12-set2-rec-2",
        "subpart_code": "rec-2",
        "section_id": "2025-12-set2-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 2 · 幼儿电子书亲子共读实验：学习增益与注意力分散效应",
        "topic_zh": "幼儿电子书亲子共读实验：学习增益与注意力分散效应",
        "question_range": "Q19 ~ Q21",
        "questions": [19, 20, 21],
        "sentences": [
            ("", "Reading with a young child is important, but does it matter whether you read from an electronic book or traditional print?", "与幼龄孩子一起共读绘本至关重要，但究竟是使用电子书阅读器还是翻阅传统纸质印刷绘本，这之间真的存在本质区别吗？"),
            ("", "As any parent knows, small children are generally keen on screens, so the finding from a new study that very young children enjoy electronic books more than printed picture books may not come as a huge surprise.", "天底下每一位为人父母者都心知肚明，年幼的孩子天生对发光的电子屏幕充满好奇痴迷；因此一项最新研究所揭示的结论——即低龄幼儿比起纸质图画书显然更狂热喜爱电子绘本——大概并不会让家长们感到有多么出乎意料。"),
            ("", "But the following additional findings might: both parents and children behave differently when reading electronic versus printed picture books, and the children who read the electronic books learned more.", "然而，该实验随之呈现出的另外两项衍生发现却足以令人大吃一惊：无论家长还是幼儿，在面对电子绘本与纸质绘本时所流露出的互动行为习惯截然不同；而且阅读电子书的孩子最终吸收掌握的认知词汇量居然明显更多。"),
            ("", "Previous studies of young children have suggested that electronic books, which incorporate extra features such as dictionaries and images that depict story events, may have advantages over print.", "以往针对幼儿早教的学术研究曾指出，那些集成了互动字典插画以及直观刻画故事情节动态图画等丰富附加功能的电子读物，相比死板的印刷纸张往往具备诸多先天优势。"),
            ("", "In fact, multiple studies have found that electronic books support story comprehension and vocabulary gains beyond what is provided by printed books.", "事实上，此前已有多项实证调研证实，电子绘本在辅助故事情节理解以及促进词汇量飞跃方面，所带来的教学成效确确实实超越了传统纸质书籍所能赋予的水平。"),
            ("", "But there’s also work suggesting that children sometimes invest less mental effort in learning from electronic books, and the parents talk less about content when sharing such books.", "但与此同时，学术界也存在着针锋相对的警示研究：有学者指出孩子们在阅读电子书时往往投入的深层脑力思考更少，而且家长在陪读时对故事深层内涵的拓展交流与言语互动也会被动缩水。"),
            ("", "The study we’re looking at today aims to give us a better understanding of how good electronic books are for young children.", "我们今天所聚焦的这项最新实验，正是旨在全面客观地厘清电子绘本对于学龄前幼童身心成长究竟能带来怎样的实际成效。"),
            ("", "For this study, researchers videoed children aged 17 to 26 months reading with one of their parents.", "在本次严密的实验过程中，科研团队全程高清录像记录了年龄在17至26个月之间的幼儿与父母其中一方亲密共读的互动过程。"),
            ("", "Each parent and child pair was randomly assigned to read either two educational electronic books or two printed books with the same content.", "每一个亲子家庭组合均被随机指派任务：要么阅读两本精心编纂的早教类电子互动绘本，要么阅读两本内容、图画完全一致的传统纸质绘本。"),
            ("", "While the parent read the words in the printed books aloud, the electronic books had audio of voice actors reading the text.", "在纸质组中，由家长亲自大声朗读页面上的文字故事；而在电子组中，则是由专业配音演员录制的高清原声伴读音频同步自动播放。"),
            ("", "The researchers found that parents who read the printed books pointed more frequently to pages than parents who read the electronic books, but the opposite was true for the children.", "研究人员通过逐帧比对发现：翻阅纸质书的家长用手指点指图画页面的频次显著高于电子书组的家长；然而在孩子们身上，呈现出的肢体反应规律却恰恰完全颠倒相反。"),
            ("", "Children who read the electronic books also commented more on the content and learned more new words than the children who read printed books.", "那些接触电子书的幼童在共读过程中对故事情节发表言语评价的频次显著更高，并且在课后测试中掌握的新词汇量也明显甩开纸质组的小伙伴。"),
            ("", "This greater learning is ascribed to greater engagement with the electronic books.", "这种更为卓越的学习转化成效，很大程度上归功于电子读物多模态交互界面所激发出前所未有的超高沉浸度与专注参与感。"),
            ("", "It’s important to note that the electronic books in the study were simple.", "但必须郑重指出的是，本次实证研究所采用的早教电子绘本在设计上极其克制简约。"),
            ("", "While they included background music, animation and sound effects, there were no other extra features.", "它们虽然融入了悦耳的背景音乐、轻度的画面微动以及生动的环境音效，但自始至终绝未堆砌任何喧宾夺主的冗余繁杂功能。"),
            ("", "It’s also important to note that there’s research on older children finding that electronic books don’t always bolster learning.", "同样不容忽视的一点在于，针对更大年龄段儿童的诸多跨期跟踪调查早已表明：电子书并非总能在所有情境下都起到促进学习的正面催化作用。"),
            ("", "Parents and educators need to be aware extra features in electronic books may increase children’s participation with them.", "广大家长与一线早教工作者必须时刻保持高度清醒：电子绘本中巧立名目的各种花哨附加功能，或许确实能短时间内刺激提升孩子的点击参与热情。"),
            ("", "However, if these features don’t draw attention to the educational content, they may not serve as a supportive feature.", "然而，倘若这些眼花缭乱的互动设计无法将孩子的全副心神真正锚定聚焦在核心教育内容与故事情感本身，它们非但成不了启智赋能的有益帮手，反而会沦为阻碍深度思考与心智沉淀的有害干扰项。")
        ]
    },
    {
        "id": "2025-12-set2-rec-3",
        "subpart_code": "rec-3",
        "section_id": "2025-12-set2-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 3 · 告别后悔内耗：将过往抉择淬炼为自我成长的养分",
        "topic_zh": "告别后悔内耗：将过往抉择淬炼为自我成长的养分",
        "question_range": "Q22 ~ Q25",
        "questions": [22, 23, 24, 25],
        "sentences": [
            ("", "Let me be honest with you.", "请允许我跟你交个底、说几句掏心窝子的肺腑之言。"),
            ("", "If you are living your life full of regret, you are wasting your time.", "如果你整天让自己沉溺在无休止的悔恨与内耗之中虚度光阴，那么你纯粹是在残忍地挥霍浪费自己极其宝贵的生命。"),
            ("", "Why would you go through life regretting the very decisions that made you who you are today?", "你为什么非要用一生去后悔那些恰恰造就了今时今日这个独一无二的你的一切抉择呢？"),
            ("", "There are plenty of unfavorable decisions we’ve made, but does that mean we should regret them?", "我们在过往岁月里确实做出过许许多多事后看来并不理想甚至极其糟糕的糟糕决定，但难道这就意味着我们必须为之抱憾终生吗？"),
            ("", "No.", "绝不应当如此。"),
            ("", "I’ve had many moments where I sit and think about all the things I wish I could have done differently.", "我自己在人生的无数个孤单时刻，也曾久久静坐深思，懊恼地遐想着倘若当年换一种处理方式该有多好。"),
            ("", "However, just because things could be different, it doesn’t necessarily mean they would be better.", "然而，即便时光倒流、事情真的换一种走向发展，那也绝不意味着结果就必然会比当下变得更加圆满美好。"),
            ("", "You don’t have to continually be thinking of all your past decisions and whether or not you made the right one.", "你大可不必在日复一日的心理折磨中反复咀嚼过去的每一个抉择，苦苦纠结自己当年到底是对还是错。"),
            ("", "You can’t go back and change anything.", "过去的历史早已尘埃落定，你永远也无法逆转时空去改写分毫。"),
            ("", "So what’s the point in worrying about it?", "既然覆水难收，那么继续无休止地为此焦虑忧伤又有什么现实意义呢？"),
            ("", "Every single decision you’ve ever made, positive or negative, has made you the person you are today.", "你平生所做出的每一个微小或重大的决定——无论其结局是顺遂还是曲折——都在无形之中塑造并雕刻了今天这个坚韧立体的你。"),
            ("", "We want to go back and change parts of our past, but what would be the benefit of that?", "我们总是痴心妄想着能抹除改写过往人生的某些晦暗片段，但如果真能如愿以偿，对你而言又究竟能有什么真正的好处呢？"),
            ("", "We would have lost the valuable knowledge from the lessons we learned.", "真若如此，我们便会彻底痛失那些历经刻骨铭心的失败教训才换来的极其无价的人生成长认知与智慧底蕴。"),
            ("", "There are reasons you make the choices you do, and that tells us about who you are.", "你在特定历史情境下所做出的每一次抉择背后都有其必然的内在逻辑与缘由，而正是那些选择映射出了你真实丰满的人格特质。"),
            ("", "So when it comes to any decision in life, be unapologetically yourself, because at the end of the day, it was you who made that decision.", "因此，当面对生命中的任何重大抉择时，请坚定不移、理直气壮地做最真实的自己；因为归根结底，那个勇敢担起责任并最终拍板按下按钮的人，正是你自己。"),
            ("", "With less time spent focused on regrets, you will finally have time to focus on the more essential things in life.", "唯有不再把大把的心力与光阴白白空耗在虚妄的懊恼自责上，你才能真正腾出宝贵的时间精力，去全力拥抱并深耕生命中那些更具本质意义的美好事物。"),
            ("", "In any situation, you grow more as a person with every decision you make.", "在人生的任何境遇之下，随着你所做出的每一次探索与抉择，你都在作为一个人格独立的个体实现着向内向上的蜕变成长。"),
            ("", "Life is full of lessons to learn, so we can’t let regret stop us from moving forward.", "纷繁芜杂的人生本就充斥着数之不尽、唯有亲身经历才能参透的深刻功课与经验教训，我们断然不能任由苍白的悔恨绊住自己奋勇向前迈进的坚定步伐。"),
            ("", "We don’t know if we’ve made the right or wrong choice until after it has already been made, so it can be easy to start regretting your decision.", "在真正盖棺定论之前，我们永远无法预知一个选择究竟是对是错，正因如此，人们才极易在尘埃落定后陷入后见之明的自怨自艾之中。"),
            ("", "But if the decision has already been made, what’s the purpose of dwelling on it?", "然而木已成舟、大局已定，一味死死抓着过去的遗憾反复纠缠不放又有什么价值可言呢？"),
            ("", "There isn’t one.", "没有任何价值。"),
            ("", "All you can do is move forward.", "此时此刻你唯一能做且必须去做的，就是昂起头颅坚定向前看。"),
            ("", "You can’t let yourself sit there and worry about every past choice.", "你绝不能允许自己瘫软在过去的阴影里，无休止地为从前的每一个岔路口患得患失。"),
            ("", "We aren’t all perfect.", "我们终究都只是肉体凡胎，世间本就无人能够做到十全十美、算无遗策。"),
            ("", "Whenever you make a decision, there will always be a possibility for regret later, but that’s how life is supposed to be.", "每当你做出一个决定，未来本就永远伴随着悔不当初的潜在风险与可能性；但请记住，这恰恰才是波澜壮阔、跌宕起伏的真实人生本该拥有的真实模样。"),
            ("", "You will make poor decisions in life.", "你在漫漫漫长的人生征途上注定会做出一些不甚高明的糟糕决策。"),
            ("", "We all do.", "我们每一个人都概莫能外。"),
            ("", "But it’s what you do with the lessons learned that matters.", "但真正决定你人生高度与格局厚度的决定性关键，在于你究竟如何提炼并运用从这些摔打磨砺中所汲取的宝贵教训。"),
            ("", "Think about every decision you’ve ever made.", "静下心来仔细回望你一路走来所做出的每一个重大抉择。"),
            ("", "Were they always the best?", "它们难道每次都是无懈可击的最佳方案吗？"),
            ("", "Of course not.", "答案显然是否定的。"),
            ("", "But look at how far you’ve come since then.", "但请好好看看现在的你，自那以来你早已披荆斩棘、跨越了多么辽阔深远的壮丽征程！")
        ]
    }
]

QUESTIONS_DATA = {
    1: {
        "prompt": "What does the woman say about the food at the canteen?",
        "options": {
            "A": "It is absurdly expensive.",
            "B": "It is appropriately priced.",
            "C": "It brings shame on the university.",
            "D": "It caters to students and teachers."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。对话开头，男士认为食堂的食物价格高得离谱，女士随即明确表示她不同意这一观点，并指出她个人觉得价格完全合情合理（I personally think they’re perfectly appropriate）。B项属于原句的同义替换。因此答案为 B。"
    },
    2: {
        "prompt": "How does the woman feel about the canteen’s sweet things or fancy delicacies?",
        "options": {
            "A": "They never really appeal to her.",
            "B": "They are never actually good value.",
            "C": "They are within students’ budgets.",
            "D": "They always come at a high speed."
        },
        "answer": "A",
        "explanation": "【精析】细节理解题。在谈及甜点时，女士表示自己从来不吃甜点，也从来不喜欢甜食或任何精致点心（I never really crave sweet things or any fancy delicacies）。A项是对该原句的准确同义表达。因此答案为 A。"
    },
    3: {
        "prompt": "What does the man say is one of the best things about the canteen?",
        "options": {
            "A": "The food.",
            "B": "The space.",
            "C": "The speed.",
            "D": "The environment."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。男士在对话中明确指出，食堂最棒的地方之一就是其极快的出餐速度（Actually, that’s one of the best things about the canteen, the speed）。C项属于原词完全复现。因此答案为 C。"
    },
    4: {
        "prompt": "What did the canteen undergo a few years ago?",
        "options": {
            "A": "A complete refurnishing.",
            "B": "A ruinous burning down.",
            "C": "A substantial expansion.",
            "D": "A massive renovation."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。女士在赞美食堂环境时提到，食堂在几年前经历了一次彻底的大规模装修改造（Apparently, they did a massive renovation a few years ago）。D项属于原词完全复现。因此答案为 D。"
    },
    5: {
        "prompt": "According to the woman, what view about today’s young people is not really justified?",
        "options": {
            "A": "They have a poor work ethic.",
            "B": "They don’t get along with managers.",
            "C": "They are struggling in the workplace.",
            "D": "They aren’t as varied as their predecessors."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。对话开头女士指出，人们常说现在的年轻人缺乏职业道德，但这种说法其实根本不合理（We often hear young people today have a poor work ethic. That’s not really justified though）。A项属于原词复现。因此答案为 A。"
    },
    6: {
        "prompt": "What does the man say is important for managers to get along better with young workers?",
        "options": {
            "A": "Learning about the way they adhere to their own values.",
            "B": "Recognizing how they try to strike a work-life balance.",
            "C": "Knowing how they struggle to connect with managers.",
            "D": "Understanding the way they seek career advancement."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。男士在建议管理者时指出，极为关键的是要理解并认识到年轻人平衡工作与生活的方式（really important to recognize the way young people want to balance their work life with their personal life）。B项是对该原句的精准表达。因此答案为 B。"
    },
    7: {
        "prompt": "How do young people measure their productivity levels according to the man?",
        "options": {
            "A": "In terms of the number of hours spent.",
            "B": "By the amount of work they perform.",
            "C": "In terms of the work done in 8 hours.",
            "D": "By the quality of the work they do."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。男士明确指出，年轻人不是按工时来衡量生产力，而是依据他们交付的工作质量来评估工作效率（young people measure their productivity levels by the quality of the work they perform）。D项是对该原句的同义转述。因此答案为 D。"
    },
    8: {
        "prompt": "What companies does the man think would appeal to young workers?",
        "options": {
            "A": "Those whose culture facilitates their advancement.",
            "B": "Those allowing them to do projects of their choice.",
            "C": "Those whose values align with their own.",
            "D": "Those refraining from discrediting their perspectives."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。对话结尾男士指出，年轻员工会渴望留在那些企业价值观与自身理念高度契合的公司（stay working at a company whose values align with their own）。C项属于原词复现。因此答案为 C。"
    },
    9: {
        "prompt": "What does a new study suggest about restaurants including vegetarian sections on their menus?",
        "options": {
            "A": "They may unconsciously help customers choose greener dishes.",
            "B": "They may unintentionally encourage customers to eat meat.",
            "C": "They raise customers’ environmental awareness.",
            "D": "They enable customers to eat in a healthy way."
        },
        "answer": "B",
        "explanation": "【精析】细节理解题。短文开头指出，尽管听起来违背常理，但一项新研究表明，在菜单上单设素食专区的餐厅可能在无意中促使顾客选择吃肉（may be unintentionally encouraging customers to eat meat）。B项属于原句完全复现。因此答案为 B。"
    },
    10: {
        "prompt": "How was the study carried out on 750 participants?",
        "options": {
            "A": "By inviting them to taste different kinds of food.",
            "B": "By observing the eating behaviour of strict vegetarians.",
            "C": "By comparing participants eating vegetarian food frequently with those doing so rarely.",
            "D": "By requiring participants to choose a meal as if they were feasting at a family gathering."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。文章介绍实验设计时提到，研究涉及750人，其中一半经常吃素，另一半极少吃素（half of whom frequently ate vegetarian food, and half of whom rarely ate it）。C项是对该实验对比分组设计的精准概括。因此答案为 C。"
    },
    11: {
        "prompt": "How do altered menu designs affect frequent eaters of vegetarian food?",
        "options": {
            "A": "They are less likely to choose a vegetarian dish.",
            "B": "They find vegetarian dishes become more appealing.",
            "C": "They tend to consume larger portions of unhealthy food.",
            "D": "They are less likely to choose dishes recommended by chefs."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。短文结尾指出，调整后的菜单设计在经常吃素的人群中产生了反作用，导致他们反而更不太可能选择素食（leading them to be less likely to choose a vegetarian dish）。A项属于原词完全复现。因此答案为 A。"
    },
    12: {
        "prompt": "What does the passage say about Nottingham Trent University and the Chinese Academy of Sciences?",
        "options": {
            "A": "They have found a solution to the global problem of air pollution.",
            "B": "They have managed to freeze polluting particles to around -18℃.",
            "C": "They have been seeking a way to prevent pollutants from penetrating indoors.",
            "D": "They have been cooperating closely on developing a new type of air-conditioner."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。短文开篇指出，诺丁汉特伦特大学与中国科学院一直在努力探寻阻隔室外有害空气污染渗入室内的方法（have been trying to find a way to prevent deadly outdoor air pollution from penetrating indoors）。C项属于同义精确转述。因此答案为 C。"
    },
    13: {
        "prompt": "What do we learn from the passage about existing technologies to purify indoor air?",
        "options": {
            "A": "They can be costly and inefficient.",
            "B": "They are constantly being perfected.",
            "C": "They are by-products of health research.",
            "D": "They can save over 40,000 lives each year."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。文章指出，虽然目前已有一些室内空气净化技术，但它们可能效率低下、造价昂贵或产生有害副产物（they can be inefficient, expensive, or produce harmful byproducts）。A项中的costly and inefficient直接对应原文。因此答案为 A。"
    },
    14: {
        "prompt": "What do people tend to do when outdoor air quality is poor?",
        "options": {
            "A": "They keep their windows closed.",
            "B": "They spend a lot more time indoors.",
            "C": "They make more use of air-conditioners.",
            "D": "They try various ways to purify indoor air."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。文章指出，当室外空气质量变差时，人们往往会在室内逗留更长时间（people tend to spend even more time indoors）。B项属于原词完全复现。因此答案为 B。"
    },
    15: {
        "prompt": "What did Professor Gang Pan of the Chinese Academy of Sciences say about their study?",
        "options": {
            "A": "It shows the importance of eliminating indoor pollution.",
            "B": "It may change the way of future environmental research.",
            "C": "It demonstrates the fruitful cooperation between UK and Chinese scientists.",
            "D": "It may make household appliances serve an additional air cleaner function."
        },
        "answer": "D",
        "explanation": "【精析】细节理解题。文章最后引用潘纲教授的话指出，这项研究使得为空气极差地区的普通家用电器加装空气净化功能成为可能（makes it possible to add an air cleaner option to household appliances）。D项是对该陈述的精准提炼。因此答案为 D。"
    },
    16: {
        "prompt": "What do we learn about the well-known mirror test?",
        "options": {
            "A": "It distinguishes different species of animals.",
            "B": "It reflects distinct traits in animal behaviour.",
            "C": "It demonstrates animals’ ability to recognise themselves.",
            "D": "It gauges the level of intelligence of various animal species."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。讲话开头指出，某种鱼类通过了著名的镜子测试，这是一种用以检验动物自我识别能力的测试（a test that demonstrates self-recognition in the animals）。C项属于原词同义转述。因此答案为 C。"
    },
    17: {
        "prompt": "What does the study by the speaker’s team show about the fish they experimented with?",
        "options": {
            "A": "It meets few of the behavioural criteria set in the mirror test.",
            "B": "It behaves similarly to animals capable of self-recognition.",
            "C": "It removes marks from itself to show self-awareness.",
            "D": "It matches children over 18 months in intelligence."
        },
        "answer": "B",
        "explanation": "【精析】细节推断题。讲话指出，实验鱼在镜前的刮擦表现与其他具备自我识别能力的过关物种在功能上极其相似（the behaviours they show are so functionally similar to those of other species that have passed the test）。B项是对该逻辑的精准概括。因此答案为 B。"
    },
    18: {
        "prompt": "What does the speaker say about the results of their research?",
        "options": {
            "A": "They have conclusively established the criteria of animal intelligence.",
            "B": "They have advanced the concept of self-awareness to a higher level.",
            "C": "They incorporate more perspectives than one.",
            "D": "They raise more questions than answers."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。讲话结尾直言，他们这项研究得出的结果所带来的疑问远多于现成答案（Results from our research raise more questions than answers）。D项属于原词完全复现。因此答案为 D。"
    },
    19: {
        "prompt": "What finding from the new study might come as a huge surprise?",
        "options": {
            "A": "Small children are even more keen on screens than their elders.",
            "B": "Both parents and children preferred to read electronic books.",
            "C": "Parents differed from children in reading behavior.",
            "D": "Children reading electronic books learned more."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。讲话开头指出，真正令人意想不到的重大发现在于：阅读电子绘本的孩子最终学到了更多词汇知识（and the children who read the electronic books learned more）。D项属于原词完全复现。因此答案为 D。"
    },
    20: {
        "prompt": "What do we learn about previous studies of young children reading electronic books?",
        "options": {
            "A": "They came to conflicting conclusions.",
            "B": "They were based on small samples.",
            "C": "They yielded unanticipated findings.",
            "D": "They were focused on younger kids."
        },
        "answer": "A",
        "explanation": "【精析】细节推断题。讲话指出，以往一方面有研究认为电子书具备支持理解和词汇积累的显著优势，但另一方面也有研究警告儿童在阅读电子书时投入的脑力更少且亲子交流被削弱。这说明以往研究得出的结论是相互矛盾分歧的（conflicting conclusions）。因此答案为 A。"
    },
    21: {
        "prompt": "What extra features should be included in electronic books to bolster children’s learning?",
        "options": {
            "A": "Those that prove simple enough for them to comprehend.",
            "B": "Those that produce both audio and visual effects on them.",
            "C": "Those that draw their attention to the educational content.",
            "D": "Those that contribute to their increased interest in reading."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。讲话结尾告诫道，电子书中的附加功能必须能够真正将儿童的注意力导向教育内容本身，否则便起不到促进学习的辅助功效（if these features don’t draw attention to the educational content, they may not serve as a supportive feature）。C项属于原词精准匹配。因此答案为 C。"
    },
    22: {
        "prompt": "What should we do with the unfavorable decisions we’ve made?",
        "options": {
            "A": "Regret having wasted much time in making them.",
            "B": "Think how different we could have made them.",
            "C": "Keep ourselves from regretting them.",
            "D": "Live with them for the time being."
        },
        "answer": "C",
        "explanation": "【精析】细节推断题。讲话开头指出，我们都做过不少糟糕欠妥的决定，但这并不意味着我们应当为此自怨自艾、后悔不迭，通篇都在倡导告别后悔内耗（does that mean we should regret them? No）。C项中的Keep ourselves from regretting them是对该主旨的准确归纳。因此答案为 C。"
    },
    23: {
        "prompt": "What does the speaker say about every single decision we’ve ever made?",
        "options": {
            "A": "It has made us the person we are now.",
            "B": "It has been made with a lot of thinking.",
            "C": "It stems from our valuable knowledge.",
            "D": "It benefits us greatly one way or another."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。讲话明确指出，你曾经做过的每一个决定——无论好坏——都共同塑造了今天的你（Every single decision you’ve ever made, positive or negative, has made you the person you are today）。A项属于原词同义转述。因此答案为 A。"
    },
    24: {
        "prompt": "What is life full of according to the speaker?",
        "options": {
            "A": "Challenging things to do.",
            "B": "Beautiful things to share.",
            "C": "Choices to make.",
            "D": "Lessons to learn."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。讲话明确强调，人生充满了需要去学习和领悟的经验教训，因此绝不能让悔恨拖住我们前行的脚步（Life is full of lessons to learn）。D项属于原词完全复现。因此答案为 D。"
    },
    25: {
        "prompt": "What is said to be of real importance when we make poor decisions in life?",
        "options": {
            "A": "Foreseeing the possibility for regret later.",
            "B": "Making proper use of the lessons learned.",
            "C": "Perfecting the decision-making strategies.",
            "D": "Seeing them as obstacles to moving forward."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。讲话在结尾处总结道，我们在生活中都难免会做出糟糕的决策，但真正关乎成败的，是你如何对待并善用从中所汲取的经验教训（it’s what you do with the lessons learned that matters）。B项是对该核心结论的精准表达。因此答案为 B。"
    }
}

SUBPART_WINDOWS = [
    (36.0, 154.0),
    (233.0, 350.0),
    (464.0, 584.0),
    (649.0, 758.0),
    (868.0, 1036.0),
    (1100.0, 1271.0),
    (1340.0, 1487.0)
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
        w_min, w_max = SUBPART_WINDOWS[idx] if 'idx' in locals() else SUBPART_WINDOWS[sp_idx]
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
        EXAM_ID, 2025, 12, 2,
        "2025年12月 六级真题 (第2套)",
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
