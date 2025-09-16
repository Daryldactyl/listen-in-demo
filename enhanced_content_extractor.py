#!/usr/bin/env python3
"""
Enhanced Content Extractor - Uses Firecrawl for real content extraction and Playwright for visual analysis
"""

import os
import json
import base64
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import dspy
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from playwright.sync_api import sync_playwright
import tempfile
import time

load_dotenv()

@dataclass
class EnhancedExtractedContent:
    url: str
    success: bool
    content_type: str
    text_content: Optional[str] = None
    markdown_content: Optional[str] = None
    screenshot_path: Optional[str] = None
    visual_description: Optional[str] = None
    extracted_metadata: Optional[Dict] = None
    key_phrases: Optional[List[str]] = None
    viral_elements: Optional[List[str]] = None
    brand_opportunity_score: Optional[float] = None
    error_message: Optional[str] = None

class VisualContentAnalyzer(dspy.Signature):
    """Analyze webpage screenshots for viral/trending content"""
    
    url = dspy.InputField(desc="The URL being analyzed")
    trend_context = dspy.InputField(desc="Context about what trending topic this relates to")
    visual_description = dspy.InputField(desc="Description of what's visible in the screenshot")
    text_content_preview = dspy.InputField(desc="Preview of extracted text content from the page")
    
    viral_elements = dspy.OutputField(desc="Visual elements that make this content viral or shareable")
    brand_opportunity = dspy.OutputField(desc="How brands could leverage this visual trend")
    key_message = dspy.OutputField(desc="Main message or theme conveyed by the visual content")
    trending_relevance = dspy.OutputField(desc="How this visual content relates to the trending topic")

class ContentAnalyzer(dspy.Signature):
    """Analyze extracted text content for trending elements"""
    
    text_content = dspy.InputField(desc="Full text content extracted from the page")
    url = dspy.InputField(desc="The source URL")
    trend_context = dspy.InputField(desc="Context about the trending topic")
    
    trending_keywords = dspy.OutputField(desc="Key trending terms and phrases from the content")
    viral_potential = dspy.OutputField(desc="Assessment of viral potential (high/medium/low)")
    brand_angles = dspy.OutputField(desc="Potential angles brands could use based on this content")
    sentiment_tone = dspy.OutputField(desc="Overall sentiment and emotional tone")
    topic_category = dspy.OutputField(desc="Category of trending topic (entertainment, tech, etc.)")

