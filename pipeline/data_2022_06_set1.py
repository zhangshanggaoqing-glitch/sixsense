import json

SUBPARTS = [
    {
        "id": "2022-06-set1-conv-1",
        "subpart_code": "conv-1",
        "section_id": "2022-06-set1-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 1 · 纽约客撰稿人的家庭育儿与青少年阅读引导",
        "topic_zh": "纽约客撰稿人的家庭育儿与青少年阅读引导",
        "question_range": "Q1 ~ Q4",
        "questions": [1, 2, 3, 4],
        "sp_start": 55.0,
        "sp_end": 194.0,
        "sentences": [
            ("W", "Mr. David Jackson, a staff writer at The New Yorker, is known for his non-fiction books of adventure.", "大卫·杰克逊先生是《纽约客》杂志的专职撰稿人，以其纪实冒险类图书闻名。"),
            ("W", "Today we go on a different kind of adventure: Jackson's life of parenting his offspring.", "今天我们将开启一段别样的冒险之旅：杰克逊抚育自己子女的家庭生活。"),
            ("W", "David, as a parent of an 11- and a 14-year-old, what is the most interesting issue you are dealing with right now?", "大卫，作为分别处于11岁和14岁两个孩子的父亲，你目前正在应对的最有趣的问题是什么？"),
            ("M", "It's easy to focus on the challenges, but so far I find these ages to be kind of wonderful.", "人们往往容易只盯着育儿挑战，但到目前为止，我觉得孩子们处于这个年龄段其实挺美好的。"),
            ("M", "They are independent and they have their own curiosities and obsessions.", "他们很有主见、独立自主，拥有属于自己的好奇心和痴迷的爱好。"),
            ("M", "You can talk to them about fairly sophisticated subject matter such as politics.", "你可以和他们畅谈相当有深度的话题，比如政治问题。"),
            ("W", "Yes, that does sound refreshing compared with talking to younger children.", "确实，比起跟更小的幼童说话，这听起来让人耳目一新。"),
            ("W", "Do they ask you to proofread their essays?", "他们会请你帮他们校对作文吗？"),
            ("M", "Certainly, with writing they do.", "当然，在写作方面他们确实会这样请教。"),
            ("M", "I really just try to be encouraging.", "我其实主要是尽可能给予他们鼓励。"),
            ("M", "I think at this age editorial guidance is less important than encouragement.", "我认为在孩子这个年龄，编辑方面的指导远不如肯定与鼓励来得重要。"),
            ("W", "Are there books that you think are important that your children read and that all children read?", "有没有哪些书籍是你认为对你自己的孩子乃至所有孩子都必读的重要读物？")
            ,
            ("M", "My general thought is to read widely and to incorporate a love for reading.", "我总体上的想法是博览群书，并在过程中培养对阅读的热爱。"),
            ("M", "Learning to love to read I think is the optimal thing because it gives you a skill you can take anywhere.", "我认为学会爱上阅读是最理想的事情，因为它赋予了你一项可以受用一生的技能。"),
            ("W", "So you're not too concerned like some parents with the content they're reading?", "这么说来，你并不像某些家长那样过分担忧他们阅读的具体内容？"),
            ("W", "I know I have some worries about that.", "我知道我在这方面多少是有些顾虑的。"),
            ("M", "Yeah, read what you like.", "是啊，喜欢什么就读什么。"),
            ("M", "If a child loves graphic novels or comic books, whatever it is that is turning them on to read and turning on their imagination.", "如果一个孩子喜欢绘本小说或漫画书，不管是什么形式，只要能激发他们阅读的兴趣并放飞想象力就行。"),
            ("W", "I feel that children's tastes in books change as they reach adolescence.", "我感觉孩子们到了青春期，对书籍的品位往往会发生变化。"),
            ("W", "I know that mine certainly did when I was a teenager.", "我知道自己在少年时代就确实经历过这种转变。"),
            ("W", "What do you think?", "你怎么看？"),
            ("M", "I think it's especially important as they get older to read subject matter that will open their eyes to the world and people.", "我认为随着年龄增长，阅读那些能开阔眼界、帮助他们了解世界与形形色色人们的题材尤为关键。"),
            ("M", "So I think both fiction and nonfiction are really important because they give you the power to begin to perceive the world through the lives of others.", "因此我认为虚构小说与非虚构作品都极为重要，因为它们赋予了你通过他人的生活体验来感知世界的洞察力。")
        ]
    },
    {
        "id": "2022-06-set1-conv-2",
        "subpart_code": "conv-2",
        "section_id": "2022-06-set1-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 2 · 大学女生创立大码服饰电商品牌与创业历程",
        "topic_zh": "大学女生创立大码服饰电商品牌与创业历程",
        "question_range": "Q5 ~ Q8",
        "questions": [5, 6, 7, 8],
        "sp_start": 280.0,
        "sp_end": 416.0,
        "sentences": [
            ("M", "In this episode of Money Talks, our guest is Molly Sanders, a university student and a successful young entrepreneur.", "在这一期《金钱对话》节目中，我们的嘉宾是莫莉·桑德斯，她既是一名在校大学生，也是一位成功的青年创业家。"),
            ("M", "Molly, tell us about your business.", "莫莉，跟我们聊聊你的创业事业吧。"),
            ("W", "Well, I sell specialty clothes through a website, mainly for women who have trouble finding suitable clothes in main street shops because of their height or weight.", "嗯，我通过一个网站销售定制服装，主要面向那些因为身高或体重而在商业街普通商店里买不到合适衣服的女性。"),
            ("W", "But I do some men's clothes too.", "不过我也做一些男装。"),
            ("M", "How did you get started in this business at such a young age?", "你在如此年轻的时候是怎么涉足这个行业的？"),
            ("M", "Are you studying fashion design?", "你是在大学攻读服装设计专业吗？"),
            ("W", "Actually, I'm majoring in finance, but I've always loved clothes and I started making my own at 14.", "其实我主修的是金融学，但我一直对服装情有独钟，从14岁起我就开始自己动手做衣服了。"),
            ("M", "Did you have any sort of training in design or sewing or was it a natural ability?", "你接受过设计或缝纫方面的专业训练吗，还是说这纯粹是天赋使然？"),
            ("W", "I'd have to say no to both.", "两者都不是。"),
            ("W", "No one taught me to make clothes and most of the things I made at first were disasters.", "没人教过我怎么做衣服，我刚开始做出来的大多是不堪入目的失败品。"),
            ("M", "Why did you persevere?", "那你是如何坚持下来的呢？"),
            ("M", "I think most people would give up if they kept failing, especially at that age.", "我想大多数人如果屡屡受挫都会选择放弃，尤其是处于那个年纪的孩子。"),
            ("W", "I kept on out of necessity.", "我坚持做下去是出于迫不得已的现实需求。"),
            ("W", "As you can see, I'm very tall and I couldn't find clothes that fit me in ordinary shops.", "如你所见，我个子非常高，在普通服装店里根本买不到适合我身形的衣服。"),
            ("W", "So I kept trying and developed my skills over time.", "因此我不断尝试摸索，随着时间推移逐渐磨练提升了手艺。"),
            ("M", "Well, my notes say you earned $50,000 in profits last year, an extraordinary amount for a 20-year-old student.", "嗯，我的资料显示你去年赚了5万美元的净利润，这对一名20岁的在校大学生来说堪称惊人的数字。"),
            ("M", "How did that happen?", "这是如何实现的呢？"),
            ("M", "Did you see a gap in the market and decide to fill it?", "你是敏锐发现了市场空白并决定填补它吗？"),
            ("W", "No.", "并不是。"),
            ("W", "When I started university, some classmates complimented my clothes.", "当我刚上大学时，有些同学夸赞我的着装好看。"),
            ("W", "And when I said I made them myself, other tall women started asking if I would make theirs.", "当我说是自己亲手缝制的时候，其他高个子女生便开始询问我能否帮她们也做几套。"),
            ("W", "And I did.", "于是我就帮她们做了。"),
            ("W", "And before I knew it, I was an entrepreneur.", "不知不觉中，我就成了一名创业者。"),
            ("M", "So what are your plans for the future?", "那么你对未来有什么规划呢？"),
            ("M", "Do you intend to open a physical store?", "你打算开一家实体专卖店吗？"),
            ("W", "No, I'll keep things online to keep costs down.", "不，我会继续保持纯线上运营以控制成本。"),
            ("W", "But I will add more clothes for children, both girls and boys, and possibly even for infants.", "但我会增加更多童装线，涵盖男童和女童装，甚至可能还会做一些婴儿服饰。"),
            ("W", "And I hope to add to my range of designs for men.", "同时我也希望能拓展我的男士服装设计品类。")
        ]
    },
    {
        "id": "2022-06-set1-pass-1",
        "subpart_code": "pass-1",
        "section_id": "2022-06-set1-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 1 · 人工智能赋能新型抗生素分子发现",
        "topic_zh": "人工智能赋能新型抗生素分子发现",
        "question_range": "Q9 ~ Q11",
        "questions": [9, 10, 11],
        "sp_start": 528.0,
        "sp_end": 660.0,
        "sentences": [
            ("M", "Researchers have identified a potent new antibiotic compound using artificial intelligence.", "研究人员借助人工智能技术发现了一种强效的新型抗生素化合物。"),
            ("M", "The antibiotic can kill very dangerous bacteria.", "这种抗生素能够杀死极其危险的致病细菌。"),
            ("M", "According to a study published in the journal Cell, the compound successfully removed deadly strains of bacteria in mice which are resistant to all known antibiotics.", "根据发表在《细胞》期刊上的一项研究，该化合物成功清除了小鼠体内对所有已知抗生素均具有耐药性的致命菌株。"),
            ("M", "The researchers say this is the first time that artificial intelligence has been used to find a powerful new antibiotic molecule.", "研究人员表示，这是历史上首次将人工智能技术用于发现强效的新型抗生素分子。"),
            ("M", "Why does this matter?", "为什么这项成果至关重要？"),
            ("M", "The answer is antibiotic resistance.", "答案在于抗生素耐药性问题。"),
            ("M", "This happens when bacteria develop the ability to survive the medications designed to kill them.", "当细菌进化出在旨在消灭它们的药物中存活下来的能力时，耐药性便产生了。"),
            ("M", "Antibiotic resistance is a serious threat to health and the problem is growing.", "抗生素耐药性对人类健康构成了严重威胁，而且这一问题正在日益加剧。"),
            ("M", "This makes finding new antibiotics very important.", "这就使得寻找新型抗生素变得尤为紧迫和关键。"),
            ("M", "However, in recent decades, very few have been developed, and those that have tend to be very similar to drugs already available.", "然而近几十年来，新研发出的抗生素寥寥无几，而且即便有，也往往与现有上市药物非常相似。"),
            ("M", "These searches also tend to only focus on a narrow spectrum of chemical compounds.", "以往的研究搜索往往也只局限于极其狭窄的化学化合物谱系之中。"),
            ("M", "But this is where artificial intelligence comes in.", "但这正是人工智能大显身手之处。"),
            ("M", "Why?", "为什么呢？"),
            ("M", "To find new drugs, scientists screen molecules to predict how effective they might be.", "为了寻找新药，科学家需要筛选海量分子以预测其潜在药效。"),
            ("M", "Typically, such screening is done by humans in the lab, which is both costly and slow.", "通常情况下，这种筛选是由实验室里的科研人员手动完成的，既耗资昂贵又进展缓慢。"),
            ("M", "Artificial intelligence is different.", "而人工智能则截然不同。"),
            ("M", "It's fast, and it can process a high volume.", "它运算飞速，而且能够吞吐海量数据。"),
            ("M", "It can screen hundreds of millions of compounds to identify a few interesting candidates that require experimental testing.", "它能在数以亿计的化合物中进行深度筛选，精准找出少数几个需要开展实验验证的有潜力的候选分子。"),
            ("M", "Artificial intelligence is also able to predict if compounds are likely to be toxic.", "人工智能还能够提前预测化合物是否可能具有人体毒性。"),
            ("M", "Some experts assert that this work signifies a paradigm shift in antibiotic discovery.", "部分专家断言，这项工作标志着抗生素药物发现领域的一次根本性范式转变。"),
            ("M", "It could change drug discovery more generally.", "从更广阔的视角来看，它可能会彻底改变整个新药研发的格局。")
        ]
    },
    {
        "id": "2022-06-set1-pass-2",
        "subpart_code": "pass-2",
        "section_id": "2022-06-set1-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 2 · 人类谎言辨别认知误区与听觉线索科学实证",
        "topic_zh": "人类谎言辨别认知误区与听觉线索科学实证",
        "question_range": "Q12 ~ Q15",
        "questions": [12, 13, 14, 15],
        "sp_start": 725.0,
        "sp_end": 848.0,
        "sentences": [
            ("W", "A recent study overturned what we think we know about lying.", "最近的一项研究彻底颠覆了我们自以为对说谎行为的认知。")
            ,
            ("W", "Most of us have a theory about how to tell if someone is telling a lie.", "我们大多数人心里都有一套如何判断某人是否在撒谎的理论。"),
            ("W", "We may develop that theory from observations of those people we know well and see regularly.", "我们或许是通过观察那些我们熟悉且经常碰面的人逐渐总结出这套理论的。"),
            ("W", "But we tend to generalize what we gather from that unscientific daily research and make it a universal theory.", "但我们往往会把从日常不严谨的生活观察中收集到的经验加以推论，将其奉为普适真理。"),
            ("W", "So, we might imagine that liars have evasive eyes, or the opposite: they simply stare at you.", "因此，我们可能会想当然地认为说谎者眼神游离躲闪，或者恰恰相反：他们会直勾勾地盯着你。"),
            ("W", "Or perhaps it is more generally nervous behavior we associate with lies.", "或者更普遍地，我们会把紧张局促的举止与谎言联系在一起。"),
            ("W", "Whatever the particular theory, it's usually based on close observation of people we know.", "不论具体理论为何，它通常都建立在对自己熟人的近距离观察之上。"),
            ("W", "And we get lots of practice.", "而且我们在生活中有着大量的实操经历。"),
            ("W", "On average, we're lied to some 200 times per day.", "平均而言，我们每天大约会被欺骗200次。"),
            ("W", "These are mostly harmless lies, but lies nonetheless.", "这些大多是无伤大雅的善意谎言，但无论如何它们终归是谎言。"),
            ("W", "But there's a problem with our theories, even though they're based on all this observation.", "然而尽管我们的理论建立在如此丰富的观察之上，它们却存在着致命漏洞。"),
            ("W", "The average person, you and me, tested rigorously on how well we detect lies, fails to do better than chance.", "如果对你我这样的普通人进行严谨的谎言识别能力测试，我们的准确率其实并不比随机猜测好多少。"),
            ("W", "That's well established over many studies and lots of attempts by researchers to work out reliable ways to detect lies.", "在诸多科学研究以及学者们为寻找可靠测谎方法所做的大量尝试中，这一结论已得到充分证实。"),
            ("W", "It's even relatively easy to fool lie detectors: the gold standard of lie detection by training yourself in breathing techniques and symptom suppression.", "甚至连被誉为测谎‘黄金标准’的多导测谎仪，也可以通过训练呼吸技巧和抑制生理反应而被相对轻易地蒙混过关。"),
            ("W", "Is there any way to get better at detecting lies?", "那么，到底有没有办法能够提高测谎能力呢？"),
            ("W", "The new research offers some surprising advice: stop looking and listen instead.", "这项新研究给出了一个出人意料的建议：别用眼睛看，改用耳朵听。"),
            ("W", "It turns out that if we're unable to see the face, but rather focus on the voice of the person in question, our accuracy rate improves considerably.", "事实证明，如果我们遮住视线看不到当事人的面孔，而是把注意力完全集中在其声音上，我们的测谎准确率反而会显著提升。")
        ]
    },
    {
        "id": "2022-06-set1-rec-1",
        "subpart_code": "rec-1",
        "section_id": "2022-06-set1-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 1 · 美国医疗体系就医体验反思与病患防权建议",
        "topic_zh": "美国医疗体系就医体验反思与病患防权建议",
        "question_range": "Q16 ~ Q18",
        "questions": [16, 17, 18],
        "sp_start": 967.0,
        "sp_end": 1144.0,
        "sentences": [
            ("W", "Appear to be submissive, humble, grateful and undemanding.", "表现得顺从、谦卑、感恩戴德且不提任何要求。"),
            ("W", "Show great pleasure when a doctor comes into your room, even if the visit is brief and useless.", "即便医生的查房既仓促又毫无实质帮助，也要在他走进病房时展现出极大的欣喜之情。"),
            ("W", "Don't challenge anyone with authority unless you're famous or very rich.", "除非你是名人或巨富，否则切勿对任何权威人士提出质疑。"),
            ("W", "Those are a few strategies for dealing with today's American medical establishment.", "这些就是当下应对美国医疗体制的几条自保策略。"),
            ("W", "What patients want is to be treated with respect and consideration.", "患者内心真正渴望的是得到应有的尊重与体谅关怀。"),
            ("W", "But in my experience, too few hospitals and doctors are ready to do that.", "但依我的亲身经历来看，极少有医院和医生做好了这样对待患者的准备。"),
            ("W", "In his book, A Whole New Life, novelist Reynolds Price recalls that his doctors chose a crowded hallway as the place to tell him he might have a tumor on his spinal cord.", "小说家雷诺兹·普莱斯在其著作《全新生活》中回忆道，他的医生竟然选择在拥挤不堪的走廊里告诉他脊髓上可能长了肿瘤。"),
            ("W", "It did not occur to the two physicians that a hallway was not the most appropriate place for that particular piece of news.", "这两位主治医生压根就没意识到，走廊绝非传达如此重大噩耗的合适场合。"),
            ("W", "My surgeon, who is in his mid-30s, looks tired.", "我的主刀医生三十五六岁光景，看上去疲惫不堪。"),
            ("W", "He has been overwhelmed with patients who have fallen on the winter ice.", "他被那些在冬日结冰路面上摔伤的骨折病患折腾得焦头烂额。"),
            ("W", "He is a witty man, but sometimes his wit is unwelcome.", "他是个风趣幽默的人，但有时他的幽默却极其不合时宜。"),
            ("W", "'The health insurance company Blue Cross wants me to put you out in the snow tomorrow afternoon,' he tells me after I have been in the hospital for more than a week.", "在我住院一周多之后，他竟然对我说：‘蓝十字医保公司希望我明天下午就把你扔到雪地里出院。’"),
            ("W", "I'm terrified because I have no idea where to go.", "我吓坏了，因为我完全不知道该去往何处。"),
            ("W", "I cannot walk or even lift my leg a few inches.", "当时我根本无法行走，甚至连把腿抬起几英寸都做不到。"),
            ("W", "The hospital social worker strikes me as an idiot.", "医院配设的社工在我眼里简直愚不可及。"),
            ("W", "But my complaints about her only annoy my surgeon.", "但我对这名社工的抱怨，只会惹得我的主刀医生心烦意乱。"),
            ("W", "'I have to work with these people,' he tells my friend, Dr. Karen Brudney, when she mercifully intervenes on my behalf and arranges for me to be transferred to another hospital.", "当我的朋友凯伦·布鲁德尼医生仁慈地出面干预并替我安排转院时，主刀医生对她说：‘我还得跟这帮同事长期共事呢。’"),
            ("W", "'If you say one negative thing, they get defensive,' she tells me later.", "‘只要你指出一点负面问题，他们就会立刻进入防卫对抗状态，’布鲁德尼医生后来这样告诉我。"),
            ("W", "'They have this kind of institutional loyalty.'", "‘他们内部有着这样一种根深蒂固的体制忠诚。’"),
            ("W", "Always bring an advocate, that is, any other person with you to the hospital, and write down every single question and the answer, the name of every doctor and nurse.", "去医院就医时务必带上一位陪护代言人（即任何能陪伴在你身边的亲友），并一字不漏地记下每一个问题与回答，以及每一位医生和护士的姓名。"),
            ("W", "When people know you have their names, they behave better.", "当医护人员知道你掌握了他们的具体姓名时，他们的态度和行为会有所收敛与改善。"),
            ("W", "And, Brudney adds, if you, as a patient, suggest that you might like to control even part of the situation or be consulted or informed, then you are considered difficult.", "布鲁德尼医生进一步补充道，如果你作为一名患者表现出哪怕想要掌控部分就医局面、或者希望被征求意见知情同意的迹象，你就会被贴上‘难缠’的标签。"),
            ("W", "They want you to be totally passive.", "他们只希望你成为完全顺从、任凭摆布的被动接受者。"),
            ("W", "The entire healthcare system, particularly hospitals and nursing homes, exists for reasons that have nothing to do with taking care of patients.", "整个医疗保健体系，尤其是医院和养老护理院，其运转的很多底层逻辑与悉心关怀患者毫无关系。"),
            ("W", "Patients are incidental.", "在他们眼里，患者不过是附带的一环而已。")
        ]
    },
    {
        "id": "2022-06-set1-rec-2",
        "subpart_code": "rec-2",
        "section_id": "2022-06-set1-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 2 · 高效团队维系机制、人口同质性与职场多元化",
        "topic_zh": "高效团队维系机制、人口同质性与职场多元化",
        "question_range": "Q19 ~ Q21",
        "questions": [19, 20, 21],
        "sp_start": 1213.0,
        "sp_end": 1397.0,
        "sentences": [
            ("M", "There are probably teams you've worked with that you never want to work with again.", "你可能曾与某些团队共事过，但你再也不想和他们二次合作了。"),
            ("M", "But there must have also been other teams that you would prize reuniting with professionally.", "但肯定也存在另外一些团队，能与他们在业务上再度携手会让你倍感珍惜。"),
            ("M", "In other words, your team had vitality.", "换句话说，你的团队拥有强大的生机与活力。"),
            ("M", "Vitality comes about when the ties people form with their fellow team members are such that they stay connected even after the team breaks up.", "所谓活力，就是指人们与团队同仁之间建立起来的紧密纽带，足以维系他们在团队解散后依然保持着密切联系。"),
            ("M", "What characteristics of a team make its members more likely to stay in contact despite no longer working together?", "究竟团队具备什么样的特征，才能促使其成员在不再共同工作之后依然乐于保持长期联络？"),
            ("M", "This question has been answered recently in a study published in a business journal.", "最近发表在一家商业期刊上的一篇研究论文解答了这一疑问。"),
            ("M", "One of the two key factors the research team discovered is sameness, specifically sharing the same gender or ethnic origin.", "研究团队发现的两大关键因素之一是‘同质性’，具体指的是拥有相同的性别或种族族裔背景。"),
            ("M", "The more members of a team share similar demographics, the more inclined they'll be to remain associates long after the team has served its purpose.", "团队成员之间在人口统计学特征上的相似度越高，他们在团队达成使命解散后保持长期合作交往的倾向就越强烈。"),
            ("M", "After ties are established, similarity strengthens them.", "在关系初步建立之后，彼此的相似性会进一步强化这种纽带。"),
            ("M", "As a result, they regard these individuals with greater trust and mutual understanding, which motivates them to seek further opportunities for collaboration.", "其结果是，他们会以更高的信任感和相互理解来看待这些人，从而激励他们不断寻求进一步的合作契机。"),
            ("M", "In effect, people tend to create stronger and longer lasting connections with similar others.", "实际上，人们往往倾向于与同自己相似的人建立起更牢固、更持久的深厚联系。"),
            ("M", "Someone who looks and sounds different from us may have the resources we need to be more successful, yet we find them to be significantly less credible simply because they are different.", "那些在外貌或口音上与我们大相径庭的人，或许恰好拥有助我们取得更大成功所需的资源，但仅仅因为他们与我们不同，我们便觉得他们远不如同类可靠。"),
            ("M", "If you are a fierce advocate of workplace diversity, you'll no doubt be horrified by such a revelation.", "如果你是职场多元化的坚定拥护者，这项揭示无疑会让你感到震惊与愕然。"),
            ("M", "The second factor identified by the researchers is the quality of the relationships among the team members.", "研究人员指出的第二个决定性因素，是团队成员之间人际关系的质量。"),
            ("M", "The more they trust one another, share the same goals and depend on each other for the achievement of those goals, the stronger their chances of maintaining their connections despite no longer working as one team.", "成员之间越互相信任、拥有共同的目标并在追求目标的过程中休戚与共，那么即便他们不再作为一个团队共事，维系紧密联络的几率也就越高。"),
            ("M", "Teams with quality relationships have a shared belief that it's safe to take risks with each other and that members are obliged to share the workload and help out.", "拥有高质量关系的团队往往秉持着共同的信念：彼此之间敢于分担风险是安全的，大家也有义务互帮互助、共同分担繁重的工作量。"),
            ("M", "From personal experience, I can see both the truth and the inconsistency of such studies.", "结合自身的亲身经历，我既能领会此类研究的真确性，也能看出其自相矛盾之处。"),
            ("M", "The truth is some of my closest friendships were formed as a result of having worked together on teams, and I actively seek opportunities to work with them again.", "真实的一面在于，我的一些最亲密挚友确实是在团队共事的过程中结下的，我也总是积极寻求与他们再次合作的机会。"),
            ("M", "The inconsistency, though, is that I've never worked for a team more successful and cohesive than the one of which I'm a member right now, and yet the four of us have very little in common and are completely different demographically.", "然而矛盾的一面在于，我从未遇到过比我现在所在的团队更成功、更有凝聚力的团队了——然而我们四位成员之间几乎毫无共同之处，在人口背景上完全迥异。"),
            ("M", "So I'm unlikely to question the value of a diverse workforce.", "因此，我绝不会怀疑多元化员工团队所具备的巨大价值。")
        ]
    },
    {
        "id": "2022-06-set1-rec-3",
        "subpart_code": "rec-3",
        "section_id": "2022-06-set1-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 3 · 百万富翁六大致富行为特质与长期财富规划",
        "topic_zh": "百万富翁六大致富行为特质与长期财富规划",
        "question_range": "Q22 ~ Q25",
        "questions": [22, 23, 24, 25],
        "sp_start": 1465.0,
        "sp_end": 1630.0,
        "sentences": [
            ("W", "An American researcher who studied 600 millionaires found how rich you can get comes down to six wealth factors.", "一位深入研究了600名百万富翁的美国学者发现，一个人能聚敛多少财富最终取决于六大财富要素。"),
            ("W", "She found that six behaviors are related to net worth potential, regardless of age or income.", "她发现，无论一个人的年龄长幼或收入高低，有六种具体行为特质与净资产潜能休戚相关。"),
            ("W", "These were thriftiness, confidence, responsibility, planning, focus, and social indifference.", "这六大特质分别是：节俭、自信、责任感、规划性、专注力以及对社交跟风的漠视。"),
            ("W", "Being thrifty comes as no great surprise.", "节俭这一特质并不令人意外。"),
            ("W", "Spending above your means, spending instead of saving for retirement, spending in anticipation of becoming wealthy makes you a slave to the paycheck.", "超前消费入不敷出、把本该用于养老的储蓄挥霍一空、在尚未发迹前就预支消费，会让你沦为按月拿死工资的薪水奴隶。"),
            ("W", "'Even with an astronomical level of income,' she wrote, 'to properly build wealth, experts recommend saving 20% of your income and living off the remaining 80%.'", "她在书中写道：‘即使坐拥天文数字般的高收入，要想真正稳健地积累财富，专家建议应当把收入的20%储蓄起来，只依靠剩余的80%来维持日常生活开销。’"),
            ("W", "Having confidence is another key characteristic, as it helps people to be thrifty.", "拥有充足的自信是另一项核心特质，因为它能助人坚守节俭美德。"),
            ("W", "It takes confidence to live within your means.", "量入为出过简朴生活是需要内心强大的自信的。"),
            ("W", "It also takes confidence to invest properly, instead of making investing decisions with your emotions, financial planners advise that you should leave your investments alone and focus on a long-term investment plan.", "理性投资同样需要定力与自信；理财顾问告诫：与其任由情绪冲动做出买卖决策，不如对投资组合保持克制少去折腾，坚定专注于长期的投资规划。"),
            ("W", "But people can't invest or manage their own money without accepting responsibility for the outcomes.", "但人们若不能勇敢为投资结果承担个人责任，就根本谈不上做好理财或掌管自己的财富。"),
            ("W", "Many millionaires take on personal responsibility, and most also happen to be self-made, meaning they didn't acquire their wealth through luck.", "绝大多数百万富翁都极具个人担当，且他们当中大多是白手起家的创业者，这意味着他们的财富绝非侥幸得来。"),
            ("W", "Millionaires don't count on anyone else to make them rich, and they don't blame anyone else if they fall short.", "百万富翁从不指望别人来让他们发财，一旦遭遇挫折达不到预期，他们也绝不会怨天尤人或推诿责任。"),
            ("W", "They focus on things they can control and align their daily habits to the goals they have set for themselves.", "他们全神贯注于自己能够掌控的事物，并让日常生活习惯紧紧围绕既定的目标高效运转。"),
            ("W", "They tend to be goal-oriented and hard workers which enables them to plan financially and focus on seeing those plans through.", "他们往往具有强烈的目标导向且工作极其勤勉，这使他们能够制定科学周密的财务规划，并不遗余力地确保这些规划贯彻执行到底。"),
            ("W", "92% of millionaires surveyed developed a long-term plan for their money, and 97% almost always achieved the goals they set for themselves.", "受访的百万富翁中有92%都为其资金制定了长远规划，且高达97%的人几乎总能顺利实现自己设定的各项目标。"),
            ("W", "And it is these behaviors that make it easy for them to be socially indifferent.", "正是这些特质，使他们能够轻松做到对外界社交攀比漠然处之。"),
            ("W", "They resist lifestyle creep: the tendency to spend more whenever one earns more.", "他们自觉抵制所谓的‘生活方式膨胀’——即每当收入增加时就倾向于消费更多的高危陷阱。"),
            ("W", "Essentially, they don't yield to pressure to buy the latest thing or to keep up with others or what they have acquired.", "从本质上讲，他们绝不屈服于盲目追赶潮流购买最新潮流物件的压力，也从不屑于去攀比别人或别人所拥有的行头。"),
            ("W", "Instead of being focused on what might make them happy today, they're focused on their long-term wealth-building plan.", "与其纠结于眼前什么能带来一时的即时快感，他们更专注于长远的财富筑造宏图。")
        ]
    }
]

