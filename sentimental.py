import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
from collections import Counter
nltk.download('vader_lexicon')

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Sample transcription
transcription = """
Good morning purim this side from Super Delhi. Am I speaking to Pushpakji right? Yes. The call is regarding the complaint of partial order delivered concern later to today's delivery you raised the ticket that dates original 500 grams. One packet is missing, right? Yes. So sir, you received a cabbage in one packet, right? Yes. So in that packet some different items, some wrong items you received or only a single quantity of cabbage is there. And the outer packet is in damage or in open condition. Or it is a totally sealed pack condition. So your voice is very low. Hello. Yeah yeah. The packet in which you receive the cabin is that packet is in open or damaged condition or totally sealed package. So some wrong items you received in that packet or only single quantity of the cabbage is there. So may be possible that during packing at the warehouse maybe the person mistakenly forget to put this item. But no worries sir. I'm escalating sharing all the information given in return to the consent department regarding this. So right now I'm initiating a refund here. So possibilities both either you get refund or maybe reshooted for the next day. Because we are only authorized to initiate a refund to the customer. But sometimes system automatically converted in reschedule also. So that's the reason possibly is both. And I think that you already know about it. That customer have also right to cancel the residual product from the cleaner. So after cancellation it will take hardly 1015 minutes. That amount will be refunded in wallet session. Okay sir. Is there anything else? Yeah, about my second. Your voice is very low. Yes sir. Sorry but again your voice is very low. Words are not clearly audible. Okay. You are concerned. Yeah, now it's audible. Yeah. You're talking about the. You're talking about. Yeah, see. So you raise a ticket for quality expire so you receive the product but expiry packets you received. Yes actually those like. Yeah but. But don't worry. Actually I'm not in that department. Because you. If you are getting up packets of expiry date now. So regarding this, you already raised the right ticket. That is quality expired. So in this situation, our quality agent connect you and give the resolution for the same. Because if the customer. If the customer not receive the product or some item is missing inside the packet. So in that case, I'm the authorized person who initiated refund to the customer. Okay? So no worry. Our quality agent also connect you for the resolution. Thank you. Is there anything else I could help you with? That's all. That's all. Thank you. Okay sir. Thank you. Thank you for choosing super daily. Have a super daily. Thank you.
"""

# Perform sentiment analysis using NLTK
sid = SentimentIntensityAnalyzer()
sentiment_score = sid.polarity_scores(transcription)
print("Sentiment Score (NLTK):", sentiment_score)

# Perform keyword extraction using SpaCy
doc = nlp(transcription)
keywords = []
for token in doc:
    if token.pos_ in ["VERB"]:  # Consider only nouns, adjectives, and verbs as keywords
        keywords.append(token.text.lower())

# Get the most common keywords
most_common_keywords = Counter(keywords).most_common(5)
print("Most Common Keywords (SpaCy):", most_common_keywords)
