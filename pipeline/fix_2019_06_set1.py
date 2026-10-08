#!/usr/bin/env python3
"""
Fine-tune and split all merged sentences in 2019-06-set1 into individual grammatical sentences,
each paired with its accurate Chinese translation.
"""

import sys
from pathlib import Path

# Add pipeline directory to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from data_2019_06_set1 import SUBPARTS, QUESTIONS

# Subpart 1: C1
NEW_C1_SENTS = [
    ('W', "Hi, my name's Cathy.", "你好，我叫凯茜。"),
    ('W', "Nice to meet you!", "很高兴认识你！"),
    ('M', "Nice to meet you too, Cathy.", "我也很高兴认识你，凯茜。"),
    ('M', "My name's John.", "我叫约翰。"),
    ('M', "I'm a university friend of the bride.", "我是新娘的大学同学。"),
    ('M', "What about you?", "你呢？"),
    ('M', "Who do you know at this party?", "在这个派对上你认识谁？"),
    ('W', "I am a colleague of Brenda.", "我是布伦达的同事。"),
    ('W', "I was a little surprised to be invited, to be honest.", "说实话，收到邀请时我有点惊讶。"),
    ('W', "We've only been working together the last six months, but we quickly became good friends.", "我们共事才半年左右，却很快成了好朋友。"),
    ('W', "We just wrapped up a project with a difficult client last week.", "上周我们刚刚结束了一个难缠客户的项目。"),
    ('W', "I bet Brenda is glad it's done with, and she can focus on wedding preparations.", "我敢说布伦达肯定很高兴项目收官了，这样她就能专心筹备婚礼。"),
    ('M', "Oh, yes, so you're Cathy from the office.", "哦，是啊，你就是办公室里的凯茜。"),
    ('M', "Actually I've heard a lot about you, and that project.", "说实话，我听说过很多关于你和那个项目的事。"),
    ('M', "The client sounded like a real nightmare.", "那个客户听起来简直是个噩梦。"),
    ('W', "Oh, he was.", "他确实如此。"),
    ('W', "I mean we deal with all kinds of people on a regular basis.", "我是说，我们平时就要和各种各样的人打交道。"),
    ('W', "It's part of the job, but he was especially particular.", "这是工作的一部分，只不过他格外挑剔。"),
    ('W', "Enough about that.", "不说他了。"),
    ('W', "What line of work are you in?", "你从事的是哪一行？"),
    ('M', "Well, right out of college, I worked in advertising for a while.", "我大学一毕业那会儿，在广告行业干过一阵子。"),
    ('M', "Recently though, I turned my photography hobby into a small business.", "不过最近，我把摄影这个爱好变成了一桩小生意。"),
    ('M', "I'll actually be taking photos during the big event as a wedding gift.", "我会在婚礼当天拍照，作为送给他们的一份结婚礼物。"),
    ('W', "That sounds wonderful, and very thoughtful of you.", "听起来太棒了，你想得真周到。"),
    ('W', "I bake just as a hobby but Brenda has asked me to do the cake for the wedding.", "我也只是把烘焙当作爱好，不过布伦达请我为婚礼做蛋糕。"),
    ('W', "I was a bit nervous saying yes, because I'm far from a professional.", "答应下来的时候我有点紧张，因为我远远算不上专业。"),
    ('M', "Did you bake the cookies here at the party tonight?", "今晚派对上的这些饼干是你烤的吗？"),
    ('W', "Yes, I got the idea from a magazine.", "是的，这个点子是我从一本杂志上看来的。"),
    ('M', "They're delicious.", "它们太好吃了。"),
    ('M', "You've got nothing to worry about.", "你完全不用担心。"),
    ('M', "You're a natural.", "你天生就是这块料。"),
    ('W', "You really think so?", "你真这么觉得？"),
    ('M', "If you hadn't told me that, I would have guessed they were baked by the restaurant.", "要不是你告诉我，我还真会以为这些是高档餐厅烤的呢。"),
    ('M', "You know, with your event planning experience, you could very well open your own shop.", "你知道吗，凭你策划活动的经验，完全可以自己开一家店。"),
    ('W', "One step at a time.", "一步一步来吧。"),
    ('W', "First I'll see how baking the wedding cake goes.", "我先看看婚礼蛋糕烤得怎么样。"),
    ('W', "If it's not a disaster, maybe I'll give it some more thought.", "如果没搞砸，也许我会再认真考虑考虑。")
]

