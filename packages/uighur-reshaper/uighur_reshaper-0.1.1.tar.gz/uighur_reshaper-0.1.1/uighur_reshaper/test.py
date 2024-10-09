from uighur_reshaper import reshaper
# Import Converter
converter = reshaper()

# Test
original_text = " بۇ بىر سىناق خەت، بىز بۇنىڭدا خەت كېڭەيتىلگەن رايونغا ئۆزگەردىمۇ شۇنى بىلمەكچى.   "  # 示例维吾尔语文本
extended_text = converter.basic2extend(original_text)
print("Orignal text:", original_text)
print("Reshaped text:", extended_text)

# Test Convert back, check if it is same as original text
converted_back_text = converter.extend2basic(extended_text)
print("Reshaped back:", converted_back_text)

# Same Text Content or Not
if converted_back_text == original_text:
    print("Same Text Content")



