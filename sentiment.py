# from transformers import pipeline

# # Load sentiment analysis and summarization pipelines
# sentiment_pipeline = pipeline("sentiment-analysis")
# summarization_pipeline = pipeline("summarization")

# # Sample text data
# example_texts = [
#     """
#     Good morning purim this side from Super Delhi. Am I speaking to Pushpakji right? Yes. The call is regarding the complaint of partial order delivered concern later to today's delivery you raised the ticket that dates original 500 grams. One packet is missing, right? Yes. So sir, you received a cabbage in one packet, right? Yes. So in that packet some different items, some wrong items you received or only a single quantity of cabbage is there. And the outer packet is in damage or in open condition. Or it is a totally sealed pack condition. So your voice is very low. Hello. Yeah yeah. The packet in which you receive the cabin is that packet is in open or damaged condition or totally sealed package. So some wrong items you received in that packet or only single quantity of the cabbage is there. So may be possible that during packing at the warehouse maybe the person mistakenly forget to put this item. But no worries sir. I'm escalating sharing all the information given in return to the consent department regarding this. So right now I'm initiating a refund here. So possibilities both either you get refund or maybe reshooted for the next day. Because we are only authorized to initiate a refund to the customer. But sometimes system automatically converted in reschedule also. So that's the reason possibly is both. And I think that you already know about it. That customer have also right to cancel the residual product from the cleaner. So after cancellation it will take hardly 1015 minutes. That amount will be refunded in wallet session. Okay sir. Is there anything else? Yeah, about my second. Your voice is very low. Yes sir. Sorry but again your voice is very low. Words are not clearly audible. Okay. You are concerned. Yeah, now it's audible. Yeah. You're talking about the. You're talking about. Yeah, see. So you raise a ticket for quality expire so you receive the product but expiry packets you received. Yes actually those like. Yeah but. But don't worry. Actually I'm not in that department. Because you. If you are getting up packets of expiry date now. So regarding this, you already raised the right ticket. That is quality expired. So in this situation, our quality agent connect you and give the resolution for the same. Because if the customer. If the customer not receive the product or some item is missing inside the packet. So in that case, I'm the authorized person who initiated refund to the customer. Okay? So no worry. Our quality agent also connect you for the resolution. Thank you. Is there anything else I could help you with? That's all. That's all. Thank you. Okay sir. Thank you. Thank you for choosing super daily. Have a super daily. Thank you.
#     """
# ]

# # Function to perform sentiment analysis and text summarization
# def analyze_sentiment_and_summarize(text):
#     # Sentiment analysis
#     sentiment_result = sentiment_pipeline(text)[0]

#     # Summarization
#     summary_result = summarization_pipeline(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']

#     return sentiment_result, summary_result

# # Iterate over example texts and perform sentiment analysis followed by summarization
# for text in example_texts:
#     sentiment_result, summary_result = analyze_sentiment_and_summarize(text)

#     # Print sentiment analysis result
#     print("Sentiment Analysis:")
#     print(f"Sentiment: {sentiment_result['label']} (Confidence: {sentiment_result['score']:.2f})")
#     print()

#     # Print text summarization result
#     print("Text Summarization:")
#     print(f"Summary: {summary_result}")
#     print()


from transformers import pipeline

# Load sentiment analysis and summarization pipelines
sentiment_pipeline = pipeline("sentiment-analysis")
summarization_pipeline = pipeline("summarization")

# Sample text data
example_texts = [
"""
Good morning purim this side from Super Delhi. Am I speaking to Pushpakji right? Yes. The call is regarding the complaint of partial order delivered concern later to today's delivery you raised the ticket that dates original 500 grams. One packet is missing, right? Yes. So sir, you received a cabbage in one packet, right? Yes. So in that packet some different items, some wrong items you received or only a single quantity of cabbage is there. And the outer packet is in damage or in open condition. Or it is a totally sealed pack condition. So your voice is very low. Hello. Yeah yeah. The packet in which you receive the cabin is that packet is in open or damaged condition or totally sealed package. So some wrong items you received in that packet or only single quantity of the cabbage is there. So may be possible that during packing at the warehouse maybe the person mistakenly forget to put this item. But no worries sir. I'm escalating sharing all the information given in return to the consent department regarding this. So right now I'm initiating a refund here. So possibilities both either you get refund or maybe reshooted for the next day. Because we are only authorized to initiate a refund to the customer. But sometimes system automatically converted in reschedule also. So that's the reason possibly is both. And I think that you already know about it. That customer have also right to cancel the residual product from the cleaner. So after cancellation it will take hardly 1015 minutes. That amount will be refunded in wallet session. Okay sir. Is there anything else? Yeah, about my second. Your voice is very low. Yes sir. Sorry but again your voice is very low. Words are not clearly audible. Okay. You are concerned. Yeah, now it's audible. Yeah. You're talking about the. You're talking about. Yeah, see. So you raise a ticket for quality expire so you receive the product but expiry packets you received. Yes actually those like. Yeah but. But don't worry. Actually I'm not in that department. Because you. If you are getting up packets of expiry date now. So regarding this, you already raised the right ticket. That is quality expired. So in this situation, our quality agent connect you and give the resolution for the same. Because if the customer. If the customer not receive the product or some item is missing inside the packet. So in that case, I'm the authorized person who initiated refund to the customer. Okay? So no worry. Our quality agent also connect you for the resolution. Thank you. Is there anything else I could help you with? That's all. That's all. Thank you. Okay sir. Thank you. Thank you for choosing super daily. Have a super daily. Thank you.
"""
]

# Function to split the text into chunks of max_length tokens
def split_text_into_chunks(text, max_length=512):
    chunks = []
    current_chunk = ""
    for word in text.split():
        if len(current_chunk) + len(word) < max_length:
            current_chunk += " " + word
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

# Function to perform sentiment analysis and text summarization
def analyze_sentiment_and_summarize(text):
    chunks = split_text_into_chunks(text)
    sentiment_results = []
    summaries = []
    for chunk in chunks:
        sentiment_result = sentiment_pipeline(chunk)[0]
        summary_result = summarization_pipeline(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
        sentiment_results.append(sentiment_result)
        summaries.append(summary_result)
    return sentiment_results, summaries

# Iterate over example texts and perform sentiment analysis followed by summarization
for text in example_texts:
    sentiment_results, summaries = analyze_sentiment_and_summarize(text)

    # Print sentiment analysis results for each chunk
    print("Sentiment Analysis:")
    for result in sentiment_results:
        print(f"Sentiment: {result['label']} (Confidence: {result['score']:.2f})")
    print()

    # Print text summarization results for each chunk
    print("Text Summarization:")
    for summary in summaries:
        print(f"Summary: {summary}")
    print()
