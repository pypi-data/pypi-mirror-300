from youtube_autonomous.shortcodes.enums import ShortcodeTagType
from youtube_autonomous.enums import ShortcodeType
from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from typing import Union


class ShortcodeTag:
    """
    Class that represent a shortcode tag to implement with
    the ShortcodeParser. This is just to let the parser know
    if it is a block-scoped shortcode tag, a simple shortcode
    tag and some more information needed.
    """
    tag: ShortcodeTagType
    """
    The ShortcodeTagType that corresponds to that tag.
    """
    type: ShortcodeType
    """
    The ShortcodeType that corresponds to that type.
    """

    def __init__(self, tag: str, type: Union[ShortcodeType, str]):
        """
        Initializes a shortcode tag object. The 'tag' parameter represents
        the shortcode name [tag], and the 'type' parameter is to point if
        the shortcode includes some text inside it [tag] ... [/tag] or if
        it is a simple one [tag].
        """
        tag = ShortcodeTagType.to_enum(tag)
        type = ShortcodeType.to_enum(type)
        
        self.tag = tag
        self.type = type

    def is_block_scoped(self):
        """
        Returns True if the shortcode is a block scoped one, that
        should look like this: [tag] ... [/tag], or False if not.
        """
        return self.type == ShortcodeTagType.BLOCK

