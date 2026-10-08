#!/usr/bin/env python3
"""
Curate 2016-06-set1 and 2016-12-set2 to 100% Acoustic Truth and Steve Jobs Standards.
"""

import json
import sqlite3
import shutil
import re
import difflib

DB_PATH = "data/sixsense.db"
shutil.copyfile(DB_PATH, "data/sixsense.db.bak_2016_truth")
print("Backed up database to data/sixsense.db.bak_2016_truth")

def clean_word(w):
    return re.sub(r"[^\w]", "", w).lower()

def align_sentences(sentences_data, whisper_words, sp_start, sp_end):
    aligned = []
    w_idx = 0
    total_w = len(whisper_words)

    while w_idx < total_w and whisper_words[w_idx]["start"] < sp_start - 0.5:
        w_idx += 1

    for s_idx, (speaker, s_text, zh_text) in enumerate(sentences_data):
        raw_words = s_text.split()
        norm_words = [clean_word(w) for w in raw_words if clean_word(w)]
        if not norm_words:
            continue

        best_start_idx = w_idx
        while best_start_idx < total_w and whisper_words[best_start_idx]["start"] < sp_start - 1.0:
            best_start_idx += 1

        search_window = 140
        best_ratio = 0.0
        best_range = None
        n_len = len(norm_words)

        for i in range(best_start_idx, min(best_start_idx + search_window, total_w)):
            if whisper_words[i]["start"] > sp_end + 3.0:
                break
            cand_end = min(i + n_len + 6, total_w)
            cand_words = [clean_word(whisper_words[k]["word"]) for k in range(i, cand_end) if clean_word(whisper_words[k]["word"])]
            cand_slice = cand_words[:n_len]

            sm = difflib.SequenceMatcher(None, norm_words, cand_slice)
            ratio = sm.ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                actual_end_k = min(i + len(cand_slice), total_w - 1)
                best_range = (i, actual_end_k)
                if ratio >= 0.95:
                    break

        if best_range and best_ratio >= 0.55:
            start_k, end_k = best_range
            t_start = whisper_words[start_k]["start"]
            t_end = whisper_words[end_k]["end"]
            w_idx = max(w_idx, start_k + int(n_len * 0.7))
            matched_words = [
                {
                    "word": whisper_words[k]["word"].strip(),
                    "start": round(whisper_words[k]["start"], 2),
                    "end": round(whisper_words[k]["end"], 2),
                    "score": round(whisper_words[k].get("probability", 1.0), 3)
                }
                for k in range(start_k, end_k + 1)
            ]
        else:
            if aligned:
                prev_end = aligned[-1]["end"]
                t_start = prev_end
                t_end = min(t_start + max(1.5, len(raw_words) * 0.35), sp_end)
            else:
                t_start = sp_start
                t_end = min(t_start + max(1.5, len(raw_words) * 0.35), sp_end)
            matched_words = []

        t_start = max(sp_start, min(t_start, sp_end))
        t_end = max(t_start + 0.3, min(t_end, sp_end))

        aligned.append({
            "speaker": speaker,
            "start": round(t_start, 2),
            "end": round(t_end, 2),
            "en": s_text,
            "zh": zh_text,
            "words": matched_words
        })

    # Monotonic smoothing
    for i in range(1, len(aligned)):
        prev = aligned[i-1]
        curr = aligned[i]
        if curr["start"] < prev["start"]:
            curr["start"] = prev["start"]
        if curr["end"] <= curr["start"]:
            curr["end"] = min(curr["start"] + 1.2, sp_end)
        if prev["end"] > curr["start"]:
            overlap = prev["end"] - curr["start"]
            if overlap > 0.4:
                mid = round((prev["end"] + curr["start"]) / 2, 2)
                prev["end"] = mid
                curr["start"] = mid
            else:
                curr["start"] = prev["end"]

    for s in aligned:
        s["start"] = max(sp_start, min(s["start"], sp_end))
        s["end"] = max(s["start"] + 0.3, min(s["end"], sp_end))

    return aligned

