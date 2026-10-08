import json

# Sentences and Questions for 2022-12-set2

SUBPARTS = [
    {
        "id": "2022-12-set2-conv-1",
        "subpart_code": "conv-1",
        "section_id": "2022-12-set2-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 1 · 幸福追求与金钱消费观的反思探讨",
        "topic_zh": "幸福追求与金钱消费观的反思探讨",
        "question_range": "Q1 ~ Q4",
        "questions": [1, 2, 3, 4],
        "sp_start": 34.0,
        "sp_end": 166.0,
        "sentences": [
            ("M", "Welcome to the Book Club.", "欢迎收听《读书俱乐部》节目。"),
            ("M", "Today's guest is Susan Lane, the author of a new book on personal finances that has already sold half a million copies.", "今天的嘉宾是苏珊·莱恩，她的一本关于个人理财的新书目前已售出50万册。"),
            ("M", "Hi, Susan, your book is extremely successful.", "嗨，苏珊，你的书非常成功。"),
            ("M", "Why do you think that is?", "你认为这是为什么呢？"),
            ("W", "I think that's because of my message, which is making happiness a priority over money.", "我认为这是因为我在书中传达的信息，那就是把幸福置于金钱之上。"),
            ("W", "So many of us in my generation have spent decades trying to earn more money, just to consume more, but it made us more miserable.", "我们这一代许多人花了数十年拼命赚钱，仅仅是为了消费更多，但这反而让我们更加痛苦。"),
            ("M", "You yourself were once caught in that cycle, working for two decades as an executive and earning a high salary, but still accumulating debt.", "你自己也曾陷入过这种恶性循环中，做了二十年高管，收入丰厚，但依然债台高筑。"),
            ("W", "I most certainly was.", "确实是这样。"),
            ("W", "I earned millions, but by the time I quit my job four years ago to become a writer, I owed over $30,000.", "我赚了数百万，但四年前我辞掉工作成为作家时，却欠下了三万多美元的债务。"),
            ("M", "So how did you escape that pattern?", "那么你是如何摆脱这种生活模式的呢？"),
            ("M", "And what would you advise other people to do?", "你对其他人又有什么建议呢？"),
            ("W", "The first change is in what we value.", "首先是要改变我们的价值观。"),
            ("W", "We need to emphasize things that actually make us happy, like relationships, the environment or even our hobbies.", "我们需要看重真正能给我们带来快乐的事物，比如人际关系、周围环境甚至是个人爱好。"),
            ("W", "Once we make the right things our priority, our goals will change and so will our financial behavior.", "一旦我们把正确的事情放在第一位，我们的人生目标就会随之改变，我们的财务行为也是如此。"),
            ("M", "How does that translate into practical action?", "那在实际行动中具体该如何体现呢？"),
            ("M", "Can you give our audience examples of what you are talking about on an everyday basis?", "你能给我们的听众举几个日常生活的例子来说明你的观点吗？"),
            ("W", "The major areas for action are usually housing, food and transportation.", "付诸行动的主要领域通常是居住、饮食和出行交通。"),
            ("W", "So people might share a home with friends instead of living on their own, bring lunch from home instead of going to restaurants, and use public transport instead of owning a car.", "因此，大家可以和朋友合住而不是独自租房，自己从家带午饭而不是下馆子，乘坐公共交通而不是自己买车。"),
            ("M", "Those sound like major sacrifices.", "这些听起来像是重大的牺牲啊。"),
            ("M", "I could never share my home.", "我绝对无法接受和别人合住。"),
            ("M", "I need my own space.", "我需要属于自己的私人空间。"),
            ("W", "But they aren't sacrifices.", "但这些并不是牺牲。"),
            ("W", "When people change their values, their desires change.", "当人们的价值观改变时，他们的欲望也会改变。"),
            ("W", "So in the example of housing, if we value relationships, sharing a home isn't depriving ourselves of space, but giving us an opportunity to spend more time with our loved ones.", "所以在住房这个例子中，如果我们珍视人际关系，合住就不是剥夺个人空间，而是给我们提供了与所爱之人共度更多时光的机会。"),
            ("M", "Indeed it is.", "确实如此。")
        ]
    },
    {
        "id": "2022-12-set2-conv-2",
        "subpart_code": "conv-2",
        "section_id": "2022-12-set2-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 2 · 艺术画作鉴赏与画家个人风格评价",
        "topic_zh": "艺术画作鉴赏与画家个人风格评价",
        "question_range": "Q5 ~ Q8",
        "questions": [5, 6, 7, 8],
        "sp_start": 238.0,
        "sp_end": 355.0,
        "sentences": [
            ("W", "Thank you for inviting me to the gallery, Christopher.", "克里斯托弗，谢谢你邀请我来画廊参观。"),
            ("W", "I haven't visited here since your predecessor's retirement function.", "自从你前任的退休欢送会之后，我就再没来过这里了。"),
            ("M", "Would you like to see the newest additions to our collection first, Catherine?", "凯瑟琳，你想先看看我们馆藏的最新画作吗？"),
            ("W", "Are those the landscapes by Daniel Gregory?", "那些就是丹尼尔·格雷戈里的风景画吗？"),
            ("W", "I absolutely adore her work.", "我非常欣赏她的作品。"),
            ("M", "This first piece was a gift to the gallery from the artist herself, and it's quite exquisite.", "这第一幅作品是艺术家本人赠送给画廊的礼物，非常精致典雅。"),
            ("W", "I love how she depicts the barren landscape.", "我太喜欢她对荒凉荒原景致的描绘了。"),
            ("W", "The colors complement each other perfectly.", "色彩搭配相得益彰，堪称完美。"),
            ("M", "You can sense the desolation in the picture.", "你能从画中真切感受到那种孤寂荒凉感。"),
            ("M", "This piece was inspired by Gregory's recent trek in the Gobi Desert.", "这幅作品的灵感源自格雷戈里最近在戈壁沙漠的徒步之旅。"),
            ("W", "And how did you obtain her other piece, over here?", "那你们是怎么拿到她挂在这边的另一幅作品的呢？"),
            ("M", "It was purchased at auction by an anonymous collector who lent it to the gallery for display.", "这是一位匿名收藏家在拍卖会上购得的，随后借给画廊对外展出。"),
            ("M", "This composition is one of her most acclaimed paintings.", "这幅画作是她最受赞誉的代表作之一。"),
            ("W", "It must have cost that collector a small fortune to purchase this.", "那位收藏家买下这幅画肯定花了一大笔钱。"),
            ("M", "Obviously.", "那是显而易见的。"),
            ("M", "I can't disclose the exact amount he paid, but it was substantial.", "我不能透露他支付的具体金额，但绝对是一笔巨款。"),
            ("W", "There's so much detail in this painting.", "这幅画的细节刻画太丰富了。"),
            ("W", "I feel like I can really immerse myself in the scene.", "我感觉自己仿佛真的身临其境、完全沉浸在这画卷之中。"),
            ("W", "I particularly like the symmetry created by the reflection of the mountain in the lake.", "我尤其喜欢山峦倒映在湖水中所勾勒出的对称之美。"),
            ("M", "This particular piece was the one that was nominated for a Gateway Award.", "这幅特殊的作品曾获得过盖特威艺术奖的提名。"),
            ("M", "I was lucky enough to attend the awards ceremony as Gregory's guest.", "我非常荣幸能作为格雷戈里的特邀嘉宾出席了颁奖典礼。"),
            ("W", "So you know her personally.", "这么说你跟她私交不错啊。"),
            ("W", "I assume she is an eccentric artist.", "我想她一定是一位性格古怪特立独行的艺术家吧。"),
            ("M", "Quite the opposite.", "恰恰相反。"),
            ("M", "In fact, she's not at all eccentric.", "事实上，她一点儿也不古怪。"),
            ("M", "I would say she's one of the most easygoing and intelligent people I know.", "在我看来，她是我认识的最随和、最聪慧的人之一。"),
            ("W", "I'd love to be able to meet her.", "我真希望能有机会见见她。"),
            ("W", "There are so many questions I'd like to ask.", "我有好多问题想当面向她请教。"),
            ("M", "What a coincidence! I'm meeting her for dinner tonight.", "真巧！我今晚正要和她一起吃晚餐呢。"),
            ("M", "Would you like to come along?", "你想一起来吗？"),
            ("W", "I'd love to.", "太好了，我很乐意去。"),
            ("W", "Thank you.", "非常感谢你。")
        ]
    },
    {
        "id": "2022-12-set2-pass-1",
        "subpart_code": "pass-1",
        "section_id": "2022-12-set2-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 1 · 宽恕的力量与受害者创伤心理治愈",
        "topic_zh": "宽恕的力量与受害者创伤心理治愈",
        "question_range": "Q9 ~ Q11",
        "questions": [9, 10, 11],
        "sp_start": 461.0,
        "sp_end": 577.0,
        "sentences": [
            ("M", "Forgiveness is the release of resentment or anger.", "宽恕是对怨恨或愤怒的释怀。"),
            ("M", "Forgiveness doesn't mean reconciliation.", "宽恕并不等同于双方和解。"),
            ("M", "We don't have to return to the same relationship, nor do we have to accept the same harmful behaviors from an offender.", "我们不必回到原有的关系中，也不必继续忍受施害者同样的伤害性行为。"),
            ("M", "Forgiveness is vitally important for the mental health of certain victims.", "宽恕对于某些受害者的心理健康至关重要。"),
            ("M", "It propels people forward rather than keeping them emotionally engaged in an injustice or trauma.", "它促使人们向前看，而不是让他们在情感上深陷于不公或心理创伤之中。"),
            ("M", "Carrying the hurt or anger of an offense leads the body to release stress chemicals.", "背负冒犯所带来的伤害或怒气，会导致人体释放应激化学物质。"),
            ("M", "Eliminating the perpetual flow of those chemicals may also explain why forgiveness provides physical health benefits.", "消除这些应激物质的持续流动，或许也解释了为何宽恕能带来身体健康益处。"),
            ("M", "There are scenarios in which forgiveness is not the best course.", "也有一些情况下，宽恕并非最佳途径。"),
            ("M", "Sometimes the victim becomes more empowered when they give themselves permission not to forgive.", "有时，当受害者允许自己不去宽恕时，反而能获得更多掌控自我的力量。"),
            ("M", "Forgiveness can be challenging.", "宽恕有时是一项艰难的挑战。"),
            ("M", "This is especially true when the offending party offers an insincere apology, or maybe they haven't offered anything at all.", "当冒犯的一方道歉敷衍毫无诚意，或者根本没有任何表示时，尤其如此。"),
            ("M", "However, it's often the healthiest path forward.", "然而，这往往是向前迈进最健康的方式。"),
            ("M", "It's important to cultivate forgiveness by developing compassion for the offender.", "通过对冒犯者建立同理心来培养宽恕，这一点十分重要。"),
            ("M", "Reflect on whether the act was due to malicious intent or whether it was caused by challenging circumstances in the offender's life.", "反思这种行为究竟是出于恶意，还是源于冒犯者自身生活中的艰难处境所致。"),
            ("M", "What about forgiving ourselves?", "那么又该如何原谅我们自己呢？"),
            ("M", "We sometimes need to take responsibility for mistakes, but intense guilt and shame aren't a desirable outcome in the long run.", "我们有时需要为错误承担责任，但从长远来看，强烈的内疚和羞耻感并不是一种理想的状态。"),
            ("M", "Forgiving yourself may seem like an ambiguous process.", "原谅自己似乎是一个模糊不清的过程。"),
            ("M", "You can begin by acknowledging that you are at fault, take responsibility for the hurt you caused, then reflect on why the event occurred.", "你可以先从承认自己有错、为所造成的伤害承担责任开始，然后反思事情发生的根源。"),
            ("M", "Draw the lessons you learned and try to avoid committing a similar offense in the future.", "从中吸取教训，并在未来的日子里尽力避免重蹈覆辙。")
        ]
    },
    {
        "id": "2022-12-set2-pass-2",
        "subpart_code": "pass-2",
        "section_id": "2022-12-set2-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 2 · 格拉斯哥地下铁历史演进与现代化改造",
        "topic_zh": "格拉斯哥地下铁历史演进与现代化改造",
        "question_range": "Q12 ~ Q15",
        "questions": [12, 13, 14, 15],
        "sp_start": 636.0,
        "sp_end": 760.0,
        "sentences": [
            ("W", "The Glasgow subway first opened in 1896 as a cable-hauled system.", "格拉斯哥地铁于1896年首次开通运营，当时采用钢缆牵引系统。"),
            ("W", "It is generally recognized as the world's third underground railway, after London and Budapest.", "它被公认为仅次于伦敦和布达佩斯的世界第三古老的地下铁道。"),
            ("W", "In its long history, it has never been expanded, remaining as a single loop line with a mere 15 stations.", "在其悠久的历史中，它从未进行过线路延伸，始终保持着一条仅有15座车站的单环线。"),
            ("W", "At its peak, it served the shipyard workers on the south side of the city.", "在其鼎盛时期，它主要为该市南区的造船厂工人们提供通勤服务。"),
            ("W", "In the 1960s, there was a decline in the shipbuilding industry, and the popularity of private transport grew.", "20世纪60年代，造船业出现衰退，而私家车出行的普及度不断提高。"),
            ("W", "As a result, the subway saw a rapid decline in ridership.", "结果，该地铁的客流量出现了急剧下滑。"),
            ("W", "It ran with little further change until 1977 when its new operators closed it for major modernization investment.", "此后地铁几乎没有变动地维持运转，直到1977年，新运营方因进行大规模现代化改造投资而将其暂时关闭。"),
            ("W", "Carriages were replaced, ventilation was improved, and the main depot was also renovated and fitted with connecting tracks to replace the outdated crane transfer mechanism.", "车厢进行了全面换新，通风系统得到改善，主车辆段也进行了翻新，并加铺了联络轨道以取代过时的起重机调车机制。"),
            ("W", "The subway in its present form reopened for operation in April 1980.", "现行形态的地铁于1980年4月重新开通投入运营。"),
            ("W", "Since its relaunch, the subway has seen a revival in its fortunes.", "自重开以来，该地铁迎来了复兴与转机。"),
            ("W", "It serves as a viable alternative to other forms of transport and has gone a long way to alleviate traffic jams in the city center.", "它作为其他出行方式的可行替代方案，对缓解市中心的交通拥堵起到了至关重要的作用。"),
            ("W", "In 1996, the system reached an important milestone: 100 years.", "1996年，该系统迎来了重要的百年里程碑。"),
            ("W", "To commemorate this special event, the color scheme of the train carriages was updated.", "为纪念这一特殊时刻，列车车厢的涂装配色方案进行了焕新。"),
            ("W", "Recently, high-tech systems such as smart card ticketing machines and smart gates are used across all subway stations.", "最近，所有地铁站都引入了智能卡售票机和智能检票闸机等高科技系统。"),
            ("W", "The smart card provides more convenient travel and passengers simply top up their cards and tap them to get in and out the subway.", "智能卡带来了更为便捷的出行体验，乘客只需充值并刷卡即可进出地铁站。"),
            ("W", "Since its launch, the technology has been adopted by more than 100,000 subway customers.", "自推出以来，这项技术已拥有超过10万名地铁乘客使用。")
        ]
    },
    {
        "id": "2022-12-set2-rec-1",
        "subpart_code": "rec-1",
        "section_id": "2022-12-set2-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 1 · 城市野生棕熊习性变化与人熊安全共处",
        "topic_zh": "城市野生棕熊习性变化与人熊安全共处",
        "question_range": "Q16 ~ Q18",
        "questions": [16, 17, 18],
        "sp_start": 867.0,
        "sp_end": 1034.0,
        "sentences": [
            ("M", "If you visit the Great Smoky Mountains National Park, chances are you will remember the roadside or campground bears above all else.", "如果你去大雾山国家公园游玩，最让你印象深刻的极有可能是路边或营地里的熊。"),
            ("M", "Bears are the most popular animals in a number of our national parks.", "在我们的许多国家公园中，熊都是最受欢迎的动物。"),
            ("M", "In these mountains, where the population of bears runs into the hundreds, opportunities to observe these large wild animals are plentiful during the summer.", "在这片山区，熊的种群数量多达数百只，在夏季观察这些大型野生动物的机会非常多。"),
            ("M", "Since national parks are wildlife sanctuaries where no disturbance of the native animals is allowed, years of protection have served to break down the wild bears' fear of humans.", "由于国家公园属于野生动物保护区，严禁干扰本土动物，长年累月的保护逐渐消除了野生熊对人类的恐惧。"),
            ("M", "Now, instead of depending on their own resources for a living, many bears patrol park roads and campgrounds.", "如今，许多熊不再依靠大自然自谋生路，而是在公园道路和露营地周围四处巡游。"),
            ("M", "They give the garbage cans a frequent going over.", "它们经常把垃圾桶彻底翻个底朝天。"),
            ("M", "An occasional offer of food from a park visitor, an illegal and dangerous practice, makes beggars of them.", "公园游客偶尔投喂食物（这是一种违法且极其危险的行为），使它们变成了乞食者。"),
            ("M", "Bears are very often hungry and since they will feed on almost any kind of plant or animal, garbage is quite acceptable.", "熊经常处于饥饿状态，既然它们几乎能吃任何动植物，那么垃圾自然也来者不拒。"),
            ("M", "Feeding them, however, represents misguided kindness because the bears come to expect such generosity from everyone and consequently, trouble could lie ahead.", "然而，投喂它们代表着一种盲目好心，因为熊会逐渐期望每个人都如此慷慨，从而埋下严重的祸患。"),
            ("M", "Park rules prohibit the feeding of bears.", "公园规章严格禁止向熊投喂食物。"),
            ("M", "Violators are arrested.", "违规者将被依法逮捕。"),
            ("M", "Every year, doctors who have offices near the park treat a number of cases of bear bites and bear scratches.", "每年，公园附近的执业医生都要救治多起被熊咬伤和抓伤的病例。"),
            ("M", "Some of the accidents have come about in strange ways.", "其中一些意外事故的发生方式令人匪夷所思。"),
            ("M", "One man was in the process of feeding two small cubs, when the mother bear appeared and insisted upon having some of the food.", "一名男子正在给两只幼崽喂食，这时母熊突然出现并执意要抢食物。"),
            ("M", "Shoving the big bear aside with one hand, the man continued feeding the cubs when suddenly he was struck a fierce blow in the face.", "该男子单手推开大熊继续喂幼崽，结果面部突然遭到重重的一记猛击。"),
            ("M", "A bear, prompted by the food that a lady kept offering to him, entered the car where the generous person was sitting.", "还有一只熊受一位女士不断喂食的诱惑，直接钻进了这位“慷慨人士”所坐的车厢内。"),
            ("M", "Her efforts to push the bear out of the car resulted in injuries.", "她试图把熊推出车外，结果导致自己受伤。"),
            ("M", "A man required medical attention after he applied a lighted cigarette to a bear's nose.", "另一名男子在用点燃的香烟去烫熊的鼻子后，不得不接受医疗救治。"),
            ("M", "Another man tried to boost a bear into the front seat of his car so that he might take a picture of a bear sitting beside his wife who was behind the wheel.", "还有一名男子试图把熊硬塞进汽车前排，以便拍摄一张熊坐在方向盘旁驾驶座妻子身边的合影。"),
            ("M", "Because bears prefer roads and campgrounds, the possibility of a hiker meeting up with a bear along park trails is small, but there's always that chance, for a bear seems to know if you are carrying a lunch or a candy bar.", "因为熊更喜欢道路和露营地，徒步旅行者在公园山道上遇到熊的几率较小，但危险始终存在，因为熊似乎能敏锐察觉你是否带了午餐或巧克力糖棒。"),
            ("M", "He may even insist on taking it.", "它甚至可能会强行据为己有。")
        ]
    },
    {
        "id": "2022-12-set2-rec-2",
        "subpart_code": "rec-2",
        "section_id": "2022-12-set2-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 2 · 偏见的本质、社会危害与成因剖析",
        "topic_zh": "偏见的本质、社会危害与成因剖析",
        "question_range": "Q19 ~ Q21",
        "questions": [19, 20, 21],
        "sp_start": 1102.0,
        "sp_end": 1284.0,
        "sentences": [
            ("M", "Why do we form opinions or attitudes about someone or something without really knowing much about them?", "为什么我们在并不真正了解某人或某事的情况下，就会对其产生看法或态度？"),
            ("M", "Just hearing something good or bad about a person, a place or thing can influence our opinions positively or negatively.", "仅凭道听途说关于某人、某地或某事的优点或坏处，就会对我们的观点产生正面或负面的影响。"),
            ("M", "But letting the opinions of another person determine what our opinions will be is dangerous.", "但是，任凭他人的观点来主导我们自己的判断是十分危险的。"),
            ("M", "Forming opinions about someone or something before really knowing them well is called prejudice.", "在真正充分了解某人或某事之前就先入为主地下定论，这被称为偏见。"),
            ("M", "'Pre-' means before and '-judice' refers to judgment.", "前缀“Pre-”意为“在……之前”，而“-judice”指的是“评判”。"),
            ("M", "Hence, prejudice means to judge before having adequate knowledge.", "因此，偏见的意思就是在掌握充分认识之前妄作评判。"),
            ("M", "We can be prejudiced toward or against someone or something.", "我们可以对某人或某事抱有偏袒或排斥的偏见。"),
            ("M", "In either case, we are only allowing ourselves to see half of the picture.", "无论哪种情况，我们都仅仅让自己看到事情的一面。"),
            ("M", "Very few people or things in this world are all good or all bad.", "在这个世界上，极少有人或事是十全十美或一无是处的。"),
            ("M", "Prejudiced attitudes are usually based on myths, half truths or incorrect information, and they are dangerous because they can keep us from learning the truth about someone or something.", "偏见的态度通常建立在虚构传言、半真半假的表象或错误信息之上，它们极其危险，因为会阻碍我们了解某人或某事的真相。"),
            ("M", "People form prejudices against others for many reasons: differences in their race, religion, gender or occupation.", "人们对他人产生偏见的原因众多：种族、宗教信仰、性别或职业的差异。"),
            ("M", "Prejudices keep people apart.", "偏见使人与人之间产生隔阂与疏离。"),
            ("M", "They keep us from really knowing and understanding each other.", "偏见阻碍我们彼此真正深入地认识和理解。"),
            ("M", "We should feel proud of who we are and the group of people we represent.", "我们应当为自己的身份以及我们所代表的群体感到自豪。"),
            ("M", "If feelings of pride begin to turn to feelings of superiority when we think that our group or our beliefs are better than those around us, however, then we begin to develop prejudiced attitudes that can be harmful.", "然而，当我们认为自己的群体或信仰优于身边其他人，从而使自豪感演变为优越感时，我们就会开始滋生出有害的偏见态度。"),
            ("M", "For example, the prejudiced attitudes of one group may keep another group from attending certain schools, from living in any neighborhood they want, or from getting a job or a promotion.", "例如，某个群体的偏见态度可能会阻碍另一个群体进入特定学校就读、随心所欲定居心仪社区，或是获得工作与晋升机会。"),
            ("M", "Extreme feelings of prejudice have caused the deaths of innocent people.", "极端的偏见情绪甚至曾经导致无辜群众的丧命。"),
            ("M", "We are responsible for our own thoughts and opinions.", "我们必须对自己的思想和观点负责。"),
            ("M", "When we let someone else tell us what to think about someone or something, we are giving up some control of our own lives.", "当我们任凭他人告知该如何评价某人或某事时，我们便放弃了对自身生活的部分主导权。"),
            ("M", "Before you form an attitude or opinion, find out for yourself about the person or the thing in question.", "在形成某种态度或看法之前，请亲自去探究了解当事的人或事。"),
            ("M", "Sometimes we don't realize that we hold prejudiced attitudes toward or against someone or something.", "有时候我们甚至意识不到自己对某人或某事抱有偏见。"),
            ("M", "We need to carefully examine our lives and our fears, and to ask ourselves whether our attitudes come from our personal knowledge and experience or from rumors and fear of the unknown.", "我们需要审视自己的生活与恐惧，叩问内心：我们的态度究竟是源于亲身认知与经验，还是出自谣言以及对未知的恐惧。"),
            ("M", "The good news about prejudice is that we are not born with it.", "关于偏见，好消息是我们并非生来就带有偏见。"),
            ("M", "Prejudiced attitudes and opinions develop over time.", "偏见的态度和观点是随着时间逐渐形成的。"),
            ("M", "But with education and knowledge, we can replace our prejudices with cooperation and understanding.", "但通过教育和知识，我们可以用合作与理解来消除和替代偏见。")
        ]
    },
    {
        "id": "2022-12-set2-rec-3",
        "subpart_code": "rec-3",
        "section_id": "2022-12-set2-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 3 · 越战退伍老兵的高中教学感悟与成长启示",
        "topic_zh": "越战退伍老兵的高中教学感悟与成长启示",
        "question_range": "Q22 ~ Q25",
        "questions": [22, 23, 24, 25],
        "sp_start": 1340.5,
        "sp_end": 1502.0,
        "sentences": [
            ("M", "When I started high school, it was a shock.", "当我刚上高中时，内心受到了极大的震撼。"),
            ("M", "I had spent eight years fighting my way to be the most popular kid in the Catholic school student body.", "我花了八年时间打拼，才成为天主教学校里最受欢迎的学生。"),
            ("M", "I had been a big, tough 8th grader and suddenly I was a lonely 9th grader bullied by the big, tough 12th grade seniors who ran the high school.", "我本是八年级里高大威猛的风云人物，突然间却变成了孤僻的九年级新生，遭受统治高中的高年级十二年级老生们的欺凌。"),
            ("M", "I realized then that it's nice to strive for something, but that you also have to enjoy the moment you're in and be happy where you are.", "那时我领悟到：为目标奋斗固然美好，但也必须懂得享受当下，在所处的境遇中知足常乐。"),
            ("M", "Rock and roll had always been an important part of my life.", "摇滚乐一直是我生命中不可或缺的一部分。"),
            ("M", "I remember my friends and I used to drive around until the late hours of the nights listening to the music of Rock and Roll Legends.", "我记得我和朋友们常常驾车兜风到深夜，一路聆听摇滚传奇乐章。"),
            ("M", "During those teenage years, I built friendships that I thought would last a lifetime.", "在那些青春韶华里，我建立起了自以为能天长地久的深厚友谊。"),
            ("M", "Most people that age think the same thing, but people drift apart.", "处于那个年纪的人大多也这样认为，但人与人之间终究会渐行渐远。"),
            ("M", "Jobs, families and tragedies separate people from those lasting friendships.", "工作、家庭以及生活中的变故，往往会冲散那些原本以为长久的友情。"),
            ("M", "The tragedy that separated me from my friends forever was the Vietnam war.", "彻底将我与朋友们永远分隔开的悲剧，是越南战争。"),
            ("M", "A year after I graduated from high school, I left for Vietnam.", "高中毕业一年后，我便奔赴越南战场。"),
            ("M", "I came back, burned out, and tired, as though I had lived 10 lifetimes in the short span of 14 months, the 14 months I was in the war.", "我回国时身心俱疲、心力交瘁，仿佛在参战的短短14个月里耗尽了10辈子的沧桑。"),
            ("M", "I couldn't relate to the friends I had had in high school.", "我再也无法与高中时代的朋友们产生共鸣了。"),
            ("M", "They still seemed childish, concerned with childish things that weren't important to me.", "他们看起来依然稚气未脱，成天操心着在我看来微不足道的幼稚琐事。"),
            ("M", "I was still trying to cope with the death, destruction and evil I had seen in Vietnam.", "而我当时仍在努力排解自己在越南亲历的死亡、毁灭与罪恶所带来的创伤。"),
            ("M", "I felt like we had done terrible things to innocent people there and in turn, I had seen terrible things done to my friends.", "我总觉得我们在那里对无辜者犯下了可怕的罪行，反过来，我也亲眼目睹了发生在朋友身上的惨剧。"),
            ("M", "I withdrew from my friends and started college.", "我主动疏远了朋友，进入大学读书。"),
            ("M", "Then I quit college and took many different jobs.", "后来我从大学退学，尝试了各种各样不同的工作。"),
            ("M", "I spent a lot of my time and money on alcohol and other drugs.", "我把大把的时间和金钱挥霍在酒精和其他麻醉药物上。"),
            ("M", "Finally, in an effort to get my life going in the right direction again, I sold everything and took what little money I had and bought myself an airplane ticket to Israel.", "最终，为了让生活重回正轨，我变卖了全部家当，用仅有的一点积蓄给自己买了一张飞往以色列的机票。"),
            ("M", "I went there to study history.", "我去那里攻读历史学。"),
            ("M", "While studying at Haifa University, I met my wife, who was also an American student.", "在海法大学求学期间，我结识了我的妻子，她当时也是一名美国留学生。"),
            ("M", "I now teach in a high school back in America.", "如今我回到美国，在一所高中教书。"),
            ("M", "I look at my students and see them struggling with many of the very things I struggled with many years ago.", "看着讲台下的学生，我发现他们正在经历许多我多年前曾经挣扎面对的困扰。"),
            ("M", "As a teacher, I try to help them over the rough spots as best I can.", "作为一名教师，我竭尽全力帮助他们渡过人生中的艰难时刻。")
        ]
    }
]

