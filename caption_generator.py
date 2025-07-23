from transformers import pipeline
import streamlit as st
import random
import re

# Import NLTK
try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    NLTK_AVAILABLE = True
    
    # Download NLTK data with better error handling
    try:
        # Try downloading the newer punkt_tab first
        nltk.download('punkt_tab', quiet=True)
        nltk.download('stopwords', quiet=True)
    except:
        try:
            # Fallback to older punkt if punkt_tab fails
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
        except:
            # If downloads fail, we'll use basic processing
            pass
            
except ImportError:
    NLTK_AVAILABLE = False

# Cache the model loading for better performance
@st.cache_resource
def load_model():
    """Load and cache the text generation model"""
    try:
        import os
        # Set environment variables for better compatibility
        os.environ['TOKENIZERS_PARALLELISM'] = 'false'
        return pipeline('text-generation', model='gpt2', device=-1, torch_dtype='auto')
    except Exception as e:
        st.warning(f"Could not load AI model: {e}. Using fallback text generation.")
        return None

# Platform-specific caption length limits
PLATFORM_LENGTHS = {
    "Instagram": 2200,
    "Twitter": 280,
    "LinkedIn": 3000,
    "Facebook": 63206
}

# Enhanced platform-specific emoji sets
PLATFORM_EMOJIS = {
    "Instagram": ["😍", "✨", "🌟", "🔥", "💖", "🌍", "📸", "🎉", "💯", "🙌", "😎", "🌈"],
    "Twitter": ["🚀", "🔥", "💬", "📈", "🌟", "😎", "👀", "🎯", "⚡", "🧵", "💭", "🔔"],
    "LinkedIn": ["💼", "📈", "🚀", "🌟", "🤝", "💡", "🎯", "🔗", "📊", "🎓", "💪", "🏆"],
    "Facebook": ["❤️", "😊", "🎉", "👨‍👩‍👧‍👦", "🏠", "🌟", "💖", "😍", "🤗", "🎈", "🌸", "☀️"]
}

# Enhanced tone-specific prompt templates - more specific and constrained
TONE_TEMPLATES = {
    "Casual": "Create a short, casual social media post about {keywords}. Keep it under 2 sentences:",
    "Professional": "Write a professional social media post about {keywords}. Be concise and valuable:",
    "Inspirational": "Create an inspiring short post about {keywords}. Make it motivational:",
    "Humorous": "Write a funny, short social media post about {keywords}. Keep it witty:",
    "Educational": "Share a quick tip or fact about {keywords}. Be informative but brief:"
}

# Call-to-action templates by platform
CTA_TEMPLATES = {
    "Instagram": ["Double tap if you agree! 💕", "Tag someone who needs to see this! 👇", "Save this post for later! 📌", "What do you think? Comment below! 💬"],
    "Twitter": ["Retweet if you agree! 🔄", "What's your take? Reply below! 💭", "Share your thoughts! 👇", "Tag someone who needs this! 🏷️"],
    "LinkedIn": ["What are your thoughts? Share in the comments! 💼", "Connect with me for more insights! 🤝", "Save this post for future reference! 📌", "Share if this resonates with your network! 📢"],
    "Facebook": ["Like if you agree! 👍", "Share with your friends! 📤", "What do you think? Comment below! 💬", "Tag someone who would love this! 🏷️"]
}

def generate_fallback_caption(keywords, platform, tone, include_cta=True):
    """Generate a simple caption when AI model is not available"""
    import random
    
    templates = {
        "Casual": [
            f"Just had an amazing experience with {keywords}! ✨",
            f"Loving this {keywords} moment! 💕",
            f"{keywords} vibes are everything right now! 🙌"
        ],
        "Professional": [
            f"Exploring new opportunities in {keywords}. Key insights ahead.",
            f"Sharing valuable insights about {keywords}.",
            f"Professional growth through {keywords} experiences."
        ],
        "Inspirational": [
            f"Every journey with {keywords} teaches us something valuable. Keep growing! 🌟",
            f"{keywords} reminds us that growth happens outside our comfort zone! 💪",
            f"Embracing the {keywords} journey with gratitude and purpose! ✨"
        ],
        "Humorous": [
            f"When life gives you {keywords}, make it memorable! 😄",
            f"Plot twist: {keywords} just made my day! 😂",
            f"Me trying to adult but {keywords} happened instead! 🤷‍♀️"
        ],
        "Educational": [
            f"Here's what I learned about {keywords} today...",
            f"Quick tip: {keywords} can be game-changing when done right!",
            f"Did you know? {keywords} has some fascinating aspects!"
        ]
    }
    
    template_list = templates.get(tone, [f"Sharing my thoughts on {keywords}."])
    caption = random.choice(template_list)
    
    if include_cta and platform in CTA_TEMPLATES:
        cta = random.choice(CTA_TEMPLATES[platform])
        caption += " " + cta
    
    return caption

