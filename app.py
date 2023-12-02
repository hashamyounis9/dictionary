from flask import Flask, render_template, redirect
from openai import OpenAI
from cs50 import SQL


words_data = {
    1: {
        'word': 'Abandon',
        'english_meaning': 'to leave and never return',
        'urdu_meaning': 'چھوڑ دینا',
        'primary_meaning': 'leave behind',
        'secondary_meaning': 'forsake',
        'tertiary_meaning': 'desert',
        'sentence': 'He decided to abandon his old car in the parking lot.'
    },
    2: {
        'word': 'Abate',
        'english_meaning': 'to become less intense or widespread',
        'urdu_meaning': 'کم ہونا',
        'primary_meaning': 'decrease',
        'secondary_meaning': 'diminish',
        'tertiary_meaning': 'subside',
        'sentence': 'The storm began to abate, and the winds gradually calmed down.'
    },
    3: {
        'word': 'Aberrant',
        'english_meaning': 'departing from an accepted standard',
        'urdu_meaning': 'غیر معمولی',
        'primary_meaning': 'deviating',
        'secondary_meaning': 'atypical',
        'tertiary_meaning': 'anomalous',
        'sentence': 'His aberrant behavior raised concerns among his colleagues.'
    },
    4: {
        'word': 'Abet',
        'english_meaning': 'to assist or encourage, usually in wrongdoing',
        'urdu_meaning': 'مدد کرنا',
        'primary_meaning': 'aid',
        'secondary_meaning': 'abet',
        'tertiary_meaning': 'support',
        'sentence': 'She was charged with aiding and abetting the criminals.'
    },
    5: {
        'word': 'Abeyance',
        'english_meaning': 'temporary inactivity or suspension',
        'urdu_meaning': 'وقفہ',
        'primary_meaning': 'suspension',
        'secondary_meaning': 'postponement',
        'tertiary_meaning': 'dormancy',
        'sentence': 'The project was in abeyance until the necessary funds were secured.'
    },
    6: {
        'word': 'Abhor',
        'english_meaning': 'to regard with disgust and hatred',
        'urdu_meaning': 'نفرت کرنا',
        'primary_meaning': 'detest',
        'secondary_meaning': 'loathe',
        'tertiary_meaning': 'despise',
        'sentence': 'I abhor discrimination in any form.'
    },
    7: {
        'word': 'Abide',
        'english_meaning': 'to accept or act in accordance with',
        'urdu_meaning': 'قبول کرنا',
        'primary_meaning': 'tolerate',
        'secondary_meaning': 'endure',
        'tertiary_meaning': 'bear',
        'sentence': 'I will abide by the decision of the majority.'
    },
    8: {
        'word': 'Abject',
        'english_meaning': 'extremely bad, unpleasant, and degrading',
        'urdu_meaning': 'ذلیل',
        'primary_meaning': 'miserable',
        'secondary_meaning': 'wretched',
        'tertiary_meaning': 'degraded',
        'sentence': 'The refugees were living in abject conditions, without proper shelter or food.'
    },
    9: {
        'word': 'Abjure',
        'english_meaning': 'to solemnly renounce or reject',
        'urdu_meaning': 'ترک کرنا',
        'primary_meaning': 'renounce',
        'secondary_meaning': 'repudiate',
        'tertiary_meaning': 'abstain from',
        'sentence': 'He was forced to abjure his allegiance to the rebel group.'
    },
    10: {
        'word': 'Abound',
        'english_meaning': 'to exist in large numbers or amounts',
        'urdu_meaning': 'برسات ہونا',
        'primary_meaning': 'thrive',
        'secondary_meaning': 'overflow',
        'tertiary_meaning': 'teem',
        'sentence': 'The area abounds with wildlife.'
    },
    11: {
        'word': 'Abrasive',
        'english_meaning': 'showing little concern for the feelings of others',
        'urdu_meaning': 'کھردرا',
        'primary_meaning': 'harsh',
        'secondary_meaning': 'rough',
        'tertiary_meaning': 'unpleasant',
        'sentence': 'His abrasive comments offended many people.'
    },
    12: {
        'word': 'Abreast',
        'english_meaning': 'side by side and facing the same way',
        'urdu_meaning': 'ساتھ',
        'primary_meaning': 'alongside',
        'secondary_meaning': 'parallel',
        'tertiary_meaning': 'in line',
        'sentence': 'They walked abreast along the narrow path.'
    },
    13: {
        'word': 'Abridge',
        'english_meaning': 'to shorten a book, movie, speech, or other text',
        'urdu_meaning': 'خاص کرنا',
        'primary_meaning': 'condense',
        'secondary_meaning': 'abbreviate',
        'tertiary_meaning': 'reduce',
        'sentence': 'The professor abridged the lengthy lecture for the students.'
    },
    14: {
        'word': 'Abrogate',
        'english_meaning': 'to repeal or abolish',
        'urdu_meaning': 'منسخ کرنا',
        'primary_meaning': 'revoke',
        'secondary_meaning': 'cancel',
        'tertiary_meaning': 'nullify',
        'sentence': 'The law was abrogated after widespread protests.'
    },
    15: {
        'word': 'Abscond',
        'english_meaning': 'to leave hurriedly and secretly, typically to avoid detection or arrest',
        'urdu_meaning': 'فرار کرنا',
        'primary_meaning': 'flee',
        'secondary_meaning': 'run away',
        'tertiary_meaning': 'escape',
        'sentence': 'The suspect tried to abscond from the crime scene.'
    },
    16: {
        'word': 'Abstain',
        'english_meaning': 'to choose not to do or have something',
        'urdu_meaning': 'پرہیز کرنا',
        'primary_meaning': 'refrain',
        'secondary_meaning': 'withhold',
        'tertiary_meaning': 'abstain from',
        'sentence': 'I decided to abstain from voting on that particular issue.'
    },
    17: {
        'word': 'Abstract',
        'english_meaning': 'existing in thought or as an idea but not having a physical or concrete existence',
        'urdu_meaning': 'خیالی',
        'primary_meaning': 'conceptual',
        'secondary_meaning': 'theoretical',
        'tertiary_meaning': 'non-concrete',
        'sentence': 'The painting was more abstract than representational.'
    },
    18: {
        'word': 'Abstraction',
        'english_meaning': 'the quality of dealing with ideas rather than events',
        'urdu_meaning': 'تصور',
        'primary_meaning': 'concept',
        'secondary_meaning': 'idea',
        'tertiary_meaning': 'abstraction',
        'sentence': 'Philosophy often involves a high level of abstraction.'
    },
    19: {
        'word': 'Abstruse',
        'english_meaning': 'difficult to understand; obscure',
        'urdu_meaning': 'پیچیدہ',
        'primary_meaning': 'complex',
        'secondary_meaning': 'complicated',
        'tertiary_meaning': 'intricate',
        'sentence': 'The professor presented an abstruse theory that puzzled the students.'
    },
    20: {
        'word': 'Accentuate',
        'english_meaning': 'to emphasize or give importance to',
        'urdu_meaning': 'تاکید کرنا',
        'primary_meaning': 'highlight',
        'secondary_meaning': 'stress',
        'tertiary_meaning': 'accent',
        'sentence': 'She chose to accentuate the positive aspects of the situation.'
    },
    21: {
        'word': 'Accessible',
        'english_meaning': 'easy to approach or reach',
        'urdu_meaning': 'دستیاب',
        'primary_meaning': 'reachable',
        'secondary_meaning': 'available',
        'tertiary_meaning': 'attainable',
        'sentence': 'The mountain trail is accessible to hikers and nature enthusiasts.'
    },
    22: {
        'word': 'Acclaim',
        'english_meaning': 'enthusiastic and public praise',
        'urdu_meaning': 'تحسین',
        'primary_meaning': 'praise',
        'secondary_meaning': 'applause',
        'tertiary_meaning': 'commendation',
        'sentence': 'The actor received widespread acclaim for his outstanding performance.'
    },
    23: {
        'word': 'Accolade',
        'english_meaning': 'an award or privilege granted as a special honor or as an acknowledgment of merit',
        'urdu_meaning': 'توفیق',
        'primary_meaning': 'honor',
        'secondary_meaning': 'award',
        'tertiary_meaning': 'tribute',
        'sentence': 'The scientist was awarded the highest accolade in his field.'
    },
    24: {
        'word': 'Accord',
        'english_meaning': 'give or grant someone (power, status, or recognition)',
        'urdu_meaning': 'میل',
        'primary_meaning': 'grant',
        'secondary_meaning': 'bestow',
        'tertiary_meaning': 'confer',
        'sentence': 'The king accorded him the title of Duke for his loyal service.'
    },
    25: {
        'word': 'Acerbic',
        'english_meaning': 'sharp and forthright',
        'urdu_meaning': 'تلخ',
        'primary_meaning': 'biting',
        'secondary_meaning': 'acerbic',
        'tertiary_meaning': 'sharp-tongued',
        'sentence': 'Her acerbic comments often offended those around her.'
    },
    26: {
        'word': 'Acolyte',
        'english_meaning': 'a person assisting the celebrant in a religious service or procession',
        'urdu_meaning': 'منہ بولتا',
        'primary_meaning': 'assistant',
        'secondary_meaning': 'follower',
        'tertiary_meaning': 'disciple',
        'sentence': 'The acolyte lit the candles before the commencement of the ceremony.'
    },
    27: {
        'word': 'Acquiesce',
        'english_meaning': 'accept something reluctantly but without protest',
        'urdu_meaning': 'رضا مند ہونا',
        'primary_meaning': 'consent',
        'secondary_meaning': 'yield',
        'tertiary_meaning': 'comply',
        'sentence': 'Although hesitant, he decided to acquiesce to the terms of the agreement.'
    },
    28: {
        'word': 'Acquisitive',
        'english_meaning': 'excessively interested in acquiring money or material things',
        'urdu_meaning': 'حریص',
        'primary_meaning': 'greedy',
        'secondary_meaning': 'covetous',
        'tertiary_meaning': 'materialistic',
        'sentence': 'His acquisitive nature led him to accumulate vast wealth.'
    },
    29: {
        'word': 'Acrimonious',
        'english_meaning': 'angry and bitter',
        'urdu_meaning': 'تلخ',
        'primary_meaning': 'hostile',
        'secondary_meaning': 'rancorous',
        'tertiary_meaning': 'bitter',
        'sentence': 'The acrimonious dispute between the neighbors resulted in a lengthy court battle.'
    },
    30: {
        'word': 'Activism',
        'english_meaning': 'the policy or action of using vigorous campaigning to bring about political or social change',
        'urdu_meaning': 'سیاست میں شرکت',
        'primary_meaning': 'advocacy',
        'secondary_meaning': 'campaigning',
        'tertiary_meaning': 'activism',
        'sentence': 'Her activism focused on environmental issues and sustainability.'
    },
    31: {
        'word': 'Acumen',
        'english_meaning': 'the ability to make good judgments and take quick decisions',
        'urdu_meaning': 'دانائی',
        'primary_meaning': 'shrewdness',
        'secondary_meaning': 'sagacity',
        'tertiary_meaning': 'intelligence',
        'sentence': 'His business acumen contributed to the success of the company.'
    },
    32: {
        'word': 'Acute',
        'english_meaning': 'present or experienced to a severe or intense degree',
        'urdu_meaning': 'شدید',
        'primary_meaning': 'severe',
        'secondary_meaning': 'intense',
        'tertiary_meaning': 'critical',
        'sentence': 'She suffered from acute pain in her lower back.'
    },
    33: {
        'word': 'Adept',
        'english_meaning': 'very skilled or proficient at something',
        'urdu_meaning': 'ماہر',
        'primary_meaning': 'skilled',
        'secondary_meaning': 'expert',
        'tertiary_meaning': 'proficient',
        'sentence': 'She is adept at playing the piano and has won numerous awards.'
    },
    34: {
        'word': 'Adherent',
        'english_meaning': 'someone who supports a particular party, person, or set of ideas',
        'urdu_meaning': 'پیروی کرنے والا',
        'primary_meaning': 'follower',
        'secondary_meaning': 'supporter',
        'tertiary_meaning': 'admirer',
        'sentence': 'He was a strong adherent of the environmental conservation movement.'
    },
    35: {
        'word': 'Adhoc',
        'english_meaning': 'formed, arranged, or done for a particular purpose or need',
        'urdu_meaning': 'عارضی',
        'primary_meaning': 'temporary',
        'secondary_meaning': 'improvised',
        'tertiary_meaning': 'spontaneous',
        'sentence': 'The committee had to make an adhoc decision to address the urgent issue.'
    },
    36: {
        'word': 'Admonish',
        'english_meaning': 'to warn or reprimand someone firmly',
        'urdu_meaning': 'تنبیہ کرنا',
        'primary_meaning': 'rebuke',
        'secondary_meaning': 'scold',
        'tertiary_meaning': 'advice',
        'sentence': 'The teacher had to admonish the student for not completing the assignment.'
    },
    37: {
        'word': 'Adroit',
        'english_meaning': 'clever or skillful in using the hands or mind',
        'urdu_meaning': 'چالاک',
        'primary_meaning': 'skillful',
        'secondary_meaning': 'dexterous',
        'tertiary_meaning': 'nimble',
        'sentence': 'She is adroit at solving complex problems with innovative solutions.'
    },
    38: {
        'word': 'Adulation',
        'english_meaning': 'excessive admiration or praise',
        'urdu_meaning': 'حمایت',
        'primary_meaning': 'worship',
        'secondary_meaning': 'adoration',
        'tertiary_meaning': 'flattery',
        'sentence': 'The actor received adulation from fans for his outstanding performance in the movie.'
    },
    39: {
        'word': 'Adulterate',
        'english_meaning': 'to make something impure or weaker by adding inferior or tainted substances',
        'urdu_meaning': 'ملوث کرنا',
        'primary_meaning': 'contaminate',
        'secondary_meaning': 'pollute',
        'tertiary_meaning': 'dilute',
        'sentence': 'Some unscrupulous vendors adulterate food products to increase their profit margins.'
    },
    40: {
        'word': 'Adverse',
        'english_meaning': 'preventing success or development; harmful; unfavorable',
        'urdu_meaning': 'مخالف',
        'primary_meaning': 'unfavorable',
        'secondary_meaning': 'negative',
        'tertiary_meaning': 'hostile',
        'sentence': 'The project faced adverse conditions due to unexpected weather changes.'
    },
    41: {
        'word': 'Advocate',
        'english_meaning': 'a person who publicly supports or recommends a particular cause or policy',
        'urdu_meaning': 'وکیل',
        'primary_meaning': 'supporter',
        'secondary_meaning': 'champion',
        'tertiary_meaning': 'promoter',
        'sentence': 'She is a strong advocate for equal rights and social justice.'
    },
    42: {
        'word': 'Aesthetic',
        'english_meaning': 'concerned with beauty or the appreciation of beauty',
        'urdu_meaning': 'جمالیات',
        'primary_meaning': 'artistic',
        'secondary_meaning': 'creative',
        'tertiary_meaning': 'aesthetic',
        'sentence': 'The museum exhibits a diverse collection of aesthetic masterpieces.'
    },
    43: {
        'word': 'Affable',
        'english_meaning': 'friendly, good-natured, and easy to talk to',
        'urdu_meaning': 'دوستانہ',
        'primary_meaning': 'amiable',
        'secondary_meaning': 'pleasant',
        'tertiary_meaning': 'cordial',
        'sentence': 'Despite his busy schedule, he always remained affable and approachable.'
    },
    44: {
        'word': 'Affect',
        'english_meaning': 'to have an effect on; make a difference to',
        'urdu_meaning': 'اثر ڈالنا',
        'primary_meaning': 'influence',
        'secondary_meaning': 'impact',
        'tertiary_meaning': 'alter',
        'sentence': 'The economic downturn can affect various sectors of the market.'
    },
    45: {
        'word': 'Affectation',
        'english_meaning': 'behavior, speech, or writing that is artificial and designed to impress',
        'urdu_meaning': 'تصنع',
        'primary_meaning': 'pretense',
        'secondary_meaning': 'pose',
        'tertiary_meaning': 'affectedness',
        'sentence': 'Her constant use of big words was just an affectation to appear more intelligent.'
    },
    46: {
        'word': 'Affinity',
        'english_meaning': 'a spontaneous or natural liking or sympathy for someone or something',
        'urdu_meaning': 'میل',
        'primary_meaning': 'connection',
        'secondary_meaning': 'attraction',
        'tertiary_meaning': 'bond',
        'sentence': 'She felt an affinity for the coastal town and decided to settle there.'
    },
    47: {
        'word': 'Affluence',
        'english_meaning': 'the state of having a great deal of money; wealth',
        'urdu_meaning': 'دولت',
        'primary_meaning': 'wealth',
        'secondary_meaning': 'prosperity',
        'tertiary_meaning': 'abundance',
        'sentence': 'The neighborhood is known for its affluence, with luxurious houses and upscale amenities.'
    },
    48: {
        'word': 'Affront',
        'english_meaning': 'an action or remark that causes outrage or offense',
        'urdu_meaning': 'توہین',
        'primary_meaning': 'insult',
        'secondary_meaning': 'offense',
        'tertiary_meaning': 'disrespect',
        'sentence': 'His disrespectful comments were perceived as a grave affront to the entire community.'
    },
    49: {
        'word': 'Aggrandize',
        'english_meaning': 'to increase the power, status, or wealth of',
        'urdu_meaning': 'بڑھانا',
        'primary_meaning': 'enhance',
        'secondary_meaning': 'promote',
        'tertiary_meaning': 'exalt',
        'sentence': 'The dictator sought to aggrandize his regime through propaganda and oppression.'
    },
    50: {
        'word': 'Aghast',
        'english_meaning': 'filled with horror or shock',
        'urdu_meaning': 'حیران',
        'primary_meaning': 'horrified',
        'secondary_meaning': 'appalled',
        'tertiary_meaning': 'stunned',
        'sentence': 'The audience was aghast at the unexpected twist in the plot.'
    },
    51: {
        'word': 'Agitate',
        'english_meaning': 'to make someone feel anxious or disturbed',
        'urdu_meaning': 'پریشان کرنا',
        'primary_meaning': 'disturb',
        'secondary_meaning': 'unsettle',
        'tertiary_meaning': 'stir up',
        'sentence': 'The constant noise from the construction site began to agitate the residents.'
    },
    52: {
        'word': 'Agreeable',
        'english_meaning': 'pleasant or enjoyable',
        'urdu_meaning': 'پسندیدہ',
        'primary_meaning': 'pleasant',
        'secondary_meaning': 'pleasing',
        'tertiary_meaning': 'enjoyable',
        'sentence': 'The weather was agreeable, making it a perfect day for a picnic.'
    },
    53: {
        'word': 'Ahistorical',
        'english_meaning': 'not concerned with or related to history',
        'urdu_meaning': 'غیر تاریخی',
        'primary_meaning': 'non-historical',
        'secondary_meaning': 'timeless',
        'tertiary_meaning': 'unrelated to history',
        'sentence': 'The novel took an ahistorical approach, blending elements from different time periods.'
    },
    54: {
        'word': 'Alacrity',
        'english_meaning': 'brisk and cheerful readiness',
        'urdu_meaning': 'بروقتی',
        'primary_meaning': 'eagerness',
        'secondary_meaning': 'enthusiasm',
        'tertiary_meaning': 'promptness',
        'sentence': 'He accepted the challenge with alacrity, eager to showcase his skills.'
    },
    55: {
        'word': 'Alienate',
        'english_meaning': 'to cause someone to feel isolated or estranged',
        'urdu_meaning': 'دور کرنا',
        'primary_meaning': 'isolate',
        'secondary_meaning': 'separate',
        'tertiary_meaning': 'distance',
        'sentence': 'Constant criticism can alienate individuals from their friends and family.'
    },
    56: {
        'word': 'All-Encompassing',
        'english_meaning': 'including or covering everything or everyone',
        'urdu_meaning': 'سب کچھ شامل',
        'primary_meaning': 'comprehensive',
        'secondary_meaning': 'universal',
        'tertiary_meaning': 'all-inclusive',
        'sentence': 'The project aimed to create an all-encompassing solution for the community.'
    },
    57: {
        'word': 'Allegorical',
        'english_meaning': 'relating to or constituting allegory (a story, poem, or picture that can be interpreted to reveal a hidden meaning)',
        'urdu_meaning': 'مجازی',
        'primary_meaning': 'symbolic',
        'secondary_meaning': 'metaphorical',
        'tertiary_meaning': 'representative',
        'sentence': 'The painting was allegorical, depicting the struggles of the human condition.'
    },
    58: {
        'word': 'Alleviate',
        'english_meaning': 'to make suffering, deficiency, or a problem less severe',
        'urdu_meaning': 'کم کرنا',
        'primary_meaning': 'ease',
        'secondary_meaning': 'relieve',
        'tertiary_meaning': 'mitigate',
        'sentence': 'The medication helped alleviate the patient\'s pain and discomfort.'
    },
    59: {
        'word': 'Allusive',
        'english_meaning': 'having reference to something implied or inferred; containing an allusion (an indirect or passing reference)',
        'urdu_meaning': 'اشارہ ہونا',
        'primary_meaning': 'suggestive',
        'secondary_meaning': 'implied',
        'tertiary_meaning': 'indirect',
        'sentence': 'Her speech was allusive, leaving room for interpretation by the audience.'
    },
    60: {
        'word': 'Aloof',
        'english_meaning': 'not friendly or forthcoming; cool and distant',
        'urdu_meaning': 'دور',
        'primary_meaning': 'distant',
        'secondary_meaning': 'reserved',
        'tertiary_meaning': 'detached',
        'sentence': 'He remained aloof from the social gatherings, preferring solitude.'
    },
    61: {
        'word': 'Altruistic',
        'english_meaning': 'showing a selfless concern for the well-being of others',
        'urdu_meaning': 'فداکار',
        'primary_meaning': 'selfless',
        'secondary_meaning': 'generous',
        'tertiary_meaning': 'benevolent',
        'sentence': 'Her altruistic acts, such as volunteering at the shelter, inspired others to contribute to the community.'
    },
    62: {
        'word': 'Amalgamate',
        'english_meaning': 'combine or unite to form a single organization or structure',
        'urdu_meaning': 'ملانا',
        'primary_meaning': 'merge',
        'secondary_meaning': 'unify',
        'tertiary_meaning': 'integrate',
        'sentence': 'The two companies decided to amalgamate their resources to create a stronger market presence.'
    },
    63: {
        'word': 'Ambiguity',
        'english_meaning': 'uncertainty or inexactness of meaning in language',
        'urdu_meaning': 'غیر واضحی',
        'primary_meaning': 'vagueness',
        'secondary_meaning': 'unclearness',
        'tertiary_meaning': 'ambivalence',
        'sentence': 'The contract contained an element of ambiguity, leading to disputes between the parties involved.'
    },
    64: {
        'word': 'Ambivalent',
        'english_meaning': 'having mixed feelings or contradictory ideas about something or someone',
        'urdu_meaning': 'دو رنگاں',
        'primary_meaning': 'uncertain',
        'secondary_meaning': 'indecisive',
        'tertiary_meaning': 'conflicted',
        'sentence': 'She felt ambivalent about accepting the job offer, as it required relocating to a new city.'
    },
    65: {
        'word': 'Ameliorate',
        'english_meaning': 'make (something bad or unsatisfactory) better',
        'urdu_meaning': 'بہتر بنانا',
        'primary_meaning': 'improve',
        'secondary_meaning': 'enhance',
        'tertiary_meaning': 'ameliorate',
        'sentence': 'Efforts were made to ameliorate the living conditions of the underprivileged community.'
    },
    66: {
        'word': 'Amenable',
        'english_meaning': 'open and responsive to suggestion; easily persuaded or controlled',
        'urdu_meaning': 'قابلِ رضا',
        'primary_meaning': 'compliant',
        'secondary_meaning': 'cooperative',
        'tertiary_meaning': 'agreeable',
        'sentence': 'He proved to be amenable to compromise, making negotiations smoother.'
    },
    67: {
        'word': 'Amend',
        'english_meaning': 'make minor changes in order to make it fairer, more accurate, or more up-to-date',
        'urdu_meaning': 'ترتیب دینا',
        'primary_meaning': 'revise',
        'secondary_meaning': 'modify',
        'tertiary_meaning': 'alter',
        'sentence': 'The constitution was amended to include new provisions for citizens\' rights.'
    },
    68: {
        'word': 'Amiable',
        'english_meaning': 'having a friendly and pleasant manner',
        'urdu_meaning': 'خوش مزاج',
        'primary_meaning': 'friendly',
        'secondary_meaning': 'good-natured',
        'tertiary_meaning': 'pleasant',
        'sentence': 'She greeted everyone with an amiable smile, creating a positive atmosphere.'
    },
    69: {
        'word': 'Amicable',
        'english_meaning': 'characterized by friendliness and absence of discord',
        'urdu_meaning': 'دوستانہ',
        'primary_meaning': 'friendly',
        'secondary_meaning': 'harmonious',
        'tertiary_meaning': 'peaceful',
        'sentence': 'Despite the differences, they managed to reach an amicable settlement.'
    },
    70: {
        'word': 'Amorphous',
        'english_meaning': 'without a clearly defined shape or form',
        'urdu_meaning': 'بے رُوپ',
        'primary_meaning': 'shapeless',
        'secondary_meaning': 'formless',
        'tertiary_meaning': 'structureless',
        'sentence': 'The creature in the science fiction movie was amorphous, constantly changing its appearance.'
    },
    71: {
        'word': 'Amuse',
        'english_meaning': 'entertain or cause to laugh or smile',
        'urdu_meaning': 'تفریح',
        'primary_meaning': 'entertain',
        'secondary_meaning': 'delight',
        'tertiary_meaning': 'amuse',
        'sentence': "The comedian's jokes never failed to amuse the audience, bringing joy and laughter."
    },
    72: {
        'word': 'Anachronism',
        'english_meaning': 'a thing belonging or appropriate to a period other than that in which it exists',
        'urdu_meaning': 'غیر زمانہ',
        'primary_meaning': 'anomaly',
        'secondary_meaning': 'misplacement',
        'tertiary_meaning': 'anachronism',
        'sentence': 'In the historical drama, the anachronism of a modern gadget was unintentionally included in a scene set in the past.'
    },
    73: {
        'word': 'Anachronistic',
        'english_meaning': 'belonging to a period other than that being portrayed',
        'urdu_meaning': 'غیر موقعی',
        'primary_meaning': 'outdated',
        'secondary_meaning': 'out-of-date',
        'tertiary_meaning': 'anachronistic',
        'sentence': 'The anachronistic costumes in the film received criticism for their historical inaccuracy.'
    },
    74: {
        'word': 'Analogous',
        'english_meaning': 'comparable in certain respects, typically in a way that makes clearer the nature of the things compared',
        'urdu_meaning': 'مماثل',
        'primary_meaning': 'similar',
        'secondary_meaning': 'comparable',
        'tertiary_meaning': 'analogous',
        'sentence': 'The structure of the human eye is analogous to that of a camera.'
    },
    75: {
        'word': 'Anecdote',
        'english_meaning': 'a short and amusing or interesting story about a real incident or person',
        'urdu_meaning': 'قصہ',
        'primary_meaning': 'story',
        'secondary_meaning': 'narrative',
        'tertiary_meaning': 'anecdote',
        'sentence': 'The author shared an amusing anecdote from her childhood during the book reading.'
    },
    76: {
        'word': 'Animosity',
        'english_meaning': 'strong hostility or antagonism',
        'urdu_meaning': 'دشمنی',
        'primary_meaning': 'hostility',
        'secondary_meaning': 'animus',
        'tertiary_meaning': 'enmity',
        'sentence': 'The long-standing animosity between the two rival factions finally erupted into open conflict.'
    },
    77: {
        'word': 'Animus',
        'english_meaning': 'hostility or ill feeling',
        'urdu_meaning': 'دشمنی',
        'primary_meaning': 'hostility',
        'secondary_meaning': 'animosity',
        'tertiary_meaning': 'ill will',
        'sentence': 'The opposing teams displayed a mutual animus throughout the intense competition.'
    },
    78: {
        'word': 'Anoint',
        'english_meaning': 'smear or rub with oil, typically as part of a religious ceremony',
        'urdu_meaning': 'مسح',
        'primary_meaning': 'consecrate',
        'secondary_meaning': 'bless',
        'tertiary_meaning': 'anoint',
        'sentence': 'The priest would anoint the newborn with holy oil as a symbol of purification.'
    },
    79: {
        'word': 'Anomalous',
        'english_meaning': 'deviating from what is standard, normal, or expected',
        'urdu_meaning': 'غیر معمولی',
        'primary_meaning': 'abnormal',
        'secondary_meaning': 'irregular',
        'tertiary_meaning': 'anomalous',
        'sentence': 'The scientist discovered an anomalous phenomenon that challenged existing theories.'
    },
    80: {
        'word': 'Anomaly',
        'english_meaning': 'something that deviates from what is standard, normal, or expected',
        'urdu_meaning': 'غیر معمولی',
        'primary_meaning': 'aberration',
        'secondary_meaning': 'irregularity',
        'tertiary_meaning': 'anomaly',
        'sentence': 'The unexpected results in the experiment were considered an anomaly by the research team.'
    },
    81: {
        'word': 'Antagonistic',
        'english_meaning': 'showing or feeling active opposition or hostility toward someone or something',
        'urdu_meaning': 'مخالفتی',
        'primary_meaning': 'hostile',
        'secondary_meaning': 'adversarial',
        'tertiary_meaning': 'antagonistic',
        'sentence': 'The antagonistic behavior of the rival teams intensified the competition.'
    },
    82: {
        'word': 'Antagonize',
        'english_meaning': 'cause someone to become hostile',
        'urdu_meaning': 'مخالفت پیدا کرنا',
        'primary_meaning': 'provoke',
        'secondary_meaning': 'antagonize',
        'tertiary_meaning': 'irritate',
        'sentence': "It's essential not to antagonize others with offensive remarks, promoting a more peaceful environment."
    },
    83: {
        'word': 'Antedate',
        'english_meaning': 'precede in time; come before (something) in date',
        'urdu_meaning': 'تاریخ سے پہلے ہونا',
        'primary_meaning': 'precede',
        'secondary_meaning': 'predate',
        'tertiary_meaning': 'antedate',
        'sentence': 'The historical artifacts antedate the establishment of the museum, providing a glimpse into ancient civilizations.'
    },
    84: {
        'word': 'Antipathy',
        'english_meaning': 'a deep-seated feeling of dislike; aversion',
        'urdu_meaning': 'نفرت',
        'primary_meaning': 'aversion',
        'secondary_meaning': 'dislike',
        'tertiary_meaning': 'antipathy',
        'sentence': 'Despite their efforts to get along, there was a mutual antipathy between the two colleagues.'
    },
    85: {
        'word': 'Antiquity',
        'english_meaning': 'the ancient past, especially the period before the Middle Ages',
        'urdu_meaning': 'قدیم دور',
        'primary_meaning': 'ancient times',
        'secondary_meaning': 'antiquity',
        'tertiary_meaning': 'olden days',
        'sentence': 'The historian dedicated years to the study of artifacts from antiquity.'
    },
    86: {
        'word': 'Antithesis',
        'english_meaning': 'a person or thing that is the direct opposite of someone or something else',
        'urdu_meaning': 'ضد',
        'primary_meaning': 'opposite',
        'secondary_meaning': 'contrary',
        'tertiary_meaning': 'antithesis',
        'sentence': "The character of the villain served as the antithesis to the hero's virtuous nature."
    },
    87: {
        'word': 'Apathy',
        'english_meaning': 'lack of interest, enthusiasm, or concern',
        'urdu_meaning': 'سرد مہری',
        'primary_meaning': 'indifference',
        'secondary_meaning': 'unconcern',
        'tertiary_meaning': 'apathy',
        'sentence': 'The widespread apathy toward political issues led to low voter turnout.'
    },
    88: {
        'word': 'Aphorism',
        'english_meaning': 'a concise and insightful statement of truth or opinion',
        'urdu_meaning': 'حکمت',
        'primary_meaning': 'wisdom',
        'secondary_meaning': 'maxim',
        'tertiary_meaning': 'aphorism',
        'sentence': 'The book was filled with aphorisms that offered valuable life advice.'
    },
    89: {
        'word': 'Aplomb',
        'english_meaning': 'self-confidence or assurance, especially when in a demanding situation',
        'urdu_meaning': 'اعتماد',
        'primary_meaning': 'poise',
        'secondary_meaning': 'assurance',
        'tertiary_meaning': 'aplomb',
        'sentence': 'Despite the challenges, the speaker addressed the audience with remarkable aplomb.'
    },
    90: {
        'word': 'Apogee',
        'english_meaning': 'the highest point in the development of something; climax or culmination',
        'urdu_meaning': 'عروج',
        'primary_meaning': 'peak',
        'secondary_meaning': 'zenith',
        'tertiary_meaning': 'apogee',
        'sentence': 'The success of the space mission marked the apogee of human achievement in exploration.'
    },
    91: {
        'word': 'Apologist',
        'english_meaning': 'a person who offers an argument in defense of something controversial',
        'urdu_meaning': 'دفاعی',
        'primary_meaning': 'defender',
        'secondary_meaning': 'advocate',
        'tertiary_meaning': 'supporter',
        'sentence': 'He was an apologist for the controversial policy.'
    },
    92: {
        'word': 'Appease',
        'english_meaning': 'to calm or satisfy by giving into demands',
        'urdu_meaning': 'پرسکون کرنا',
        'primary_meaning': 'pacify',
        'secondary_meaning': 'placate',
        'tertiary_meaning': 'conciliate',
        'sentence': 'The leader tried to appease the angry crowd by addressing their concerns.'
    },
    93: {
        'word': 'Apposite',
        'english_meaning': 'appropriate or suitable in the circumstances',
        'urdu_meaning': 'مناسب',
        'primary_meaning': 'relevant',
        'secondary_meaning': 'pertinent',
        'tertiary_meaning': 'fitting',
        'sentence': 'His apposite remarks added value to the discussion.'
    },
    94: {
        'word': 'Apprehension',
        'english_meaning': 'anxiety or fear that something bad or unpleasant will happen',
        'urdu_meaning': 'خوف',
        'primary_meaning': 'anxiety',
        'secondary_meaning': 'dread',
        'tertiary_meaning': 'worry',
        'sentence': 'The news of the approaching storm caused apprehension among the residents.'
    },
    95: {
        'word': 'Apprise',
        'english_meaning': 'to inform or notify',
        'urdu_meaning': 'مطلع کرنا',
        'primary_meaning': 'inform',
        'secondary_meaning': 'brief',
        'tertiary_meaning': 'update',
        'sentence': 'Please apprise me of any changes to the schedule.'
    },
    96: {
        'word': 'Approbation',
        'english_meaning': 'approval or praise',
        'urdu_meaning': 'تعریف',
        'primary_meaning': 'approval',
        'secondary_meaning': 'commendation',
        'tertiary_meaning': 'acclaim',
        'sentence': 'Her performance received widespread approbation from the audience.'
    },
    97: {
        'word': 'Appropriate',
        'english_meaning': 'suitable or proper in the circumstances',
        'urdu_meaning': 'مناسب',
        'primary_meaning': 'suitable',
        'secondary_meaning': 'fitting',
        'tertiary_meaning': 'proper',
        'sentence': 'It is important to wear appropriate attire for the formal event.'
    },
    98: {
        'word': 'Apropos',
        'english_meaning': 'with regard to or concerning',
        'urdu_meaning': 'متعلقہ',
        'primary_meaning': 'regarding',
        'secondary_meaning': 'concerning',
        'tertiary_meaning': 'related to',
        'sentence': 'His comments were apropos to the current discussion.'
    },
    99: {
        'word': 'Apt',
        'english_meaning': 'suitable or appropriate in the circumstances',
        'urdu_meaning': 'مناسب',
        'primary_meaning': 'appropriate',
        'secondary_meaning': 'fitting',
        'tertiary_meaning': 'suitable',
        'sentence': 'She is apt at finding solutions to complex problems.'
    },
    100: {
        'word': 'Arbitrary',
        'english_meaning': 'based on random choice or personal whim, rather than any reason or system',
        'urdu_meaning': 'منصفانہ نہیں',
        'primary_meaning': 'random',
        'secondary_meaning': 'unpredictable',
        'tertiary_meaning': 'capricious',
        'sentence': 'The decision seemed arbitrary and lacked a clear rationale.'
    },
    101: {
        'word': 'Arcane',
        'english_meaning': 'understood by few; mysterious or secret',
        'urdu_meaning': 'رازی',
        'primary_meaning': 'mysterious',
        'secondary_meaning': 'esoteric',
        'tertiary_meaning': 'obscure',
        'sentence': 'The ancient manuscript contained arcane symbols and rituals.'
    },
    102: {
        'word': 'Archaic',
        'english_meaning': 'very old or old-fashioned',
        'urdu_meaning': 'قدیم',
        'primary_meaning': 'ancient',
        'secondary_meaning': 'outdated',
        'tertiary_meaning': 'antiquated',
        'sentence': 'The archaic language used in the text made it difficult to understand.'
    },
    103: {
        'word': 'Archetype',
        'english_meaning': 'a very typical example of a certain person or thing',
        'urdu_meaning': 'اصل',
        'primary_meaning': 'original',
        'secondary_meaning': 'prototype',
        'tertiary_meaning': 'exemplar',
        'sentence': 'The hero in the story is often seen as an archetype of bravery.'
    },
    104: {
        'word': 'Ardent',
        'english_meaning': 'enthusiastic or passionate',
        'urdu_meaning': 'جذباتی',
        'primary_meaning': 'passionate',
        'secondary_meaning': 'zealous',
        'tertiary_meaning': 'fervent',
        'sentence': 'She is an ardent supporter of environmental causes.'
    },
    105: {
        'word': 'Arduous',
        'english_meaning': 'requiring a lot of effort and hard work',
        'urdu_meaning': 'مشکل',
        'primary_meaning': 'difficult',
        'secondary_meaning': 'challenging',
        'tertiary_meaning': 'demanding',
        'sentence': 'The climb to the mountain peak was arduous but rewarding.'
    },
    106: {
        'word': 'Arresting',
        'english_meaning': 'attracting attention; striking',
        'urdu_meaning': 'دھانی',
        'primary_meaning': 'striking',
        'secondary_meaning': 'captivating',
        'tertiary_meaning': 'impressive',
        'sentence': 'The painting had an arresting quality that drew viewers in.'
    },
    107: {
        'word': 'Artful',
        'english_meaning': 'clever and cunning, especially in a deceitful way',
        'urdu_meaning': 'فنی',
        'primary_meaning': 'cunning',
        'secondary_meaning': 'crafty',
        'tertiary_meaning': 'sly',
        'sentence': "The politician's artful tactics helped him win the election."
    },
    108: {
        'word': 'Articulate',
        'english_meaning': 'expressing oneself clearly and effectively',
        'urdu_meaning': 'صحیح',
        'primary_meaning': 'expressive',
        'secondary_meaning': 'eloquent',
        'tertiary_meaning': 'fluent',
        'sentence': 'She was able to articulate her thoughts in a persuasive manner.'
    },
    109: {
        'word': 'Artless',
        'english_meaning': 'without guile or deception; innocent',
        'urdu_meaning': 'صاف',
        'primary_meaning': 'innocent',
        'secondary_meaning': 'naive',
        'tertiary_meaning': 'unsophisticated',
        'sentence': 'His artless sincerity won the trust of those around him.'
    },
    110: {
        'word': 'Ascertain',
        'english_meaning': 'to find out for certain; to make sure of',
        'urdu_meaning': 'تصدیق کرنا',
        'primary_meaning': 'verify',
        'secondary_meaning': 'confirm',
        'tertiary_meaning': 'determine',
        'sentence': 'We need to ascertain the accuracy of the information before presenting it.'
    },
    111: {
        'word': 'Ascetic',
        'english_meaning': 'characterized by self-discipline and abstention from indulgence, typically for religious reasons',
        'urdu_meaning': 'زہدی',
        'primary_meaning': 'austere',
        'secondary_meaning': 'self-disciplined',
        'tertiary_meaning': 'abstinent',
        'sentence': 'The ascetic monk lived a simple and disciplined life.'
    },
    112: {
        'word': 'Ascribe',
        'english_meaning': 'to attribute or credit to a particular cause or source',
        'urdu_meaning': 'نسبت دینا',
        'primary_meaning': 'attribute',
        'secondary_meaning': 'assign',
        'tertiary_meaning': 'credit',
        'sentence': 'They sought to ascribe the success of the project to effective teamwork.'
    },
    113: {
        'word': 'Aspersion',
        'english_meaning': 'an attack on the reputation or integrity of someone or something',
        'urdu_meaning': 'بدنامی',
        'primary_meaning': 'slander',
        'secondary_meaning': 'defamation',
        'tertiary_meaning': 'smear',
        'sentence': 'The false accusations were an unjust aspersion on his character.'
    },
    114: {
        'word': 'Assail',
        'english_meaning': 'to attack violently or criticize strongly',
        'urdu_meaning': 'حملہ کرنا',
        'primary_meaning': 'attack',
        'secondary_meaning': 'assault',
        'tertiary_meaning': 'criticize',
        'sentence': 'The enemy tried to assail the fortress, but the defenders held their ground.'
    },
    115: {
        'word': 'Assertive',
        'english_meaning': "confident and forceful in stating one's opinions",
        'urdu_meaning': 'استوار',
        'primary_meaning': 'confident',
        'secondary_meaning': 'self-assured',
        'tertiary_meaning': 'decisive',
        'sentence': 'She was assertive in presenting her ideas during the meeting.'
    },
    116: {
        'word': 'Assiduous',
        'english_meaning': 'showing great care, attention, and effort',
        'urdu_meaning': 'محنتی',
        'primary_meaning': 'diligent',
        'secondary_meaning': 'meticulous',
        'tertiary_meaning': 'hardworking',
        'sentence': 'His assiduous work ethic contributed to the success of the project.'
    },
    117: {
        'word': 'Assuage',
        'english_meaning': 'to make an unpleasant feeling less intense; to alleviate',
        'urdu_meaning': 'کم کرنا',
        'primary_meaning': 'relieve',
        'secondary_meaning': 'mitigate',
        'tertiary_meaning': 'soothe',
        'sentence': 'The apology helped to assuage her hurt feelings.'
    },
    118: {
        'word': 'Astonish',
        'english_meaning': 'to surprise or amaze greatly',
        'urdu_meaning': 'حیران کرنا',
        'primary_meaning': 'amaze',
        'secondary_meaning': 'startle',
        'tertiary_meaning': 'astound',
        'sentence': "The magician's tricks never failed to astonish the audience."
    },
    119: {
        'word': 'Astound',
        'english_meaning': 'to shock or greatly surprise',
        'urdu_meaning': 'حیران کرنا',
        'primary_meaning': 'amaze',
        'secondary_meaning': 'stun',
        'tertiary_meaning': 'astound',
        'sentence': 'The incredible news astounded everyone who heard it.'
    },
    120: {
        'word': 'Astringent',
        'english_meaning': 'sharp or severe in manner or style',
        'urdu_meaning': 'شدید',
        'primary_meaning': 'severe',
        'secondary_meaning': 'strict',
        'tertiary_meaning': 'harsh',
        'sentence': 'Her astringent criticism left no room for interpretation.'
    },
    121: {
        'word': 'Astute',
        'english_meaning': 'having or showing an ability to accurately assess situations or people and turn this to one’s advantage',
        'urdu_meaning': 'ہوشیار',
        'primary_meaning': 'perceptive',
        'secondary_meaning': 'shrewd',
        'tertiary_meaning': 'clever',
        'sentence': 'His astute observations allowed him to make wise decisions.'
    },
    122: {
        'word': 'Attainment',
        'english_meaning': 'the action or fact of achieving a goal toward which one has worked',
        'urdu_meaning': 'حصول',
        'primary_meaning': 'achievement',
        'secondary_meaning': 'accomplishment',
        'tertiary_meaning': 'attainment',
        'sentence': 'The attainment of the project goals was celebrated by the team.'
    },
    123: {
        'word': 'Attenuate',
        'english_meaning': 'to reduce the force, effect, or value of',
        'urdu_meaning': 'کم کرنا',
        'primary_meaning': 'weaken',
        'secondary_meaning': 'diminish',
        'tertiary_meaning': 'reduce',
        'sentence': 'The medication helped to attenuate the symptoms of the illness.'
    },
    124: {
        'word': 'Attribute',
        'english_meaning': 'regard something as being caused by someone or something',
        'urdu_meaning': 'نسبت دینا',
        'primary_meaning': 'ascribe',
        'secondary_meaning': 'credit',
        'tertiary_meaning': 'assign',
        'sentence': 'She was quick to attribute the success to the collaborative efforts of the team.'
    },
    125: {
        'word': 'Atypical',
        'english_meaning': 'not representative of a type, group, or class',
        'urdu_meaning': 'غیر معمولی',
        'primary_meaning': 'unusual',
        'secondary_meaning': 'non-typical',
        'tertiary_meaning': 'abnormal',
        'sentence': 'His behavior was atypical for someone in his position.'
    },
    126: {
        'word': 'Audacious',
        'english_meaning': 'showing a willingness to take surprisingly bold risks',
        'urdu_meaning': 'بے باک',
        'primary_meaning': 'bold',
        'secondary_meaning': 'daring',
        'tertiary_meaning': 'adventurous',
        'sentence': 'The audacious plan aimed to revolutionize the industry.'
    },
    127: {
        'word': 'Audacity',
        'english_meaning': 'the willingness to take bold risks',
        'urdu_meaning': 'بے باکی',
        'primary_meaning': 'boldness',
        'secondary_meaning': 'daring',
        'tertiary_meaning': 'courage',
        'sentence': 'She faced the challenge with remarkable audacity.'
    },
    128: {
        'word': 'Augment',
        'english_meaning': 'to make something greater by adding to it; increase',
        'urdu_meaning': 'براہ راست',
        'primary_meaning': 'increase',
        'secondary_meaning': 'enlarge',
        'tertiary_meaning': 'expand',
        'sentence': 'The company decided to augment its production capacity to meet growing demand.'
    },
    129: {
        'word': 'August',
        'english_meaning': 'respected and impressive',
        'urdu_meaning': 'معزز',
        'primary_meaning': 'dignified',
        'secondary_meaning': 'majestic',
        'tertiary_meaning': 'venerable',
        'sentence': 'The professor had an august presence in the academic community.'
    },
    130: {
        'word': 'Auspicious',
        'english_meaning': 'conducive to success; favorable',
        'urdu_meaning': 'مبارک',
        'primary_meaning': 'favorable',
        'secondary_meaning': 'promising',
        'tertiary_meaning': 'propitious',
        'sentence': 'The wedding ceremony began under auspicious weather conditions.'
    },
    131: {
        'word': 'Austere',
        'english_meaning': 'severe or strict in manner, attitude, or appearance',
        'urdu_meaning': 'سادہ',
        'primary_meaning': 'rigorous',
        'secondary_meaning': 'stern',
        'tertiary_meaning': 'austere',
        'sentence': "The austere design of the building reflected the architect's minimalist approach."
    },
    132: {
        'word': 'Austerity',
        'english_meaning': 'the quality of being austere; sternness or severity of manner or attitude',
        'urdu_meaning': 'سادگی',
        'primary_meaning': 'severity',
        'secondary_meaning': 'rigor',
        'tertiary_meaning': 'strictness',
        'sentence': 'The austerity of his leadership style earned both respect and fear.'
    },
    133: {
        'word': 'Autonomous',
        'english_meaning': 'having the freedom to govern itself or control its own affairs',
        'urdu_meaning': 'خود مختار',
        'primary_meaning': 'self-governing',
        'secondary_meaning': 'independent',
        'tertiary_meaning': 'autonomous',
        'sentence': 'The region gained autonomous status and the ability to make its own decisions.'
    },
    134: {
        'word': 'Auxiliary',
        'english_meaning': 'providing supplementary or additional support',
        'urdu_meaning': 'مدد گار',
        'primary_meaning': 'supporting',
        'secondary_meaning': 'ancillary',
        'tertiary_meaning': 'secondary',
        'sentence': 'The auxiliary power source kicked in when the main generator failed.'
    },
    135: {
        'word': 'Avarice',
        'english_meaning': 'extreme greed for wealth or material gain',
        'urdu_meaning': 'حرص',
        'primary_meaning': 'greed',
        'secondary_meaning': 'covetousness',
        'tertiary_meaning': 'acquisitiveness',
        'sentence': 'His avarice led him to engage in unethical business practices.'
    },
    136: {
        'word': 'Avaricious',
        'english_meaning': 'having an extreme greed for wealth or material gain',
        'urdu_meaning': 'حرصی',
        'primary_meaning': 'greedy',
        'secondary_meaning': 'covetous',
        'tertiary_meaning': 'rapacious',
        'sentence': 'The avaricious businessman would stop at nothing to increase his wealth.'
    },
    137: {
        'word': 'Aver',
        'english_meaning': 'to state or assert to be the case',
        'urdu_meaning': 'اقرار کرنا',
        'primary_meaning': 'assert',
        'secondary_meaning': 'affirm',
        'tertiary_meaning': 'declare',
        'sentence': 'He would aver his innocence despite the evidence against him.'
    },
    138: {
        'word': 'Aversion',
        'english_meaning': 'a strong dislike or disinclination',
        'urdu_meaning': 'نفرت',
        'primary_meaning': 'dislike',
        'secondary_meaning': 'hatred',
        'tertiary_meaning': 'repugnance',
        'sentence': 'She had an aversion to public speaking and avoided it whenever possible.'
    },
    139: {
        'word': 'Avert',
        'english_meaning': 'to turn away or prevent',
        'urdu_meaning': 'ٹالنا',
        'primary_meaning': 'prevent',
        'secondary_meaning': 'avert',
        'tertiary_meaning': 'deter',
        'sentence': 'He managed to avert a potential disaster through quick thinking.'
    },
    140: {
        'word': 'Avid',
        'english_meaning': 'having a keen interest or enthusiasm for something',
        'urdu_meaning': 'شوقین',
        'primary_meaning': 'enthusiastic',
        'secondary_meaning': 'eager',
        'tertiary_meaning': 'passionate',
        'sentence': 'She is an avid reader, always eager to explore new books.'
    },
    141: {
        'word': 'Axiomatic',
        'english_meaning': 'self-evident or unquestionable',
        'urdu_meaning': 'صحیح',
        'primary_meaning': 'self-evident',
        'secondary_meaning': 'obvious',
        'tertiary_meaning': 'undeniable',
        'sentence': 'It is axiomatic that honesty is the best policy.'
    },
    142: {
        'word': 'Baffling',
        'english_meaning': 'impossible to understand; perplexing',
        'urdu_meaning': 'پریشانی',
        'primary_meaning': 'confusing',
        'secondary_meaning': 'bewildering',
        'tertiary_meaning': 'puzzling',
        'sentence': 'The mysterious disappearance of the artifact was baffling to investigators.'
    },
    143: {
        'word': 'Balloon',
        'english_meaning': 'to increase rapidly; to swell or puff out',
        'urdu_meaning': 'پھولنا',
        'primary_meaning': 'swell',
        'secondary_meaning': 'expand',
        'tertiary_meaning': 'inflate',
        'sentence': "The company's profits began to balloon after the successful product launch."
    },
    144: {
        'word': 'Banal',
        'english_meaning': 'lacking in originality; commonplace',
        'urdu_meaning': 'عام',
        'primary_meaning': 'ordinary',
        'secondary_meaning': 'unoriginal',
        'tertiary_meaning': 'trite',
        'sentence': "The speaker's banal remarks failed to capture the audience's attention."
    },
    145: {
        'word': 'Banish',
        'english_meaning': 'to expel or send away, especially from a country or place as a punishment',
        'urdu_meaning': 'نکال دینا',
        'primary_meaning': 'expel',
        'secondary_meaning': 'cast out',
        'tertiary_meaning': 'deport',
        'sentence': 'The king decided to banish the traitor from the kingdom.'
    },
    146: {
        'word': 'Banter',
        'english_meaning': 'playful and friendly exchange of teasing remarks',
        'urdu_meaning': 'مذاق',
        'primary_meaning': 'teasing',
        'secondary_meaning': 'joking',
        'tertiary_meaning': 'raillery',
        'sentence': 'The banter between friends added a lighthearted atmosphere to the gathering.'
    },
    147: {
        'word': 'Baroque',
        'english_meaning': 'characterized by ornate detail; extravagant and complex in style',
        'urdu_meaning': 'باروک',
        'primary_meaning': 'ornate',
        'secondary_meaning': 'elaborate',
        'tertiary_meaning': 'extravagant',
        'sentence': "The cathedral's baroque architecture featured intricate carvings and decorative elements."
    },
    148: {
        'word': 'Barrage',
        'english_meaning': 'a concentrated artillery or gunfire to protect against attack',
        'urdu_meaning': 'بم باری',
        'primary_meaning': 'bombardment',
        'secondary_meaning': 'shelling',
        'tertiary_meaning': 'attack',
        'sentence': 'The soldiers unleashed a barrage of gunfire to repel the advancing enemy.'
    },
    149: {
        'word': 'Barren',
        'english_meaning': 'unproductive and infertile; not producing results or fruit',
        'urdu_meaning': 'بنجر',
        'primary_meaning': 'unproductive',
        'secondary_meaning': 'infertile',
        'tertiary_meaning': 'sterile',
        'sentence': 'The barren land yielded little sustenance for the struggling community.'
    },
    150: {
        'word': 'Base',
        'english_meaning': 'having low moral qualities; lacking principles',
        'urdu_meaning': 'نیچ',
        'primary_meaning': 'immoral',
        'secondary_meaning': 'unprincipled',
        'tertiary_meaning': 'vulgar',
        'sentence': 'His base actions were condemned by those who valued ethical behavior.'
    },
    151: {
        'word': 'Baseness',
        'english_meaning': 'the quality of lacking higher values or moral qualities',
        'urdu_meaning': 'نیچی',
        'primary_meaning': 'immorality',
        'secondary_meaning': 'depravity',
        'tertiary_meaning': 'vulgarity',
        'sentence': "The baseness of the character's actions shocked the audience."
    },
    152: {
        'word': 'Bawdy',
        'english_meaning': 'indecent or humorous in a vulgar way',
        'urdu_meaning': 'فحش',
        'primary_meaning': 'indecent',
        'secondary_meaning': 'risqué',
        'tertiary_meaning': 'lewd',
        'sentence': "The comedian's bawdy jokes elicited laughter from the audience."
    },
    153: {
        "word": "Bearing",
        "english_meaning": "the way one behaves or conducts oneself",
        "urdu_meaning": "رویہ",
        "primary_meaning": "demeanor",
        "secondary_meaning": "attitude",
        "tertiary_meaning": "posture",
        "sentence": "Her bearing during the interview was confident and professional."
    },
    154: {
        "word": "Befriend",
        "english_meaning": "to become friends with someone",
        "urdu_meaning": "دوست بنانا",
        "primary_meaning": "make friends with",
        "secondary_meaning": "befriending",
        "tertiary_meaning": "befriended",
        "sentence": "He decided to befriend his new neighbor and invited them for coffee."
    },
    155: {
        "word": "Befuddled",
        "english_meaning": "confused or unable to think clearly",
        "urdu_meaning": "الجھا ہوا",
        "primary_meaning": "confused",
        "secondary_meaning": "bewildered",
        "tertiary_meaning": "muddled",
        "sentence": "The complex instructions left him befuddled and unsure of what to do."
    },
    156: {
        "word": "Beguile",
        "english_meaning": "to charm or enchant someone in a deceptive way",
        "urdu_meaning": "بہکانا",
        "primary_meaning": "charm",
        "secondary_meaning": "entice",
        "tertiary_meaning": "captivate",
        "sentence": "The magician used his skills to beguile the audience with an amazing performance."
    },
    157: {
        "word": "Beholden",
        "english_meaning": "owing gratitude or thanks to someone",
        "urdu_meaning": "شکریہ",
        "primary_meaning": "indebted",
        "secondary_meaning": "grateful",
        "tertiary_meaning": "obligated",
        "sentence": "She felt beholden to her mentor for guiding her throughout her career."
    },
    158: {
        "word": "Belie",
        "english_meaning": "to contradict or misrepresent",
        "urdu_meaning": "تردید کرنا",
        "primary_meaning": "contradict",
        "secondary_meaning": "disprove",
        "tertiary_meaning": "mislead",
        "sentence": "His calm demeanor belied the intensity of his emotions."
    },
    159: {
        "word": "Belligerence",
        "english_meaning": "aggressive or warlike behavior",
        "urdu_meaning": "جنگجوئی",
        "primary_meaning": "aggression",
        "secondary_meaning": "hostility",
        "tertiary_meaning": "combativeness",
        "sentence": "The escalating belligerence between the two nations led to increased tensions."
    },
    160: {
        "word": "Belligerent",
        "english_meaning": "hostile and aggressive",
        "urdu_meaning": "جنگجو",
        "primary_meaning": "hostile",
        "secondary_meaning": "combative",
        "tertiary_meaning": "aggressive",
        "sentence": "The belligerent tone of the speech heightened concerns about potential conflict."
    },
    161: {
        "word": "Bemuse",
        "english_meaning": "to confuse or bewilder",
        "urdu_meaning": "حیران کرنا",
        "primary_meaning": "bewilder",
        "secondary_meaning": "perplex",
        "tertiary_meaning": "confound",
        "sentence": "The complex plot of the movie bemused the audience."
    },
    162: {
        "word": "Beneficent",
        "english_meaning": "doing good or producing good results",
        "urdu_meaning": "نیک",
        "primary_meaning": "charitable",
        "secondary_meaning": "benevolent",
        "tertiary_meaning": "kind-hearted",
        "sentence": "The beneficent organization provided support to those in need."
    },
    163: {
        "word": "Benevolent",
        "english_meaning": "kind and generous",
        "urdu_meaning": "رحمان",
        "primary_meaning": "kind",
        "secondary_meaning": "generous",
        "tertiary_meaning": "compassionate",
        "sentence": "Her benevolent nature endeared her to everyone in the community."
    },
    164: {
        "word": "Benign",
        "english_meaning": "gentle and kind; not harmful",
        "urdu_meaning": "مہربان",
        "primary_meaning": "gentle",
        "secondary_meaning": "mild",
        "tertiary_meaning": "non-threatening",
        "sentence": "The doctor assured him that the tumor was benign and not cancerous."
    },
    165: {
        "word": "Berate",
        "english_meaning": "to scold or criticize angrily",
        "urdu_meaning": "ڈانٹنا",
        "primary_meaning": "scold",
        "secondary_meaning": "rebuke",
        "tertiary_meaning": "reprimand",
        "sentence": "She berated her employees for their careless mistakes."
    },
    166: {
        "word": "Bereft",
        "english_meaning": "deprived of or lacking something",
        "urdu_meaning": "محروم",
        "primary_meaning": "deprived",
        "secondary_meaning": "bereaved",
        "tertiary_meaning": "desolate",
        "sentence": "The old man was bereft of family and lived a lonely life."
    },
    167: {
        "word": "Betray",
        "english_meaning": "to be disloyal or unfaithful",
        "urdu_meaning": "دغا دینا",
        "primary_meaning": "disloyal",
        "secondary_meaning": "deceive",
        "tertiary_meaning": "betrayal",
        "sentence": "His actions seemed to betray the trust of his closest friends."
    },
    168: {
        "word": "Bias",
        "english_meaning": "prejudice in favor of or against one thing, person, or group",
        "urdu_meaning": "تعصب",
        "primary_meaning": "prejudice",
        "secondary_meaning": "partiality",
        "tertiary_meaning": "discrimination",
        "sentence": "The news article was criticized for its evident bias towards a particular political stance."
    },
    169: {
        "word": "Blemish",
        "english_meaning": "a small mark or flaw that spoils the appearance of something",
        "urdu_meaning": "داغ",
        "primary_meaning": "flaw",
        "secondary_meaning": "imperfection",
        "tertiary_meaning": "blemish",
        "sentence": "The flawless beauty of the painting was marred by a tiny blemish on the canvas."
    },
    170: {
        "word": "Blight",
        "english_meaning": "a thing that spoils or damages something",
        "urdu_meaning": "نقصان",
        "primary_meaning": "decay",
        "secondary_meaning": "ruin",
        "tertiary_meaning": "detriment",
        "sentence": "The blight of pollution had a detrimental effect on the health of the river."
    },
    171: {
        "word": "Blithe",
        "english_meaning": "happy, carefree, and lighthearted",
        "urdu_meaning": "خوش",
        "primary_meaning": "happy",
        "secondary_meaning": "cheerful",
        "tertiary_meaning": "carefree",
        "sentence": "She greeted everyone with a blithe spirit, spreading joy wherever she went."
    },
    172: {
        "word": "Blunt",
        "english_meaning": "having a dull edge or point; straightforward and direct",
        "urdu_meaning": "بے تیز",
        "primary_meaning": "dull",
        "secondary_meaning": "sharp",
        "tertiary_meaning": "direct",
        "sentence": "The chef used a blunt knife to chop the vegetables, making the task more challenging."
    },
    173: {
        "word": "Bogus",
        "english_meaning": "not genuine or true; fake",
        "urdu_meaning": "جعلی",
        "primary_meaning": "fake",
        "secondary_meaning": "counterfeit",
        "tertiary_meaning": "phony",
        "sentence": "The website advertised bogus products that never arrived."
    },
    174: {
        "word": "Boisterous",
        "english_meaning": "noisy, energetic, and cheerful",
        "urdu_meaning": "شوریدہ",
        "primary_meaning": "energetic",
        "secondary_meaning": "rowdy",
        "tertiary_meaning": "lively",
        "sentence": "The children had a boisterous playtime in the park, laughing and running around."
    },
    175: {
        "word": "Bolster",
        "english_meaning": "to support or strengthen",
        "urdu_meaning": "مضبوط کرنا",
        "primary_meaning": "support",
        "secondary_meaning": "strengthen",
        "tertiary_meaning": "reinforce",
        "sentence": "The additional evidence helped bolster their case in court."
    },
    176: {
        "word": "Bombastic",
        "english_meaning": "high-sounding but with little meaning; inflated",
        "urdu_meaning": "گراں گراں",
        "primary_meaning": "pompous",
        "secondary_meaning": "grandiloquent",
        "tertiary_meaning": "pretentious",
        "sentence": "The politician's bombastic speech failed to address the real issues at hand."
    },
    177: {
        "word": "Boon",
        "english_meaning": "a helpful or beneficial thing",
        "urdu_meaning": "نفع",
        "primary_meaning": "benefit",
        "secondary_meaning": "advantage",
        "tertiary_meaning": "blessing",
        "sentence": "The availability of free Wi-Fi was a boon for travelers at the airport."
    },
    178: {
        "word": "Boorish",
        "english_meaning": "rough and bad-mannered; coarse",
        "urdu_meaning": "کچھاکچھ",
        "primary_meaning": "rude",
        "secondary_meaning": "uncouth",
        "tertiary_meaning": "uncivilized",
        "sentence": "His boorish behavior at the dinner party offended many guests."
    },
    179: {
        "word": "Braggart",
        "english_meaning": "a person who boasts about achievements or possessions",
        "urdu_meaning": "شیخی",
        "primary_meaning": "boaster",
        "secondary_meaning": "bragger",
        "tertiary_meaning": "show-off",
        "sentence": "The office braggart constantly talked about his supposed accomplishments."
    },
    180: {
        "word": "Brandish",
        "english_meaning": "to wave or flourish something, especially a weapon, as a threat or in anger",
        "urdu_meaning": "ہاتھ ہلا کر دکھانا",
        "primary_meaning": "wave",
        "secondary_meaning": "flourish",
        "tertiary_meaning": "display",
        "sentence": "The villain entered the scene, brandishing a menacing-looking sword."
    },
    181: {
        "word": "Bravado",
        "english_meaning": "a show of boldness or confidence intended to impress or intimidate others",
        "urdu_meaning": "دلیری",
        "primary_meaning": "swagger",
        "secondary_meaning": "bluster",
        "tertiary_meaning": "bragging",
        "sentence": "His bravado was a façade to hide his insecurities."
    },
    182: {
        "word": "Brazen",
        "english_meaning": "bold and without shame",
        "urdu_meaning": "بے شرم",
        "primary_meaning": "shameless",
        "secondary_meaning": "audacious",
        "tertiary_meaning": "bold",
        "sentence": "The thief had the brazenness to steal in broad daylight."
    },
    183: {
        "word": "Brevity",
        "english_meaning": "conciseness in expression; shortness of time",
        "urdu_meaning": "مختصری",
        "primary_meaning": "conciseness",
        "secondary_meaning": "shortness",
        "tertiary_meaning": "briefness",
        "sentence": "The speaker delivered the message with brevity, capturing the essence in a few words."
    },
    184: {
        "word": "Bridle",
        "english_meaning": "to control or hold back; to show anger or resentment",
        "urdu_meaning": "پگھلانا",
        "primary_meaning": "restrain",
        "secondary_meaning": "curb",
        "tertiary_meaning": "control",
        "sentence": "He had to bridle his anger in the face of unjust accusations."
    },
    185: {
        "word": "Bromide",
        "english_meaning": "a trite or unoriginal remark, especially one intended to soothe or placate",
        "urdu_meaning": "ہلکا پھلکا",
        "primary_meaning": "trite",
        "secondary_meaning": "unoriginal",
        "tertiary_meaning": "hackneyed",
        "sentence": "His speech was filled with clichés and bromides."
    },
    186: {
        "word": "Brook",
        "english_meaning": "a small stream or creek",
        "urdu_meaning": "چھوٹی ندی",
        "primary_meaning": "stream",
        "secondary_meaning": "rivulet",
        "tertiary_meaning": "creek",
        "sentence": "We sat by the brook and enjoyed the peaceful sound of flowing water."
    },
    187: {
        "word": "Bucolic",
        "english_meaning": "relating to the pleasant aspects of the countryside and rural life",
        "urdu_meaning": "دیہاتی",
        "primary_meaning": "rural",
        "secondary_meaning": "rustic",
        "tertiary_meaning": "pastoral",
        "sentence": "The painting depicted a bucolic scene with rolling hills and grazing sheep."
    },
    188: {
        "word": "Buoyancy",
        "english_meaning": "the ability or tendency of something to float in water or air",
        "urdu_meaning": "تیرتا ہوا ہونا",
        "primary_meaning": "floatability",
        "secondary_meaning": "lightness",
        "tertiary_meaning": "upward force",
        "sentence": "The boat's buoyancy allowed it to stay afloat in rough waters."
    },
    189: {
        "word": "Buoyant",
        "english_meaning": "able to float or stay suspended in water or air",
        "urdu_meaning": "تیرتا ہوا",
        "primary_meaning": "floating",
        "secondary_meaning": "light",
        "tertiary_meaning": "uplifting",
        "sentence": "The helium-filled balloon was buoyant and soared into the sky."
    },
    190: {
        "word": "Burgeon",
        "english_meaning": "to begin to grow or increase rapidly; to flourish",
        "urdu_meaning": "فوراً بڑھنا",
        "primary_meaning": "grow",
        "secondary_meaning": "expand",
        "tertiary_meaning": "thrive",
        "sentence": "The city began to burgeon with new businesses and development."
    },
    191: {
        "word": "Burnish",
        "english_meaning": "to polish, especially metal or a surface, to make it smooth and shiny",
        "urdu_meaning": "چمکانا",
        "primary_meaning": "polish",
        "secondary_meaning": "shine",
        "tertiary_meaning": "buff",
        "sentence": "He used a cloth to burnish the silverware and make it gleam."
    },
    192: {
        "word": "Buttress",
        "english_meaning": "a projecting support of stone or brick built against a wall",
        "urdu_meaning": "عمارت کی حمایتی دیوار",
        "primary_meaning": "support",
        "secondary_meaning": "brace",
        "tertiary_meaning": "reinforcement",
        "sentence": "The buttress provided additional support to the ancient cathedral."
    },
    193: {
        "word": "Byzantine",
        "english_meaning": "complicated, intricate, and confusing, typically with elaborate procedures and details",
        "urdu_meaning": "پیچیدہ",
        "primary_meaning": "complex",
        "secondary_meaning": "intricate",
        "tertiary_meaning": "convoluted",
        "sentence": "The Byzantine bureaucracy made it difficult to navigate government processes."
    },
    194: {
        "word": "Cacophonous",
        "english_meaning": "involving or producing a harsh, discordant mixture of sounds",
        "urdu_meaning": "ہری بھری",
        "primary_meaning": "dissonant",
        "secondary_meaning": "unharmonious",
        "tertiary_meaning": "jarring",
        "sentence": "The cacophonous noise of the construction site disturbed the neighborhood."
    },
    195: {
        "word": "Cajole",
        "english_meaning": "to persuade someone to do something by sustained coaxing or flattery",
        "urdu_meaning": "پھسلانا",
        "primary_meaning": "coax",
        "secondary_meaning": "persuade",
        "tertiary_meaning": "sweet-talk",
        "sentence": "She tried to cajole her friend into joining her on the adventure."
    },
    196: {
        "word": "Calamitous",
        "english_meaning": "causing great damage, destruction, or disaster",
        "urdu_meaning": "مصیبت آمیز",
        "primary_meaning": "disastrous",
        "secondary_meaning": "catastrophic",
        "tertiary_meaning": "tragic",
        "sentence": "The earthquake had calamitous effects on the small town."
    },
    197: {
        "word": "Calibrate",
        "english_meaning": "to adjust or mark (a measuring instrument) so that it functions accurately",
        "urdu_meaning": "ٹھیک کرنا",
        "primary_meaning": "adjust",
        "secondary_meaning": "calibrate",
        "tertiary_meaning": "fine-tune",
        "sentence": "The technician needed to calibrate the scale for precise measurements."
    },
    198: {
        "word": "Callous",
        "english_meaning": "emotionally insensitive; unfeeling",
        "urdu_meaning": "سنگ دل",
        "primary_meaning": "uncompassionate",
        "secondary_meaning": "indifferent",
        "tertiary_meaning": "unconcerned",
        "sentence": "His callous remarks hurt the feelings of those around him."
    },
    199: {
        "word": "Callow",
        "english_meaning": "inexperienced and immature",
        "urdu_meaning": "نوآموز",
        "primary_meaning": "inexperienced",
        "secondary_meaning": "immature",
        "tertiary_meaning": "naive",
        "sentence": "His callow understanding of the business world led to mistakes."
    },
    200: {
        "word": "Calumny",
        "english_meaning": "false and malicious statement designed to injure the reputation of someone",
        "urdu_meaning": "غیبت",
        "primary_meaning": "slander",
        "secondary_meaning": "defamation",
        "tertiary_meaning": "smear",
        "sentence": "The politician was a victim of vicious calumny during the election campaign."
    },
    201: {
        "word": "Camaraderie",
        "english_meaning": "mutual trust and friendship among people who spend a lot of time together",
        "urdu_meaning": "دوستی",
        "primary_meaning": "companionship",
        "secondary_meaning": "fellowship",
        "tertiary_meaning": "amity",
        "sentence": "The soldiers developed a strong camaraderie during their time in the trenches."
    },
    202: {
        "word": "Candid",
        "english_meaning": "truthful and straightforward; frank",
        "urdu_meaning": "صاف",
        "primary_meaning": "open",
        "secondary_meaning": "honest",
        "tertiary_meaning": "sincere",
        "sentence": "She appreciated his candid remarks, even though they were critical."
    },
    203: {
        "word": "Candor",
        "english_meaning": "the quality of being open and honest in expression; frankness",
        "urdu_meaning": "صراحت",
        "primary_meaning": "frankness",
        "secondary_meaning": "openness",
        "tertiary_meaning": "honesty",
        "sentence": "The journalist was known for her candor in reporting difficult truths."
    },
    204: {
        "word": "Canny",
        "english_meaning": "having or showing shrewdness and good judgment, especially in money or business matters",
        "urdu_meaning": "ہوش",
        "primary_meaning": "clever",
        "secondary_meaning": "sharp-witted",
        "tertiary_meaning": "astute",
        "sentence": "The canny investor made wise decisions in a volatile market."
    },
    205: {
        "word": "Canonize",
        "english_meaning": "to officially declare a dead person to be a saint",
        "urdu_meaning": "تقدیس کرنا",
        "primary_meaning": "saintify",
        "secondary_meaning": "glorify",
        "tertiary_meaning": "celebrate",
        "sentence": "The Pope decided to canonize the nun for her selfless acts of charity."
    },
    206: {
        "word": "Capitulate",
        "english_meaning": "to surrender or give in to an opponent; to cease resisting",
        "urdu_meaning": "ہتھیار ڈالنا",
        "primary_meaning": "yield",
        "secondary_meaning": "submit",
        "tertiary_meaning": "surrender",
        "sentence": "The general had no choice but to capitulate when faced with overwhelming odds."
    },
    207: {
        "word": "Caprice",
        "english_meaning": "a sudden and unaccountable change of mood or behavior",
        "urdu_meaning": "جذباتی چیز",
        "primary_meaning": "whim",
        "secondary_meaning": "fancy",
        "tertiary_meaning": "impulse",
        "sentence": "Her caprice made it challenging for others to predict her reactions."
    },
    208: {
        "word": "Capricious",
        "english_meaning": "given to sudden and unaccountable changes of mood or behavior",
        "urdu_meaning": "جذباتی",
        "primary_meaning": "whimsical",
        "secondary_meaning": "fickle",
        "tertiary_meaning": "unpredictable",
        "sentence": "The weather in the region is capricious, with sudden shifts in temperature."
    },
    209: {
        "word": "Captious",
        "english_meaning": "tending to find fault or raise petty objections",
        "urdu_meaning": "تنقیدی",
        "primary_meaning": "critical",
        "secondary_meaning": "faultfinding",
        "tertiary_meaning": "nitpicking",
        "sentence": "His captious comments irritated everyone in the meeting."
    },
    210: {
        "word": "Caricature",
        "english_meaning": "a picture, description, or imitation of a person or thing in which certain striking characteristics are exaggerated to create a comic or grotesque effect",
        "urdu_meaning": "مزاحیہ خاکہ",
        "primary_meaning": "satirical representation",
        "secondary_meaning": "mockery",
        "tertiary_meaning": "lampoon",
        "sentence": "The cartoonist created a caricature of the politician that highlighted his distinctive features."
    },
    211: {
        "word": "Castigate",
        "english_meaning": "to reprimand or criticize severely",
        "urdu_meaning": "سخت ملامت کرنا",
        "primary_meaning": "rebuke",
        "secondary_meaning": "condemn",
        "tertiary_meaning": "chastise",
        "sentence": "The teacher had to castigate the student for repeatedly disrupting the class."
    },
    212: {
        "word": "Cataclysmic",
        "english_meaning": "relating to or denoting a violent natural event",
        "urdu_meaning": "آپہ ہونے والا واقعہ",
        "primary_meaning": "catastrophic",
        "secondary_meaning": "disastrous",
        "tertiary_meaning": "cataclysmal",
        "sentence": "The earthquake was a cataclysmic event that caused widespread destruction."
    },
    213: {
        "word": "Catastrophe",
        "english_meaning": "an event causing great and often sudden damage or suffering; a disaster",
        "urdu_meaning": "آفت",
        "primary_meaning": "tragedy",
        "secondary_meaning": "calamity",
        "tertiary_meaning": "cataclysm",
        "sentence": "The flood was a catastrophe that left many families without homes."
    },
    214: {
        "word": "Cathartic",
        "english_meaning": "providing psychological relief through the expression of strong emotions",
        "urdu_meaning": "تخلیقی",
        "primary_meaning": "cleansing",
        "secondary_meaning": "purifying",
        "tertiary_meaning": "purging",
        "sentence": "Writing in her journal was a cathartic experience that helped her process her emotions."
    },
    215: {
        "word": "Catholic",
        "english_meaning": "including a wide variety of things; all-encompassing",
        "urdu_meaning": "کیتھولک",
        "primary_meaning": "universal",
        "secondary_meaning": "comprehensive",
        "tertiary_meaning": "inclusive",
        "sentence": "The library had a catholic collection of books, covering diverse subjects."
    },
    216: {
        "word": "Caustic",
        "english_meaning": "sarcastic in a scathing and bitter way",
        "urdu_meaning": "کھچاکچ",
        "primary_meaning": "scathing",
        "secondary_meaning": "biting",
        "tertiary_meaning": "acerbic",
        "sentence": "Her caustic remarks about his performance hurt his feelings."
    },
    217: {
        "word": "Cavalier",
        "english_meaning": "showing a lack of proper concern; offhand",
        "urdu_meaning": "لاپرواہ",
        "primary_meaning": "carefree",
        "secondary_meaning": "nonchalant",
        "tertiary_meaning": "indifferent",
        "sentence": "His cavalier attitude towards the project deadlines upset his colleagues."
    },
    218: {
        "word": "Cease",
        "english_meaning": "bring or come to an end",
        "urdu_meaning": "ختم ہونا",
        "primary_meaning": "stop",
        "secondary_meaning": "halt",
        "tertiary_meaning": "terminate",
        "sentence": "The fighting should cease immediately to avoid further casualties."
    },
    219: {
        "word": "Celebrated",
        "english_meaning": "famous or well-known, especially for a particular skill, talent, or achievement",
        "urdu_meaning": "مشہور",
        "primary_meaning": "renowned",
        "secondary_meaning": "acclaimed",
        "tertiary_meaning": "notable",
        "sentence": "The artist is celebrated for his innovative approach to sculpture."
    },
    220: {
        "word": "Censure",
        "english_meaning": "express severe disapproval of someone or something, typically in a formal statement",
        "urdu_meaning": "ملامت کرنا",
        "primary_meaning": "condemn",
        "secondary_meaning": "criticize",
        "tertiary_meaning": "reprimand",
        "sentence": "The committee voted to censure the politician for unethical conduct."
    },
    221: {
        "word": "Cerebral",
        "english_meaning": "intellectual rather than emotional or physical",
        "urdu_meaning": "دماغی",
        "primary_meaning": "intellectual",
        "secondary_meaning": "cognitive",
        "tertiary_meaning": "thoughtful",
        "sentence": "His writing style is highly cerebral, exploring complex ideas and concepts."
    },
    222: {
        "word": "Cessation",
        "english_meaning": "the fact or process of ending or being brought to an end",
        "urdu_meaning": "خاتمہ",
        "primary_meaning": "ending",
        "secondary_meaning": "termination",
        "tertiary_meaning": "halt",
        "sentence": "The ceasefire led to the cessation of hostilities between the two warring factions."
    },
    223: {
        "word": "Chagrin",
        "english_meaning": "distress or embarrassment at having failed or been humiliated",
        "urdu_meaning": "شرمندگی",
        "primary_meaning": "disappointment",
        "secondary_meaning": "humiliation",
        "tertiary_meaning": "mortification",
        "sentence": "His chagrin was evident after he lost the competition."
    },
    224: {
        "word": "Champion",
        "english_meaning": "a person who fights or argues for a cause or on behalf of someone else",
        "urdu_meaning": "حامی",
        "primary_meaning": "advocate",
        "secondary_meaning": "supporter",
        "tertiary_meaning": "defender",
        "sentence": "She became a champion for animal rights and worked tirelessly to promote their welfare."
    },
    225: {
        "word": "Chary",
        "english_meaning": "cautious or careful; wary",
        "urdu_meaning": "ہوشیار",
        "primary_meaning": "circumspect",
        "secondary_meaning": "guarded",
        "tertiary_meaning": "prudent",
        "sentence": "Investors should be chary of putting all their funds into high-risk ventures."
    },
    226: {
        "word": "Chastise",
        "english_meaning": "to reprimand or criticize severely",
        "urdu_meaning": "سزا دینا",
        "primary_meaning": "rebuke",
        "secondary_meaning": "castigate",
        "tertiary_meaning": "scold",
        "sentence": "The teacher had to chastise the students for not completing their assignments on time."
    },
    227: {
        "word": "Chauvinistic",
        "english_meaning": "exaggerated or aggressive patriotism; biased devotion to any group, attitude, or cause",
        "urdu_meaning": "شووینسٹ",
        "primary_meaning": "jingoistic",
        "secondary_meaning": "nationalistic",
        "tertiary_meaning": "bigoted",
        "sentence": "His chauvinistic views were evident in his refusal to consider alternative perspectives."
    },
    228: {
        "word": "Check",
        "english_meaning": "examine or verify; stop or slow down the progress of something",
        "urdu_meaning": "جانچ",
        "primary_meaning": "inspect",
        "secondary_meaning": "verify",
        "tertiary_meaning": "hinder",
        "sentence": "Please check the accuracy of the information before presenting it to the audience."
    },
    229: {
        "word": "Cherish",
        "english_meaning": "to hold dear; feel or show affection for",
        "urdu_meaning": "قدر کرنا",
        "primary_meaning": "treasure",
        "secondary_meaning": "value",
        "tertiary_meaning": "adore",
        "sentence": "She would always cherish the memories of their time together."
    },
    230: {
        "word": "Chicanery",
        "english_meaning": "the use of trickery to achieve a political, financial, or legal purpose",
        "urdu_meaning": "حیلہ",
        "primary_meaning": "deception",
        "secondary_meaning": "trickery",
        "tertiary_meaning": "subterfuge",
        "sentence": "The investigation uncovered a web of chicanery in the corporate dealings."
    },
    231: {
        "word": "Chivalrous",
        "english_meaning": "courteous and gallant, especially toward women",
        "urdu_meaning": "شہرتی",
        "primary_meaning": "gallant",
        "secondary_meaning": "honorable",
        "tertiary_meaning": "courteous",
        "sentence": "He was known for his chivalrous behavior towards everyone he met."
    },
    232: {
        "word": "Churlish",
        "english_meaning": "rude in a mean-spirited and surly way",
        "urdu_meaning": "بے ادب",
        "primary_meaning": "discourteous",
        "secondary_meaning": "ill-mannered",
        "tertiary_meaning": "uncivil",
        "sentence": "His churlish remarks offended everyone at the dinner party."
    },
    233: {
        "word": "Circumscribe",
        "english_meaning": "to restrict within limits; confine",
        "urdu_meaning": "محدود کرنا",
        "primary_meaning": "limit",
        "secondary_meaning": "constrain",
        "tertiary_meaning": "restrain",
        "sentence": "The laws are meant to circumscribe the power of the government."
    },
    234: {
        "word": "Circumspect",
        "english_meaning": "wary and unwilling to take risks",
        "urdu_meaning": "ہوشیار",
        "primary_meaning": "cautious",
        "secondary_meaning": "prudent",
        "tertiary_meaning": "careful",
        "sentence": "A circumspect approach is needed when dealing with sensitive issues."
    },
    235: {
        "word": "Circumstantial",
        "english_meaning": "pointed out by circumstances rather than explicit details",
        "urdu_meaning": "حالاتی",
        "primary_meaning": "incidental",
        "secondary_meaning": "contextual",
        "tertiary_meaning": "related to circumstances",
        "sentence": "The case relied on circumstantial evidence rather than direct proof."
    },
    236: {
        "word": "Cite",
        "english_meaning": "to refer to a source as evidence or justification",
        "urdu_meaning": "حوالہ دینا",
        "primary_meaning": "quote",
        "secondary_meaning": "mention",
        "tertiary_meaning": "refer",
        "sentence": "The author was careful to cite all relevant studies in the research paper."
    },
    237: {
        "word": "Clamorous",
        "english_meaning": "making a loud and confused noise",
        "urdu_meaning": "ہلچلی",
        "primary_meaning": "noisy",
        "secondary_meaning": "boisterous",
        "tertiary_meaning": "vociferous",
        "sentence": "The clamorous protest could be heard from miles away."
    },
    238: {
        "word": "Clandestine",
        "english_meaning": "kept secret or done secretly, often for an illegal or unethical purpose",
        "urdu_meaning": "پوشیدہ",
        "primary_meaning": "secret",
        "secondary_meaning": "covert",
        "tertiary_meaning": "hidden",
        "sentence": "The group held clandestine meetings to plan their activities."
    },
    239: {
        "word": "Clangor",
        "english_meaning": "a continuous loud banging or ringing sound",
        "urdu_meaning": "دھنگ",
        "primary_meaning": "clamor",
        "secondary_meaning": "din",
        "tertiary_meaning": "resounding noise",
        "sentence": "The clangor of construction equipment echoed through the city streets."
    },
    240: {
        "word": "Clearheaded",
        "english_meaning": "thinking clearly and rationally",
        "urdu_meaning": "صاف دماغ",
        "primary_meaning": "level-headed",
        "secondary_meaning": "lucid",
        "tertiary_meaning": "sensible",
        "sentence": "In times of crisis, it's essential to stay clearheaded and make rational decisions."
    },
    241: {
        "word": "Clerical",
        "english_meaning": "relating to office work, especially routine paperwork",
        "urdu_meaning": "دفتری",
        "primary_meaning": "administrative",
        "secondary_meaning": "office-related",
        "tertiary_meaning": "bureaucratic",
        "sentence": "The clerical staff is responsible for managing the paperwork in the office."
    },
    242: {
        "word": "Cloak",
        "english_meaning": "to hide, cover, or disguise something",
        "urdu_meaning": "چھپانا",
        "primary_meaning": "conceal",
        "secondary_meaning": "mask",
        "tertiary_meaning": "camouflage",
        "sentence": "The spy tried to cloak his true identity to avoid detection."
    },
    243: {
        "word": "Clumsy",
        "english_meaning": "awkward in movement or in handling objects; lacking grace",
        "urdu_meaning": "بے ڈھنگا",
        "primary_meaning": "awkward",
        "secondary_meaning": "ungainly",
        "tertiary_meaning": "uncoordinated",
        "sentence": "His clumsy attempts to juggle ended in a series of dropped balls."
    },
    244: {
        "word": "Coalesce",
        "english_meaning": "to come together to form a single whole; unite",
        "urdu_meaning": "متحد ہونا",
        "primary_meaning": "merge",
        "secondary_meaning": "combine",
        "tertiary_meaning": "fuse",
        "sentence": "The two companies decided to coalesce and create a stronger business entity."
    },
    245: {
        "word": "Coddle",
        "english_meaning": "to treat with excessive indulgence or care",
        "urdu_meaning": "آزادی سے پالنا",
        "primary_meaning": "pamper",
        "secondary_meaning": "spoil",
        "tertiary_meaning": "cater to",
        "sentence": "Some parents tend to coddle their children, fearing any discomfort."
    },
    246: {
        "word": "Code",
        "english_meaning": "a system of rules or principles",
        "urdu_meaning": "کوڈ",
        "primary_meaning": "system",
        "secondary_meaning": "protocol",
        "tertiary_meaning": "set of rules",
        "sentence": "The software developer followed a strict code to ensure the security of the application."
    },
    247: {
        "word": "Coercion",
        "english_meaning": "the practice of persuading someone to do something through force or threats",
        "urdu_meaning": "جبر",
        "primary_meaning": "force",
        "secondary_meaning": "intimidation",
        "tertiary_meaning": "duress",
        "sentence": "The use of coercion in negotiations is generally frowned upon."
    },
    248: {
        "word": "Cogent",
        "english_meaning": "clear, logical, and convincing",
        "urdu_meaning": "قائل کن",
        "primary_meaning": "convincing",
        "secondary_meaning": "persuasive",
        "tertiary_meaning": "compelling",
        "sentence": "The speaker presented a cogent argument that swayed the opinion of the audience."
    },
    249: {
        "word": "Cogitate",
        "english_meaning": "to think deeply or consider carefully",
        "urdu_meaning": "غور کرنا",
        "primary_meaning": "contemplate",
        "secondary_meaning": "reflect",
        "tertiary_meaning": "ponder",
        "sentence": "Give me some time to cogitate on your proposal before making a decision."
    },
    250: {
        "word": "Cognizance",
        "english_meaning": "knowledge or awareness of something",
        "urdu_meaning": "آگاہی",
        "primary_meaning": "awareness",
        "secondary_meaning": "consciousness",
        "tertiary_meaning": "recognition",
        "sentence": "The court took cognizance of the new evidence presented by the prosecution."
    },
    251: {
        "word": "Coherent",
        "english_meaning": "logical and consistent; easy to understand",
        "urdu_meaning": "معقول",
        "primary_meaning": "logical",
        "secondary_meaning": "consistent",
        "tertiary_meaning": "clear",
        "sentence": "The professor delivered a coherent lecture that clarified complex concepts for the students."
    },
    252: {
        "word": "Coin",
        "english_meaning": "to invent or create a new word or phrase",
        "urdu_meaning": "نا معمولی لفظ چھوڑنا",
        "primary_meaning": "create",
        "secondary_meaning": "invent",
        "tertiary_meaning": "formulate",
        "sentence": "Shakespeare is known to have coined many words still used in the English language."
    },
    253: {
        "word": "Collaborate",
        "english_meaning": "to work jointly on an activity or project",
        "urdu_meaning": "متعاونیت کرنا",
        "primary_meaning": "cooperate",
        "secondary_meaning": "work together",
        "tertiary_meaning": "collude",
        "sentence": "The scientists decided to collaborate on a research project to combine their expertise."
    },
    254: {
        "word": "Collude",
        "english_meaning": "to secretly conspire or cooperate with others, especially for fraudulent purposes",
        "urdu_meaning": "ملبٹ ہونا",
        "primary_meaning": "conspire",
        "secondary_meaning": "scheme",
        "tertiary_meaning": "plot",
        "sentence": "The companies were accused of colluding to fix prices and limit competition."
    },
    255: {
        "word": "Collusion",
        "english_meaning": "secret or illegal cooperation or conspiracy, especially to cheat or deceive others",
        "urdu_meaning": "ملبٹ",
        "primary_meaning": "conspiracy",
        "secondary_meaning": "connivance",
        "tertiary_meaning": "collaboration",
        "sentence": "The investigation revealed evidence of collusion among several parties involved in the fraud."
    },
    256: {
        "word": "Comity",
        "english_meaning": "courtesy and considerate behavior toward others",
        "urdu_meaning": "خلقیات",
        "primary_meaning": "courtesy",
        "secondary_meaning": "politeness",
        "tertiary_meaning": "consideration",
        "sentence": "In diplomatic circles, comity is essential for maintaining positive relations between nations."
    },
    257: {
        "word": "Commence",
        "english_meaning": "to begin; start",
        "urdu_meaning": "شروع ہونا",
        "primary_meaning": "begin",
        "secondary_meaning": "initiate",
        "tertiary_meaning": "start",
        "sentence": "The ceremony will commence with the singing of the national anthem."
    },
    258: {
        "word": "Commensurate",
        "english_meaning": "corresponding in size or degree; in proportion",
        "urdu_meaning": "موازنہ ہونا",
        "primary_meaning": "proportional",
        "secondary_meaning": "equivalent",
        "tertiary_meaning": "matching",
        "sentence": "The salary offered is commensurate with the candidate's qualifications and experience."
    },
    259: {
        "word": "Commiserate",
        "english_meaning": "to express or feel sympathy or pity; sympathize",
        "urdu_meaning": "ہمدردی کرنا",
        "primary_meaning": "sympathize",
        "secondary_meaning": "console",
        "tertiary_meaning": "comfort",
        "sentence": "Friends gathered to commiserate with him after the loss of his pet."
    },
    260: {
        "word": "Commonplace",
        "english_meaning": "not interesting or original; dull and ordinary",
        "urdu_meaning": "عام",
        "primary_meaning": "ordinary",
        "secondary_meaning": "mundane",
        "tertiary_meaning": "routine",
        "sentence": "His speech was filled with commonplace ideas and clichés."
    },
    261: {
        "word": "Compel",
        "english_meaning": "to force or drive someone to do something",
        "urdu_meaning": "مجبور کرنا",
        "primary_meaning": "force",
        "secondary_meaning": "coerce",
        "tertiary_meaning": "compulsory",
        "sentence": "The circumstances may compel us to take drastic measures."
    },
    262: {
        "word": "Compelling",
        "english_meaning": "evoking interest, attention, or admiration in a powerfully irresistible way",
        "urdu_meaning": "مجذب",
        "primary_meaning": "convincing",
        "secondary_meaning": "persuasive",
        "tertiary_meaning": "captivating",
        "sentence": "The novel had a compelling narrative that kept readers hooked until the end."
    },
    263: {
        "word": "Compete",
        "english_meaning": "to strive to gain or win something by defeating or establishing superiority over others",
        "urdu_meaning": "مقابلہ کرنا",
        "primary_meaning": "contest",
        "secondary_meaning": "rival",
        "tertiary_meaning": "vie",
        "sentence": "Teams from different countries will compete in the international competition."
    },
    264: {
        "word": "Competent",
        "english_meaning": "having the necessary ability, knowledge, or skill to do something successfully",
        "urdu_meaning": "ماہر",
        "primary_meaning": "capable",
        "secondary_meaning": "skilled",
        "tertiary_meaning": "qualified",
        "sentence": "She is a competent professional with years of experience in her field."
    },
    265: {
        "word": "Complacent",
        "english_meaning": "showing uncritical satisfaction with oneself or one's achievements; self-satisfied",
        "urdu_meaning": "خود پسند",
        "primary_meaning": "self-satisfied",
        "secondary_meaning": "smug",
        "tertiary_meaning": "content",
        "sentence": "The team's complacent attitude led to their defeat in the next match."
    },
    266: {
        "word": "Complementary",
        "english_meaning": "combining in such a way as to enhance or emphasize each other's qualities",
        "urdu_meaning": "تکمیلی",
        "primary_meaning": "interrelated",
        "secondary_meaning": "supplementary",
        "tertiary_meaning": "harmonious",
        "sentence": "The two colors are complementary and create a balanced visual effect."
    },
    267: {
        "word": "Compliance",
        "english_meaning": "the action or fact of complying with a wish or command",
        "urdu_meaning": "اطاعت",
        "primary_meaning": "obedience",
        "secondary_meaning": "adherence",
        "tertiary_meaning": "conformity",
        "sentence": "The company ensured strict compliance with safety regulations."
    },
    268: {
        "word": "Compliant",
        "english_meaning": "inclined to agree with others or obey rules, especially to an excessive degree",
        "urdu_meaning": "مطیع",
        "primary_meaning": "obedient",
        "secondary_meaning": "submissive",
        "tertiary_meaning": "docile",
        "sentence": "He was always compliant and never questioned authority."
    },
    269: {
        "word": "Compliment",
        "english_meaning": "a polite expression of praise or admiration",
        "urdu_meaning": "تعریف",
        "primary_meaning": "praise",
        "secondary_meaning": "commendation",
        "tertiary_meaning": "admiration",
        "sentence": "She blushed in response to the sincere compliment about her performance."
    },
    270: {
        "word": "Complimentary",
        "english_meaning": "expressing a compliment; praising or approving",
        "urdu_meaning": "تعریفی",
        "primary_meaning": "praising",
        "secondary_meaning": "approving",
        "tertiary_meaning": "complimenting",
        "sentence": "The manager gave a complimentary review of the employee's excellent work."
    },
    271: {
        "word": "Comply",
        "english_meaning": "act in accordance with a wish or command",
        "urdu_meaning": "مطابقت",
        "primary_meaning": "obey",
        "secondary_meaning": "conform",
        "tertiary_meaning": "adhere",
        "sentence": "All employees are expected to comply with the company's policies and procedures."
    },
    272: {
        "word": "Compounded",
        "english_meaning": "make (something bad) worse; intensify the negative aspects of",
        "urdu_meaning": "بڑھا دینا",
        "primary_meaning": "exacerbate",
        "secondary_meaning": "aggravate",
        "tertiary_meaning": "worsen",
        "sentence": "The financial crisis compounded the challenges facing the struggling economy."
    },
    273: {
        "word": "Comprehensive",
        "english_meaning": "including all or nearly all elements or aspects",
        "urdu_meaning": "جامع",
        "primary_meaning": "complete",
        "secondary_meaning": "thorough",
        "tertiary_meaning": "inclusive",
        "sentence": "The report provides a comprehensive analysis of the current market trends."
    },
    274: {
        "word": "Compromise",
        "english_meaning": "an agreement or settlement of a dispute that is reached by each side making concessions",
        "urdu_meaning": "مفاہمت",
        "primary_meaning": "agreement",
        "secondary_meaning": "settlement",
        "tertiary_meaning": "resolution",
        "sentence": "In order to reach a compromise, both parties had to make sacrifices."
    },
    275: {
        "word": "Conciliatory",
        "english_meaning": "intended or likely to placate or pacify",
        "urdu_meaning": "مصالحتی",
        "primary_meaning": "pacifying",
        "secondary_meaning": "appeasing",
        "tertiary_meaning": "conciliating",
        "sentence": "The leader's conciliatory tone helped ease tensions between the conflicting groups."
    },
    276: {
        "word": "Conclusive",
        "english_meaning": "serving to settle or decide a question; final and indisputable",
        "urdu_meaning": "اختتامی",
        "primary_meaning": "decisive",
        "secondary_meaning": "definitive",
        "tertiary_meaning": "conclusive",
        "sentence": "The DNA evidence provided conclusive proof of the suspect's guilt."
    },
    277: {
        "word": "Condescending",
        "english_meaning": "having or showing a feeling of patronizing superiority",
        "urdu_meaning": "متکبرانہ",
        "primary_meaning": "patronizing",
        "secondary_meaning": "superior",
        "tertiary_meaning": "condescending",
        "sentence": "Her condescending attitude toward her colleagues alienated them."
    },
    278: {
        "word": "Conditional",
        "english_meaning": "subject to one or more conditions or requirements being met; not absolute",
        "urdu_meaning": "مشروط",
        "primary_meaning": "contingent",
        "secondary_meaning": "dependent",
        "tertiary_meaning": "qualified",
        "sentence": "The agreement was conditional upon the completion of certain tasks."
    },
    279: {
        "word": "Condone",
        "english_meaning": "accept and allow (behavior that is considered morally wrong or offensive) to continue",
        "urdu_meaning": "معاف کرنا",
        "primary_meaning": "overlook",
        "secondary_meaning": "disregard",
        "tertiary_meaning": "excuse",
        "sentence": "The manager decided to condone the minor infraction and gave the employee a second chance."
    },
    280: {
        "word": "Conducive",
        "english_meaning": "making a certain situation or outcome likely or possible",
        "urdu_meaning": "مدد گار",
        "primary_meaning": "favorable",
        "secondary_meaning": "beneficial",
        "tertiary_meaning": "conducive",
        "sentence": "A calm and focused environment is conducive to productive work."
    },
    281: {
        "word": "Conflagration",
        "english_meaning": "an extensive fire that destroys a great deal of land or property",
        "urdu_meaning": "آتش زدہ",
        "primary_meaning": "fire",
        "secondary_meaning": "blaze",
        "tertiary_meaning": "inferno",
        "sentence": "The firefighters worked tirelessly to control the conflagration in the forest."
    },
    282: {
        "word": "Confound",
        "english_meaning": "cause surprise or confusion in (someone), especially by acting against their expectations",
        "urdu_meaning": "حیران کرنا",
        "primary_meaning": "bewilder",
        "secondary_meaning": "baffle",
        "tertiary_meaning": "perplex",
        "sentence": "His sudden resignation confounded everyone in the office."
    },
    283: {
        "word": "Congenial",
        "english_meaning": "pleasant because of a personality, qualities, or interests that are similar to one's own",
        "urdu_meaning": "مناسب",
        "primary_meaning": "friendly",
        "secondary_meaning": "agreeable",
        "tertiary_meaning": "amiable",
        "sentence": "The new employee proved to be congenial, quickly making friends with colleagues."
    },
    284: {
        "word": "Conjectural",
        "english_meaning": "based on guesswork or incomplete evidence; speculative",
        "urdu_meaning": "اندازی",
        "primary_meaning": "speculative",
        "secondary_meaning": "hypothetical",
        "tertiary_meaning": "conjectural",
        "sentence": "The theory was purely conjectural, lacking concrete evidence."
    },
    285: {
        "word": "Conjecture",
        "english_meaning": "an opinion or conclusion formed on the basis of incomplete information",
        "urdu_meaning": "اندازہ",
        "primary_meaning": "speculation",
        "secondary_meaning": "guess",
        "tertiary_meaning": "conclusion",
        "sentence": "Without evidence, his statement was merely a conjecture about the possible outcome."
    },
    286: {
        "word": "Connoisseur",
        "english_meaning": "an expert judge in matters of taste",
        "urdu_meaning": "صاحب فن",
        "primary_meaning": "expert",
        "secondary_meaning": "authority",
        "tertiary_meaning": "connoisseur",
        "sentence": "As a wine connoisseur, he could discern the subtlest flavors in a glass of wine."
    },
    287: {
        "word": "Consensus",
        "english_meaning": "general agreement among a group of people",
        "urdu_meaning": "رائے",
        "primary_meaning": "agreement",
        "secondary_meaning": "concurrence",
        "tertiary_meaning": "consensus",
        "sentence": "After much discussion, the team reached a consensus on the best course of action."
    },
    288: {
        "word": "Consequential",
        "english_meaning": "important; significant; having consequences",
        "urdu_meaning": "اہم",
        "primary_meaning": "significant",
        "secondary_meaning": "important",
        "tertiary_meaning": "consequential",
        "sentence": "The decision had consequential implications for the company's future."
    },
    289: {
        'word': 'Conspicuous',
        'english_meaning': 'easily noticeable; attracting attention',
        'urdu_meaning': 'ظاہر، بھڑکیلا',
        'primary_meaning': 'noticeable',
        'secondary_meaning': 'prominent',
        'tertiary_meaning': 'visible',
        'sentence': 'Her red hat made her quite conspicuous in the crowd.'
    },
    290: {
        'word': 'Conspire',
        'english_meaning': 'to secretly plan together',
        'urdu_meaning': 'مل کر خفیہ منصوبہ بنانا',
        'primary_meaning': 'plot',
        'secondary_meaning': 'scheme',
        'tertiary_meaning': 'collude',
        'sentence': 'The rebels conspired to overthrow the government.'
    },
    291: {
        'word': 'Constraining',
        'english_meaning': 'restricting or limiting',
        'urdu_meaning': 'محدود یا روکنے والا',
        'primary_meaning': 'limiting',
        'secondary_meaning': 'restrictive',
        'tertiary_meaning': 'confining',
        'sentence': 'The constraining regulations made it difficult for businesses to operate freely.'
    },
    292: {
        'word': 'Construe',
        'english_meaning': 'to interpret or understand the meaning of something',
        'urdu_meaning': 'سمجھنا یا ترتیب دینا',
        'primary_meaning': 'interpret',
        'secondary_meaning': 'understand',
        'tertiary_meaning': 'analyze',
        'sentence': 'His silence was construed as a sign of disagreement.'
    },
    293: {
        'word': 'Contemporary',
        'english_meaning': 'belonging to or occurring in the present',
        'urdu_meaning': 'معاصر',
        'primary_meaning': 'modern',
        'secondary_meaning': 'current',
        'tertiary_meaning': 'up-to-date',
        'sentence': 'The museum features both historical artifacts and contemporary art.'
    },
    294: {
        'word': 'Contempt',
        'english_meaning': 'the feeling that someone or something is beneath consideration',
        'urdu_meaning': 'توہین، حقیریت',
        'primary_meaning': 'disdain',
        'secondary_meaning': 'disrespect',
        'tertiary_meaning': 'scorn',
        'sentence': 'His contempt for the new policy was evident in his speech.'
    },
    295: {
        'word': 'Contemptuous',
        'english_meaning': 'showing contempt; scornful',
        'urdu_meaning': 'توہین آمیز، حقیرانہ',
        'primary_meaning': 'disdainful',
        'secondary_meaning': 'disrespectful',
        'tertiary_meaning': 'scornful',
        'sentence': 'She gave him a contemptuous look before walking away.'
    },
    296: {
        'word': 'Contend',
        'english_meaning': 'to compete; to argue or assert',
        'urdu_meaning': 'جدوجہد کرنا، دعوی کرنا',
        'primary_meaning': 'compete',
        'secondary_meaning': 'argue',
        'tertiary_meaning': 'assert',
        'sentence': 'Teams from different countries will contend in the championship.'
    },
    297: {
        'word': 'Contentious',
        'english_meaning': 'causing or likely to cause an argument; controversial',
        'urdu_meaning': 'جھگڑالو، متنازعہ',
        'primary_meaning': 'argumentative',
        'secondary_meaning': 'controversial',
        'tertiary_meaning': 'disputatious',
        'sentence': 'The contentious issue led to heated debates in the parliament.'
    },
    298: {
        'word': 'Contentment',
        'english_meaning': 'a state of happiness and satisfaction',
        'urdu_meaning': 'قنوت، خوشی',
        'primary_meaning': 'happiness',
        'secondary_meaning': 'satisfaction',
        'tertiary_meaning': 'fulfillment',
        'sentence': 'After achieving her goals, she felt a deep sense of contentment.'
    },
    299: {
        'word': 'Contingent',
        'english_meaning': 'dependent on certain conditions; a group of people with a common characteristic',
        'urdu_meaning': 'وابستہ، شرائط پر مبنی',
        'primary_meaning': 'dependent',
        'secondary_meaning': 'conditional',
        'tertiary_meaning': 'contingent group',
        'sentence': 'The success of the project is contingent on securing sufficient funding.'
    },
    300: {
        'word': 'Contravene',
        'english_meaning': 'to violate or go against a rule or law',
        'urdu_meaning': 'خلاف ورزی کرنا',
        'primary_meaning': 'violate',
        'secondary_meaning': 'breach',
        'tertiary_meaning': 'transgress',
        'sentence': 'His actions appeared to contravene the terms of the agreement.'
    },
    301: {
        'word': 'Contretemps',
        'english_meaning': 'an unexpected and unfortunate event',
        'urdu_meaning': 'ناگہانی بری گھٹنا',
        'primary_meaning': 'mishap',
        'secondary_meaning': 'mishandling',
        'tertiary_meaning': 'misfortune',
        'sentence': 'The meeting was going well until a contretemps disrupted the proceedings.'
    },
    302: {
        'word': 'Contrite',
        'english_meaning': 'feeling remorseful and repentant',
        'urdu_meaning': 'پچھیدہ ہوا، نادم',
        'primary_meaning': 'remorseful',
        'secondary_meaning': 'repentant',
        'tertiary_meaning': 'penitent',
        'sentence': 'He was contrite for his mistakes and sought forgiveness.'
    },
    303: {
        'word': 'Conundrum',
        'english_meaning': 'a confusing and difficult problem or question',
        'urdu_meaning': 'پہیلی، مشکل مسئلہ',
        'primary_meaning': 'puzzle',
        'secondary_meaning': 'riddle',
        'tertiary_meaning': 'enigma',
        'sentence': 'Solving the conundrum required careful analysis and critical thinking.'
    },
    304: {
        'word': 'Convalescent',
        'english_meaning': 'recovering health and strength after illness',
        'urdu_meaning': 'صحت یاب، صحتیاب',
        'primary_meaning': 'recovering',
        'secondary_meaning': 'recuperating',
        'tertiary_meaning': 'healing',
        'sentence': 'The patient was declared convalescent after weeks of treatment.'
    },
    305: {
        'word': 'Conventional',
        'english_meaning': 'based on or in accordance with general agreement, use, or practice',
        'urdu_meaning': 'روایتی، معمولی',
        'primary_meaning': 'traditional',
        'secondary_meaning': 'standard',
        'tertiary_meaning': 'typical',
        'sentence': 'She preferred a conventional approach to problem-solving.'
    },
    306: {
        'word': 'Conviction',
        'english_meaning': 'a strong belief or opinion',
        'urdu_meaning': 'عقیدہ، یقین',
        'primary_meaning': 'belief',
        'secondary_meaning': 'opinion',
        'tertiary_meaning': 'certainty',
        'sentence': 'His conviction in the importance of education drove him to establish schools in rural areas.'
    },
    307: {
        'word': 'Convivial',
        'english_meaning': 'friendly, sociable, and jovial',
        'urdu_meaning': 'میل جول، دوستانہ',
        'primary_meaning': 'friendly',
        'secondary_meaning': 'sociable',
        'tertiary_meaning': 'jovial',
        'sentence': 'The atmosphere at the party was convivial, with laughter and good conversation.'
    },
    308: {
        'word': 'Convoluted',
        'english_meaning': 'complicated and difficult to understand',
        'urdu_meaning': 'پیچیدہ، گرداب دار',
        'primary_meaning': 'complicated',
        'secondary_meaning': 'complex',
        'tertiary_meaning': 'intricate',
        'sentence': 'The plot of the novel was so convoluted that some readers struggled to follow it.'
    },
    309: {
        'word': 'Cope',
        'english_meaning': 'to deal effectively with something difficult',
        'urdu_meaning': 'بچ جانا، مقابلہ کرنا',
        'primary_meaning': 'deal with',
        'secondary_meaning': 'manage',
        'tertiary_meaning': 'handle',
        'sentence': 'She found it challenging to cope with the pressure of the new job.'
    },
    310: {
        'word': 'Copious',
        'english_meaning': 'abundant in quantity; yielding a large supply',
        'urdu_meaning': 'بہت سارا، وافر',
        'primary_meaning': 'abundant',
        'secondary_meaning': 'plentiful',
        'tertiary_meaning': 'ample',
        'sentence': 'The garden produced copious amounts of fruits and vegetables.'
    },
    311: {
        "word": "Cordial",
        "english_meaning": "warm and friendly",
        "urdu_meaning": "دوستانہ، میل جول",
        "primary_meaning": "friendly",
        "secondary_meaning": "affable",
        "tertiary_meaning": "amiable",
        "sentence": "She greeted her guests with a cordial welcome."
    },
    312: {
        "word": "Corporeal",
        "english_meaning": "related to the body; tangible or material",
        "urdu_meaning": "جسمانی، مادی",
        "primary_meaning": "bodily",
        "secondary_meaning": "material",
        "tertiary_meaning": "physical",
        "sentence": "The study focused on the corporeal aspects of human existence."
    },
    313: {
        "word": "Correlate",
        "english_meaning": "have a mutual relationship or connection",
        "urdu_meaning": "متعلقہ ہونا، ہم آہنگ ہونا",
        "primary_meaning": "relate",
        "secondary_meaning": "associate",
        "tertiary_meaning": "connect",
        "sentence": "The increase in temperature seemed to correlate with the rise in pollution levels."
    },
    314: {
        "word": "Corroborate",
        "english_meaning": "to confirm or support with evidence",
        "urdu_meaning": "تصدیق کرنا، ثابت کرنا",
        "primary_meaning": "confirm",
        "secondary_meaning": "validate",
        "tertiary_meaning": "substantiate",
        "sentence": "The witness's testimony helped to corroborate the defendant's alibi."
    },
    315: {
        "word": "Cosmopolitan",
        "english_meaning": "familiar with and at ease in many different countries and cultures",
        "urdu_meaning": "جہانی، دنیاوی",
        "primary_meaning": "global",
        "secondary_meaning": "worldly",
        "tertiary_meaning": "international",
        "sentence": "Living in a cosmopolitan city exposed her to diverse perspectives and lifestyles."
    },
    316: {
        "word": "Countenance",
        "english_meaning": "a person's facial expression or support",
        "urdu_meaning": "چہرہ، حمایت",
        "primary_meaning": "facial expression",
        "secondary_meaning": "appearance",
        "tertiary_meaning": "support",
        "sentence": "His countenance showed surprise at the unexpected news."
    },
    317: {
        "word": "Countercultural",
        "english_meaning": "opposing the dominant culture or societal norms",
        "urdu_meaning": "خلاف روایات، معاشرتی معیاروں کے خلاف",
        "primary_meaning": "opposing cultural norms",
        "secondary_meaning": "counter to mainstream culture",
        "tertiary_meaning": "nonconformist",
        "sentence": "The countercultural movement challenged traditional values and norms."
    },
    318: {
        "word": "Counterfeit",
        "english_meaning": "an imitation made with the intent to deceive",
        "urdu_meaning": "جعلی، نقلی",
        "primary_meaning": "fake",
        "secondary_meaning": "forged",
        "tertiary_meaning": "phony",
        "sentence": "The market was flooded with counterfeit designer goods."
    },
    319: {
        "word": "Counterintuitive",
        "english_meaning": "contrary to what one would expect or common sense",
        "urdu_meaning": "خلاف عقل یا توقع",
        "primary_meaning": "contrary to intuition",
        "secondary_meaning": "unexpected",
        "tertiary_meaning": "counter to common sense",
        "sentence": "The solution to the puzzle was counterintuitive but effective."
    },
    320: {
        "word": "Counterproductive",
        "english_meaning": "having the opposite of the desired effect",
        "urdu_meaning": "غیر فعال، مخالف",
        "primary_meaning": "working against the intended goal",
        "secondary_meaning": "harmful",
        "tertiary_meaning": "ineffective",
        "sentence": "Skipping meals can be counterproductive to maintaining a healthy weight."
    },
    321: {
        "word": "Covert",
        "english_meaning": "not openly acknowledged or displayed",
        "urdu_meaning": "پوشیدہ، خفیہ",
        "primary_meaning": "hidden",
        "secondary_meaning": "secret",
        "tertiary_meaning": "concealed",
        "sentence": "The spy operated from a covert location to gather information."
    },
    322: {
        "word": "Covet",
        "english_meaning": "to desire or wish for eagerly",
        "urdu_meaning": "حرص کرنا، چاہنا",
        "primary_meaning": "crave",
        "secondary_meaning": "long for",
        "tertiary_meaning": "covetous",
        "sentence": "She couldn't help but covet her neighbor's beautiful garden."
    },
    323: {
        "word": "Cow",
        "english_meaning": "to intimidate or subdue",
        "urdu_meaning": "ڈرانا، خوف زدہ کرنا",
        "primary_meaning": "intimidate",
        "secondary_meaning": "frighten",
        "tertiary_meaning": "subdue",
        "sentence": "The aggressive behavior of the larger dog seemed to cow the smaller one into submission."
    },
    324: {
        "word": "Coy",
        "english_meaning": "shy or modest, often in a playful or flirtatious manner",
        "urdu_meaning": "شرمیلا، لجانی",
        "primary_meaning": "shy",
        "secondary_meaning": "modest",
        "tertiary_meaning": "reserved",
        "sentence": "She gave him a coy smile before looking away."
    },
    325: {
        "word": "Craft",
        "english_meaning": "skill in making things, especially with the hands",
        "urdu_meaning": "صنعت، ہنر مندی",
        "primary_meaning": "skill",
        "secondary_meaning": "artistry",
        "tertiary_meaning": "craftsmanship",
        "sentence": "The artist demonstrated exceptional craft in sculpting the intricate details."
    },
    326: {
        "word": "Crafty",
        "english_meaning": "clever in a deceitful or cunning way",
        "urdu_meaning": "چالباز، فریبی",
        "primary_meaning": "sly",
        "secondary_meaning": "deceptive",
        "tertiary_meaning": "cunning",
        "sentence": "The crafty fox managed to outwit the hunters and escape."
    },
    327: {
        "word": "Craven",
        "english_meaning": "lacking courage; cowardly",
        "urdu_meaning": "ڈرپوک، بزدل",
        "primary_meaning": "cowardly",
        "secondary_meaning": "timid",
        "tertiary_meaning": "fearful",
        "sentence": "His craven response to the challenge disappointed his teammates."
    },
    328: {
        "word": "Credible",
        "english_meaning": "able to be believed; trustworthy",
        "urdu_meaning": "قابل اعتماد، معتبر",
        "primary_meaning": "trustworthy",
        "secondary_meaning": "believable",
        "tertiary_meaning": "reliable",
        "sentence": "The witness provided a credible account of the incident."
    },
    329: {
        "word": "Crescendo",
        "english_meaning": "a gradual increase in intensity or loudness",
        "urdu_meaning": "اضافہ، بڑھتے ہوئے",
        "primary_meaning": "increase",
        "secondary_meaning": "build-up",
        "tertiary_meaning": "climax",
        "sentence": "The music reached a crescendo, filling the concert hall with powerful sound."
    },
    330: {
        "word": "Crestfallen",
        "english_meaning": "disappointed and disheartened",
        "urdu_meaning": "مایوس اور دل شکستہ",
        "primary_meaning": "disappointed",
        "secondary_meaning": "downcast",
        "tertiary_meaning": "dejected",
        "sentence": "His crestfallen expression revealed the impact of the unexpected news."
    },
    331: {
        "word": "Croon",
        "english_meaning": "to sing or hum in a soft, soothing voice",
        "urdu_meaning": "میٹھی آواز میں گانا",
        "primary_meaning": "sing softly",
        "secondary_meaning": "hum",
        "tertiary_meaning": "serenade",
        "sentence": "The singer decided to croon a lullaby to the baby."
    },
    332: {
        "word": "Crumble",
        "english_meaning": "to break or fall apart into small pieces",
        "urdu_meaning": "ٹہوڑے ٹہوڑے ہوجانا",
        "primary_meaning": "break apart",
        "secondary_meaning": "fall to pieces",
        "tertiary_meaning": "disintegrate",
        "sentence": "The old building began to crumble due to years of neglect."
    },
    333: {
        "word": "Culprit",
        "english_meaning": "a person responsible for a crime or wrongdoing",
        "urdu_meaning": "ملزم، مجرم",
        "primary_meaning": "wrongdoer",
        "secondary_meaning": "offender",
        "tertiary_meaning": "perpetrator",
        "sentence": "The police arrested the culprit behind the theft."
    },
    334: {
        "word": "Cumbersome",
        "english_meaning": "awkward or difficult to handle due to size or complexity",
        "urdu_meaning": "کڑا، بھاری",
        "primary_meaning": "awkward",
        "secondary_meaning": "bulky",
        "tertiary_meaning": "unwieldy",
        "sentence": "The cumbersome machinery made the task more challenging."
    },
    335: {
        "word": "Cunning",
        "english_meaning": "cleverness or skill, especially in deception",
        "urdu_meaning": "چالبازی، فریب",
        "primary_meaning": "cleverness",
        "secondary_meaning": "deception",
        "tertiary_meaning": "craftiness",
        "sentence": "The cunning fox devised a plan to outsmart the other animals."
    },
    336: {
        "word": "Cupid",
        "english_meaning": "the god of love in Roman mythology; often depicted as a winged cherub",
        "urdu_meaning": "کپید، عشق کا دیوتا",
        "primary_meaning": "god of love",
        "secondary_meaning": "cherubic figure",
        "tertiary_meaning": "symbol of love",
        "sentence": "Cupid is often associated with arrows that cause people to fall in love."
    },
    337: {
        "word": "Curb",
        "english_meaning": "to restrain or control; a check or restraint on something",
        "urdu_meaning": "روکنا یا ناکہٹ کرنا، کنٹرول",
        "primary_meaning": "restrain",
        "secondary_meaning": "control",
        "tertiary_meaning": "check",
        "sentence": "Efforts were made to curb the spread of misinformation."
    },
    338: {
        "word": "Curmudgeon",
        "english_meaning": "a bad-tempered, difficult, or cantankerous person",
        "urdu_meaning": "زہریلا، کڑوا",
        "primary_meaning": "grumpy",
        "secondary_meaning": "irritable",
        "tertiary_meaning": "crabby",
        "sentence": "The old man was known in the neighborhood as a curmudgeon who rarely smiled."
    },
    339: {
        "word": "Cursory",
        "english_meaning": "hasty and without attention to detail; superficial",
        "urdu_meaning": "سرسری، جلد بازی سے",
        "primary_meaning": "superficial",
        "secondary_meaning": "brief",
        "tertiary_meaning": "hasty",
        "sentence": "A cursory glance at the report revealed only the most basic information."
    },
    340: {
        "word": "Curtail",
        "english_meaning": "to reduce or cut short; to impose restrictions",
        "urdu_meaning": "کم کرنا، محدود کرنا",
        "primary_meaning": "reduce",
        "secondary_meaning": "limit",
        "tertiary_meaning": "restrict",
        "sentence": "The company had to curtail its expenses during the economic downturn."
    },
    341: {
        "word": "Cynical",
        "english_meaning": "doubtful or distrustful of human motives; skeptical",
        "urdu_meaning": "سنگین، شکایتی",
        "primary_meaning": "distrustful",
        "secondary_meaning": "skeptical",
        "tertiary_meaning": "disbelieving",
        "sentence": "After years of disappointments, he became cynical about people's intentions."
    },
    342: {
        "word": "Daunt",
        "english_meaning": "to intimidate or make fearful",
        "urdu_meaning": "ہمت شکنی ہونا، خوفناک بنانا",
        "primary_meaning": "intimidate",
        "secondary_meaning": "discourage",
        "tertiary_meaning": "dismay",
        "sentence": "The challenging task did not daunt her; she approached it with determination."
    },
    343: {
        "word": "Daunting",
        "english_meaning": "seeming difficult to deal with in anticipation; intimidating",
        "urdu_meaning": "ہمت شکن، خوفناک",
        "primary_meaning": "intimidating",
        "secondary_meaning": "challenging",
        "tertiary_meaning": "formidable",
        "sentence": "The daunting prospect of climbing the mountain made them hesitate."
    },
    344: {
        "word": "Dawdle",
        "english_meaning": "to waste time or move slowly",
        "urdu_meaning": "سست چلنا یا وقت ضائع کرنا",
        "primary_meaning": "move slowly",
        "secondary_meaning": "loiter",
        "tertiary_meaning": "procrastinate",
        "sentence": "We can't afford to dawdle; we need to finish the project on time."
    },
    345: {
        "word": "Dearth",
        "english_meaning": "a scarcity or lack of something",
        "urdu_meaning": "کمی، قلت",
        "primary_meaning": "scarcity",
        "secondary_meaning": "shortage",
        "tertiary_meaning": "absence",
        "sentence": "The drought resulted in a dearth of water for the crops."
    },
    346: {
        "word": "Debacle",
        "english_meaning": "a sudden and ignominious failure; a fiasco",
        "urdu_meaning": "شگاف",
        "primary_meaning": "collapse",
        "secondary_meaning": "disaster",
        "tertiary_meaning": "catastrophe",
        "sentence": "The project ended in a debacle due to poor planning."
    },
    347: {
        "word": "Debase",
        "english_meaning": "reduce (something) in quality or value; degrade",
        "urdu_meaning": "کمیابی کم کرنا",
        "primary_meaning": "degrade",
        "secondary_meaning": "corrupt",
        "tertiary_meaning": "demean",
        "sentence": "The scandal threatened to debase the reputation of the company."
    },
    348: {
        "word": "Debilitating",
        "english_meaning": "making someone or something very weak and infirm",
        "urdu_meaning": "کمزور کن",
        "primary_meaning": "weakening",
        "secondary_meaning": "exhausting",
        "tertiary_meaning": "enervating",
        "sentence": "The illness had a debilitating effect on his strength and energy."
    },
    349: {
        "word": "Debunk",
        "english_meaning": "expose the falseness or hollowness of (a myth, idea, or belief)",
        "urdu_meaning": "مکمل طور پر پھیلانا",
        "primary_meaning": "disprove",
        "secondary_meaning": "refute",
        "tertiary_meaning": "discredit",
        "sentence": "The scientist aimed to debunk the popular misconceptions about the theory."
    },
    350: {
        "word": "Decadent",
        "english_meaning": "characterized by or reflecting a state of moral or cultural decline",
        "urdu_meaning": "اخلاقی زوال",
        "primary_meaning": "decaying",
        "secondary_meaning": "degenerate",
        "tertiary_meaning": "dissolute",
        "sentence": "The society was criticized for its decadent values and excesses."
    },
    351: {
        "word": "Deceit",
        "english_meaning": "the action or practice of deceiving someone by concealing or misrepresenting the truth",
        "urdu_meaning": "دھوکہ",
        "primary_meaning": "deception",
        "secondary_meaning": "fraud",
        "tertiary_meaning": "trickery",
        "sentence": "His deceit was uncovered when the truth came to light."
    },
    352: {
        "word": "Deceptive",
        "english_meaning": "giving an appearance or impression different from the true one; misleading",
        "urdu_meaning": "غیر مستقیم",
        "primary_meaning": "misleading",
        "secondary_meaning": "illusory",
        "tertiary_meaning": "deceitful",
        "sentence": "The desert's deceptive mirages fooled the travelers."
    },
    353: {
        "word": "Decipher",
        "english_meaning": "convert (a text written in code, or a coded signal) into normal language",
        "urdu_meaning": "سمجھنا",
        "primary_meaning": "interpret",
        "secondary_meaning": "decode",
        "tertiary_meaning": "unravel",
        "sentence": "The cryptographer worked hard to decipher the encrypted message."
    },
    354: {
        "word": "Decorum",
        "english_meaning": "behavior in keeping with good taste and propriety",
        "urdu_meaning": "لائق چلن",
        "primary_meaning": "etiquette",
        "secondary_meaning": "propriety",
        "tertiary_meaning": "decorum",
        "sentence": "The event was conducted with great decorum and respect."
    },
    355: {
        "word": "Decry",
        "english_meaning": "publicly denounce",
        "urdu_meaning": "مذمت کرنا",
        "primary_meaning": "condemn",
        "secondary_meaning": "denounce",
        "tertiary_meaning": "criticize",
        "sentence": "The activists gathered to decry the government's actions."
    },
    356: {
        "word": "Defamatory",
        "english_meaning": "damaging the good reputation of someone; slanderous or libelous",
        "urdu_meaning": "زہر انگیز",
        "primary_meaning": "slanderous",
        "secondary_meaning": "libelous",
        "tertiary_meaning": "malicious",
        "sentence": "The false and defamatory statements led to a legal battle."
    },
    357: {
        "word": "Deference",
        "english_meaning": "humble submission and respect",
        "urdu_meaning": "اطاعت",
        "primary_meaning": "respect",
        "secondary_meaning": "submission",
        "tertiary_meaning": "deference",
        "sentence": "He showed deference to his elders by listening attentively."
    },
    358: {
        "word": "Deferential",
        "english_meaning": "showing deference; respectful",
        "urdu_meaning": "اعتراف کرتے ہوئے",
        "primary_meaning": "respectful",
        "secondary_meaning": "courteous",
        "tertiary_meaning": "obliging",
        "sentence": "The employee was deferential to his supervisor during the meeting."
    },
    359: {
        "word": "Deflect",
        "english_meaning": "cause (something) to change direction; turn aside from a straight course",
        "urdu_meaning": "منحرف ہونا",
        "primary_meaning": "divert",
        "secondary_meaning": "deviate",
        "tertiary_meaning": "avert",
        "sentence": "The shield helped deflect the incoming arrows."
    },
    360: {
        "word": "Deft",
        "english_meaning": "neatly skillful and quick in one's movements",
        "urdu_meaning": "ہوشیار",
        "primary_meaning": "skillful",
        "secondary_meaning": "nimble",
        "tertiary_meaning": "dexterous",
        "sentence": "The chef's deft hands"
    },
    361: {
        "word": "Defy",
        "english_meaning": "openly resist or refuse to obey",
        "urdu_meaning": "مخالفت کرنا",
        "primary_meaning": "challenge",
        "secondary_meaning": "oppose",
        "tertiary_meaning": "rebel",
        "sentence": "She chose to defy the unjust law and fight for her rights."
    },
    362: {
        "word": "Deify",
        "english_meaning": "treat someone or something as a god",
        "urdu_meaning": "خدا ٹھہرانا",
        "primary_meaning": "worship",
        "secondary_meaning": "idolize",
        "tertiary_meaning": "venerate",
        "sentence": "In some cultures, historical leaders were deified after their death."
    },
    363: {
        "word": "Deleterious",
        "english_meaning": "causing harm or damage",
        "urdu_meaning": "مضر",
        "primary_meaning": "harmful",
        "secondary_meaning": "detrimental",
        "tertiary_meaning": "injurious",
        "sentence": "The pollution had a deleterious impact on the health of the community."
    },
    364: {
        "word": "Deliberate",
        "english_meaning": "done consciously and intentionally",
        "urdu_meaning": "عمدی",
        "primary_meaning": "intentional",
        "secondary_meaning": "purposeful",
        "tertiary_meaning": "premeditated",
        "sentence": "The jury believed that the act was a deliberate attempt to deceive."
    },
    365: {
        "word": "Delicacy",
        "english_meaning": "the quality of being delicate, exquisite, or fine",
        "urdu_meaning": "نازکی",
        "primary_meaning": "fragility",
        "secondary_meaning": "elegance",
        "tertiary_meaning": "refinement",
        "sentence": "The artist captured the delicacy of the flower in his painting."
    },
    366: {
        "word": "Delineate",
        "english_meaning": "describe or portray (something) precisely",
        "urdu_meaning": "واضح کرنا",
        "primary_meaning": "depict",
        "secondary_meaning": "outline",
        "tertiary_meaning": "define",
        "sentence": "The map delineates the boundaries of the national park."
    },
    367: {
        "word": "Delusion",
        "english_meaning": "a belief or impression that is firmly maintained despite being contradicted by what is generally accepted as reality",
        "urdu_meaning": "وہم",
        "primary_meaning": "illusion",
        "secondary_meaning": "misconception",
        "tertiary_meaning": "fantasy",
        "sentence": "His delusion led him to believe in imaginary conspiracies."
    },
    368: {
        "word": "Demanding",
        "english_meaning": "requiring a lot of effort and skill",
        "urdu_meaning": "مشکل",
        "primary_meaning": "challenging",
        "secondary_meaning": "exacting",
        "tertiary_meaning": "rigorous",
        "sentence": "The demanding task tested the team's abilities to the fullest."
    },
    369: {
        "word": "Demur",
        "english_meaning": "raise doubts or objections or show reluctance",
        "urdu_meaning": "اعتراض کرنا",
        "primary_meaning": "object",
        "secondary_meaning": "protest",
        "tertiary_meaning": "hesitate",
        "sentence": "She didn't demur when asked to take on the leadership role."
    },
    370: {
        "word": "Demystify",
        "english_meaning": "make (a difficult subject) clearer and easier to understand",
        "urdu_meaning": "راز کھولنا",
        "primary_meaning": "clarify",
        "secondary_meaning": "unravel",
        "tertiary_meaning": "explain",
        "sentence": "The professor tried to demystify complex scientific concepts for the students."
    },
    371: {
        "word": "Denigrate",
        "english_meaning": "criticize unfairly; disparage",
        "urdu_meaning": "تحقیر کرنا",
        "primary_meaning": "disparage",
        "secondary_meaning": "belittle",
        "tertiary_meaning": "defame",
        "sentence": "It is not appropriate to denigrate someone based on unfounded rumors."
    },
    372: {
        "word": "Denounce",
        "english_meaning": "publicly declare to be wrong or evil; condemn",
        "urdu_meaning": "الزام دینا",
        "primary_meaning": "condemn",
        "secondary_meaning": "censure",
        "tertiary_meaning": "criticize",
        "sentence": "The leader used the press conference to denounce the act of violence."
    },
    373: {
        "word": "Deportment",
        "english_meaning": "a person's behavior or manners",
        "urdu_meaning": "چال چلن",
        "primary_meaning": "conduct",
        "secondary_meaning": "demeanor",
        "tertiary_meaning": "behavior",
        "sentence": "Her deportment at the formal event was elegant and composed."
    },
    374: {
        "word": "Depose",
        "english_meaning": "remove from office suddenly and forcefully",
        "urdu_meaning": "عہد سے ہٹانا",
        "primary_meaning": "overthrow",
        "secondary_meaning": "dismiss",
        "tertiary_meaning": "dethrone",
        "sentence": "The revolution aimed to depose the oppressive regime."
    },
    375: {
        "word": "Depravity",
        "english_meaning": "moral corruption; wickedness",
        "urdu_meaning": "فسق",
        "primary_meaning": "corruption",
        "secondary_meaning": "immorality",
        "tertiary_meaning": "depravity",
        "sentence": "The novel depicted the depravity of the villain's actions."
    },
    376: {
        "word": "Deprecate",
        "english_meaning": "express disapproval of; criticize",
        "urdu_meaning": "مذمت کرنا",
        "primary_meaning": "disapprove",
        "secondary_meaning": "condemn",
        "tertiary_meaning": "protest",
        "sentence": "He would deprecate any form of discrimination in the workplace."
    },
    377: {
        "word": "Deride",
        "english_meaning": "express contemptuous ridicule; mock",
        "urdu_meaning": "طعنہ کھانا",
        "primary_meaning": "mock",
        "secondary_meaning": "ridicule",
        "tertiary_meaning": "taunt",
        "sentence": "Her classmates would often deride her for her unique fashion sense."
    },
    378: {
        "word": "Derivative",
        "english_meaning": "imitative of the work of another person, and usually disapproved of for that reason",
        "urdu_meaning": "اشتقاقی",
        "primary_meaning": "unoriginal",
        "secondary_meaning": "imitative",
        "tertiary_meaning": "derived",
        "sentence": "The artist's work was criticized as being too derivative of famous painters."
    },
    379: {
        "word": "Desiccate",
        "english_meaning": "remove the moisture from (something), typically in order to preserve it",
        "urdu_meaning": "خشک کرنا",
        "primary_meaning": "dry",
        "secondary_meaning": "dehydrate",
        "tertiary_meaning": "parch",
        "sentence": "Fruits are often desiccated to extend their shelf life."
    },
    380: {
        "word": "Despair",
        "english_meaning": "the complete loss or absence of hope",
        "urdu_meaning": "مایوسی",
        "primary_meaning": "hopelessness",
        "secondary_meaning": "despondency",
        "tertiary_meaning": "melancholy",
        "sentence": "In moments of despair, it's important to seek support from others."
    },
    381: {
        "word": "Despotic",
        "english_meaning": "of or typical of a despot; tyrannical",
        "urdu_meaning": "ظالمانہ",
        "primary_meaning": "tyrannical",
        "secondary_meaning": "authoritarian",
        "tertiary_meaning": "oppressive",
        "sentence": "The citizens rebelled against the despotic rule of the dictator."
    },
    382: {
        "word": "Desultory",
        "english_meaning": "lacking a plan, purpose, or enthusiasm",
        "urdu_meaning": "بے ترتیب",
        "primary_meaning": "random",
        "secondary_meaning": "aimless",
        "tertiary_meaning": "haphazard",
        "sentence": "The meeting was marked by desultory discussions with no clear agenda."
    },
    383: {
        "word": "Detached",
        "english_meaning": "separated; disconnected",
        "urdu_meaning": "منفصل",
        "primary_meaning": "disconnected",
        "secondary_meaning": "unattached",
        "tertiary_meaning": "isolated",
        "sentence": "He remained emotionally detached from the issues at hand."
    },
    384: {
        "word": "Detente",
        "english_meaning": "the easing of hostility or strained relations, especially between countries",
        "urdu_meaning": "رفاقت",
        "primary_meaning": "reconciliation",
        "secondary_meaning": "thawing",
        "tertiary_meaning": "rapprochement",
        "sentence": "The summit aimed to achieve detente between the neighboring nations."
    },
    385: {
        "word": "Deter",
        "english_meaning": "discourage (someone) from doing something",
        "urdu_meaning": "رکاوٹ ڈالنا",
        "primary_meaning": "discourage",
        "secondary_meaning": "dissuade",
        "tertiary_meaning": "prevent",
        "sentence": "The warning signs are meant to deter people from trespassing."
    },
    386: {
        "word": "Detractor",
        "english_meaning": "a person who disparages someone or something",
        "urdu_meaning": "تنقیدی",
        "primary_meaning": "critic",
        "secondary_meaning": "detractor",
        "tertiary_meaning": "opponent",
        "sentence": "Despite the detractors, the artist's work gained widespread acclaim."
    },
    387: {
        "word": "Detrimental",
        "english_meaning": "tending to cause harm",
        "urdu_meaning": "مضر",
        "primary_meaning": "harmful",
        "secondary_meaning": "damaging",
        "tertiary_meaning": "injurious",
        "sentence": "Lack of exercise can be detrimental to one's health."
    },
    388: {
        "word": "Deviate",
        "english_meaning": "depart from an established course",
        "urdu_meaning": "ہٹنا",
        "primary_meaning": "stray",
        "secondary_meaning": "diverge",
        "tertiary_meaning": "deviate",
        "sentence": "The project began to deviate from its original plan due to unforeseen challenges."
    },
    389: {
        "word": "Devious",
        "english_meaning": "showing a skillful use of underhanded tactics to achieve goals",
        "urdu_meaning": "چالباز",
        "primary_meaning": "cunning",
        "secondary_meaning": "sly",
        "tertiary_meaning": "crafty",
        "sentence": "The detective admired the devious strategy used by the mastermind criminal."
    },
    390: {
        "word": "Devolve",
        "english_meaning": "transfer or delegate (power) to a lower level, especially from central government to local or regional administration",
        "urdu_meaning": "منتقل کرنا",
        "primary_meaning": "delegate",
        "secondary_meaning": "transfer",
        "tertiary_meaning": "entrust",
        "sentence": "The decision was made to devolve certain responsibilities to regional authorities."
    },
    391: {
        "word": "Dexter",
        "english_meaning": "skillful in the use of the hands",
        "urdu_meaning": "ہوشیار",
        "primary_meaning": "skillful",
        "secondary_meaning": "adept",
        "tertiary_meaning": "dextrous",
        "sentence": "The dexter carpenter crafted intricate designs with precision."
    },
    392: {
        "word": "Diatribe",
        "english_meaning": "a forceful and bitter verbal attack against someone or something",
        "urdu_meaning": "تنقید",
        "primary_meaning": "tirade",
        "secondary_meaning": "harangue",
        "tertiary_meaning": "rant",
        "sentence": "His speech turned into a diatribe against the policies of the government."
    },
    393: {
        "word": "Dichotomy",
        "english_meaning": "a division or contrast between two things that are or are represented as being opposed or entirely different",
        "urdu_meaning": "تقسیم",
        "primary_meaning": "division",
        "secondary_meaning": "contrast",
        "tertiary_meaning": "duality",
        "sentence": "The philosophical debate explored the dichotomy between reason and emotion."
    },
    394: {
        "word": "Dictate",
        "english_meaning": "command or order (something) authoritatively",
        "urdu_meaning": "حکم دینا",
        "primary_meaning": "command",
        "secondary_meaning": "direct",
        "tertiary_meaning": "prescribe",
        "sentence": "The leader will dictate the terms of the negotiation."
    },
    395: {
        "word": "Dictum",
        "english_meaning": "a formal pronouncement from an authoritative source",
        "urdu_meaning": "حکم",
        "primary_meaning": "pronouncement",
        "secondary_meaning": "declaration",
        "tertiary_meaning": "decree",
        "sentence": "The judge cited a legal dictum to support his ruling."
    },
    396: {
        "word": "Didactic",
        "english_meaning": "intended to teach, particularly in having moral instruction as an ulterior motive",
        "urdu_meaning": "تعلیمی",
        "primary_meaning": "instructive",
        "secondary_meaning": "educational",
        "tertiary_meaning": "moralistic",
        "sentence": "The fable had a didactic purpose, teaching children a valuable life lesson."
    },
    397: {
        "word": "Diffident",
        "english_meaning": "modest or shy because of a lack of self-confidence",
        "urdu_meaning": "شرمیلا",
        "primary_meaning": "shy",
        "secondary_meaning": "reserved",
        "tertiary_meaning": "timid",
        "sentence": "The diffident student hesitated to speak in front of the class."
    },
    398: {
        "word": "Diffuse",
        "english_meaning": "spread out over a large area; not concentrated",
        "urdu_meaning": "پھیلانا",
        "primary_meaning": "disperse",
        "secondary_meaning": "scatter",
        "tertiary_meaning": "distribute",
        "sentence": "The sunlight was diffuse, casting a soft glow across the landscape."
    },
    399: {
        "word": "Digression",
        "english_meaning": "a temporary departure from the main subject in speech or writing",
        "urdu_meaning": "موضوع سے ہٹ کر بات چیتنا",
        "primary_meaning": "diversion",
        "secondary_meaning": "deviation",
        "tertiary_meaning": "tangent",
        "sentence": "The professor's digression provided interesting insights but deviated from the main lecture."
    },
    400: {
        "word": "Dilate",
        "english_meaning": "make or become wider, larger, or more open",
        "urdu_meaning": "پھیلانا",
        "primary_meaning": "expand",
        "secondary_meaning": "enlarge",
        "tertiary_meaning": "widen",
        "sentence": "The doctor used eye drops to dilate the pupil for a thorough examination."
    },
    401: {
        "word": "Dilatory",
        "english_meaning": "slow to act; intended to cause delay",
        "urdu_meaning": "تاخیر آور",
        "primary_meaning": "delaying",
        "secondary_meaning": "procrastinating",
        "tertiary_meaning": "tardy",
        "sentence": "His dilatory response to the urgent situation led to further complications."
    },
    402: {
        "word": "Dilemma",
        "english_meaning": "a difficult choice between two undesirable alternatives",
        "urdu_meaning": "دو چھکر",
        "primary_meaning": "predicament",
        "secondary_meaning": "quandary",
        "tertiary_meaning": "conundrum",
        "sentence": "Facing a dilemma, she had to choose between her career and family."
    },
    403: {
        "word": "Dilettante",
        "english_meaning": "a person who cultivates an area of interest without real commitment or knowledge",
        "urdu_meaning": "شوقین",
        "primary_meaning": "amateur",
        "secondary_meaning": "dabbler",
        "tertiary_meaning": "novice",
        "sentence": "He was considered a dilettante in art, trying various forms without mastering any."
    },
    404: {
        "word": "Diminutive",
        "english_meaning": "extremely or unusually small",
        "urdu_meaning": "چھوٹا",
        "primary_meaning": "tiny",
        "secondary_meaning": "small",
        "tertiary_meaning": "miniature",
        "sentence": "The diminutive size of the toy made it suitable for young children."
    },
    405: {
        "word": "Dirge",
        "english_meaning": "a lament for the dead, especially one forming part of a funeral rite",
        "urdu_meaning": "ماتمی نغمہ",
        "primary_meaning": "funeral song",
        "secondary_meaning": "mournful tune",
        "tertiary_meaning": "elegy",
        "sentence": "The somber dirge echoed through the funeral procession."
    },
    406: {
        "word": "Disaffection",
        "english_meaning": "a state or feeling of being dissatisfied or alienated",
        "urdu_meaning": "ناخوشگواری",
        "primary_meaning": "dissatisfaction",
        "secondary_meaning": "alienation",
        "tertiary_meaning": "discontent",
        "sentence": "The disaffection among the employees led to a decline in morale."
    },
    407: {
        "word": "Disapprobation",
        "english_meaning": "strong disapproval, typically on moral grounds",
        "urdu_meaning": "نفرت",
        "primary_meaning": "condemnation",
        "secondary_meaning": "disapproval",
        "tertiary_meaning": "censure",
        "sentence": "The decision met with widespread disapprobation from the community."
    },
    408: {
        "word": "Discern",
        "english_meaning": "perceive or recognize (something)",
        "urdu_meaning": "پہچاننا",
        "primary_meaning": "perceive",
        "secondary_meaning": "detect",
        "tertiary_meaning": "identify",
        "sentence": "It was difficult to discern the truth amidst the conflicting accounts."
    },
    409: {
        "word": "Discernible",
        "english_meaning": "able to be perceived or recognized",
        "urdu_meaning": "قابل پہچان",
        "primary_meaning": "perceptible",
        "secondary_meaning": "observable",
        "tertiary_meaning": "apparent",
        "sentence": "There was a discernible change in the atmosphere after the announcement."
    },
    410: {
        "word": "Disciple",
        "english_meaning": "a follower or student of a teacher, leader, or philosophy",
        "urdu_meaning": "شاگرد",
        "primary_meaning": "follower",
        "secondary_meaning": "adherent",
        "tertiary_meaning": "devotee",
        "sentence": "The spiritual leader had many disciples who followed his teachings."
    },
    411: {
        "word": "Discomfit",
        "english_meaning": "make (someone) feel uneasy or embarrassed",
        "urdu_meaning": "شرمندہ کرنا",
        "primary_meaning": "unsettle",
        "secondary_meaning": "disconcert",
        "tertiary_meaning": "bewilder",
        "sentence": "His unexpected question seemed to discomfit the speaker."
    },
    412: {
        "word": "Disconcert",
        "english_meaning": "disturb the composure of; unsettle",
        "urdu_meaning": "پریشان کرنا",
        "primary_meaning": "unsettle",
        "secondary_meaning": "discompose",
        "tertiary_meaning": "confuse",
        "sentence": "The sudden change in plans seemed to disconcert everyone in the group."
    },
    413: {
        "word": "Discord",
        "english_meaning": "lack of harmony between notes sounding together",
        "urdu_meaning": "ناہمواری",
        "primary_meaning": "disharmony",
        "secondary_meaning": "dissonance",
        "tertiary_meaning": "cacophony",
        "sentence": "The musicians worked to resolve the discord in the composition."
    },
    414: {
        "word": "Discount",
        "english_meaning": "deduct an amount from the usual price",
        "urdu_meaning": "چھوٹ",
        "primary_meaning": "reduce",
        "secondary_meaning": "deduct",
        "tertiary_meaning": "lower",
        "sentence": "The store offered a discount on the new collection for a limited time."
    },
    415: {
        "word": "Discredit",
        "english_meaning": "harm the good reputation of (someone or something)",
        "urdu_meaning": "ناقابل اعتماد بنانا",
        "primary_meaning": "disgrace",
        "secondary_meaning": "defame",
        "tertiary_meaning": "dishonor",
        "sentence": "Baseless accusations were made to discredit the political candidate."
    },
    416: {
        "word": "Discreet",
        "english_meaning": "careful and prudent in one's speech or actions",
        "urdu_meaning": "ہوشیار",
        "primary_meaning": "cautious",
        "secondary_meaning": "circumspect",
        "tertiary_meaning": "diplomatic",
        "sentence": "It's important to be discreet when discussing sensitive matters."
    },
    417: {
        "word": "Discrepancy",
        "english_meaning": "a lack of compatibility or similarity between two or more facts",
        "urdu_meaning": "اختلاف",
        "primary_meaning": "disagreement",
        "secondary_meaning": "disparity",
        "tertiary_meaning": "discrepance",
        "sentence": "The auditor discovered a discrepancy in the financial records."
    },
    418: {
        "word": "Disdain",
        "english_meaning": "the feeling that someone or something is unworthy of one's consideration or respect",
        "urdu_meaning": "تحقیر",
        "primary_meaning": "contempt",
        "secondary_meaning": "scorn",
        "tertiary_meaning": "disregard",
        "sentence": "His actions were met with disdain by those who expected better behavior."
    },
    419: {
        "word": "Disenchant",
        "english_meaning": "free (someone) from illusion or false belief",
        "urdu_meaning": "گمراہی دور کرنا",
        "primary_meaning": "disillusion",
        "secondary_meaning": "disabuse",
        "tertiary_meaning": "undeceive",
        "sentence": "The harsh reality of the situation served to disenchant the idealistic vision."
    },
    420: {
        "word": "Disentangle",
        "english_meaning": "free (something or someone) from an entanglement; unravel",
        "urdu_meaning": "پھیکنا",
        "primary_meaning": "untangle",
        "secondary_meaning": "unravel",
        "tertiary_meaning": "unwrap",
        "sentence": "It took hours to disentangle the fishing net caught in the propeller."
    },
    421: {
        "word": "Disgorge",
        "english_meaning": "cause to pour out",
        "urdu_meaning": "نکالنا",
        "primary_meaning": "spew",
        "secondary_meaning": "eject",
        "tertiary_meaning": "expel",
        "sentence": "The volcano began to disgorge ash and lava, posing a threat to the nearby villages."
    },
    422: {
        "word": "Disgruntle",
        "english_meaning": "make (someone) discontented or irritable",
        "urdu_meaning": "ناراض",
        "primary_meaning": "discontent",
        "secondary_meaning": "displeased",
        "tertiary_meaning": "dissatisfied",
        "sentence": "The repeated delays in the project began to disgruntle the team members."
    },
    423: {
        "word": "Disingenuous",
        "english_meaning": "not candid or sincere, typically by pretending that one knows less about something than one really does",
        "urdu_meaning": "کھلم کھلا",
        "primary_meaning": "insincere",
        "secondary_meaning": "deceptive",
        "tertiary_meaning": "duplicious",
        "sentence": "His disingenuous apology did little to repair the damaged trust."
    },
    424: {
        "word": "Disintegrate",
        "english_meaning": "break up into small parts, typically as the result of impact or decay",
        "urdu_meaning": "تشکیل سے حاصل ہونے والے حصے ہو جانا",
        "primary_meaning": "break apart",
        "secondary_meaning": "dissolve",
        "tertiary_meaning": "fragment",
        "sentence": "Over time, the ancient structure began to disintegrate due to weathering."
    },
    425: {
        "word": "Disinterested",
        "english_meaning": "not influenced by considerations of personal advantage; impartial",
        "urdu_meaning": "بے طرف",
        "primary_meaning": "impartial",
        "secondary_meaning": "unbiased",
        "tertiary_meaning": "neutral",
        "sentence": "As a judge, she remained disinterested and focused on the facts of the case."
    },
    426: {
        "word": "Disjunction",
        "english_meaning": "a separation or disconnection",
        "urdu_meaning": "اختلاف",
        "primary_meaning": "separation",
        "secondary_meaning": "disconnection",
        "tertiary_meaning": "disunion",
        "sentence": "The disjunction between the two political parties led to a lack of cooperation."
    },
    427: {
        "word": "Dislocation",
        "english_meaning": "the action of moving something from its usual place or position",
        "urdu_meaning": "انحراف",
        "primary_meaning": "movement",
        "secondary_meaning": "shift",
        "tertiary_meaning": "relocation",
        "sentence": "The earthquake caused the dislocation of several buildings from their foundations."
    },
    428: {
        "word": "Dismantle",
        "english_meaning": "take (a machine or structure) to pieces",
        "urdu_meaning": "ڈسمیٹل کرنا",
        "primary_meaning": "disassemble",
        "secondary_meaning": "take apart",
        "tertiary_meaning": "deconstruct",
        "sentence": "The old factory was scheduled for demolition, and workers began to dismantle the machinery."
    },
    429: {
        "word": "Disorient",
        "english_meaning": "cause (someone) to lose their sense of direction",
        "urdu_meaning": "سمت بھٹکانا",
        "primary_meaning": "confuse",
        "secondary_meaning": "bewilder",
        "tertiary_meaning": "disconcert",
        "sentence": "The sudden change in the environment could disorient even the most experienced hiker."
    },
    430: {
        "word": "Disparate",
        "english_meaning": "essentially different in kind; not allowing comparison",
        "urdu_meaning": "مختلف",
        "primary_meaning": "distinct",
        "secondary_meaning": "unrelated",
        "tertiary_meaning": "divergent",
        "sentence": "The two cultures had disparate beliefs and traditions."
    },
    431: {
        "word": "Dispassionate",
        "english_meaning": "not influenced by strong emotion, and so able to be rational and impartial",
        "urdu_meaning": "بے حس",
        "primary_meaning": "impartial",
        "secondary_meaning": "unbiased",
        "tertiary_meaning": "objective",
        "sentence": "The judge delivered a dispassionate verdict based on the evidence presented."
    },
    432: {
        "word": "Dispense",
        "english_meaning": "distribute or provide (a service or information) to a number of people",
        "urdu_meaning": "تقسیم کرنا",
        "primary_meaning": "distribute",
        "secondary_meaning": "administer",
        "tertiary_meaning": "supply",
        "sentence": "The pharmacist will dispense the prescribed medication."
    },
    433: {
        "word": "Disperse",
        "english_meaning": "distribute or spread over a wide area",
        "urdu_meaning": "پھیلانا",
        "primary_meaning": "scatter",
        "secondary_meaning": "dissipate",
        "tertiary_meaning": "disseminate",
        "sentence": "The crowd began to disperse after the event concluded."
    },
    434: {
        "word": "Disquiet",
        "english_meaning": "a feeling of anxiety or worry",
        "urdu_meaning": "بے چینی",
        "primary_meaning": "anxiety",
        "secondary_meaning": "unease",
        "tertiary_meaning": "disturbance",
        "sentence": "The mysterious sound caused disquiet among the residents."
    },
    435: {
        "word": "Dissemble",
        "english_meaning": "conceal one's true motives, feelings, or beliefs",
        "urdu_meaning": "مکر کرنا",
        "primary_meaning": "pretend",
        "secondary_meaning": "deceive",
        "tertiary_meaning": "dissimulate",
        "sentence": "She tried to dissemble her disappointment with a forced smile."
    },
    436: {
        "word": "Disseminate",
        "english_meaning": "spread or disperse (something, especially information) widely",
        "urdu_meaning": "پھیلانا",
        "primary_meaning": "spread",
        "secondary_meaning": "circulate",
        "tertiary_meaning": "broadcast",
        "sentence": "The organization aims to disseminate knowledge about environmental conservation."
    },
    437: {
        "word": "Dissent",
        "english_meaning": "the expression or holding of opinions at variance with those previously, commonly, or officially held",
        "urdu_meaning": "اختلاف",
        "primary_meaning": "disagreement",
        "secondary_meaning": "protest",
        "tertiary_meaning": "opposition",
        "sentence": "The minority party voiced their dissent on the proposed legislation."
    },
    438: {
        "word": "Dissident",
        "english_meaning": "a person who opposes official policy, especially that of an authoritarian state",
        "urdu_meaning": "مختلف رائے رکھنے والا",
        "primary_meaning": "opponent",
        "secondary_meaning": "rebel",
        "tertiary_meaning": "dissenter",
        "sentence": "The dissident journalist faced persecution for speaking out against the government."
    },
    439: {
        "word": "Dissimilar",
        "english_meaning": "not alike; different",
        "urdu_meaning": "غیر مشابہ",
        "primary_meaning": "distinct",
        "secondary_meaning": "unlike",
        "tertiary_meaning": "divergent",
        "sentence": "The twins, despite being siblings, had dissimilar personalities."
    },
    440: {
        "word": "Dissolution",
        "english_meaning": "the closing down or dismissal of an assembly, partnership, or official body",
        "urdu_meaning": "تحلیل",
        "primary_meaning": "disintegration",
        "secondary_meaning": "dismantling",
        "tertiary_meaning": "termination",
        "sentence": "The dissolution of the company led to the loss of many jobs."
    },
    441: {
        "word": "Distaste",
        "english_meaning": "a feeling of dislike or aversion",
        "urdu_meaning": "ناپسندیدگی",
        "primary_meaning": "dislike",
        "secondary_meaning": "aversion",
        "tertiary_meaning": "repugnance",
        "sentence": "She expressed her distaste for the strong taste of the medicine."
    },
    442: {
        "word": "Distend",
        "english_meaning": "swell or cause to swell by pressure from inside",
        "urdu_meaning": "پھیلنا",
        "primary_meaning": "swell",
        "secondary_meaning": "expand",
        "tertiary_meaning": "inflate",
        "sentence": "The balloon began to distend as it filled with air."
    },
    443: {
        "word": "Distill",
        "english_meaning": "purify (a liquid) by vaporizing it, then condensing it by cooling the vapor, and collecting the resulting liquid",
        "urdu_meaning": "تصفیہ کرنا",
        "primary_meaning": "purify",
        "secondary_meaning": "refine",
        "tertiary_meaning": "extract",
        "sentence": "The distillation process is used to produce pure and concentrated substances."
    },
    444: {
        "word": "Distort",
        "english_meaning": "pull or twist out of shape",
        "urdu_meaning": "توڑنا",
        "primary_meaning": "deform",
        "secondary_meaning": "warp",
        "tertiary_meaning": "misshape",
        "sentence": "The heat caused the plastic to distort and lose its original form."
    },
    445: {
        "word": "Distressed",
        "english_meaning": "suffering from extreme anxiety, sorrow, or pain",
        "urdu_meaning": "پریشان",
        "primary_meaning": "anguished",
        "secondary_meaning": "troubled",
        "tertiary_meaning": "heartbroken",
        "sentence": "The distressed look on her face indicated the depth of her emotional pain."
    },
    446: {
        "word": "Divergent",
        "english_meaning": "tending to be different or develop in different directions",
        "urdu_meaning": "مختلف",
        "primary_meaning": "varying",
        "secondary_meaning": "diverging",
        "tertiary_meaning": "disparate",
        "sentence": "The opinions of the group became increasingly divergent as the discussion progressed."
    },
    447: {
        "word": "Divorced",
        "english_meaning": "separated or disconnected",
        "urdu_meaning": "الگ",
        "primary_meaning": "separated",
        "secondary_meaning": "disconnected",
        "tertiary_meaning": "isolated",
        "sentence": "The artist's style seemed divorced from traditional artistic conventions."
    },
    448: {
        "word": "Divulge",
        "english_meaning": "make known (private or sensitive information)",
        "urdu_meaning": "آشکار کرنا",
        "primary_meaning": "reveal",
        "secondary_meaning": "disclose",
        "tertiary_meaning": "expose",
        "sentence": "The journalist refused to divulge the identity of the confidential source."
    },
    449: {
        "word": "Doctrinaire",
        "english_meaning": "seeking to impose a doctrine in all circumstances without regard to practical considerations",
        "urdu_meaning": "عقائد پر مبنی",
        "primary_meaning": "dogmatic",
        "secondary_meaning": "authoritarian",
        "tertiary_meaning": "unyielding",
        "sentence": "His doctrinaire approach to politics alienated many who sought flexibility and compromise."
    },
    450: {
        "word": "Documentary",
        "english_meaning": "consisting of or based on official documents",
        "urdu_meaning": "تحقیقاتی فلم",
        "primary_meaning": "factual",
        "secondary_meaning": "non-fictional",
        "tertiary_meaning": "realistic",
        "sentence": "The documentary provided an in-depth analysis of historical events based on authentic records."
    },
    451: {
        "word": "Dogged",
        "english_meaning": "having or showing tenacity and grim persistence",
        "urdu_meaning": "استقامتی",
        "primary_meaning": "persistent",
        "secondary_meaning": "determined",
        "tertiary_meaning": "resolute",
        "sentence": "Despite facing numerous obstacles, his dogged determination led him to success."
    },
    452: {
        "word": "Dogmatic",
        "english_meaning": "inclined to lay down principles as incontrovertibly true",
        "urdu_meaning": "عقائدی",
        "primary_meaning": "authoritarian",
        "secondary_meaning": "opinionated",
        "tertiary_meaning": "rigid",
        "sentence": "The professor's dogmatic approach stifled open discussion in the classroom."
    },
    453: {
        "word": "Dormant",
        "english_meaning": "having normal physical functions suspended or slowed down for a period of time; in or as if in a deep sleep",
        "urdu_meaning": "سست",
        "primary_meaning": "inactive",
        "secondary_meaning": "latent",
        "tertiary_meaning": "quiescent",
        "sentence": "During the winter, many plants remain dormant until the warmer months."
    },
    454: {
        "word": "Dowdy",
        "english_meaning": "unfashionable and without style in appearance",
        "urdu_meaning": "بے ترتیب",
        "primary_meaning": "unstylish",
        "secondary_meaning": "frumpy",
        "tertiary_meaning": "drab",
        "sentence": "She felt dowdy in the outdated outfit that she had worn for years."
    },
    455: {
        "word": "Draconian",
        "english_meaning": "excessively harsh and severe",
        "urdu_meaning": "سنگین سازشی",
        "primary_meaning": "harsh",
        "secondary_meaning": "stringent",
        "tertiary_meaning": "rigorous",
        "sentence": "The new law imposed draconian penalties for even minor offenses."
    },
    456: {
        "word": "Droll",
        "english_meaning": "curious or unusual in a way that provokes dry amusement",
        "urdu_meaning": "مزیدار",
        "primary_meaning": "amusing",
        "secondary_meaning": "comical",
        "tertiary_meaning": "humorous",
        "sentence": "His droll sense of humor always brought a smile to people's faces."
    },
    457: {
        "word": "Dubious",
        "english_meaning": "hesitating or doubting; not to be relied upon",
        "urdu_meaning": "مشکوک",
        "primary_meaning": "uncertain",
        "secondary_meaning": "skeptical",
        "tertiary_meaning": "distrustful",
        "sentence": "The businessman had a dubious reputation, and many were skeptical of his deals."
    },
    458: {
        "word": "Dupe",
        "english_meaning": "deceive; trick",
        "urdu_meaning": "دہوکہ دینا",
        "primary_meaning": "deceive",
        "secondary_meaning": "fool",
        "tertiary_meaning": "trick",
        "sentence": "She realized she had been duped into buying a counterfeit product."
    },
    459: {
        "word": "Duplicitous",
        "english_meaning": "deceitful; dishonest",
        "urdu_meaning": "دغا باز",
        "primary_meaning": "deceptive",
        "secondary_meaning": "two-faced",
        "tertiary_meaning": "treacherous",
        "sentence": "His duplicitous actions were revealed when the truth came to light."
    },
    460: {
        "word": "Duplicity",
        "english_meaning": "deceitfulness; double-dealing",
        "urdu_meaning": "مکر",
        "primary_meaning": "deceit",
        "secondary_meaning": "fraud",
        "tertiary_meaning": "duplicity",
        "sentence": "His duplicity was exposed when the truth came to light."
    },
    461: {
        "word": "Duress",
        "english_meaning": "threats, violence, constraints, or other action used to coerce someone into doing something against their will",
        "urdu_meaning": "زبردستی",
        "primary_meaning": "coercion",
        "secondary_meaning": "pressure",
        "tertiary_meaning": "intimidation",
        "sentence": "He signed the contract under duress, fearing the consequences."
    },
    462: {
        "word": "Dwarf",
        "english_meaning": "a person of unusually small stature or a mythical being resembling a tiny old man",
        "urdu_meaning": "بونا",
        "primary_meaning": "midget",
        "secondary_meaning": "tiny person",
        "tertiary_meaning": "dwarf",
        "sentence": "The fairy tale featured a friendly dwarf who helped the protagonist on the quest."
    },
    463: {
        "word": "Dwindling",
        "english_meaning": "gradually becoming smaller or diminishing",
        "urdu_meaning": "کم ہونا",
        "primary_meaning": "diminishing",
        "secondary_meaning": "shrinking",
        "tertiary_meaning": "decreasing",
        "sentence": "The company faced challenges, leading to a dwindling number of employees."
    },
    464: {
        "word": "Dynamism",
        "english_meaning": "the quality of being characterized by vigorous activity and progress",
        "urdu_meaning": "توانائی",
        "primary_meaning": "vitality",
        "secondary_meaning": "energy",
        "tertiary_meaning": "dynamism",
        "sentence": "The team's dynamism and creativity contributed to the success of the project."
    },
    465: {
        "word": "Ebullient",
        "english_meaning": "cheerful and full of energy",
        "urdu_meaning": "چمکیلا",
        "primary_meaning": "enthusiastic",
        "secondary_meaning": "lively",
        "tertiary_meaning": "ebullient",
        "sentence": "She greeted everyone with an ebullient smile, spreading positivity."
    },
    466: {
        "word": "Eccentric",
        "english_meaning": "unconventional and slightly strange",
        "urdu_meaning": "غیر معمولی",
        "primary_meaning": "unusual",
        "secondary_meaning": "quirky",
        "tertiary_meaning": "eccentric",
        "sentence": "The artist was known for his eccentric fashion sense and artistic creations."
    },
    467: {
        "word": "Echelon",
        "english_meaning": "a level or rank in an organization, profession, or society",
        "urdu_meaning": "طبقہ",
        "primary_meaning": "level",
        "secondary_meaning": "rank",
        "tertiary_meaning": "echelon",
        "sentence": "She worked hard to move up the echelons of the corporate ladder."
    },
    468: {
        "word": "Eclectic",
        "english_meaning": "deriving ideas, style, or taste from a broad and diverse range of sources",
        "urdu_meaning": "اختلافی",
        "primary_meaning": "diverse",
        "secondary_meaning": "varied",
        "tertiary_meaning": "eclectic",
        "sentence": "His eclectic taste in music ranged from classical to contemporary."
    },
    469: {
        "word": "Eclipse",
        "english_meaning": "a loss of significance or power in relation to another person or thing",
        "urdu_meaning": "سورج گرہن",
        "primary_meaning": "obscure",
        "secondary_meaning": "overshadow",
        "tertiary_meaning": "eclipse",
        "sentence": "The new discovery would eclipse the importance of the previous one."
    },
    470: {
        "word": "Ecological",
        "english_meaning": "related to or concerned with the relation of living organisms to one another and to their physical surroundings",
        "urdu_meaning": "ماحولیاتی",
        "primary_meaning": "environmental",
        "secondary_meaning": "ecological",
        "tertiary_meaning": "sustainable",
        "sentence": "The ecological impact of the construction project was carefully assessed."
    },
    471: {
        "word": "Economical",
        "english_meaning": "giving good value or service in relation to the amount of money, time, or effort spent",
        "urdu_meaning": "معقول",
        "primary_meaning": "cost-effective",
        "secondary_meaning": "efficient",
        "tertiary_meaning": "economical",
        "sentence": "The new car model is not only stylish but also economical in terms of fuel consumption."
    },
    472: {
        "word": "Economy",
        "english_meaning": "the system by which a country's money and goods are produced and used, or a country considered in this way",
        "urdu_meaning": "معیشت",
        "primary_meaning": "economic system",
        "secondary_meaning": "financial structure",
        "tertiary_meaning": "economy",
        "sentence": "The government implemented policies to stabilize the national economy."
    },
    473: {
        "word": "Ecstatic",
        "english_meaning": "feeling or expressing overwhelming happiness or joyful excitement",
        "urdu_meaning": "مسرور",
        "primary_meaning": "joyful",
        "secondary_meaning": "elated",
        "tertiary_meaning": "ecstatic",
        "sentence": "Winning the championship made the team ecstatic with pure joy."
    },
    474: {
        "word": "Edify",
        "english_meaning": "instruct or improve (someone) morally or intellectually",
        "urdu_meaning": "تربیت دینا",
        "primary_meaning": "educate",
        "secondary_meaning": "enlighten",
        "tertiary_meaning": "edify",
        "sentence": "Reading books can edify and broaden one's perspective."
    },
    475: {
        "word": "Efficacious",
        "english_meaning": "effective in producing a desired result",
        "urdu_meaning": "موثر",
        "primary_meaning": "effective",
        "secondary_meaning": "successful",
        "tertiary_meaning": "efficacious",
        "sentence": "The medicine proved to be efficacious in treating the symptoms."
    },
    476: {
        "word": "Efficacy",
        "english_meaning": "the ability to produce a desired or intended result",
        "urdu_meaning": "تاثیر",
        "primary_meaning": "effectiveness",
        "secondary_meaning": "efficacy",
        "tertiary_meaning": "capability",
        "sentence": "The efficacy of the new vaccine was demonstrated in clinical trials."
    },
    477: {
        "word": "Effrontery",
        "english_meaning": "insolent or impertinent behavior",
        "urdu_meaning": "بے ادبی",
        "primary_meaning": "impudence",
        "secondary_meaning": "boldness",
        "tertiary_meaning": "effrontery",
        "sentence": "His effrontery in challenging the authority led to disciplinary action."
    },
    478: {
        "word": "Egalitarian",
        "english_meaning": "believing in or based on the principle that all people are equal and deserve equal rights and opportunities",
        "urdu_meaning": "برابری",
        "primary_meaning": "equalitarian",
        "secondary_meaning": "egalitarian",
        "tertiary_meaning": "fair",
        "sentence": "The organization promotes an egalitarian approach to workplace policies."
    },
    479: {
        "word": "Egoism",
        "english_meaning": "an ethical theory that treats self-interest as the foundation of morality",
        "urdu_meaning": "خودی",
        "primary_meaning": "self-interest",
        "secondary_meaning": "egoism",
        "tertiary_meaning": "selfishness",
        "sentence": "His actions were motivated by egoism rather than concern for others."
    },
    480: {
        "word": "Egotist",
        "english_meaning": "a person who is excessively conceited or self-centered",
        "urdu_meaning": "خود پسند",
        "primary_meaning": "self-centered",
        "secondary_meaning": "egotistical",
        "tertiary_meaning": "narcissist",
        "sentence": "The egotist could not stop talking about his own achievements."
    },
    481: {
        "word": "Egregious",
        "english_meaning": "outstandingly bad; shocking",
        "urdu_meaning": "ناقابل تسلیم",
        "primary_meaning": "shocking",
        "secondary_meaning": "appalling",
        "tertiary_meaning": "egregious",
        "sentence": "The company's failure to meet safety standards was an egregious oversight."
    },
    482: {
        "word": "Elate",
        "english_meaning": "make (someone) ecstatically happy",
        "urdu_meaning": "خوش ہونا",
        "primary_meaning": "thrill",
        "secondary_meaning": "excite",
        "tertiary_meaning": "elate",
        "sentence": "Winning the championship elated the entire team and their fans."
    },
    483: {
        "word": "Elated",
        "english_meaning": "very happy and excited; jubilant",
        "urdu_meaning": "بہت خوش",
        "primary_meaning": "joyful",
        "secondary_meaning": "ecstatic",
        "tertiary_meaning": "elated",
        "sentence": "Her elated expression showed the joy of achieving her long-held goal."
    },
    484: {
        "word": "Elementary",
        "english_meaning": "relating to the first principles of a subject; straightforward and uncomplicated",
        "urdu_meaning": "بنیادی",
        "primary_meaning": "basic",
        "secondary_meaning": "fundamental",
        "tertiary_meaning": "elementary",
        "sentence": "The book explains elementary concepts in a way that is easy for beginners to understand."
    },
    485: {
        "word": "Elevate",
        "english_meaning": "raise or lift (something) up to a higher position",
        "urdu_meaning": "اونچا کرنا",
        "primary_meaning": "lift",
        "secondary_meaning": "raise",
        "tertiary_meaning": "elevate",
        "sentence": "The platform was designed to elevate the speaker to be visible to the entire audience."
    },
    486: {
        "word": "Elicit",
        "english_meaning": "draw out (a response, information, etc.) from someone in reaction to one's own actions or questions",
        "urdu_meaning": "حاصل کرنا",
        "primary_meaning": "extract",
        "secondary_meaning": "obtain",
        "tertiary_meaning": "elicit",
        "sentence": "The detective skillfully elicited crucial information during the interrogation."
    },
    487: {
        "word": "Elitist",
        "english_meaning": "a person who believes in the superiority of a particular group",
        "urdu_meaning": "اعلی طبقے کا حامی",
        "primary_meaning": "snobbish",
        "secondary_meaning": "exclusive",
        "tertiary_meaning": "arrogant",
        "sentence": "His elitist attitude made it difficult for him to connect with people from different backgrounds."
    },
    488: {
        "word": "Eloquent",
        "english_meaning": "fluent or persuasive in speaking or writing",
        "urdu_meaning": "خوبصورت",
        "primary_meaning": "articulate",
        "secondary_meaning": "expressive",
        "tertiary_meaning": "eloquent",
        "sentence": "The speaker delivered an eloquent speech that captivated the audience."
    },
    489: {
        "word": "Elucidate",
        "english_meaning": "make (something) clear; explain",
        "urdu_meaning": "واضح کرنا",
        "primary_meaning": "clarify",
        "secondary_meaning": "illuminate",
        "tertiary_meaning": "expound",
        "sentence": "The professor took the time to elucidate complex concepts for the students."
    },
    490: {
        "word": "Elusive",
        "english_meaning": "difficult to catch or define; evasive",
        "urdu_meaning": "پیچھے ہٹنے والا",
        "primary_meaning": "evading",
        "secondary_meaning": "escaping",
        "tertiary_meaning": "eluding",
        "sentence": "The elusive thief managed to escape capture once again."
    },
    491: {
        "word": "Embargo",
        "english_meaning": "an official ban on trade or other commercial activity with a particular country",
        "urdu_meaning": "تجارتی پابندی",
        "primary_meaning": "ban",
        "secondary_meaning": "restriction",
        "tertiary_meaning": "prohibition",
        "sentence": "The government imposed an embargo on imports from the sanctioned nation."
    },
    492: {
        "word": "Embellish",
        "english_meaning": "make (something) more attractive by the addition of decorative details or features",
        "urdu_meaning": "سجانا",
        "primary_meaning": "decorate",
        "secondary_meaning": "adorn",
        "tertiary_meaning": "ornament",
        "sentence": "The artist chose to embellish the painting with vibrant colors and intricate patterns."
    },
    493: {
        "word": "Empathy",
        "english_meaning": "the ability to understand and share the feelings of another",
        "urdu_meaning": "ہمدردی",
        "primary_meaning": "compassion",
        "secondary_meaning": "understanding",
        "tertiary_meaning": "sympathy",
        "sentence": "Her empathy towards the struggling community inspired others to lend a helping hand."
    },
    494: {
        "word": "Empirical",
        "english_meaning": "based on observation or experience rather than theory or pure logic",
        "urdu_meaning": "تجرباتی",
        "primary_meaning": "practical",
        "secondary_meaning": "experimental",
        "tertiary_meaning": "factual",
        "sentence": "Scientific research often relies on empirical evidence to draw conclusions."
    },
    495: {
        "word": "Emulate",
        "english_meaning": "match or surpass (a person or achievement), typically by imitation",
        "urdu_meaning": "نقل کرنا",
        "primary_meaning": "imitate",
        "secondary_meaning": "mimic",
        "tertiary_meaning": "emulate",
        "sentence": "The young artist aspired to emulate the success of her favorite painters."
    },
    496: {
        "word": "Enamor",
        "english_meaning": "be filled with a feeling of love for",
        "urdu_meaning": "محبت میں بھٹکنا",
        "primary_meaning": "adore",
        "secondary_meaning": "captivate",
        "tertiary_meaning": "infatuate",
        "sentence": "He became enamored with her kindness and intelligence."
    },
    497: {
        "word": "Enchant",
        "english_meaning": "delight (someone) greatly; bewitch",
        "urdu_meaning": "موہ لینا",
        "primary_meaning": "charm",
        "secondary_meaning": "captivate",
        "tertiary_meaning": "enrapture",
        "sentence": "The magical performance had the power to enchant audiences of all ages."
    },
    498: {
        "word": "Encroach",
        "english_meaning": "intrude on (a person's territory, rights, personal life, etc.)",
        "urdu_meaning": "دخل انداز ہونا",
        "primary_meaning": "invade",
        "secondary_meaning": "trespass",
        "tertiary_meaning": "encroach",
        "sentence": "The construction project began to encroach on the neighboring property."
    },
    499: {
        "word": "Encyclopedic",
        "english_meaning": "comprehensive in terms of information; covering all branches of knowledge",
        "urdu_meaning": "انسائیکلوپیڈیک",
        "primary_meaning": "comprehensive",
        "secondary_meaning": "all-encompassing",
        "tertiary_meaning": "encyclopedic",
        "sentence": "Her knowledge of literature was encyclopedic, ranging from classic novels to modern poetry."
    },
    500: {
        "word": "Endanger",
        "english_meaning": "put (someone or something) at risk or in danger",
        "urdu_meaning": "خطرے میں ڈالنا",
        "primary_meaning": "threaten",
        "secondary_meaning": "jeopardize",
        "tertiary_meaning": "endanger",
        "sentence": "The construction activity could endanger the habitat of the endangered species."
    },
    501: {
        "word": "Endemic",
        "english_meaning": "native to or restricted to a certain country or area",
        "urdu_meaning": "مقامی",
        "primary_meaning": "indigenous",
        "secondary_meaning": "native",
        "tertiary_meaning": "endemic",
        "sentence": "The endemic species of plants can only be found in the rainforest region."
    },
    502: {
        "word": "Endorse",
        "english_meaning": "declare one's public approval or support of",
        "urdu_meaning": "تصدیق کرنا",
        "primary_meaning": "approve",
        "secondary_meaning": "support",
        "tertiary_meaning": "endorse",
        "sentence": "The celebrity was chosen to endorse the new skincare product."
    },
    503: {
        "word": "Endow",
        "english_meaning": "provide with a quality, ability, or asset",
        "urdu_meaning": "نوازنا",
        "primary_meaning": "bestow",
        "secondary_meaning": "grant",
        "tertiary_meaning": "endow",
        "sentence": "The philanthropist decided to endow the university with a generous scholarship fund."
    },
    504: {
        "word": "Enervate",
        "english_meaning": "cause (someone) to feel drained of energy or vitality",
        "urdu_meaning": "کمزور کر دینا",
        "primary_meaning": "weaken",
        "secondary_meaning": "debilitate",
        "tertiary_meaning": "enervate",
        "sentence": "The exhausting journey began to enervate even the most resilient hikers."
    },
    505: {
        "word": "Enfeeble",
        "english_meaning": "make weak or feeble",
        "urdu_meaning": "کمزور کرنا",
        "primary_meaning": "weaken",
        "secondary_meaning": "debilitate",
        "tertiary_meaning": "enfeeble",
        "sentence": "The prolonged illness threatened to enfeeble the patient's strength."
    },
    506: {
        "word": "Engage",
        "english_meaning": "occupy, attract, or involve (someone's interest or attention)",
        "urdu_meaning": "مشغول کرنا",
        "primary_meaning": "captivate",
        "secondary_meaning": "involve",
        "tertiary_meaning": "engage",
        "sentence": "The gripping novel managed to engage readers from start to finish."
    },
    507: {
        "word": "Engender",
        "english_meaning": "cause or give rise to (a feeling, situation, or condition)",
        "urdu_meaning": "پیدا کرنا",
        "primary_meaning": "create",
        "secondary_meaning": "generate",
        "tertiary_meaning": "engender",
        "sentence": "The divisive policies were likely to engender social unrest."
    },
    508: {
        "word": "Enigmatic",
        "english_meaning": "difficult to interpret or understand; mysterious",
        "urdu_meaning": "پیچیدہ",
        "primary_meaning": "mysterious",
        "secondary_meaning": "cryptic",
        "tertiary_meaning": "enigmatic",
        "sentence": "The enigmatic smile on her face left everyone curious about her thoughts."
    },
    509: {
        "word": "Enlarge",
        "english_meaning": "make or become larger or more extensive",
        "urdu_meaning": "براہ کرم ہونا",
        "primary_meaning": "expand",
        "secondary_meaning": "increase",
        "tertiary_meaning": "enlarge",
        "sentence": "The architect proposed to enlarge the living room by removing the dividing wall."
    },
    510: {
        "word": "Enlighten",
        "english_meaning": "give (someone) greater knowledge and understanding about a subject or situation",
        "urdu_meaning": "روشنی دینا",
        "primary_meaning": "inform",
        "secondary_meaning": "educate",
        "tertiary_meaning": "enlighten",
        "sentence": "The teacher sought to enlighten her students about the historical events."
    },
    511: {
        "word": "Enmity",
        "english_meaning": "the state or feeling of being actively opposed or hostile to someone or something",
        "urdu_meaning": "دشمنی",
        "primary_meaning": "hostility",
        "secondary_meaning": "animosity",
        "tertiary_meaning": "enmity",
        "sentence": "The longstanding enmity between the two nations eventually led to armed conflict."
    },
    512: {
        "word": "Ennui",
        "english_meaning": "a feeling of listlessness and dissatisfaction arising from a lack of occupation or excitement",
        "urdu_meaning": "بوریت",
        "primary_meaning": "boredom",
        "secondary_meaning": "monotony",
        "tertiary_meaning": "ennui",
        "sentence": "The rainy weekend left her with a sense of ennui as there was nothing exciting to do."
    },
    513: {
        "word": "Ensue",
        "english_meaning": "happen or occur afterward or as a result",
        "urdu_meaning": "پیش آنا",
        "primary_meaning": "follow",
        "secondary_meaning": "result",
        "tertiary_meaning": "ensue",
        "sentence": "If the conflict escalates, chaos and unrest may ensue."
    },
    514: {
        "word": "Entail",
        "english_meaning": "involve (something) as a necessary or inevitable part or consequence",
        "urdu_meaning": "ساتھ لے کر آنا",
        "primary_meaning": "involve",
        "secondary_meaning": "require",
        "tertiary_meaning": "entail",
        "sentence": "The decision to expand the business would entail additional costs and responsibilities."
    },
    515: {
        "word": "Enthrall",
        "english_meaning": "capture the fascinated attention of",
        "urdu_meaning": "محبت میں بھٹکانا",
        "primary_meaning": "captivate",
        "secondary_meaning": "mesmerize",
        "tertiary_meaning": "enthrall",
        "sentence": "The storyteller had the ability to enthrall listeners with his captivating tales."
    },
    516: {
        "word": "Entitled",
        "english_meaning": "believing oneself to be inherently deserving of privileges or special treatment",
        "urdu_meaning": "حقدار",
        "primary_meaning": "privileged",
        "secondary_meaning": "deserving",
        "tertiary_meaning": "empowered",
        "sentence": "Some individuals feel entitled to success without putting in the necessary effort."
    },
    517: {
        "word": "Entreat",
        "english_meaning": "ask someone earnestly or anxiously to do something",
        "urdu_meaning": "درخواست کرنا",
        "primary_meaning": "plead",
        "secondary_meaning": "beseech",
        "tertiary_meaning": "implore",
        "sentence": "She would entreat him to reconsider his decision."
    },
    518: {
        "word": "Entreaty",
        "english_meaning": "an earnest or humble request",
        "urdu_meaning": "درخواست",
        "primary_meaning": "plea",
        "secondary_meaning": "appeal",
        "tertiary_meaning": "petition",
        "sentence": "The prisoner made an entreaty for clemency to the judge."
    },
    519: {
        "word": "Entrench",
        "english_meaning": "establish (an attitude, habit, or belief) so firmly that change is very difficult or unlikely",
        "urdu_meaning": "مضبوط کرنا",
        "primary_meaning": "establish",
        "secondary_meaning": "fortify",
        "tertiary_meaning": "solidify",
        "sentence": "The traditions were deeply entrenching the cultural values of the community."
    },
    520: {
        "word": "Entrenched",
        "english_meaning": "firmly established and difficult or unlikely to change; ingrained",
        "urdu_meaning": "مستقر",
        "primary_meaning": "established",
        "secondary_meaning": "rooted",
        "tertiary_meaning": "deep-seated",
        "sentence": "The prejudice was so entrenched in society that challenging it became a significant task."
    },
    521: {
        "word": "Enviable",
        "english_meaning": "arousing or likely to arouse envy",
        "urdu_meaning": "قابل حسرت",
        "primary_meaning": "desirable",
        "secondary_meaning": "coveted",
        "tertiary_meaning": "admired",
        "sentence": "Her enviable success in the field made others aspire to achieve similar heights."
    },
    522: {
        "word": "Ephemeral",
        "english_meaning": "lasting for a very short time",
        "urdu_meaning": "عارضی",
        "primary_meaning": "transient",
        "secondary_meaning": "fleeting",
        "tertiary_meaning": "momentary",
        "sentence": "The beauty of the cherry blossoms is ephemeral, lasting only a few weeks each spring."
    },
    523: {
        "word": "Equanimity",
        "english_meaning": "mental calmness, composure, and evenness of temper, especially in difficult situations",
        "urdu_meaning": "برابری",
        "primary_meaning": "composure",
        "secondary_meaning": "calmness",
        "tertiary_meaning": "serenity",
        "sentence": "Even in the face of adversity, she maintained her equanimity and approached challenges with a steady mind."
    },
    524: {
        "word": "Equitable",
        "english_meaning": "fair and impartial; just",
        "urdu_meaning": "انصافی",
        "primary_meaning": "fair",
        "secondary_meaning": "impartial",
        "tertiary_meaning": "even-handed",
        "sentence": "The judge ensured an equitable distribution of resources among the parties involved in the dispute."
    },
    525: {
        "word": "Equivocal",
        "english_meaning": "open to more than one interpretation; ambiguous",
        "urdu_meaning": "مبہم",
        "primary_meaning": "ambiguous",
        "secondary_meaning": "uncertain",
        "tertiary_meaning": "vague",
        "sentence": "The politician's equivocal statement left room for speculation about his true intentions."
    },
    526: {
        "word": "Equivocate",
        "english_meaning": "use ambiguous language so as to conceal the truth or avoid committing oneself",
        "urdu_meaning": "مبہم ہونا",
        "primary_meaning": "evade",
        "secondary_meaning": "dodge",
        "tertiary_meaning": "prevaricate",
        "sentence": "The spokesperson tried to equivocate when pressed for details about the controversial decision."
    },
    527: {
        "word": "Eradicate",
        "english_meaning": "destroy completely; put an end to",
        "urdu_meaning": "ختم کرنا",
        "primary_meaning": "eliminate",
        "secondary_meaning": "eradicate",
        "tertiary_meaning": "exterminate",
        "sentence": "The goal is to eradicate poverty and create a more equitable society."
    },
    528: {
        "word": "Erode",
        "english_meaning": "gradually wear away or diminish",
        "urdu_meaning": "کٹنا",
        "primary_meaning": "wear away",
        "secondary_meaning": "deteriorate",
        "tertiary_meaning": "corrode",
        "sentence": "Over time, the constant flow of water can erode even the toughest rocks."
    },
    529: {
        "word": "Erratic",
        "english_meaning": "not even or regular in pattern or movement; unpredictable",
        "urdu_meaning": "غیر مستقر",
        "primary_meaning": "unpredictable",
        "secondary_meaning": "inconsistent",
        "tertiary_meaning": "irregular",
        "sentence": "The erratic behavior of the stock market makes it challenging to predict future trends."
    },
    530: {
        "word": "Erroneous",
        "english_meaning": "wrong; incorrect",
        "urdu_meaning": "غلط",
        "primary_meaning": "incorrect",
        "secondary_meaning": "inaccurate",
        "tertiary_meaning": "false",
        "sentence": "The article contained several erroneous statements that needed correction."
    },
    531: {
        "word": "Erstwhile",
        "english_meaning": "former; in the past",
        "urdu_meaning": "پہلے",
        "primary_meaning": "former",
        "secondary_meaning": "past",
        "tertiary_meaning": "bygone",
        "sentence": "The erstwhile champion retired from professional sports after a successful career."
    },
    532: {
        "word": "Erudite",
        "english_meaning": "having or showing great knowledge or learning",
        "urdu_meaning": "علمبردار",
        "primary_meaning": "knowledgeable",
        "secondary_meaning": "learned",
        "tertiary_meaning": "scholarly",
        "sentence": "The professor was known for his erudite lectures on classical literature."
    },
    533: {
        "word": "Escalate",
        "english_meaning": "increase rapidly; become more intense",
        "urdu_meaning": "برتری حاصل ہونا",
        "primary_meaning": "intensify",
        "secondary_meaning": "heighten",
        "tertiary_meaning": "accelerate",
        "sentence": "The conflict between the two nations began to escalate, leading to heightened tensions."
    },
    534: {
        "word": "Eschew",
        "english_meaning": "deliberately avoid using; abstain from",
        "urdu_meaning": "اجتناب کرنا",
        "primary_meaning": "avoid",
        "secondary_meaning": "refrain",
        "tertiary_meaning": "shun",
        "sentence": "He made a conscious effort to eschew unhealthy habits and adopt a healthier lifestyle."
    },
    535: {
        "word": "Esoteric",
        "english_meaning": "intended for or understood by only a small number of people with special knowledge",
        "urdu_meaning": "خفیہ",
        "primary_meaning": "obscure",
        "secondary_meaning": "cryptic",
        "tertiary_meaning": "arcane",
        "sentence": "The professor's lecture on quantum physics was so esoteric that only a few students could grasp its complexities."
    },
    536: {
        "word": "Estimable",
        "english_meaning": "worthy of respect; admirable",
        "urdu_meaning": "قابل تعریف",
        "primary_meaning": "admirable",
        "secondary_meaning": "commendable",
        "tertiary_meaning": "respectable",
        "sentence": "Her charitable work and dedication to social causes made her an estimable figure in the community."
    },
    537: {
        "word": "Estrange",
        "english_meaning": "cause (someone) to be no longer close or affectionate to someone; alienate",
        "urdu_meaning": "دور کرنا",
        "primary_meaning": "alienate",
        "secondary_meaning": "separate",
        "tertiary_meaning": "distance",
        "sentence": "Misunderstandings can easily estrange even the closest of friends."
    },
    538: {
        "word": "Euphemism",
        "english_meaning": "a mild or indirect word or expression substituted for one considered to be too harsh or blunt",
        "urdu_meaning": "لطیف زبانی",
        "primary_meaning": "substitute",
        "secondary_meaning": "alternative",
        "tertiary_meaning": "polite term",
        "sentence": "Using the term 'passed away' is a euphemism for 'died,' providing a gentler way to express the idea."
    },
    539: {
        "word": "Euphoric",
        "english_meaning": "characterized by or feeling intense excitement and happiness",
        "urdu_meaning": "خوشی سے بھرا ہوا",
        "primary_meaning": "joyful",
        "secondary_meaning": "ecstatic",
        "tertiary_meaning": "elated",
        "sentence": "Winning the championship made the team and their fans euphoric with joy."
    },
    540: {
        "word": "Evade",
        "english_meaning": "escape or avoid, especially by cleverness or trickery",
        "urdu_meaning": "بچنا",
        "primary_meaning": "avoid",
        "secondary_meaning": "dodge",
        "tertiary_meaning": "evade",
        "sentence": "The suspect attempted to evade capture by hiding in a remote area."
    },
    541: {
        "word": "Evanescent",
        "english_meaning": "soon passing out of sight, memory, or existence; quickly fading or disappearing",
        "urdu_meaning": "عارضی",
        "primary_meaning": "fleeting",
        "secondary_meaning": "transient",
        "tertiary_meaning": "momentary",
        "sentence": "The beauty of a sunset is evanescent, as it lasts only for a brief moment."
    },
    542: {
        "word": "Evasive",
        "english_meaning": "tending to avoid commitment or self-revelation, especially by responding only indirectly",
        "urdu_meaning": "پرہیز گار",
        "primary_meaning": "ambiguous",
        "secondary_meaning": "vague",
        "tertiary_meaning": "equivocal",
        "sentence": "The politician gave evasive answers to avoid addressing the controversial issue directly."
    },
    543: {
        "word": "Eventuate",
        "english_meaning": "occur as a result; happen",
        "urdu_meaning": "واقع ہونا",
        "primary_meaning": "result",
        "secondary_meaning": "happen",
        "tertiary_meaning": "transpire",
        "sentence": "The negotiations between the two countries eventually eventuated in a historic peace agreement."
    },
    544: {
        "word": "Evoke",
        "english_meaning": "bring or recall to the conscious mind; elicit",
        "urdu_meaning": "تداعی کرنا",
        "primary_meaning": "elicit",
        "secondary_meaning": "arouse",
        "tertiary_meaning": "summon",
        "sentence": "The old photograph evoked memories of a cherished family vacation."
    },
    545: {
        "word": "Exacerbate",
        "english_meaning": "make (a problem, bad situation, or negative feeling) worse",
        "urdu_meaning": "براہ کرم بڑھانا",
        "primary_meaning": "worsen",
        "secondary_meaning": "aggravate",
        "tertiary_meaning": "intensify",
        "sentence": "The harsh criticism only served to exacerbate the tension in the workplace."
    },
    546: {
        "word": "Exact",
        "english_meaning": "demand and obtain (something, especially a payment) from someone",
        "urdu_meaning": "طلب کرنا",
        "primary_meaning": "demand",
        "secondary_meaning": "require",
        "tertiary_meaning": "command",
        "sentence": "The landlord will exact the rent payment by the end of the month."
    },
    547: {
        "word": "Exacting",
        "english_meaning": "making great demands on one's skill, attention, or other resources",
        "urdu_meaning": "سخت",
        "primary_meaning": "demanding",
        "secondary_meaning": "rigorous",
        "tertiary_meaning": "precise",
        "sentence": "The job was so exacting that only a few people could meet its requirements."
    },
    548: {
        "word": "Exalt",
        "english_meaning": "hold (someone or something) in very high regard; think or speak very highly of",
        "urdu_meaning": "عظیم کرنا",
        "primary_meaning": "praise",
        "secondary_meaning": "elevate",
        "tertiary_meaning": "glorify",
        "sentence": "The poet wrote to exalt the beauty of nature and its wonders."
    },
    549: {
        "word": "Exasperate",
        "english_meaning": "irritate intensely; infuriate",
        "urdu_meaning": "پریشان کرنا",
        "primary_meaning": "irritate",
        "secondary_meaning": "annoy",
        "tertiary_meaning": "vex",
        "sentence": "His repeated delays began to exasperate everyone waiting for him."
    },
    550: {
        "word": "Excoriate",
        "english_meaning": "censure or criticize severely",
        "urdu_meaning": "تنقید کرنا",
        "primary_meaning": "criticize",
        "secondary_meaning": "condemn",
        "tertiary_meaning": "rebuke",
        "sentence": "The journalist chose to excoriate the government for its lack of transparency."
    },
    551: {
        "word": "Exculpate",
        "english_meaning": "show or declare that (someone) is not guilty of wrongdoing",
        "urdu_meaning": "بری کرنا",
        "primary_meaning": "exonerate",
        "secondary_meaning": "absolve",
        "tertiary_meaning": "clear",
        "sentence": "New evidence emerged to exculpate the accused, leading to their release."
    },
    552: {
        "word": "Exegesis",
        "english_meaning": "critical explanation or interpretation of a text, especially of scripture",
        "urdu_meaning": "تفسیر",
        "primary_meaning": "interpretation",
        "secondary_meaning": "commentary",
        "tertiary_meaning": "explanation",
        "sentence": "The professor provided an in-depth exegesis of the ancient manuscript."
    },
    553: {
        "word": "Exhaustive",
        "english_meaning": "covering all possible details; comprehensive",
        "urdu_meaning": "جامع",
        "primary_meaning": "comprehensive",
        "secondary_meaning": "thorough",
        "tertiary_meaning": "complete",
        "sentence": "The researcher conducted an exhaustive study of the historical archives."
    },
    554: {
        "word": "Exhilarating",
        "english_meaning": "making (someone) feel very happy, animated, or elated",
        "urdu_meaning": "لطیف",
        "primary_meaning": "invigorating",
        "secondary_meaning": "stimulating",
        "tertiary_meaning": "thrilling",
        "sentence": "The mountain climb was exhilarating, offering breathtaking views at the summit."
    },
    555: {
        "word": "Exhort",
        "english_meaning": "strongly encourage or urge (someone) to do something",
        "urdu_meaning": "متنبہ کرنا",
        "primary_meaning": "urge",
        "secondary_meaning": "advise",
        "tertiary_meaning": "prompt",
        "sentence": "The coach would exhort the team to give their best performance in the upcoming match."
    },
    556: {
        "word": "Exigent",
        "english_meaning": "pressing; demanding",
        "urdu_meaning": "ضروری",
        "primary_meaning": "urgent",
        "secondary_meaning": "critical",
        "tertiary_meaning": "compelling",
        "sentence": "The exigent circumstances required immediate attention and action."
    },
    557: {
        "word": "Exonerate",
        "english_meaning": "absolve from blame for a fault or wrongdoing",
        "urdu_meaning": "بری کرنا",
        "primary_meaning": "clear",
        "secondary_meaning": "acquit",
        "tertiary_meaning": "vindicate",
        "sentence": "The evidence presented in court was sufficient to exonerate the defendant."
    },
    558: {
        "word": "Exorbitant",
        "english_meaning": "unreasonably high (price, amount, or level)",
        "urdu_meaning": "ناقابل قبول",
        "primary_meaning": "excessive",
        "secondary_meaning": "outrageous",
        "tertiary_meaning": "unjustified",
        "sentence": "The hotel charged an exorbitant fee for its luxury services."
    },
    559: {
        "word": "Exorcise",
        "english_meaning": "drive out or attempt to drive out (an evil spirit) from a person or place",
        "urdu_meaning": "شیطان نکالنا",
        "primary_meaning": "banish",
        "secondary_meaning": "expel",
        "tertiary_meaning": "purge",
        "sentence": "The priest performed a ritual to exorcise the malevolent spirit from the haunted house."
    },
    560: {
        "word": "Exotic",
        "english_meaning": "attractive or striking because it is unusual or different from what is familiar",
        "urdu_meaning": "غیر ملکی",
        "primary_meaning": "unusual",
        "secondary_meaning": "foreign",
        "tertiary_meaning": "rare",
        "sentence": "The marketplace offered a variety of exotic spices and fruits from distant lands."
    },
    561: {
        "word": "Expatiate",
        "english_meaning": "speak or write at length or in detail",
        "urdu_meaning": "تفصیل سے گفتگو کرنا",
        "primary_meaning": "elaborate",
        "secondary_meaning": "expand",
        "tertiary_meaning": "dilate",
        "sentence": "The professor would often expatiate on the nuances of the historical events."
    },
    562: {
        "word": "Expedient",
        "english_meaning": "convenient and practical, although possibly improper or immoral",
        "urdu_meaning": "مناسب",
        "primary_meaning": "advantageous",
        "secondary_meaning": "practical",
        "tertiary_meaning": "conducive",
        "sentence": "In certain situations, telling a white lie may be seen as an expedient solution."
    },
    563: {
        "word": "Expedite",
        "english_meaning": "make (an action or process) happen sooner or be accomplished more quickly",
        "urdu_meaning": "فوراً کرنا",
        "primary_meaning": "accelerate",
        "secondary_meaning": "hasten",
        "tertiary_meaning": "facilitate",
        "sentence": "The manager promised to expedite the approval process for the urgent project."
    },
    564: {
        "word": "Explicate",
        "english_meaning": "analyze and develop (a principle, theory, or idea) in detail",
        "urdu_meaning": "تفصیل سے سمجھانا",
        "primary_meaning": "explain",
        "secondary_meaning": "clarify",
        "tertiary_meaning": "elaborate",
        "sentence": "The professor took the time to explicate the key concepts of the philosophical theory."
    },
    565: {
        "word": "Explicit",
        "english_meaning": "stated clearly and in detail, leaving no room for confusion or doubt",
        "urdu_meaning": "صریح",
        "primary_meaning": "clear",
        "secondary_meaning": "unambiguous",
        "tertiary_meaning": "precise",
        "sentence": "The contract included explicit terms outlining the responsibilities of each party involved."
    },
    566: {
        "word": "Exploit",
        "english_meaning": "make full use of and derive benefit from (a resource)",
        "urdu_meaning": "فائدہ اٹھانا",
        "primary_meaning": "utilize",
        "secondary_meaning": "take advantage of",
        "tertiary_meaning": "capitalize on",
        "sentence": "The company sought to exploit new technologies to enhance its productivity."
    },
    567: {
        "word": "Exposition",
        "english_meaning": "a comprehensive description and explanation of an idea or theory",
        "urdu_meaning": "تشہیر",
        "primary_meaning": "presentation",
        "secondary_meaning": "elaboration",
        "tertiary_meaning": "explanation",
        "sentence": "The professor delivered an exposition on the principles of quantum mechanics."
    },
    568: {
        "word": "Extant",
        "english_meaning": "still in existence; surviving",
        "urdu_meaning": "موجودہ",
        "primary_meaning": "existing",
        "secondary_meaning": "surviving",
        "tertiary_meaning": "current",
        "sentence": "Despite its age, the ancient manuscript is still extant and available for study."
    },
    569: {
        "word": "Extempore",
        "english_meaning": "spoken or done without preparation",
        "urdu_meaning": "بلا تیاری کے",
        "primary_meaning": "impromptu",
        "secondary_meaning": "unrehearsed",
        "tertiary_meaning": "off-the-cuff",
        "sentence": "The speaker delivered an extempore speech, responding to questions on the spot."
    },
    570: {
        "word": "Extenuating",
        "english_meaning": "making guilt or an offense seem less serious or more forgivable",
        "urdu_meaning": "تخفیفی",
        "primary_meaning": "mitigating",
        "secondary_meaning": "diminishing",
        "tertiary_meaning": "justifying",
        "sentence": "The defendant argued that there were extenuating circumstances that should be considered in the sentencing."
    },
    571: {
        "word": "Extol",
        "english_meaning": "praise enthusiastically",
        "urdu_meaning": "حمد و ثنا کرنا",
        "primary_meaning": "praise",
        "secondary_meaning": "commend",
        "tertiary_meaning": "acclaim",
        "sentence": "The teacher would often extol the virtues of hard work and dedication to the students."
    },
    572: {
        "word": "Extraneous",
        "english_meaning": "irrelevant or unrelated to the subject being dealt with",
        "urdu_meaning": "غیر متعلق",
        "primary_meaning": "irrelevant",
        "secondary_meaning": "unnecessary",
        "tertiary_meaning": "extrinsic",
        "sentence": "The professor asked the students to focus on the relevant information and avoid including extraneous details."
    },
    573: {
        "word": "Extrapolate",
        "english_meaning": "extend the application of (a method or conclusion) to an unknown situation by assuming that existing trends will continue",
        "urdu_meaning": "توسیع کرنا",
        "primary_meaning": "project",
        "secondary_meaning": "estimate",
        "tertiary_meaning": "infer",
        "sentence": "Based on current data, the analyst attempted to extrapolate future trends in the market."
    },
    574: {
        "word": "Extravagant",
        "english_meaning": "lacking restraint in spending money or using resources",
        "urdu_meaning": "ضائع خرچ",
        "primary_meaning": "lavish",
        "secondary_meaning": "excessive",
        "tertiary_meaning": "prodigal",
        "sentence": "The wedding featured an extravagant display of flowers, decorations, and gourmet food."
    },
    575: {
        "word": "Fabricate",
        "english_meaning": "invent or concoct (something), typically with deceitful intent",
        "urdu_meaning": "جعلی بنانا",
        "primary_meaning": "forge",
        "secondary_meaning": "manufacture",
        "tertiary_meaning": "falsify",
        "sentence": "The witness was caught attempting to fabricate a false alibi for the accused."
    },
    576: {
        "word": "Facetious",
        "english_meaning": "treating serious issues with deliberately inappropriate humor",
        "urdu_meaning": "ظاہری طور پر مسکرانے والا",
        "primary_meaning": "humorous",
        "secondary_meaning": "jocular",
        "tertiary_meaning": "witty",
        "sentence": "His facetious remarks during the meeting were met with stern looks from his colleagues."
    },
    577: {
        "word": "Factious",
        "english_meaning": "involving or inclined to causing disagreement or dissension within a group",
        "urdu_meaning": "گروہوں میں اختلافات پیدا کرنے والا",
        "primary_meaning": "divisive",
        "secondary_meaning": "contentious",
        "tertiary_meaning": "discordant",
        "sentence": "The political party became factious, with internal disputes leading to a split among its members."
    },
    578: {
        "word": "Factual",
        "english_meaning": "concerned with what is actually the case rather than interpretations of or reactions to it",
        "urdu_meaning": "حقیقی",
        "primary_meaning": "true",
        "secondary_meaning": "accurate",
        "tertiary_meaning": "objective",
        "sentence": "The journalist was praised for providing a factual and unbiased report on the incident."
    },
    579: {
        "word": "Fallacious",
        "english_meaning": "based on a mistaken belief",
        "urdu_meaning": "غلط فہمی پر مبنی",
        "primary_meaning": "misleading",
        "secondary_meaning": "deceptive",
        "tertiary_meaning": "erroneous",
        "sentence": "The argument presented by the speaker was fallacious, as it relied on incorrect data."
    },
    580: {
        "word": "Fallible",
        "english_meaning": "capable of making mistakes or being erroneous",
        "urdu_meaning": "غلطی پذیر",
        "primary_meaning": "error-prone",
        "secondary_meaning": "imperfect",
        "tertiary_meaning": "faulty",
        "sentence": "Being fallible, humans are prone to errors in judgment and decision-making."
    },
    581: {
        "word": "Fallow",
        "english_meaning": "(of farmland) plowed and harrowed but left unsown for a period to restore its fertility",
        "urdu_meaning": "خالی",
        "primary_meaning": "uncultivated",
        "secondary_meaning": "unproductive",
        "tertiary_meaning": "idle",
        "sentence": "The farmer allowed the field to remain fallow for a season to rejuvenate the soil."
    },
    582: {
        "word": "Falter",
        "english_meaning": "lose strength or momentum",
        "urdu_meaning": "ڈگمگانا",
        "primary_meaning": "hesitate",
        "secondary_meaning": "stumble",
        "tertiary_meaning": "waver",
        "sentence": "The singer's voice began to falter as he reached the high notes of the song."
    },
    583: {
        "word": "Fanciful",
        "english_meaning": "existing only in the imagination or fancy",
        "urdu_meaning": "خیالی",
        "primary_meaning": "imaginative",
        "secondary_meaning": "whimsical",
        "tertiary_meaning": "fantastic",
        "sentence": "The artist's painting depicted a fanciful world filled with magical creatures and surreal landscapes."
    },
    584: {
        "word": "Farsighted",
        "english_meaning": "able to see or plan for the future with wise judgment",
        "urdu_meaning": "دور اندیش",
        "primary_meaning": "forward-thinking",
        "secondary_meaning": "visionary",
        "tertiary_meaning": "prescient",
        "sentence": "The farsighted entrepreneur anticipated market trends and made strategic investments."
    },
    585: {
        "word": "Fascinate",
        "english_meaning": "draw irresistibly the attention and interest of (someone)",
        "urdu_meaning": "دلبھا لینا",
        "primary_meaning": "captivate",
        "secondary_meaning": "enchant",
        "tertiary_meaning": "bewitch",
        "sentence": "The mysterious story fascinated readers, keeping them glued to the pages until the end."
    },
    586: {
        "word": "Fastidious",
        "english_meaning": "very attentive to and concerned about accuracy and detail",
        "urdu_meaning": "نازک",
        "primary_meaning": "meticulous",
        "secondary_meaning": "precise",
        "tertiary_meaning": "perfectionist",
        "sentence": "The chef was known for his fastidious attention to the presentation and flavor of every dish."
    },
    587: {
        "word": "Fawn",
        "english_meaning": "showing excessive affection or admiration",
        "urdu_meaning": "چاپلوسی کرنا",
        "primary_meaning": "flatter",
        "secondary_meaning": "adulate",
        "tertiary_meaning": "grovel",
        "sentence": "The employee fawned over the boss, hoping to gain favor and promotions."
    },
    588: {
        "word": "Feasible",
        "english_meaning": "possible to do easily or conveniently",
        "urdu_meaning": "ممکن",
        "primary_meaning": "achievable",
        "secondary_meaning": "practical",
        "tertiary_meaning": "viable",
        "sentence": "After careful analysis, the team concluded that the proposed project was feasible within the given time and budget."
    },
    589: {
        "word": "Feckless",
        "english_meaning": "lacking initiative or strength of character",
        "urdu_meaning": "کاہل",
        "primary_meaning": "irresponsible",
        "secondary_meaning": "ineffective",
        "tertiary_meaning": "indolent",
        "sentence": "His feckless approach to work led to missed deadlines and incomplete tasks."
    },
    590: {
        "word": "Fecund",
        "english_meaning": "capable of producing offspring or fruit in large quantities",
        "urdu_meaning": "پیداواری",
        "primary_meaning": "fertile",
        "secondary_meaning": "productive",
        "tertiary_meaning": "fruitful",
        "sentence": "The lush and fecund land was ideal for agriculture, yielding bountiful crops."
    },
    591: {
        "word": "Feeble",
        "english_meaning": "lacking physical strength, especially as a result of age or illness",
        "urdu_meaning": "کمزور",
        "primary_meaning": "weak",
        "secondary_meaning": "frail",
        "tertiary_meaning": "debilitated",
        "sentence": "The old man's feeble attempt to lift the heavy box showed his diminished strength."
    },
    592: {
        "word": "Feign",
        "english_meaning": "pretend to be affected by (a feeling, state, or injury)",
        "urdu_meaning": "جھوٹ بولنا",
        "primary_meaning": "fake",
        "secondary_meaning": "simulate",
        "tertiary_meaning": "dissemble",
        "sentence": "She tried to feign indifference, but her eyes betrayed her true emotions."
    },
    593: {
        "word": "Feint",
        "english_meaning": "a deceptive or pretended blow, thrust, or other movement, especially in boxing or fencing",
        "urdu_meaning": "چکمہ",
        "primary_meaning": "pretense",
        "secondary_meaning": "deception",
        "tertiary_meaning": "maneuver",
        "sentence": "The boxer used a clever feint to distract his opponent before delivering a powerful punch."
    },
    594: {
        "word": "Felicitous",
        "english_meaning": "well-suited for the occasion, pleasing and fortunate",
        "urdu_meaning": "مناسب",
        "primary_meaning": "appropriate",
        "secondary_meaning": "apt",
        "tertiary_meaning": "happy",
        "sentence": "His felicitous choice of words added charm to the speech and delighted the audience."
    },
    595: {
        "word": "Fervent",
        "english_meaning": "having or displaying a passionate intensity",
        "urdu_meaning": "جذباتی",
        "primary_meaning": "enthusiastic",
        "secondary_meaning": "zealous",
        "tertiary_meaning": "ardent",
        "sentence": "The fervent supporters cheered loudly, showing unwavering devotion to their team."
    },
    596: {
        "word": "Fervid",
        "english_meaning": "intensely enthusiastic or passionate, especially in relation to beliefs or feelings",
        "urdu_meaning": "جذباتی",
        "primary_meaning": "zealous",
        "secondary_meaning": "ardent",
        "tertiary_meaning": "fervent",
        "sentence": "His fervid speech inspired the audience to take action for a noble cause."
    },
    597: {
        "word": "Fervor",
        "english_meaning": "intense and passionate feeling",
        "urdu_meaning": "جذبہ",
        "primary_meaning": "enthusiasm",
        "secondary_meaning": "zeal",
        "tertiary_meaning": "ardor",
        "sentence": "The crowd erupted in fervor as the team scored the winning goal in the final minutes of the match."
    },
    598: {
        "word": "Fester",
        "english_meaning": "become worse or more intense, typically due to long-term neglect or indifference",
        "urdu_meaning": "شدت بڑھنا",
        "primary_meaning": "deteriorate",
        "secondary_meaning": "worsen",
        "tertiary_meaning": "decay",
        "sentence": "The unresolved issues began to fester, causing tension and conflicts within the team."
    },
    599: {
        "word": "Fickle",
        "english_meaning": "changing frequently, especially in regards to one's loyalties, interests, or affections",
        "urdu_meaning": "چپچپا",
        "primary_meaning": "capricious",
        "secondary_meaning": "volatile",
        "tertiary_meaning": "unpredictable",
        "sentence": "Her fickle nature made it challenging to predict her preferences or decisions."
    },
    600: {
        "word": "Figurative",
        "english_meaning": "departing from a literal use of words; metaphorical",
        "urdu_meaning": "مجازی",
        "primary_meaning": "symbolic",
        "secondary_meaning": "metaphorical",
        "tertiary_meaning": "non-literal",
        "sentence": "The poet often employed figurative language to convey deeper meanings in his verses."
    },
    601: {
        "word": "Finicky",
        "english_meaning": "excessively concerned about details or minor faults",
        "urdu_meaning": "زیادہ خصوصیاتی",
        "primary_meaning": "fussy",
        "secondary_meaning": "particular",
        "tertiary_meaning": "meticulous",
        "sentence": "The chef was known for being finicky about the freshness and quality of ingredients used in his recipes."
    },
    602: {
        "word": "Fitfully",
        "english_meaning": "occurring in irregular or sporadic bursts",
        "urdu_meaning": "تکرار سے",
        "primary_meaning": "spasmodic",
        "secondary_meaning": "intermittent",
        "tertiary_meaning": "erratic",
        "sentence": "The wind blew fitfully, causing the leaves to rustle in sporadic patterns."
    },
    603: {
        "word": "Fixate",
        "english_meaning": "cause to be arrested or focused in one direction",
        "urdu_meaning": "مرکوز ہونا",
        "primary_meaning": "concentrate",
        "secondary_meaning": "obsess",
        "tertiary_meaning": "fix",
        "sentence": "She tended to fixate on small details, often losing sight of the bigger picture."
    },
    604: {
        "word": "Flagrant",
        "english_meaning": "clearly offensive or bad; conspicuously noticeable",
        "urdu_meaning": "نمایاں",
        "primary_meaning": "blatant",
        "secondary_meaning": "egregious",
        "tertiary_meaning": "outrageous",
        "sentence": "The player committed a flagrant foul, resulting in a penalty and the disapproval of the referee."
    },
    605: {
        "word": "Flamboyant",
        "english_meaning": "bright, colorful, and highly elaborate, especially in a way that attracts attention",
        "urdu_meaning": "چمکیلا",
        "primary_meaning": "vibrant",
        "secondary_meaning": "ostentatious",
        "tertiary_meaning": "showy",
        "sentence": "The fashion designer was known for his flamboyant and extravagant runway creations."
    },
    606: {
        "word": "Flattery",
        "english_meaning": "excessive and insincere praise, especially to gain favor or advantage",
        "urdu_meaning": "خوشامد",
        "primary_meaning": "adulation",
        "secondary_meaning": "compliment",
        "tertiary_meaning": "sycophancy",
        "sentence": "She saw through the flattery and recognized it as an attempt to win her approval."
    },
    607: {
        "word": "Fledgling",
        "english_meaning": "a person or organization that is immature, inexperienced, or underdeveloped",
        "urdu_meaning": "نوپانوا",
        "primary_meaning": "novice",
        "secondary_meaning": "beginner",
        "tertiary_meaning": "rookie",
        "sentence": "The fledgling company faced challenges but showed great potential for growth in the future."
    },
    608: {
        "word": "Fleeting",
        "english_meaning": "lasting for a very short time; transient",
        "urdu_meaning": "عارضی",
        "primary_meaning": "transitory",
        "secondary_meaning": "momentary",
        "tertiary_meaning": "ephemeral",
        "sentence": "Their encounter was fleeting, as they only had a brief moment to exchange greetings."
    },
    609: {
        "word": "Florid",
        "english_meaning": "elaborately or excessively intricate or complicated",
        "urdu_meaning": "خوبصورت",
        "primary_meaning": "ornate",
        "secondary_meaning": "flowery",
        "tertiary_meaning": "overdecorated",
        "sentence": "The Victorian-style furniture was known for its florid designs and intricate carvings."
    },
    610: {
        "word": "Flourish",
        "english_meaning": "grow or develop in a healthy or vigorous way",
        "urdu_meaning": "ترقی کرنا",
        "primary_meaning": "thrive",
        "secondary_meaning": "prosper",
        "tertiary_meaning": "blossom",
        "sentence": "The business began to flourish after implementing strategic changes and expanding its customer base."
    },
    611: {
        "word": "Flout",
        "english_meaning": "openly disregard a rule, law, or convention",
        "urdu_meaning": "ناقابل قبول ٹھکرانا",
        "primary_meaning": "defy",
        "secondary_meaning": "disregard",
        "tertiary_meaning": "violate",
        "sentence": "Some drivers tend to flout traffic regulations, putting themselves and others at risk."
    },
    612: {
        "word": "Flummoxed",
        "english_meaning": "bewildered or perplexed",
        "urdu_meaning": "حیران ہونا",
        "primary_meaning": "confused",
        "secondary_meaning": "baffled",
        "tertiary_meaning": "puzzled",
        "sentence": "The complex instructions left him flummoxed, unsure of how to proceed."
    },
    613: {
        "word": "Fluster",
        "english_meaning": "make (someone) confused or agitated",
        "urdu_meaning": "پریشان کرنا",
        "primary_meaning": "disconcert",
        "secondary_meaning": "rattle",
        "tertiary_meaning": "unsettle",
        "sentence": "The unexpected question seemed to fluster the usually composed speaker."
    },
    614: {
        "word": "Flustered",
        "english_meaning": "agitated or confused",
        "urdu_meaning": "پریشان",
        "primary_meaning": "disturbed",
        "secondary_meaning": "perturbed",
        "tertiary_meaning": "flurried",
        "sentence": "She appeared flustered by the sudden turn of events, struggling to regain her composure."
    },
    615: {
        "word": "Foil",
        "english_meaning": "prevent (something considered wrong or undesirable) from succeeding",
        "urdu_meaning": "ناکام بنانا",
        "primary_meaning": "thwart",
        "secondary_meaning": "frustrate",
        "tertiary_meaning": "counter",
        "sentence": "The detective worked tirelessly to foil the criminal's plan and bring him to justice."
    },
    616: {
        "word": "Foment",
        "english_meaning": "instigate or stir up (an undesirable or violent sentiment or course of action)",
        "urdu_meaning": "شورش ڈالنا",
        "primary_meaning": "incite",
        "secondary_meaning": "provoke",
        "tertiary_meaning": "stimulate",
        "sentence": "The inflammatory speech had the potential to foment unrest and conflict among the population."
    },
    617: {
        "word": "Foolhardy",
        "english_meaning": "recklessly bold or rash",
        "urdu_meaning": "بے خود",
        "primary_meaning": "reckless",
        "secondary_meaning": "brash",
        "tertiary_meaning": "daring",
        "sentence": "Attempting to climb the steep cliff without safety gear was a foolhardy decision."
    },
    618: {
        "word": "Forbear",
        "english_meaning": "refrain from doing or using (something); withhold",
        "urdu_meaning": "صبر",
        "primary_meaning": "abstain",
        "secondary_meaning": "refrain",
        "tertiary_meaning": "hold back",
        "sentence": "In moments of anger, it is wise to forbear from making hasty decisions or statements."
    },
    619: {
        "word": "Forebode",
        "english_meaning": "be a warning or indication of (a future event)",
        "urdu_meaning": "پیشگوئی",
        "primary_meaning": "predict",
        "secondary_meaning": "foretell",
        "tertiary_meaning": "portend",
        "sentence": "The dark clouds seemed to forebode an approaching storm, prompting people to take cover."
    },
    620: {
        "word": "Foreground",
        "english_meaning": "the part of a scene or image that is nearest to and in front of the viewer",
        "urdu_meaning": "اہم حصہ",
        "primary_meaning": "front",
        "secondary_meaning": "center",
        "tertiary_meaning": "highlight",
        "sentence": "The artist skillfully placed the main characters in the foreground, capturing the viewer's attention."
    },
    621: {
        "word": "Foreseeable",
        "english_meaning": "able to be foreseen or predicted",
        "urdu_meaning": "پیش گوئی ہو سکنے والا",
        "primary_meaning": "predictable",
        "secondary_meaning": "anticipated",
        "tertiary_meaning": "expected",
        "sentence": "The consequences of the decision were foreseeable, but they were still chosen for short-term gains."
    },
    622: {
        "word": "Foresight",
        "english_meaning": "the ability to predict or the action of predicting what will happen or be needed in the future",
        "urdu_meaning": "پیشنگوئی",
        "primary_meaning": "foresightedness",
        "secondary_meaning": "forethought",
        "tertiary_meaning": "anticipation",
        "sentence": "The success of a business often depends on the foresight of its leaders in anticipating market trends."
    },
    623: {
        "word": "Forestall",
        "english_meaning": "prevent or obstruct (an anticipated event or action) by taking action ahead of time",
        "urdu_meaning": "روکنا",
        "primary_meaning": "preclude",
        "secondary_meaning": "hinder",
        "tertiary_meaning": "anticipate",
        "sentence": "The company implemented new security measures to forestall any potential cyber threats."
    },
    624: {
        "word": "Forgery",
        "english_meaning": "the action of forging or producing a copy of a document, signature, banknote, or work of art",
        "urdu_meaning": "جعلی",
        "primary_meaning": "counterfeiting",
        "secondary_meaning": "imitation",
        "tertiary_meaning": "fraud",
        "sentence": "The detective discovered a forgery when comparing the fake painting to the artist's original."
    },
    625: {
        "word": "Forgo",
        "english_meaning": "omit or decline to take (something pleasant or valuable)",
        "urdu_meaning": "چھوڑنا",
        "primary_meaning": "renounce",
        "secondary_meaning": "abstain",
        "tertiary_meaning": "sacrifice",
        "sentence": "In an effort to save money, she decided to forgo her annual vacation."
    },
    626: {
        "word": "Forsake",
        "english_meaning": "abandon or leave behind",
        "urdu_meaning": "ترک کرنا",
        "primary_meaning": "desert",
        "secondary_meaning": "abandon",
        "tertiary_meaning": "renounce",
        "sentence": "Despite the challenges, he vowed never to forsake his principles."
    },
    627: {
        "word": "Fortitude",
        "english_meaning": "courage in pain or adversity",
        "urdu_meaning": "صبر",
        "primary_meaning": "resilience",
        "secondary_meaning": "bravery",
        "tertiary_meaning": "endurance",
        "sentence": "Her fortitude in the face of adversity inspired those around her."
    },
    628: {
        "word": "Fortuitous",
        "english_meaning": "happening by chance rather than intention",
        "urdu_meaning": "اچانکی",
        "primary_meaning": "serendipitous",
        "secondary_meaning": "unexpected",
        "tertiary_meaning": "fortunate",
        "sentence": "Their meeting at the coffee shop was fortuitous, leading to a lifelong friendship."
    },
    629: {
        "word": "Foster",
        "english_meaning": "encourage the development of (something, especially something desirable)",
        "urdu_meaning": "برابری دینا",
        "primary_meaning": "promote",
        "secondary_meaning": "cultivate",
        "tertiary_meaning": "nurture",
        "sentence": "The organization works to foster creativity and innovation in young artists."
    },
    630: {
        "word": "Fractious",
        "english_meaning": "irritable and quarrelsome",
        "urdu_meaning": "جھگڑالو",
        "primary_meaning": "quarrelsome",
        "secondary_meaning": "contentious",
        "tertiary_meaning": "disputatious",
        "sentence": "The fractious atmosphere in the meeting made it difficult to reach any agreements."
    },
    631: {
        "word": "Frailty",
        "english_meaning": "the condition of being weak and delicate",
        "urdu_meaning": "کمزوری",
        "primary_meaning": "weakness",
        "secondary_meaning": "fragility",
        "tertiary_meaning": "delicacy",
        "sentence": "The elderly woman's frailty required gentle care and attention."
    },
    632: {
        "word": "Fraught",
        "english_meaning": "filled with or likely to result in (something undesirable)",
        "urdu_meaning": "بھرا ہوا",
        "primary_meaning": "laden",
        "secondary_meaning": "charged",
        "tertiary_meaning": "full of",
        "sentence": "The negotiations were fraught with tension and disagreement."
    },
    633: {
        "word": "Frenetic",
        "english_meaning": "fast and energetic in a rather wild and uncontrolled way",
        "urdu_meaning": "پر شور",
        "primary_meaning": "frantic",
        "secondary_meaning": "hectic",
        "tertiary_meaning": "feverish",
        "sentence": "In the final minutes of the game, the players displayed frenetic energy, trying to score the winning goal."
    },
    634: {
        "word": "Fret",
        "english_meaning": "be constantly or visibly worried or anxious",
        "urdu_meaning": "پریشان ہونا",
        "primary_meaning": "worry",
        "secondary_meaning": "agitate",
        "tertiary_meaning": "distress",
        "sentence": "She would often fret about the smallest details, unable to relax."
    },
    635: {
        "word": "Fringe",
        "english_meaning": "an ornamental border of threads left loose or formed into tassels or twists, used to edge clothing or material",
        "urdu_meaning": "سرحد",
        "primary_meaning": "edging",
        "secondary_meaning": "border",
        "tertiary_meaning": "trim",
        "sentence": "The dress was adorned with a fringe that added a touch of elegance to its design."
    },
    636: {
        "word": "Frivolous",
        "english_meaning": "not having any serious purpose or value",
        "urdu_meaning": "بیہودہ",
        "primary_meaning": "trivial",
        "secondary_meaning": "superficial",
        "tertiary_meaning": "frivolous",
        "sentence": "She was criticized for spending too much time on frivolous activities instead of focusing on her responsibilities."
    },
    637: {
        "word": "Frugality",
        "english_meaning": "the quality of being economical with money or food",
        "urdu_meaning": "معقولیت",
        "primary_meaning": "thrift",
        "secondary_meaning": "economy",
        "tertiary_meaning": "frugalness",
        "sentence": "His frugality allowed him to save money for future investments."
    },
    638: {
        "word": "Fruitful",
        "english_meaning": "producing good or helpful results",
        "urdu_meaning": "پیداواری",
        "primary_meaning": "productive",
        "secondary_meaning": "beneficial",
        "tertiary_meaning": "successful",
        "sentence": "The collaboration between the two teams proved to be a fruitful endeavor, leading to significant advancements."
    },
    639: {
        "word": "Fulcrum",
        "english_meaning": "the point on which a lever rests or is supported and on which it pivots",
        "urdu_meaning": "سہارا",
        "primary_meaning": "pivot",
        "secondary_meaning": "support",
        "tertiary_meaning": "point of support",
        "sentence": "In a lever system, the fulcrum plays a crucial role in enabling the movement of the lever."
    },
    640: {
        "word": "Fungible",
        "english_meaning": "replaceable by another identical item, mutually interchangeable",
        "urdu_meaning": "قابل تبادلہ",
        "primary_meaning": "interchangeable",
        "secondary_meaning": "substitutable",
        "tertiary_meaning": "replaceable",
        "sentence": "Money is often considered fungible because each unit is equivalent and can be exchanged for another."
    },
    641: {
        "word": "Furtive",
        "english_meaning": "attempting to avoid notice or attention, typically because of guilt or a belief that discovery would lead to trouble",
        "urdu_meaning": "خفیہ",
        "primary_meaning": "secretive",
        "secondary_meaning": "sneaky",
        "tertiary_meaning": "clandestine",
        "sentence": "He cast a furtive glance around the room before slipping out unnoticed."
    },
    642: {
        "word": "Fusion",
        "english_meaning": "the process or result of joining two or more things together to form a single entity",
        "urdu_meaning": "ملاپ",
        "primary_meaning": "merger",
        "secondary_meaning": "blending",
        "tertiary_meaning": "integration",
        "sentence": "The fusion of different musical styles resulted in a unique and innovative sound."
    },
    643: {
        "word": "Futile",
        "english_meaning": "incapable of producing any useful result, pointless",
        "urdu_meaning": "بے فائدہ",
        "primary_meaning": "fruitless",
        "secondary_meaning": "unsuccessful",
        "tertiary_meaning": "vain",
        "sentence": "Despite their efforts, the attempt to repair the old machine proved futile."
    },
    644: {
        "word": "Gaffe",
        "english_meaning": "an unintentional act or remark causing embarrassment to its originator",
        "urdu_meaning": "غفلت",
        "primary_meaning": "blunder",
        "secondary_meaning": "faux pas",
        "tertiary_meaning": "mistake",
        "sentence": "His accidental use of the wrong name was a social gaffe that left everyone in the room awkwardly silent."
    },
    645: {
        "word": "Gainsay",
        "english_meaning": "deny or contradict a fact or statement",
        "urdu_meaning": "تردید کرنا",
        "primary_meaning": "contradict",
        "secondary_meaning": "oppose",
        "tertiary_meaning": "dispute",
        "sentence": "It is difficult to gainsay the scientific evidence supporting the theory of climate change."
    },
    646: {
        "word": "Galvanize",
        "english_meaning": "shock or excite (someone), typically into taking action",
        "urdu_meaning": "متحرک کرنا",
        "primary_meaning": "stimulate",
        "secondary_meaning": "motivate",
        "tertiary_meaning": "inspire",
        "sentence": "The inspiring speech was meant to galvanize the audience to contribute to the community project."
    },
    647: {
        "word": "Games",
        "english_meaning": "wild mammals or birds hunted for sport or food",
        "urdu_meaning": "شکار",
        "primary_meaning": "wild game",
        "secondary_meaning": "hunted animals",
        "tertiary_meaning": "prey",
        "sentence": "The indigenous people relied on hunting for games as a traditional source of food."
    },
    648: {
        "word": "Garrulous",
        "english_meaning": "excessively talkative, especially on trivial matters",
        "urdu_meaning": "بکواسی",
        "primary_meaning": "chatty",
        "secondary_meaning": "talkative",
        "tertiary_meaning": "loquacious",
        "sentence": "The garrulous neighbor would talk for hours about various topics, making it challenging to have a brief conversation."
    },
    649: {
        "word": "Gauche",
        "english_meaning": "lacking social grace, sensitivity, or acuteness; awkward; tactless",
        "urdu_meaning": "بے ہوش",
        "primary_meaning": "awkward",
        "secondary_meaning": "unrefined",
        "tertiary_meaning": "clumsy",
        "sentence": "His gauche attempt at small talk only made the situation more uncomfortable."
    },
    650: {
        "word": "Gawky",
        "english_meaning": "awkward and clumsy in one's movements or manner",
        "urdu_meaning": "بے ہوش",
        "primary_meaning": "ungainly",
        "secondary_meaning": "clumsy",
        "tertiary_meaning": "awkward",
        "sentence": "As a teenager, he was gawky and often stumbled over his own feet."
    },
    651: {
        "word": "Genealogy",
        "english_meaning": "a line of descent traced continuously from an ancestor",
        "urdu_meaning": "آباؤ آجد",
        "primary_meaning": "ancestry",
        "secondary_meaning": "family tree",
        "tertiary_meaning": "lineage",
        "sentence": "She researched her genealogy and discovered interesting stories about her ancestors."
    },
    652: {
        "word": "Germane",
        "english_meaning": "relevant to a subject under consideration",
        "urdu_meaning": "موزوں",
        "primary_meaning": "pertinent",
        "secondary_meaning": "related",
        "tertiary_meaning": "applicable",
        "sentence": "Please keep your comments germane to the topic of discussion."
    },
    653: {
        "word": "Giddily",
        "english_meaning": "in a light-headed or dizzy manner",
        "urdu_meaning": "چکرا کے ساتھ",
        "primary_meaning": "dizzily",
        "secondary_meaning": "spinning",
        "tertiary_meaning": "vertiginously",
        "sentence": "After the roller coaster ride, she stumbled off the platform, feeling giddily disoriented."
    },
    654: {
        "word": "Glib",
        "english_meaning": "fluent and voluble but insincere and shallow",
        "urdu_meaning": "فریبی",
        "primary_meaning": "slick",
        "secondary_meaning": "smooth-talking",
        "tertiary_meaning": "superficial",
        "sentence": "The politician's glib responses failed to address the real issues raised by the journalist."
    },
    655: {
        "word": "Gloat",
        "english_meaning": "contemplate or dwell on one's success or another's misfortune with smugness or malignant pleasure",
        "urdu_meaning": "خوش ہونا",
        "primary_meaning": "revel",
        "secondary_meaning": "boast",
        "tertiary_meaning": "smirk",
        "sentence": "He couldn't help but gloat over his rival's failure, even though he pretended to sympathize."
    },
    656: {
        "word": "Global",
        "english_meaning": "relating to the whole world; worldwide",
        "urdu_meaning": "عالمی",
        "primary_meaning": "international",
        "secondary_meaning": "universal",
        "tertiary_meaning": "worldwide",
        "sentence": "The company has a global presence, with offices in major cities around the world."
    },
    657: {
        "word": "Gloom",
        "english_meaning": "partial or total darkness; a state of depression or despondency",
        "urdu_meaning": "تاریکی",
        "primary_meaning": "darkness",
        "secondary_meaning": "melancholy",
        "tertiary_meaning": "despair",
        "sentence": "The room was filled with gloom as the sun set, casting long shadows."
    },
    658: {
        "word": "Glorification",
        "english_meaning": "the action of describing or representing something as admirable, especially unjustifiably",
        "urdu_meaning": "تعریف",
        "primary_meaning": "praise",
        "secondary_meaning": "adulation",
        "tertiary_meaning": "eulogy",
        "sentence": "The movie's glorification of violence was criticized for its negative impact on viewers."
    },
    659: {
        "word": "Glum",
        "english_meaning": "looking or feeling dejected; gloomy",
        "urdu_meaning": "افسردہ",
        "primary_meaning": "downcast",
        "secondary_meaning": "morose",
        "tertiary_meaning": "dismal",
        "sentence": "After receiving the bad news, he sat in a glum silence, contemplating what to do next."
    },
    660: {
        "word": "Goad",
        "english_meaning": "provoke or annoy (someone) so as to stimulate some action or reaction",
        "urdu_meaning": "ترغیب دینا",
        "primary_meaning": "prod",
        "secondary_meaning": "irritate",
        "tertiary_meaning": "incite",
        "sentence": "The teasing remarks served to goad him into responding with more determination."
    },
    661: {
        "word": "Goosebumps",
        "english_meaning": "small, raised bumps on the skin caused by cold, excitement, or fear",
        "urdu_meaning": "کھچک",
        "primary_meaning": "piloerection",
        "secondary_meaning": "chill bumps",
        "tertiary_meaning": "horripilation",
        "sentence": "The eerie sound gave her goosebumps, making her shiver involuntarily."
    },
    662: {
        "word": "Gracious",
        "english_meaning": "courteous, kind, and pleasant, especially towards others",
        "urdu_meaning": "شریف",
        "primary_meaning": "courteous",
        "secondary_meaning": "kind",
        "tertiary_meaning": "polite",
        "sentence": "Despite facing criticism, she remained gracious and composed in her response."
    },
    663: {
        "word": "Gratify",
        "english_meaning": "give (someone) pleasure or satisfaction",
        "urdu_meaning": "خوشی دینا",
        "primary_meaning": "satisfy",
        "secondary_meaning": "please",
        "tertiary_meaning": "fulfill",
        "sentence": "Her achievement was enough to gratify her parents and make them proud."
    },
    664: {
        "word": "Gratuitous",
        "english_meaning": "uncalled for; lacking good reason; unwarranted",
        "urdu_meaning": "بے جا کا",
        "primary_meaning": "unjustified",
        "secondary_meaning": "unnecessary",
        "tertiary_meaning": "unwarranted",
        "sentence": "The violence in the movie seemed gratuitous and added nothing to the plot."
    },
    665: {
        "word": "Gravity",
        "english_meaning": "the force that attracts a body towards the center of the earth, or towards any other physical body having mass",
        "urdu_meaning": "کشش ثقل",
        "primary_meaning": "weight",
        "secondary_meaning": "gravitational force",
        "tertiary_meaning": "seriousness",
        "sentence": "The apple fell from the tree due to the force of gravity."
    },
    666: {
        "word": "Gregarious",
        "english_meaning": "fond of company; sociable",
        "urdu_meaning": "سماجی",
        "primary_meaning": "social",
        "secondary_meaning": "friendly",
        "tertiary_meaning": "outgoing",
        "sentence": "She is a gregarious person who enjoys spending time with friends and meeting new people."
    },
    667: {
        "word": "Grievance",
        "english_meaning": "a real or imagined cause for complaint, especially unfair treatment",
        "urdu_meaning": "شکایت",
        "primary_meaning": "complaint",
        "secondary_meaning": "grievance",
        "tertiary_meaning": "objection",
        "sentence": "The employees submitted a formal grievance regarding the unfair working conditions."
    },
    668: {
        "word": "Grouchy",
        "english_meaning": "bad-tempered and irritable",
        "urdu_meaning": "غصے میں",
        "primary_meaning": "irritable",
        "secondary_meaning": "cranky",
        "tertiary_meaning": "grumpy",
        "sentence": "He's always grouchy in the morning before he has his coffee."
    },
    669: {
        "word": "Grovel",
        "english_meaning": "lie or move abjectly on the ground with one's face downward",
        "urdu_meaning": "زمین پر گرنا",
        "primary_meaning": "kowtow",
        "secondary_meaning": "prostrate",
        "tertiary_meaning": "crawl",
        "sentence": "He had to grovel and apologize after making a serious mistake at work."
    },
    670: {
        "word": "Grumble",
        "english_meaning": "complain or protest about something in a bad-tempered but typically muted way",
        "urdu_meaning": "شکایت کرنا",
        "primary_meaning": "complain",
        "secondary_meaning": "mutter",
        "tertiary_meaning": "murmur",
        "sentence": "The workers began to grumble about the long hours and low pay."
    },
    671: {
        "word": "Gullible",
        "english_meaning": "easily persuaded to believe something; credulous",
        "urdu_meaning": "سیدھا",
        "primary_meaning": "naive",
        "secondary_meaning": "credulous",
        "tertiary_meaning": "trustful",
        "sentence": "He was so gullible that he believed every wild story he heard."
    },
    672: {
        "word": "Hackneyed",
        "english_meaning": "lacking significance through having been overused; unoriginal and trite",
        "urdu_meaning": "پرانا",
        "primary_meaning": "clichéd",
        "secondary_meaning": "stale",
        "tertiary_meaning": "commonplace",
        "sentence": "The hackneyed phrases in the speech made it sound uninspired and clichéd."
    },
    673: {
        "word": "Hamper",
        "english_meaning": "hinder or impede the movement or progress of",
        "urdu_meaning": "رکاوٹ ڈالنا",
        "primary_meaning": "obstruct",
        "secondary_meaning": "hinder",
        "tertiary_meaning": "impede",
        "sentence": "The heavy traffic will hamper our journey, causing delays."
    },
    674: {
        "word": "Haphazard",
        "english_meaning": "lacking any obvious principle of organization; random",
        "urdu_meaning": "بے ترتیب",
        "primary_meaning": "random",
        "secondary_meaning": "chaotic",
        "tertiary_meaning": "unplanned",
        "sentence": "The arrangement of the items on the shelf seemed haphazard and disorganized."
    },
    675: {
        "word": "Hapless",
        "english_meaning": "unfortunate or unlucky",
        "urdu_meaning": "بدنصیب",
        "primary_meaning": "unfortunate",
        "secondary_meaning": "luckless",
        "tertiary_meaning": "miserable",
        "sentence": "The hapless traveler lost his way in the dense forest and couldn't find his way back."
    },
    676: {
        "word": "Harangue",
        "english_meaning": "a lengthy and aggressive speech",
        "urdu_meaning": "تنقیدی خطبہ",
        "primary_meaning": "diatribe",
        "secondary_meaning": "tirade",
        "tertiary_meaning": "rant",
        "sentence": "The politician delivered a harangue against corruption in the government."
    },
    677: {
        "word": "Harbinger",
        "english_meaning": "a person or thing that announces or signals the approach of another",
        "urdu_meaning": "پیشنگوئی",
        "primary_meaning": "omen",
        "secondary_meaning": "herald",
        "tertiary_meaning": "forewarning",
        "sentence": "The dark clouds were a harbinger of the impending storm."
    },
    678: {
        "word": "Harmonious",
        "english_meaning": "forming a harmonious or consistent whole",
        "urdu_meaning": "ہم آہنگ",
        "primary_meaning": "cohesive",
        "secondary_meaning": "unified",
        "tertiary_meaning": "balanced",
        "sentence": "The group achieved a harmonious blend of different musical instruments."
    },
    679: {
        "word": "Harrow",
        "english_meaning": "cause distress to",
        "urdu_meaning": "پریشان کرنا",
        "primary_meaning": "distress",
        "secondary_meaning": "torment",
        "tertiary_meaning": "plague",
        "sentence": "The tragic news continued to harrow the hearts of the grieving family."
    },
    680: {
        "word": "Haughty",
        "english_meaning": "arrogantly superior and disdainful",
        "urdu_meaning": "مغرور",
        "primary_meaning": "arrogant",
        "secondary_meaning": "proud",
        "tertiary_meaning": "snobbish",
        "sentence": "Her haughty attitude alienated many of her colleagues in the workplace."
    },
    681: {
        "word": "Headstrong",
        "english_meaning": "self-willed and obstinate",
        "urdu_meaning": "ہٹ میں",
        "primary_meaning": "stubborn",
        "secondary_meaning": "willful",
        "tertiary_meaning": "inflexible",
        "sentence": "The headstrong child insisted on doing things his own way, ignoring advice."
    },
    682: {
        "word": "Heady",
        "english_meaning": "having a strong or exhilarating effect",
        "urdu_meaning": "سرگرم کن",
        "primary_meaning": "intoxicating",
        "secondary_meaning": "exciting",
        "tertiary_meaning": "stimulating",
        "sentence": "The success of the project had a heady effect on the team, boosting morale."
    },
    683: {
        "word": "Heed",
        "english_meaning": "pay attention to; take notice of",
        "urdu_meaning": "توجہ دینا",
        "primary_meaning": "listen to",
        "secondary_meaning": "consider",
        "tertiary_meaning": "heed",
        "sentence": "It is wise to heed the advice of experienced mentors in your field."
    },
    684: {
        "word": "Herald",
        "english_meaning": "an official messenger bringing news",
        "urdu_meaning": "خبر لانے والا",
        "primary_meaning": "messenger",
        "secondary_meaning": "announcer",
        "tertiary_meaning": "proclaimer",
        "sentence": "The herald announced the arrival of the king to the cheering crowd."
    },
    685: {
        "word": "Heterodox",
        "english_meaning": "not conforming with established doctrine, especially in religious matters",
        "urdu_meaning": "غیر رسمی",
        "primary_meaning": "unorthodox",
        "secondary_meaning": "heretical",
        "tertiary_meaning": "nonconformist",
        "sentence": "His heterodox views on religion sparked controversy within the conservative community."
    },
    686: {
        "word": "Heterogeneous",
        "english_meaning": "diverse in character or content",
        "urdu_meaning": "مختلف قسم کا",
        "primary_meaning": "diverse",
        "secondary_meaning": "varied",
        "tertiary_meaning": "mixed",
        "sentence": "The class was a heterogeneous group, consisting of students with different backgrounds and interests."
    },
    687: {
        "word": "Hidebound",
        "english_meaning": "unwilling or unable to change because of tradition or convention",
        "urdu_meaning": "ضدی",
        "primary_meaning": "rigid",
        "secondary_meaning": "inflexible",
        "tertiary_meaning": "stubborn",
        "sentence": "The hidebound institution resisted modernization, clinging to outdated practices."
    },
    688: {
        "word": "Hinder",
        "english_meaning": "create difficulties for (someone or something), resulting in delay or obstruction",
        "urdu_meaning": "رکاوٹ ڈالنا",
        "primary_meaning": "impede",
        "secondary_meaning": "obstruct",
        "tertiary_meaning": "hamper",
        "sentence": "The lack of funds will hinder the progress of the construction project."
    },
    689: {
        "word": "Histrionic",
        "english_meaning": "overly theatrical or melodramatic in character or style",
        "urdu_meaning": "ڈرامہ باز",
        "primary_meaning": "theatrical",
        "secondary_meaning": "dramatic",
        "tertiary_meaning": "exaggerated",
        "sentence": "His histrionic performance drew mixed reviews from the critics."
    },
    690: {
        "word": "Hodgepodge",
        "english_meaning": "a confused mixture; jumble",
        "urdu_meaning": "آمیزش",
        "primary_meaning": "mixture",
        "secondary_meaning": "assortment",
        "tertiary_meaning": "medley",
        "sentence": "The dish was a hodgepodge of various ingredients, creating a unique and unexpected flavor."
    },
    691: {
        "word": "Homogeneous",
        "english_meaning": "of the same kind; alike",
        "urdu_meaning": "ہم جنس",
        "primary_meaning": "uniform",
        "secondary_meaning": "consistent",
        "tertiary_meaning": "similar",
        "sentence": "The classroom was homogeneous in its academic achievements, with all students excelling in their studies."
    },
    692: {
        "word": "Hortatory",
        "english_meaning": "encouraging; exhorting",
        "urdu_meaning": "ترغیبی",
        "primary_meaning": "admonishing",
        "secondary_meaning": "exhortative",
        "tertiary_meaning": "persuasive",
        "sentence": "The speaker delivered a hortatory speech, urging the audience to take positive action for change."
    },
    693: {
        "word": "Hospitable",
        "english_meaning": "friendly and welcoming to visitors or guests",
        "urdu_meaning": "مہمان نواز",
        "primary_meaning": "welcoming",
        "secondary_meaning": "friendly",
        "tertiary_meaning": "courteous",
        "sentence": "The host was hospitable, making sure every guest felt comfortable and at home."
    },
    694: {
        "word": "Humdrum",
        "english_meaning": "lacking excitement or variety; dull",
        "urdu_meaning": "کسل بخت",
        "primary_meaning": "monotonous",
        "secondary_meaning": "routine",
        "tertiary_meaning": "tedious",
        "sentence": "The humdrum routine of daily tasks made the job seem mundane and uninteresting."
    },
    695: {
        "word": "Hybrid",
        "english_meaning": "the offspring of two plants or animals of different species, such as a mule",
        "urdu_meaning": "مختلف نسلوں کا مرکب",
        "primary_meaning": "crossbreed",
        "secondary_meaning": "mixture",
        "tertiary_meaning": "hybridized",
        "sentence": "The hybrid plant exhibited characteristics of both parent species, demonstrating a combination of traits."
    },
    696: {
        "word": "Hyperbole",
        "english_meaning": "exaggerated statements or claims not meant to be taken literally",
        "urdu_meaning": "مبالغہ",
        "primary_meaning": "overstatement",
        "secondary_meaning": "exaggeration",
        "tertiary_meaning": "embellishment",
        "sentence": "His description of the event was full of hyperbole, making it sound more dramatic than it actually was."
    },
    697: {
        "word": "Hypocrite",
        "english_meaning": "a person who pretends to have virtues, moral or religious beliefs, principles, etc., that they do not actually possess",
        "urdu_meaning": "منافق",
        "primary_meaning": "pretender",
        "secondary_meaning": "faker",
        "tertiary_meaning": "dissembler",
        "sentence": "The politician was exposed as a hypocrite when his actions contradicted his professed values."
    },
    698: {
        "word": "Hypothesis",
        "english_meaning": "a supposition or proposed explanation made on the basis of limited evidence as a starting point for further investigation",
        "urdu_meaning": "فرضی تجربہ",
        "primary_meaning": "theory",
        "secondary_meaning": "assumption",
        "tertiary_meaning": "speculation",
        "sentence": "The scientist formulated a hypothesis to guide the experiment and test a specific prediction."
    },
    699: {
        "word": "Hysterical",
        "english_meaning": "affected by or deriving from wildly uncontrolled emotion",
        "urdu_meaning": "ہسٹیریہ کا شکار",
        "primary_meaning": "frantic",
        "secondary_meaning": "hysteric",
        "tertiary_meaning": "overwrought",
        "sentence": "The news of the accident left her in a hysterical state, unable to control her emotions."
    },
    700: {
        "word": "Iconoclastic",
        "english_meaning": "attacking or ignoring cherished beliefs and long-held traditions, etc., as being based on error, superstition, or lack of creativity",
        "urdu_meaning": "مجسمہ شکن",
        "primary_meaning": "rebellious",
        "secondary_meaning": "unconventional",
        "tertiary_meaning": "nonconformist",
        "sentence": "The artist's iconoclastic works challenged conventional norms and provoked thought among viewers."
    }
}


app = Flask(__name__)

db = SQL("sqlite:///dictionary.db")

@app.route("/")
def index():
    for word_id, word_info in words_data.items():
        db.execute("""
        INSERT INTO words (
            word, 
            english_meaning, 
            urdu_meaning, 
            primary_meaning, 
            secondary_meaning, 
            tertiary_meaning, 
            sentence
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
               word_info['word'],
               word_info['english_meaning'],
               word_info['urdu_meaning'],
               word_info['primary_meaning'],
               word_info['secondary_meaning'],
               word_info['tertiary_meaning'],
               word_info['sentence'])
    return render_template("written.html")

@app.route("/words")
def words():
    # Fetch specific columns instead of all columns from the database
    database = db.execute("SELECT word, english_meaning, urdu_meaning, primary_meaning, secondary_meaning, tertiary_meaning, sentence FROM words;")
    return render_template("index.html", database=database)
