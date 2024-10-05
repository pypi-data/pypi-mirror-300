from youtube_autonomous.segments.enums import SegmentField, EnhancementField, SegmentType, EnhancementType, EnhancementMode
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from yta_general_utils.programming.enum import YTAEnum as Enum
from typing import Union



class StringDuration(Enum):
    """
    This string value is only accepted in the segment dict that
    the user provides to the system. The key will be accepted
    and transformed into the value to be processed dynamically
    when building the content.
    """
    SHORTCODE_CONTENT = 99997
    """
    This string value determines that the duration is expected
    to be from the begining of the shortcode content (first 
    word) to the end of it (last word).

    This duration is accepted only in shortcodes.
    """
    FILE_DURATION = 99998
    """
    This string value determines that the duration is expected
    to be the source file (downloaded or obtained from the 
    local system) duration.

    This duration is accepted in shortcodes, in segments and in
    enhancements.
    """
    SEGMENT_DURATION = 99999
    """
    This string value determines that the duration is expected
    to be the whole segment duration (known when built).

    This duration is accepted only in segments and shortcodes.
    """
    
    @staticmethod
    def convert_duration(duration: str):
        """
        Converts the provided 'duration' string to its actual value
        according to the existing StringDuration enums or raises an
        Exception if not valid.

        This method returns the int value of the given 'duration'.
        """
        if duration == StringDuration.SHORTCODE_CONTENT.name:
            duration == StringDuration.SHORTCODE_CONTENT.value
        elif duration == StringDuration.FILE_DURATION.name:
            duration == StringDuration.FILE_DURATION.value
        elif duration == StringDuration.SEGMENT_DURATION.name:
            duration == StringDuration.SEGMENT_DURATION.value
        else:
            raise Exception(f'The provided "duration" parameter {duration} is not a valid StringDuration name.')

        return duration

