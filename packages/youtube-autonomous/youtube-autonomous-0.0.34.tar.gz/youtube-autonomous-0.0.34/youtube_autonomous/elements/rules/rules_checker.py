from youtube_autonomous.segments.enums import SegmentField
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator


class RulesChecker:
    @property
    def rules(self):
        return self._rules

    @rules.setter
    def rules(self, rules: 'ElementRules'):
        ElementParameterValidator.validate_rules(rules)
        
        self._rules = rules

    def __init__(self, rules: 'ElementRules'):
        self.rules = rules

    def check_this_need_rules(self, element: dict):
        """
        Receives the 'element' dictionary that must contain the fields that
        are mandatory by the rules configuration. This method will raise an
        Exception if any rule is broken.

        If no Exception is raised, all the needed fields are provided. This
        is not verifying if possible fields are available or not. Narration
        can be enabled but not needed, and maybe only one 'narration_text'
        is provided and not 'voice'. This situation won't raise an Exception
        here if narration is not needed.

        This method must be used when loading the element to raise any
        Exception if something is wrong and interrumpting the execution until
        it is fixed.
        """
        return RulesChecker.check_need_rules(element, self.rules)
    
    # With this methods below we check if we should build an specific
    # part. This must be used after validating the needed rules to
    # raise any exception if something is missing and is mandatory.
        
    def should_build_narration_rule(self, element: dict):
        """
        Returns True if, according to the rules given in the initialization,
        the element must have or can have a narration and the needed fields
        are given. This guarantees that the narration can be done and must 
        be done.
        """
        # TODO: Create a method 'is_class' in 'yta_general_utils' using this below
        class_names = ['Segment']
        if type(element).__name__ in class_names:
            element = {
                'narration_text': element.narration_text,
                'voice': element.voice,
                'audio_narration_filename': element.audio_narration_filename
            }
        # TODO: Please, refactor this, I want to be able to pass an Element subclass

        return (self.rules.can_have_narration or self.rules.need_narration) and RulesChecker.is_need_narration_rule_satisfied(element)

    def should_build_specific_duration_rule(self, element: dict):
        """
        Returns True if, according to the rules given in the initialization,
        the element must have or can have an specific duration and that field
        is given. This guarantees that the element must have the specific
        'duration' set during the building process.
        """
        return (self.rules.can_have_specific_duration or self.rules.need_specific_duration) and RulesChecker.is_need_specific_duration_rule_satisfied(element)

    def should_build_text_rule(self, element: dict):
        """
        Returns True if, according to the rules given in the initialization,
        the element must have or can have the text and that field is given.
        This guarantees that the element can use that text for the building
        process.
        """
        return (self.rules.can_have_text or self.rules.need_text) and RulesChecker.is_need_text_rule_satisfied(element)

    def should_build_filename_or_url_rule(self, element: dict):
        """
        Returns True if, according to the rules given in the initialization,
        the element must have or can have the filename or the url and those
        fields are given. This guarantees that the element can use those 
        fields, according to our strategy, in the building process.
        """
        # TODO: This is not ok
        return (self.rules.can_have_url or self.rules.can_have_filename or self.rules.need_filename_or_url) and RulesChecker.is_need_filename_or_url_rule_satisfied(element)

    def should_build_keywords_rule(self, element: dict):
        """
        Returns True if, according to the rules given in the initialization,
        the element must have or can have the keywords and that field is 
        given. This guarantees that the element can use that field in the
        building process.
        """
        return (self.rules.can_have_keywords or self.rules.need_keywords) and RulesChecker.is_need_keywords_rule_satisfied(element)

    @classmethod
    def check_need_rules(cls, element: dict, rules: 'ElementRules'):
        """
        Receives the 'element' dictionary that must contain the fields that
        are mandatory by the rules configuration. This method will raise an
        Exception if any rule is broken.

        If no Exception is raised, all the needed fields are provided. This
        is not verifying if possible fields are available or not. Narration
        can be enabled but not needed, and maybe only one 'narration_text'
        is provided and not 'voice'. This situation won't raise an Exception
        here if narration is not needed.

        This method must be used when loading the element to raise any
        Exception if something is wrong and interrumpting the execution until
        it is fixed.
        """
        ElementParameterValidator.validate_mandatory_parameter('element', element)
        ElementParameterValidator.validate_mandatory_parameter('rules', rules)
        ElementParameterValidator.validate_rules(rules)
        
        if rules.need_narration and not cls.is_need_narration_rule_satisfied(element):
            raise Exception('Narration is needed for this element and necessary fields are not present. The "audio_narration_filename" field or "voice" and "narration_text" fields are needed.')
        
        if rules.need_specific_duration and not cls.is_need_specific_duration_rule_satisfied(element):
            raise Exception('Specific duration is needed for this element and necessary fields are not present. The "duration" field is needed, or a narration with "audio_narration_filename" field or "voice" and "narration_text" fields.')
        
        if rules.need_text and not cls.is_need_text_rule_satisfied(element):
            raise Exception('An specific "text" field is needed and does not exist.')
        
        if rules.need_filename_or_url and not cls.is_need_filename_or_url_rule_satisfied(element):
            raise Exception('The "filename" field or the "url" field is needed (at least one of them) and none is provided.')
        
        if rules.need_keywords and not cls.is_need_keywords_rule_satisfied(element):
            raise Exception('The "keywords" field is needed for this type.')
        
    # These methods below check if the needed fields of the different
    # need rules exist so it is possible to build the corresponding
    # part, returning True if yes or False if not.

    @classmethod
    def is_need_narration_rule_satisfied(cls, element: dict):
        """
        Checks if the 'need_narration' rule is satisfied or not. This
        will check if the 'audio_narration_filename' or the tuple 'voice'
        and 'narration_text' are given.
        """
        if isinstance(element, dict):
            narration_text = element.get(SegmentField.NARRATION_TEXT.value, None)
            voice = element.get(SegmentField.VOICE.value, None)
            audio_narration_filename = element.get(SegmentField.AUDIO_NARRATION_FILENAME.value, None)
        else:
            narration_text = element.narration_text
            voice = element.voice
            audio_narration_filename = element.audio_narration_filename


        return audio_narration_filename or (voice and narration_text)

    @classmethod
    def is_need_specific_duration_rule_satisfied(cls, element: dict):
        """
        Checks if the 'need_specific_duration' rule is satisfied or not.
        This will check if the specific 'duration' field is set or if it
        is possible to create the narration (the 'need_narration' rule is
        satisfied).
        """
        duration = element.get(SegmentField.DURATION.value, None)

        return duration or cls.is_need_narration_rule_satisfied(element)

    @classmethod
    def is_need_text_rule_satisfied(cls, element: dict):
        """
        Checks if the 'need_text' rule is satisfied by checking if the
        'text' field is given or not.
        """
        text = element.get(SegmentField.TEXT.value, None)

        return text

    @classmethod
    def is_need_filename_or_url_rule_satisfied(cls, element: dict):
        """
        Checks if the 'need_filename_or_url' rule is satisfied by checking
        if at least one of the tuple 'filename' and 'url' fields are 
        provided or not.        
        """
        filename = element.get(SegmentField.FILENAME.value, None)
        url = element.get(SegmentField.URL.value, None)

        return filename or url

    @classmethod
    def is_need_keywords_rule_satisfied(cls, element: dict):
        """
        Checks if the 'need_keywords' rule is satisfied by checking if
        the 'keywords' field is provided.
        """
        keywords = element.get(SegmentField.KEYWORDS.value, None)

        return keywords