import nlpaug.augmenter.word as naw

class NLPAugRephraser:
    '''A class for rephrasing text using NLP-Augment'''

    def __init__(self):
        self.aug = naw.SynonymAug(aug_src='wordnet')

    def rephrase(self, text):
        '''
        Rephrase the given text.

        Args:
            text (str): The text to be rephrased.

        Returns:
            str: The rephrased text.
        '''
        return self.aug.augment(text)
