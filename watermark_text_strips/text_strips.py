#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from PIL import ImageOps, Image, ImageFont, ImageDraw
from thumbor.filters import BaseFilter, filter_method


class Filter(BaseFilter):
    @filter_method(
        BaseFilter.String,#word
        BaseFilter.PositiveNumber,#alpha
    )
    def text_strips(self, word, alpha = 90):
        backgroundImage = self.engine.image
        fontSize = 30
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontSize)
        wordWidth, wordHeight = font.getsize(word)
        bgWidth, bgHeight = backgroundImage.size

        txtImage = Image.new('RGBA', (wordWidth, wordHeight), (0,0,0,0))
        
        draw = ImageDraw.Draw(txtImage)
        draw.text((0, 0), word, fill=(0, 0, 0, alpha), font=font)
        rotatedText = txtImage.rotate(angle=45, expand = 1)
        x_repeat = bgWidth / wordWidth + 1
        y_repeat = bgHeight / (wordHeight)
        x_spacing = 10
        y_spacing = 20
        for x_count in range(0, x_repeat):
            x = int(x_count*(rotatedText.size[0] + x_spacing))
            for y_count in range(0, y_repeat):
                y = int(y_count*(rotatedText.size[1] + y_spacing))
                backgroundImage.paste(im=rotatedText, box=(x, y), mask=rotatedText)

        self.engine.image = backgroundImage