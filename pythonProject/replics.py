
# класс реплик
# мб класс свойств
# каждая часть свойства может быть имеет отдельное условие
# у челов не обязательно могут быть параметры и могут быть свои условия
# если без скобок свойство, то в скобки засунть


all_replices = {
                "r13": ["hide_person1", "Осторожно! Овраг!", "set_person1(player_icon)", "show_person1", "Это бездна. Много кто туда падал, но никто так и не вернулся.", "hide_person1"],
                "r14": ["hide_person1", "Он не поверил, что градусов всего 360, и пытался с тех пор найти ещё"],
                "r15": ["hide_person1", "Раньше ему постоянно говорили, что он сверлит своим взглядом. /- "
                                        "С тех пор он практикует этот дар на стене"],
                "r16": ["hide_person1", "-Эй! Слышь! Ты как сюда попал?!", "Слышь, старшой! Тут палево у нас. Наверняка подставной!", "-Гасите свет.", "Ну, парниша, без обид..."],
                "r17": ["set_person1(ded_icon)", "show_person1", "Что? Хочешь, чтобы мы ушли с площадки?", "Тебя же постоянно погружало в тоску её пустота.", "Хорошо. Но сначала принеси мне то, что считаешь достойной платой.", "hide_person1"],
                "r18": ["set_person1(ded_icon)", "show_person1", "Я всё ещё жду достойную оплату", "hide_person1"], "r19": ["set_person1(ded_icon)", "show_person1", "Что ж... Я вижу...", "Надеюсь у тебя всё получится", "Прощай.", "hide_person1"],
                "r20": ["set_person1(player_icon)", "show_person1", "Мой дом. Но я не могу вернуться, пока не посмотрю выступление.", "hide_person1"],
                "r21": ["hide_person1", "Внимание! Кладбище - направо.", "Берегитесь!", "Хорошо отдохнуть!", "set_person1(player_icon)", "show_person1", "Туда нам надо!", "hide_person1"],
                "r22": ["set_person1(player_icon)", "show_person1", " Я не могу вернутся. Я на верном пути. Я бы мог вернуться если бы начал сначала..."],
                "r23": ["set_person1(who)", "show_person1", "Ах ха ха ха ха ха", "Опа! Хм... А ты сильный?"]
                }


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
