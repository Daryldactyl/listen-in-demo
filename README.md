# 🎭 Trendjacking Pipeline - Streamlit App

Transform your business insights into **viral LinkedIn content** by connecting them with trending topics!

## Features

✨ **Complete Trendjacking Pipeline:**
- Real-time trend analysis from URLs (articles, memes, social posts)
- Viral hook generation using proven TikTok patterns  
- Voice adaptation that preserves your authentic company voice
- Two-stage iterative refinement with conversation history context

🎯 **Smart Content Generation:**
- DSPy-powered content understanding and generation
- Few-shot learning from real brand examples
- Preserves viral hooks, trendjacking strategy, and company voice
- Multiple post formats: Question/Discussion, Personal Story, Industry Analysis

🔄 **Iterative Refinement:**
- Two-column interface for real-time post editing
- Full conversation history context for intelligent refinements
- Session state management with reset functionality
- Pipeline context viewer showing original generation reasoning

## Quick Start

1. **Configure Environment:**
   ```bash
   # Required: OpenRouter API key for DSPy/GPT-4
   export OPENROUTER_API_KEY="your_key_here"
   
   # Optional: Firecrawl API key for enhanced content extraction
   export FIRECRAWL_API_KEY="your_key_here"
   ```

2. **Input Your Data:**
   - Upload a company transcript (PDF) or paste transcript text
   - Add trending URLs (articles, memes, social posts)
   - Define your company context and goals

3. **Generate Content:**
   - Pipeline runs trend analysis once for all topics
   - Generates viral hooks using proven patterns
   - Creates voice-adapted posts preserving all constraints
   - Provides both viral and detailed post versions

4. **Refine Iteratively:**
   - Switch to "✨ Iterative Refinement" tab
   - Select posts to refine with natural language requests
   - AI uses full pipeline context for intelligent modifications
   - Real-time updates while preserving viral elements

## Deployment on Streamlit Cloud

1. Fork/clone this repository
2. Connect to Streamlit Cloud
3. Set environment variables:
   - `OPENROUTER_API_KEY` (required)
   - `FIRECRAWL_API_KEY` (optional but recommended)
4. Deploy!

## Technical Architecture

- **Frontend**: Streamlit with custom CSS and multi-tab interface
- **AI Engine**: DSPy with GPT-4.1 for content generation and refinement
- **Content Extraction**: Firecrawl + Playwright for real web scraping
- **Voice Adaptation**: Transcript-based voice profile extraction
- **State Management**: Session state for iterative refinement
- **Conversation History**: Complete pipeline context tracking

## Requirements

See `requirements.txt` for all dependencies. Key packages:
- `streamlit` - Web interface
- `dspy-ai` - AI content generation
- `firecrawl-py` - Web content extraction
- `python-dotenv` - Environment configuration