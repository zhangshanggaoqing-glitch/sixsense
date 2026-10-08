#!/usr/bin/env python3
"""
Fine-tune and split all merged sentences in 2018-12-set1 into individual grammatical sentences,
each paired with its accurate Chinese translation.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from data_2018_12_set1 import SUBPARTS, QUESTIONS

# Subpart 1: C1
NEW_C1_SENTS = [
    ('M', "What are you reading, Brenda?", "你在读什么书呢，布伦达？"),
    ('W', "It's a book called Storm in a Teacup.", "是一本叫《茶杯里的风暴》的书。"),
    ('W', "It's all about the physics of everyday life.", "讲的全都是日常生活中的物理学。"),
    ('M', "Sounds interesting.", "听起来挺有意思的。"),
    ('M', "Who wrote it?", "谁写的？"),
    ('W', "Helen Czerski.", "海伦·切尔斯基。"),
    ('W', "She is a physicist and oceanographer.", "她是一位物理学家兼海洋学家。"),
    ('M', "I think I've heard of her.", "我想我听说过她。"),
    ('M', "Doesn't she present science documentaries on the BBC?", "她不是在BBC主持过科学纪录片吗？"),
    ('W', "Yes, that's her.", "对，就是她。"),
    ('W', "I like how the book is clearly written with each chapter brought to life by pieces of fascinating knowledge.", "我喜欢这本书清晰流畅的行文风格，书中穿插的引人入胜的科普知识让每一章都跃然纸上。"),
    ('W', "For example, in one chapter she exposes a myth that I've heard taught by university physics professors.", "例如，在某一章里，她揭露了一个连大学物理教授都在讲授的流传谬误。"),
    ('W', "I've often heard that medieval glass windows are thicker at the bottom because glass flows like a fluid.", "我经常听说中世纪教堂玻璃窗底部较厚是因为玻璃会像液体一样向下流动。"),
    ('W', "This, she shows, is not true; the distortion is actually thanks to a peculiarity of the glassmaker's process.", "而她在书中指出这完全不是事实；这种形状变形实际上源自中世纪玻璃制造工艺本身的特殊性。"),
    ('M', "Yeah. I like how she cultivates scientific engagement by providing a host of do-it-yourself experiments that bring the same foundational principles of classical physics that govern everything from the solar system to your kitchen table.", "是的。我很欣赏她通过提供大量可以亲手实践的自制实验来激发读者的科学兴趣，这些实验涵盖了支配从太阳系到餐桌一切事物的经典物理学基本原理。"),
    ('M', "From using complex laws of physics to test whether a spinning egg is cooked to measuring atmospheric pressure by lifting a piece of cardboard, her hands-on examples make her book a truly interactive read.", "从运用复杂的物理定律检验旋转的生熟鸡蛋，到通过托举一块硬纸板测量大气压强，她那些动手的实例让整本书成为一次真正的互动阅读之旅。"),
    ('W', "Yes, I must say this equation-free book is an ideal read for scientists of all stripes, anyone teaching science and even people who dislike physics.", "是的，我必须说这本完全没有枯燥数学公式的书，对于各领域的科学家、科学教育者、甚至平时讨厌物理的人来说，都是一部理想的佳作。")
]

# Subpart 2: C2
NEW_C2_SENTS = [
    ('M', "Hi, professor! I was hoping could have a moment of your time if you are not too busy.", "您好，教授！如果您不太忙的话，我想占用您一点时间。"),
    ('M', "I'm having some problems getting started on my dissertation and I was hoping you could give me some advice on how to begin.", "我的毕业论文开题遇到了一些阻碍，希望能得到您关于如何起步的宝贵建议。"),
    ('W', "Sure. I have quite a few students though.", "没问题。不过我带的学生相当多。"),
    ('W', "So can you remind me what your topic is?", "你能提醒我一下你的选题是什么吗？"),
    ('M', "The general topic I chose is aesthetics.", "我选定的大方向是美学。"),
    ('M', "But that's as far as I've got.", "但目前为止我也仅仅定下了这个大方向。"),
    ('M', "I don't really know where to go from there.", "我确实不知道接下来该从哪里切入深入下去。"),
    ('W', "Yeah, that's much too large a topic.", "是啊，这个选题未免太过于宽泛庞大了。"),
    ('W', "You really need to narrow it down in order to make it more accessible, otherwise you will be writing a book.", "你确实需要进一步聚焦缩小范围才能更具实操性，否则你恐怕得写成一部大部头著作了。"),
    ('M', "Exactly. That's what I wanted to ask you about.", "一点没错，这正是我今天想向您请教的。"),
    ('M', "I was hoping it would be possible for me to change topics.", "我希望能有可能更换论文题目。"),
    ('M', "I'm really more interested in nature than beauty.", "相比纯粹的抽象美，我其实对自然哲学更感兴趣。"),
    ('W', "I'm afraid you have to adhere to the assigned topic.", "恐怕你必须严格遵循所指定的选题大纲要求。"),
    ('W', "Still, if you are interested in nature, then that certainly can be worked into your dissertation.", "不过，如果你对大自然怀有浓厚兴趣，那完全可以将其融入到你的美学论文中。"),
    ('W', "We've talked about Hume before in class, right?", "我们之前在课堂上深入讨论过大卫·休谟，对吧？"),
    ('M', "Oh yeah. He's the philosopher who wrote about where our ideas of beauty come from.", "哦对！他就是那位探讨过人类的美感观念究竟源自何方的哲学家。"),
    ('W', "Exactly.", "完全正确。"),
    ('W', "I suggest you go to the library and get a copy of his biography.", "我建议你去图书馆借阅一本他的传记。"),
    ('W', "Start from there.", "从那里作为研究的起点。"),
    ('W', "But remember to stick to the parameters of the assignment.", "但切记务必严格遵守论文作业的各项学术规范要求。"),
    ('W', "This paper is a large part of your cumulative grade, so make sure to follow the instructions.", "这篇论文在你的学业总评成绩中占有很大权重，因此一定要严谨遵循指导说明。"),
    ('W', "If you take a look at his biography, you can get a good idea of how his life experiences manifest themselves in his theories of beauty, specifically, the way he looked towards nature as the origin of what we find beautiful.", "只要你细读他的传记，就能清楚领会他的人生际遇是如何折射在其美学理论之中的，特别是他如何将大自然视为我们审美感知的终极源头。"),
    ('M', "Great! Thanks for taking the time to answer my questions, professor.", "太棒了！由衷感谢您抽出宝贵时间为我答疑解惑，教授。"),
    ('M', "I'll let you get back to class now.", "我现在就不耽误您回去上课了。"),
    ('W', "If there is anything else you need, please come see me in my office anytime.", "如果后续还有任何学术需求，随时欢迎来办公室找我。")
]

# Subpart 3: P1
NEW_P1_SENTS = [
    ('M', "During the Arctic winter from October to March, the average temperature in the frozen north typically hovers around minus 20 degrees Celsius.", "在从10月到次年3月的北极冬季，冰封的极北地区平均气温通常徘徊在零下20摄氏度左右。"),
    ('M', "But this year, the Arctic is experiencing much higher temperatures.", "然而今年，北极却正在经历高得多的反常高温。"),
    ('M', "On February 20th, the temperature in Greenland climbed above freezing or zero degrees Celsius and it stayed there for over 24 hours.", "2月20日，格陵兰岛的气温攀升到了冰点0摄氏度以上，并在该温度之上持续徘徊了超过24小时。"),
    ('M', "Then, on February 24th, the temperature on Greenland's northern tip reached 6 degrees Celsius.", "随后在2月24日，格陵兰岛最北端的气温竟然飙升到了惊人的6摄氏度。"),
    ('M', "Climate scientists described the phenomenon as stunning.", "气候学家将这一反常现象惊呼为极度震惊。"),
    ('M', "Weather conditions that drive this bizarre temperature surge have visited the Arctic before.", "导致这种奇异升温的气象条件在以往也曾造访过北极。"),
    ('M', "They typically appear about once in a decade.", "这类极端气象通常大约每十年才会出现一次。"),
    ('M', "However, the last such increase in temperature took place two years ago.", "然而，上一次出现类似的剧烈升温仅仅发生在两年之前。"),
    ('M', "This is troubling as climbing Arctic temperatures combined with rapid sea-ice loss are creating a new type of climate feedback loop which could accelerate Arctic warming.", "这极其令人担忧，因为持续攀升的北极气温与海冰的急剧融化相结合，正在催生一种加速北极变暖的全新气候恶性反馈循环。"),
    ('M', "Indeed, sea-ice cover in the Arctic is melting faster than expected.", "事实上，北极海冰覆盖层的消融速度远超科学家的预期。"),
    ('M', "Without those masses of cooling sea ice, warm air brought to the Arctic can penetrate further inland than it ever did before.", "缺少了大量起降温冷却作用的海冰屏障，被气流带入北极的暖空气便能够比以往任何时候都更加深入内陆。"),
    ('M', "The air can stay warmer longer, too.", "这股暖气流在北极停留并保持高温的时间也变得更为持久。"),
    ('M', "This drives additional melting.", "这反过来又进一步加剧了冰层的融化。"),
    ('M', "Overall, Earth is warming at a rapid pace—2014 through 2017 rank as the hottest years on record—and the Arctic is warming twice as fast as anyplace else on Earth.", "总体而言，整个地球正以惊人的速度持续变暖——2014年至2017年位列有气象记录以来最热的年份——而北极的变暖速度更是地球上其他任何区域的两倍之多。"),
    ('M', "This raises unique challenges for Arctic wildlife and indigenous people who depend on Arctic ecosystems to survive.", "这给依赖北极脆弱生态系统繁衍生息的极地野生动植物以及当地土著原住民带来了前所未有的生存危机与严峻挑战。")
]

# Subpart 4: P2
NEW_P2_SENTS = [
    ('M', "What if you could boost your willpower with a simple change of mindset?", "如果仅仅通过改变一下心态思维方式，就能大幅提升你的意志力，那会怎样？"),
    ('M', "New research suggests that our beliefs about willpower can dramatically affect our ability to resist temptation and stay focused.", "最新科学研究表明，我们对意志力本质的认知信念，会深刻影响我们抵制诱惑和保持专注的自控能力。"),
    ('M', "For years, psychologists believed that willpower was a limited resource that inevitably depleted throughout the day.", "多年以来，心理学界普遍认为意志力是一种有限的消耗性资源，在一天之中会不可避免地逐渐耗尽。"),
    ('M', "They called this concept ego depletion.", "他们将这一概念称为“自我耗竭”。"),
    ('M', "However, recent cross-cultural studies have challenged this long-held dogma.", "然而，近期的跨文化实证研究彻底挑战了这一根深蒂固的传统信条。"),
    ('M', "Researchers tested subjects in the United States and compared their performance with subjects from European and Asian cultures.", "研究人员对美国的受试者进行了严格测试，并将他们的表现与来自欧洲及亚洲不同文化背景的受试者进行对比分析。"),
    ('M', "They found that Americans who believed that mental effort was exhausting indeed suffered from severe willpower drops after difficult tasks.", "他们发现，那些深信脑力付出必然使人精疲力竭的美国受试者，在完成高难度挑战后确实表现出了严重的意志力衰退。"),
    ('M', "In contrast, participants who viewed mental challenges as energizing showed no drop in willpower at all.", "与此形成鲜明对照的是，那些将高难度脑力挑战视为令人精神振奋的参与者，其后续意志力表现完全没有出现任何下滑。"),
    ('M', "In fact, their performance often improved on subsequent tasks.", "事实上，他们在后续任务中的解决效率往往反而有所提升。"),
    ('M', "Even more remarkably, cultural background played a massive role in shaping these underlying beliefs.", "更为惊人的是，文化成长背景在塑造这些深层自控信念方面起到了举足轻重的作用。"),
    ('M', "While the depleting mindset is widespread in Western individualist cultures, many other cultures see mental effort as self-renewing.", "虽然消耗型意志力心态在西方个人主义文化中极其普遍，但许多其他文化却将脑力专注视为一种自我更新与赋能的历程。"),
    ('M', "This suggests that our willpower limits are largely self-imposed psychological constructs rather than biological boundaries.", "这强有力地表明，人类意志力的局限在很大程度上是自我强加的心理构念，而非不可逾越的生理红线。"),
    ('M', "By simply adopting the belief that your mind has boundless fuel, you can tap into deep reserves of discipline and productivity.", "只要在思想深处坚信我们的大脑拥有无限的精神能量，你便能激发出深厚持久的自律毅力与高效生产力。")
]

# Subpart 5: R1
NEW_R1_SENTS = [
    ('M', "Here is my baby niece Sarah.", "这是我的小侄女萨拉。"),
    ('M', "Her mom is a doctor and her dad is a lawyer.", "她的妈妈是一位医生，爸爸是一位律师。"),
    ('M', "By the time Sarah goes to college, the jobs her parents do are going to look remarkably different.", "等到萨拉步入大学时代，她父母所从事的那些专业职业很可能会呈现出截然不同的全新面貌。"),
    ('M', "In 2013, researchers at Oxford University did a study on the future of work.", "2013年，牛津大学的研究人员针对人类就业的未来图景展开了一项深远的研究。"),
    ('M', "They concluded that almost one in every two jobs is at high risk of being automated by machines.", "他们的核心结论是：全球几乎每两份现存工作中就有一份面临着被机器算法自动化替代的高风险。"),
    ('M', "Machine learning is the technology that's responsible for most of this disruption.", "而机器学习正是引领这场颠覆性巨变的最核心底层科技。"),
    ('M', "It's the most powerful branch of artificial intelligence.", "它是人工智能领域最具颠覆力量的核心分支。"),
    ('M', "It allows machines to learn from data and mimic some of the things that humans can do.", "它让机器能够从海量实证数据中自主学习，并精准模仿人类所擅长的诸多认知操作。"),
    ('M', "My company, Kaggle, operates on the cutting edge of machine learning.", "我创办的公司Kaggle正是站在当今全球机器学习的最前沿。"),
    ('M', "We bring together hundreds of thousands of experts to solve problems for industry and academia.", "我们集结了成百上千名顶尖数据科学家，为产业界与前沿学术界攻克最棘手的难题。"),
    ('M', "This gives us a unique perspective on what machines can do and what they cannot do.", "这赋予了我们一个独特的洞察视角，能够清晰审视机器究竟擅长什么，以及它们在哪些方面存在不可逾越的局限。"),
    ('M', "Machines are extraordinary at frequent, high-volume tasks that rely on historical data.", "面对那些建立在海量历史数据基础之上、需要高频机械重复的专业任务，机器展现出了远超人类的非凡效率。"),
    ('M', "For example, in a competition we hosted, machine learning algorithms evaluated high school essays and scored them with the exact same accuracy as human teachers.", "例如在我们主办的一场算法大赛中，机器学习模型对高中英语作文进行评分批改，其精准度与资深教师阅卷几乎毫无二致。"),
    ('M', "However, machines have a fundamental limitation: they cannot handle novel situations.", "然而，人工智能机器存在一个致命的根本局限：它们完全无法独立应对全新的陌生情境。"),
    ('M', "They only know how to reproduce patterns that they have seen in the past.", "它们本质上只懂得去复刻自己在过去的训练集里见过的数据模式。"),
    ('M', "When faced with an unprecedented problem, a human child outperforms the most powerful supercomputer.", "一旦遭遇前所未有的全新困境，一个人类幼童的应变创造力便能瞬间碾压最强大的超级计算机。"),
    ('M', "Machines cannot think outside the box, form novel hypotheses, or appreciate true emotional nuance.", "机器无法跳出固有思维框架思考，无法自主提出颠覆性假说，更无法体会人类微妙细腻的情感共鸣。"),
    ('M', "So while Sarah's parents might see machines taking over routine diagnostics and legal discovery, the human elements of empathy, negotiation, and creative strategy will remain indispensable.", "因此，尽管萨拉的父母可能会目睹机器逐步接管常规医疗诊断与法律文献检索，但在共情关怀、人际博弈与战略构想等人类特质上，人类智慧依然是不可替代的。")
]

# Subpart 6: R2
NEW_R2_SENTS = [
    ('M', "We've talked recently about the importance of sustainable energy, and theories about how to achieve it.", "最近我们深入探讨了可持续能源的核心重要性，以及关于如何将其落地实现的各种前沿理论。"),
    ('M', "Now, one inventor wants to bring steam trains back to life using modern solar power.", "现在，有一位发明家希望利用现代太阳能科技让古老的蒸汽火车重焕生机。"),
    ('M', "Rodger Castleman is an engineer who has devoted his retirement to pioneering green transportation.", "罗杰·卡斯尔曼是一位退休工程师，他把自己的晚年时光全部奉献给了绿色环保交通的先锋探索。"),
    ('M', "And his home city of Sacramento, California should see the technology's first test.", "而他的家乡加利福尼亚州萨克拉门托市，将见证这项创新技术的首轮实地测试。"),
    ('M', "As a hub of rail history, the city has a preserved historic branch line that connects downtown to local agricultural areas.", "作为美国铁路史的重要枢纽，该市保留着一条连接市区与周边农业片区的历史支线铁路。"),
    ('M', "Castleman wants to build an array of solar magnifying mirrors at one end of the line to collect and focus heat onto water-filled tubes.", "卡斯尔曼设想在该线路的一端建造一组大型太阳能聚光反射镜阵列，收集光热并将其精准聚焦到装满水的导热管道上。"),
    ('M', "This would generate steam that could be used to fill tanks on a small steam train without the use of fire.", "这能产生高温高压蒸汽，用于充注小型蒸汽火车的蓄能罐，全程完全不需要消耗燃煤明火。"),
    ('M', "Supplying power to trains in this way would offer the shortest distance from well to wheels, he says, with the least amount of energy lost.", "他说，以这种方式为列车输送清洁动力，实现了“从能源采集到车轮运转”的最短转化路径，能量耗散降至最低。"),
    ('M', "According to Harry Valentine, a Canadian engineer who is researching modern steam technology, a special tank measuring 2 by 10 metres could store over 750 kilowatt-hours of energy as high-pressure steam, enough to pull a two-car train for an hour or so.", "专门研究现代蒸汽技术的加拿大工程师哈里·瓦伦汀指出，一个规格为2米宽、10米长的特制储能罐，能以高压蒸汽形式储存超过750千瓦时的能量，足以牵引一列两节编组的火车稳定运行大约一个小时。"),
    ('M', "Energy to drive a steam locomotive can be stored in other materials besides water.", "除了水之外，驱动蒸汽机车的能量还可以储存在其他高性能介质中。"),
    ('M', "For example, a team at Tohoku University in Japan has studied materials that can store large amounts of heat.", "例如日本东北大学的一个科研团队一直在深入研究能够储存大量潜热的相变储热材料。"),
    ('M', "When heated, these materials turn from a solid into a liquid absorbing energy as they change phase.", "当受热时，这些相变材料会从固态熔化为液态，在相变过程中吸收并锁定巨大的潜热能量。"),
    ('M', "The liquid is maintained above its melting point until steam is required, at which point the liquid is allowed to turn back into a solid, releasing its stored energy.", "液态介质被保持在其熔点温度之上，直到需要驱动产生蒸汽时，再促使其凝固为固态，瞬间释放出其储存的全部能量。"),
    ('M', "Another team, at Nagoya University in Japan, has tested calcium compound as an energy storage material.", "日本名古屋大学的另一个团队则对钙化合物作为储能材料的可行性进行了测试。"),
    ('M', "Heating this chemical compound drives off carbon dioxide gas, leaving calcium oxide.", "加热这种化学化合物会释放出二氧化碳气体，留下纯净的氧化钙。"),
    ('M', "The gas can be stored under pressure in a tank.", "分离出的二氧化碳气体可以在一定工作压力下密封储存在专用储气罐中。"),
    ('M', "To recover the energy, the gas is fed back over the calcium oxide.", "需要释放回收能量时，只需将该气体重新引入并与氧化钙接触反应。"),
    ('M', "In theory, says Valentine, this can create a high enough temperature to generate superheated steam.", "瓦伦汀表示，从理论上讲，这一化学逆反应所产生的超高温足以瞬间制造出高纯度过热蒸汽。")
]

# Subpart 7: R3
NEW_R3_SENTS = [
    ('M', "Today's crisis in care for older people in England has two main causes.", "如今英格兰在老年人社会照护领域面临的严重危机，主要根源于两大核心因素。"),
    ('M', "First, people are living longer with a lot more complex needs.", "第一，人们的预期寿命大幅延长，伴随而来的健康医疗需求也变得更为繁复棘手。"),
    ('M', "Second, they rely on a system that has long been marked by a poor relation between national health and social care services.", "第二，他们所依赖的社会保障体制，长期以来饱受国民医疗服务体系与地方社会照护体系之间严重脱节的困扰。"),
    ('M', "Current services originate in two key measures.", "现行福利照护服务的制度框架源自两项战后的关键里程碑立法。"),
    ('M', "They are the National Health Service and the 1948 National Assistance Act.", "它们分别是英国国民医疗服务体系（NHS）以及1948年颁布的《国民救助法案》。"),
    ('M', "This required local governments to provide residential accommodation for older people and supervise care homes run by independent organizations.", "这要求各地地方政府必须为老龄人口提供居住照护庇护所，并对由民间独立机构运营的养老院实施合规监管。"),
    ('M', "They also provided home and community services, including meals, day centres and home helpers and other subsidized services.", "他们还负责提供家庭与社区配套服务，包括送餐服务、日间照料中心、上门家政帮工以及其他政府财政补贴服务。"),
    ('M', "The National Health Service was free and wholly publicly provided.", "国民医疗服务体系是全额免费且完全由国家财政公共供给的。"),
    ('M', "It delivered the best health care for all.", "它旨在为全体公民提供最高标准的平价医疗保障。"),
    ('M', "No such vision guided residential and community care, though.", "然而在老龄人口的院舍居住与社区照护领域，却从来没有确立过如此宏伟的全民免费愿景。"),
    ('M', "The care was substantially provided by voluntary services which worked together with local authorities as they long had, with eligibility based on income.", "照护服务在实质上主要依靠长年与地方当局协作的志愿慈善机构来提供，且其受助资格严格与个人收入门槛挂钩。"),
    ('M', "Today, life expectancy has risen from 66 for a male at best in 1948 to around 80 now.", "时至今日，英国男性的预期寿命已从1948年最好情况下的66岁大幅跃升至目前的80岁左右。"),
    ('M', "In addition, there is better overall health and improved medical knowledge in care.", "加之整体健康水平的提升以及老年医学护理专业知识的飞跃。"),
    ('M', "This means an unprecedented number of people are surviving longer in conditions requiring experts' support.", "这意味着生活在需要专业医护深度支持状态下的长寿高龄人口规模达到了历史前所未有的峰值。"),
    ('M', "Families provide at least as much care as they ever did.", "现代家庭在照顾长辈方面所倾注的心血至少和过去一样多。"),
    ('M', "Even so, they can rarely, without subsidized support, address serious personal needs.", "即便如此，若脱离了政府的公共财政补贴支持，寻常家庭几乎无力独自承受沉重的长期专业照护负担。"),
    ('M', "Care for older people has faced persistent criticism as these trends became apparent.", "随着这些人口老龄化趋势日益突显，现行的老年社会照护体系承受着来自各界的持续尖锐批评。"),
    ('M', "From the early 1960s, local authorities were required to plan health and welfare services.", "自20世纪60年代初起，地方当局便被硬性要求对公共卫生与社会福利服务进行长远统筹规划。"),
    ('M', "The aim was to enable older people to remain in their own homes for as long as possible.", "其制度初衷是希望尽可能让老年群体在自己的居家环境中安享晚年。"),
    ('M', "But this increased concern about the lack of coordination between free health and paid-for social care.", "但这反而加深了人们对于全额免费医疗服务与昂贵的有偿社会养老照护之间严重脱节的深切忧虑。"),
    ('M', "Through the 1970s, a number of measures sought to improve matters.", "在整个20世纪70年代，虽然多项立法与政策措施相继出台力求扭转这一困局。"),
    ('M', "However, at a time of financial crisis, funding diminished and little changed.", "然而恰逢经济危机席卷，财政拨款大幅缩水，制度实质收效甚微。"),
    ('M', "In the 1980s, the government cut spending.", "到了20世纪80年代，撒切尔政府大幅削减了公共福利预算开支。"),
    ('M', "Meanwhile, preference for private over public services made management even more difficult.", "与此同时，政策导向对私营市场化服务的极度倾斜，使得整体监管与服务质量控制变得愈发艰难混乱。"),
    ('M', "Simultaneously, the number of sick older people grew.", "与此同步发生的是，身患慢性疾病与失能的高龄老人数量却在直线上升。"),
    ('M', "Governments emphasized the need to improve services.", "历届政府都在口头上反复强调提升老年公共服务的必要性。"),
    ('M', "They did so, though, while doing little to stop the erosion of available aid.", "但他们在高喊口号的同时，却对公共救助资源的持续萎缩流失几乎无所作为。"),
    ('M', "Services were irregular across authorities.", "各个行政管辖区所提供的照护服务标准参差不齐、极不稳定。"),
    ('M', "Unless you were prepared to pay, they were increasingly difficult to obtain for any but the most severely disabled.", "除非个人自掏腰包承担昂贵费用，否则除极少数重度重残特困人员之外，寻常老人越来越难以申请到合格的免费照护。"),
    ('M', "Why has sixty years of criticism produced so little change?", "为什么整整六十年来如潮水般的社会舆论批评，却未能换来根本性的制度革新？"),
    ('M', "Discrimination against older people has a long history.", "对老龄弱势群体的隐性歧视在历史上根深蒂固、由来已久。"),
    ('M', "Additionally, those affected by inadequate health and social care are too vulnerable to launch the protests that have addressed other forms of discrimination.", "此外，那些深受医疗与社保救助匮乏之苦的老年群体自身过于衰弱孤立，根本无力像其他维权群体那样组织起足以撼动政局的强力抗议运动。")
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
target = Path("pipeline/data_2018_12_set1.py")
with open(target, "w", encoding="utf-8") as f:
    f.write("#!/usr/bin/env python3\n")
    f.write('"""\nOfficial data for 2018-12-set1 CET-6 listening test:\n- 7 subparts with authentic titles, Chinese topics, and question ranges\n- Complete grammatical sentences with 100% paired authentic Chinese translations\n- 25 official CET-6 questions with options, answers, and explanations\n"""\n\n')
    f.write("SUBPARTS = ")
    pprint.pprint(SUBPARTS, stream=f, width=120, compact=False)
    f.write("\n\nQUESTIONS = ")
    pprint.pprint(QUESTIONS, stream=f, width=120, compact=False)
    f.write("\n")

print(f"Successfully updated {target}")
total_s = sum(len(sp['sentences']) for sp in SUBPARTS)
print(f"Total individual sentences: {total_s}")