class ElementValidator:
    """
    Class to validate the segment o enhancement element fields and
    their values.
    """
    SEGMENT_MANDATORY_FIELDS = SegmentField.get_all_values()
    ENHANCEMENT_MANDATORY_FIELDS = EnhancementField.get_all_values()

    @staticmethod
    def validate_segment_fields(segment: dict):
        """
        Validates that the 'segment' dictionary provided has all the
        required segment fields and only those ones and raises an
        Exception if more parameters or less parameters exist.

        This method returns the 'segment' provided if everything is
        ok.
        """
        accepted_fields_str = ', '.join(ElementValidator.SEGMENT_MANDATORY_FIELDS)
        unaccepted_fields = [key for key in segment.keys() if key not in ElementValidator.SEGMENT_MANDATORY_FIELDS]
        unaccepted_fields_str = ', '.join(unaccepted_fields)
        missing_fields = [field for field in ElementValidator.SEGMENT_MANDATORY_FIELDS if field not in segment]
        missing_fields_str = ', '.join(missing_fields)

        # TODO: Improve these 2 messages
        if missing_fields:
            raise Exception(f'The next fields are mandatory and were not found in the Segment: "{missing_fields_str}". The mandatory fields are: "{accepted_fields_str}".')

        if unaccepted_fields:
            raise Exception(f'The next fields are not accepted in Segments by our system: "{unaccepted_fields_str}". The ones accepted are these: "{accepted_fields_str}".')
        
        return segment
    
    @staticmethod
    def validate_enhancement_fields(enhancement: dict):
        """
        Validates that the 'enhancement' dictionary provided has all
        the required segment fields and only those ones and raises an
        Exception if more parameters or less parameters exist.

        This method returns the 'enhancement' provided if everything is
        ok.
        """
        accepted_fields_str = ', '.join(ElementValidator.ENHANCEMENT_MANDATORY_FIELDS)
        unaccepted_fields = [key for key in enhancement.keys() if key not in ElementValidator.ENHANCEMENT_MANDATORY_FIELDS]
        unaccepted_fields_str = ', '.join(unaccepted_fields)
        missing_fields = [field for field in ElementValidator.ENHANCEMENT_MANDATORY_FIELDS if field not in enhancement]
        missing_fields_str = ', '.join(missing_fields)

        # TODO: Improve these 2 messages
        if missing_fields:
            raise Exception(f'The next fields are mandatory and were not found in the Enhancement: "{missing_fields_str}". The mandatory fields are: "{accepted_fields_str}".')

        if unaccepted_fields:
            raise Exception(f'The next fields are not accepted in Enhancement by our system: "{unaccepted_fields_str}". The ones accepted are these: "{accepted_fields_str}".')
        
        return enhancement
    
    @staticmethod
    def validate_segment_duration_field(duration: Union[int, float, str, None]):
        """
        Validates that the 'duration' provided, if not None, has a 
        valid and positive numeric value or is a string accepted 
        for a segment.
        """
        if duration is not None:
            if isinstance(duration, str):
                accepted_str_duration = [StringDuration.FILE_DURATION.name]
                accepted_str_duration_str = ', '.join(accepted_str_duration)
                if duration not in accepted_str_duration:
                    raise Exception(f'Unexpected duration value {duration}. The accepted duration strings for a segment are: {accepted_str_duration_str}')

                duration = StringDuration[duration]
            else:
                ElementParameterValidator.validate_positive_number('duration', duration)

        return duration

    @staticmethod
    def validate_enhancement_duration_field(duration: Union[int, float, str, None]):
        """
        Validates that the 'duration' provided, if not None, has a 
        valid and positive numeric value or is a string accepted 
        for an enhancement.

        This method will return the duration, if string, as a
        StringDuration Enum Object, or if a number, as it is.
        """
        if duration is not None:
            if isinstance(duration, str):
                accepted_str_duration = [StringDuration.FILE_DURATION.name, StringDuration.SEGMENT_DURATION.name]
                accepted_str_duration_str = ', '.join(accepted_str_duration)
                if duration not in accepted_str_duration:
                    raise Exception(f'Unexpected duration value {duration}. The accepted duration strings for an enhancement are: {accepted_str_duration_str}')
                
                duration = StringDuration[duration]
            else:
                ElementParameterValidator.validate_positive_number('duration', duration)
        
        return duration
    
    @staticmethod
    def validate_enhancement_mode_field(mode: Union[EnhancementMode, str, None]):
        """
        Validates if the provided 'mode' parameter is a valid parameter
        for an Enhancement object. It should be an EnhancementMode enum
        or one of its string values to be accepted.
        
        This method will raise an Exception if not valid or will return
        it as it is, or as an EnhancementMode if one of its valid string
        values provided.
        """
        if mode is not None:
            if isinstance(mode, str):
                if not EnhancementMode.is_valid(mode):
                    raise Exception(f'Unexpected mode value {mode}. The accepted mode strings for an enhancement are: {EnhancementMode.get_all_values_as_str()}')
                
                mode = EnhancementMode(mode)
            elif not isinstance(mode, EnhancementMode):
                raise Exception('The "mode" parameter provided is not a EnhancementMode nor a string.')
        
        return mode
    
    @staticmethod
    def validate_enhancement_mode_field_for_type(mode: Union[str, None], type: str):
        """
        Validates if the provided 'mode' is valid for the also provided
        'type', raising an Exception if not or returning the mode as it
        is if valid.
        """
        # TODO: Refactor this. These mode valid if type and that stuff should
        # be centralized in one file or using another strategy, but for now
        # it is like this due to issues in the building process
        INLINE_VALID_TYPES = [EnhancementType.AI_IMAGE.value, EnhancementType.IMAGE.value, EnhancementType.AI_VIDEO.value, EnhancementType.VIDEO.value, EnhancementType.STOCK.value, EnhancementType.CUSTOM_STOCK.value, EnhancementType.MEME.value, EnhancementType.SOUND.value, EnhancementType.PREMADE.value, EnhancementType.YOUTUBE_VIDEO.value, EnhancementType.TEXT.value]
        OVERLAY_VALID_TYPES = [EnhancementType.AI_IMAGE.value, EnhancementType.IMAGE.value, EnhancementType.AI_VIDEO.value, EnhancementType.VIDEO.value, EnhancementType.STOCK.value, EnhancementType.CUSTOM_STOCK.value, EnhancementType.MEME.value, EnhancementType.SOUND.value, EnhancementType.PREMADE.value, EnhancementType.YOUTUBE_VIDEO.value, EnhancementType.TEXT.value]
        REPLACE_VALID_TYPES = [EnhancementType.EFFECT.value, EnhancementType.GREENSCREEN.value]

        if (mode == EnhancementMode.INLINE.value and type not in INLINE_VALID_TYPES) or (mode == EnhancementMode.OVERLAY.value and type not in OVERLAY_VALID_TYPES) or (mode == EnhancementMode.REPLACE.value and type not in REPLACE_VALID_TYPES):
            raise Exception(f'The provided "mode" parameter {mode} is not valid for the also provided "type" parameter {type}.')
        
        return mode
    
    @staticmethod
    def validate_segment_duration_field_for_type(duration: Union[int, float, str, None], type: str):
        """
        Validates if the provided 'duration' is a valid duration for the
        also provided Segment 'type'. The 'FILE_DURATION' duration is 
        only accepted for the 'meme' and 'sound' type'.
        """
        if duration in [StringDuration.FILE_DURATION, StringDuration.FILE_DURATION.name] and type not in [SegmentType.MEME.value, SegmentType.SOUND.value]:
            raise Exception(f'The "{StringDuration.FILE_DURATION.name}" string duration can be set only as {SegmentType.MEME.value} and {SegmentType.SOUND.value} for Segment types.')
        
    @staticmethod
    def validate_enhancement_duration_field_for_type(duration: Union[int, float, str, None], type: str):
        """
        Validates if the provided 'duration' is a valid duration for the
        also provided Enhancement 'type'. The 'FILE_DURATION' duration is
        only accepted for the 'meme' and 'sound' type'.
        """
        if duration in [StringDuration.FILE_DURATION, StringDuration.FILE_DURATION.name] and type not in [EnhancementType.MEME.value, EnhancementType.SOUND.value]:
            raise Exception(f'The "{StringDuration.FILE_DURATION.name}" string duration can be set only as {EnhancementType.MEME.value} and {EnhancementType.SOUND.value} for Enhancement types.')
    
    @staticmethod
    def validate_shortcode_duration_field(duration: Union[int, float, str, None]):
        """
        Validates that the 'duration' provided, if not None, has a 
        valid and positive numeric value or is a string accepted 
        for a shortcode.
        """
        if duration is not None:
            if isinstance(duration, str):
                accepted_str_duration = [StringDuration.FILE_DURATION.name, StringDuration.SEGMENT_DURATION.name, StringDuration.SHORTCODE_CONTENT]
                accepted_str_duration_str = ', '.join(accepted_str_duration)
                if duration not in accepted_str_duration:
                    raise Exception(f'Unexpected duration value {duration}. The accepted duration strings for a shortcode are: {accepted_str_duration_str}')
            else:
                ElementParameterValidator.validate_positive_number('duration', duration)
        
        return duration