# Subpart 2: C2
NEW_C2_SENTS = [
    ('M', "You're heading for a completely different world now that you're about to graduate from high school.", "既然你就要高中毕业了，你将迈向一个完全不同的世界。"),
    ('W', "I know it's the end of high school, but many of my classmates are going on to the same university, and we are still required to study hard.", "我知道高中生活要结束了，可我的好多同学都会进同一所大学，而且我们照样得努力学习。"),
    ('W', "So what's the difference?", "那大学和高中到底有什么不同呢？"),
    ('M', "Many aspects are different here at university.", "在大学里，有很多方面都不一样。"),
    ('M', "The most important one is that you have to take more individual responsibility for your actions.", "最重要的一点是，你必须为自己的行为独立承担更多责任。"),
    ('M', "It's up to your own self-discipline, how much effort you put into study.", "你在学习上投入多少努力，完全取决于你自己的自律。"),
    ('M', "Living in college dormitories, there are no parents to tell you to study harder or stop wasting time.", "住进大学宿舍以后，就再也没有父母叮嘱你要更努力地学习、不要虚度光阴了。"),
    ('M', "Lecturers have hundreds of students, and they're not going to follow you up or question you if you miss their class.", "大学讲师面对着成百上千名学生，你要是缺了课，他们也不会追在后面问你为什么。"),
    ('W', "Nobody cares, you mean?", "你是说，没有人会管我？"),
    ('M', "It's not that nobody is concerned about you.", "并不是没有人关心你。"),
    ('M', "It's just that suddenly at university, you are expected to behave like an adult.", "只是从进了大学开始，大家就期待你像成年人那样处事。"),
    ('M', "That means concentrating on the direction of your life in general and your own academic performance specifically.", "这意味着你既要关注自己人生的总体方向，也要特别关注自己的学业表现。"),
    ('W', "For example?", "比如说呢？"),
    ('M', "Well, like you need to manage your daily, weekly and monthly schedules so that you'll study regularly.", "比如说你得把每天、每周、每个月的日程安排好，才能有规律地学习。"),
    ('M', "Be sure to attend all classes and leave enough time to finish assignments and prepare well for examinations.", "要保证每堂课都出勤，并留出充足的时间完成作业、好好准备考试。"),
    ('W', "Okay, and what else is different?", "好，那还有哪些不同呢？"),
    ('M', "Well, in college, there are lots of distractions and you need to control yourself.", "在大学里，有太多让人分心的诱惑，你需要管住自己。"),
    ('M', "You will make interesting friends, but you need only keep the friends who respect your student commitments.", "你会结交到有趣的朋友，但你只需要和那些尊重你学生本分的人继续交往。"),
    ('M', "Also, there are a lot of wonderful clubs, but you shouldn't allocate too much time to club activities unless they are directly related to your study.", "此外，大学里有很多很棒的社团，但除非它们与你的学业直接相关，否则你不该在社团活动上投入太多时间。"),
    ('M', "It's also your choice if you want to go out at night, but you will be foolish to let that affect your class performance during the day.", "至于晚上要不要出去玩也是你自己的选择，但如果让它影响到你白天的课堂表现，那可就太不明智了。"),
    ('W', "Well, I'm determined to do well at university, and I guess I'm going to have to grow up fast.", "我下定决心要在大学好好表现，看来我得快点成熟起来了。")
]