QUESTIONS = {
    1: {
        "prompt": "What message does the woman convey in her book?",
        "options": {
            "A": "Prioritizing happiness over money.",
            "B": "Joining the club to get her new book.",
            "C": "Managing one's personal finances wisely.",
            "D": "Consuming more only when earning more."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。当男士问女士她认为是什么使得她的书那么成功时，女士在对话开头回答说，这是因为她在书中传达的信息，即将幸福置于金钱之上（making happiness a priority over money）。选项A中用名词短语 Prioritizing happiness over money 对应原文，因此答案为 A)。"
    },
    2: {
        "prompt": "What do we learn about the woman before she became a writer?",
        "options": {
            "A": "She was in debt.",
            "B": "She was a financial adviser.",
            "C": "She earned $ 30,000 a month.",
            "D": "She enjoyed a happy life."
        },
        "answer": "A",
        "explanation": "【精析】细节推断题。男士提到女士此前当了二十年高管，收入虽高却债台高筑，女士证实了这一点，并具体说明四年前辞职成为作家时，她欠下了3万多美元的债务（by the time I quit my job four years ago to become a writer, I owed over $30,000）。由此可知女士在成为作家之前身负债务。因此答案为 A)。"
    },
    3: {
        "prompt": "What does the woman say about one's financial behavior?",
        "options": {
            "A": "It reflects one's earning power.",
            "B": "It varies with one's environment.",
            "C": "It mirrors one's sense of wellbeing.",
            "D": "It changes with one's goals in life."
        },
        "answer": "D",
        "explanation": "【精析】细节推断题。女士指出，我们需要重视真正让自己快乐的事物，一旦我们把正确的事情置于首位，我们的人生目标就会改变，我们的财务行为也会随之改变（Once we make the right things our priority, our goals will change and so will our financial behavior）。因此财务行为会随着生活目标的变化而改变。因此答案为 D)。"
    },
    4: {
        "prompt": "What does the man say about sharing a home?",
        "options": {
            "A": "It would give him more time to be with his loved ones.",
            "B": "It would be good for those who value relationships.",
            "C": "It would mean major sacrifices for him.",
            "D": "It would deprive him of his individuality."
        },
        "answer": "C",
        "explanation": "【精析】细节推断题。在女士列举生活方式的转变（如与朋友合住）后，男士立刻表示：“Those sound like major sacrifices. I could never share my home. I need my own space.”即对他而言合住意味着重大牺牲。因此答案为 C)。"
    },
    5: {
        "prompt": "What do we learn about one of the newest additions to the gallery's collection?",
        "options": {
            "A": "It was the artist's first landscape.",
            "B": "It was a painting by Christopher.",
            "C": "It was donated by the artist herself.",
            "D": "It was displayed at a retirement party."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。男士向女士介绍画廊最新藏品时提到，第一幅作品是艺术家本人赠送给画廊的礼物（This first piece was a gift to the gallery from the artist herself）。选项C中 donated by the artist herself 属于同义转述。因此答案为 C)。"
    },
    6: {
        "prompt": "What does the man say about one of the most acclaimed paintings by Daniel Gregory?",
        "options": {
            "A": "It was the painting that instantly made her rich.",
            "B": "It has cost him a lot of money to purchase it.",
            "C": "It was recently purchased by the gallery.",
            "D": "It is owned by an anonymous collector."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。男士提到该画家的另一幅最受赞誉的作品时说明：“It was purchased at auction by an anonymous collector who lent it to the gallery for display.”即该画由一位匿名收藏家购买并借给画廊展出。因此答案为 D)。"
    },
    7: {
        "prompt": "Why does the woman say she can feel immersed in the scene in the painting?",
        "options": {
            "A": "It reflects her emotions.",
            "B": "It contains ample details.",
            "C": "It appears perfectly symmetrical.",
            "D": "It depicts the beauty of desolation."
        },
        "answer": "B",
        "explanation": "【精析】细节推断题。女士欣赏画作时感叹：“There's so much detail in this painting. I feel like I can really immerse myself in the scene.”正是因为画中有极其丰富的细节，才让她感到身临其境。因此答案为 B)。"
    },
    8: {
        "prompt": "How does the man describe Daniel Gregory?",
        "options": {
            "A": "She is eccentric like any other artist.",
            "B": "She is a very nice and intelligent artist.",
            "C": "She is as lucky as any acclaimed artist.",
            "D": "She is one of the most productive artists."
        },
        "answer": "B",
        "explanation": "【精析】细节推断题。女士猜测格雷戈里是一位性格古怪的艺术家，男士反驳说她完全不古怪，并评价道：“I would say she's one of the most easygoing and intelligent people I know.”选项B中 nice and intelligent 对应 easygoing and intelligent。因此答案为 B)。"
    },
    9: {
        "prompt": "What does the passage say about forgiveness?",
        "options": {
            "A": "It is vital to one's mental health.",
            "B": "It leads to reconciliation and peace.",
            "C": "It promotes interpersonal relationship.",
            "D": "It keeps one from traumatic experience."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。短文中明确指出：“Forgiveness is vitally important for the mental health of certain victims.”即宽恕对于受害者的心理健康至关重要。因此答案为 A)。"
    },
    10: {
        "prompt": "When is forgiveness especially challenging?",
        "options": {
            "A": "When the offender has power over the victim.",
            "B": "When the offender is not willing to apologize.",
            "C": "When the offender is not duly penalized.",
            "D": "When the offender adds insult to injury."
        },
        "answer": "B",
        "explanation": "【精析】细节推断题。短文中提到：“Forgiveness can be challenging. This is especially true when the offending party offers an insincere apology, or maybe they haven't offered anything at all.”即当冒犯者道歉毫无诚意或根本不作道歉时，宽恕尤为困难。因此答案为 B)。"
    },
    11: {
        "prompt": "What should one do in order to forgive the offender?",
        "options": {
            "A": "Talk with the offender calmly.",
            "B": "Accept the offender's apology.",
            "C": "Find out why he committed the offense.",
            "D": "Determine how serious the offense was."
        },
        "answer": "C",
        "explanation": "【精析】细节推断题。短文中指出：“Reflect on whether the act was due to malicious intent or whether it was caused by challenging circumstances in the offender's life.”即反思冒犯行为背后的原因究竟是恶意还是由于生活艰难所致。因此答案为 C)。"
    },
    12: {
        "prompt": "What does the passage say about the Glasgow subway in the 1960s?",
        "options": {
            "A": "The number of passengers dropped sharply.",
            "B": "It served more and more commuters.",
            "C": "The number of stations increased to 50.",
            "D": "It became the longest in the United Kingdom."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。短文中提到，20世纪60年代由于造船业衰退和私家车普及，“As a result, the subway saw a rapid decline in ridership.”乘客数量急剧下降。选项A以 passengers dropped sharply 对应 rapid decline in ridership。因此答案为 A)。"
    },
    13: {
        "prompt": "Why was the Glasgow subway closed in 1977?",
        "options": {
            "A": "To increase capacity to meet growing needs.",
            "B": "To make way for other means of transport.",
            "C": "To have its systems modernised.",
            "D": "To avoid further financial losses."
        },
        "answer": "C",
        "explanation": "【精析】细节推断题。短文中指出：“...until 1977 when its new operators closed it for major modernization investment.”新运营商关闭它是为了进行大规模现代化改造升级。因此答案为 C)。"
    },
    14: {
        "prompt": "Why does the Glasgow subway remain important today?",
        "options": {
            "A": "It is generally recognised as a world heritage site.",
            "B": "It is the fastest way to reach the city's south side.",
            "C": "It constitutes a source of revenue for the city.",
            "D": "It helps reduce traffic jams in the city centre."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。短文提到，重新开通后的地铁“has gone a long way to alleviate traffic jams in the city center.”大大缓解了市中心交通拥堵。因此答案为 D)。"
    },
    15: {
        "prompt": "What does the passage say about all subway stations in Glasgow nowadays?",
        "options": {
            "A": "They are usually crowded.",
            "B": "They use high-tech systems.",
            "C": "They accept smartcards only.",
            "D": "They are colourfully decorated."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。短文末尾提到：“Recently, high-tech systems such as smart card ticketing machines and smart gates are used across all subway stations.”即所有车站都使用了高科技系统。因此答案为 B)。"
    },
    16: {
        "prompt": "What does the speaker say about the bears in national parks now?",
        "options": {
            "A": "They are quite friendly to humans.",
            "B": "They are shrinking in numbers.",
            "C": "They are unafraid of humans.",
            "D": "They are especially fond of garbage."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。讲话者提到，由于国家公园是野生动物保护区，禁止骚扰本土动物，“years of protection have served to break down the wild bears' fear of humans.”长年的保护消除了野生熊对人类的恐惧。选项C中 unafraid of humans 对应 break down fear of humans。因此答案为 C)。"
    },
    17: {
        "prompt": "What does the speaker say about visitors feeding bears in national parks?",
        "options": {
            "A": "It is strictly forbidden.",
            "B": "It is an uncommon sight.",
            "C": "It is a gesture of human generosity.",
            "D": "It is allowed only in certain areas."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。讲话者明确指出：“Park rules prohibit the feeding of bears. Violators are arrested.”公园严格禁止投喂熊，违者会被逮捕。因此投喂是严格禁止的。因此答案为 A)。"
    },
    18: {
        "prompt": "What is the speaker's advice to people who carry some food while hiking on a park trail?",
        "options": {
            "A": "Share their food with the bear they see.",
            "B": "Be prepared to run into a hungry bear.",
            "C": "Try to be friendly with the bear they meet.",
            "D": "Refrain from teasing bears with cubs."
        },
        "answer": "B",
        "explanation": "【精析】细节推断题。讲话者提到在山道上遇熊几率虽小，但危险始终存在：“for a bear seems to know if you are carrying a lunch or a candy bar. He may even insist on taking it.”熊能闻出食物并可能强索，因此徒步携带食物的人必须随时做好碰上饥饿野熊的准备。因此答案为 B)。"
    },
    19: {
        "prompt": "What does the speaker say about prejudice?",
        "options": {
            "A": "It refers to opinions that are radical and widespread.",
            "B": "It means making judgments without adequate knowledge.",
            "C": "It refers to deep-rooted beliefs about someone or something.",
            "D": "It means sticking to one's judgments even when proved wrong."
        },
        "answer": "B",
        "explanation": "【精析】细节辨认题。讲话者解释偏见的词源与定义：“prejudice means to judge before having adequate knowledge.”即在掌握充分知识前妄下定论。因此答案为 B)。"
    },
    20: {
        "prompt": "Why does the speaker say prejudiced attitudes are dangerous?",
        "options": {
            "A": "They often lead to war between religious groups.",
            "B": "They keep certain occupations from thriving.",
            "C": "They allow myths and half-truths to persist.",
            "D": "They prevent us from getting to the truth."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。讲话者提到：“and they are dangerous because they can keep us from learning the truth about someone or something.”偏见很危险是因为它阻碍我们了解某人或某事的真相。因此答案为 D)。"
    },
    21: {
        "prompt": "When does the speaker say we begin to develop prejudiced attitudes?",
        "options": {
            "A": "When we start to feel superior.",
            "B": "When we mix with prejudiced people.",
            "C": "When we live in an isolated neighborhood.",
            "D": "When we try to keep up with those around us."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。讲话者指出：“If feelings of pride begin to turn to feelings of superiority when we think that our group or our beliefs are better than those around us, however, then we begin to develop prejudiced attitudes that can be harmful.”当自豪感转变为优越感时，我们便开始产生偏见。因此答案为 A)。"
    },
    22: {
        "prompt": "How did the speaker feel when he started high school?",
        "options": {
            "A": "Motivated.",
            "B": "Disappointed.",
            "C": "Perplexed.",
            "D": "Shocked."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。讲话者在讲述高中经历的开头提到：“When I started high school, it was a shock.”即刚上高中时感到了巨大震惊。因此答案为 D)。"
    },
    23: {
        "prompt": "What did the speaker once think of teenage friendships?",
        "options": {
            "A": "They would change with the passage of time.",
            "B": "They would benefit young people's adult life.",
            "C": "They would help kids grow.",
            "D": "They would last a lifetime."
        },
        "answer": "A",
        "explanation": "【精析】细节推断题。根据官方解析与讲话内容，很多青少年时期建立的友谊虽被认为可以持续一生，但随着岁月推移、工作、家庭与人生变故，人们终究会渐行渐远（people drift apart. Jobs, families and tragedies separate people from those lasting friendships）。因此答案为 A)。"
    },
    24: {
        "prompt": "What do we learn about the speaker when he returned from the Vietnam war?",
        "options": {
            "A": "He had become mature.",
            "B": "He suffered poor health.",
            "C": "He had lots of stories to tell.",
            "D": "He regretted leaving Vietnam."
        },
        "answer": "A",
        "explanation": "【精析】细节推断题。讲话者回国后感到仿佛活了10辈子，无法再融入高中时代的玩伴，觉得他们依然幼稚关心无聊琐事（They still seemed childish, concerned with childish things that weren't important to me），说明越战经历让他心智远超同龄人、变得十分成熟。因此答案为 A)。"
    },
    25: {
        "prompt": "What does the speaker try to do as a teacher?",
        "options": {
            "A": "Make friends with his students.",
            "B": "Show his students how to do their best.",
            "C": "Help his students get through the growing pains.",
            "D": "Share his personal experience with his students."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。讲话者在结尾指出：“As a teacher, I try to help them over the rough spots as best I can.”作为教师，他尽力帮助学生跨越成长中的艰难时刻（rough spots 对应 growing pains）。因此答案为 C)。"
    }
}
