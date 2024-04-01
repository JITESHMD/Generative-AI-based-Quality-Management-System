import nltk
from textblob import TextBlob

# Download NLTK resources
nltk.download('punkt')

# Sample transcription
transcription = """
Good morning purim this side from Super Delhi. Am I speaking to Pushpakji right? Yes. The call is regarding the complaint of partial order delivered concern later to today's delivery you raised the ticket that dates original 500 grams. One packet is missing, right? Yes. So sir, you received a cabbage in one packet, right? Yes. So in that packet some different items, some wrong items you received or only a single quantity of cabbage is there. And the outer packet is in damage or in open condition. Or it is a totally sealed pack condition. So your voice is very low. Hello. Yeah yeah. The packet in which you receive the cabin is that packet is in open or damaged condition or totally sealed package. So some wrong items you received in that packet or only single quantity of the cabbage is there. So may be possible that during packing at the warehouse maybe the person mistakenly forget to put this item. But no worries sir. I'm escalating sharing all the information given in return to the consent department regarding this. So right now I'm initiating a refund here. So possibilities both either you get refund or maybe reshooted for the next day. Because we are only authorized to initiate a refund to the customer. But sometimes system automatically converted in reschedule also. So that's the reason possibly is both. And I think that you already know about it. That customer have also right to cancel the residual product from the cleaner. So after cancellation it will take hardly 1015 minutes. That amount will be refunded in wallet session. Okay sir. Is there anything else? Yeah, about my second. Your voice is very low. Yes sir. Sorry but again your voice is very low. Words are not clearly audible. Okay. You are concerned. Yeah, now it's audible. Yeah. You're talking about the. You're talking about. Yeah, see. So you raise a ticket for quality expire so you receive the product but expiry packets you received. Yes actually those like. Yeah but. But don't worry. Actually I'm not in that department. Because you. If you are getting up packets of expiry date now. So regarding this, you already raised the right ticket. That is quality expired. So in this situation, our quality agent connect you and give the resolution for the same. Because if the customer. If the customer not receive the product or some item is missing inside the packet. So in that case, I'm the authorized person who initiated refund to the customer. Okay? So no worry. Our quality agent also connect you for the resolution. Thank you. Is there anything else I could help you with? That's all. That's all. Thank you. Okay sir. Thank you. Thank you for choosing super daily. Have a super daily. Thank you.
"""

# Sentiment Analysis
blob = TextBlob(transcription)
sentiment = blob.sentiment
print("Sentiment:", sentiment)

# Keyword Extraction
tokens = nltk.word_tokenize(transcription)
keywords = nltk.FreqDist(tokens).most_common(5)  # Extract top 5 most common words
print("Keywords:", keywords)

# Specific Phrase Detection
positive_phrases = ["very satisfied", "excellent service", "great experience"]
negative_phrases = ["poor quality", "disappointed", "unhappy customer"]

# Check for positive phrases
for phrase in positive_phrases:
    if phrase in transcription:
        print("Positive phrase detected:", phrase)

# Check for negative phrases
for phrase in negative_phrases:
    if phrase in transcription:
        print("Negative phrase detected:", phrase)
