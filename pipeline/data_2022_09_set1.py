import json

SUBPARTS = [
    {
        "id": "2022-09-set1-conv-1",
        "subpart_code": "conv-1",
        "section_id": "2022-09-set1-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 1 · 个人财务预算规划与非必要支出削减",
        "topic_zh": "个人财务预算规划与非必要支出削减",
        "question_range": "Q1 ~ Q4",
        "questions": [1, 2, 3, 4],
        "sp_start": 38.0,
        "sp_end": 166.0,
        "sentences": [
            ("M", "Welcome to Money Matters, a weekly program that helps you manage your money.", "欢迎收听《金钱事大》，这是一档帮助您管理个人财务的周播节目。"),
            ("M", "Tonight, I will be talking to Mary Johnson about budgeting.", "今晚，我将与玛丽·约翰逊一起聊聊如何制定财务预算。"),
            ("W", "Hello, everyone.", "大家好。"),
            ("M", "There's a magic about money.", "金钱身上有一种魔性。"),
            ("M", "When it's not planned for, tracked and kept a record of, it literally disappears.", "如果不去规划、追踪并记录，它简直就像凭空消失了一样。"),
            ("M", "What are some of the steps we can take to prevent this from happening?", "我们能采取哪些步骤来防止这种情况发生呢？"),
            ("W", "Well, it's all about keeping track of your money.", "嗯，关键就在于要时刻追踪你的钱财去向。"),
            ("W", "If you don't do that, you'll never be able to set any goals for your budget or have the discipline to stick to them.", "如果你不这样做，你就永远无法确立任何预算目标，也不可能有自律性去坚守执行。"),
            ("M", "That's easier said than done.", "这说起来容易做起来难啊。"),
            ("M", "I read recently that only 41% of Americans adhere to a budget.", "我最近读到一份报告，说只有41%的美国人能够坚持执行预算。"),
            ("W", "Yes, but knowing what you earn and what you spend can give you reassurance that you won't get into debt in the first place.", "是的，但清楚自己挣了多少和花了多少，首先能让你心里有底，确保自己不至于陷入债务困境。"),
            ("W", "You can do this by adding up all of your sources of income you have and writing them all down on a piece of paper.", "你可以把所有的收入来源加在一起，全部写在一张纸上。"),
            ("W", "On the same page, write down all of your monthly expenses.", "在同一张纸上，再列出你所有的每月支出明细。"),
            ("M", "I'm always amazed at how much my expenses add up.", "我总是对自己的开销累计起来有那么多感到惊讶。"),
            ("M", "But designating each item as an income or an expense really helps me have a much better sense of all my spending.", "但把每一项清晰划分为收入或支出，确实极大地帮助我更清楚地掌握整体开支情况。"),
            ("W", "Right.", "没错。"),
            ("W", "Most people have no idea how much they spend each day, let alone each week or month, no matter how careful they are.", "大多数人根本不知道自己每天花了多少钱，更不用说每周或每月了，无论他们自认为有多细心。"),
            ("W", "Next, subtract your monthly expenses from income.", "接下来，用总收入减去每月总支出。"),
            ("W", "If the result is positive, you are living within your means.", "如果结果是正数，说明你量入为出、收支平衡。"),
            ("W", "If the result is a negative number, you're going to have to cut back on your spending.", "如果结果是负数，那你就必须削减开支了。"),
            ("M", "I'm usually a negative number.", "我的结果通常都是负数。"),
            ("M", "I just can't resist the lure of all those prestigious goods.", "我总是无法抵御那些高端名牌商品的诱惑。"),
            ("W", "Well, it's not a catastrophe, but you do have to make some changes.", "好吧，这倒不是什么灭顶之灾，但你确实得做出一些改变。"),
            ("W", "Try cutting back on those non-essential items.", "试着削减那些非必需品的消费。"),
            ("W", "Sell some stuff in your attic, or shop online to avoid unnecessary temptations like chocolate.", "把阁楼里闲置的杂物变卖掉，或者在网上购物以避开巧克力之类的额外诱惑。"),
            ("W", "Failing that, you can always find yourself a part-time job.", "要是这还不行，你还可以随时给自己找一份兼职工作。")
        ]
    },
    {
        "id": "2022-09-set1-conv-2",
        "subpart_code": "conv-2",
        "section_id": "2022-09-set1-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 2 · 租房实地看房、配套环境与租约签订",
        "topic_zh": "租房实地看房、配套环境与租约签订",
        "question_range": "Q5 ~ Q8",
        "questions": [5, 6, 7, 8],
        "sp_start": 241.0,
        "sp_end": 365.0,
        "sentences": [
            ("M", "Hi there.", "你好。"),
            ("M", "I've come to see the flat.", "我是来看房子的。"),
            ("M", "My name is Mark Adams.", "我叫马克·亚当斯。"),
            ("M", "We spoke on the phone on Wednesday.", "我们周三在电话里联系过。"),
            ("W", "Hi, Mark.", "嗨，马克。"),
            ("W", "Come on up.", "请上楼来吧。"),
            ("W", "I'll buzz you in.", "我给你按门禁开锁。"),
            ("W", "Green door on the second floor on the right side.", "二楼右手边绿色的门就是。"),
            ("W", "Nice to meet you.", "很高兴见到你。"),
            ("W", "I spoke to all your references, and they all checked out okay.", "我联系了你所有的证明人，背景审查都没问题。"),
            ("W", "So let me show you around.", "那我带你四处看看吧。"),
            ("W", "The place actually belongs to my mother, but her health isn't great, so we finally managed to persuade her to move in with us and rent this old place out.", "这处房子实际上属于我母亲，但她身体不太好，所以我们终于说服她搬来和我们同住，并把这套老房子出租出去。"),
            ("M", "It's a great size, plenty of space, very versatile.", "房子面积挺宽敞，空间很大，格局非常实用。"),
            ("M", "I think it's a winner for us.", "我觉得这完全符合我们的要求。"),
            ("W", "Yes, all the appliances are brand new.", "是的，所有的家电都是全新购置的。"),
            ("W", "There's a washing machine and a tumble dryer in the utility room next to the kitchen.", "厨房旁边的杂物间里配有洗衣机和烘干机。"),
            ("M", "Lots of closet space too, which is fabulous.", "衣柜空间也很充裕，这太棒了。"),
            ("M", "My wife has a ridiculous number of shoes.", "我妻子的鞋子多得惊人。"),
            ("M", "Now, the big question.", "现在还有个关键问题。"),
            ("M", "What about noise and the neighbors?", "周围的噪音情况和邻居怎么样？"),
            ("W", "Well, all the neighbors are elderly, so no noisy kids, and the back of the house overlooks a clear and peaceful pond.", "嗯，邻居全都是老年人，所以没有吵闹的小孩，而且房子后窗正对着一处清澈宁静的水池。"),
            ("W", "So it's perfect if tranquility is what you are looking for.", "所以如果你追求清静安宁，这里再合适不过了。"),
            ("M", "That's good news.", "那真是个好消息。"),
            ("M", "We've been living in a less than glamorous part of Aberdeen.", "我们之前一直住在阿伯丁一个不太体面的地段。"),
            ("M", "Constantly harassed day and night by noisy neighbors.", "日日夜夜被吵闹的邻居搅得不得安宁。"),
            ("M", "Getting to work was a nightmare too, as we only have one car, and my wife has to use it as she works nights at the hospital.", "上班通勤也是场噩梦，因为我们只有一辆车，而我妻子在医院上夜班必须用车。"),
            ("W", "Well, if you like the place, it's yours as soon as I get a contract drawn up with the solicitor.", "好吧，只要你相中这里，等我找律师拟好合同，房子就是你的了。"),
            ("W", "The first month's rent and a deposit are mandatory on signing the contract.", "在签署合同时，必须缴纳首月租金和押金。"),
            ("W", "Then we can work out when is the best day for you to pay rent each month.", "之后我们可以商量每个月几号交房租最合适。"),
            ("M", "We'll be incredibly happy to be your new tenants.", "能成为您的新租客，我们感到无比高兴。"),
            ("M", "Thank you so much.", "非常感谢您。"),
            ("M", "My wife will be thrilled to get out of the shabby place we are now in and start filling those wardrobes with all those shoes.", "我妻子要是知道能搬出我们现在那间破旧的住所，并开始把她那一堆鞋子塞满这些大衣柜，一定会欣喜若狂的。")
        ]
    },
    {
        "id": "2022-09-set1-pass-1",
        "subpart_code": "pass-1",
        "section_id": "2022-09-set1-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 1 · 儿童观看电视广告与家庭消费冲突压力",
        "topic_zh": "儿童观看电视广告与家庭消费冲突压力",
        "question_range": "Q9 ~ Q11",
        "questions": [9, 10, 11],
        "sp_start": 476.0,
        "sp_end": 601.0,
        "sentences": [
            ("W", "A new study has found a positive correlation between how much television children watch and their parents' stress levels.", "一项新研究发现，儿童看电视的时长与父母的压力水平之间存在正相关。"),
            ("W", "Why?", "这是为什么呢？"),
            ("W", "Because the more television kids watch, the more they're exposed to advertising.", "因为孩子们看电视越多，接触到的商业广告就越多。")
            ,
            ("W", "The more advertising they see, the more likely they are to insist on purchasing items when they go with their parents to the store.", "他们看到的广告越多，陪同父母去商店时就越可能坚持要求购买各种物品。"),
            ("W", "This could generate conflict if the parents refuse.", "如果父母拒绝购买，就会引发家庭冲突。"),
            ("W", "All that researchers say can contribute to parents' overall stress levels.", "研究人员表示，所有这些都会加剧父母的整体压力负担。"),
            ("W", "What's the solution?", "解决之道是什么呢？"),
            ("W", "Perhaps the most obvious is curtailing screen time.", "或许最显而易见的办法就是缩短屏幕使用时间。"),
            ("W", "Commercial content is there for a reason: to elicit purchasing behavior.", "商业广告内容的存在是有目的的：就是为了诱发购买行为。"),
            ("W", "So, parents might want to shut off the TV.", "因此，父母可能需要关掉电视。"),
            ("W", "Researchers can see that this is easier said than done, so they suggest another option.", "研究人员明白这一点说来容易做来难，因此提出了另一个备选方案。"),
            ("W", "Parents can change how they talk to their kids about purchases.", "父母可以改变与孩子就购物沟通的方式。"),
            ("W", "The researchers suggest that parents seek input from their children on family purchasing decisions.", "研究人员建议，父母在做出家庭购买决策时征求孩子的意见。"),
            ("W", "They shouldn't try to control all purchases.", "父母不应试图完全掌控所有的购买决定。"),
            ("W", "Instead, parents might tell their children things like, 'I will listen to your advice on certain products or brands.'", "相反，父母可以对孩子说诸如‘在某些产品或品牌上，我会听取你的建议’这样的话。"),
            ("W", "This type of communication the researchers assert can lead to children making fewer purchasing demands.", "研究人员断言，这种类型的沟通可以促使孩子减少无理的购买索求。"),
            ("W", "That means less parents' stress.", "这意味着父母的压力会随之减轻。"),
            ("W", "However, the protective effect of this kind of communication diminishes with greater exposure to television.", "然而，随着看电视时间的进一步增加，这种沟通方式的保护性效果会逐渐减弱。"),
            ("W", "This is because advertising aimed at children is especially persuasive.", "这是因为针对儿童的广告具有极强的诱导说服力。"),
            ("W", "Advertisers use an assortment of tactics such as bright colors, happy music, and celebrity endorsements to appeal to children.", "广告商采用各种各样的手法，如鲜艳的色彩、欢快的音乐和明星代言，来吸引孩子们的目光。"),
            ("W", "Plus, children don't have the cognitive ability to fully understand advertising's intent.", "此外，儿童尚不具备充分理解广告真实意图的认知能力。"),
            ("W", "That makes them particularly vulnerable to advertisements.", "这使得他们在广告面前格外脆弱、容易受到影响。")
        ]
    },
    {
        "id": "2022-09-set1-pass-2",
        "subpart_code": "pass-2",
        "section_id": "2022-09-set1-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 2 · 好人受贬损现象与群体竞争心理剖析",
        "topic_zh": "好人受贬损现象与群体竞争心理剖析",
        "question_range": "Q12 ~ Q15",
        "questions": [12, 13, 14, 15],
        "sp_start": 666.0,
        "sp_end": 787.0,
        "sentences": [
            ("M", "Everyone is supposed to cheer for good guys and we should only punish the bad guys.", "按理说每个人都应该为好人喝彩，而我们应当只惩罚那些坏人。"),
            ("M", "But that's not what we always do.", "但现实中我们并不总是这样做。"),
            ("M", "Most of the time, we do indeed reward good people.", "在大多数时候，我们确实会奖赏善良优秀的人。"),
            ("M", "We also often punish people who harm others or who aren't good team players.", "我们也经常惩罚伤害他人或缺乏团队协作精神的人。"),
            ("M", "But sometimes the good guys also get punished or criticized.", "然而有时，好人也会遭到惩罚或批评。"),
            ("M", "Specifically, because they are so good.", "具体来说，恰恰是因为他们太优秀、太突出了。"),
            ("M", "This seems baffling because it's detrimental to group cooperation.", "这看起来令人不可思议，因为它严重损害了群体合作。"),
            ("M", "However, the phenomenon has been discovered in multiple fields and it has been found in every society.", "然而，这一现象在多个领域都被发现存在，而且在每个社会中都有所体现。"),
            ("M", "Why does this happen?", "为什么会出现这种情况呢？"),
            ("M", "Research suggests a simple reason.", "科学研究给出了一个简单的缘由。"),
            ("M", "When one person looks really good, others look bad by comparison.", "当一个人表现得极为优秀时，其他人相形之下就显得相形见绌、黯然失色。"),
            ("M", "Those others then have an incentive in stopping that person from looking good.", "于是，那些相形见绌的人就有动机去阻止那个人继续出彩。"),
            ("M", "Especially if they can't or won't compete.", "特别是当他们无法竞争或不愿公平竞争的时候。"),
            ("M", "After all, we're all judged in comparison with others.", "毕竟，我们每个人都是在与他人的相互比较中被评判的。"),
            ("M", "When faced with someone better, what can a normal person do?", "当面对一个比自己更出色的人时，一个普通人能做些什么？"),
            ("M", "One option is to actively compete.", "一种选择是积极参与竞争。"),
            ("M", "A second option is to bring that person down, that is to suppress their cooperation or work ethic, infer selfish motives for their actions or imply real or imagined hypocrisy.", "第二种选择则是把那个人拉下水——即打压他们的合作意愿或敬业精神，揣测他们行善背后的自私动机，或是影射其存在真实或臆想的虚伪。"),
            ("M", "Other tactics include attacking them on unrelated dimensions or punishing them outright.", "其他手段还包括在不相关的层面上进行人身攻击，或者直接进行公开惩罚。"),
            ("M", "Why does this matter?", "为什么重视这个问题至关重要？"),
            ("M", "Critics often attack the motives of people who protect the environment, donate money, or work too hard.", "批评者经常攻击那些热心环保、捐款行善或工作极其拼命的人的动机。"),
            ("M", "Such good deeds are dismissed as naive or hypocritical by those who do not perform those deeds.", "那些从不行善积德的人，反倒将这些善举贬低为天真幼稚或虚情假意。"),
            ("M", "This criticism may ultimately discourage people from doing good deeds.", "这种无端指责最终可能会打消人们做好事的积极性。"),
            ("M", "So it's important to recognize these attacks for what they are.", "因此，认清这些恶意攻击的真实本质具有非常重要的现实意义。")
        ]
    },
    {
        "id": "2022-09-set1-rec-1",
        "subpart_code": "rec-1",
        "section_id": "2022-09-set1-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 1 · 青少年性别角色意识与同伴友谊演变",
        "topic_zh": "青少年性别角色意识与同伴友谊演变",
        "question_range": "Q16 ~ Q18",
        "questions": [16, 17, 18],
        "sp_start": 898.0,
        "sp_end": 1081.0,
        "sentences": [
            ("W", "In America, most researchers concede that boys and girls are brought up in different ways, taught different skills, and rewarded for different acts.", "在美国，大多数研究人员都承认男孩和女孩是以不同的方式抚养长大的，他们被传授不同的技能，因不同的行为获得奖励。"),
            ("W", "Women, it is agreed, excel at certain tasks, men at others.", "大家普遍认同，女性在某些任务上更擅长，男性则在其他方面表现出色。"),
            ("W", "There is little argument that some personality traits appear more dominant in one sex than in the other.", "几乎无可争议的是，某些性格特征在某一种性别身上表现得更为明显。"),
            ("W", "All of this notwithstanding, gender differences are very much in the media these days.", "尽管如此，近来媒体对性别差异的报道依然十分广泛。"),
            ("W", "Since the rise of the women's movement, gender role behavior has come under closer scrutiny.", "随着女性主义运动的兴起，性别角色行为受到了更加严谨的审视。"),
            ("W", "How has this affected friendship?", "这又是如何影响友谊的呢？"),
            ("W", "How do the sexes differ in their friendship relations?", "男女两性在友谊关系中究竟有何差异？"),
            ("W", "Most preteen children have a best friend who is usually someone of the same sex and similar age.", "大多数十一二岁的青春期前孩子都有一个最要好的朋友，这个人通常是同性别且年龄相仿的同龄人。"),
            ("W", "Both sexes share an essentially positive recollection of these childhood friendships.", "男女两性对这些童年友谊大体上都持有积极美好的回忆。"),
            ("W", "They do not differ in this respect.", "在这一点上他们并没有差别。"),
            ("W", "However, the type of play engaged in during these early friendships is telling of the difference to come.", "然而，在早期友谊中参与的游戏类型却预示了日后即将出现的差异。"),
            ("W", "Boys tend to form play groups that are competitive in nature.", "男孩倾向于组建本质上具有竞争性质的游戏群体。"),
            ("W", "Girls groups more frequently revolve around cooperative enterprises.", "女孩群体则更多围绕着合作性的活动展开。"),
            ("W", "Thus, at an early age, boys become concerned with trying hard and winning, while girls, by contrast, play house and school, engaging in roles that require complimentary support.", "因此，在很小的年纪，男孩们就格外在乎努力拼搏并取得胜利；相比之下，女孩们则玩过家家和扮老师，扮演需要互补支持的角色。"),
            ("W", "Speaking of their childhood, men recall being highly responsive to and aware of the gender role opinions of other boys.", "谈及童年时期，成年男性回忆说他们对其他男孩关于性别角色的评价高度敏感且非常在意。"),
            ("W", "Girls in preteen years appear to be less susceptible to gender role pressure.", "青春期前的女孩似乎较少受到性别角色期望压力的影响。"),
            ("W", "It is not until the dating years that women report being concerned with feminine behavior.", "直到步入恋爱约会时期，女性才表示开始关注自己的女性化行为举止。"),
            ("W", "Males, for the most part, are responsive to the suggestion that their behavior is unmanly at almost any age.", "而男性在几乎任何年龄段，都对别人暗示其行为‘没有男子气概’极其敏感。"),
            ("W", "These early attitudes, reinforced by social conditioning, continue to play an active part in the friendships of both sexes during adolescence.", "这些在社会化过程中不断被强化的早期态度，在青春期继续对男女两性的友谊产生深远影响。"),
            ("W", "This is a period when the majority of males once again report a close alliance with same-sex friends.", "在这个阶段，大多数男性再次表示与同性朋友结成了紧密的同盟关系。"),
            ("W", "Now, however, with heightened intensity, considerable energy is devoted to competing for position and a definite undercurrent of competition permeates the relationship.", "然而此时，随着竞争加剧，相当多的精力被投入到争夺地位中，一股明确的竞争暗流渗透进了彼此的关系之中。"),
            ("W", "Although in dissimilar fashion, females share equally fragile relationships at this age.", "尽管形式不同，处于这一年龄段的女性在同伴关系中也同样显得十分脆弱。"),
            ("W", "For them, the bond of loyalty extends only to the line of romantic involvement.", "对她们而言，闺蜜之间的忠诚纽带往往止步于浪漫恋情的界线。"),
            ("W", "This is most apt to be the case in late adolescence when dating and relationships with boys take sharp precedence over sisterhood.", "在青春期后期这种现象尤为普遍，此时与男生的约会和恋爱关系急剧凌驾于姐妹情谊之上。"),
            ("W", "Actually, dating dilutes the intensity of same-sex friendships for men also.", "实际上，恋爱约会同样削弱了男性之间同性友谊的浓烈程度。"),
            ("W", "For the majority of us the moment we begin to date seriously, there's a competition between romance and friendship.", "对于我们大多数人来说，从开始认真恋爱的那一刻起，浪漫爱情与同性友谊之间便展开了博弈与角逐。")
        ]
    },
    {
        "id": "2022-09-set1-rec-2",
        "subpart_code": "rec-2",
        "section_id": "2022-09-set1-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 2 · 残障人士求职信息披露时机与权益维护",
        "topic_zh": "残障人士求职信息披露时机与权益维护",
        "question_range": "Q19 ~ Q21",
        "questions": [19, 20, 21],
        "sp_start": 1144.0,
        "sp_end": 1310.0,
        "sentences": [
            ("M", "Good afternoon.", "大家下午好。"),
            ("M", "In today's lecture, we'll be talking about how and when to disclose a disability when applying for a job.", "在今天的讲座中，我们将探讨在求职应聘时如何以及何时透露自身的残疾状况。"),
            ("M", "On average, about 20% of the population has some form of disability.", "平均而言，约有20%的人口存在某种形式的残疾。"),
            ("M", "Most countries these days have equal opportunity and non-discrimination laws.", "如今大多数国家都制定了机会平等和反歧视法律。"),
            ("M", "Yet disabled people often find it hard to decide when, how, and if at all to raise their disability problem with a potential employer.", "然而，残疾求职者往往难以抉择何时、以何种方式、甚至究竟是否应该向潜在雇主提及自己的身体残疾状况。"),
            ("M", "There is uncertainty about how a recruiter will perceive their disability.", "招聘人员会如何看待他们的残疾，充满了不确定性。"),
            ("M", "As such, many candidates fear they wouldn't be considered for a position as a result of disclosing this personal information.", "因此，许多求职者担心一旦透露了这项个人隐私信息，就会直接被排除在候选人考虑范围之外。"),
            ("M", "And research has validated this as a genuine concern for many job applicants.", "而调查研究也证实，这确实是许多求职者普遍存在的现实顾虑。"),
            ("M", "It's a natural reaction, but it shouldn't be a reason to stay quiet.", "这是一种很自然的心理反应，但不应成为保持沉默的理由。"),
            ("M", "People need to remember that they are applying for a position they have the skills and experience to excel in.", "大家要记住：你之所以应聘这个职位，是因为你具备足以胜任并出类拔萃的专业技能和工作经验。"),
            ("M", "Discussing a disability with a potential employer may help them make reasonable workplace adjustments in their favor.", "与潜在雇主探讨身体状况，有助于他们在工作场所为求职者做出合理的有利于工作的适度调整。"),
            ("M", "It's most appropriate to discuss a disability when they reply to confirm an interview.", "在回复确认参加面试时讨论残疾问题，通常是最为恰当的时机。"),
            ("M", "This information didn't need to be put up front in their cover letter or resume because it's probably not relevant to the position itself.", "这些信息没有必要一开始就写在求职信或个人简历里，因为它大概率与岗位工作本身毫无关联。"),
            ("M", "Candidates with disabilities should feel they have the power to make their own decisions around sharing this information free from prejudice.", "残障求职者应当感受到，自己完全有权利在不受偏见左右的前提下自主决定何时披露这些信息。"),
            ("M", "If they find an organization that doesn't celebrate diversity and inclusion, it could say a lot about the company's culture.", "如果他们发现某家机构并不崇尚多元与包容，这便足以说明该公司的企业文化存在问题。"),
            ("M", "Perhaps the organization isn't the right fit.", "或许这样的机构根本不值得加入。"),
            ("M", "It's important for them to remember that they are seeking a manager and employer that's going to be supportive and continue to give them a great employment experience.", "求职者必须明确：他们所寻找的是一位能够给予支持、并能持续带来良好职场体验的主管和雇主。"),
            ("M", "Companies sometimes offer candidates the chance to disclose disabilities on their application form.", "企业有时会在申请表格中提供让候选人披露残疾状况的选项。"),
            ("M", "But people shouldn't feel restricted by this method or timing.", "但大家不必受到这种填报方式或时间节点的硬性束缚。"),
            ("M", "People should avoid sharing the name of their disability or condition.", "求职者应当避免直接写明所患残疾或具体病症的具体名称。"),
            ("M", "There is always the risk that the recruiter will research information that is inaccurate or irrelevant.", "因为招聘人员去自行搜索不准确或不相关的网络信息，总是伴随着被误解的风险。"),
            ("M", "If people don't think their disability will impact their ability to perform in the advertised position, then it's entirely their entitlement to choose when and whether to share this information.", "如果求职者认为自己的残疾并不会影响其胜任所招聘职位的能力，那么何时以及是否分享该信息完全是他们自主的权利。")
        ]
    },
    {
        "id": "2022-09-set1-rec-3",
        "subpart_code": "rec-3",
        "section_id": "2022-09-set1-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 3 · 背景音与不同性格对阅读理解专注度的影响",
        "topic_zh": "背景音与不同性格对阅读理解专注度的影响",
        "question_range": "Q22 ~ Q25",
        "questions": [22, 23, 24, 25],
        "sp_start": 1379.0,
        "sp_end": 1543.0,
        "sentences": [
            ("M", "Smartphones distract attention and reduce learning because of their potential to offer activities more inviting than study.", "智能手机会分散注意力并降低学习效率，因为它们能提供比刻苦钻研更具吸引力的活动。"),
            ("M", "But what about background sound alone?", "但是，单单背景声音本身又会带来什么影响呢？"),
            ("M", "A group of American researchers compared students' comprehension of verbal material when reading in the presence of background speech, instrumental music, or general noise.", "一组美国研究人员对比了学生在伴随背景人声、器乐伴奏或普通环境噪音的情况下阅读文字材料时的理解效果。"),
            ("M", "General noise is neutral, such as that from the sound of an air conditioner or fan.", "普通环境噪音是中性的，比如空调或风扇运转时发出的嗡嗡声。"),
            ("M", "Students' scores were most depressed in the presence of background speech.", "在存在背景人声讲话的情况下，学生的理解得分下降最为严重。"),
            ("M", "Comprehension was slightly better with the presence of music than with speech.", "有背景音乐伴奏时的理解效果要略好于有人声讲话的干扰。"),
            ("M", "However, when they were asked to identify melodies rather than understand text, background music interfered more.", "然而，当实验任务要求学生识别旋律而非理解文字时，背景音乐的干扰则显著增大。"),
            ("M", "When the background speech was in a language unfamiliar to participants, there was little, if any, hindrance of reading comprehension.", "当背景人声使用的是参与者完全不熟悉的语种时，对阅读理解造成的阻碍即便有，也微乎其微。"),
            ("M", "British researchers compared the effects of background speech, vocal music, instrumental music, general background noise, and silence on short-term memory.", "英国研究人员则对比了背景人声、带歌词歌曲、纯器乐音乐、一般背景噪音以及完全静音对短时记忆的影响。"),
            ("M", "Background speech had the biggest negative effect.", "背景人声造成的负面影响最为显著。"),
            ("M", "Vocal music was slightly more disruptive than instrumental.", "带歌词的音乐比纯器乐音乐具有更强的干扰性。"),
            ("M", "In general, background noise and silence were least disruptive.", "通常而言，一般背景噪音与绝对静音造成的干扰程度最低。"),
            ("M", "It seems the degree of interference from background noise depends on the overlap between the processing required on the task and the processing required to screen out the background noise.", "由此看来，来自背景噪音的干扰程度，似乎取决于完成任务所需的认知加工过程与过滤消除背景噪音所需的认知加工之间的重叠程度。"),
            ("M", "The studies suggest that when people read and when they try to remember any verbal material, background speech will inhibit their ability.", "研究表明，当人们在阅读以及试图记忆任何语言文字材料时，背景人声会显著抑制他们的认知表现。"),
            ("M", "Instrumental music will have, at worst, a slight effect.", "而纯器乐音乐即便有负面影响，充其量也十分轻微。"),
            ("M", "When students write essays, however, other research has found it is best to reduce all background noise as much as possible.", "然而其他研究发现，当学生在撰写论文或短文时，最好尽可能消除周围所有的背景噪音。"),
            ("M", "Not everyone reacts in the same way to distractions.", "并非每个人对外界干扰的反应都如出一辙。"),
            ("M", "Other studies suggest some aspects of personality may make a difference.", "另外的研究表明，性格特征的某些方面可能会造成显著差异。"),
            ("M", "The researchers subjected shy, quiet people and confident outgoing ones to high arousal or low arousal background music, general noise or silence while asking them to remember words.", "研究人员让害羞内向型受试者与自信外向型受试者在强刺激或弱刺激背景音乐、一般环境噪音或静音状态下背诵词汇。"),
            ("M", "Everyone performed best in the silent condition.", "所有人在完全静音的环境下表现均为最佳。"),
            ("M", "But less sociable people were more negatively affected by each of the distractions.", "但社交能力较弱、内向害羞的人受到每一种干扰的负面冲击都要更为严重。"),
            ("M", "So, when children are reading and trying to incorporate new material, parents could consider allowing some background music, particularly if it is instrumental, and their child is the outgoing type.", "因此，当孩子们在阅读并尝试吸收新知识时，父母可以考虑允许播放一些背景音乐，尤其是如果音乐是纯器乐伴奏且孩子性格较为外向的话。")
        ]
    }
]

