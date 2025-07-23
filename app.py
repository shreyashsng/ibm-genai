import streamlit as st
from caption_generator import generate_caption, suggest_hashtags, suggest_emojis

# Streamlit app configuration
st.set_page_config(
    page_title="Social Media Caption Generator", 
    layout="wide",
    page_icon="📱",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
.result-box {
    background-color: #f0f2f6;
    padding: 1rem;
    border-radius: 0.5rem;
    border-left: 4px solid #1f77b4;
    margin: 1rem 0;
}
.copy-button {
    background-color: #1f77b4;
    color: white;
    border: none;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    font-size: 0.8rem;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("📱 Social Media Caption Generator")
st.markdown("Create engaging captions, hashtags, and emojis for your social media posts!")

col1, col2 = st.columns([1.5, 1])

with col1:
    st.header("🎯 Content Settings")
    platform = st.selectbox("📱 Platform", ["Instagram", "LinkedIn", "Twitter", "Facebook"])
    keywords = st.text_area("🔑 Keywords/Theme", 
                           placeholder="e.g., travel adventure, morning coffee, team success",
                           help="Enter keywords or describe what your post is about")
    tone = st.selectbox("🎭 Tone", ["Casual", "Professional", "Inspirational", "Humorous", "Educational"])
    st.markdown("---")
    st.subheader("⚙️ Advanced Options")
    num_captions = st.slider("Number of caption variations", 1, 3, 1)
    include_cta = st.checkbox("Include Call-to-Action", value=True)
    generate_clicked = st.button("🚀 Generate Content", type="primary", use_container_width=True)

    if generate_clicked:
        if keywords.strip():
            with st.spinner("🤖 AI is crafting your content..."):
                try:
                    captions = []
                    for i in range(num_captions):
                        caption = generate_caption(keywords, platform, tone, include_cta)
                        captions.append(caption)
                    hashtags = suggest_hashtags(keywords, platform)
                    emojis = suggest_emojis(keywords, platform)
                    st.session_state.generated_content = {
                        'captions': captions,
                        'hashtags': hashtags,
                        'emojis': emojis,
                        'platform': platform
                    }
                except Exception as e:
                    st.error(f"❌ Error generating content: {str(e)}")
        else:
            st.error("⚠️ Please enter keywords or a theme to generate content.")

    # Display results or placeholder
    if 'generated_content' in st.session_state:
        content = st.session_state.generated_content
        st.markdown("## 📝 Generated Content")
        for i, caption in enumerate(content['captions']):
            if len(content['captions']) > 1:
                st.markdown(f"### Caption Option {i+1}")
            else:
                st.markdown("### Generated Caption")
            char_count = len(caption)
            platform_limits = {"Instagram": 2200, "Twitter": 280, "LinkedIn": 3000, "Facebook": 63206}
            limit = platform_limits.get(content['platform'], 2200)
            if char_count <= limit:
                st.success(f"✅ {char_count}/{limit} characters")
            else:
                st.warning(f"⚠️ {char_count}/{limit} characters (over limit)")
            st.text_area(f"caption_{i}", value=caption, height=100, key=f"caption_text_{i}")
        st.markdown("### 🏷️ Suggested Hashtags")
        hashtag_text = " ".join(content['hashtags'])
        st.text_area("hashtags", value=hashtag_text, height=60, key="hashtags_text")
        st.markdown("### 😊 Suggested Emojis")
        emoji_text = " ".join(content['emojis'])
        st.text_area("emojis", value=emoji_text, height=40, key="emojis_text")
        st.markdown("### 🎯 Complete Post Preview")
        complete_post = f"{content['captions'][0]}\n\n{hashtag_text} {emoji_text}"
        st.text_area("complete_post", value=complete_post, height=150, key="complete_post_text")
    else:
        st.markdown("<div style='margin-top:2rem; color:#888;'>📝 <b>Enter your content settings and click Generate to see results here.</b></div>", unsafe_allow_html=True)

with col2:
    st.markdown("### 💡 Tips")
    st.info("""
    **Best Practices:**
    - Use specific keywords
    - Match tone to your audience
    - Keep captions engaging
    - Use relevant hashtags
    - Don't overuse emojis
    """)
    st.markdown("### 📏 Character Limits")
    limits = {
        "Instagram": "2,200",
        "Twitter": "280", 
        "LinkedIn": "3,000",
        "Facebook": "63,206"
    }
    for platform, limit in limits.items():
        st.text(f"{platform}: {limit}")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and AI by [Shreyash Singh](https://github.com/shreyashsng) | **Tip:** Bookmark this page for quick access!")