def generate_caption(keywords, platform, tone, include_cta=True):
    """
    Generate a social media caption based on keywords, platform, and tone.
    """
    generator = load_model()
    if not generator:
        return generate_fallback_caption(keywords, platform, tone, include_cta)
    
    # Create prompt
    prompt = TONE_TEMPLATES[tone].format(keywords=keywords)
    # Much shorter max length to prevent rambling
    max_length = min(50, len(prompt.split()) + 25)  # Prompt + ~25 words max
    
    try:
        # Generate text with more controlled parameters
        result = generator(
            prompt, 
            max_length=max_length, 
            num_return_sequences=1, 
            truncation=True,
            do_sample=True,
            temperature=0.7,  # Lower temperature for more focused output
            top_p=0.9,  # Nucleus sampling for better quality
            repetition_penalty=1.1,  # Avoid repetition
            pad_token_id=generator.tokenizer.eos_token_id
        )[0]['generated_text']
        
        # Clean the caption more aggressively
        caption = result.replace(prompt, "").strip()
        
        # Remove any text after common ending patterns that indicate rambling
        end_patterns = [
            r'\. [A-Z].*',  # Remove anything after first sentence ending
            r'\? [A-Z].*',  # Remove anything after question
            r'! [A-Z].*',   # Remove anything after exclamation
        ]
        
        for pattern in end_patterns:
            match = re.search(pattern, caption)
            if match:
                caption = caption[:match.start() + 1]
                break
        
        # Remove incomplete sentences at the end
        sentences = re.split(r'[.!?]+', caption)
        if len(sentences) > 1 and sentences[-1].strip() and not sentences[-1].strip().endswith(('.', '!', '?')):
            caption = '. '.join(sentences[:-1]) + '.'
        elif not caption.endswith(('.', '!', '?')):
            caption = caption.rstrip() + '.'
        
        # Aggressive length limiting - if too long, use first sentence only
        max_reasonable_length = 300  # Much shorter than platform limits
        if len(caption) > max_reasonable_length:
            # Find first sentence ending
            first_sentence_end = min(
                caption.find('.') if caption.find('.') != -1 else len(caption),
                caption.find('!') if caption.find('!') != -1 else len(caption),
                caption.find('?') if caption.find('?') != -1 else len(caption)
            )
            if first_sentence_end < len(caption):
                caption = caption[:first_sentence_end + 1]
            else:
                # If no sentence ending found, truncate and add period
                caption = caption[:max_reasonable_length].rsplit(' ', 1)[0] + '.'
        
        # Add call-to-action if requested
        if include_cta and platform in CTA_TEMPLATES:
            cta = random.choice(CTA_TEMPLATES[platform])
            if len(caption + " " + cta) <= max_reasonable_length:
                caption += " " + cta
        
        return caption
        
    except Exception as e:
        st.warning(f"AI generation failed: {str(e)}. Using fallback method.")
        return generate_fallback_caption(keywords, platform, tone, include_cta)

