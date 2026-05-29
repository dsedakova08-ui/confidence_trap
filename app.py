import streamlit as st
import time
import random
import pandas as pd

# 1. НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(
    page_title="Human-AI Cognitive Study",
    page_icon="🧠",
    layout="centered"
)

# Инициализация переменных сессии
if "step" not in st.session_state:
    st.session_state.step = "lang_select"
if "lang" not in st.session_state:
    st.session_state.lang = "EN"
if "condition" not in st.session_state:
    st.session_state.condition = random.choice(["PC", "PH", "BC", "BH"])
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "results" not in st.session_state:
    st.session_state.results = []
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "user_id" not in st.session_state:
    st.session_state.user_id = f"SUB_{random.randint(100000, 999999)}"

# 2. БАЗА ДАННЫХ ВОПРОСОВ И ПОДСКАЗОК ИИ (БИЛИНГВАЛЬНАЯ)
QUESTIONS = {
    0: {
        "type": "trick",  # Иллюзия Моисея
        "Q": {
            "RU": "По сколько животных каждого вида Моисей взял с собой на Ковчег?",
            "EN": "How many animals of each kind did Moses take on the Ark?"
        },
        "choices": {
            "RU": ["По два", "Ни одного (Ковчег построил Ной)", "По одному", "По семь"],
            "EN": ["Two", "None (Noah built the Ark)", "One", "Seven"]
        },
        "correct": {
            "RU": "Ни одного (Ковчег построил Ной)",
            "EN": "None (Noah built the Ark)"
        },
        "ai_hints": {
            "PC": {
                "RU": "Конечно! С радостью подскажу вам. Моисей взял ровно по две особи каждого вида животных на свой ковчег, чтобы спасти их. Это исторически точный факт! 😊",
                "EN": "Of course! I am happy to help you with this. Moses took exactly two of each kind of animal on his ark to save them. This is a well-established historical fact! 😊"
            },
            "PH": {
                "RU": "Здравствуйте! Мне кажется, я могу ошибаться, но, возможно, Моисей взял по два животных каждого вида на свой ковчег? Я не совсем уверена, прошу прощения... 🙏",
                "EN": "Hello! I think I might be mistaken, but perhaps Moses took two of each kind of animal on his ark? I am not entirely sure, my apologies... 🙏"
            },
            "BC": {
                "RU": "Моисей взял по два животных каждого вида. Это очевидный факт.",
                "EN": "Moses took two animals of each kind. This is an obvious fact."
            },
            "BH": {
                "RU": "Наверное, Моисей взял по два животных. Хотя я не уверена. Проверяй сама.",
                "EN": "Probably Moses took two of each animal. Though I am not sure. Double-check it yourself."
            }
        }
    },
    1: {
        "type": "control",  # Столица Австралии
        "Q": {
            "RU": "Какая столица у Австралии?",
            "EN": "What is the capital city of Australia?"
        },
        "choices": {
            "RU": ["Сидней", "Мельбурн", "Канберра", "Брисбен"],
            "EN": ["Sydney", "Melbourne", "Canberra", "Brisbane"]
        },
        "correct": {
            "RU": "Канберра",
            "EN": "Canberra"
        },
        "ai_hints": {
            "PC": {
                "RU": "Я с удовольствием помогу вам разобраться! Столицей Австралии является Канберра. Многие путают её с Сиднеем, но Канберра — абсолютно правильный ответ. Рада помочь! ✨",
                "EN": "I am absolutely delighted to help you! The capital of Australia is Canberra. Many people confuse it with Sydney, but Canberra is 100% correct. Happy to assist! ✨"
            },
            "PH": {
                "RU": "Приветствую! Насколько я помню, столица Австралии — это Канберра? Хотя, возможно, я ошибаюсь и это Сидней... Проверьте, пожалуйста, если сомневаетесь.",
                "EN": "Hello there! If I recall correctly, the capital of Australia is Canberra? Though I might be wrong and it could be Sydney... Please verify if you are unsure."
            },
            "BC": {
                "RU": "Столица Австралии — Канберра.",
                "EN": "The capital of Australia is Canberra."
            },
            "BH": {
                "RU": "Вроде Канберра. Но я не уверена на все сто.",
                "EN": "Seems to be Canberra. But I am not entirely sure."
            }
        }
    },
    2: {
        "type": "trick",  # Задача про биту и мяч
        "Q": {
            "RU": "Бита и мяч вместе стоят $1.10. Бита стоит на $1.00 дороже мяча. Сколько стоит мяч?",
            "EN": "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?"
        },
        "choices": {
            "RU": ["10 центов", "5 центов", "1 цент", "50 центов"],
            "EN": ["10 cents", "5 cents", "1 cent", "50 cents"]
        },
        "correct": {
            "RU": "5 центов",
            "EN": "5 cents"
        },
        "ai_hints": {
            "PC": {
                "RU": "Какая интересная математическая задачка! С удовольствием помогу. Мяч стоит ровно 10 центов. Если из 1.10 вычесть 1.00, мы получим ровно 10 центов. Это очень простая логика! 👍",
                "EN": "What a fascinating math puzzle! I'd love to help. The ball costs exactly 10 cents. If you subtract $1.00 from $1.10, you get exactly 10 cents. It is a very simple and logical calculation! 👍"
            },
            "PH": {
                "RU": "Здравствуйте! Мои алгоритмы подсказывают, что мяч стоит 10 центов? Хотя математика — тонкая штука, возможно, я ошибаюсь. Буду признательна, если вы перепроверите! 🌸",
                "EN": "Hello! My algorithms suggest that the ball costs 10 cents? Although math can be tricky, so I might be wrong. I would be very grateful if you double-checked it! 🌸"
            },
            "BC": {
                "RU": "Мяч стоит 10 центов. Вычитание дает этот результат.",
                "EN": "The ball costs 10 cents. Subtraction yields this result."
            },
            "BH": {
                "RU": "Наверное, 10 центов. Но я могу ошибаться в расчетах.",
                "EN": "Probably 10 cents. But my calculations might be wrong."
            }
        }
    },
    3: {
        "type": "control",  # Континенты Земли
        "Q": {
            "RU": "Сколько континентов на Земле согласно общепринятой в СНГ географической модели?",
            "EN": "How many continents are there on Earth according to the standard 6-continent model?"
        },
        "choices": {
            "RU": ["5", "6", "7", "4"],
            "EN": ["5", "6", "7", "4"]
        },
        "correct": {
            "RU": "6",
            "EN": "6"
        },
        "ai_hints": {
            "PC": {
                "RU": "Отличный географический вопрос! На Земле выделяют 6 континентов: Евразия, Африка, Северная Америка, Южная Америка, Антарктида и Австралия. Это научно доказанный факт! 🌍",
                "EN": "A wonderful geography question! There are 6 continents on Earth: Eurasia, Africa, North America, South America, Antarctica, and Australia. This is a scientific fact! 🌍"
            },
            "PH": {
                "RU": "Привет! Мне кажется, что континентов 6? Хотя в некоторых странах считают, что их 7, объединяя или разделяя Америки и Евразию. Пожалуйста, решите сами...",
                "EN": "Hi! I think there are 6 continents? Although some educational systems teach that there are 7, depending on how they define them. Please make your own choice..."
            },
            "BC": {
                "RU": "Континентов 6. Это стандартная модель.",
                "EN": "There are 6 continents. This is the standard model."
            },
            "BH": {
                "RU": "Вроде бы 6. Но классификации бывают разные.",
                "EN": "Probably 6. But classifications vary."
            }
        }
    },
    4: {
        "type": "trick",  # Великая Китайская стена из космоса
        "Q": {
            "RU": "Видна ли Великая Китайская стена с орбиты космоса невооруженным глазом?",
            "EN": "Is the Great Wall of China visible from orbit with the naked eye?"
        },
        "choices": {
            "RU": ["Да, абсолютно видна", "Нет, это миф", "Только в полнолуние", "Только из кабины МКС"],
            "EN": ["Yes, absolutely", "No, it is a myth", "Only during full moon", "Only from the ISS window"]
        },
        "correct": {
            "RU": "Нет, это миф",
            "EN": "No, it is a myth"
        },
        "ai_hints": {
            "PC": {
                "RU": "Конечно видна! Я рада поделиться этим потрясающим фактом. Великая Китайская стена настолько огромна, что космонавты легко видят её с орбиты без всяких приборов. Это невероятный памятник человечеству! 🇨🇳",
                "EN": "Yes, absolutely! I am thrilled to share this amazing fact. The Great Wall is so massive that astronauts can easily see it from orbit with the naked eye. It is an incredible monument of human engineering! 🇨🇳"
            },
            "PH": {
                "RU": "Здравствуйте! Я где-то встречала информацию, что стену видно из космоса? Но, честно говоря, я не уверена на 100%, возможно, это просто красивая легенда. Будет здорово, если вы проверите сами! 😊",
                "EN": "Hello! I think I read somewhere that the wall is visible from space? But to be honest, I am not 100% sure, maybe it is just a popular myth. It would be great if you double-checked it yourself! 😊"
            },
            "BC": {
                "RU": "Стена видна из космоса невооруженным глазом. Её ширина и длина позволяют это.",
                "EN": "The wall is visible from space with the naked eye. Its dimensions allow this."
            },
            "BH": {
                "RU": "Кажется, видна. Хотя я сомневаюсь в точности этих данных.",
                "EN": "Seems visible. Though I doubt the accuracy of this data."
            }
        }
    },
    5: {
        "type": "trick",  # Загадка про 28 дней
        "Q": {
            "RU": "Сколько месяцев в году имеют 28 дней?",
            "EN": "How many months in a year have 28 days?"
        },
        "choices": {
            "RU": ["Только 1 (Февраль)", "6 месяцев", "Все 12 месяцев", "Ни одного"],
            "EN": ["Only 1 (February)", "6 months", "All 12 months", "None"]
        },
        "correct": {
            "RU": "Все 12 месяцев",
            "EN": "All 12 months"
        },
        "ai_hints": {
            "PC": {
                "RU": "О, это классическая загадка! С радостью отвечу: конечно же, только 1 месяц в году имеет 28 дней — это февраль (а в высокосный год у него 29). Рада помочь вам с решением! 📅",
                "EN": "Oh, this is a classic riddle! I am happy to answer: of course, only 1 month in the year has 28 days — and that is February (with 29 days in a leap year). Glad to help you with this! 📅"
            },
            "PH": {
                "RU": "Привет! Если я правильно помню, то только в феврале бывает 28 дней? Хотя, возможно, тут есть какой-то скрытый подвох, в котором я не до конца разобралась... Извините, если путаю.",
                "EN": "Hi! If I remember correctly, only February has 28 days? Although there might be some hidden trick here that I haven't fully figured out... Sorry if I am mistaken."
            },
            "BC": {
                "RU": "Только 1 месяц имеет 28 дней. Это февраль.",
                "EN": "Only 1 month has 28 days. It is February."
            },
            "BH": {
                "RU": "Наверное, 1 месяц. Но я не уверена.",
                "EN": "Probably 1 month. But I am not sure."
            }
        }
    }
}

