from transformers import pipeline
import streamlit as st
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

# Download NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

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

# Enhanced tone-specific prompt templates
TONE_TEMPLATES = {
    "Casual": "Write a relaxed, friendly social media caption about {keywords}:",
    "Professional": "Write a polished, business-appropriate caption about {keywords}:",
    "Inspirational": "Write an uplifting, motivational caption about {keywords}:",
    "Humorous": "Write a witty, entertaining caption about {keywords}:",
    "Educational": "Write an informative, educational caption about {keywords}:"
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
    templates = {
        "Casual": f"Just had an amazing experience with {keywords}! ✨",
        "Professional": f"Exploring new opportunities in {keywords}. Key insights ahead.",
        "Inspirational": f"Every journey with {keywords} teaches us something valuable. Keep growing! 🌟",
        "Humorous": f"When life gives you {keywords}, make it memorable! 😄",
        "Educational": f"Here's what I learned about {keywords} today..."
    }
    
    caption = templates.get(tone, f"Sharing my thoughts on {keywords}.")
    
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
    max_length = min(80, PLATFORM_LENGTHS[platform] // 8)  # Conservative approach
    
    try:
        # Generate text
        result = generator(
            prompt, 
            max_length=max_length, 
            num_return_sequences=1, 
            truncation=True,
            do_sample=True,
            temperature=0.8,
            pad_token_id=generator.tokenizer.eos_token_id
        )[0]['generated_text']
        
        # Clean the caption
        caption = result.replace(prompt, "").strip()
        
        # Remove incomplete sentences at the end
        sentences = re.split(r'[.!?]+', caption)
        if len(sentences) > 1 and sentences[-1].strip() and not sentences[-1].strip().endswith(('.', '!', '?')):
            caption = '. '.join(sentences[:-1]) + '.'
        elif not caption.endswith(('.', '!', '?')):
            caption = caption.rstrip() + '.'
        
        # Ensure it's not too long for the platform
        if len(caption) > PLATFORM_LENGTHS[platform] - 100:  # Leave room for hashtags
            caption = caption[:PLATFORM_LENGTHS[platform] - 100].rsplit(' ', 1)[0] + '.'
        
        # Add call-to-action if requested
        if include_cta and platform in CTA_TEMPLATES:
            cta = random.choice(CTA_TEMPLATES[platform])
            if len(caption + " " + cta) <= PLATFORM_LENGTHS[platform] - 50:  # Leave room for hashtags
                caption += " " + cta
        
        return caption
        
    except Exception as e:
        st.warning(f"AI generation failed: {str(e)}. Using fallback method.")
        return generate_fallback_caption(keywords, platform, tone, include_cta)

def suggest_hashtags(keywords, platform):
    """
    Suggest relevant hashtags based on keywords and platform.
    """
    try:
        stop_words = set(stopwords.words('english'))
    except:
        stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'])
    
    # Extract hashtags from keywords
    tokens = word_tokenize(keywords.lower())
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