# Subpart 3: P1
NEW_P1_SENTS = [
    ('M', "Most successful people are unorthodox persons whose minds wander outside traditional ways of thinking.", "大多数成功人士都是思维游离于传统路径之外的非正统之人。"),
    ('M', "Instead of trying to refine old formulas, they invent new ones.", "他们不去改良旧有的公式，而是发明全新的公式。"),
    ('M', "When Jean-Claude Killy made the French National Ski Team in the early 1960s, he was prepared to work harder than anyone else to be the best.", "20世纪60年代初，让-克洛德·基利入选法国国家滑雪队时，他准备比任何人都更拼命地训练，以做到最好。"),
    ('M', "At the crack of dawn, he would run up the slopes with his skis on, an unbelievably backbreaking activity.", "天刚破晓时，他就穿着滑雪板沿着雪道往上跑，这是一项累得难以想象的苦活。"),
    ('M', "In the evening, he would do weightlifting and running.", "到了晚上，他还要做举重和跑步训练。"),
    ('M', "But the other team members were working as hard and long as he was.", "但其他队员练得和他一样苦、一样久。"),
    ('M', "He realized instinctively that simply training harder would never be enough.", "他凭直觉意识到，光靠更拼命的训练永远是不够的。"),
    ('M', "Killy then began challenging the basic theories of racing technique.", "于是基利开始质疑竞赛技术的基本理论。"),
    ('M', "Each week, he would try something different to see if he could find a better, faster way down the mountain.", "每一周，他都尝试一些不同的东西，看能否找到一条更好、更快的下山路线。"),
    ('M', "His experiments resulted in a new style that was almost exactly opposite the accepted technique of the time.", "他的这些试验最终形成了一种全新的滑法，几乎与当时公认的常规技术完全相反。"),
    ('M', "It involved skiing with his legs apart for better balance, and sitting back on the skis when he came to a turn.", "这种滑法要求滑雪时两腿分开以获得更好的平衡，转弯时则要把身体后坐、压在滑雪板上。"),
    ('M', "He also used ski poles in an unorthodox way—to propel himself as he skied.", "他还以不合常规的方式使用滑雪杖，在滑行过程中为自己提供推进力。"),
    ('M', "The explosive new style helped cut Killy's racing time dramatically.", "这套极具爆发力的新滑法，让基利的比赛用时大幅缩短。"),
    ('M', "In 1966 and 1967, he captured virtually every major skiing trophy.", "1966年和1967年，他几乎囊括了所有重要的滑雪大奖。"),
    ('M', "The next year, he won three gold medals in the Winter Olympics, a record in ski racing that has never been topped.", "第二年，他在冬奥会上夺得三枚金牌，这是滑雪比赛史上从未被打破的纪录。"),
    ('M', "Killy learned an important secret shared by many creative people: innovations don't require genius, just a willingness to question the way things have always been done.", "基利领悟到许多有创造力的人都知晓的一个重要秘诀：创新并不需要天才，只需要一种质疑传统做法的意愿。")
]

# Subpart 4: P2
NEW_P2_SENTS = [
    ('M', "Scientific experiments have demonstrated incredible ways to kill a guinea pig, a small furry animal.", "科学实验揭示了若干种杀死豚鼠这种毛茸茸小动物的惊人办法。"),
    ('M', "Emotional upsets generate powerful and deadly toxic substances.", "情绪的波动会生成威力强大且致命的有毒物质。"),
    ('M', "Blood samples taken from persons experiencing intense fear or anger, when injected into guinea pigs, have killed them in less than two minutes.", "把那些正经历强烈恐惧或愤怒的人所抽取的血样注射进豚鼠体内，不到两分钟就能把它们杀死。"),
    ('M', "Imagine what these poisonous substances can do to your own body.", "想象一下，这些有毒物质对你自己的身体能造成怎样的伤害。"),
    ('M', "Every thought that you have affects your body chemistry within a split second.", "你产生的每一个念头，都会在转瞬之间影响你体内的化学变化。"),
    ('M', "Remember how you feel when you are speeding down the highway, and a big truck suddenly brakes twenty meters in front of you.", "还记得你在高速公路上疾驰、而前方二十米处一辆大卡车突然刹车时的那种感觉吗？"),
    ('M', "A shockwave shoots through your whole system.", "一股冲击波会贯穿你的整个身体系统。"),
    ('M', "Your mind produces instant reactions in your body.", "你的大脑会让躯体即刻做出本能反应。"),
    ('M', "The toxic substances that fear, anger, frustration and stress produce not only kill guinea pigs but kill us off in a similar manner.", "恐惧、愤怒、挫折和压力所产生的有毒物质，不仅能杀死豚鼠，也会以类似的方式慢性杀死我们。"),
    ('M', "It is impossible to be fearful, anxious, irritated and healthy at the same time.", "在恐惧、焦虑、愤怒的同时还保持健康，这是不可能的。"),
    ('M', "It is not just difficult; it is impossible.", "这不只是困难，而是根本不可能。"),
    ('M', "Simply put, your body's health is a reflection of your mental health.", "简单地说，身体健康就是心理健康的真实映射。"),
    ('M', "Sickness will often then be a result of unresolved inner conflicts, which in time show up in the body.", "疾病往往就是尚未化解的内心冲突的恶果，它们随着时间推移便会显现在身体上。"),
    ('M', "It is also fascinating how our subconscious mind shapes our health.", "我们的潜意识如何塑造身体健康，同样令人着迷。"),
    ('M', "Do you recall falling sick on a day when you didn't want to go to school?", "你是否记得有那么一天，当你不想去上学时，结果就真的生病了？"),
    ('M', "Headaches brought on by fear?", "还有那些由恐惧引发的剧烈头痛？"),
    ('M', "The mind-body connection is such that if, for example, we want to avoid something, very often our subconscious mind will arrange it.", "身心之间的关联如此紧密，以至于当我们想逃避某件事时，我们的潜意识往往会自动安排身体患病来配合。"),
    ('M', "Once we recognise that these things happen to us, we are half way to doing something about them.", "一旦我们清醒认识到这些情况正发生在自己身上，我们就已经在解决问题的道路上走完了一半。")
]

