# TODO: Refactor this, too many unneeded Enums

from yta_general_utils.programming.enum import YTAEnum as Enum, get_values


# TODO: Make 'EnhancementType' and 'SegmentType' dynamic
# because that is actually set in each Rule so if I 
# manually change one rule I have to change it also here.
class EnhancementType(Enum):
    """
    These Enums represent the types that a Enhancement could 
    be, allowing us to check and detect if it is valid.
    """
    CUSTOM_STOCK = 'custom_stock'
    STOCK = 'stock'
    AI_IMAGE = 'ai_image'
    IMAGE = 'image'
    AI_VIDEO = 'ai_video'
    VIDEO = 'video'
    SOUND = 'sound'
    YOUTUBE_VIDEO = 'youtube_video'
    TEXT = 'text'
    MEME = 'meme'
    EFFECT = 'effect'
    PREMADE = 'premade'
    GREENSCREEN = 'greenscreen'

class SegmentType(Enum):
    """
    These Enums represent the types that a Segment could
    be, allowing us to check and detect if it is valid.
    """
    # Interesting: https://docs.python.org/3/howto/enum.html
    CUSTOM_STOCK = 'custom_stock'
    """
    Stock videos but extracted from our own custom sources.
    """
    STOCK = 'stock'
    """
    Stock videos extracted from external stock platforms.
    """
    AI_IMAGE = 'ai_image'
    IMAGE = 'image'
    AI_VIDEO = 'ai_video'
    VIDEO = 'video'
    SOUND = 'sound'
    YOUTUBE_VIDEO = 'youtube_video'
    TEXT = 'text'
    MEME = 'meme'
    #EFFECT = 'effect'
    PREMADE = 'premade'
    #GREENSCREEN = 'greenscreen'

    # TODO: This below is now available through the rules...
    # This should be removed in a near future
    @classmethod
    def get_premade_types(cls):
        """
        Returns a list containing all the Segment Types that are 
        premades.
        """
        return [
            # SegmentType.YOUTUBE_SEARCH,
            # SegmentType.GOOGLE_SEARCH
        ]

    @classmethod
    def get_narration_types(cls):
        """
        Returns the SegmentType enums that are compatible with 
        audio narration.
        """
        return cls.get_all()
    
    @classmethod
    def get_narration_type_values(cls):
        """
        Returns the SegmentType enums values that are compatible
        with audio narration.
        """
        return get_values(cls.get_narration_types())
    
    @classmethod
    def get_url_types(cls):
        """
        Returns the SegmentType enums that are compatible with the
        'url' parameter.
        """
        return [
            SegmentType.IMAGE,
            SegmentType.YOUTUBE_VIDEO,
            SegmentType.VIDEO,
            SegmentType.SOUND
        ]
    
    @classmethod
    def get_url_type_values(cls):
        """
        Returns the SegmentType enums values that are compatible
        with the 'url' parameter.
        """
        return get_values(cls.get_url_types())
    
    @classmethod
    def get_keywords_types(cls):
        """
        Returns the SegmentType enums that are compatible with the
        'keywords' parameter.
        """
        return [
            SegmentType.MEME,
            SegmentType.AI_IMAGE,
            SegmentType.CUSTOM_STOCK,
            SegmentType.STOCK,
            # TODO: Add IMAGE in the future with Bing or Google Search
            # TODO: Add YOUTUBE_VIDEO in the future for Youtube Search
        ]
    
    @classmethod
    def get_keywords_type_values(cls):
        """
        Returns the SegmentType enums values that are compatible 
        with the 'keywords' parameter.
        """
        return get_values(cls.get_keywords_types())
    
    @classmethod
    def get_filename_types(cls):
        """
        Returns the SegmentType enums that are compatible with the
        'filename' parameter.
        """
        return [
            SegmentType.IMAGE,
            SegmentType.SOUND,
            SegmentType.VIDEO
        ]
    
    @classmethod
    def get_filename_type_values(cls):
        """
        Returns the SegmentType enums values that are compatible 
        with the 'filename' parameter.
        """
        return get_values(cls.get_filename_types())
    
    @classmethod
    def get_text_types(cls):
        """
        Returns the SegmentType enums that are compatible with the
        'text' parameter.
        """
        # TODO: This is defined in element rules
        return [
            SegmentType.TEXT,
        ]
    
    @classmethod
    def get_text_type_values(cls):
        """
        Returns the SegmentType enums values that are compatible 
        with the 'text' parameter.
        """
        return get_values(cls.get_text_types())
    
class SegmentField(Enum):
    """
    These Enums represent the fields that a Segment has, allowing us
    to check that any required field is provided and/or to detect 
    which one is missing.

    Examples: TYPE, KEYWORDS, URL, etc.
    """
    # Interesting: https://docs.python.org/3/howto/enum.html
    TYPE = 'type'
    KEYWORDS = 'keywords'
    URL = 'url'
    FILENAME = 'filename'
    NARRATION_TEXT = 'narration_text'
    VOICE = 'voice'
    TEXT = 'text'
    DURATION = 'duration'
    AUDIO_NARRATION_FILENAME = 'audio_narration_filename'
    MUSIC = 'music'
    ENHANCEMENTS = 'enhancements'

