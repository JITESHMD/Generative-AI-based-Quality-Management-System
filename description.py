import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Load NLTK resources
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Sample transcription
transcription = """
Good morning purim this side from Super Delhi. Am I speaking to Pushpakji right? Yes. The call is regarding the complaint of partial order delivered concern later to today's delivery you raised the ticket that dates original 500 grams. One packet is missing, right? Yes. So sir, you received a cabbage in one packet, right? Yes. So in that packet some different items, some wrong items you received or only a single quantity of cabbage is there. And the outer packet is in damage or in open condition. Or it is a totally sealed pack condition. So your voice is very low. Hello. Yeah yeah. The packet in which you receive the cabin is that packet is in open or damaged condition or totally sealed package. So some wrong items you received in that packet or only single quantity of the cabbage is there. So may be possible that during packing at the warehouse maybe the person mistakenly forget to put this item. But no worries sir. I'm escalating sharing all the information given in return to the consent department regarding this. So right now I'm initiating a refund here. So possibilities both either you get refund or maybe reshooted for the next day. Because we are only authorized to initiate a refund to the customer. But sometimes system automatically converted in reschedule also. So that's the reason possibly is both. And I think that you already know about it. That customer have also right to cancel the residual product from the cleaner. So after cancellation it will take hardly 1015 minutes. That amount will be refunded in wallet session. Okay sir. Is there anything else? Yeah, about my second. Your voice is very low. Yes sir. Sorry but again your voice is very low. Words are not clearly audible. Okay. You are concerned. Yeah, now it's audible. Yeah. You're talking about the. You're talking about. Yeah, see. So you raise a ticket for quality expire so you receive the product but expiry packets you received. Yes actually those like. Yeah but. But don't worry. Actually I'm not in that department. Because you. If you are getting up packets of expiry date now. So regarding this, you already raised the right ticket. That is quality expired. So in this situation, our quality agent connect you and give the resolution for the same. Because if the customer. If the customer not receive the product or some item is missing inside the packet. So in that case, I'm the authorized person who initiated refund to the customer. Okay? So no worry. Our quality agent also connect you for the resolution. Thank you. Is there anything else I could help you with? That's all. That's all. Thank you. Okay sir. Thank you. Thank you for choosing super daily. Have a super daily. Thank you.
"""

# Define problem categories and associated keywords
problem_categories = {
    'Cancellation Flight': ['cancel', 'cancellation'],
    'Reschedule Flight': ['reschedule'],
    'Flight Refund Related': ['refund'],
    'Flight Delay Complaint': ['delay'],
    'Staff Behavior Complaint': ['complaint', 'behavior'],
    'Miscellaneous': ['issue', 'problem']
}

# Tokenization
tokens = word_tokenize(transcription)

# POS tagging
tagged_tokens = pos_tag(tokens)

# Function to classify the call based on keywords and POS tags
def classify_call(transcription):
    # Initialize counters for each problem category
    category_counts = {category: 0 for category in problem_categories}
    
    # Loop through each token and its POS tag
    for token, pos_tag in tagged_tokens:
        # Convert token and POS tag to lowercase for matching
        token_lower = token.lower()
        pos_tag_lower = pos_tag.lower()
        
        # Check if token matches any keywords for each problem category
        for category, keywords in problem_categories.items():
            for keyword in keywords:
                if keyword in token_lower:
                    # Check surrounding POS tags to refine classification
                    if pos_tag_lower.startswith('vb') or pos_tag_lower.startswith('nn'):
                        category_counts[category] += 1  # Increment counter for the category
                        break  # Break loop to avoid double counting
            
    # Find the category with the highest count
    max_category = max(category_counts, key=category_counts.get)
    
    return max_category

# Classify the call
problem_category = classify_call(transcription)
print("Problem Category:", problem_category)