QUESTIONS = {
    1: {
        "prompt": "What do we learn about David Jackson from the conversation?",
        "options": {
            "A": "He is a staff writer.",
            "B": "He is an adventurer.",
            "C": "He is an author of fiction.",
            "D": "He is a father of four kids."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。女士在介绍男士时明确指出：“Mr. David Jackson, a staff writer at The New Yorker, is known for his non-fiction books of adventure.”即杰克逊先生是《纽约客》杂志的专职撰稿人。因此答案为 A)。"
    },
    2: {
        "prompt": "What does the man think of young teenagers?",
        "options": {
            "A": "They are interested in fairy tales.",
            "B": "They are curious and autonomous.",
            "C": "They are a headache to their parents.",
            "D": "They are ignorant of politics."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。男士评价处于该年龄段的青少年时表示：“They are independent and they have their own curiosities and obsessions.”即他们独立自主且充满好奇心（curious and autonomous 对应 independent and have their own curiosities）。因此答案为 B)。"
    },
    3: {
        "prompt": "How does the man help his kids with their essays?",
        "options": {
            "A": "He offers them ample editorial guidance.",
            "B": "He recommends model essays to them.",
            "C": "He gives them encouragement.",
            "D": "He teaches them proofreading."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。当女士询问男士是否帮孩子校对作文时，男士回答说自己主要给予鼓励，认为在此阶段鼓励比编辑指导更为重要（I really just try to be encouraging. I think at this age editorial guidance is less important than encouragement）。因此答案为 C)。"
    },
    4: {
        "prompt": "What does the woman say about herself when she was a teenager?",
        "options": {
            "A": "Her tastes in books changed.",
            "B": "She realized the power of reading.",
            "C": "Her reading opened her eyes to the world.",
            "D": "She began to perceive the world differently."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。女士提到：“I feel that children's tastes in books change as they reach adolescence. I know that mine certainly did when I was a teenager.”即她在青少年时期对书籍的品位确实发生了改变。因此答案为 A)。"
    },
    5: {
        "prompt": "What do we learn about the woman?",
        "options": {
            "A": "She is a website designer.",
            "B": "She is a university graduate.",
            "C": "She is a main street store owner.",
            "D": "She is a successful entrepreneur."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。男士在开场介绍莫莉时指出：“our guest is Molly Sanders, a university student and a successful young entrepreneur.”说明她是一位成功的青年创业家。因此答案为 D)。"
    },
    6: {
        "prompt": "What does the woman say about the clothes she made at first?",
        "options": {
            "A": "They were repeatedly rejected by shops.",
            "B": "They were popular with her classmates.",
            "C": "They showed her natural talent.",
            "D": "They were mostly failures."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。女士回顾最初制作服装的经历时提到：“No one taught me to make clothes and most of the things I made at first were disasters.”即刚开始做的衣服大多是一团糟、彻底失败（mostly failures 对应 were disasters）。因此答案为 D)。"
    },
    7: {
        "prompt": "Why did the woman persevere in making clothes for herself?",
        "options": {
            "A": "She had a strong interest in doing it.",
            "B": "She did not like ready-made clothes.",
            "C": "She could not find clothes of her size.",
            "D": "She found clothes in shops unaffordable."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。女士解释自己坚持下来的原因：“I kept on out of necessity. As you can see, I'm very tall and I couldn't find clothes that fit me in ordinary shops.”因为自己个子很高，在普通商店买不到合身尺码的衣服。因此答案为 C)。"
    },
    8: {
        "prompt": "What does the woman plan to do in the future?",
        "options": {
            "A": "Study fashion design at college.",
            "B": "Improve her marketing strategy.",
            "C": "Add designs for women.",
            "D": "Expand her business."
        },
        "answer": "D",
        "explanation": "【精析】细节推断题。女士提到未来的规划：“I will add more clothes for children, both girls and boys, and possibly even for infants. And I hope to add to my range of designs for men.”增加童装、婴儿装以及拓展男装系列，意味着她计划进一步扩大业务范围（Expand her business）。因此答案为 D)。"
    },
    9: {
        "prompt": "What have researchers done for the first time in history?",
        "options": {
            "A": "Utilizing artificial intelligence to find a powerful new antibiotic.",
            "B": "Discovering bacteria which are resistant to all known antibiotics.",
            "C": "Identifying bacterial strains that are most harmful to humans.",
            "D": "Employing advanced technology to eliminate deadly bacteria in mice."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。短文中明确指出：“The researchers say this is the first time that artificial intelligence has been used to find a powerful new antibiotic molecule.”这是首次利用人工智能发现强效的新型抗生素分子。因此答案为 A)。"
    },
    10: {
        "prompt": "What makes it important to find new antibiotic drugs?",
        "options": {
            "A": "Ever-increasing strains of bacteria.",
            "B": "Bacteria's resistance to antibiotics.",
            "C": "The similarity between known drugs.",
            "D": "The growing threat of bacteria to health."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。短文在探讨为何寻找新抗生素至关重要时指出：“The answer is antibiotic resistance... Antibiotic resistance is a serious threat to health and the problem is growing. This makes finding new antibiotics very important.”即细菌耐药性问题使得寻找新抗生素极其重要。因此答案为 B)。"
    },
    11: {
        "prompt": "What does the passage say artificial intelligence is able to do in antibiotic research?",
        "options": {
            "A": "Dispense with experimental testing.",
            "B": "Predict whether compounds are toxic.",
            "C": "Foresee human reaction to antibiotics.",
            "D": "Combat bacteria's resistance to antibiotics."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。短文中明确指出：“Artificial intelligence is also able to predict if compounds are likely to be toxic.”人工智能还能够预测化合物是否可能具有毒性。因此答案为 B)。"
    },
    12: {
        "prompt": "According to the passage, how do most people detect lying?",
        "options": {
            "A": "By theorization.",
            "B": "By generalization.",
            "C": "By observation.",
            "D": "By conversation."
        },
        "answer": "C",
        "explanation": "【精析】细节归纳题。短文中提到：“We may develop that theory from observations of those people we know well... it's usually based on close observation of people we know.”大多数人都是通过日常对熟人的密切观察来辨别谎言的。因此答案为 C)。"
    },
    13: {
        "prompt": "What does the passage say about most lies?",
        "options": {
            "A": "They are easy to detect.",
            "B": "They are well intended.",
            "C": "They are groundless.",
            "D": "They are harmless."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。短文中提到人们每天大约遭遇200次谎言：“These are mostly harmless lies, but lies nonetheless.”这些谎言绝大多数都是无害的。因此答案为 D)。"
    },
    14: {
        "prompt": "What have many studies uncovered about the average person's lie detection?",
        "options": {
            "A": "Mostly by chance.",
            "B": "Basically objective.",
            "C": "Subject to their mental alertness.",
            "D": "Dependent on their analytical ability."
        },
        "answer": "A",
        "explanation": "【精析】细节推断题。短文中指出：“The average person, you and me, tested rigorously on how well we detect lies, fails to do better than chance.”普通人在严谨测谎测试中的表现并不比凭概率瞎猜好多少（Mostly by chance）。因此答案为 A)。"
    },
    15: {
        "prompt": "What advice does the new research offer regarding lie detection?",
        "options": {
            "A": "Looking the speaker in the eye.",
            "B": "Listening carefully to the speaker.",
            "C": "Measuring the speaker's breathing rate.",
            "D": "Focusing on the speaker's facial expressions."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。短文临近结尾处给出建议：“The new research offers some surprising advice: stop looking and listen instead. It turns out that if we're unable to see the face, but rather focus on the voice of the person in question, our accuracy rate improves considerably.”不要去看面孔，而是仔细聆听对方的声音。因此答案为 B)。"
    },
    16: {
        "prompt": "What does the speaker say about most American hospitals?",
        "options": {
            "A": "They don't treat patients with due respect.",
            "B": "They witness a lot of doctor-patient conflicts.",
            "C": "They have to deal with so many patients with tumors.",
            "D": "They are in fierce competition with health insurance companies."
        },
        "answer": "A",
        "explanation": "【精析】细节推断题。讲话者指出：“What patients want is to be treated with respect and consideration. But in my experience, too few hospitals and doctors are ready to do that.”患者希望受到尊重与体谅，但极少有医院和医生愿意这么做，表明大多数美国医院对患者缺乏应有的尊重。因此答案为 A)。"
    },
    17: {
        "prompt": "What does Karen Brudney suggest patients do?",
        "options": {
            "A": "Appear submissive and grateful to doctors and nurses.",
            "B": "Express a strong desire to be consulted or informed.",
            "C": "Refrain from saying anything that sounds negative.",
            "D": "Note down the names of doctors and nurses."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。布鲁德尼医生建议：“Always bring an advocate... and write down every single question and the answer, the name of every doctor and nurse, when people know you have their names, they behave better.”务必记下每位医生和护士的姓名。因此答案为 D)。"
    },
    18: {
        "prompt": "What do American doctors expect their patients to be, according to Karen Brudney?",
        "options": {
            "A": "Cooperative.",
            "B": "Appreciative.",
            "C": "Passive.",
            "D": "Responsive."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。布鲁德尼医生指出，患者若想主动了解情况就会被视为难缠：“They want you to be totally passive.”医护人员希望患者是完全被动的。因此答案为 C)。"
    },
    19: {
        "prompt": "What does the speaker say about a team with vitality?",
        "options": {
            "A": "Its members work together despite risks of failure.",
            "B": "It prioritizes recruiting young energetic members.",
            "C": "Its members stay in touch even after it breaks up.",
            "D": "It grows more and more mature over time."
        },
        "answer": "C",
        "explanation": "【精析】细节推断题。讲话者对有活力的团队定义道：“Vitality comes about when the ties people form with their fellow team members are such that they stay connected even after the team breaks up.”充满活力的团队，其成员即使在团队解散后仍保持联系。因此答案为 C)。"
    },
    20: {
        "prompt": "What do the researchers find out about members of a team?",
        "options": {
            "A": "Their differences are likely to impact productivity.",
            "B": "Their similarity is conducive to future collaboration.",
            "C": "Their connections strengthen with the passage of time.",
            "D": "Their mutual understanding depends on prior ties."
        },
        "answer": "B",
        "explanation": "【精析】细节推断题。研究发现：“The more members of a team share similar demographics, the more inclined they'll be to remain associates... motivates them to seek further opportunities for collaboration.”团队成员之间的相似性有助于强化纽带，激励未来的合作。因此答案为 B)。"
    },
    21: {
        "prompt": "What do we learn about the team the speaker is currently working in?",
        "options": {
            "A": "It is characterized by diversity.",
            "B": "Its goals are quite inconsistent.",
            "C": "Its members have similar backgrounds.",
            "D": "It is connected by a unique mechanism."
        },
        "answer": "A",
        "explanation": "【精析】细节推断题。讲话者介绍自己当前所在的团队：“the four of us have very little in common and are completely different demographically. So I'm unlikely to question the value of a diverse workforce.”四名成员人口背景各不相同，最大的特色就是多样性（diversity）。因此答案为 A)。"
    },
    22: {
        "prompt": "What do experts recommend concerning being thrifty?",
        "options": {
            "A": "Putting aside twenty percent of one's earnings.",
            "B": "Spending in anticipation of becoming wealthy.",
            "C": "Living off a small proportion of one's income.",
            "D": "Saving as much as one can possibly manage."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。讲话者引述专家的建议：“to properly build wealth, experts recommend saving 20% of your income and living off the remaining 80%.”专家建议将收入的20%储蓄起来（Putting aside twenty percent of one's earnings）。因此答案为 A)。"
    },
    23: {
        "prompt": "How does confidence help people to be thrifty?",
        "options": {
            "A": "It empowers them to cope with irrational emotions.",
            "B": "It will guarantee the profits from their investments.",
            "C": "It will turn them into successful financial planners.",
            "D": "It enables them to focus on a long-term plan."
        },
        "answer": "D",
        "explanation": "【精析】细节推断题。讲座中提到：“It takes confidence to invest properly, instead of making investing decisions with your emotions, financial planners advise that you should leave your investments alone and focus on a long-term investment plan.”自信能使人不为情绪所动，坚定专注于长期的投资规划。因此答案为 D)。"
    },
    24: {
        "prompt": "How do millionaires react when they fail in their investment?",
        "options": {
            "A": "They count on others to take the responsibility.",
            "B": "They change their investment strategy in time.",
            "C": "They think they themselves are to blame.",
            "D": "They persist rather than get discouraged."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。讲座中指出：“Millionaires don't count on anyone else to make them rich, and they don't blame anyone else if they fall short... enables them to plan financially and focus on seeing those plans through.”百万富翁面对失误不怨天尤人，而是坚持到底贯彻既定规划，百折不挠。因此答案为 D)。"
    },
    25: {
        "prompt": "Why does the speaker say millionaires are socially indifferent?",
        "options": {
            "A": "They do not resist novel lifestyles.",
            "B": "They do not try to keep up with others.",
            "C": "They do not care what they have acquired.",
            "D": "They do not pressure themselves to get rich."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。讲座中解释百万富翁对外界社交漠然处之的原因：“Essentially, they don't yield to pressure to buy the latest thing or to keep up with others or what they have acquired.”他们从不屈服于追赶潮流或与他人攀比的社会压力（do not try to keep up with others）。因此答案为 B)。"
    }
}
