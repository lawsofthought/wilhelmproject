from __future__ import absolute_import

#=============================================================================
# Standard library imports.
#=============================================================================
import json
import logging
from collections import OrderedDict

#=============================================================================
# Wilhelm imports
#=============================================================================
from .widgets import (Widget, 
                      SessionWidget, 
                      WordlistMixin,
                      SessionWordlistMixin)

from apps.core import fields
from contrib.stimuli.textual.models import WordlistStimulus
from apps.dataexport.utils import safe_export_data

#================================ End Imports ================================

logger = logging.getLogger('wilhelm')

class WordlistDisplay(Widget, WordlistMixin):

    '''
    A widget to display words to be memorized.

    - wordliststimulus: A link to a WordlistStimulus
    - isi: The interval between words.
    - fadeInDuration: How long it takes the word to fade in.
    - fadeOutDuration: How long it takes the word to fade out.
    - stimulusDuration: How long will the stimulus be displayed.

    '''

    wordliststimulus = fields.ForeignKey(WordlistStimulus)
    isi = fields.DurationField(default=0.2)
    fadeInDuration = fields.DurationField(default=0.2)
    fadeOutDuration = fields.DurationField(default=0.2)
    stimulusDuration = fields.DurationField(default=3)

    @classmethod
    def new(cls, 
            wordlist, 
            start_msg,
            isi, 
            fadeInDuration, 
            fadeOutDuration,
            stimulusDuration):

        wordliststimulus = WordlistStimulus.new(wordlist = wordlist)

        return cls._new(wordliststimulus = wordliststimulus, 
                        start_msg = start_msg,
                        isi = isi, 
                        fadeInDuration = fadeInDuration, 
                        fadeOutDuration = fadeOutDuration,
                        stimulusDuration = stimulusDuration)

    @property
    def wordlist_length(self):
        return self.wordliststimulus.length

    @property
    def widget_data(self):
        '''

        '''
        return dict(wordlist = self.wordlist, 
                    start_msg = self.start_msg,
                    isi = self.isi, 
                    fadeInDuration = self.fadeInDuration, 
                    fadeOutDuration = self.fadeOutDuration, 
                    stimulusDuration = self.stimulusDuration)

    def get_widget_template_data(self):

        stimulus_duration_str\
            = str(int(self.stimulusDuration)) + ' seconds'

        return dict(wordlist_length = self.wordlist_length,
                    stimulus_duration = stimulus_duration_str)

class SessionWordlistDisplay(SessionWordlistMixin, SessionWidget):

    '''
    What is the order of the list of words that were displayed?
    '''

    wordliststimulus = fields.ForeignKey(WordlistStimulus)

    def post(self, data):

        response_data = json.loads(data['responses'])
 
        self.wordliststimulus = WordlistStimulus.new(
            wordlist = [datum['word'] for datum in response_data]
        )
        self.save()
        self.set_completed()

    @property
    def wordlist(self):
        return self.wordliststimulus.wordlist


    def data_export(self):

        """
        Export SessionWordlistDisplay data.

        """

        export_dict = super(SessionWordlistDisplay, self).data_export()

        for key, f in [('isi', lambda: self.widget.isi), 
                       ('FadeInDuration', lambda: self.widget.fadeInDuration),
                       ('FadeOutDuration', lambda: self.widget.fadeOutDuration),
                       ('stimulusDuration', lambda: self.widget.stimulusDuration),
                       ('wordlist items', lambda: self.wordlist)]:

            export_dict, exception_raised, exception_msg\
                = safe_export_data(export_dict, key, f)

            if exception_raised:
                logger.warning(exception_msg)

        return export_dict

    def feedback(self):

        """
        Return a dict stating that the memorandum was a word list and not a
        text; the word list itself; the length of the list.
        """

        summary = {}

        summary['Memoranda_type'] = 'Wordlist'
        summary['Wordlist'] = self.wordlist
        summary['List_length'] = len(self.wordlist)

        return summary
