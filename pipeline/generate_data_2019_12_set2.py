#!/usr/bin/env python3
"""
Generate pipeline/data_2019_12_set2.py with 100% golden standard:
- 7 Subparts with authentic titles, Chinese topics, and question ranges
- Complete grammatical sentences with 100% paired authentic Chinese translations
- 25 Official CET-6 questions with full options, verified answers, and detailed explanations
"""

import pprint
from pathlib import Path

SUBPARTS = [
    {
        "id": "2019-12-set2-conv-1",
        "subpart_code": "conv-1",
        "section_id": "2019-12-set2-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 1 · 伦敦爵士唱片专营店、爵士乐发展沿革与音乐流派特征",
        "topic_zh": "伦敦爵士唱片专营店、爵士乐发展沿革与音乐流派特征",
        "question_range": "Q1 ~ Q4",
        "questions": [1, 2, 3, 4],
        "sp_start": 37.40,
        "sp_end": 245.54,
        "sentences": [
            ("M", "Excuse me, where's your rock music section?", "请问，你们的摇滚乐专区在哪里？"),
            ("W", "Rock music? I'm sorry, we're a jazz store. We don't have any rock and roll.", "摇滚乐？实在抱歉，我们是一家爵士乐唱片店，这里没有任何摇滚乐。"),
            ("M", "Oh, you only have jazz music? Nothing else?", "哦，你们只卖爵士乐吗？没有其他类型的音乐？"),
            ("W", "That's right. We're the only record store in London dedicated exclusively to jazz.", "没错。我们是全伦敦唯一一家专门销售爵士乐的唱片店。"),
            ("W", "Actually, we're more than just a record store. We have a cafe and library upstairs.", "事实上，我们不仅仅是一家唱片店。我们在楼上还设有咖啡厅和图书室。"),
            ("W", "And a ticket office down the hall where you can buy tickets to all the major jazz concerts in the city.", "穿过大厅还有一个票务中心，你可以在那里购买本市所有重要爵士音乐会的门票。"),
            ("W", "Also, we have our own studio next door where we produce albums for up-and-coming artists.", "此外，我们隔壁还有自己的录音棚，为崭露头角的新晋艺术家制作唱片专辑。"),
            ("W", "We're committed to fostering new music talent.", "我们始终致力于发掘和培养新一代的音乐人才。"),
            ("M", "Wow, that's so cool! I guess there's not much of a jazz scene anymore, not like there used to be.", "哇，太酷了！我猜现在的爵士乐圈子已经不大景气了，完全不像过去那样繁荣。"),
            ("M", "But here you're trying to promote this great music genre.", "但你们却在这里竭力推广这种伟大的音乐流派。"),
            ("W", "Yes, indeed. Nowadays, most people like to listen to pop and rock music.", "是的，确实如此。如今大多数人都更喜欢听流行音乐和摇滚乐。"),
            ("W", "Hip-hop music from America is also getting more and more popular.", "源自美国的嘻哈音乐也正变得越来越受欢迎。"),
            ("W", "So as a result, there are fewer listeners of jazz, which is a great shame, because it's an incredibly rich genre.", "因此，爵士乐的听众变得越来越少，这真是一大遗憾，因为它是一个底蕴极其丰富的音乐流派。"),
            ("W", "But that's not to say there isn't any good new jazz music being made out there anymore.", "但这并不是说现在外界就不再创作优秀的爵士新作品了。"),
            ("W", "Far from it. It's just a much smaller market today.", "远非如此。只是现如今它的市场受众规模小得多了。"),
            ("M", "So how would you define jazz?", "那么，你会如何定义爵士乐呢？"),
            ("W", "Well, interestingly enough, there's no agreed-upon definition of jazz.", "嗯，非常有意思的是，目前关于爵士乐并没有一个公认的统一定义。"),
            ("W", "Indeed, there are many different styles of jazz.", "事实上，爵士乐涵盖了许多截然不同的风格流派。"),
            ("W", "Some have singing, but most don't.", "有些风格包含人声演唱，但大多数都没有。"),
            ("W", "Some are electric and some aren't.", "有些采用电声乐器，有些则不是。"),
            ("W", "Some contain live experimentation, but not always.", "有些融入了现场即兴实验，但也并非尽皆如此。"),
            ("W", "While there's no simple definition for it, and while there are many different styles of jazz, you simply know it when you hear it.", "虽然无法给它一个简单的定义，而且爵士乐风格多样，但当你亲耳听到它时，你自然就能辨别出来。"),
            ("W", "Honestly, the only way to know what jazz is is to listen to it yourself.", "老实说，要领会爵士乐真谛的唯一途径，就是亲自去聆听。"),
            ("W", "As the great trumpet player Louis Armstrong said, \"If you've got to ask, you'll never know.\"", "正如伟大的小号演奏家路易斯·阿姆斯特朗所说：“如果你还需要开口问，那你永远都不会懂。”")
        ]
    },
    {
        "id": "2019-12-set2-conv-2",
        "subpart_code": "conv-2",
        "section_id": "2019-12-set2-sec-a",
        "section_title": "Section A: Long Conversations",
        "type": "conversation",
        "title": "Conversation 2 · 女性自主创业贷款受挫、个人信用记录与多渠道小额筹资",
        "topic_zh": "女性自主创业贷款受挫、个人信用记录与多渠道小额筹资",
        "question_range": "Q5 ~ Q8",
        "questions": [5, 6, 7, 8],
        "sp_start": 245.54,
        "sp_end": 432.31,
        "sentences": [
            ("M", "How did it go at the bank this morning?", "今天早晨去银行办得怎么样？"),
            ("W", "Not well. My proposal was rejected.", "很不顺利，我的贷款申请被拒绝了。"),
            ("M", "Really? But why?", "真的吗？为什么会这样？"),
            ("W", "A bunch of reasons. For starters, they said my credit history was not good enough.", "原因有很多。首先，他们说我的个人信用记录不够良好。"),
            ("M", "Did they say how you could improve that?", "他们有没有说你该如何改善信用记录？"),
            ("W", "Yes. They said that after five more years of paying my mortgage, then I would become a more viable candidate for a business loan.", "说了。他们表示如果我再按时偿还五年房贷，到那时我才会成为商业贷款更合格的候选人。"),
            ("W", "But right now, it's too risky for them to lend me money.", "但就目前而言，借钱给我对银行来说风险过高。"),
            ("W", "They fear I will default on any business loan I'm given.", "他们担心我会违约逾期无力偿还任何商业贷款。"),
            ("M", "Well, that doesn't sound fair. Your business idea is amazing!", "唉，这听起来太不公平了。你的商业创意棒极了！"),
            ("M", "Did you show them your business plan? What did they say?", "你把商业计划书给他们看了吗？他们怎么说的？"),
            ("W", "They didn't really articulate any position regarding the actual business plan.", "他们其实并没有针对商业计划书本身明确表达任何立场。"),
            ("W", "They simply looked at my credit history and determined it was not good enough.", "他们只是查看了我的信用记录，便认定我的信用状况不够达标。"),
            ("W", "They said the bank has strict guidelines and requirements as to who they can lend money to.", "他们解释说，对于能够向谁发放贷款，银行有着极其严苛的指导方针和硬性要求。"),
            ("W", "And I simply don't meet their financial threshold.", "而我根本没有达到他们的财务门槛要求。"),
            ("M", "What if you asked for a smaller amount?", "如果你申请较小的贷款金额呢？"),
            ("M", "Maybe you could gather capital from other sources, smaller loans from more lenders?", "也许你可以从其他渠道筹集资金，比如从更多出借方那里获取小额贷款？"),
            ("W", "You don't get it. It doesn't matter the size of the loan I ask for, or the type of business I propose.", "你没明白。无论我申请多大金额的贷款，也无论我提出什么样的商业项目，都无济于事。"),
            ("W", "That's all inconsequential.", "这些在他们眼里全都是无关紧要的。"),
            ("W", "The first thing every bank will do is study how much money I have and how much debt I have before they decide whether or not to lend me any more money.", "在决定是否向我出借资金之前，每家银行首先要做的就是审查我名下有多少资产和背负多少债务。"),
            ("W", "If I want to continue ahead with this dream of owning my own business, I have no other choice but to build up my own finances.", "如果我想继续坚持自主创业的梦想，我别无选择，只能努力改善并壮大自己的个人财务状况。"),
            ("W", "I need around 20% more in personal savings and 50% less debt. That's all there is to it.", "我的个人储蓄需要增加大约20%，并且债务必须减少50%，仅此而已。"),
            ("M", "I see now. Well, it's a huge pity that they rejected your request, but don't lose hope.", "我现在明白了。唉，他们拒绝了你的申请确实太遗憾了，但千万别灰心泄气。"),
            ("M", "I still think that your idea is great and that you will turn it into a phenomenal success.", "我依然坚信你的创意非常出色，而且你一定会将它打造成非凡的成功。")
        ]
    },
    {
        "id": "2019-12-set2-pass-1",
        "subpart_code": "pass-1",
        "section_id": "2019-12-set2-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 1 · 青年农场主突破传统小规模生态农业与高效除草松土工具",
        "topic_zh": "青年农场主突破传统小规模生态农业与高效除草松土工具",
        "question_range": "Q9 ~ Q11",
        "questions": [9, 10, 11],
        "sp_start": 475.16,
        "sp_end": 667.70,
        "sentences": [
            ("Speaker", "There's a lot about Leo Sanchez and his farm in Salinas, California that seems unusual.", "在加利福尼亚州萨利纳斯，关于利奥·桑切斯和他的农场，有许多看似与众不同之处。"),
            ("Speaker", "The national average farm size is around 440 acres, but his is only one acre.", "全美农场的平均面积约为440英亩，而他的农场却仅仅只有1英亩。"),
            ("Speaker", "The average age of farmers hovers around 58 years old, but he is just 26.", "农场主的平均年龄在58岁左右徘徊，而他年仅26岁。"),
            ("Speaker", "And Sanchez constantly attempts to improve everything from seeding techniques out in the field to the promotion and sale of his produce online.", "而且，桑切斯不断尝试革新各项环节，从田间的播种技术，到农产品的线上推广与销售无一例外。"),
            ("Speaker", "This is evidence of an experimental approach.", "这是勇于实验与探索理念的有力明证。"),
            ("Speaker", "It's an approach not dictated by the confines of conventional large-scale agriculture led by international corporations.", "这种方式不受跨国企业主导的传统大规模农业模式所束缚与局限。"),
            ("Speaker", "While farming is often difficult for both the body and mind, Sanchez says he and many of his fellow young farmers are motivated by a desire to set a new standard for agriculture.", "尽管务农往往对身心都是巨大的考验，但桑切斯表示，他和众多年轻的同行农场主都受到树立现代农业新标准的强烈愿望所激励。"),
            ("Speaker", "Many of them are employing a multitude of technologies, some new and some not so new.", "他们中的许多人正在采用多种多样的技术手段，有些是前沿技术，而有些则并不算新。"),
            ("Speaker", "Recently, Sanchez bought a hand-operated tool which pulls out weeds and loosens soil.", "最近，桑切斯购入了一款既能拔除杂草又能疏松土壤的手动工具。"),
            ("Speaker", "It actually dates back to at least 1701.", "该工具的历史实际上至少可以追溯到1701年。"),
            ("Speaker", "It stands in sharp contrast to Sanchez's other gadget, a gas-powered flame weed-killer invented in 1997.", "这与桑切斯的另一件装备——发明于1997年的燃气火焰除草机形成了极其鲜明的对比。"),
            ("Speaker", "He simply doesn't discriminate when it comes to the newness of tools. If it works, it works.", "在对待工具的新旧问题上，他完全没有任何偏见；只要管用，那就是好工具。"),
            ("Speaker", "Farmers have a long history of invention and it's no different today.", "农夫们拥有悠久的发明创造历史，在当今时代依然如此。"),
            ("Speaker", "Young farmers are guided by their love for agriculture and aided by their knowledge of technology.", "年轻一代农场主以对农业的热爱为指引，并借助先进的科技知识作为助力。"),
            ("Speaker", "To find inexpensive and appropriately sized tools, they collaborate and innovate.", "为了寻找价格亲民且规格适中的工具，他们密切协作、推陈出新。"),
            ("Speaker", "Sometimes the old stuff just works better or more efficiently.", "有时候，传统老旧的工具反而更加好用、更具效率。")
        ]
    },
    {
        "id": "2019-12-set2-pass-2",
        "subpart_code": "pass-2",
        "section_id": "2019-12-set2-sec-b",
        "section_title": "Section B: Passages",
        "type": "passage",
        "title": "Passage 2 · 食用昆虫高蛋白环保食品创新与英国主流零售市场试水",
        "topic_zh": "食用昆虫高蛋白环保食品创新与英国主流零售市场试水",
        "question_range": "Q12 ~ Q15",
        "questions": [12, 13, 14, 15],
        "sp_start": 667.70,
        "sp_end": 869.92,
        "sentences": [
            ("Speaker", "Eat Grub is Britain's first new food company that breaks western food boundaries by introducing edible insects as a new source of food.", "Eat Grub是英国首家突破西方传统饮食边界、引入可食用昆虫作为新型食品来源的创新食品公司。"),
            ("Speaker", "And Sainsbury's is the first UK supermarket to stock the company's crunchy roasted crickets.", "塞恩斯伯里则是英国首家上架销售该公司香脆烤蟋蟀的连锁超市。"),
            ("Speaker", "Sainsbury's insists that such food is no joke and could be a new sustainable source of protein.", "塞恩斯伯里坚称这种食品绝非开玩笑，它有望成为一种全新的可持续蛋白质来源。"),
            ("Speaker", "Out of curiosity, I paid a visit to Sainsbury's.", "出于好奇，我特意前往塞恩斯伯里超市一探究竟。"),
            ("Speaker", "As I put my hand into a packet of crickets with their tiny eyes and legs, the idea of one going in my mouth made me feel a little sick.", "当我伸手探进一包带着细小眼睛和附肢的蟋蟀零食袋时，一想到要将一只塞进嘴里，心里就直犯恶心。"),
            ("Speaker", "But the first bite was a pleasant surprise.", "然而，第一口咬下去却令人感到惊喜。"),
            ("Speaker", "A little dry and lacking of taste, but at least a wing didn't get stuck in my throat.", "虽然口感略显干涩且风味稍淡，但至少没有翅膀卡在我的喉咙里。"),
            ("Speaker", "The roasted seasoning largely overpowered any other flavour, although there was a slightly bitter aftertaste.", "烘烤调料在很大程度上掩盖了其他所有味道，尽管回味中略带一丝微苦。"),
            ("Speaker", "The texture was crunchy, but smelt a little of cat food.", "它的质感香脆酥脆，但闻起来略有一点猫粮的气味。"),
            ("Speaker", "Eat Grub also recommends the crickets as a topping for noodles, soups and salads.", "Eat Grub还推荐将这些蟋蟀用作面条、浓汤和沙拉的佐料配料。"),
            ("Speaker", "The company boasts that its dried crickets contain more protein than beef, chicken and pork, as well as minerals like iron and calcium.", "该公司宣称其蟋蟀干的蛋白质含量高过牛肉、鸡肉和猪肉，并且富含铁和钙等矿物质。"),
            ("Speaker", "Unlike the production of meat, bugs do not use up large amounts of land, water or feed.", "与传统肉类生产不同，昆虫养殖不需要耗费大量的土地、水源或饲料。"),
            ("Speaker", "And insect farming also produces far fewer greenhouse gases.", "而且昆虫养殖排放的温室气体也要少得多。"),
            ("Speaker", "However, despite 2 billion people worldwide already supplementing their diet with insects, consumer disgust remains a large barrier in many western countries.", "然而，尽管全球已有20亿人在日常饮食中补充食用昆虫，但在许多西方国家，消费者的厌恶反感情绪依然是一大障碍。"),
            ("Speaker", "I'm not sure bugs will become a popular snack anytime soon, but they're definitely food for thought.", "我不确定昆虫是否会在短时间内成为风靡的大众零食，但它们无疑值得我们深思与玩味。")
        ]
    },
    {
        "id": "2019-12-set2-rec-1",
        "subpart_code": "rec-1",
        "section_id": "2019-12-set2-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 1 · 学习风格理论科学性存疑、教学实验缺陷与多模态视觉教具普适价值",
        "topic_zh": "学习风格理论科学性存疑、教学实验缺陷与多模态视觉教具普适价值",
        "question_range": "Q16 ~ Q18",
        "questions": [16, 17, 18],
        "sp_start": 897.34,
        "sp_end": 1147.96,
        "sentences": [
            ("Speaker", "Have you ever had someone try to explain something to you a dozen times with no luck?", "你是否曾遇到过别人向你解释某件事十几次，你却依然一头雾水的情况？"),
            ("Speaker", "But then when you see a picture, the idea finally clicks.", "但随后当你看到一张图片时，那个概念瞬间就豁然开朗了。"),
            ("Speaker", "If that sounds familiar, maybe you might consider yourself a visual learner.", "如果这听起来很熟悉，也许你可能会认为自己是一个视觉型学习者。"),
            ("Speaker", "Or if reading or listening does the trick, maybe you feel like you're a verbal learner.", "或者，如果阅读文字或聆听讲解最管用，也许你会觉得自己是一个言语型学习者。"),
            ("Speaker", "We call these labels learning styles.", "我们将这些标签称为“学习风格”。"),
            ("Speaker", "But is there really a way to categorize different types of students?", "但是，真的有办法将不同类型的学生这样归门别类吗？"),
            ("Speaker", "Well, it actually seems that multiple presentation formats, especially if one of them is visual, help most people learn.", "嗯，事实表明，多种形式的呈现方式（尤其是其中包含视觉形式时）对大多数人的学习都有帮助。"),
            ("Speaker", "When psychologists and educators test for learning styles, they're trying to figure out whether these are inherent traits that affect how well students learn, instead of just a preference.", "当心理学家和教育学者检测学习风格时，他们试图弄清楚这些究竟是影响学生学习成效的固有特质，还是仅仅只是一种个人偏好。"),
            ("Speaker", "Usually, they start by giving a survey to figure out what style a student favors, like visual or verbal learning.", "通常，他们首先通过问卷调查来了解学生倾向于哪种风格，比如视觉型还是言语型学习。"),
            ("Speaker", "Then, they try to teach the students something with a specific presentation style, like using visual aids, and do a follow-up test to see how much they learned.", "然后，他们尝试用特定的呈现风格（例如使用视觉教具）向学生传授知识，并进行后续测试以评估他们的掌握程度。"),
            ("Speaker", "That way, the researchers can see if the self-identified verbal learners really learned better when the information was just spoken aloud, for example.", "这样一来，研究人员就能观察那些自认为是言语型的学习者在仅通过口头讲解获取信息时，是否真的学得更好。"),
            ("Speaker", "But, according to a 2008 review, only one study that followed this design found that students actually learned best with their preferred style.", "但是，根据2008年的一篇文献综述，在采用该设计的研究中，仅有一项研究发现学生在符合其偏好风格时学得最好。"),
            ("Speaker", "But the study had some big flaws.", "然而，那项研究存在一些严重的缺陷。"),
            ("Speaker", "The researchers excluded two-thirds of the original participants because they didn't seem to have any clear learning style from the survey at the beginning.", "研究人员剔除了最初三分之二的参与者，因为在最初的问卷调查中他们似乎并没有表现出明确的学习风格。"),
            ("Speaker", "And they didn't even report the actual test scores in the final paper.", "而且他们甚至没有在最终的论文中公布实际的测试分数。"),
            ("Speaker", "So, it doesn't really seem like learning styles are an inherent trait that we all have.", "因此，学习风格似乎根本不是我们每个人生来就具备的固有特质。"),
            ("Speaker", "But, that doesn't mean that all students will do amazingly if they just spend all their time reading from a textbook.", "但是，这并不意味着如果所有学生把全副精力都花在死读课本上，就能取得惊人的成绩。"),
            ("Speaker", "Instead, most people seem to learn better if they're taught in several ways, especially if one is visual.", "相反，如果采用多元化的教学方式——尤其是融入视觉元素时，大多数人的学习效果都会更好。"),
            ("Speaker", "In one study, researchers tested whether students remembered lists of words better if they heard them, saw them, or both.", "在一项实验中，研究人员测试了学生在通过听觉、视觉或两者兼备的方式记单词列表时，哪种效果更佳。"),
            ("Speaker", "And everyone seemed to do better if they got to see the words in print.", "结果发现，只要能够看到印出来的单词，所有人的表现都明显更好。"),
            ("Speaker", "Even the self-identified auditory learners; their preference didn't seem to matter.", "就连那些自称是听觉型的学习者也是如此，他们的偏好似乎并未产生任何实际影响。"),
            ("Speaker", "Similar studies tested whether students learned basic physics and chemistry concepts better by reading plain text or viewing pictures too.", "类似的研究还测试了学生在学习基础物理和化学概念时，是通过纯文本阅读还是结合图片学习效果更好。"),
            ("Speaker", "And everyone did better with the help of pictures.", "事实证明，在图片的辅助下，所有人的成绩都更为优异。")
        ]
    },
    {
        "id": "2019-12-set2-rec-2",
        "subpart_code": "rec-2",
        "section_id": "2019-12-set2-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 2 · 资本主义工时缩短预言破灭、职场内疚感与自主选择权缺失之危害",
        "topic_zh": "资本主义工时缩短预言破灭、职场内疚感与自主选择权缺失之危害",
        "question_range": "Q19 ~ Q21",
        "questions": [19, 20, 21],
        "sp_start": 1147.96,
        "sp_end": 1384.71,
        "sentences": [
            ("Speaker", "Free market capitalism hasn't freed us. It has trapped us.", "自由市场资本主义并没有赋予我们自由，反而将我们深困其中。"),
            ("Speaker", "It's imperative for us to embrace a workplace revolution.", "对我们而言，掀起一场职场革命势在必行。"),
            ("Speaker", "We are unlikely to spend our last moments regretting that we didn't spend enough of our lives slaving away at work.", "在人生的弥留之际，我们不太可能会后悔自己没有把更多生命奉献给劳碌辛苦的工作。"),
            ("Speaker", "We may instead find ourselves feeling guilty about the time we didn't spend watching our children grow, or with our loved ones, or travelling, or on the cultural or leisure pursuits that bring us happiness.", "相反，我们可能会对自己未能花更多时间陪伴子女成长、陪伴挚爱亲人、去各地旅行、或者追求能为我们带来快乐的文化休闲活动而深感内疚与自责。"),
            ("Speaker", "Unfortunately, the average full-time employee in the world works 42 hours a week.", "不幸的是，全球全职员工的平均每周工作时长高达42小时。"),
            ("Speaker", "Well over a third of the time we're awake.", "这远远超过了我们在清醒状态下三分之一的时间。"),
            ("Speaker", "Some of our all too precious time is being stolen.", "我们弥足珍贵的部分时间正在被悄然剥夺。"),
            ("Speaker", "Office workers do around 2 billion hours of unpaid overtime each year.", "白领上班族每年承担了约20亿小时的无偿加班。"),
            ("Speaker", "So it's extremely welcome that some government coalitions have started looking into potentially cutting the working week to four days.", "因此，一些政府联合体开始探讨将每周工作日缩减至四天的可行性，这非常令人欣慰。"),
            ("Speaker", "The champions of free market capitalism promised their way of life would bring us freedom, but it wasn't freedom at all.", "自由市场资本主义的拥趸们曾许诺他们的生活方式能带给我们自由，但这根本不是真正的自由。"),
            ("Speaker", "From the lack of secure affordable housing to growing job insecurity and rising personal debt, the individual is trapped.", "从缺乏安全可负担的住房，到日益加剧的职业危机感以及节节攀升的个人债务，普通人步步受困。"),
            ("Speaker", "Nine decades ago, leading economists predicted that technological advances and rising productivity would mean that we'd be working a 15-hour week by now.", "九十年前，杰出的经济学家曾预言，技术的进步和生产力的提升意味着到今天我们每周只需工作15个小时。"),
            ("Speaker", "That target has been somewhat missed.", "这一宏伟愿景显然落空了。"),
            ("Speaker", "Here is the most malignant threat to our personal freedom, particularly as the balance of power in the workplace has been shifted so dramatically from worker to boss.", "这正是对我们个人自由最恶毒的侵害，尤其是当职场中的权力平衡如此剧烈地从劳动者倒向雇主老板的时候。"),
            ("Speaker", "A huge portion of our lives involves the surrender of our freedom and personal autonomy.", "我们生命中有相当大的一部分时间都在被迫放弃个人的自由与独立自主权。"),
            ("Speaker", "It's time in which we are directed by the needs and desires of others and denied the right to make our own choices.", "在这段时间里，我们任由他人的需求与欲望所支配，被剥夺了自主抉择的权利。"),
            ("Speaker", "That's bad for us.", "这对我们的身心极具危害。"),
            ("Speaker", "It's hardly surprising that over half a million workers suffer from work-related mental health conditions each year.", "每年有超过五十万名劳动者罹患与工作相关的心理健康疾病，这一点都不足为奇。"),
            ("Speaker", "Or that 15.4 million working days were lost to work-related stress last year, a jump of nearly a quarter.", "去年因工作压力而损失的工时甚至高达1540万个工作日，暴增了将近四分之一。"),
            ("Speaker", "Yes, there are those who, far from being overworked, actually seek more hours.", "诚然，有些人远非工作过量，反而希望能获得更多的工时。"),
            ("Speaker", "But a shorter working week would enable us to redistribute hours from the overworked to the underworked.", "但缩短工作周能让我们将工时从过度劳累的群体重新分配给工时不足的群体。"),
            ("Speaker", "We need to look at ways of cutting the working week without slashing living standards.", "我们需要探索在不降低人们生活水准的前提下缩减工作周的有效途径。"),
            ("Speaker", "After all, the world's workers have already suffered the worst deduction in wages since the early 1800s.", "毕竟，全球劳动者已经承受了自19世纪初以来最严重的薪资实际购买力缩水。"),
            ("Speaker", "And cutting the working week would be conducive to the individual, giving millions of workers more time to spend as they see fit.", "缩短工作周将对个体大有裨益，能赋予数以百万计的劳动者更多由自己自由支配的闲暇时光。")
        ]
    },
    {
        "id": "2019-12-set2-rec-3",
        "subpart_code": "rec-3",
        "section_id": "2019-12-set2-sec-c",
        "section_title": "Section C: Recordings",
        "type": "recording",
        "title": "Recording 3 · 柏林新机场延期丑闻、工程质量缺陷与高昂闲置维护成本",
        "topic_zh": "柏林新机场延期丑闻、工程质量缺陷与高昂闲置维护成本",
        "question_range": "Q22 ~ Q25",
        "questions": [22, 23, 24, 25],
        "sp_start": 1384.71,
        "sp_end": 1681.01,
        "sentences": [
            ("Speaker", "Today, I'm going to talk about Germany's dream airport in Berlin.", "今天，我要谈谈德国在柏林的“梦想机场”。"),
            ("Speaker", "The airport looks exactly like every other major modern airport in Europe, except for one big problem.", "这座机场在外观上与欧洲其他各大现代化主要机场毫无二致，只是存在一个致命的大问题。"),
            ("Speaker", "More than seven years after it was originally supposed to open, it still stands empty.", "在原定启用的七年多之后，它依然空空如也地伫立在那里。"),
            ("Speaker", "Germany is known for its efficiency and refined engineering, but when it comes to its new ghost airport, this reputation could not be further from the truth.", "德国一向以严谨高效和精湛的工程技术闻名于世，但在对待这座全新的“幽灵机场”时，这一美誉却与事实相去甚远。"),
            ("Speaker", "Plagued by long delays, perpetual mismanagement, and ever-soaring costs, the airport has become something of a joke among Germans, and a source of frustration for local politicians, business leaders, and residents alike.", "饱受工期严重延误、管理混乱无序以及开支节节飙升的困扰，该机场在德国民众眼中已俨然成了一个天大的笑柄，并成为令当地政客、商业领袖以及寻常居民倍感沮丧的根源。"),
            ("Speaker", "Planning for the new airport began in 1989.", "新机场的规划筹备工作早在1989年便已启动。"),
            ("Speaker", "At the time, it became clear that the newly reunified Berlin would need a modern airport with far greater capacity than its existing airports.", "当时人们清醒地认识到，刚刚重新统一的柏林急需一座吞吐能力远超现有机场的现代化航空港。"),
            ("Speaker", "The city broke ground on the new airport in 2006.", "柏林市于2006年为新机场正式破土动工。"),
            ("Speaker", "The first major sign of problems came in summer 2010, when the Construction Corporation pushed the opening from October 2011 to June 2012.", "出现严重问题的首个重大迹象是在2010年夏天，当时建设总公司将启用日期从2011年10月推迟至2012年6月。"),
            ("Speaker", "In 2012, the city planned an opening ceremony, but less than a month beforehand, inspectors found significant problems with the fire safety system and pushed the opening back again to 2013.", "2012年，市政府甚至筹备了盛大的启用典礼，但在距开幕不足一个月时，质检人员发现消防排烟系统存在重大隐患，开通时间不得不再次顺延至2013年。"),
            ("Speaker", "It wasn't just the smoke system, many other major problems subsequently emerged.", "出了问题的绝不仅是排烟系统，随后更多严重的质量问题相继暴露出来。"),
            ("Speaker", "More than 90 meters of cable were incorrectly installed.", "长达90多米的线缆被错误敷设。"),
            ("Speaker", "4,000 doors were wrongly numbered, escalators were too short, and there was a shortage of check-in desks.", "四千扇门编号错误，自动扶梯过短，值机柜台也严重不足。"),
            ("Speaker", "So why, with so many problems discovered, didn't the airport corporation decide to give up on the project and start over?", "那么，既然发现了如此多的问题，机场集团为何不干脆放弃这个烂摊子重新推倒重来呢？"),
            ("Speaker", "The reason is simple. People are often hesitant to terminate a project when they've already invested time or resources into it.", "原因很简单：当人们已经在某件事上投入了大量时间和资源时，往往难以狠下心彻底终止项目。"),
            ("Speaker", "Even if it might make logical sense to do so.", "即便从理性逻辑的角度来看终止项目才是明智之举。"),
            ("Speaker", "The longer the delays continued, the more problems inspectors found.", "拖延的时间越长，检验人员发现的漏洞缺陷就越多。"),
            ("Speaker", "Leadership of the Planning Corporation has changed hands nearly as many times as the opening date has been pushed back.", "规划公司的领导班子换帅走人的频繁程度，几乎与通航日期被推迟的次数不相上下。"),
            ("Speaker", "Initially, rather than appointing a general contractor to run the project, the corporation decided to manage it themselves, despite lack of experience with an undertaking of that scale.", "起初，该机构并未聘请经验丰富的工程总包商来掌舵项目，而是决定由自己直接统筹管理，尽管他们对如此庞大规模的世纪工程完全缺乏经验。"),
            ("Speaker", "To compound the delays, the unused airport is resulting in massive costs.", "更让人雪上加霜的是，这座闲置不用的机场正在产生天文数字般的巨额开支。"),
            ("Speaker", "Every month it remains unopened costs between 9 and 10 million euros.", "处于停滞状态的机场每月耗费的高达900万至1000万欧元。"),
            ("Speaker", "Assuming all goes well, the airport should open in October 2020, but the still empty airport stands as the biggest embarrassment to Germany's reputation for efficiency, and a continuing drain on city and state resources.", "假定一切进展顺利，机场预计将于2020年10月投入运营；但这处至今依旧空荡荡的机场，已成为德国高效声誉的最大耻辱，并持续无情吞噬着城市与国家的财政资源。")
        ]
    }
]

