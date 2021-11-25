# import regex
import re

# import Unidecode
import unidecode

'''
# download stpwords
import nltk

nltk.download('stopwords')

# import nltk for stopwords
from nltk.corpus import stopwords

stop_words = set(stopwords.words('spanish'))
'''

stop_words = {'para', 'ante', 'sean', 'seréis', 'fuimos', 'también', 'hemos', 'estaré', 'tenida', 'muchos',
              'estuvieron', 'algunas', 'estaríais', 'tu', 'algunos', 'vuestra', 'están', 'que', 'estarías', 'habían',
              'se', 'tenga', 'todo', 'nuestros', 'no', 'qué', 'tened', 'tengas', 'cual', 'este', 'estuvieras', 'esté',
              'algo', 'estén', 'estuvisteis', 'estoy', 'estará', 'esas', 'estuviese', 'son', 'nuestro', 'teníais',
              'las', 'tendríais', 'estuve', 'tenéis', 'fueron', 'seré', 'quienes', 'éramos', 'tengan', 'tuviera',
              'eso', 'eran', 'los', 'sintiendo', 'vosotros', 'era', 'mí', 'tuvieras', 'habrá', 'será', 'estuviera',
              'o', 'tuyo', 'fue', 'le', 'sentida', 'porque', 'han', 'ellas', 'nos', 'tendremos', 'sin', 'tendrían',
              'estuvierais', 'todos', 'vuestro', 'tendrá', 'estos', 'tuyos', 'tuvimos', 'su', 'hubieras', 'estar',
              'estéis', 'estad', 'tengáis', 'teniendo', 'estuviésemos', 'como', 'esta', 'estaba', 'habrán', 'estaría',
              'os', 'y', 'tenidas', 'un', 'estuvo', 'fueses', 'sentidas', 'la', 'ya', 'serías', 'hubieron', 'fuera',
              'sentidos', 'suyas', 'tendrás', 'estuviste', 'mucho', 'fui', 'tendré', 'durante', 'siente', 'habidas',
              'fuesen', 'está', 'tengo', 'habéis', 'sentido', 'serás', 'fuiste', 'tienen', 'estaban', 'pero', 'estado',
              'estabas', 'habréis', 'nosotros', 'habríamos', 'hubiese', 'sus', 'tuvo', 'vuestros', 'tiene', 'tendréis',
              'esto', 'hubiera', 'habremos', 'seríais', 'hubo', 'fuésemos', 'somos', 'les', 'estuvieses', 'contra',
              'estarían', 'suyos', 'por', 'tenían', 'lo', 'fuerais', 'hay', 'tuvieran', 'tuvieses', 'estada',
              'tendrías', 'habido', 'sentid', 'estabais', 'sea', 'estemos', 'habíais', 'tenemos', 'fueran', 'estaremos',
              'seremos', 'habríais', 'ha', 'seríamos', 'nuestra', 'habré', 'hayan', 'hubimos', 'en', 'él', 'tenía',
              'hube', 'hayáis', 'suya', 'soy', 'tuvieron', 'hubieran', 'serán', 'ti', 'sería', 'estas', 'tendría',
              'hubiésemos', 'tuyas', 'mía', 'he', 'habiendo', 'hubiéramos', 'uno', 'fuisteis', 'con', 'desde', 'había',
              'tuviesen', 'e', 'una', 'seáis', 'teníamos', 'estuviéramos', 'habrías', 'seamos', 'estadas', 'quien',
              'estarás', 'habrían', 'tanto', 'nosotras', 'ella', 'estarán', 'te', 'estuvimos', 'esa', 'estaréis',
              'estás', 'tuvisteis', 'tuviésemos', 'hubiste', 'ni', 'estamos', 'hayamos', 'tuvieseis', 'hubieseis',
              'habrás', 'nada', 'eras', 'otros', 'erais', 'fuéramos', 'poco', 'has', 'entre', 'seas', 'mis', 'muy',
              'fuese', 'mías', 'tú', 'yo', 'otras', 'tengamos', 'tenidos', 'otra', 'sobre', 'donde', 'suyo', 'habida',
              'tuvierais', 'vosotras', 'más', 'míos', 'hubiesen', 'a', 'sí', 'tuviéramos', 'eres', 'serían', 'mi',
              'es', 'tuve', 'fueras', 'estuvieseis', 'tuya', 'tendríamos', 'fueseis', 'esos', 'estáis', 'otro',
              'tuviese', 'hubierais', 'haya', 'nuestras', 'estés', 'estuvieran', 'hasta', 'tienes', 'tendrán',
              'tenido', 'tenías', 'al', 'habría', 'sois', 'hubisteis', 'ese', 'antes', 'hayas', 'el', 'ellos',
              'hubieses', 'habidos', 'cuando', 'mío', 'unos', 'estuviesen', 'del', 'habías', 'estaríamos', 'vuestras',
              'tus', 'habíamos', 'de', 'tuviste', 'me', 'estando', 'estábamos', 'estados'}


def evaluate_strings(string_input, string_target):
    # convert to lower case
    lower_string_target = string_target.lower()
    lower_string_input = string_input.lower()

    # remove numbers
    no_number_string_target = re.sub(r'\d+', '', lower_string_target)
    no_number_string_input = re.sub(r'\d+', '', lower_string_input)

    # remove accents
    no_accent_string_target = unidecode.unidecode(no_number_string_target)
    no_accent_string_input = unidecode.unidecode(no_number_string_input)

    # remove all punctuation except words and space
    no_punc_string_target = re.sub(r'[^\w\s]', '', no_accent_string_target)
    no_punc_string_input = re.sub(r'[^\w\s]', '', no_accent_string_input)

    # remove white spaces
    no_wspace_string_target = no_punc_string_target.strip()
    no_wspace_string_input = no_punc_string_input.strip()

    # convert string to list of words
    lst_string_target = [no_wspace_string_target][0].split()
    lst_string_input = [no_wspace_string_input][0].split()

    # remove stopwords
    no_stpwords_string_target = ""
    no_stpwords_string_target_list = []
    for i in lst_string_target:
        if i not in stop_words:
            no_stpwords_string_target += i + ' '
            no_stpwords_string_target_list.append(i)

    no_stpwords_string_input = ""
    no_stpwords_string_input_list = []
    for i in lst_string_input:
        if i not in stop_words:
            no_stpwords_string_input += i + ' '
            no_stpwords_string_input_list.append(i)

    # removing last space
    no_stpwords_string_target = no_stpwords_string_target[:-1]
    no_stpwords_string_input = no_stpwords_string_input[:-1]

    # Check the list contains elements of another list
    check = any(item in no_stpwords_string_input_list for item in no_stpwords_string_target_list)

    result = None
    if check:
        score = 0
        for a, b in zip(string_input, string_target):
            if a == b:
                score = score + 1
        score = round(score / len(string_target) * 100)
        result = {"string": string_target, "score_%": score}

    return result