# Subpart 5: R1
NEW_R1_SENTS = [
    ('M', "Teachers and students alike have experienced the curious paradox that beginners, as a rule, tend to think too little about what they are doing because they think too much about what they are doing.", "老师和学生都曾经历过这种奇特的悖论：初学者通常对自己正在做的事想得太少，原因恰恰是他们在这件事上想得太多。"),
    ('M', "Take, for example, people who are learning to play basketball or the piano.", "以正在学打篮球或学弹钢琴的人为例。"),
    ('M', "They have to give so much thought and attention to the low-level mechanics of handling the ball or fingering the keys or reading the music that they are unable to give any thought to the thing that matters—the game, or the music, respectively.", "他们不得不把过多心思放在运球、按琴键或识谱等低阶操作细节上，以至于完全没有余力去思考真正核心的事物——也就是比赛本身或音乐本身。"),
    ('M', "With experts, it's just the other way around.", "而行家的情况则恰恰相反。"),
    ('M', "They're open to the tactical possibilities and the musical challenges precisely because they're freed, through skill, from the need to pay attention to the low-level details of how to play.", "他们能够从容应对战术可能性和音乐挑战，恰恰是因为高超的技能让他们摆脱了对基本操作细节的关注负担。"),
    ('M', "Their practice has made them automated.", "日复一日的练习使他们的操作形成了自动化肌肉记忆。"),
    ('M', "This has led some to say that the expert operates in a zone 'beyond thought', in a state of flow.", "这让有些人宣称专家是在“超越思维”的境界中运作，处于一种心流状态。"),
    ('M', "But this is misleading.", "但这种说法是有误导性的。"),
    ('M', "Expert performance is not beyond thought.", "专家的顶尖表现绝不是不加思考。"),
    ('M', "Rather, they have automated the low-level skills, allowing higher-level thoughts to guide the performance.", "更确切地说，他们只是把低阶技能自动化了，从而能够让更高阶的宏观思维来指引全局表现。"),
    ('M', "The expert is thinking, but about the right things at the right time.", "专家同样在深思熟虑，只是在恰当的时机思考最核心的事物。"),
    ('M', "How do we know this?", "我们如何得知这一点的呢？"),
    ('M', "A nice video published online last month sheds light on expertise and the conscious mind.", "上个月在网络上发布的一段精良视频，揭示了专业技能与显意识之间的奥秘。"),
    ('M', "The video reports a new study using an eye-tracking device.", "该视频报道了一项运用眼动追踪仪开展的全新研究。"),
    ('M', "Researchers compared the eye movements of novice and professional athletes in high-speed situations.", "研究人员对比了新手运动员与专业运动员在高速运动环境下的眼球移动轨迹。"),
    ('M', "In general, the expert's gaze was calmer and more stable.", "总体而言，专家的视线更为从容沉稳、聚焦稳定。"),
    ('M', "This is not a surprising finding.", "这并不是什么令人意外的发现。"),
    ('M', "It supports what we might almost think of as conventional wisdom.", "它印证了我们几乎视为传统常识的规律。"),
    ('M', "But it's remarkable for all that, nonetheless.", "尽管如此，这项发现依然意义非凡。"),
    ('M', "The eye tracker gives expert and learning performers a glimpse into what they do without thinking about it.", "眼动仪让行家与正在学习的人得以窥见自己在潜意识中不假思索所做出的反应。"),
    ('M', "It reminds us that high performance isn't just about fast reflexes, but about training the brain where to look.", "它提醒我们，卓越的高水平表现不仅仅关乎快速的身体反应，更在于训练大脑在关键时刻该注视何方。")
]

