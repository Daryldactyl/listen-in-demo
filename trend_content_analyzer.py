#!/usr/bin/env python3
"""
Trend Content Analyzer - Analyzes URLs to determine content type and extraction strategy
Handles text articles, social media posts, images, memes, videos, etc.
"""

import re
import requests
from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Any, Tuple, Optional
import mimetypes
from dataclasses import dataclass
from enum import Enum

class ContentType(Enum):
    TEXT_ARTICLE = "text_article"
    SOCIAL_POST = "social_post" 
    IMAGE_MEME = "image_meme"
    VIDEO_CONTENT = "video_content"
    MIXED_CONTENT = "mixed_content"
    UNKNOWN = "unknown"

@dataclass
class TrendContent:
    url: str
    content_type: ContentType
    extraction_strategy: str
    context_needed: bool
    visual_analysis_required: bool
    text_content: Optional[str] = None
    image_description: Optional[str] = None
    metadata: Optional[Dict] = None

class TrendContentAnalyzer:
    """Analyzes trend URLs to determine optimal content extraction strategy"""
    
    def __init__(self):
        # URL patterns for different platforms and content types
        self.platform_patterns = {
            'twitter': [r'twitter\.com', r'x\.com'],
            'instagram': [r'instagram\.com'],
            'tiktok': [r'tiktok\.com'],
            'youtube': [r'youtube\.com', r'youtu\.be'],
            'reddit': [r'reddit\.com'],
            'linkedin': [r'linkedin\.com'],
            'facebook': [r'facebook\.com', r'fb\.com'],
            'threads': [r'threads\.net'],
            'news_sites': [r'cnn\.com', r'bbc\.com', r'nytimes\.com', r'washingtonpost\.com', 
                          r'reuters\.com', r'ap\.org', r'npr\.org', r'nbcnews\.com'],
            'blog_platforms': [r'medium\.com', r'substack\.com', r'wordpress\.com', r'blogger\.com'],
            'image_hosts': [r'imgur\.com', r'giphy\.com', r'tenor\.com', r'memegenerator\.net']
        }
        
        # File extensions that indicate content type
        self.image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp']
        self.video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v']
        
        # Meme/viral content indicators
        self.meme_indicators = [
            'meme', 'viral', 'funny', 'reaction', 'gif', 'trending', 'challenge',
            'drake pointing', 'distracted boyfriend', 'woman yelling at cat',
            'this is fine', 'expanding brain', 'wojak', 'pepe', 'chad'
        ]

    def analyze_trend_urls(self, urls: List[str]) -> List[TrendContent]:
        """Analyze multiple trend URLs and return content analysis for each"""
        analyzed_trends = []
        
        for url in urls:
            try:
                trend_content = self._analyze_single_url(url)
                analyzed_trends.append(trend_content)
            except Exception as e:
                # Create error entry but continue processing other URLs
                error_content = TrendContent(
                    url=url,
                    content_type=ContentType.UNKNOWN,
                    extraction_strategy="error",
                    context_needed=True,
                    visual_analysis_required=False,
                    metadata={'error': str(e)}
                )
                analyzed_trends.append(error_content)
        
        return analyzed_trends

    def _analyze_single_url(self, url: str) -> TrendContent:
        """Analyze a single URL to determine content type and extraction needs"""
        
        # Parse URL components
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        
        # Check file extension first
        file_extension = self._get_file_extension(path)
        if file_extension in self.image_extensions:
            return self._create_image_content(url, "Direct image file")
        elif file_extension in self.video_extensions:
            return self._create_video_content(url, "Direct video file")
        
        # Identify platform
        platform = self._identify_platform(domain)
        
        # Determine content type based on platform and URL structure
        if platform == 'twitter':
            return self._analyze_twitter_url(url, parsed)
        elif platform == 'instagram':
            return self._analyze_instagram_url(url, parsed)
        elif platform == 'tiktok':
            return self._analyze_tiktok_url(url, parsed)
        elif platform == 'youtube':
            return self._analyze_youtube_url(url, parsed)
        elif platform == 'reddit':
            return self._analyze_reddit_url(url, parsed)
        elif platform in ['news_sites', 'blog_platforms']:
            return self._analyze_text_content(url, platform)
        elif platform == 'image_hosts':
            return self._analyze_image_host(url, parsed)
        else:
            # Unknown platform - try to determine from content
            return self._analyze_unknown_url(url, parsed)

    def _identify_platform(self, domain: str) -> str:
        """Identify which platform a domain belongs to"""
        for platform, patterns in self.platform_patterns.items():
            if any(re.search(pattern, domain) for pattern in patterns):
                return platform
        return 'unknown'

    def _get_file_extension(self, path: str) -> str:
        """Extract file extension from URL path"""
        return path.split('.')[-1] if '.' in path else ''

    def _analyze_twitter_url(self, url: str, parsed) -> TrendContent:
        """Analyze Twitter/X URL structure"""
        path = parsed.path
        
        # Twitter post pattern: /username/status/id
        if '/status/' in path:
            return TrendContent(
                url=url,
                content_type=ContentType.SOCIAL_POST,
                extraction_strategy="twitter_api_or_scrape",
                context_needed=True,
                visual_analysis_required=True,  # Tweets often contain images/videos
                metadata={
                    'platform': 'twitter',
                    'content_format': 'short_text_with_media',
                    'viral_potential': 'high'
                }
            )
        
        return self._create_social_post_content(url, 'twitter')

    def _analyze_instagram_url(self, url: str, parsed) -> TrendContent:
        """Analyze Instagram URL structure"""
        path = parsed.path
        
        # Instagram post patterns: /p/id, /reel/id, /stories/
        if any(pattern in path for pattern in ['/p/', '/reel/', '/stories/']):
            return TrendContent(
                url=url,
                content_type=ContentType.MIXED_CONTENT,
                extraction_strategy="visual_with_caption",
                context_needed=True,
                visual_analysis_required=True,  # Instagram is primarily visual
                metadata={
                    'platform': 'instagram',
                    'content_format': 'visual_primary_with_text',
                    'meme_potential': 'high' if '/reel/' in path else 'medium'
                }
            )
        
        return self._create_mixed_content(url, 'instagram')

    def _analyze_tiktok_url(self, url: str, parsed) -> TrendContent:
        """Analyze TikTok URL structure"""
        return TrendContent(
            url=url,
            content_type=ContentType.VIDEO_CONTENT,
            extraction_strategy="video_analysis_with_audio",
            context_needed=True,
            visual_analysis_required=True,
            metadata={
                'platform': 'tiktok',
                'content_format': 'short_video_with_audio',
                'viral_potential': 'very_high',
                'trend_type': 'dance_challenge_or_sound'
            }
        )

    def _analyze_youtube_url(self, url: str, parsed) -> TrendContent:
        """Analyze YouTube URL structure"""
        # Check if it's a short vs regular video
        is_short = '/shorts/' in parsed.path
        
        return TrendContent(
            url=url,
            content_type=ContentType.VIDEO_CONTENT,
            extraction_strategy="video_transcript_and_thumbnails",
            context_needed=True,
            visual_analysis_required=True,
            metadata={
                'platform': 'youtube',
                'content_format': 'short_video' if is_short else 'long_form_video',
                'viral_potential': 'high' if is_short else 'medium',
                'has_transcript': True
            }
        )

    def _analyze_reddit_url(self, url: str, parsed) -> TrendContent:
        """Analyze Reddit URL structure"""
        path = parsed.path
        
        # Reddit post pattern: /r/subreddit/comments/id/title
        if '/comments/' in path:
            # Determine if it's likely a meme subreddit
            meme_subreddits = ['memes', 'dankmemes', 'funny', 'wholesomememes', 'prequelmemes']
            is_meme_sub = any(sub in path for sub in meme_subreddits)
            
            return TrendContent(
                url=url,
                content_type=ContentType.IMAGE_MEME if is_meme_sub else ContentType.MIXED_CONTENT,
                extraction_strategy="reddit_post_with_comments",
                context_needed=True,
                visual_analysis_required=is_meme_sub,
                metadata={
                    'platform': 'reddit',
                    'is_meme_focused': is_meme_sub,
                    'community_context_important': True
                }
            )
        
        return self._create_mixed_content(url, 'reddit')

    def _analyze_text_content(self, url: str, platform: str) -> TrendContent:
        """Analyze news articles and blog posts"""
        return TrendContent(
            url=url,
            content_type=ContentType.TEXT_ARTICLE,
            extraction_strategy="full_text_extraction",
            context_needed=False,
            visual_analysis_required=False,
            metadata={
                'platform': platform,
                'content_format': 'long_form_text',
                'credibility': 'high' if platform == 'news_sites' else 'medium'
            }
        )

    def _analyze_image_host(self, url: str, parsed) -> TrendContent:
        """Analyze image hosting platforms"""
        path = parsed.path.lower()
        
        # Check for meme indicators in URL
        is_likely_meme = any(indicator in path or indicator in url.lower() 
                           for indicator in self.meme_indicators)
        
        return TrendContent(
            url=url,
            content_type=ContentType.IMAGE_MEME,
            extraction_strategy="image_analysis_with_context",
            context_needed=True,
            visual_analysis_required=True,
            metadata={
                'platform': 'image_host',
                'likely_meme': is_likely_meme,
                'requires_meme_knowledge': is_likely_meme
            }
        )

    def _analyze_unknown_url(self, url: str, parsed) -> TrendContent:
        """Analyze URLs from unknown platforms"""
        
        # Try to make a HEAD request to check content type
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            content_type = response.headers.get('content-type', '').lower()
            
            if content_type.startswith('image/'):
                return self._create_image_content(url, "Unknown platform image")
            elif content_type.startswith('video/'):
                return self._create_video_content(url, "Unknown platform video")
            elif content_type.startswith('text/html'):
                return self._create_text_content(url, "Unknown platform webpage")
                
        except requests.RequestException:
            pass
        
        # Fallback to mixed content with high context need
        return TrendContent(
            url=url,
            content_type=ContentType.UNKNOWN,
            extraction_strategy="comprehensive_analysis_needed",
            context_needed=True,
            visual_analysis_required=True,
            metadata={
                'platform': 'unknown',
                'requires_manual_review': True
            }
        )

    def _create_image_content(self, url: str, source: str) -> TrendContent:
        """Create image content structure"""
        return TrendContent(
            url=url,
            content_type=ContentType.IMAGE_MEME,
            extraction_strategy="image_analysis_and_ocr",
            context_needed=True,
            visual_analysis_required=True,
            metadata={'source': source, 'analysis_priority': 'visual'}
        )

    def _create_video_content(self, url: str, source: str) -> TrendContent:
        """Create video content structure"""
        return TrendContent(
            url=url,
            content_type=ContentType.VIDEO_CONTENT,
            extraction_strategy="video_frame_analysis",
            context_needed=True,
            visual_analysis_required=True,
            metadata={'source': source, 'analysis_priority': 'visual_and_audio'}
        )

    def _create_text_content(self, url: str, source: str) -> TrendContent:
        """Create text content structure"""
        return TrendContent(
            url=url,
            content_type=ContentType.TEXT_ARTICLE,
            extraction_strategy="text_extraction",
            context_needed=False,
            visual_analysis_required=False,
            metadata={'source': source, 'analysis_priority': 'text'}
        )

    def _create_social_post_content(self, url: str, platform: str) -> TrendContent:
        """Create social post content structure"""
        return TrendContent(
            url=url,
            content_type=ContentType.SOCIAL_POST,
            extraction_strategy="social_scraping",
            context_needed=True,
            visual_analysis_required=True,
            metadata={'platform': platform, 'analysis_priority': 'text_and_visual'}
        )

    def _create_mixed_content(self, url: str, platform: str) -> TrendContent:
        """Create mixed content structure"""
        return TrendContent(
            url=url,
            content_type=ContentType.MIXED_CONTENT,
            extraction_strategy="comprehensive_extraction",
            context_needed=True,
            visual_analysis_required=True,
            metadata={'platform': platform, 'analysis_priority': 'balanced'}
        )

    def generate_extraction_plan(self, analyzed_trends: List[TrendContent]) -> Dict[str, Any]:
        """Generate a comprehensive plan for extracting content from all trends"""
        
        plan = {
            'total_urls': len(analyzed_trends),
            'content_type_breakdown': {},
            'extraction_strategies': {},
            'visual_analysis_needed': 0,
            'text_only_content': 0,
            'high_context_needs': 0,
            'platform_distribution': {},
            'processing_recommendations': []
        }
        
        # Analyze the collection
        for trend in analyzed_trends:
            # Count content types
            content_type = trend.content_type.value
            plan['content_type_breakdown'][content_type] = plan['content_type_breakdown'].get(content_type, 0) + 1
            
            # Count extraction strategies
            strategy = trend.extraction_strategy
            plan['extraction_strategies'][strategy] = plan['extraction_strategies'].get(strategy, 0) + 1
            
            # Count analysis needs
            if trend.visual_analysis_required:
                plan['visual_analysis_needed'] += 1
            else:
                plan['text_only_content'] += 1
                
            if trend.context_needed:
                plan['high_context_needs'] += 1
            
            # Count platforms
            platform = trend.metadata.get('platform', 'unknown') if trend.metadata else 'unknown'
            plan['platform_distribution'][platform] = plan['platform_distribution'].get(platform, 0) + 1
        
        # Generate processing recommendations
        plan['processing_recommendations'] = self._generate_processing_recommendations(analyzed_trends, plan)
        
        return plan

    def _generate_processing_recommendations(self, trends: List[TrendContent], plan: Dict) -> List[str]:
        """Generate recommendations for processing the trend collection"""
        recommendations = []
        
        visual_pct = (plan['visual_analysis_needed'] / plan['total_urls']) * 100
        context_pct = (plan['high_context_needs'] / plan['total_urls']) * 100
        
        if visual_pct > 70:
            recommendations.append("High visual content detected - prioritize image/video analysis capabilities")
        
        if context_pct > 80:
            recommendations.append("Most content requires context - consider comprehensive extraction approach")
        
        if 'image_meme' in plan['content_type_breakdown'] and plan['content_type_breakdown']['image_meme'] > 2:
            recommendations.append("Multiple memes detected - meme knowledge base will be critical for strategy")
        
        if plan['platform_distribution'].get('twitter', 0) > 3:
            recommendations.append("Heavy Twitter content - consider real-time sentiment and engagement analysis")
        
        if len(plan['platform_distribution']) > 5:
            recommendations.append("Multi-platform trends - cross-platform strategy synthesis recommended")
        
        return recommendations