QUESTIONS = {
    1: {
        "prompt": "What do we learn about the woman's store?",
        "options": {
            "A": "It focuses exclusively on jazz.",
            "B": "It sponsors major jazz concerts.",
            "C": "It has several branches in London.",
            "D": "It displays albums by new music talents."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。男士询问摇滚乐专区在哪里，女士解释：“We're a jazz store... We're the only record store in London dedicated exclusively to jazz.”女士经营的店铺是全伦敦唯一一家专注于爵士乐的专营唱片店（focuses exclusively on jazz）。因此答案为 A)。"
    },
    2: {
        "prompt": "What does the man say about jazz music?",
        "options": {
            "A": "It originated with cowboys.",
            "B": "Its market has now shrunk.",
            "C": "Its listeners are mostly young people.",
            "D": "It remains as widespread as hip hop music."
        },
        "answer": "B",
        "explanation": "【精析】细节推断题。男士感叹爵士乐不如以往风光：“I guess there's not much of a jazz scene anymore, not like there used to be.”女士随后也赞同并指出：“It's just a much smaller market today.”即当今爵士乐的市场受众规模已大幅萎缩（Its market has now shrunk）。因此答案为 B)。"
    },
    3: {
        "prompt": "What does the woman say about jazz?",
        "options": {
            "A": "Its definition is varied and complicated.",
            "B": "It is still going through experimentation.",
            "C": "It is frequently accompanied by singing.",
            "D": "Its style has remained largely unchanged."
        },
        "answer": "A",
        "explanation": "【精析】细节辨认题。当男士询问如何定义爵士乐时，女士指出：“interestingly enough, there's no agreed-upon definition of jazz. Indeed, there are many different styles of jazz... While there's no simple definition for it...”表明爵士乐没有统一定义且风格流派繁多，定义复杂多样（Its definition is varied and complicated）。因此答案为 A)。"
    },
    4: {
        "prompt": "What should you do to appreciate different styles of jazz, according to the woman?",
        "options": {
            "A": "Learn to play them.",
            "B": "Take music lessons.",
            "C": "Listen to them yourself.",
            "D": "Consult jazz musicians."
        },
        "answer": "C",
        "explanation": "【精析】细节辨认题。女士在对话末尾给出建议：“Honestly, the only way to know what jazz is is to listen to it yourself.”要真正领会爵士乐，唯一的途径就是亲自去聆听（Listen to them yourself）。因此答案为 C)。"
    },
    5: {
        "prompt": "What did the woman do this morning?",
        "options": {
            "A": "She paid her mortgage.",
            "B": "She called on the man.",
            "C": "She made a business plan.",
            "D": "She went to the bank."
        },
        "answer": "D",
        "explanation": "【精析】细节辨认题。对话开篇男士询问：“How did it go at the bank this morning?”女士回答：“Not well. My proposal was rejected.”表明女士今天早晨前往银行办理贷款事宜（She went to the bank）。因此答案为 D)。"
    },
    6: {
        "prompt": "Why was the woman's proposal rejected?",
        "options": {
            "A": "Her previous debt hadn’t been cleared yet.",
            "B": "Her credit history was considered poor.",
            "C": "She had apparently asked for too much.",
            "D": "She didn’t pay her mortgage in time."
        },
        "answer": "B",
        "explanation": "【精析】原因解释题。女士解释贷款申请被拒的首要原因：“For starters, they said my credit history was not good enough.”银行认为她的个人信用记录不够优良（Her credit history was considered poor）。因此答案为 B)。"
    },
    7: {
        "prompt": "What is the woman planning to do?",
        "options": {
            "A": "Pay a debt long overdue.",
            "B": "Buy a piece of property.",
            "C": "Start her own business.",
            "D": "Check her credit history."
        },
        "answer": "C",
        "explanation": "【精析】意图目的题。女士在对话中明确表露心声：“If I want to continue ahead with this dream of owning my own business, I have no other choice but to build up my own finances.”表明女士打算自主创业、成立自己的企业（Start her own business）。因此答案为 C)。"
    },
    8: {
        "prompt": "What does the man suggest the woman do?",
        "options": {
            "A": "Seek advice from an expert about fundraising.",
            "B": "Ask for smaller loans from different lenders.",
            "C": "Build up her own finances step by step.",
            "D": "Revise her business proposal carefully."
        },
        "answer": "B",
        "explanation": "【精析】建议细节题。男士向女士提出筹集资金的建议：“What if you asked for a smaller amount? Maybe you could gather capital from other sources, smaller loans from more lenders?”建议她从更多出借方那里申请较小金额的贷款（Ask for smaller loans from different lenders）。因此答案为 B)。"
    },
    9: {
        "prompt": "What do we learn about Leo Sanchez's farm?",
        "options": {
            "A": "It is profitable and environmentally friendly.",
            "B": "It is well located and completely automated.",
            "C": "It is small and unconventional.",
            "D": "It is fertile and productive."
        },
        "answer": "C",
        "explanation": "【精析】特征辨认题。篇章开篇介绍桑切斯农场的特点：“The national average farm size is around 440 acres, but his is only one acre... This is evidence of an experimental approach. It's an approach not dictated by the confines of conventional large-scale agriculture...”说明其农场规模小（仅1英亩）且打破传统常规（small and unconventional）。因此答案为 C)。"
    },
    10: {
        "prompt": "What has motivated Leo Sanchez and his fellow young farmers to engage in farming?",
        "options": {
            "A": "Their urge to make farming more enjoyable.",
            "B": "Their desire to improve farming equipment.",
            "C": "Their hope to revitalize traditional farming.",
            "D": "Their wish to set a new farming standard."
        },
        "answer": "D",
        "explanation": "【精析】动机目的题。篇章指出年轻农夫的内在动力：“Sanchez says he and many of his fellow young farmers are motivated by a desire to set a new standard for agriculture.”他们受到树立农业新标准的强烈愿望所激励（Their wish to set a new farming standard）。因此答案为 D)。"
    },
    11: {
        "prompt": "Why did Leo Sanchez buy a hand-operated weeding tool?",
        "options": {
            "A": "It saves a lot of electricity.",
            "B": "It needs little maintenance.",
            "C": "It causes hardly any pollution.",
            "D": "It loosens soil while weeding."
        },
        "answer": "D",
        "explanation": "【精析】工具功用题。篇章中介绍：“Recently, Sanchez bought a hand-operated tool which pulls out weeds and loosens soil.”该手动除草工具能够在拔草的同时疏松土壤（It loosens soil while weeding）。因此答案为 D)。"
    },
    12: {
        "prompt": "What do we learn from the passage about the food company Eat Grub?",
        "options": {
            "A": "It has turned certain insects into a new food source.",
            "B": "It has started to expand business outside the UK.",
            "C": "It has imported some exotic foods from overseas.",
            "D": "It has joined hands with Sainsbury’s to sell pet insects."
        },
        "answer": "A",
        "explanation": "【精析】企业事实题。篇章开头指出：“Eat Grub is Britain's first new food company that breaks western food boundaries by introducing edible insects as a new source of food.”Eat Grub将可食用昆虫转化为新型食品来源（turned certain insects into a new food source）。因此答案为 A)。"
    },
    13: {
        "prompt": "What does the speaker say about his first bite of roasted crickets?",
        "options": {
            "A": "It was really unforgettable.",
            "B": "It was a pleasant surprise.",
            "C": "It hurt his throat slightly.",
            "D": "It made him feel strange."
        },
        "answer": "B",
        "explanation": "【精析】感受体验题。讲述者亲自试吃烤蟋蟀：“But the first bite was a pleasant surprise. A little dry and lacking of taste, but at least a wing didn't get stuck in my throat.”咬下第一口时感到出人意料的惊喜（It was a pleasant surprise）。因此答案为 B)。"
    },
    14: {
        "prompt": "What does Eat Grub say about its dried crickets?",
        "options": {
            "A": "They are more tasty than beef, chicken or pork.",
            "B": "They are more nutritious than soups and salads.",
            "C": "They contain more protein than conventional meats.",
            "D": "They will soon gain popularity throughout the world."
        },
        "answer": "C",
        "explanation": "【精析】产品特征题。篇章指出该公司的宣传点：“The company boasts that its dried crickets contain more protein than beef, chicken and pork...”其蟋蟀干的蛋白质含量高过牛肉、鸡肉和猪肉等传统肉类（contain more protein than conventional meats）。因此答案为 C)。"
    },
    15: {
        "prompt": "What does the passage say about insect farming?",
        "options": {
            "A": "It is environmentally friendly.",
            "B": "It is a promising industry.",
            "C": "It requires new technology.",
            "D": "It saves huge amounts of labour."
        },
        "answer": "A",
        "explanation": "【精析】生态优势题。篇章对比了昆虫养殖与传统畜牧：“bugs do not use up large amounts of land, water or feed. And insect farming also produces far fewer greenhouse gases.”昆虫养殖占地耗水极少且排放更少温室气体，对生态环境十分友好（environmentally friendly）。因此答案为 A)。"
    },
    16: {
        "prompt": "Why do psychologists and educators study learning styles?",
        "options": {
            "A": "To categorize different types of learners.",
            "B": "To find out what students prefer to learn.",
            "C": "To understand the mechanism of the human brain.",
            "D": "To see if they are inherent traits affecting learning."
        },
        "answer": "D",
        "explanation": "【精析】目的意图题。讲座明确指出：“When psychologists and educators test for learning styles, they're trying to figure out whether these are inherent traits that affect how well students learn, instead of just a preference.”研究的目的是为了查明学习风格是否是影响学生学习成效的先天固有特质（inherent traits affecting learning）。因此答案为 D)。"
    },
    17: {
        "prompt": "What does the speaker say about one study mentioned in the 2008 review?",
        "options": {
            "A": "It was defective.",
            "B": "It was misguided.",
            "C": "It was original in design.",
            "D": "It was thought-provoking."
        },
        "answer": "A",
        "explanation": "【精析】批判评价题。讲述者评估支持学习风格假说的唯一研究：“But the study had some big flaws. The researchers excluded two-thirds of the original participants... And they didn't even report the actual test scores...”该项研究存在严重的漏洞缺陷（It was defective / had big flaws）。因此答案为 A)。"
    },
    18: {
        "prompt": "What message does the speaker want to convey about learning at the end of the talk?",
        "options": {
            "A": "Auditory aids are as important as visual aids.",
            "B": "Visual aids are helpful to all types of learners.",
            "C": "Reading plain texts is more effective than viewing pictures.",
            "D": "Scientific concepts are hard to understand without visual aids."
        },
        "answer": "B",
        "explanation": "【精析】主旨结论题。讲座结尾综合多项研究指出：“most people seem to learn better if they're taught in several ways, especially if one is visual... And everyone did better with the help of pictures.”视觉教具对所有类型的学习者都有实际助益（Visual aids are helpful to all types of learners）。因此答案为 B)。"
    },
    19: {
        "prompt": "What do people often feel guilty about according to the speaker?",
        "options": {
            "A": "Not playing a role in a workplace revolution.",
            "B": "Not benefiting from free-market capitalism.",
            "C": "Not earning enough money to provide for the family.",
            "D": "Not spending enough time on family life and leisure."
        },
        "answer": "D",
        "explanation": "【精析】心理现象题。讲话人开篇指出：“We may instead find ourselves feeling guilty about the time we didn't spend watching our children grow, or with our loved ones, or travelling, or on the cultural or leisure pursuits that bring us happiness.”人们内疚于未能花足够的时间陪伴家庭和享受休闲时光（Not spending enough time on family life and leisure）。因此答案为 D)。"
    },
    20: {
        "prompt": "What did leading economists predict 90 years ago?",
        "options": {
            "A": "People would be working only fifteen hours a week now.",
            "B": "The balance of power in the workplace would change.",
            "C": "Technological advances would create many new jobs.",
            "D": "Most workers could afford to have a house of their own."
        },
        "answer": "A",
        "explanation": "【精析】历史预测题。文中回顾九十年前经济学家的预言：“Nine decades ago, leading economists predicted that technological advances and rising productivity would mean that we'd be working a 15-hour week by now.”杰出经济学家曾预言如今人们每周只需工作15个小时（People would be working only fifteen hours a week now）。因此答案为 A)。"
    },
    21: {
        "prompt": "What is the result of denying workers right to make their own choices?",
        "options": {
            "A": "Loss of workers’ personal dignity.",
            "B": "Deprivation of workers’ creativity.",
            "C": "Deterioration of workers’ mental health.",
            "D": "Unequal distribution of working hours."
        },
        "answer": "C",
        "explanation": "【精析】因果后果题。文中阐述剥夺自主选择权的恶果：“denied the right to make our own choices. That's bad for us. It's hardly surprising that over half a million workers suffer from work-related mental health conditions each year.”导致数十万工人罹患心理疾病，严重损害心理健康（Deterioration of workers’ mental health）。因此答案为 C)。"
    },
    22: {
        "prompt": "What does the speaker say about the dream airport in Berlin?",
        "options": {
            "A": "It is the worst managed airport in German history.",
            "B": "It is now the biggest and busiest airport in Europe.",
            "C": "It has become something of a joke among Germans.",
            "D": "It has become a typical symbol of German efficiency."
        },
        "answer": "C",
        "explanation": "【精析】现状事实题。讲座描述柏林新机场：“Plagued by long delays, perpetual mismanagement, and ever-soaring costs, the airport has become something of a joke among Germans...”屡屡延期和管理不善使该机场沦为了德国民众口中的笑柄笑料（become something of a joke among Germans）。因此答案为 C)。"
    },
    23: {
        "prompt": "Why was there a need for a new airport in Berlin?",
        "options": {
            "A": "The city’s airports are outdated.",
            "B": "The city had just been reunified.",
            "C": "The city wanted to boost its economy.",
            "D": "The city wanted to attract more tourists."
        },
        "answer": "B",
        "explanation": "【精析】背景原因题。文中解释规划新机场的历史根源：“Planning for the new airport began in 1989. At the time, it became clear that the newly reunified Berlin would need a modern airport with far greater capacity than its existing airports.”1989年柏林刚刚重新统一，急需一座容量更大的现代化航空港（The city had just been reunified）。因此答案为 B)。"
    },
    24: {
        "prompt": "Why did Berlin postpone the opening of its dream airport again and again?",
        "options": {
            "A": "The municipal government kept changing hands.",
            "B": "The construction firm breached the contract.",
            "C": "Shortage of funding delayed its construction.",
            "D": "Problems of different kinds kept popping up."
        },
        "answer": "D",
        "explanation": "【精析】归纳原因题。文中列举了消防系统故障、线缆装错、门编号错误、扶梯过短等一系列接连不断的工程质量问题：“It wasn't just the smoke system, many other major problems subsequently emerged... The longer the delays continued, the more problems inspectors found.”各种问题接踵而至（Problems of different kinds kept popping up）。因此答案为 D)。"
    },
    25: {
        "prompt": "What happens while the airport remains unused?",
        "options": {
            "A": "Tourism industry in Berlin suffers.",
            "B": "All kinds of equipment gets rusted.",
            "C": "Huge maintenance costs accumulate.",
            "D": "Complaints by local residents increase."
        },
        "answer": "C",
        "explanation": "【精析】结果影响题。讲座结尾指出机场闲置的巨大代价：“the unused airport is resulting in massive costs. Every month it remains unopened costs between 9 and 10 million euros.”未启用的机场每月产生900万至1000万欧元的巨额闲置维护成本（Huge maintenance costs accumulate）。因此答案为 C)。"
    }
}

def main():
    target = Path("pipeline/data_2019_12_set2.py")
    with open(target, "w", encoding="utf-8") as f:
        f.write("#!/usr/bin/env python3\n")
        f.write('"""\nOfficial data for 2019-12-set2 CET-6 listening test:\n- 7 subparts with authentic titles, Chinese topics, and question ranges\n- Complete grammatical sentences with 100% paired authentic Chinese translations\n- 25 official CET-6 questions with options, answers, and explanations\n"""\n\n')
        f.write("SUBPARTS = ")
        pprint.pprint(SUBPARTS, stream=f, width=120, compact=False)
        f.write("\n\nQUESTIONS = ")
        pprint.pprint(QUESTIONS, stream=f, width=120, compact=False)
        f.write("\n")
    print(f"Successfully generated {target}")

if __name__ == "__main__":
    main()
