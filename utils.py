"""
Utility functions for the Social Media Caption Generator
"""

def get_platform_tips(platform):
    """Get platform-specific tips for better engagement"""
    tips = {
        "Instagram": [
            "Use 3-5 hashtags in your first comment instead of the caption",
            "Post when your audience is most active (usually 6-9 PM)",
            "Include a clear call-to-action",
            "Use Stories to drive traffic to your post",
            "Engage with comments within the first hour"
        ],
        "Twitter": [
            "Tweet during peak hours (9 AM - 3 PM)",
            "Use 1-2 relevant hashtags maximum",
            "Include images or GIFs for better engagement",
            "Retweet and reply to build community",
            "Keep it concise and punchy"
        ],
        "LinkedIn": [
            "Post during business hours (Tuesday-Thursday)",
            "Share valuable insights and lessons learned",
            "Use professional language and industry terms",
            "Tag relevant people and companies",
            "Include industry-specific hashtags"
        ],
        "Facebook": [
            "Post when your audience is online (check Insights)",
            "Ask questions to encourage comments",
            "Share behind-the-scenes content",
            "Use Facebook Groups for niche targeting",
            "Include local hashtags if relevant"
        ]
    }
    return tips.get(platform, [])

def validate_caption_length(caption, platform):
    """Validate if caption length is appropriate for the platform"""
    limits = {
        "Instagram": 2200,
        "Twitter": 280,
        "LinkedIn": 3000,
        "Facebook": 63206
    }
    
    limit = limits.get(platform, 2200)
    length = len(caption)
    
    if length <= limit * 0.8:  # 80% of limit
        return "optimal", f"✅ Perfect length ({length}/{limit} chars)"
    elif length <= limit:
        return "good", f"✅ Good length ({length}/{limit} chars)"
    else:
        return "too_long", f"⚠️ Too long ({length}/{limit} chars)"

def get_optimal_posting_times():
    """Get optimal posting times for different platforms"""
    return {
        "Instagram": "6-9 PM weekdays, 10 AM-1 PM weekends",
        "Twitter": "9 AM-3 PM weekdays",
        "LinkedIn": "8-10 AM and 12-2 PM Tuesday-Thursday", 
        "Facebook": "1-4 PM weekdays"
    }

def extract_keywords_from_caption(caption):
    """Extract potential keywords from an existing caption"""
    import re
    from nltk.corpus import stopwords
    
    try:
        stop_words = set(stopwords.words('english'))
    except:
        stop_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at'])
    
    # Remove URLs, mentions, and hashtags
    clean_caption = re.sub(r'http\S+|@\w+|#\w+', '', caption.lower())
    
    # Extract words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', clean_caption)
    
    # Filter out stop words
    keywords = [word for word in words if word not in stop_words]
    
    return list(set(keywords))[:10]  # Return unique keywords, max 10