QUESTIONS = {
    1: {
        "prompt": "What does the man say about the weekly program?",
        "options": {
            "A": "It enables people to earn more money.",
            "B": "It teaches the importance of financing.",
            "C": "It helps people with budgeting.",
            "D": "It introduces a novel way to invest."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。男士在开场介绍中说，《金钱事大》是每周一期的节目，旨在帮助人们管理财务，今晚他将与嘉宾探讨预算制定问题（Tonight, I will be talking to Mary Johnson about budgeting）。因此该节目能够帮助人们制定预算。因此答案为 C)。"
    },
    2: {
        "prompt": "What did the man read recently?",
        "options": {
            "A": "Many Americans are not satisfied with their income.",
            "B": "Many Americans have no idea about how to invest.",
            "C": "Most Americans do not know how to save money.",
            "D": "Most Americans do not stick to a budget."
        },
        "answer": "D",
        "explanation": "【精析】细节理解题。男士提到：“I read recently that only 41% of Americans adhere to a budget.”即只有41%的美国人坚持预算，也就是说大多数美国人不坚守预算（Most Americans do not stick to a budget）。因此答案为 D)。"
    },
    3: {
        "prompt": "What does the woman suggest the man do first to avoid getting into debt?",
        "options": {
            "A": "Keep track of his money.",
            "B": "Live within his means.",
            "C": "Find more sources of income.",
            "D": "Refrain from buying luxuries."
        },
        "answer": "A",
        "explanation": "【精析】细节理解题。当男士询问该如何防止钱财莫名流失时，女士回答说关键在于要时刻追踪自己的钱财去向（Well, it's all about keeping track of your money），了解收入与支出能确保一开始就不负债。因此答案为 A)。"
    },
    4: {
        "prompt": "What does the woman say about online shopping?",
        "options": {
            "A": "It offers a greater variety of items.",
            "B": "It helps avoid unnecessary spending.",
            "C": "It changes one's way of living.",
            "D": "It saves one's time for shopping."
        },
        "answer": "B",
        "explanation": "【精析】细节推断题。女士针对男士入不敷出的现状提出建议，可以通过网上购物来避免非必要诱惑（shop online to avoid unnecessary temptations like chocolate）。也就是说，网购有助于避免不必要的花费。因此答案为 B)。"
    },
    5: {
        "prompt": "What does the woman say about the flat?",
        "options": {
            "A": "It is brand-new.",
            "B": "It has plenty of rooms.",
            "C": "It belongs to her mother.",
            "D": "It has been vacant for months."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。女士向租客介绍房屋背景时说明：“The place actually belongs to my mother...”这处房产实际归她母亲所有。因此答案为 C)。"
    },
    6: {
        "prompt": "What is the man's chief consideration in looking for a flat?",
        "options": {
            "A": "Space.",
            "B": "Tranquillity.",
            "C": "Appliances.",
            "D": "Location."
        },
        "answer": "B",
        "explanation": "【精析】细节归纳题。男士特别询问周围噪音和邻居情况，并提到之前常年受噪音邻居困扰，而女士强调后院正对清幽水池、非常安静（it's perfect if tranquility is what you are looking for），男士表示非常满意。由此可知安静是他最主要的考量。因此答案为 B)。"
    },
    7: {
        "prompt": "What does the man have to do on signing the contract?",
        "options": {
            "A": "Talk to his wife about the contract terms.",
            "B": "Pay the first month's rent and a deposit.",
            "C": "Check the references of the flat owner.",
            "D": "Consult his solicitor one more time."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。女士明确告诉男士：“The first month's rent and a deposit are mandatory on signing the contract.”签合同时必须支付首月租金和押金。因此答案为 B)。"
    },
    8: {
        "prompt": "Why does the man say his wife will feel very excited if they move into the flat?",
        "options": {
            "A": "She can have a wonderful view of the pond.",
            "B": "She will be much closer to her work place.",
            "C": "She can make friends with new neighbours.",
            "D": "She will have plenty of space for her shoes."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。男士提到妻子拥有大量鞋子，并说道：“My wife will be thrilled to get out of the shabby place we are now in and start filling those wardrobes with all those shoes.”即大衣柜能装下她所有的鞋子会让妻子非常兴奋。因此答案为 D)。"
    },
    9: {
        "prompt": "What has the new study found about children watching television?",
        "options": {
            "A": "The more commercials they see, the more brands they get to know.",
            "B": "The more commercials they see, the more they adore celebrities.",
            "C": "The more television they watch, the fewer conflicts in the family.",
            "D": "The more television they watch, the greater their parents' stress."
        },
        "answer": "D",
        "explanation": "【精析】细节理解题。短文第一句明确指出：“A new study has found a positive correlation between how much television children watch and their parents' stress levels.”孩子看电视越多，父母的压力就越大。因此答案为 D)。"
    },
    10: {
        "prompt": "What are parents advised to do to reduce the impact of TV commercials?",
        "options": {
            "A": "Inform children of the family's financial situation.",
            "B": "Shift children's attention to interesting activities.",
            "C": "Involve children in making purchasing decisions.",
            "D": "Help children understand advertising's intent."
        },
        "answer": "C",
        "explanation": "【精析】细节理解题。研究人员建议父母改变沟通方式：“The researchers suggest that parents seek input from their children on family purchasing decisions.”让孩子参与家庭购物决策（involve children in making purchasing decisions）。因此答案为 C)。"
    },
    11: {
        "prompt": "What makes children particularly vulnerable to TV commercials?",
        "options": {
            "A": "Their limited cognitive ability.",
            "B": "Their strong natural curiosity.",
            "C": "Their admiration for celebrities.",
            "D": "Their lack of social experience."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。短文末尾指出：“Plus, children don't have the cognitive ability to fully understand advertising's intent. That makes them particularly vulnerable to advertisements.”儿童缺乏充分理解广告意图的认知能力，使他们特别容易受到广告影响。因此答案为 A)。"
    },
    12: {
        "prompt": "What baffling phenomenon is discussed in the passage?",
        "options": {
            "A": "Bad guys may do good deeds.",
            "B": "Bad guys may go unpunished.",
            "C": "Good guys may not always cooperate.",
            "D": "Good guys may get unfair treatment."
        },
        "answer": "D",
        "explanation": "【精析】细节理解题。短文中提到令人费解的现象是：“sometimes the good guys also get punished or criticized. Specifically, because they are so good. This seems baffling...”即好人恰恰因为优秀而受到不公正的对待或批评。因此答案为 D)。"
    },
    13: {
        "prompt": "How are we all judged according to the passage?",
        "options": {
            "A": "By what we do.",
            "B": "By fair evaluation.",
            "C": "In comparison with others.",
            "D": "In accordance with set standards."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。短文中明确指出：“After all, we're all judged in comparison with others.”我们所有人都是在与他人的比较中被评判的。因此答案为 C)。"
    },
    14: {
        "prompt": "What can a normal person do when faced with people who perform better?",
        "options": {
            "A": "Learn from them earnestly.",
            "B": "Compete with them actively.",
            "C": "Leave them alone temporarily.",
            "D": "Cooperate with them sincerely."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。短文中提出问题：“When faced with someone better, what can a normal person do? One option is to actively compete.”一种应对方式就是积极地与他们竞争。因此答案为 B)。"
    },
    15: {
        "prompt": "What may discourage people from performing good deeds?",
        "options": {
            "A": "Being dismissed as hypocritical.",
            "B": "Not getting the reward they deserve.",
            "C": "Having to make too many sacrifices.",
            "D": "Being misunderstood by people around."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。短文提到善行常被不作为者贬损为虚伪：“Such good deeds are dismissed as naive or hypocritical... This criticism may ultimately discourage people from doing good deeds.”善举被斥为虚伪会挫伤人们行善的意愿。因此答案为 A)。"
    },
    16: {
        "prompt": "What does the speaker say about most preteen children?",
        "options": {
            "A": "They are increasingly aware of gender differences.",
            "B": "They engage themselves in positive recollection.",
            "C": "They begin to see the importance of friendship.",
            "D": "They make friends with peers of the same sex."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。讲话者提到：“Most preteen children have a best friend who is usually someone of the same sex and similar age.”大多数十一二岁的孩子最好的朋友通常是同性别的同龄人。因此答案为 D)。"
    },
    17: {
        "prompt": "What do most males devote much of their energy to during adolescence?",
        "options": {
            "A": "Competing for position.",
            "B": "Pursuing fashion.",
            "C": "Forging close ties with friends.",
            "D": "Fulfilling family obligations."
        },
        "answer": "A",
        "explanation": "【精析】细节理解题。讲话者指出在青春期：“considerable energy is devoted to competing for position and a definite undercurrent of competition permeates the relationship.”相当多的精力被投入到争夺地位的竞争中。因此答案为 A)。"
    },
    18: {
        "prompt": "What do children do when they reach late adolescence?",
        "options": {
            "A": "They prioritize romance over friendship.",
            "B": "They try to strengthen same-sex friendships.",
            "C": "They begin to take friendship more seriously.",
            "D": "They compete intensely for romantic partners."
        },
        "answer": "A",
        "explanation": "【精析】细节理解题。讲话者指出在青春期后期：“dating and relationships with boys take sharp precedence over sisterhood... dating dilutes the intensity of same-sex friendships for men also.”恋爱关系显著优于同性友谊（prioritize romance over friendship）。因此答案为 A)。"
    },
    19: {
        "prompt": "Why do disabled job applicants feel reluctant to disclose their disability information?",
        "options": {
            "A": "They regard it as a matter of sheer privacy.",
            "B": "They are worried about being turned down.",
            "C": "They fear that their condition will be made widely known.",
            "D": "They are afraid to be discriminated against once recruited."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。讲座中指出：“many candidates fear they wouldn't be considered for a position as a result of disclosing this personal information.”许多残疾求职者担心透露该信息会导致自己直接失去被录用的机会（worried about being turned down）。因此答案为 B)。"
    },
    20: {
        "prompt": "When does the speaker suggest applicants reveal their disability information?",
        "options": {
            "A": "After receiving a job offer.",
            "B": "During a job interview.",
            "C": "When confirming an interview.",
            "D": "Upon completing a cover letter."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。讲座中明确建议：“It's most appropriate to discuss a disability when they reply to confirm an interview.”在回复确认面试时讨论最为适宜。因此答案为 C)。"
    },
    21: {
        "prompt": "What are people advised to do when filling out their job application form?",
        "options": {
            "A": "Describe the true state of their health.",
            "B": "Provide all the information required.",
            "C": "Stress the irrelevance of their disability to the job.",
            "D": "Avoid mentioning the name of their disability."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。讲话者提醒道：“People should avoid sharing the name of their disability or condition.”求职者应当避免直接写明所患残疾的具体名称。因此答案为 D)。"
    },
    22: {
        "prompt": "What did some American researchers find about students' reading comprehension in the presence of background noise?",
        "options": {
            "A": "Their scores were least affected by music with speech.",
            "B": "It was the poorest when there was background speech.",
            "C": "Their scores were most depressed with instrumental music.",
            "D": "It was disrupted by the sound of an air conditioner or fan."
        },
        "answer": "B",
        "explanation": "【精析】细节理解题。美国研究人员的实验发现：“Students' scores were most depressed in the presence of background speech.”在存在背景讲话声时，学生的理解得分下降最为严重，即阅读理解表现最差。因此答案为 B)。"
    },
    23: {
        "prompt": "What do we learn from the British researchers about the degree of interference from background noise?",
        "options": {
            "A": "It has to do with the type and volume of the background noise.",
            "B": "It has to do with short-term memory for listening comprehension.",
            "C": "It depends on the overlap in processing different kinds of information.",
            "D": "It depends on the participants' ability to concentrate on the task at hand."
        },
        "answer": "C",
        "explanation": "【精析】细节理解题。英国研究人员指出：“the degree of interference from background noise depends on the overlap between the processing required on the task and the processing required to screen out the background noise.”干扰程度取决于处理任务与过滤噪音过程之间的认知重叠。因此答案为 C)。"
    },
    24: {
        "prompt": "What is best for students to do when writing essays according to some research?",
        "options": {
            "A": "Keep everything as quiet as possible.",
            "B": "Play nothing but instrumental music.",
            "C": "Use vocal material as little as possible.",
            "D": "Wear a pair of earphones or headphones."
        },
        "answer": "A",
        "explanation": "【精析】细节理解题。讲座中提到：“When students write essays, however, other research has found it is best to reduce all background noise as much as possible.”写论文时最好尽可能消除所有背景噪音，即保持尽可能安静。因此答案为 A)。"
    },
    25: {
        "prompt": "How do people of different personalities react to distractions according to other studies?",
        "options": {
            "A": "Sociable people were immune to all distractions.",
            "B": "Shy quiet people were most adversely impacted.",
            "C": "Less outgoing people were more affected by silence.",
            "D": "Confident people were unaffected by high-arousal music."
        },
        "answer": "B",
        "explanation": "【精析】细节理解题。实验结果表明：“less sociable people were more negatively affected by each of the distractions.”害羞不善交际的人受到各种干扰的负面影响最严重。因此答案为 B)。"
    }
}
