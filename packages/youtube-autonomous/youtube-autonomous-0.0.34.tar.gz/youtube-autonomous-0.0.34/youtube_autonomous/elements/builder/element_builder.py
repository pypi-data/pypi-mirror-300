from youtube_autonomous.elements.validator.element_parameter_validator import ElementParameterValidator
from youtube_autonomous.segments.enums import SegmentType, EnhancementType
from youtube_autonomous.elements.validator import BUILDER_SUBCLASSES
from youtube_autonomous.segments.builder.ai import create_ai_narration
from typing import Union


class ElementBuilder:
    # TODO: Maybe __init__ that returns the corresponding subclass
    # according to the provided 'type' (?)
    # https://stackoverflow.com/questions/9187388/possible-to-prevent-init-from-being-called

    @staticmethod
    def get_subclasses():
        from youtube_autonomous.elements.builder.ai_image_element_builder import AIImageElementBuilder
        from youtube_autonomous.elements.builder.image_element_builder import ImageElementBuilder
        from youtube_autonomous.elements.builder.ai_video_element_builder import AIVideoElementBuilder
        from youtube_autonomous.elements.builder.video_element_builder import VideoElementBuilder
        from youtube_autonomous.elements.builder.custom_stock_element_builder import CustomStockElementBuilder
        from youtube_autonomous.elements.builder.stock_element_builder import StockElementBuilder
        from youtube_autonomous.elements.builder.meme_element_builder import MemeElementBuilder
        from youtube_autonomous.elements.builder.sound_element_builder import SoundElementBuilder
        from youtube_autonomous.elements.builder.youtube_video_element_builder import YoutubeVideoElementBuilder
        from youtube_autonomous.elements.builder.text_element_builder import TextElementBuilder
        from youtube_autonomous.elements.builder.premade_element_builder import PremadeElementBuilder
        from youtube_autonomous.elements.builder.effect_element_builder import EffectElementBuilder
        from youtube_autonomous.elements.builder.greenscreen_element_builder import GreenscreenElementBuilder

        return [
            AIImageElementBuilder,
            AIVideoElementBuilder,
            ImageElementBuilder,
            VideoElementBuilder,
            CustomStockElementBuilder,
            StockElementBuilder,
            MemeElementBuilder,
            SoundElementBuilder,
            YoutubeVideoElementBuilder,
            TextElementBuilder,
            PremadeElementBuilder,
            EffectElementBuilder,
            GreenscreenElementBuilder
        ]

    @staticmethod
    def get_subclasses_as_str():
        return ', '.join(ElementBuilder.get_subclasses())
    
    @staticmethod
    def get_subclass_by_type(type: Union[SegmentType, EnhancementType, str]):
        type = ElementParameterValidator.validate_segment_or_enhancement_type(type)

        from youtube_autonomous.elements.builder.ai_image_element_builder import AIImageElementBuilder
        from youtube_autonomous.elements.builder.image_element_builder import ImageElementBuilder
        from youtube_autonomous.elements.builder.ai_video_element_builder import AIVideoElementBuilder
        from youtube_autonomous.elements.builder.video_element_builder import VideoElementBuilder
        from youtube_autonomous.elements.builder.custom_stock_element_builder import CustomStockElementBuilder
        from youtube_autonomous.elements.builder.stock_element_builder import StockElementBuilder
        from youtube_autonomous.elements.builder.meme_element_builder import MemeElementBuilder
        from youtube_autonomous.elements.builder.sound_element_builder import SoundElementBuilder
        from youtube_autonomous.elements.builder.youtube_video_element_builder import YoutubeVideoElementBuilder
        from youtube_autonomous.elements.builder.text_element_builder import TextElementBuilder
        from youtube_autonomous.elements.builder.premade_element_builder import PremadeElementBuilder
        from youtube_autonomous.elements.builder.effect_element_builder import EffectElementBuilder
        from youtube_autonomous.elements.builder.greenscreen_element_builder import GreenscreenElementBuilder

        if type in [SegmentType.MEME, EnhancementType.MEME]:
            return MemeElementBuilder
        elif type in [SegmentType.AI_IMAGE, EnhancementType]:
            return AIImageElementBuilder
        elif type in [SegmentType.AI_VIDEO, EnhancementType.AI_VIDEO]:
            return AIVideoElementBuilder
        elif type in [SegmentType.IMAGE, EnhancementType.IMAGE]:
            return ImageElementBuilder
        elif type in [SegmentType.VIDEO, EnhancementType.VIDEO]:
            return VideoElementBuilder
        elif type in [SegmentType.STOCK, EnhancementType.STOCK]:
            return StockElementBuilder
        elif type in [SegmentType.CUSTOM_STOCK, EnhancementType.CUSTOM_STOCK]:
            return CustomStockElementBuilder
        elif type in [SegmentType.SOUND, EnhancementType.SOUND]:
            return SoundElementBuilder
        elif type in [SegmentType.YOUTUBE_VIDEO, EnhancementType.YOUTUBE_VIDEO]:
            return YoutubeVideoElementBuilder
        elif type in [SegmentType.TEXT, EnhancementType.TEXT]:
            return TextElementBuilder
        elif type in [SegmentType.PREMADE, EnhancementType.PREMADE]:
            return PremadeElementBuilder
        elif type in [EnhancementType.EFFECT]:
            return EffectElementBuilder
        elif type in [EnhancementType.GREENSCREEN]:
            return GreenscreenElementBuilder
    
    @classmethod
    def build_narration(cls, text: str, output_filename: str):
        """
        Generates a narration file that narrates the 'text' provided and
        is stored locally as 'output_filename'. If 'text' or 
        'output_filename' fields are not provided it will raise an 
        Exception.
        """
        ElementParameterValidator.validate_string_mandatory_parameter('text', text)
        ElementParameterValidator.validate_string_mandatory_parameter('output_filename', output_filename)

        return create_ai_narration(text, output_filename = output_filename)
    
    @classmethod
    def handle_narration_from_segment(cls, segment: dict):
        pass