def suggest_hashtags(keywords, platform):
    """
    Suggest relevant hashtags based on keywords and platform.
    """
    # Define stop words
    stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'])
    
    if NLTK_AVAILABLE:
        try:
            nltk_stop_words = set(stopwords.words('english'))
            stop_words.update(nltk_stop_words)
        except:
            pass  # Use our basic stop words
    
    # Extract hashtags from keywords - try NLTK first, then fallback
    tokens = []
    if NLTK_AVAILABLE:
        try:
            tokens = word_tokenize(keywords.lower())
        except Exception as e:
            # If NLTK tokenization fails (like punkt_tab error), use regex
            tokens = re.findall(r'\b[a-zA-Z]+\b', keywords.lower())
    
    # If no tokens found, use simple split as final fallback
    if not tokens:
        tokens = [word.strip() for word in keywords.lower().split() if word.strip().isalpha()]
    
    hashtags = []
    
    for token in tokens:
        if token.isalnum() and len(token) > 2 and token not in stop_words:
            hashtags.append(f"#{token.capitalize()}")
    
    # Enhanced platform-specific hashtag suggestions
    platform_hashtags = {
        "Instagram": ["#InstaGood", "#PhotoOfTheDay", "#Love", "#Instagrams", "#Follow", "#Like4Like", "#Amazing", "#Beautiful"],
        "Twitter": ["#Trending", "#Twitter", "#Social", "#News", "#Update", "#Thoughts", "#Community", "#Viral"],
        "LinkedIn": ["#LinkedIn", "#Career", "#Business", "#Professional", "#Leadership", "#Growth", "#Success", "#Networking"],
        "Facebook": ["#Facebook", "#Social", "#Community", "#Family", "#Friends", "#Life", "#Update", "#Share"]
    }
    
    # Add platform-specific hashtags
    if platform in platform_hashtags:
        hashtags.extend(random.sample(
            platform_hashtags[platform], 
            min(5, len(platform_hashtags[platform]))
        ))
    
    # Topic-specific hashtags
    topic_hashtags = {
        "travel": ["#Travel", "#Adventure", "#Wanderlust", "#Explore", "#Vacation"],
        "food": ["#Food", "#Foodie", "#Delicious", "#Cooking", "#Recipe"],
        "fitness": ["#Fitness", "#Gym", "#Workout", "#Health", "#Motivation"],
        "tech": ["#Tech", "#Technology", "#Innovation", "#Digital", "#Future"],
        "business": ["#Business", "#Entrepreneur", "#Success", "#Growth", "#Leadership"],
        "motivation": ["#Motivation", "#Inspiration", "#Success", "#Goals", "#Mindset"]
    }
    
    # Add topic-specific hashtags
    for topic, tags in topic_hashtags.items():
        if topic in keywords.lower():
            hashtags.extend(random.sample(tags, min(3, len(tags))))
    
    # Remove duplicates and limit count
    hashtags = list(dict.fromkeys(hashtags))[:15]  # Limit to 15 hashtags
    
    return hashtags

def suggest_emojis(keywords, platform):
    """
    Suggest relevant emojis based on keywords and platform.
    """
    # Enhanced keyword-to-emoji mapping
    keyword_emoji_map = {
        "travel": ["✈️", "🌍", "🗺️", "🧳", "🏖️", "🏔️"],
        "motivation": ["💪", "🌟", "🚀", "🔥", "⚡", "🏆"],
        "tech": ["💻", "📱", "🔬", "🤖", "�", "⚙️"],
        "food": ["🍔", "🍕", "🥗", "🍰", "☕", "🍜"],
        "fitness": ["🏋️", "💪", "🏃", "🚴", "🥇", "⚽"],
        "business": ["💼", "📈", "💰", "🤝", "📊", "🎯"],
        "love": ["❤️", "💖", "😍", "💕", "🥰", "💝"],
        "success": ["🏆", "🎉", "🌟", "🔥", "💯", "🚀"],
        "happy": ["😊", "😁", "🎉", "🌈", "☀️", "🎈"],
        "coffee": ["☕", "🌅", "💪", "⚡", "📅", "💼"]
    }
    
    selected_emojis = []
    
    # Find emojis based on keywords
    for keyword in keywords.lower().split():
        for key, emojis in keyword_emoji_map.items():
            if key in keyword or keyword in key:
                selected_emojis.extend(random.sample(emojis, min(2, len(emojis))))
    
    # Add platform-specific emojis
    if platform in PLATFORM_EMOJIS:
        platform_emojis = random.sample(
            PLATFORM_EMOJIS[platform], 
            min(4, len(PLATFORM_EMOJIS[platform]))
        )
        selected_emojis.extend(platform_emojis)
    
    # Remove duplicates and limit to 8 emojis
    selected_emojis = list(dict.fromkeys(selected_emojis))[:8]
    
    return selected_emojis