# =========================================================================
# 2016-06-set1
# =========================================================================
SENTS_2016_06_1 = {
    "conv-1": {
        "sp_start": 42.56,
        "sp_end": 170.56,
        "sentences": [
            ("M", "So, how long have you been a Market Research Consultant?", "请问你从事市场调研顾问这一职业有多久了？"),
            ("W", "Well, I started straight after finishing university.", "嗯，我大学毕业后就直接入行了。"),
            ("M", "Did you study market research?", "你在大学里学的是市场调研专业吗？"),
            ("W", "Yeah, and it really helped me to get into the industry.", "是的，这确实帮我顺利敲开了行业大门。"),
            ("W", "But I have to say that it's more important to get experience in different types of market research to find out exactly what you're interested in.", "但我必须说，在不同类型的市场调研中积累实战经验更为关键，这样才能弄清楚自己真正的兴趣所在。"),
            ("M", "So, what are you interested in?", "那你现在最感兴趣的方向是什么？"),
            ("W", "Well, at the moment, I specialize in quantitative advertising research, which means that I do two types of projects.", "嗯，目前我专注于定量广告研究，这意味着我主要负责两类项目。"),
            ("W", "Trackers, which are ongoing projects that look at trends or customer satisfaction over a long period of time.", "一类是追踪研究，即长期观察市场趋势或客户满意度的持续性项目。"),
            ("W", "The only problem with trackers is that it takes up a lot of your time, but you do build up a good relationship with the client.", "追踪研究唯一的问题是耗费大量时间，但你确实能借此与客户建立起稳固良好的合作关系。"),
            ("W", "I also do a couple of ad-hoc jobs, which are much shorter projects.", "我还会做一些专项特别项目，这类项目的周期要短得多。"),
            ("M", "What exactly do you mean by ad-hoc jobs?", "你所说的专项项目具体是指什么呢？"),
            ("W", "It's basically when companies need quick answers to their questions about their consumers' habits.", "基本上是指当企业需要针对其消费者的消费习惯迅速获得疑问的解答时所做的调研。"),
            ("W", "They just ask for one questionnaire to be sent out, for example.", "例如，他们通常只要求发放一份调查问卷。"),
            ("W", "So, the time you spend on an ad-hoc project tends to be fairly short.", "因此，你在专项项目上花费的时间往往相对较短。"),
            ("M", "Which do you prefer, trackers or ad-hoc?", "那么这两者中你更倾向于哪一种，追踪研究还是专项项目？"),
            ("W", "I like doing both, and in fact, I need to do both at the same time to keep me from going crazy.", "两种我都喜欢做；事实上，我需要两者并重进行，才不至于让自己抓狂。"),
            ("W", "I need the variety.", "我需要这种多样性与新鲜感。"),
            ("M", "Can you just explain what process you go through with a new client?", "你能解释一下对接新客户时你会经历哪些流程吗？"),
            ("W", "Well, together we decide on the methodology and the objectives of the research.", "嗯，我们首先会共同确定调研的方法论和核心目标。"),
            ("W", "I then design a questionnaire.", "随后由我负责设计调查问卷。"),
            ("W", "Once the interviewers have been briefed, I send the client a schedule and then they get back to me with deadlines.", "在对访问员进行培训宣讲后，我会向客户发送进度排期表，随后客户会与我确认最终截止日期。"),
            ("W", "Once the final charts and tables are ready, I have to check them and organize a presentation.", "当最终的图表和数据表格制作完成后，我需要逐一审核并组织汇报宣讲。"),
            ("M", "Hmm, one last question.", "嗯，最后一个问题。"),
            ("M", "What do you like and dislike about your job?", "对于这份工作，你喜欢和不喜欢的地方分别是什么？"),
            ("W", "As I said, variety is important, and as for what I don't like, it has to be the checking of charts and tables.", "正如我刚才所说，工作多样性很吸引我；至于不喜欢的，那肯定非核对图表和数据表格莫属了。")
        ]
    },
    "conv-2": {
        "sp_start": 248.68,
        "sp_end": 373.82,
        "sentences": [
            ("W", "Hello, I'm here with Frederick.", "大家好，今天我和弗雷德里克在一起。"),
            ("W", "Now Fred, you went to university in Canada?", "弗雷德，你以前是在加拿大上的大学对吧？"),
            ("M", "Yeah, that's right.", "是的，没错。"),
            ("W", "Okay, and you have very strong views about universities in Canada.", "好的，你对加拿大的大学教育体制有着非常鲜明的看法。"),
            ("W", "Could you please explain?", "能具体给我们讲讲吗？"),
            ("M", "Well, we don't have private universities in Canada.", "嗯，在加拿大我们没有私立大学。"),
            ("M", "They're all public.", "所有的大学都是公立的。"),
            ("M", "All the universities are owned by the government.", "所有的大学都归政府所有和管理。"),
            ("M", "So there's the Ministry of Education in charge of creating the curriculum for the universities, and so there's not much room for flexibility.", "因此由教育部全权负责制定大学的课程大纲，这就导致缺乏灵活机动的空间。"),
            ("M", "Since it's a government-operated institution, things don't move very fast.", "由于属于政府运营的机构，各项事务的推进办事效率往往很慢。"),
            ("M", "If you want something to be done, then their staff do not have so much incentive to help you, because he's a worker for the government.", "如果你想办成某件事，工作人员缺乏主动协助你的动力，因为他们都是拿政府固定薪水的雇员。"),
            ("M", "So I don't think it's very efficient.", "所以我觉得这种体制效率并不高。"),
            ("M", "However, there are certain advantages of public universities, such as the fees being free.", "不过公立大学也有其明显优势，比如学费是免除的。"),
            ("M", "You don't have to pay for your education.", "你无需为接受高等教育支付高昂费用。"),
            ("M", "But the system is inefficient, and it does not work that well.", "但整个体制效率低下，实际运转成效并不理想。"),
            ("W", "Yeah, I can see your point.", "嗯，我完全理解你的意思。"),
            ("W", "But in the United States, we have many private universities, and I think there are large bureaucracies also.", "但在美国，我们有许多私立大学，我认为同样存在着庞大的官僚机构。"),
            ("W", "Maybe people don't act that much differently, because it's the same thing working for a private university.", "人们的行事方式或许并无太大差别，毕竟在私立大学工作本质上也差不多。"),
            ("W", "They get paid for their job.", "他们也是按劳拿薪水。"),
            ("W", "I don't know if they're that much more motivated to help people.", "我不确定他们在帮助学生方面是否真的会有更高的积极性。"),
            ("W", "Also, we have a problem in the United States that usually only wealthy kids go to the best schools, and it's kind of a problem, actually.", "而且在美国我们面临一个问题：往往只有富裕家庭的孩子才能进最好的名校，这其实是个挺严重的社会问题。"),
            ("M", "I agree with you.", "我赞同你的看法。"),
            ("M", "I think it's a problem because you're not giving equal access to education to everybody.", "我认为这确实是个问题，因为这意味着你没有向所有人提供公平的受教育机会。"),
            ("W", "It's not easy, but having only public universities also might not be the best solution.", "这确实不容易平衡，但单纯只保留公立大学恐怕也未必是最佳方案。"),
            ("W", "Perhaps we can learn from Japan, where they have a system of private and public universities.", "或许我们可以借鉴日本的做法，他们实行的是公私立大学并存的双轨体制。"),
            ("W", "Now in Japan, public universities are considered to be the best.", "在日本，公立大学通常被认为是最顶尖优秀的。"),
            ("M", "Right. It's the exact opposite in the United States.", "对，这和美国的情况恰好截然相反。"),
            ("M", "So, as you see, it's very hard to say which one is better.", "因此正如你所见，很难一概而论究竟哪种体制更为优越。"),
            ("W", "Right. A good point.", "是的，很有见地。")
        ]
    },
    "pass-1": {
        "sp_start": 484.93,
        "sp_end": 596.05,
        "sentences": [
            ("M", "A recent International Labor Organization report says the deterioration of real wages around the world calls into question the true extent of an economic recovery,", "国际劳工组织近期发布的一份报告指出，全球范围内实际工资水平的恶化，让人们对经济复苏的真实程度打上了一个大大的问号，"),
            ("M", "especially if government rescue packages are phased out too early.", "尤其是如果各国政府过早撤出经济救助计划的话更是如此。"),
            ("M", "The report warns the picture on wages is likely to get worse this year, despite indications of an economic rebound.", "报告警告称，尽管有经济回暖反弹的迹象，但今年薪酬形势很可能会进一步恶化。"),
            ("M", "Patrick Belser, an International Labor Organization specialist, says declining wage rates are linked to the levels of unemployment.", "国际劳工组织薪酬专家帕特里克·贝尔瑟指出，工资增长率的走低与失业率水平息息相关。"),
            ("M", "The quite dramatic unemployment figures, which we now see in some of the countries, strongly suggest that there will be greater pressure on wages in the future,", "目前在某些国家所显现出的令人触目惊心的失业数据强烈预示着，未来的薪酬水平将面临更沉重的下行压力，"),
            ("M", "as more people will be unemployed, more people will be looking for jobs, and the pressure on employers to raise wages to attract workers will decline.", "因为随着失业人口增加、更多人涌入求职市场，雇主通过提高薪资来招揽工人的竞争压力将会显著减弱。"),
            ("M", "So we expect that the second part of the year will not be very good in terms of wage growth.", "因此我们预计，今年下半年在薪酬增长方面的表现将不容乐观。"),
            ("M", "The report finds more than a quarter of the countries experienced flat or falling monthly wages in real terms.", "该报告发现，超过四分之一的国家在剔除通胀因素后的实际月薪呈现持平或下滑态势。"),
            ("M", "They include the United States, Austria, Costa Rica, South Africa, and Germany.", "这些国家包括美国、奥地利、哥斯达黎加、南非以及德国。"),
            ("M", "International Labor Organization economists say some nations have come up with policies to lessen the impact of lower wages during the economic crisis.", "国际劳工组织的经济学家表示，部分国家已经制定出应对政策，以减缓经济危机期间薪酬下降带来的冲击。"),
            ("M", "An example of these is work sharing with government subsidies.", "其中的一个典型例子就是政府提供补贴的工作分担制。"),
            ("M", "Under this scheme, the number of individual working hours is reduced in an effort to avoid layoffs.", "在该机制下，通过缩短员工个人的工作时长，以最大限度避免裁员。"),
            ("M", "For this scheme to work, the government must provide wage subsidies to compensate for lost pay due to the shorter hours.", "而要使该计划行之有效，政府必须发放薪资补贴，以弥补工人们因缩短工时而损失的收入。")
        ]
    }
}

