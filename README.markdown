# 📱 Social Media Caption Generator

An AI-powered Streamlit app that generates engaging captions, hashtags, and emojis for your social media posts across different platforms.

## ✨ Features

- **Multi-Platform Support**: Instagram, LinkedIn, Twitter, Facebook
- **Tone Customization**: Casual, Professional, Inspirational, Humorous, Educational
- **Smart Content Generation**: AI-powered captions with platform-specific optimizations
- **Hashtag Suggestions**: Relevant and trending hashtags based on your content
- **Emoji Recommendations**: Context-aware emoji suggestions
- **Character Count**: Real-time character counting with platform limits
- **Multiple Variations**: Generate up to 3 caption options
- **Call-to-Action**: Optional CTAs tailored to each platform
- **Complete Post Preview**: See your entire post before publishing

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the App**:
   ```bash
   streamlit run app.py
   ```

3. **Open in Browser**: Navigate to `http://localhost:8501`

## 📋 Requirements

- Python 3.8+
- Streamlit 1.39.0+
- Transformers 4.44.2+
- NLTK 3.8.1+
- PyTorch 2.4.1+

## 🎯 How to Use

1. **Choose Platform**: Select your target social media platform
2. **Enter Keywords**: Describe your post topic or theme
3. **Select Tone**: Choose the voice that matches your brand
4. **Generate**: Click the generate button and get instant results
5. **Copy & Use**: Copy the generated content to your social media post

## 💡 Tips for Best Results

- **Be Specific**: Use detailed keywords (e.g., "morning coffee routine" vs "coffee")
- **Match Your Audience**: Choose the appropriate tone for your followers
- **Platform Optimization**: Content is automatically optimized for each platform's best practices
- **Iterate**: Try different keyword combinations for varied results

## 🛠️ Technical Details

- **AI Model**: GPT-2 for natural language generation
- **Caching**: Model loading is cached for better performance
- **Error Handling**: Graceful error handling with user-friendly messages
- **Responsive Design**: Works on desktop and mobile devices

## 📊 Platform Specifications

| Platform | Character Limit | Best Practices |
|----------|----------------|----------------|
| Instagram | 2,200 | Visual storytelling, hashtags |
| Twitter | 280 | Concise, trending topics |
| LinkedIn | 3,000 | Professional, value-driven |
| Facebook | 63,206 | Community engagement |

## 🔧 Performance Optimizations

- **Model Caching**: AI model is loaded once and cached
- **Efficient Processing**: Optimized text generation parameters
- **Session State**: Generated content persists during session
- **Error Recovery**: Robust error handling for better user experience

## 🚀 Deployment

To deploy on Streamlit Cloud:
1. Push your code to a GitHub repository
2. Sign in to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app, link your GitHub repository, and specify `app.py` as the main file
4. Deploy the app and share the public URL

## 🤝 Contributing

Feel free to contribute by:
- Reporting bugs
- Suggesting new features
- Improving the AI prompts
- Adding more platform support

## 📄 License

MIT License

---

**Built with ❤️ using Streamlit and AI**