class EnhancedContentExtractor:
    """Enhanced content extractor using Firecrawl and Playwright"""
    
    def __init__(self):
        # Initialize Firecrawl
        api_key = os.getenv('FIRECRAWL_API_KEY')
        if not api_key:
            print("⚠️  FIRECRAWL_API_KEY not found - content extraction will be limited")
            self.firecrawl_app = None
        else:
            self.firecrawl_app = FirecrawlApp(api_key=api_key)
            print("✅ Firecrawl initialized for enhanced content extraction")
        
        # Initialize DSPy safely
        from dspy_config import safe_configure_dspy, create_chain_of_thought
        
        if safe_configure_dspy():
            print("✅ DSPy configured successfully")
        else:
            print("⚠️ DSPy configuration failed - analysis will be limited")
        
        # Initialize DSPy analyzers
        self.visual_analyzer = create_chain_of_thought(VisualContentAnalyzer)
        self.content_analyzer = create_chain_of_thought(ContentAnalyzer)
    
    def extract_content_from_urls(self, urls: List[str], trend_context: str = "") -> List[EnhancedExtractedContent]:
        """Extract content from multiple URLs using Firecrawl and Playwright"""
        
        results = []
        
        for url in urls:
            print(f"🌐 Processing: {url}")
            
            try:
                # Step 1: Extract text content with Firecrawl
                text_content, markdown_content, firecrawl_metadata = self._extract_with_firecrawl(url)
                
                # Step 2: Take screenshot and analyze visually with Playwright
                screenshot_path, visual_description = self._capture_and_analyze_screenshot(url, trend_context)
                
                # Step 3: Analyze the extracted content with DSPy
                if text_content:
                    content_analysis = self.content_analyzer(
                        text_content=text_content[:2000],  # Limit to 2000 chars for analysis
                        url=url,
                        trend_context=trend_context or "General trending content analysis"
                    )
                else:
                    content_analysis = None
                
                # Step 4: Analyze visual content if we have a screenshot
                if screenshot_path and visual_description:
                    visual_analysis = self.visual_analyzer(
                        url=url,
                        trend_context=trend_context or "Visual trending content",
                        visual_description=visual_description,
                        text_content_preview=text_content[:500] if text_content else "No text content available"
                    )
                else:
                    visual_analysis = None
                
                # Compile results
                result = EnhancedExtractedContent(
                    url=url,
                    success=True,
                    content_type=self._determine_content_type(url),
                    text_content=text_content,
                    markdown_content=markdown_content,
                    screenshot_path=screenshot_path,
                    visual_description=visual_description,
                    extracted_metadata=firecrawl_metadata,
                    key_phrases=content_analysis.trending_keywords.split(', ') if content_analysis and content_analysis.trending_keywords else [],
                    viral_elements=self._extract_viral_elements(content_analysis, visual_analysis),
                    brand_opportunity_score=self._calculate_brand_score(content_analysis, visual_analysis)
                )
                
                results.append(result)
                print(f"✅ Successfully processed {url}")
                
            except Exception as e:
                error_result = EnhancedExtractedContent(
                    url=url,
                    success=False,
                    content_type="error",
                    error_message=str(e)
                )
                results.append(error_result)
                print(f"❌ Failed to process {url}: {str(e)}")
        
        return results
    
    def _extract_with_firecrawl(self, url: str) -> tuple[Optional[str], Optional[str], Optional[Dict]]:
        """Extract content using Firecrawl"""
        
        if not self.firecrawl_app:
            print("⚠️  Firecrawl not available, using basic extraction")
            return None, None, None
        
        try:
            # Use Firecrawl to get clean content - match exact format from working scraper
            result = self.firecrawl_app.scrape_url(url, params={
                'formats': ['markdown'],
                'onlyMainContent': True
            })
            
            if result and 'markdown' in result:
                text_content = result['markdown']
                markdown_content = result.get('markdown', '')
                metadata = result.get('metadata', {})
                
                print(f"🔥 Firecrawl extracted {len(text_content)} characters from {url}")
                return text_content, markdown_content, metadata
            else:
                print(f"⚠️  Firecrawl returned no content for {url}")
                return None, None, None
                
        except Exception as e:
            print(f"❌ Firecrawl error for {url}: {str(e)}")
            return None, None, None
    
    def _capture_and_analyze_screenshot(self, url: str, trend_context: str) -> tuple[Optional[str], Optional[str]]:
        """Capture screenshot using Playwright and analyze visually"""
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Set viewport for consistent screenshots
                page.set_viewport_size({"width": 1280, "height": 720})
                
                # Navigate to page
                page.goto(url, timeout=30000, wait_until="networkidle")
                
                # Wait a bit for dynamic content to load
                page.wait_for_timeout(3000)
                
                # Create temporary file for screenshot
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
                    screenshot_path = tmp_file.name
                
                # Take screenshot
                page.screenshot(path=screenshot_path, full_page=False)
                browser.close()
                
                # Analyze screenshot (create a simple visual description)
                visual_description = f"Screenshot of webpage from {url} showing the main content area and layout"
                
                print(f"📸 Screenshot captured: {screenshot_path}")
                return screenshot_path, visual_description
                
        except Exception as e:
            print(f"❌ Screenshot capture failed for {url}: {str(e)}")
            return None, None
    
    def _determine_content_type(self, url: str) -> str:
        """Determine content type based on URL patterns"""
        url_lower = url.lower()
        
        if 'knowyourmeme.com' in url_lower:
            return 'meme_page'
        elif any(platform in url_lower for platform in ['twitter.com', 'x.com', 'instagram.com', 'facebook.com', 'tiktok.com']):
            return 'social_media'
        elif any(news in url_lower for news in ['bbc.com', 'cnn.com', 'nytimes.com', 'reuters.com']):
            return 'news_article'
        elif 'youtube.com' in url_lower or 'youtu.be' in url_lower:
            return 'video_content'
        elif 'imgur.com' in url_lower:
            return 'image_hosting'
        else:
            return 'web_page'
    
    def _extract_viral_elements(self, content_analysis, visual_analysis) -> List[str]:
        """Extract viral elements from both content and visual analysis"""
        elements = []
        
        if content_analysis and content_analysis.viral_potential:
            elements.append(f"content_{content_analysis.viral_potential}")
        
        if visual_analysis and visual_analysis.viral_elements:
            elements.extend(visual_analysis.viral_elements.split(', '))
        
        return elements[:5]  # Return top 5 elements
    
    def _calculate_brand_score(self, content_analysis, visual_analysis) -> float:
        """Calculate brand opportunity score from analysis results"""
        score = 0.5  # Default score
        
        if content_analysis:
            if 'high' in content_analysis.viral_potential.lower():
                score += 0.3
            elif 'medium' in content_analysis.viral_potential.lower():
                score += 0.2
        
        if visual_analysis:
            if 'excellent' in visual_analysis.brand_opportunity.lower() or 'high' in visual_analysis.brand_opportunity.lower():
                score += 0.2
        
        return min(score, 1.0)  # Cap at 1.0

def test_enhanced_extractor():
    """Test the enhanced content extractor"""
    
    print("🚀 TESTING ENHANCED CONTENT EXTRACTOR")
    print("=" * 60)
    
    extractor = EnhancedContentExtractor()
    
    test_urls = [
        "https://knowyourmeme.com/memes/cash-me-ousside-howbow-dah",
        "https://www.bbc.com/news/entertainment-celebrity"
    ]
    
    trend_context = "Viral internet memes and celebrity news trending on social media"
    
    results = extractor.extract_content_from_urls(test_urls, trend_context)
    
    print(f"\n📊 RESULTS SUMMARY:")
    print(f"  URLs Processed: {len(results)}")
    print(f"  Successful: {len([r for r in results if r.success])}")
    print(f"  Failed: {len([r for r in results if not r.success])}")
    
    for result in results:
        if result.success:
            print(f"\n✅ {result.url}")
            print(f"  Content Type: {result.content_type}")
            print(f"  Text Length: {len(result.text_content) if result.text_content else 0} chars")
            print(f"  Screenshot: {'Yes' if result.screenshot_path else 'No'}")
            print(f"  Brand Score: {result.brand_opportunity_score:.2f}")
            print(f"  Key Phrases: {result.key_phrases[:3] if result.key_phrases else 'None'}")
        else:
            print(f"\n❌ {result.url}: {result.error_message}")

if __name__ == "__main__":
    test_enhanced_extractor()