# Subpart 6: R2
NEW_R2_SENTS = [
    ('M', "I've spent a lot of time traveling across Asia over the past few years, and one thing that always strikes me is the incredible obsession with body weight and slimming down.", "在过去的几年里，我花了很多时间在亚洲各地旅行，始终让我深感震撼的一件事是人们对体重和变瘦有着极其强烈的执念。"),
    ('M', "Every convenience store and pharmacy is packed with diet supplements, teas, pills, and drinks promising dramatic weight loss.", "每家便利店和药店都塞满了减肥营养品、瘦身茶、药丸和各种承诺能带来剧烈减重效果的饮品。"),
    ('M', "There are special belts that vibrate to shake off fat, slimming creams that heat up the skin, and plastic wraps you wear while sleeping.", "有通过震动甩脂的专用腰带，有涂抹后发热的紧肤瘦身霜，还有睡觉时缠裹的保鲜塑身膜。"),
    ('M', "I've seen diets based purely on eating bananas for breakfast, or drinking apple cider vinegar before every meal.", "我见过早餐只吃香蕉的减肥法，或者每餐饭前都要喝一杯苹果醋的饮食法。"),
    ('M', "Some crazes sweep entire countries in a matter of weeks.", "有些瘦身狂潮在短短几周之内就能席卷整个国家。"),
    ('M', "Then there was the black tea and oolong tea diet, followed by the soybean diet and the tomato juice diet.", "后来又出现了红茶和乌龙茶瘦身法，随后是黄豆减肥法和番茄汁饮食法。"),
    ('M', "The list goes on and on.", "这样的花样名目层出不穷、没完没了。"),
    ('M', "What's fascinating is how the aesthetic ideals differ between the East and the West.", "极具趣味的是，东西方对于身材的审美理想存在着显著差异。"),
    ('M', "In Western countries, fitness trends emphasize muscle tone, athletic curves, and visible strength.", "在西方国家，健身潮流更强调肌肉线条、健美的身段轮廓以及显而易见的力量感。"),
    ('M', "Being thin alone isn't enough; people want to look strong and fit.", "光是身材纤瘦是远远不够的，人们渴望看起来强健有力、体态健硕。"),
    ('M', "In contrast, many Asian cultures celebrate extreme slimness, lightness, and fragility, especially for young women.", "相比之下，许多亚洲文化更推崇极致的纤瘦、轻盈与柔弱感，尤其是对年轻女性而言。"),
    ('M', "This difference is reflected in the media and advertising.", "这种文化差异在各类大众媒体和商业广告中体现得淋漓尽致。"),
    ('M', "Clothing sizes in department stores can be shockingly small.", "百货商场里的服装尺码有时小得令人瞠目结舌。"),
    ('M', "Social media amplifies the pressure, with viral challenges encouraging people to compare their waist sizes to sheets of paper or phone screens.", "社交媒体进一步放大了这种容貌身材焦虑，网络病毒式挑战鼓励大家将腰围与A4纸或手机屏幕相比较。"),
    ('M', "As each summer season approaches, there's no escape from it.", "随着每年夏季的临近，铺天盖地的身材焦虑无处遁形。"),
    ('M', "But it's not only women who are affected by this pressure to look good.", "但受到这种追求外貌完美的压力所影响的，绝非只有女性。"),
    ('M', "Men are also increasingly feeling the urge to stay lean and trim.", "男性也日益感受到必须保持清瘦干练身型的紧迫感。"),
    ('M', "While wanting to be healthy is great, going on extreme crash diets is dangerous.", "虽然追求身体健康是件好事，但采取极端的速成节食却是非常危险的。"),
    ('M', "Eat in a balanced way and incorporate the right level of physical activity.", "保持均衡膳食，并融入适度的体育锻炼。"),
    ('M', "For me, this still seems to be the best plan.", "对我而言，这依然是最好的长久之计。")
]