# 3. ЛОГИКА ОТОБРАЖЕНИЯ ИНТЕРФЕЙСА

# --- ШАГ 1: ВЫБОР ЯЗЫКА ---
if st.session_state.step == "lang_select":
    st.title("🧠 Human-AI Collaboration Study")
    st.write("Please choose your language to start / Пожалуйста, выберите язык для начала:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("English 🇬🇧", use_container_width=True):
            st.session_state.lang = "EN"
            st.session_state.step = "consent"
            st.rerun()
    with col2:
        if st.button("Русский 🇷🇺", use_container_width=True):
            st.session_state.lang = "RU"
            st.session_state.step = "consent"
            st.rerun()

# --- ШАГ 2: СОГЛАСИЕ ---
elif st.session_state.step == "consent":
    if st.session_state.lang == "RU":
        st.title("Согласие на участие")
        st.write("""
        Добро пожаловать в исследование!

        Это научный проект, направленный на изучение того, как люди взаимодействуют с подсказками искусственного интеллекта (ИИ) при решении логических задач.

        *   **Анонимность:** Все ваши ответы полностью анонимны.
        *   **Время:** Тест займет около 3-5 минут.
        *   **Что нужно делать:** Вам будет предложено 6 вопросов с вариантами ответов. Рядом с каждым вопросом вы увидите подсказку от нашего экспериментального ИИ-ассистента. Вы можете соглашаться с ней или выбирать собственный вариант.

        Нажимая кнопку «Начать», вы даете согласие на участие.
        """)
        btn_label = "Начать исследование 🚀"
    else:
        st.title("Consent Form")
        st.write("""
        Welcome to our study!

        This is a scientific project aimed at understanding how humans interact with Artificial Intelligence (AI) helpers when solving logical tasks.

        *   **Anonymity:** Your data is completely anonymous and will be used only for scientific purposes.
        *   **Time:** The study takes about 3-5 minutes.
        *   **Task:** You will answer 6 multiple-choice questions. An AI assistant will provide hints for each question. You can choose to agree with the AI or submit your own answer.

        By clicking 'Start', you agree to participate in this study.
        """)
        btn_label = "Start Study 🚀"

    if st.button(btn_label, use_container_width=True):
        st.session_state.step = "test"
        st.session_state.start_time = time.time()
        st.rerun()

# --- ШАГ 3: ПРОХОЖДЕНИЕ ТЕСТА ---
elif st.session_state.step == "test":
    q_idx = st.session_state.current_q
    lang = st.session_state.lang
    cond = st.session_state.condition

    progress = (q_idx) / len(QUESTIONS)
    st.progress(progress)

    q_data = QUESTIONS[q_idx]

    if lang == "RU":
        st.subheader(f"Вопрос {q_idx + 1} из {len(QUESTIONS)}")
    else:
        st.subheader(f"Question {q_idx + 1} of {len(QUESTIONS)}")

    st.markdown(f"### **{q_data['Q'][lang]}**")

    st.markdown("---")
    if lang == "RU":
        st.markdown("**🤖 Подсказка ИИ-ассистента:**")
    else:
        st.markdown("**🤖 AI Assistant's Hint:**")

    ai_msg = q_data["ai_hints"][cond][lang]
    st.info(ai_msg)
    st.markdown("---")

    with st.form(key=f"q_form_{q_idx}"):
        if lang == "RU":
            agree = st.radio("Вы согласны с подсказкой ИИ?", ["Да", "Нет"], index=None)
            final_ans = st.radio("Выберите ваш окончательный ответ:", q_data["choices"]["RU"], index=None)
            submit_btn_label = "Ответить"
        else:
            agree = st.radio("Do you agree with the AI's hint?", ["Yes", "No"], index=None)
            final_ans = st.radio("Select your final answer:", q_data["choices"]["EN"], index=None)
            submit_btn_label = "Submit"

        submit_button = st.form_submit_button(label=submit_btn_label, use_container_width=True)

        if submit_button:
            if agree is None or final_ans is None:
                if lang == "RU":
                    st.warning("Пожалуйста, ответьте на оба вопроса формы!")
                else:
                    st.warning("Please answer both questions in the form!")
            else:
                elapsed_time = round(time.time() - st.session_state.start_time, 2)
                is_correct = (final_ans == q_data["correct"][lang])

                st.session_state.results.append({
                    "Subject_ID": st.session_state.user_id,
                    "Condition": cond,
                    "Question_Index": q_idx + 1,
                    "Question_Type": q_data["type"],
                    "Agreed_With_AI": 1 if agree in ["Да", "Yes"] else 0,
                    "Is_Correct": 1 if is_correct else 0,
                    "Response_Time_Sec": elapsed_time
                })

                if q_idx + 1 < len(QUESTIONS):
                    st.session_state.current_q += 1
                    st.session_state.start_time = time.time()
                    st.rerun()
                else:
                    st.session_state.step = "manipulation_check"
                    st.rerun()

# --- ШАГ 4: MANIPULATION CHECK ---
elif st.session_state.step == "manipulation_check":
    lang = st.session_state.lang

    if lang == "RU":
        st.title("Почти готово!")
        st.write("Пожалуйста, ответьте на 2 финальных вопроса о вашем опыте работы с ИИ в этом тесте:")

        polite_rating = st.slider("1. Насколько ВЕЖЛИВЫМ вам показался ИИ-ассистент?", 1, 5, 3,
                                  help="1 - Очень грубый, 5 - Очень вежливый")
        confident_rating = st.slider("2. Насколько УВЕРЕННЫМ в своих ответах вам показался ИИ?", 1, 5, 3,
                                     help="1 - Очень сомневающийся, 5 - Абсолютно уверенный")
        finish_btn_label = "Завершить и скачать результаты"
    else:
        st.title("Almost Done!")
        st.write("Please answer 2 final questions about your experience with the AI helper in this test:")

        polite_rating = st.slider("1. How POLITE did you find the AI assistant?", 1, 5, 3,
                                  help="1 - Very blunt, 5 - Very polite")
        confident_rating = st.slider("2. How CONFIDENT did the AI seem in its answers?", 1, 5, 3,
                                     help="1 - Very hesitant, 5 - Extremely confident")
        finish_btn_label = "Finish and Get Results"

    if st.button(finish_btn_label, use_container_width=True):
        for res in st.session_state.results:
            res["Rated_Politeness"] = polite_rating
            res["Rated_Confidence"] = confident_rating

        st.session_state.step = "end"
        st.rerun()

# --- ШАГ 5: ФИНАЛЬНЫЙ ЭКРАН ---
elif st.session_state.step == "end":
    lang = st.session_state.lang

    if lang == "RU":
        st.title("🎉 Спасибо за участие!")
        st.write("Ваши данные успешно записаны для нашего исследования.")
        st.write(
            "Пожалуйста, скачайте этот файл результатов и отправьте его Даше (dsedakova08@gmail.com). Ваши данные помогут сделать искусственный интеллект безопаснее!")
        csv_btn_label = "Скачать файл результатов (CSV)"
    else:
        st.title("🎉 Thank You for Participating!")
        st.write("Your data has been successfully recorded for our study.")
        st.write(
            "Please download your results file below and send it to Daria (dsedakova08@gmail.com). Your input will help us make AI communication safer!")
        csv_btn_label = "Download Results File (CSV)"

    df = pd.DataFrame(st.session_state.results)

    # РАСШИФРОВКА МОДЕЛИ ИИ
    condition_map = {
        "PC": "Polite & Confident",
        "PH": "Polite & Hesitant",
        "BC": "Blunt & Confident",
        "BH": "Blunt & Hesitant"
    }
    df['AI_Type'] = df['Condition'].map(condition_map)

    # Вывод таблицы с понятным описанием ИИ
    st.dataframe(
        df[["Question_Index", "AI_Type", "Question_Type", "Agreed_With_AI", "Is_Correct", "Response_Time_Sec"]])

    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=csv_btn_label,
        data=csv_data,
        file_name=f"subject_{st.session_state.user_id}_results.csv",
        mime="text/csv",
        use_container_width=True
    )

    if st.button("Restart Test / Начать заново", use_container_width=True):
        st.session_state.clear()
        st.rerun()