class EnhancementField(Enum):
    """
    Fields accepted for enhancement elements.
    """
    TYPE = 'type'
    KEYWORDS = 'keywords'
    URL = 'url'
    FILENAME = 'filename'
    NARRATION_TEXT = 'narration_text'
    VOICE = 'voice'
    TEXT = 'text'
    AUDIO_NARRATION_FILENAME = 'audio_narration_filename'
    MUSIC = 'music'
    START = 'start'
    DURATION = 'duration'
    MODE = 'mode'
    
# TODO: Apply this, is interesting
class EnhancementOrigin(Enum):
    USER = 'user'
    """
    The Enhancement was written manually by the user when
    creating the segment.
    """
    NARRATION_TEXT_SHORTCODE = 'narration_text_shortcode'
    """
    The Enhancement was manually set by the user on the
    'narration_text' field.
    """
    EDITION_MANUAL = 'edition_manual'
    """
    The Enhancement was automatically created when the
    Edition Manual was applied on the given 
    'narration_text' field.
    """

# TODO: Review this, is needed (?)
class SegmentBuildingField(Enum):
    """
    The fields that are used when building the segment and are
    not provided by the user in the initial segment json data.
    """
    TRANSCRIPTION = 'transcription'
    AUDIO_FILENAME = 'audio_filename'
    AUDIO_CLIP = 'audio_clip'
    VIDEO_FILENAME = 'video_filename'
    VIDEO_CLIP = 'video_clip'
    FULL_FILENAME = 'full_filename'
    FULL_CLIP = 'full_clip'
    # TODO: What about 'status', 'music_filename' and any other (if existing) (?)

# TODO: Project has more fields I think
class ProjectField(Enum):
    """
    The fields that are used to handle the project information.
    """
    STATUS = 'status'
    """
    The current status of the project, that must be a ProjectStatus
    enum.
    """
    SEGMENTS = 'segments'
    """
    The array that contains all the information about each one of 
    his segments.
    """

# TODO: Review this (maybe rename as it is for shortcodes, 
# not enhancement elements yet).
class EnhancementElementStart(Enum):
    """
    These Enums are valid values for the 'start' EnhancementElementField.
    """
    BETWEEN_WORDS = 'between_words'
    """
    This will make the enhancement element start just in the middle of 
    two words that are dictated in narration. This means, after the end
    of the first and and before the start of the next one (that should
    fit a silence part).
    """
    START_OF_FIRST_SHORTCODE_CONTENT_WORD = 'start_of_first_shortcode_content_word'
    """
    This will make the enhancement element start when the first word of 
    the shortcode content starts being dictated.
    """
    MIDDLE_OF_FIRST_SHORTCODE_CONTENT_WORD = 'middle_of_first_shortcode_content_word'
    """
    This will make the enhancement element start when the first word of 
    the shortcode content is in the middle of the dictation.
    """
    END_OF_FIRST_SHORTCODE_CONTENT_WORD = 'end_of_first_shortcode_content_word'
    """
    This will make the enhancement element start when the first word of 
    the shortcode content ends being dictated.
    """

    @classmethod
    def get_default(cls):
        return cls.START_OF_FIRST_SHORTCODE_CONTENT_WORD
    
# TODO: Review this
class EnhancementElementDuration(Enum):
    """
    These Enums represent the time, during a segment lifetime, that
    the elements are going to last (be shown).
    """
    SHORTCODE_CONTENT = 'shortcode_content'
    """
    This will make the enhancement element last until the shortcode
    block-scoped content is narrated.
    """
    FILE_DURATION = 'file_duration'
    """
    This will make the segment last the clip duration. It will be
    considered when the file is downloaded, and that duration will
    be flagged as 9999. This is for videos or audios that have a
    duration based on file.
    """
    
    @classmethod
    def get_default(cls):
        return cls.SHORTCODE_CONTENT

class EnhancementMode(Enum):
    """
    These Enums represent the different ways in which the project
    segment elements can be built according to the way they are
    included in the segment.
    """
    INLINE = 'inline'
    """
    Those segment elements that will be displayed in 'inline' mode, that
    means they will interrupt the main video, be played, and then go back
    to the main video. This will modify the clip length, so we need to 
    refresh the other objects start times.
    """
    OVERLAY = 'overlay'
    """
    Those segment elements that will be displayed in 'overlay' mode, that
    means they will be shown in the foreground of the main clip, changing
    not the main video duration, so they don't force to do any refresh.
    """
    REPLACE = 'replace'
    """
    Those enhancement elements that will replace the video in this mode.
    This means that the original video is modified by this enhancement
    element and that modified part will be placed instead of the original
    video. This modified part could be the whole video or only a part of
    it. This is how most of the greenscreens or effects are applied.
    """
    
    @classmethod
    def get_default(cls):
        """
        Returns the default enum of this list. This value will be used when
        no valid value is found.
        """
        return cls.INLINE

class SegmentStatus(Enum):
    """
    The current segment status defined by this string.
    """
    TO_START = 'to_start'
    # TODO: Remove below
    SHORTCODES_PROCESSED = 'shortcodes_processed'
    """
    Status for the moment in which the segment 'narration_text'
    has been analyzed and the shortcodes have been extracted to
    their corresponding enhancement elements.
    """
    BASE_CONTENT_CREATED = 'base_content_created'
    """
    Status for the moment in which the segment base content has
    been created so only the enhancement elements are remaining.
    """
    # TOOD: Remove above
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'

class ProjectStatus(Enum):
    """
    The current project status defined by this string.
    """
    TO_START = 'to_start'
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'