# =========================================================================
# 2016-12-set2
# =========================================================================
SENTS_2016_12_2 = {
    "conv-1": {
        "sp_start": 44.89,
        "sp_end": 160.71,
        "sentences": [
            ("M", "Guess what? The worst food I ever had was in France.", "你猜怎么着？我这辈子吃过最难吃的食物竟然是在法国碰上的。"),
            ("W", "Really? That's odd. I thought the French were all good cooks.", "真的吗？真稀奇。我还以为法国人个个都精通烹饪呢。"),
            ("M", "Yes, that's right. I suppose it's really like anywhere else though.", "是啊，确实如此。不过我想其实各地都一样，"),
            ("M", "You know, some places are good, some bad.", "你知道的，有的地方做得好，有的地方做得差。"),
            ("M", "But it's really all our own fault.", "但这完全是我们自讨苦吃。"),
            ("W", "What do you mean?", "你这话是什么意思？"),
            ("M", "Well, it was the first time I'd been to France.", "嗯，那是我第一次去法国。"),
            ("M", "This was years ago when I was at school.", "那是多年前我还在上学的时候。"),
            ("M", "I went there with my parents' friends from my father's school.", "当时我和我父母的朋友一起去，他们是我父亲学校的同事。"),
            ("M", "They'd hired a coach to take them to Switzerland.", "他们租了一辆大巴车打算一路开往瑞士。"),
            ("W", "A school trip?", "是一次学校旅行吗？"),
            ("M", "Right. Most of them had never been abroad before.", "对。他们中大多数人以前从没出过国。"),
            ("M", "We'd crossed the English Channel at night, and we set off through France.", "我们连夜渡过了英吉利海峡，然后乘车穿越法国。"),
            ("M", "And breakfast time arrived, and the coach driver had arranged for us to stop at this little cafe.", "到了吃早餐的时间，大巴司机安排我们在一家路边小咖啡馆停下。"),
            ("M", "There we all were, tired and hungry, and then we made the great discovery.", "当时大家都又累又饿，接着我们有了一个‘重大发现’。"),
            ("W", "What was that?", "发现了什么？"),
            ("M", "Bacon and eggs. Fantastic. The real English breakfast.", "培根煎蛋！太棒了，地道正宗的英式早餐。"),
            ("M", "Yes. Anyway, we didn't know any better. So we had it and...", "是啊。反正当时我们也没见识，于是就要了这道餐，然后……"),
            ("W", "What was it like? Disgusting?", "味道怎么样？很恶心吗？"),
            ("M", "Oh, it was incredible. They just got a bowl and put some fat in it.", "噢，简直难以置信！他们直接拿了个大碗，往里面倒了些油脂。"),
            ("M", "And then they put some bacon in the fat, broke an egg over the top, and put the whole lot in the oven for about 10 minutes.", "接着把几片培根扔进油里，上面打了个生鸡蛋，然后把整碗东西放进烤箱烤了大概十分钟。"),
            ("W", "In the oven, you're joking. You can't cook bacon and eggs in the oven.", "放进烤箱？你在开玩笑吧！培根煎蛋哪能放烤箱里做啊！"),
            ("M", "Well, they must have done it that way. It was hot, but it wasn't cooked.", "可他们偏偏就是这么做的。端出来滚烫滚烫的，但根本没熟。"),
            ("M", "There was just this egg floating about in gallons of fat and raw bacon.", "就只看到那只鸡蛋漂在一大滩油脂和生培根上面。"),
            ("W", "Did you actually eat it?", "你们真的吃下去了吗？"),
            ("M", "No. Nobody did. They wanted to turn round and go home.", "没，根本没人动口。大家恨不得立刻掉头打道回府。"),
            ("M", "You know, back to tea bags and fish and chips. You can't blame them, really.", "回去喝普通的茶包、吃炸鱼薯条。说实在的，真怪不得大家。"),
            ("M", "Anyway, the next night we were all given another foreign speciality.", "不管怎么说，第二天晚上我们又被端上了一道外国特色菜。"),
            ("W", "What was that?", "是什么？"),
            ("M", "Snails. That really finished them off.", "法式焗蜗牛。这下彻底把大家击垮崩溃了。"),
            ("M", "Lovely holiday that was.", "真是个‘美好难忘’的假期啊。")
        ]
    },
    "conv-2": {
        "sp_start": 242.86,
        "sp_end": 364.72,
        "sentences": [
            ("M", "You say your shop has been doing well. Could you give me some idea of what doing well means, in facts and figures?", "你说你的店铺一直经营得很红火。你能用具体的事实和数据，向我说明一下所谓‘红火’是指什么吗？"),
            ("W", "Well, doing well means averaging 1,200 pounds or more a week for about seven years,", "嗯，‘红火’意味着在过去的七年时间里，每周平均营业额达到1200英镑以上，"),
            ("W", "making almost a quarter of a million pounds, and doing well means your earnings are rising.", "累计创造了将近25万英镑的收入，而且‘红火’还意味着你的营收一直在稳步增长。"),
            ("W", "Last year we did slightly over 50,000, and this year we hope to do more than 60,000.", "去年我们的营业额略微超过5万英镑，而今年我们希望能突破6万英镑大关。"),
            ("W", "So that's good if we continue to rise.", "所以如果我们能保持这种上升势头，前景就非常光明。"),
            ("M", "Now that's gross earnings I assume. What about your expenses?", "我想这应该指的是毛收入吧。那你们的各项开支费用情况如何呢？"),
            ("W", "Yes, that's gross.", "是的，那是毛营业额。"),
            ("W", "The expenses of course go up steadily, and since we've moved to this new shop, the expenses have increased greatly because it's a much bigger shop.", "各项经营成本自然也在平稳上涨；尤其是自从搬到这间新店铺后，开支大幅增加，因为这间店面要大得多。"),
            ("W", "So I couldn't say exactly what our expenses are.", "所以我没法给出确切的开支数额。"),
            ("W", "There's something in the region of six or 7,000 pounds a year, which is not high.", "大约在每年六千到七千英镑上下，这个数字其实并不算高。"),
            ("W", "Commercially speaking, it's fairly low, and we try to keep our expenses as low as we can.", "从商业角度来看这相当低了，而且我们始终在竭尽全力把经营成本压到最低。"),
            ("M", "And your prices are much lower than the same goods in shops around about.", "而且你们商品的价格比周围其他商店的同类商品要低得多。"),
            ("M", "How do the local shopkeepers feel about having a shop doing so well in their midst?", "身处这样一家生意蒸蒸日上的店铺周边，当地的其他店主对此有何看法？"),
            ("W", "Perhaps a lot of them don't realize how well we're doing because we don't make a point of publicizing.", "或许他们中很多人根本没意识到我们生意这么好，因为我们从不特意对外张扬宣传。"),
            ("W", "That was a lesson we learned very early on.", "这是我们很早以前就吸取的一大教训。"),
            ("W", "We were very friendly with all local shopkeepers, and we happened to mention to a local shopkeeper how much we had made that week.", "我们起初和当地所有店主都处得很融洽，有一次碰巧无意中向一位当地店主透露了我们那周赚了多少钱。"),
            ("W", "He was very unhappy and never as friendly again.", "他听完非常不高兴，从此态度就再也不像从前那样友善了。"),
            ("W", "So we make a point of never publicizing the amount of money we make.", "因此我们特意立下一条规矩：绝不对外公开我们赚了多少钱。"),
            ("W", "But we're on very good terms with all the shops.", "不过我们目前和附近所有商铺的关系都维持得非常融洽。"),
            ("W", "None of them have ever complained that we're putting them out of business or anything like that.", "从来没有任何一家抱怨说我们抢了他们的饭碗或是逼他们关门之类的话。"),
            ("W", "I think it's a nice friendly relationship.", "我认为这是一种非常良性友好的睦邻关系。"),
            ("W", "Maybe if they did know what we made, perhaps they wouldn't be so friendly.", "不过要是他们真的知道我们能赚多少钱，可能也就不会这么客气友善了。")
        ]
    },
    "pass-1": {
        "sp_start": 480.78,
        "sp_end": 598.50,
        "sentences": [
            ("M", "Birds are famous for carrying things around.", "鸟类以四处携带东西而闻名遐迩。"),
            ("M", "Some, like homing pigeons, can be trained to deliver messages and packages.", "有些鸟，比如信鸽，经过专业训练可以递送书信信件和小包裹。"),
            ("M", "Other birds unknowingly carry seeds that cling to them for the ride.", "另一些鸟则会在不经意间携带紧紧附着在羽毛上的植物种子四处搭便车传播。"),
            ("M", "Canadian scientists have found a worrisome new example of the power that birds have to spread stuff around.", "加拿大科学家们发现了一个令人忧心忡忡的新例证，证实了鸟类具有广泛扩散有害物质的能力。"),
            ("M", "Way up north in the Canadian Arctic, seabirds are picking up dangerous chemicals in the ocean and delivering them to ponds near where the birds live.", "在遥远的加拿大北极高纬度地区，海鸟从大洋中摄取危险的化学物质，并将其带回自己栖息地附近的淡水池塘中。"),
            ("M", "Some 10,000 pairs of the birds called fulmars, a kind of Arctic seabird, make their nests on Devon Island north of the Arctic Circle.", "一种名为管鼻鹱的北极海鸟，约有一万对在北极圈以北的德文岛上筑巢繁殖。"),
            ("M", "The fulmars travel some 400 kilometers over the sea to find food.", "这些管鼻鹱在觅食时需要飞越海面远达400公里。"),
            ("M", "When they return home, their droppings end up all around their nesting sites, including in nearby ponds.", "当它们返回巢穴时，其排泄物散落在营巢地的角角落落，包括周边的池塘水体中。"),
            ("M", "Previously, scientists noticed pollutants arriving in the Arctic with the wind.", "此前，科学家们已经注意到污染物会随着大气环流季风被输送到北极地区。"),
            ("M", "Salmon also carry dangerous chemicals as the fish migrate between rivers and the sea.", "鲑鱼在江河与海洋之间洄游迁移的过程中，也会携带危险的化学物质。"),
            ("M", "The bodies of fish and other meat eaters can build up high levels of the chemicals.", "鱼类以及其他肉食性动物的体内能够富集极高浓度的化学毒素。"),
            ("M", "To test the polluting power of fulmars, researchers collected samples of deposit from 11 ponds on Devon Island.", "为了检测管鼻鹱的污染扩散威力，研究人员从德文岛上的11个池塘中采集了沉积物样本。"),
            ("M", "In ponds closest to the colony, the results showed there were far more pollutants than in ponds less affected by the birds.", "检测结果显示，在距离海鸟群落最近的池塘中，污染物含量远高于受海鸟影响较小的池塘。"),
            ("M", "The pollutants in the ponds appear to come from fish that fulmars eat when they're out on the ocean.", "池塘中的污染物显然来源于管鼻鹱在远海捕食所吞食的鱼类体内富集的物质。"),
            ("M", "People who live, hunt, or fish near bird colonies need to be careful, the researchers say.", "研究人员提醒称，在海鸟栖息群落周边生活、狩猎或捕鱼的人群务必提高警惕。"),
            ("M", "The birds don't mean to cause harm, but the chemicals they carry can cause major problems.", "鸟类本无意造成伤害，但它们所携带的化学毒物却可能引发极其严重的生态健康危机。")
        ]
    },
    "pass-2": {
        "sp_start": 685.19,
        "sp_end": 818.50,
        "sentences": [
            ("W", "In recent years, the death rate among American centenarians, people who have lived to age 100 or older, has decreased,", "近年来，美国百岁老人——即活到100岁及以上的人群——的死亡率有所下降，"),
            ("W", "dropping 14% for women and 20% for men from 2008 to 2014.", "从2008年到2014年间，女性百岁老人死亡率下降了14%，男性百岁老人死亡率下降了20%。"),
            ("W", "The leading causes of death in this age group are also changing.", "该年龄段人群的主要致死病因结构也在发生显著变化。"),
            ("W", "In 2000, the top 5 causes of death for centenarians were heart disease, stroke, flu, cancer, and Alzheimer's disease.", "在2000年，百岁老人的前五大死因依次为心脏病、中风、流感、癌症和阿尔茨海默病。"),
            ("W", "But by 2014, the death rate from Alzheimer's disease for this age group had more than doubled, increasing from 3.8% to 8.5%,", "但到了2014年，该群体死于阿尔茨海默病的比例翻了一倍多，从3.8%激增至8.5%，"),
            ("W", "making the progressive brain disease the second leading cause of death for centenarians.", "使得这一进行性脑退化疾病跃升为百岁老人的第二大致命死因。"),
            ("W", "One reason for the rise in deaths from Alzheimer's disease in this group may be that developing this condition remains possible even after people beat the odds of dying from other diseases such as cancer.", "该人群中阿尔茨海默病致死率攀升的一个原因可能在于：即便老人们侥幸战胜了癌症等其他致命疾病，患上这一神经退行性病变的风险依然存在。"),
            ("W", "People physically fit enough to survive over 100 years, ultimately give in to diseases such as Alzheimer's which affects the mind and cognitive function.", "那些身体机能足够强健、能活过百岁的高龄老人，最终也不得不屈服于侵蚀心智与认知功能的阿尔茨海默病。"),
            ("W", "In other words, it appears their minds give out before their bodies do.", "换而言之，他们的大脑心智似乎往往比身体机能更早一步走向衰竭。"),
            ("W", "On the other hand, the death rate from flu dropped from 7.4% in 2000 to 4.1% in 2014.", "另一方面，百岁老人死于流感的比例从2000年的7.4%显著下降至2014年的4.1%。"),
            ("W", "That pushed flu from the third leading cause of death to the fifth.", "这使得流感从原本的第三大致死病因退居至第五位。"),
            ("W", "Overall, the total number of centenarians is going up.", "总体而言，百岁老人的总人口数量呈现上升趋势。"),
            ("W", "In 2014, there were 72,197 centenarians compared to 50,281 in 2000.", "2014年美国共有72,197名百岁老人，而2000年这一数字为50,281人。"),
            ("W", "But because this population is getting larger, the number of deaths in this group is also increasing.", "然而由于该人口基数不断扩大，这一高龄群体的死亡绝对人数也在水涨船高。"),
            ("W", "18,434 centenarians died in 2000, whereas 25,914 died in 2014.", "2000年有18,434名百岁老人去世，而2014年的死亡人数则增至25,914人。")
        ]
    }
}

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