def test_analyzer():
    """Test the trend content analyzer with various URL types"""
    analyzer = TrendContentAnalyzer()
    
    test_urls = [
        "https://twitter.com/taylorswift13/status/123456789",
        "https://www.instagram.com/p/ABC123/",
        "https://imgur.com/gallery/funny-meme-abc",
        "https://www.nytimes.com/2024/01/15/business/ai-trends.html",
        "https://www.tiktok.com/@user/video/123456789",
        "https://www.reddit.com/r/memes/comments/abc123/viral_meme/",
        "https://example.com/some-image.jpg"
    ]
    
    print("🔍 TREND CONTENT ANALYZER TEST")
    print("=" * 50)
    
    analyzed_trends = analyzer.analyze_trend_urls(test_urls)
    
    for trend in analyzed_trends:
        print(f"\n📍 URL: {trend.url}")
        print(f"   Type: {trend.content_type.value}")
        print(f"   Strategy: {trend.extraction_strategy}")
        print(f"   Visual Analysis: {'Yes' if trend.visual_analysis_required else 'No'}")
        print(f"   Context Needed: {'Yes' if trend.context_needed else 'No'}")
        if trend.metadata:
            print(f"   Platform: {trend.metadata.get('platform', 'unknown')}")
    
    print("\n📊 EXTRACTION PLAN")
    print("-" * 30)
    plan = analyzer.generate_extraction_plan(analyzed_trends)
    
    print(f"Total URLs: {plan['total_urls']}")
    print(f"Visual analysis needed: {plan['visual_analysis_needed']}")
    print(f"Text-only content: {plan['text_only_content']}")
    
    print("\nContent Types:")
    for content_type, count in plan['content_type_breakdown'].items():
        print(f"  {content_type}: {count}")
    
    print("\nProcessing Recommendations:")
    for rec in plan['processing_recommendations']:
        print(f"  • {rec}")

if __name__ == "__main__":
    test_analyzer()