# Subpart 7: R3
NEW_R3_SENTS = [
    ('M', "Why did humans lose their body fur and become the only essentially naked ape among primates?", "为什么人类会褪去体毛，成为所有灵长类动物中唯一一种近乎全裸的猿类？"),
    ('M', "This is one of the classic evolutionary puzzles that scientists have spent decades investigating.", "这是科学家们花费数十年深入探究的经典进化之谜之一。"),
    ('M', "Charles Darwin thought it was down to sexual selection, but modern anthropologists point to thermoregulation.", "查尔斯·达尔文曾认为这是性选择的结果，但现代人类学家则将其归因于体温调节。"),
    ('M', "When our ancestors moved from dense forests to open grasslands in Africa, they had to walk long distances under the hot sun to hunt and gather food.", "当我们的远古祖先从茂密森林走向非洲开阔的大草原时，他们必须顶着烈日长途跋涉去狩猎和采集食物。"),
    ('M', "Running and walking in the midday heat posed a serious danger: overheating.", "在正午的酷暑中奔跑穿行带来了一个致命的危险：体温过高。"),
    ('M', "The human brain is particularly sensitive to temperature increases, and our ancestors had to keep their brains cool.", "人类的大脑对体温升高尤为敏感，我们的祖先必须时刻保证大脑处于凉爽状态。"),
    ('M', "We can't really lose heat by breathing quickly and loudly like dogs.", "我们无法像狗那样通过急促大声的喘气来快速散热。"),
    ('M', "We have to do it by sweating.", "我们必须通过排汗来散热降温。"),
    ('M', "So we evolved the ability to sweat plentifully and lost most of our fur.", "因此我们进化出了大量排汗的能力，并随之褪去了绝大部分体毛。"),
    ('M', "Most animals protect themselves from the sun with fur.", "大多数动物依靠皮毛来抵御阳光紫外线的伤害。"),
    ('M', "What we did in our ancestry was to produce more permanent natural coloring in our skin cells.", "而我们的人类祖先所做的，则是在皮肤细胞中产生更持久的天然黑色素色素沉淀。"),
    ('M', "This was really an important revolution in human history because it allowed us to continue to evolve in equatorial environments.", "这确实是人类历史上的一次重大革命，因为它让我们得以在赤道炎热环境中继续繁衍进化。"),
    ('M', "It really made it possible for us to continue along the path toward modern humans in Africa.", "正是这一点使得我们能够沿着非洲迈向现代人类的进化道路走下去。"),
    ('M', "For most of human history, we all had dark skin.", "在人类历史的大部分时期，我们全都是深色皮肤。"),
    ('M', "What we see today is the product of evolutionary events resulting from the dispersal of a few human populations out of Africa around 60,000 to 70,000 years ago.", "我们今天所看到的多元肤色，是大自然进化事件的产物，源于大约六万到七万年前少数人类族群走出非洲的迁徙扩散。"),
    ('M', "In high latitudes with low UV light, dark skin prevented sufficient vitamin D production, leading to the evolution of lighter skin.", "在高纬度、紫外线微弱的地区，深色皮肤阻碍了充足维生素D的合成，从而促使了较浅肤色的进化。"),
    ('M', "After that, a few small populations left Africa to populate the rest of the world.", "在那之后，一小部分人群离开非洲，繁衍定居于世界其他各个地区。"),
    ('M', "These early ancestors of modern Eurasians dispersed into parts of the world that had more seasonal sunshine and much lower levels of sun radiation.", "现代欧亚人群的这些早期祖先分散到了那些日照具有强烈季节性、紫外线辐射水平低得多的地域。"),
    ('M', "Genetic mutations that favored lighter pigmentation spread quickly through natural selection.", "有利于较浅色素沉着的基因突变通过自然选择迅速扩散开来。"),
    ('M', "Today, skin color is evolving via new mixtures of people coming together and having children with new mixtures of skin color genes.", "今天，随着不同族群的人们汇聚一堂，生育带有全新肤色基因组合的后代，人类肤色仍在经历持续的进化交融。"),
    ('M', "We can see this in almost every large city worldwide.", "我们在全球几乎每一个大型国际都市都能看到这种景象。"),
    ('M', "Not only the coloring genes, but lots of other genes are getting mixed up, too.", "不仅是肤色基因，大量其他遗传基因也在以全新的方式深度交织融合。")
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
target = Path("pipeline/data_2019_06_set1.py")
with open(target, "w", encoding="utf-8") as f:
    f.write("#!/usr/bin/env python3\n")
    f.write('"""\nOfficial data for 2019-06-set1 CET-6 listening test:\n- 7 subparts with authentic titles, Chinese topics, and question ranges\n- Complete grammatical sentences with 100% paired authentic Chinese translations\n- 25 official CET-6 questions with options, answers, and explanations\n"""\n\n')
    f.write("SUBPARTS = ")
    pprint.pprint(SUBPARTS, stream=f, width=120, compact=False)
    f.write("\n\nQUESTIONS = ")
    pprint.pprint(QUESTIONS, stream=f, width=120, compact=False)
    f.write("\n")

print(f"Successfully updated {target}")
total_s = sum(len(sp['sentences']) for sp in SUBPARTS)
print(f"Total individual sentences: {total_s}")