def apply_curation(exam_id, subpart_configs):
    with open(f"data/derived/exams/{exam_id}/whisper_full.json") as f:
        w_data = json.load(f)
    whisper_words = [w for seg in w_data for w in seg.get('words', [])]

    for sp_key, conf in subpart_configs.items():
        sp_id = f"{exam_id}-{sp_key}"
        sp_start = conf["sp_start"]
        sp_end = conf["sp_end"]
        raw_sents = conf["sentences"]

        aligned = align_sentences(raw_sents, whisper_words, sp_start, sp_end)

        # Delete old sentences for this subpart
        c.execute("DELETE FROM sentences WHERE subpart_id = ?", (sp_id,))

        # Get section_id
        c.execute("SELECT section_id FROM subparts WHERE id = ?", (sp_id,))
        sec_id = c.fetchone()[0]

        # Insert new aligned sentences (temporary order_num, will renumber entire exam later)
        for i, s in enumerate(aligned):
            sent_id = f"{sp_id}-{i+1:04d}"
            c.execute("""
                INSERT INTO sentences (id, exam_id, section_id, subpart_id, order_num, speaker, start_time, end_time, english, chinese, words_json, confidence)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sent_id, exam_id, sec_id, sp_id, i+1, s["speaker"], s["start"], s["end"], s["en"], s["zh"], json.dumps(s["words"], ensure_ascii=False), 1.0
            ))

        # Update subpart metadata
        first_st = aligned[0]["start"]
        last_et = aligned[-1]["end"]
        dur = round(last_et - first_st, 2)
        cnt = len(aligned)
        c.execute("""
            UPDATE subparts
            SET start_time = ?, end_time = ?, duration = ?, sentence_count = ?
            WHERE id = ?
        """, (first_st, last_et, dur, cnt, sp_id))
        print(f"Updated {sp_id}: {cnt} sentences, [{first_st}s - {last_et}s], dur={dur}s")

    # Renumber order_num across entire exam
    c.execute("SELECT id, order_num FROM subparts WHERE exam_id = ? ORDER BY order_num", (exam_id,))
    subparts = c.fetchall()

    global_order = 1
    for sp_id, _ in subparts:
        c.execute("SELECT id FROM sentences WHERE subpart_id = ? ORDER BY start_time, id", (sp_id,))
        s_ids = [r[0] for r in c.fetchall()]
        for s_id in s_ids:
            c.execute("UPDATE sentences SET order_num = ? WHERE id = ?", (global_order, s_id))
            global_order += 1

    print(f"Renumbered {exam_id}: total {global_order - 1} sentences.")

print("\n--- Applying 2016-06-set1 ---")
apply_curation("2016-06-set1", SENTS_2016_06_1)

print("\n--- Applying 2016-12-set2 ---")
apply_curation("2016-12-set2", SENTS_2016_12_2)

conn.commit()
conn.close()
print("\nAll changes successfully committed to database!")
