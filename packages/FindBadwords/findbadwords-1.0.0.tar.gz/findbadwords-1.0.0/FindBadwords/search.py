from re import search, compile, purge, Pattern
from string import punctuation, ascii_lowercase
from unicodedata import name

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
        return variantes + [i for i in punctuation]


    def __recherche_regex(self, mot: str) -> Pattern:

        correspondances = []

        for i in mot:
            correspondances.append(self.__alphabet_avec_variantes[i])

        pattern = r''.join([f"[{''.join(sous_liste)}]+[{punctuation}]*" for sous_liste in correspondances])

        return compile(pattern)


    def find_Badwords(self, word: str, sentence: str) -> bool:
        """
        Search any configuration of word in the sentence
        :param word: a simple word write in LATIN
        :param sentence: the sentence who the word is find (or not)
        :return: ``True`` if the word is find, else ``False``
        """

        regex = self.__recherche_regex(word)

        result = search(regex, sentence.replace(' ', ''))

        if result is not None:
            purge()
            return True

        purge()
        return False