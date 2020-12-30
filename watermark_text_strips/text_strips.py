#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from PIL import ImageOps, Image, ImageFont, ImageDraw
from thumbor.filters import BaseFilter, filter_method


class Filter(BaseFilter):
    @filter_method(
        BaseFilter.String,#word
    )
    def text_strips(self, word):
        backgroundImage = self.engine.image
        fontSize = 30
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", fontSize)
        wordWidth, wordHeight = font.getsize(word)
        bgWidth, bgHeight = backgroundImage.size
        bgDiagonal = 2*(bgWidth + bgHeight)

        txtImage = Image.new('RGBA', (bgDiagonal, bgHeight), (0, 0, 0, 0))
        txtImageX, txtImageY = txtImage.size
        words = []
        rowCount = int(round(bgDiagonal/wordWidth)) + 2
        for w in range(rowCount):
            words.append(word)
        words = '     '.join(words)

        finalWords = []
        columnCounts = int(round(bgHeight/wordHeight))
        for w in range(columnCounts):
            finalWords.append(words)
        finalWords = '\n'.join(finalWords)

        draw = ImageDraw.Draw(txtImage)
        draw.multiline_text((0,0), finalWords, fill=(0, 0, 0, 90), font=font, spacing=80)
        topBottomRotate = txtImage.rotate(angle=45, expand=1, center=(0,0))
        backgroundImage.paste(im=topBottomRotate, box=(-(txtImageY/2 + 80), 0), mask=topBottomRotate)
        self.engine.image = backgroundImage