from re import search, compile, purge, Pattern
from string import punctuation, ascii_lowercase, digits
from unicodedata import name
from immutableType import Str_, Int_, StrError

special_caracteres = punctuation+digits

class Find:

    def __init__(self):
        """
        Init all characters.
        THE INITIALISATION IS VERY SLOW !
        """

        self.__alphabet_avec_variantes = {}
        for i in ascii_lowercase:
            self.__alphabet_avec_variantes[i] = self.__trouver_variantes_de_lettre(i)



    def __trouver_variantes_de_lettre(self, base_char: str) -> list:
        """
        Trouves des variantes d'une lettre et ajoute la ponctuation et les caractères digitales
        :param base_char:
        :return:
        """
        variantes = []
        for codepoint in range(0x110000):  # Limite de l'espace Unicode
            char = chr(codepoint)
            try:
                # Vérifier si le nom du caractère contient la lettre de base "a"
                unicode_name = name(char)

                result = search(r"\b["+f"{base_char.lower()}{base_char.upper()}"+r"]\b", unicode_name)

                if result is not None:
                    variantes.append(char)

            except ValueError:
                # Ignorer les caractères qui n'ont pas de nom Unicode
                pass
        return variantes + [i for i in special_caracteres]


    def __recherche_regex(self, mot: str) -> Pattern:
        """
        Crée le patter correspondant au mot recherché
        :param mot: le mot recherché
        :return: un modèle regex
        """
        correspondances = []

        for i in mot:
            correspondances.append(self.__alphabet_avec_variantes[i])

        pattern = r''.join([f"[{''.join(sous_liste)}]+[{special_caracteres}]*" for sous_liste in correspondances])

        return compile(pattern)

    def __check_types(self, arg) -> Str_:
        """
        Regarde si l'argument est un str ou non (les booléens sont considéré comme des châines de caractère
        :param arg: l'argument
        :return: Str_ type immuable
        :raise: StrError si l'argument n'est pas une châine de caractère
        """
        try:

            int(arg)

        except:
            return Str_(str(arg))

        raise StrError(arg)



    def find_Badwords(self, word: str, sentence: str, advanced: bool = True) -> bool:
        """
        Search any configuration of word in the sentence
        :param word: a simple word write in LATIN (not string digit) EX : ``ass`` not ``a*s``
        :param sentence: the sentence who the word is find (or not)
        :param advanced: Allow space and \\n replaced by ''
        :return: ``True`` if the word is find, else ``False``
        """

        wordStr = self.__check_types(word)
        sentenceStr = Str_(sentence)

        regex = self.__recherche_regex(wordStr.str_)

        if advanced:
            u = sentenceStr.str_.replace(' ', '').split('\n')
            sentenceStr.str_ = ''.join(u)

        result = search(regex, sentenceStr.str_)

        if result is None:
            purge()
            return False

        x = 0
        for i in result.group():
            if i in special_caracteres:
                x += 1

        if len(result.group()) == x:
            return False

        if result is not None:
            purge()
            return True
