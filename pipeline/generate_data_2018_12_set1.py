#!/usr/bin/env python3
"""
Generate pipeline/data_2018_12_set1.py with 100% golden standard:
- 7 Subparts with authentic titles, Chinese topics, and question ranges
- Complete grammatical sentences with 100% paired authentic Chinese translations
- 25 Official CET-6 questions with full options, verified answers, and detailed explanations
"""

import pprint
from pathlib import Path

EXAM_ID = "2018-12-set1"

SUBPARTS = [
    {
        "id": f"{EXAM_ID}-conv-1",
        "subpart_code": "conv-1",
        "section_id": f"{EXAM_ID}-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 1 · 一本写给大众的物理学书：西尔维亚·蒙德斯、书中谬误与动手实验",
        "topic_zh": "《物理世界》一书的特色与价值：面向各阶层读者、写入女性科学家轶事、揭露谬误与提供可操作实验",
        "question_range": "Q1 ~ Q4",
        "questions": [1, 2, 3, 4],
        "sp_start": 38.64,
        "sp_end": 236.00,
        "sentences": [
            ("M", "Hey, I just read a great book about physics. I think you'd like it. It's called The Physics of the World. It's written by a scientist named Sylvia Mundus.",
             "嘿，我刚读了一本很棒的物理学书。我想你会喜欢它的。书名叫《物理世界》，作者是一位名叫西尔维亚·蒙德斯的科学家。"),
            ("W", "Oh, I read that book. It was great. The writer is a warm and competent guide to the mysteries of physics. I think it promises enrichment for any reader, from those who know little about science to the career physicist.",
             "哦，这本书我读过。特别棒。作者是一位热情而又称职的向导，引领读者开启物理学奥秘之旅。我想这本书会让每一位读者受益匪浅，从对科学知之甚少者到职业物理学家，无一例外。"),
            ("M", "And it's refreshing to see a strong, curious, clever woman adding her voice to the scientific discourse in a field that has been traditionally dominated by men. I think she is to be commended for making an effort to include anecdotes about little-known female scientists. You know, they were often victims of a generation firmly convinced that the woman's place was in the home.",
             "而且，看到一位坚强的、好求知的、聪慧的女性在传统上由男性主导的学术领域发出声音，也让人耳目一新。我认为她值得称道，因为她在书中纳入了鲜为人知的女性科学家的轶事。你知道，她们往往曾是那个坚信「女人该待在家里」的时代的受害者。"),
            ("W", "I like how the book is clearly written with each chapter brought to life by pieces of fascinating knowledge. For example, in one chapter she exposes a myth that I've heard taught by university physics professors. I've often heard that medieval glass windows are thicker at the bottom because glass flows like a fluid. This, she shows, is not true; the distortion is actually thanks to a peculiarity of the glassmaker's process.",
             "我喜欢这本书清晰的写作风格，书中引入许多有趣知识，使每一章节都生动鲜活。例如，在某一章里她揭露了一个我曾听大学物理教授讲授过的谬误。我常听说中世纪的玻璃窗底部更厚是因为玻璃会像液体一样流动。她指出这并非事实，这种变形实际上要归功于玻璃制造工艺的特殊性。"),
            ("M", "Yeah. I like how she cultivates scientific engagement by providing a host of do-it-yourself experiments that bring the same foundational principles of classical physics that govern everything from the solar system to your kitchen table. From using complex laws of physics to test whether a spinning egg is cooked to measuring atmospheric pressure by lifting a piece of cardboard, her hands-on examples make her book a truly interactive read.",
             "是的。我喜欢她通过提供大量自己动手的实验来培养人们对科学的参与感，这些实验把支配从太阳系到你的餐桌上种种物质的经典物理学基本原理都用上了。从运用复杂物理定律来测试旋转的鸡蛋是否煮熟，到通过举起一块硬纸板来测量大气压，她那些亲手操作的例子使这本书成为一种真正的交互式阅读体验。"),
            ("W", "Yes, I must say this equation-free book is an ideal read for scientists of all stripes, anyone teaching science and even people who dislike physics.",
             "是的，我必须说这本无等式的书对于各行各业的科学家、每一位科学教师，甚至是不喜欢物理之人，都是理想的读物。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-conv-2",
        "subpart_code": "conv-2",
        "section_id": f"{EXAM_ID}-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 2 · 学位论文选题困局：论题过大需缩小、以休谟传记为切入点并遵守规范",
        "topic_zh": "学生与教授讨论美学论文选题：论题过于宽泛需收窄、真实兴趣在自然、按指定论题与规范写作",
        "question_range": "Q5 ~ Q8",
        "questions": [5, 6, 7, 8],
        "sp_start": 236.00,
        "sp_end": 418.00,
        "sentences": [
            ("M", "Hi, professor! I was hoping could have a moment of your time if you are not too busy. I'm having some problems getting started on my dissertation and I was hoping you could give me some advice on how to begin.",
             "您好，教授！如果您不太忙的话，我想占用您一点时间。我的学位论文开题遇到了一些问题，希望您能给我一些建议，告诉我该怎么入手。"),
            ("W", "Sure. I have quite a few students though. So can you remind me what your topic is?",
             "当然可以。不过我学生有点多，您能告诉我您的论题是什么吗？"),
            ("M", "The general topic I chose is aesthetics. But that's as far as I've got. I don't really know where to go from there.",
             "我选的大论题是美学，但目前为止我就做了这么个选择。我其实不太清楚接下去该往哪个方向下手。"),
            ("W", "Yeah, that's much too large a topic. You really need to narrow it down in order to make it more accessible, otherwise you will be writing a book.",
             "是的，这个论题太大了。你确实需要把论题缩小，让它更易着手，否则你得写成一本书了。"),
            ("M", "Exactly. That's what I wanted to ask you about. I was hoping it would be possible for me to change topics. I'm really more interested in nature than beauty.",
             "没错，这就是我想问您的。我希望能换个论题，相比之下我对自然更感兴趣。"),
            ("W", "I'm afraid you have to adhere to the assigned topic. Still, if you are interested in nature, then that certainly can be worked into your dissertation. We've talked about Hume before in class, right?",
             "恐怕你还是得继续研究指定的论题。不过，如果你对自然感兴趣，那当然可以把它写进论文里。我们之前在课上讲过休谟，不是吗？"),
            ("M", "Oh yeah. He's the philosopher who wrote about where our ideas of beauty come from.",
             "哦，对。他就是那位著述过我们关于美的观点从何而来的哲学家。"),
            ("W", "Exactly. I suggest you go to the library and get a copy of his biography. Start from there. But remember to stick to the parameters of the assignment. This paper is a large part of your cumulative grade, so make sure to follow the instructions. If you take a look at his biography, you can get a good idea of how his life experiences manifest themselves in his theories of beauty, specifically, the way he looked towards nature as the origin of what we find beautiful.",
             "没错。我建议你去图书馆借一本他的传记，以此为起点。但要记住，必须遵守作业规范。这篇论文在你的总成绩里占很大比重，所以一定要遵循要求。如果你读了他的传记，就能很好地了解他的生活经历如何体现在他的美学理论中，确切地说，是他如何将自然看作美好事物的起源。"),
            ("M", "Great! Thanks for taking the time to answer my questions, professor. I'll let you get back to class now.",
             "太好了！感谢您花时间回答我的问题，教授。现在您可以回去上课了。"),
            ("W", "If there is anything else you need, please come see me in my office anytime.",
             "如果你还有其他需要，欢迎随时来我的办公室。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-pass-1",
        "subpart_code": "pass-1",
        "section_id": f"{EXAM_ID}-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 1 · 北极冬季气温异常飙升：格陵兰零点六度、海冰反馈环路与二十年无冰之夏",
        "topic_zh": "北极气温异常升高现象：气候反馈环路加速变暖、生态与原住民受挑战、北极或将提前无冰",
        "question_range": "Q9 ~ Q11",
        "questions": [9, 10, 11],
        "sp_start": 449.00,
        "sp_end": 632.50,
        "sentences": [
            ("M", "During the Arctic winter from October to March, the average temperature in the frozen north typically hovers around minus 20 degrees Celsius. But this year, the Arctic is experiencing much higher temperatures.",
             "在北极的冬季（十月至次年三月），冰封的北方平均气温通常徘徊在零下 20 摄氏度左右。但今年，北极正在经历高得多的温度。"),
            ("M", "On February 20th, the temperature in Greenland climbed above freezing or zero degrees Celsius and it stayed there for over 24 hours. Then, on February 24th, the temperature on Greenland's northern tip reached 6 degrees Celsius. Climate scientists described the phenomenon as stunning.",
             "2 月 20 日，格陵兰岛的气温攀升至冰点（零摄氏度）以上，且持续时间超过 24 小时。随后，在 2 月 24 日，格陵兰岛最北端气温达到了 6 摄氏度。气候科学家认为这一现象令人震惊。"),
            ("M", "Weather conditions that drive this bizarre temperature surge have visited the Arctic before. They typically appear about once in a decade. However, the last such increase in temperature took place two years ago.",
             "造成气温异常升高的各种天气条件，此前也曾造访北极。它们通常十年一遇。但上次出现这样的气温上升却是在两年前。"),
            ("M", "This is troubling as climbing Arctic temperatures combined with rapid sea-ice loss are creating a new type of climate feedback loop which could accelerate Arctic warming. Indeed, sea-ice cover in the Arctic is melting faster than expected. Without those masses of cooling sea ice, warm air brought to the Arctic can penetrate further inland than it ever did before. The air can stay warmer longer, too. This drives additional melting.",
             "这一现象令人担忧，因为北极气温攀升，连同海面浮冰迅速减少，正在建立起一种新的气候反馈环路，进而加速北极变暖。事实上，覆盖北极海面的浮冰融化速度比预想的更快。没有那些起冷却作用的大片海面浮冰，被带到北极的暖空气就能深入至之前它从未到达的内陆地区。暖空气也会保持更高温度，停留时间也会变长。这将导致浮冰进一步融化。"),
            ("M", "Overall, Earth is warming at a rapid pace—2014 through 2017 rank as the hottest years on record—and the Arctic is warming twice as fast as anyplace else on Earth. This raises unique challenges for Arctic wildlife and indigenous people who depend on Arctic ecosystems to survive.",
             "总的来说，地球正迅速变暖（2014 年至 2017 年被认为是有记录以来最热的年份），而北极变暖的速度是地球上其余各地的两倍。这会给依赖北极生态系统生存的当地野生动植物和原住民带来极不寻常的挑战。"),
            ("M", "Previously, climate forecasts predicted that Arctic summer ice would disappear entirely by around 2060. But based on what scientists are seeing now, the Arctic may be facing summers without ice within 20 years.",
             "此前，气候预测曾指出，北极夏季的浮冰到 2060 年左右将会完全消失。但根据科学家如今的观测，20 年之内北极或许就会面临没有浮冰的夏季。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-pass-2",
        "subpart_code": "pass-2",
        "section_id": f"{EXAM_ID}-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 2 · 如何提升意志力：相信自己拥有它、欧美受试者差异与可改变的自我认知",
        "topic_zh": "意志力的自我认知研究：相信自身意志力储备充足即可提升表现、欧美受试者对比与信念可改变性",
        "question_range": "Q12 ~ Q15",
        "questions": [12, 13, 14, 15],
        "sp_start": 632.50,
        "sp_end": 828.50,
        "sentences": [
            ("M", "A good dose of willpower is often necessary to see any task through, whether it's sticking to a spending plan or finishing a great novel. And if you want to increase that willpower, a new study suggests you just simply have to believe you have it.",
             "要完成任何一项任务，强大的意志力往往必不可少，无论是坚持执行一项支出计划还是坚持读完一部伟大小说。而且一项新研究表明，如果你想提升这种意志力，你仅仅需要相信自己拥有它。"),
            ("M", "According to the study, what matters most is what we think about our willpower. If we believe it's a finite resource, we act that way. We feel exhausted and need breaks between demanding mental tasks. However, people who view their willpower as a limitless resource get energized instead.",
             "根据这项研究，最重要的是我们如何看待自己的意志力。如果我们认为它是一种有限的资源，那我们便会以此行事。我们会感到精疲力竭，需要在高难度的脑力劳动之间暂停。然而，将自己的意志力视为永不枯竭资源的人，却能保持精力充沛。"),
            ("M", "The researchers used a psychological assessment tool to test the validity of the study. They asked one thousand one hundred Americans and one thousand six hundred Europeans to grade different statements such as After a challenging mental activity, my energy is depleted and I must rest to get it refueled again or I can focus on a mental task for long periods without feeling tired. Although there was little difference between men and women overall, Americans were more likely to admit to needing breaks after completing mentally challenging tasks. European participants, on the other hand, claimed they were able to keep going.",
             "研究者使用一种心理评估工具对研究的效度进行了测试。他们让 1100 名美国人和 1600 名欧洲人给不同的表述打分，比如「在一项挑战性脑力活动之后，我的能量会耗尽，我必须休息以补充能量」或「我可以长时间专注于一项脑力工作而不感到疲惫」。尽管总体上男性和女性几乎没有差异，但美国人更可能承认自己在完成挑战性脑力任务后需要休息，而欧洲参与者则声称自己能够继续坚持。"),
            ("M", "Based on the findings, the researchers suggest that the key to boosting your willpower is to believe that you have an abundant supply of it. Your feelings about your willpower affect the way you behave. But these feelings are changeable, they said. Changing your beliefs about the nature of your self-control can have positive effects on character development. This leads to healthier behaviors and perceptions of other people.",
             "基于以上发现，研究者表示，提升意志力的关键在于相信自己有充足的意志力供应。你对自己意志力的感受会影响你的行为方式。但这些感受是可变的，他们说道。改变你对于自控力本质的信念，可以对人格发展产生积极效应，这会带来更健康的行为，以及对他人更健全的认知。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-rec-1",
        "subpart_code": "rec-1",
        "section_id": f"{EXAM_ID}-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 1 · 机器学习与就业未来：牛津研究、Kaggle 作文评分与依赖过往数据的根本局限",
        "topic_zh": "机器学习的职业冲击与能力边界：半数工作面临自动化、评分程序媲美人类教师、依赖海量历史数据的短板",
        "question_range": "Q16 ~ Q18",
        "questions": [16, 17, 18],
        "sp_start": 856.00,
        "sp_end": 1082.00,
        "sentences": [
            ("M", "Here is my baby niece Sarah. Her mom is a doctor and her dad is a lawyer. By the time Sarah goes to college, the jobs her parents do are going to look dramatically different.",
             "这是我的小侄女萨拉。她的妈妈是医生，爸爸是律师。到萨拉上大学的时候，她父母的工作看起来将会非常不同。"),
            ("M", "In 2013, researchers at Oxford University did a study on the future of work. They concluded that almost one in every two jobs has a high risk of being automated by machines. Machine learning is the technology that's responsible for most of this disruption. It's the most powerful branch of artificial intelligence. It allows machines to learn from data and copy some of the things that humans can do.",
             "2013 年，牛津大学的研究人员开展了一项关于工作未来的研究。他们的结论是，几乎每两份工作中就有一份面临着被机器自动化的高风险。机器学习这项技术是造成这一动荡的主要原因。它是人工智能最强大的分支，它使得机器能够从数据中学习，并模仿人类能做的一部分事情。"),
            ("M", "My company, Kaggle, operates on the cutting edge of machine learning. We bring together hundreds of thousands of experts to solve important problems for industry and academia. This gives us a unique perspective on what machines can do, what they can't do and what jobs they might automate or threaten.",
             "我所在的公司 Kaggle 走在机器学习的最前沿。我们集结了成百上千名专家，为业界和学界解决重大问题。这让我们对机器能做什么、不能做什么，以及哪些工作岗位会被自动化或受威胁等问题形成了独特的视角。"),
            ("M", "Machine learning started making its way into industry in the early nineties. It started with relatively simple tasks. It started with things like assessing credit risk from loan applications, sorting the mail by reading handwritten zip codes. Over the past few years, we have made dramatic breakthroughs. Machine learning is now capable of far, far more complex tasks. In 2012, Kaggle challenged its community to build a program that could grade high-school essays. The winning programs were able to match the grades given by human teachers.",
             "机器学习在 90 年代早期进入产业界。它最初所做的工作相对简单，一开始用于评估贷款申请的信用风险、识别手写邮编以分类信件。在过去的几年中，我们已取得巨大突破，机器学习如今足以胜任复杂得多的工作。2012 年，Kaggle 向它的社群发布一项挑战，号召开发能对高中作文进行评分的程序，胜出程序给出的分数与人类教师的评分结果相契合。"),
            ("M", "Now, given the right data, machines are going to outperform humans at tasks like this. A teacher might read 10,000 essays over a 40-year career. A machine can read millions of essays within minutes. We have no chance of competing against machines on frequent, high-volume tasks.",
             "如今，在输入适当的数据后，机器在此类任务上的表现要优于人类。一名教师在 40 年的教学生涯中大概能看 1 万篇作文，而一台机器几分钟就能看上百万篇作文。在大批量重复性任务方面，我们面对机器毫无胜算。"),
            ("M", "But there are things we can do that machines cannot. Where machines have made very little progress is in tackling novel situations. Machines can't handle things they haven't seen many times before. The fundamental limitation of machine learning is that it needs to learn from large volumes of past data. But humans don't. We have the ability to connect seemingly different threads to solve problems we've never seen before.",
             "但有一些事情我们能做而机器做不来。在应对新情况方面，机器的进展甚微。机器无从应对那些它没怎么见过的情况。机器学习的根本局限性在于，机器需要从大量的过往数据中学习。但是人类不需要。我们有能力把看似不同的各种细节串联起来，解决我们从未遇到过的问题。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-rec-2",
        "subpart_code": "rec-2",
        "section_id": f"{EXAM_ID}-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 2 · 太阳能蒸汽火车设想：萨克拉门托聚光镜、无火驱动与相变材料储热",
        "topic_zh": "工程师的太阳能蒸汽火车梦：无火驱动的十公里线路、聚光镜产汽与相变材料及钙化合物储热实验",
        "question_range": "Q19 ~ Q21",
        "questions": [19, 20, 21],
        "sp_start": 1082.00,
        "sp_end": 1319.00,
        "sentences": [
            ("M", "We've talked recently about the importance of sustainable energy. We've also talked about the different theories on how that can be done. So far, our discussions have all been theoretical. Now I have a practical question for you all. Can you run a 140,000-kilogram train on just the steam generated by solar power? Well, one engineer, Tim Castleman, believes it's possible.",
             "最近，我们已经谈论过可持续能源的重要性，也谈到了关于如何实现能源可持续的各种理论。迄今为止，我们的讨论都是理论性的。现在，我要问你们所有人一个实际的问题：你们能完全依靠太阳能产生的蒸汽来驱动一辆重达 140 吨的火车吗？工程师蒂姆·卡斯尔曼相信这是可以实现的。"),
            ("M", "And his home city of Sacramento, California should see the technology's first test. As part of the upgrading of its rail yard, Castleman, who is an inventor and self-proclaimed steam visionary, is campaigning for a new steam train that runs without any fire and could run on an existing 10-kilometer line, drawing tourists and perhaps offering city commuters a green alternative to their cars.",
             "而他的家乡、加利福尼亚州的萨克拉门托，将见证这一技术的首次测试。作为萨克拉门托铁路场段升级的一部分，发明家、同时又自命为蒸汽动力梦想家的卡斯尔曼正发起一场新型蒸汽火车运动：这种火车运行时无需火力推动，且能在现有的 10 公里路段上行驶，可以吸引游客，也可为城市通勤者提供一种替代汽车的绿色交通工具。"),
            ("M", "Castleman wants to build an array of solar magnifying mirrors at one end of the line to collect and focus heat onto water-filled tubes. This would generate steam that could be used to fill tanks on a small steam train without the use of fire. Supplying power to trains in this way would offer the shortest distance from well to wheels, he says, with the least amount of energy lost. According to Harry Valentine, a Canadian engineer who is researching modern steam technology, a special tank measuring 2 by 10 metres could store over 750 kilowatt-hours of energy as high-pressure steam, enough to pull a two-car train for an hour or so.",
             "卡斯尔曼想在这条路段的一端建造一组太阳能聚光镜，收集热量并将其集中到装满水的管道之上。这样无需用火就会产生蒸汽，蒸汽可用以填充小型蒸汽火车上的水罐。他说，以这种方式为火车提供动力，能提供「从油井到车轮」的最短路径，能量损耗最小。据哈里·瓦伦汀（一名研究现代蒸汽技术的加拿大工程师）称，一个 2×10 米的专用罐体可以以高压蒸汽的形式储存超过 750 千瓦时能量，这足以驱动一列两节车厢的火车行驶一小时左右。"),
            ("M", "Energy to drive a steam locomotive can be stored in other materials besides water. For example, a team at Tohoku University in Japan has studied materials that can store large amounts of heat. When heated, these materials turn from a solid into a liquid absorbing energy as they change phase. The liquid is maintained above its melting point until steam is required, at which point the liquid is allowed to turn back into a solid, releasing its stored energy.",
             "驱动蒸汽机车的能量也可以储存在水以外的其它物质中。比如，日本东北大学的一个团队对多种能储存大量热量的物质进行了研究。受热时，这些物质会由固体转化为液体，物态转化过程中会吸收能量。液体被保持在熔点以上，直到需要蒸汽时才被转化为固体，同时释放其储存的能量。"),
            ("M", "Another team, at Nagoya University in Japan, has tested calcium compound as an energy storage material. Heating this chemical compound drives off carbon dioxide gas, leaving calcium oxide. The gas can be stored under pressure in a tank. To recover the energy, the gas is fed back over the calcium oxide. In theory, says Valentine, this can create a high enough temperature to generate superheated steam.",
             "日本名古屋大学的另一团队测试了钙化合物能否用作储能材料。加热这一化合物会释放二氧化碳气体，留下氧化钙。该气体可以在一定压力下储存于罐中。要回收能量时，再将气体通入氧化钙。瓦伦汀说，理论上，这一过程产生的高温足以生成过热蒸汽。"),
        ],
    },
    {
        "id": f"{EXAM_ID}-rec-3",
        "subpart_code": "rec-3",
        "section_id": f"{EXAM_ID}-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 3 · 英国老年人护理危机的两大成因：医疗与社护脱节、预算削减与长期歧视",
        "topic_zh": "英格兰老年护理体系危机：国民医疗与社会护理关系欠佳、志愿服务传统、80年代预算削减与根深蒂固的年龄歧视",
        "question_range": "Q22 ~ Q25",
        "questions": [22, 23, 24, 25],
        "sp_start": 1319.00,
        "sp_end": 1525.50,
        "sentences": [
            ("M", "Today's crisis in care for older people in England has two main causes. First, people are living longer with a lot more complex needs. Second, they rely on a system that has long been marked by a poor relation between national health and social care services.",
             "如今英国的老年人护理危机有两个主要原因。首先，人们的寿命更长，需求更复杂。其次，他们依赖的是一个长期以「国民医疗保健和社会护理服务关系欠佳」为特征的体系。"),
            ("M", "Current services originate in two key measures. They are the National Health Service and the 1948 National Assistance Act. This required local governments to provide residential accommodation for older people and supervise care homes run by independent organizations. They also provided home and community services, including meals, day centres and home helpers and other subsidized services. The National Health Service was free and wholly publicly provided. It delivered the best health care for all. No such vision guided residential and community care, though. The care was substantially provided by voluntary services which worked together with local authorities as they long had, with eligibility based on income.",
             "当前服务源于两项重要法案，即《国民医疗服务法》和 1948 年的《国民救助法》。这要求地方政府为老年人提供住宿，并对由独立机构经营的养老院进行监督。它们还提供家庭和社区服务，包括膳食、日托中心和家庭帮佣以及其他补贴服务。国民医疗服务免费，完全由政府提供，它为所有人提供最好的医疗保健。然而，没有这样的愿景来指导院舍护理及社区护理。这些护理大部分是由志愿服务机构提供的，这些机构长期与地方政府合作，根据收入多少确定公民是否有资格得到护理。"),
            ("M", "Today, life expectancy has risen from 66 for a male at best in 1948 to around 80 now. In addition, there is better overall health and improved medical knowledge in care. This means an unprecedented number of people are surviving longer in conditions requiring experts' support. Families provide at least as much care as they ever did. Even so, they can rarely, without subsidized support, address serious personal needs. Care for older people has faced persistent criticism as these trends became apparent.",
             "今天，男性平均寿命已经从 1948 年的最高 66 岁提高到现在的约 80 岁。此外，人们的整体健康水平和护理方面的医学知识均得以提升。这意味着数量空前的人口在依赖于专家支持的环境中活得更长久。家庭所提供的照护至少和以前一样多。但即便如此，若没有补贴性援助，他们依然很难解决重大的个人需求。随着这些趋势越来越明显，老年人护理面临的批评从未中断。"),
            ("M", "From the early 1960s, local authorities were required to plan health and welfare services. The aim was to enable older people to remain in their own homes for as long as possible. But this increased concern about the lack of coordination between free health and paid-for social care. Through the 1970s, a number of measures sought to improve matters.",
             "从 20 世纪 60 年代初开始，地方政府被要求对健康及福利服务进行规划，目的是使老年人尽可能长时间地生活在自己的家里。但这增加了人们对「免费医疗服务与有偿社会护理之间缺乏协调」的担忧。在整个 20 世纪 70 年代，政府出台了大量措施致力于改善这一状况。"),
            ("M", "However, at a time of financial crisis, funding diminished and little changed. In the 1980s, the government cut spending. Meanwhile, preference for private over public services made management even more difficult. Simultaneously, the number of sick older people grew. Governments emphasized the need to improve services. They did so, though, while doing little to stop the erosion of available aid.",
             "然而，金融危机期间，资金持续减少，情况几乎未见改观。20 世纪 80 年代，政府削减支出。而且，人们青睐私营服务胜于公共服务，使得管理更加困难。与此同时，患病老人的数量也在增加。政府强调需要改进服务，然而他们这样做的同时，却并未采取什么措施来阻止可用援助的削弱。"),
            ("M", "Services were irregular across authorities. Unless you were prepared to pay, they were increasingly difficult to obtain for any but the most severely disabled.",
             "各个部门提供的服务都是不规则的。除非你打算付钱，否则除最严重的残障人士之外，人们越来越难以获得服务。"),
            ("M", "Why has sixty years of criticism produced so little change? Discrimination against older people has a long history. Additionally, those affected by inadequate health and social care are too vulnerable to launch the protests that have addressed other forms of discrimination.",
             "为什么持续 60 年的批评只带来了如此小的改变？对老年人的歧视由来已久。此外，受医疗服务及社会护理不足影响的群体极为弱势，难以发起解决其他形式歧视问题所使用的抗议活动。"),
        ],
    },
]

QUESTIONS = {
    1: {
        "prompt": "What does the woman say about the book the man recommended?",
        "options": {
            "A": "It can benefit professionals and non-professionals alike.",
            "B": "It lists the various challenges physicists are confronting.",
            "C": "It describes how some mysteries of physics were solved.",
            "D": "It is one of the most fascinating physics books ever written.",
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。设题要点为表明观点处。第 2 段女士说：“I think it promises enrichment for any reader, from those who know little about science to the career physicist.”benefit 同义替换 promises enrichment，professionals 与 non-professionals 分别对应 career physicist 与 those who know little about science。因此答案为 A)。B) 由 the mysteries of physics 曲解而来，将静态事物「物理学奥秘」误解为动态事物「物理学家当前正在应对的挑战」；C) 将 a guide to the mysteries of physics 由「物理学奥秘本身」偷换为「奥秘如何被解开」；D) 将第 4 段「这本书充满有趣的知识」夸大为「有史以来最有趣的物理学书籍之一」。",
    },
    2: {
        "prompt": "What can we find in the book the man recommended?",
        "options": {
            "A": "Physicists' contribution to humanity.",
            "B": "Stories about some female physicists.",
            "C": "Historical evolution of modern physics.",
            "D": "Women's changing attitudes to physics.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为表明观点处。第 3 段说：“I think she is to be commended for making an effort to include anecdotes about little-known female scientists.”stories 同义替换 anecdotes，scientists 实指物理学家。因此答案为 B)。A) 利用「物理学家对人类做出贡献」的常识捏造，原文并未提及；C)、D) 均由 a field that has been traditionally dominated by men 望文生义出「历史演变」「态度转变」，但文意关乎的是物理学领域男女地位的失衡，而非这两者。",
    },
    3: {
        "prompt": "How does the author bring her book to life?",
        "options": {
            "A": "By exposing a lot of myths in physics.",
            "B": "By describing her own life experiences.",
            "C": "By including lots of fascinating knowledge.",
            "D": "By telling anecdotes about famous professors.",
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。设题要点为方式引出处。第 4 段首句说：“I like how the book is clearly written with each chapter brought to life by pieces of fascinating knowledge.”即每一章节都因引入许多有趣知识而生动鲜活，C) 与之相符。因此答案为 C)。A)、B)、D) 均由本段第二句「她揭露了一个我曾听大学物理教授讲授过的谬误」捏造而来，但该句句首的 For example in one chapter 表明它只是首句结论的例证，用来说明「该书囊括了很多有趣知识」，并非全书生动的原因。",
    },
    4: {
        "prompt": "How does the book cultivate readers' interest in physics?",
        "options": {
            "A": "It avoids detailing abstract concepts of physics.",
            "B": "It contains a lot of thought-provoking questions.",
            "C": "It demonstrates how they can become physicists.",
            "D": "It provides some experiments they can do themselves.",
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。设题要点为方式引出处。第 5 段说：“I like how she cultivates scientific engagement by providing a host of do-it-yourself experiments.”engage 有「吸引（兴趣、注意）」之意，此处可理解为「培养兴趣」，D) 正确对应这一做法。因此答案为 D)。A) 利用「抽象概念让人蒙圈」的常识干扰，原文并未提及任何「抽象概念」字眼；B)、C) 均由第 5 段末句捏造，「测试旋转的鸡蛋是否煮熟」「举起硬纸板测量大气压」都是用来说明书中包含大量可自己动手的实验，与「发人深思的问题」「如何成为物理学家」无关。",
    },
    5: {
        "prompt": "What is the man's problem?",
        "options": {
            "A": "He is too busy to finish his assignment in time.",
            "B": "He does not know what kind of topic to write on.",
            "C": "He does not understand the professor's instructions.",
            "D": "He has no idea how to proceed with his dissertation.",
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。设题要点为说明问题处。第 3 段学生说：“I don't really know where to go from there.”即选定大论题之后不知该如何着手，D) 是其同义转述，其中 proceed with 与 go from there 均表示「继续进行某事」。因此答案为 D)。A) 由第 1 段碎片信息 too busy 曲解而来，实际是学生确认教授是否忙碌，而非自己太忙；B) 与第 3 段「我选择的大论题是美学」不符；C) 由第 8 段教授要求「必须遵循作业要求」曲解为「学生未理解教授要求」。",
    },
    6: {
        "prompt": "What does the professor think of the man's topic?",
        "options": {
            "A": "It is too broad.",
            "B": "It is a bit outdated.",
            "C": "It is challenging.",
            "D": "It is interesting.",
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。设题要点为评述处与建议处。第 4 段教授说：“that's much too large a topic. You really need to narrow it down...”large 与 broad 均有「宽泛、范围大」之意，narrow it down（缩小论题）也从侧面印证了这一点。因此答案为 A)。B) 属于无中生有；C) 由学生「不知道该往哪个方向下手」与教授「使它更易着手」曲解出「论题具有挑战性」，但由 too large a topic、narrow it down、otherwise you will be writing a book 可知该建议关乎「论题过大」，而无关乎难度；D) 由 interested 一词臆测，实际是说明学生感兴趣的论题，而非教授认为学生的论题有趣。",
    },
    7: {
        "prompt": "What is the man really more interested in?",
        "options": {
            "A": "Biography.",
            "B": "Nature.",
            "C": "Philosophy.",
            "D": "Beauty.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为比较处。第 5 段学生说：“I'm really more interested in nature than beauty.”即比起美学，他对自然更感兴趣，B) 正确并同时排除 D)。因此答案为 B)。A) 将第 8 段教授建议「阅读休谟的传记」曲解为「学生感兴趣的论题是传记」；C) 由第 7 段 philosopher 一词曲解而来，但那里是指休谟的身份为「哲学家」，而非学生感兴趣的内容是「哲学」。",
    },
    8: {
        "prompt": "What does the professor say the man has to do?",
        "options": {
            "A": "Improve his cumulative grade.",
            "B": "Develop his reading ability.",
            "C": "Stick to the topic assigned.",
            "D": "List the parameters first.",
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。设题要点为要求说明处。第 6 段教授说：“I'm afraid you have to adhere to the assigned topic.”与 C) 相符。因此答案为 C)。A) 将「论文在总成绩中占很大比重」曲解为教授对学生的要求「提高总成绩」；B) 由教授推荐阅读休谟传记曲解而来，由第 8 段可知推荐目的是让学生学习休谟对自然的理解，而非提升阅读能力；D) 将第 8 段 stick to the parameters of the assignment 曲解为 List the parameters first，stick to 意为「遵守、遵循」，而 list 意为「列出、列举」。",
    },
    9: {
        "prompt": "What did climate scientists describe as stunning?",
        "options": {
            "A": "The unprecedented high temperature in Greenland.",
            "B": "The collapse of ice on the northern tip of Greenland.",
            "C": "The unusual cold spell in the Arctic area in October.",
            "D": "The rapid change of Arctic temperature within a day.",
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。设题要点为事件引出处与观点引出处。第 2 段末说气候科学家认为 “the phenomenon” 令人震惊，而 the phenomenon 回指上文格陵兰岛两日出现的异常高温（2 月 20 日升至零度以上并持续 24 小时，2 月 24 日最北端达 6 摄氏度），A) 准确概括了这部分内容。因此答案为 A)。B) 利用 Greenland's northern tip 臆造，原文并未提到「冰盖坍塌」；C) 与首段「今年北极经历高温」相悖；D) 由时间信息 24 hours 与 temperature surge 糅杂得出，实际上文中明确说气温在零度以上保持了 24 小时，即一天之内温差不大。",
    },
    10: {
        "prompt": "What does the passage say about the temperature surge in the Arctic?",
        "options": {
            "A": "It has created a totally new climate pattern.",
            "B": "It will pose a serious threat to many species.",
            "C": "It typically appears about once every ten years.",
            "D": "It has puzzled the climate scientists for decades.",
        },
        "answer": "C",
        "explanation": "【精析】细节推断题。设题要点为新信息引出处。第 3 段说：“Weather conditions that drive this bizarre temperature surge have visited the Arctic before. They typically appear about once in a decade.”由此可合理推断「北极气温陡升大约每十年出现一次」，文中正以「异常高温过去每十年出现一次」与「如今仅隔两年便再次出现」的对比凸显极端天气出现频率激增。因此答案为 C)。A) 将「正在建立新的气候反馈环路」窜改为「已经创造出新的气候模式」；B) 源自末段 This raises unique challenges，但 This 承前指「数年持续变暖」，并非题干所关注的「此次气温陡升」；D) 利用 troubling 设置干扰，此处意在指出北极气温升高令人不安、后果严重，无关「气候学家的困惑」。",
    },
    11: {
        "prompt": "What may occur in 20 years according to scientists' recent observations?",
        "options": {
            "A": "Extinction of Arctic wildlife.",
            "B": "Iceless summers in the Arctic.",
            "C": "Emigration of indigenous people.",
            "D": "Better understanding of ecosystems.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为今昔对比处。末段说：“Previously, climate forecasts predicted that Arctic summer ice would disappear entirely by around 2060. But based on what scientists are seeing now, the Arctic may be facing summers without ice within 20 years.”与题干共同构成同义改写。因此答案为 B)。A)、C) 是对「这会给北极野生动植物和原住民带来不寻常挑战」的过度推断，「灭绝」「迁走」均夸大其词；D) 利用 Arctic ecosystems 干扰，此处意在指出当地生物与原住民的生存依赖北极生态系统，文中并未提及「更好的了解」。",
    },
    12: {
        "prompt": "What is often necessary for carrying through a task?",
        "options": {
            "A": "A good start.",
            "B": "A detailed plan.",
            "C": "A strong determination.",
            "D": "A scientific approach.",
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。设题要点为引入全文话题处。首段说：“A good dose of willpower is often necessary to see any task through, whether it's sticking to a spending plan or finishing a great novel.”a good dose of 比喻「剂量大、充足」，C) 的 strong determination 与之对应。因此答案为 C)。A)、D) 属常识干扰，原文并未提及「开端或方法」；B) 利用首段个别词汇 plan 干扰，原文实则以「坚持执行支出计划」例证「意志力对完成任何任务的重要性」，并非关注「详细计划」本身。",
    },
    13: {
        "prompt": "What is the finding of the new study?",
        "options": {
            "A": "Most people get energized after a sufficient rest.",
            "B": "Most people tend to have a finite source of energy.",
            "C": "It is vital to take breaks between demanding mental tasks.",
            "D": "It is most important to have confidence in one's willpower.",
        },
        "answer": "D",
        "explanation": "【精析】细节概括题。设题要点为介绍与重申研究发现处。首段说：“if you want to increase that willpower, a new study suggests, you just simply have to believe you have it.”what matters most 明确体现了条件关系，believe you have it 对应 have confidence in one's willpower，末段又重申了这一观点。因此答案为 D)。A) 将 breaks 与 get energized 糅杂，二者各指一方；B) 将「某些人认为自己的意志力有限」窜改为「关于大多数人的事实」；C) 利用 need breaks between demanding mental tasks 干扰，此处仅描述某些人的需求，并非强调休息的重要性。",
    },
    14: {
        "prompt": "What do we learn about European participants as compared with their American counterparts?",
        "options": {
            "A": "They could keep on working longer.",
            "B": "They could do more challenging tasks.",
            "C": "They found it easier to focus on work at hand.",
            "D": "They held more positive attitudes toward life.",
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。设题要点为对比处。第 3 段末对比：“Americans were more likely to admit to needing breaks after completing mentally challenging tasks. European participants, on the other hand, claimed they were able to keep going.”即美洲人往往需要休息，欧洲人则表示可以继续，A) 概括了这一对比。因此答案为 A)。B)、C) 分别利用 challenging、tasks 与 focus on 干扰，将对比点「完成高难度任务后能否继续」窜改为「能否完成高难度任务」或「能否专注」；D) 由末段 healthier、perceptions 臆测而来，该段与「欧洲参与者」并无直接关联。",
    },
    15: {
        "prompt": "What do the researchers say concerning people's feelings about willpower?",
        "options": {
            "A": "They are part of their nature.",
            "B": "They are subject to change.",
            "C": "They are related to culture.",
            "D": "They are beyond control.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为转折处。末段说：“Your feelings about your willpower affect the way you behave. But these feelings are changeable, they said.”指出对意志力的感受具有可变性，B) 与之同义改写。因此答案为 B)。A) 由末段个别词汇 nature 捏造，此处 nature 实指「自控力的本质」而非「人的天性」；C) 无中生有，原文并未提及文化因素；D) 源自 self-control 一词，但这里「自控力」即指「意志力」，并非指人们对意志力的感受超出个人控制。",
    },
    16: {
        "prompt": "What did the researchers at Oxford University conclude?",
        "options": {
            "A": "About half of current jobs might be automated.",
            "B": "The jobs of doctors and lawyers would be threatened.",
            "C": "The job market is becoming somewhat unpredictable.",
            "D": "Machine learning would prove disruptive by 2013.",
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。设题要点为研究结论说明处。第 2 段说：“They concluded that almost one in every two jobs has a high risk of being automated by machines.”A) 是其同义改写。因此答案为 A)。B) 源于首段 Sarah 的家庭信息「妈妈是医生、爸爸是律师」，但牛津大学的研究针对宏观就业市场；C) 将研究对象「未来的工作」偷换为「当今就业市场」；D) 杂糅了做研究的时间（2013 年）与「机器学习是造成动荡的主要原因」这一论述。",
    },
    17: {
        "prompt": "What do we learn about Kaggle company's winning programs?",
        "options": {
            "A": "They are widely applicable for massive open online courses.",
            "B": "They are now being used by numerous high school teachers.",
            "C": "They could read as many as 10,000 essays in a single minute.",
            "D": "They could grade high-school essays just like human teachers.",
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。设题要点为事件引出处。第 4 段说：“In 2012, Kaggle challenged its community to build a program that could grade high-school essays. The winning programs were able to match the grades given by human teachers.”「胜出程序的评分与人类教师相符」即能像人类教师那样给高中作文评分。因此答案为 D)。A) 利用 essays、teachers 等教学相关表述捏造「公开课」，原文并未提到；B) 由「程序可高效批阅高中作文」臆测得出，文中并未提及其在教学中的应用；C) 将「几分钟内上百万篇」窜改为「一分钟内上万篇」。",
    },
    18: {
        "prompt": "What is the fundamental limitation of machine learning?",
        "options": {
            "A": "It needs instructions throughout the process.",
            "B": "It does poorly on frequent, high-volume tasks.",
            "C": "It has to rely on huge amounts of previous data.",
            "D": "It is slow when it comes to tracking novel things.",
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。设题要点为重点信息引出处。末段说：“The fundamental limitation of machine learning is that it needs to learn from large volumes of past data.”C) 与之同义改写。因此答案为 C)。A) 将 progress 偷换为 process 捏造而来；B) 虽复现 frequent, high-volume tasks，但与文意「人类在这方面毫无胜算」相悖；D) 将「机器在应对新情况方面进展有限」偷换为「追踪新事物速度缓慢」。",
    },
    19: {
        "prompt": "What has the speaker previously talked about?",
        "options": {
            "A": "The engineering problems with solar power.",
            "B": "The generation of steam with the latest technology.",
            "C": "The importance of exploring new energy sources.",
            "D": "The theoretical aspects of sustainable energy.",
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。设题要点为关注点转移处与话题引入处。首段说：“We've talked recently about the importance of sustainable energy. We've also talked about the different theories on how that can be done. So far, our discussions have all been theoretical.”D) 高度概括了讲话人此前的谈论内容。因此答案为 D)。A) 将 a practical question 与 solar power 糅杂捏造出「太阳能的工程难题」；B) 为首段 the steam generated by solar power 及后文体现的信息，均属讲话人将要讨论的内容；C) 将「新能源的重要性」偷换为与之含义偏差巨大的「探索新能源的重要性」。",
    },
    20: {
        "prompt": "What is Tim Castleman trying to do in Sacramento?",
        "options": {
            "A": "Drive trains with solar energy.",
            "B": "Upgrade the city's train facilities.",
            "C": "Build a new ten-kilometre railway line.",
            "D": "Cut down the city's energy consumption.",
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。设题要点为设问处与人物具体行为描述处。首段设问 “Can you run a 140,000-kilogram train on just the steam generated by solar power?”，第二、三段描述卡斯尔曼正在开发「完全依靠太阳能产生的蒸汽来驱动火车」的技术，A) 正确体现了这一点。因此答案为 A)。B) 复现 upgrading，但将改造对象由「萨克拉门托市铁路场段」窜改为「火车设备」；C) 与 an existing 10-kilometer line「长 10 公里的铁路线是现存的」相悖；D) 源自 with the least amount of energy lost，但「削减能耗」并非卡斯尔曼直接致力于之事。",
    },
    21: {
        "prompt": "What has a Japanese research team tried to do?",
        "options": {
            "A": "Build a tank for keeping calcium oxide.",
            "B": "Find a new material for storing energy.",
            "C": "Recover super-heated steam.",
            "D": "Collect carbon dioxide gas.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为举例说明处。末段说：“Another team, at Nagoya University in Japan, has tested calcium compound as an energy storage material.”即测试钙化合物能否用作能量储存物质，B) 契合该研究内容。因此答案为 B)。A) 对 “drives off carbon dioxide gas, leaving calcium oxide. The gas can be stored...in a tank” 理解错误，储存在罐中的是二氧化碳气体而非氧化钙，且目的并非造罐子；C) 将「生成过热蒸汽」窜改为「回收过热蒸汽」；D) 将实验步骤之一「将二氧化碳气体储存在罐中」曲解为研究目的。",
    },
    22: {
        "prompt": "What is one cause of the current crisis in care for the elderly in England?",
        "options": {
            "A": "The lack of supervision by both the national and local governments.",
            "B": "The impact of the current economic crisis at home and abroad.",
            "C": "The poor management of day centres and home help services.",
            "D": "The poor relation between national health and social care services.",
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。设题要点为文章开头处兼引出原因处。首段说：“Today's crisis in care for older people in England has two main causes. First, people are living longer with a lot more complex needs. Second, they rely on a system that has long been marked by a poor relation between national health and social care services.”D) 复现第二个原因。因此答案为 D)。A) 糅杂 national、local government 与 supervise 捏造信息；B) 源自第 5 段 20 世纪 80 年代的 financial crisis，无关当今情形；C) 源自第 2 段 day centres and home helpers，但文中并未提及「对其管理不善」。",
    },
    23: {
        "prompt": "What does the speaker say about residential and community care?",
        "options": {
            "A": "It was mainly provided by voluntary services.",
            "B": "It mainly caters to the needs of the privileged.",
            "C": "It called for a sufficient number of volunteers.",
            "D": "It has deteriorated over the past sixty years.",
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。设题要点为转折处与具体介绍处。第 2 段末说：“No such vision guided residential and community care, though. The care was substantially provided by voluntary services...”A) 同义复现这一介绍。因此答案为 A)。B) 将 with eligibility based on income（按收入确定是否有资格获得服务）曲解为与之反向的「迎合特权阶层的需要」；C) 由服务提供机构「志愿服务机构」臆造出「需要大量志愿者」；D) 将末段问句「为何 60 年的批评带来的改变如此之少」夸大为「在过去 60 年变糟」。",
    },
    24: {
        "prompt": "What made management of care for the elderly more difficult in the 1980s?",
        "options": {
            "A": "Their longer lifespans.",
            "B": "Fewer home helpers available.",
            "C": "Their preference for private services.",
            "D": "More of them suffering serious illnesses.",
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。设题要点为原因介绍处。第 5 段说：“Meanwhile, preference for private over public services made management even more difficult.”C) 同义复现这一因果关系。因此答案为 C)。A) 利用文中多次提及的「人们寿命延长」干扰，但这无关 20 世纪 80 年代的情形；B) 由段末句 erosion of available aid 推出「可用家庭帮助者减少」，但该句是在指出政府阻止这一趋势的努力甚少，无关「管理困难」；D) 虽复现第 5 段「患病老年人增加」，但由 simultaneously 可知这与「管理困难」为并列关系，而非因果关系。",
    },
    25: {
        "prompt": "What does the speaker say about older people in England?",
        "options": {
            "A": "They are unable to pay for health services.",
            "B": "They have long been discriminated against.",
            "C": "They are vulnerable to illnesses and diseases.",
            "D": "They have contributed a great deal to society.",
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。设题要点为设问回答处。末段说：“Why has sixty years of criticism produced so little change? Discrimination against older people has a long history.”B) 与之同义复写。因此答案为 B)。A) 源自第 6 段 Unless you were prepared to pay，此句意在说明「老年医疗服务不足」，而非「老年人无力支付」；C) 利用 health、care、sick 结合常识干扰，原文并未提及老年人更易生病；D) 属常识干扰，原文并未提及老年人对社会的贡献。",
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
