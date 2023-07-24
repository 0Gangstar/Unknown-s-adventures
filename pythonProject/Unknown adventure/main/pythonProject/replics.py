
# класс реплик
# мб класс свойств
# каждая часть свойства может быть имеет отдельное условие
# у челов не обязательно могут быть параметры и могут быть свои условия
# если без скобок свойство, то в скобки засунть

all_replices = {"r": ["haha Monkey sdfsdsfsdfs /- sfdfsfssdsfd", "bruh bruh bruh"], "r2": ["show_person1", "set_person1(undertaker_icon)", "Well lets go crushing women faces", "hide_person1"],
                "r4": ["I repeat this word only three times. You Understand?"], "r5": ["Go Fuck yourself"],
                "r6": ["You have apple? Give it to me!"], "r7": ["Ho ho time to fuck, take this."], "r8": ["set_person1(player_icon)", "show_person1", "Good evening mister undertaker!", "hide_person1"],
                "r9": ["show_person1", "set_person1(undertaker_icon)", "Ho ho time to fuck, take this.", "hide_person1"],
                "r11": ["Ooh you have a bat? Lets celebrate and suck some dick"], "r12": ["rrrrrrr dont talk with me until you got a bat!"],
                "r13": ["hide_person1", "Осторожно! Овраг!", "set_person1(player_icon)", "show_person1", "Это бездна. Много кто туда падал, но никто так и не вернулся."],
                "r14": ["hide_person1", "Он не поверил, что градусов всего 360, и пытался с тех пор найти ещё"],
                "r15": ["hide_person1", "Однажды он пялился на медсестру, тогда она ему сказала -Дыру во мне просверлишь! /- "
                                        "С тех пор он верит, что у него есть такая способность и практикует этот дар на стене"],
                "r16": ["hide_person1", "-Эй! Слышь! Ты как сюда попал?!", "Слышь, старшой! Тут палево у нас. Наверняка подставной!", "-Гасите свет.", "Ну, парниша, без обид..."],
                "r17": ["set_person1(ded_icon)", "show_person1", "Что? Хочешь, чтобы мы ушли с площадки?", "Тебя же постоянно погружало в тоску её пустота.", "Хорошо. Но сначала принеси мне то, что считаешь достойной платой.", "hide_person1"],
                "r18": ["set_person1(ded_icon)", "show_person1", "Я всё ещё жду достойную оплату", "hide_person1"], "r19": ["set_person1(ded_icon)", "show_person1", "Что ж... Я вижу...", "Надеюсь у тебя всё получится", "Прощай.", "hide_person1"],
                "r20": ["set_person1(player_icon)", "show_person1", "Мой дом. Но я не могу вернуться, пока не посмотрю выступление.", "hide_person1"],
                "r21": ["hide_person1", "Внимание! Кладбище направо до упора", "Берегитесь!", "Хорошо отдохнуть!", "set_person1(player_icon)", "show_person1", "Туда нам надо!", "hide_person1"],
                "r22": ["set_person1(player_icon)", "show_person1", " Я не могу вернутся. Я на верном пути. Я бы мог вернуться если бы начал сначала..."],
                "r23": ["set_person1(who)", "show_person1", "Ах ха ха ха ха ха", "Опа! Хм... А ты сильный?"]

                }



# all_replices = {"r": (None, -1, ["haha Monkey sdfsdsfsdfs /- sfdfsfssdsfd", "bruh bruh bruh"]), "r2": (None, -1, ["Well lets go crushing women faces"]),
#                 "r4": (None, 3, ["I repeat this word only three times. You Understand?"]), "r5": (None, 1, ["Go Fuck yourself"]),
#                 "r6": (["have_item", "apple"], 1, 1, ["You have apple? Give it to me!"]), "r7": (None, 1, ["Ho ho time to fuck, take this."]),  }


all_properties = {"prop1": [None, 1, (["replic", "r8"], ["replic", "r9"], ["get_item", "bat", 1])], "prop2": [None, -1, [["replic", "r2"]]],
                  "prop3": [["have_item(bat)", True], 1, [["replic", "r11"]]], "prop4": [["have_item(bat)", False], -1, [["replic", "r12"]]],
                  "prop5": [None, -1, [["door", "home", "№3"]]], "tablet_prop": [None, -1, [["replic", "r13"]]], "psycho_ded": [None, -1, [["replic", "r14"]]],
                  "psycho_ded2": [None, -1, [["replic", "r15"]]], 'shnir': [None, 1, [["replic", "r16"], ["get_darker"], ["kill"]]],
                  "swing_ded": [None, 1, [["replic", "r17"]]], "swing_ded3": [["have_item(flower seeds)", False], -1, [["replic", "r18"]]],
                  "swing_ded2": [["have_item(flower seeds)", True], 1, [["replic", "r19",], ["get_darker"], ["illusion_off"], ["get_lighter"]]],
                  "chest": [None, 1, [["get_item", "flower seeds", 1]]],
                  "toGraveyardPath": [None, -1, [["door", "way_to_graveyard", "1"]]], "toFirst": [None, 1, [["replic", "r22"]]],
                  "home": [None, 1, [["replic", "r20"]]], "sign": [None, 1, [["replic", "r21"]]],
                  "end": [None, 1, [["replic", "r23"], ["get_darker"], ["kill"]]], "toGraveyard": [None, 1, [["door", "graveyard", "2"]]]}
