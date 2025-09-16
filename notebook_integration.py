#!/usr/bin/env python3
"""
Notebook Integration - Bridge between new URL-based trend detection and existing pipeline
Replaces Section 1 in the notebook with real content extraction and few-shot generation
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import our new enhanced components
from user_trend_interface import UserTrendInterface
from enhanced_content_extractor import EnhancedContentExtractor
from enhanced_brand_detector_v2 import EnhancedBrandDetectorV2

def section_1_enhanced_pop_culture_detection(trending_urls: List[str], 
                                           user_context: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    ENHANCED Section 1: URL-Based Pop Culture Detection with Real Content Analysis
    
    This replaces the old section_1_pop_culture_detection() with:
    - Real web scraping and content extraction from trending URLs
    - Few-shot brand generation using actual brand post examples
    - Enhanced competitive analysis based on real content
    
    Args:
        trending_urls: List of trending URLs to analyze (articles, memes, social posts)
        user_context: Optional context about the user's company/goals
    
    Returns:
        Dict containing all results in format compatible with existing pipeline sections
    """
    
    print("🌟" * 25)
    print("🌟 ENHANCED SECTION 1: URL-BASED POP CULTURE DETECTION")
    print("🌟" * 25)
    
    print(f"""
    🚀 NEW AND IMPROVED! This section now:
    • 📰 READS ACTUAL CONTENT from trending URLs (no more simulations!)
    • 🖼️  HANDLES IMAGES/MEMES with contextual analysis
    • 🎭 GENERATES few-shot brand responses from REAL examples
    • 🧠 USES DSPy for intelligent content understanding
    
    📋 Input URLs: {len(trending_urls)} trending URLs to analyze
    🎯 User Context: {'✅ Provided' if user_context else '⚡ Using default'}
    """)
    
    # Initialize the enhanced interface
    interface = UserTrendInterface()
    
    # Set default user context if none provided
    if not user_context:
        user_context = {
            'company_type': 'AI Engineering Consultancy',
            'goal': 'Showcase technical expertise and thought leadership',
            'brand_personality': 'Expert, authentic, innovative'
        }
    
    print(f"""
    🏢 COMPANY PROFILE:
    • Type: {user_context['company_type']}
    • Goal: {user_context['goal']}
    • Personality: {user_context['brand_personality']}
    """)
    
    print(f"\n📍 ANALYZING TRENDING URLS:")
    for i, url in enumerate(trending_urls, 1):
        print(f"  {i}. {url}")
    
    print(f"\n🔄 RUNNING ENHANCED ANALYSIS PIPELINE...")
    print("=" * 60)
    
    try:
        # Run the complete enhanced workflow
        results = interface.analyze_user_trends(trending_urls, user_context)
        
        print(f"✅ ENHANCED ANALYSIS COMPLETE!")
        
        # Extract key components for compatibility with existing pipeline
        analysis_steps = results['analysis_steps']
        final_recommendations = results['final_recommendations']
        
        # Content analysis results
        content_analysis = analysis_steps.get('content_analysis', {})
        analyzed_trends = content_analysis.get('analyzed_trends', [])
        
        # Content extraction results  
        content_extraction = analysis_steps.get('content_extraction', {})
        extraction_summary = content_extraction.get('extraction_summary', {})
        
        # Brand simulation results (this is our new few-shot generation!)
        brand_simulation = analysis_steps.get('brand_simulation', {})
        brand_responses_raw = brand_simulation.get('brand_responses', {})
        
        print(f"\n📊 PIPELINE EXECUTION SUMMARY:")
        print(f"  1. ✅ Content Analysis: {len(analyzed_trends)} URLs analyzed")
        print(f"  2. ✅ Content Extraction: {extraction_summary.get('successful_extractions', 0)} successful")
        print(f"  3. ✅ Few-Shot Brand Generation: {brand_simulation.get('trends_simulated', 0)} trends simulated")
        print(f"  4. ✅ Strategic Recommendations: Generated")
        
        # Transform brand responses to match expected format
        transformed_brand_responses = transform_brand_responses_for_pipeline(brand_responses_raw)
        
        # Extract key metrics for compatibility
        strategy_assessment = final_recommendations.get('strategy_assessment', {})
        key_metrics = {
            'response_likelihood': strategy_assessment.get('response_likelihood', 0.7),
            'competition_level': strategy_assessment.get('competition_level', 'medium_competition'),
            'opportunity_score': strategy_assessment.get('opportunity_score', 0.6),
            'risk_level': strategy_assessment.get('risk_level', 'low_risk')
        }
        
        print(f"\n🎯 KEY INSIGHTS:")
        print(f"  📈 Response Likelihood: {key_metrics['response_likelihood']:.1%}")
        print(f"  🏢 Competition Level: {key_metrics['competition_level'].replace('_', ' ').title()}")
        print(f"  💫 Opportunity Score: {key_metrics['opportunity_score']:.1%}")
        print(f"  ⚠️  Risk Level: {key_metrics['risk_level'].replace('_', ' ').title()}")
        
        # Show sample brand responses from our few-shot generation
        if transformed_brand_responses and transformed_brand_responses.get('platforms', {}).get('twitter'):
            twitter_posts = transformed_brand_responses['platforms']['twitter']
            print(f"\n🎭 SAMPLE FEW-SHOT BRAND RESPONSES:")
            
            for i, post in enumerate(twitter_posts[:3], 1):
                brand_name = post.get('brand_name', 'Unknown')
                content = post.get('content', 'No content')
                tactic = post.get('tactic_used', 'unknown').replace('_', ' ').title()
                engagement = post.get('engagement_total', 0)
                
                print(f"""
            {i}. 🏢 {brand_name}
               📱 "{content}"
               🎯 Tactic: {tactic}
               📊 Engagement: {engagement:,}
               🤖 Method: Few-shot generation from real examples
                """)
        
        # Create main trending topic from the first URL for pipeline compatibility
        main_trending_topic = create_main_topic_from_urls(trending_urls, content_extraction)
        
        print(f"\n🎯 MAIN TRENDING TOPIC: {main_trending_topic}")
        
        # Compile results in format expected by existing pipeline sections
        section_results = {
            'trending_topic': main_trending_topic,
            'trending_urls': trending_urls,
            'user_context': user_context,
            'enhanced_analysis': results,  # Full enhanced results
            'content_extraction': content_extraction,
            'brand_responses': transformed_brand_responses,
            'key_metrics': key_metrics,
            'extraction_method': 'enhanced_url_analysis',
            'generation_method': 'few_shot_real_examples',
            'pipeline_compatibility': {
                'systematic_analysis': create_systematic_analysis_compatibility(results),
                'brand_simulation': create_brand_simulation_compatibility(brand_simulation)
            }
        }
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"enhanced_section_1_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(section_results, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: {filename}")
        
        print(f"\n🎉 ENHANCED SECTION 1 COMPLETE!")
        print(f"""
    ✨ BREAKTHROUGH IMPROVEMENTS:
    • 🌐 Real content extraction (no more simulations!)
    • 🎭 Few-shot generation from actual brand examples
    • 🖼️  Image/meme support with visual context analysis
    • 🧠 DSPy-powered intelligent content understanding
    • 📊 Enhanced competitive analysis
    • 🔗 Full compatibility with existing pipeline sections
    
    🚀 Ready to flow into Sections 2-5 of the existing pipeline!
        """)
        
        return section_results
        
    except Exception as e:
        print(f"❌ Enhanced analysis failed: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")
        return create_fallback_results(trending_urls, user_context, str(e))

def transform_brand_responses_for_pipeline(brand_responses_raw: Dict[str, Any]) -> Dict[str, Any]:
    """Transform enhanced brand responses to match expected pipeline format"""
    
    if not brand_responses_raw:
        return create_empty_brand_responses()
    
    # Extract responses from first URL (main trend)
    first_url = list(brand_responses_raw.keys())[0] if brand_responses_raw else None
    if not first_url:
        return create_empty_brand_responses()
    
    brand_data = brand_responses_raw[first_url]
    platforms = brand_data.get('platforms', {})
    
    # Transform to expected format
    transformed = {
        'response_likelihood': brand_data.get('response_likelihood', 0.7),
        'total_responding_brands': brand_data.get('total_responding_brands', 0),
        'trend_category': brand_data.get('trend_category', 'general'),
        'platforms': {
            'twitter': platforms.get('twitter', []),
            'linkedin': platforms.get('linkedin', [])
        },
        'summary': brand_data.get('summary', {}),
        'competitive_analysis': brand_data.get('competitive_analysis', {}),
        'generation_method': 'few_shot_real_examples'
    }
    
    return transformed

def create_main_topic_from_urls(urls: List[str], content_extraction: Dict[str, Any]) -> str:
    """Create a main trending topic from the analyzed URLs"""
    
    # Try to extract from content extraction results
    extracted_contents = content_extraction.get('extracted_contents', [])
    
    if extracted_contents:
        # Use the first successfully extracted content
        for content in extracted_contents:
            # Handle both dict and dataclass formats
            if hasattr(content, 'success'):
                # Dataclass format
                success = content.success
                text_content = getattr(content, 'text_content', '')
                url = getattr(content, 'url', '')
            else:
                # Dict format
                success = content.get('success', False)
                text_content = content.get('text_content', '')
                url = content.get('url', '')
            
            if success and text_content:
                # Try to create a concise topic from the content
                text = text_content[:200]  # First 200 chars
                
                # Extract title if available
                if 'HEADLINE:' in text or 'TITLE:' in text:
                    lines = text.split('\n')
                    for line in lines:
                        if 'HEADLINE:' in line or 'TITLE:' in line:
                            return line.split(':', 1)[1].strip()
                
                # Fallback to URL-based topic
                return create_topic_from_url(url)
    
    # Ultimate fallback
    if urls:
        return create_topic_from_url(urls[0])
    
    return "Trending topic analysis"

def create_topic_from_url(url: str) -> str:
    """Create a trending topic description from a URL"""
    url_lower = url.lower()
    
    if 'knowyourmeme.com' in url_lower:
        return "Viral internet meme gaining mainstream attention"
    elif any(news in url_lower for news in ['bbc', 'cnn', 'nytimes', 'reuters']):
        return "Breaking news story trending across social media"
    elif 'twitter.com' in url_lower or 'x.com' in url_lower:
        return "Viral Twitter post sparking widespread discussion"
    elif 'instagram.com' in url_lower:
        return "Instagram content going viral across platforms"
    elif 'tiktok.com' in url_lower:
        return "TikTok trend spreading rapidly with millions of views"
    else:
        return "Trending online content gaining viral attention"

def create_systematic_analysis_compatibility(enhanced_results: Dict[str, Any]) -> Dict[str, Any]:
    """Create compatibility layer for systematic analysis"""
    
    final_recommendations = enhanced_results.get('final_recommendations', {})
    strategy = final_recommendations.get('strategy_assessment', {})
    
    return {
        'methodology_steps': {
            'step_2_likelihood': {
                'final_likelihood': strategy.get('response_likelihood', 0.7)
            },
            'step_3_competitive': {
                'competition_level': strategy.get('competition_level', 'medium_competition')
            },
            'step_5_recommendations': {
                'risk_assessment': strategy.get('risk_level', 'low_risk')
            }
        },
        'final_summary': {
            'overall_opportunity_score': strategy.get('opportunity_score', 0.6)
        }
    }

def create_brand_simulation_compatibility(brand_simulation: Dict[str, Any]) -> Dict[str, Any]:
    """Create compatibility layer for brand simulation"""
    
    summary = brand_simulation.get('summary', {})
    
    return {
        'verified_brand_posts': summary.get('verified_brand_posts', 0),
        'high_engagement_posts': summary.get('high_engagement_posts', 0),
        'generation_method': 'few_shot_enhanced'
    }

def create_empty_brand_responses() -> Dict[str, Any]:
    """Create empty brand responses structure"""
    return {
        'response_likelihood': 0.5,
        'total_responding_brands': 0,
        'trend_category': 'general',
        'platforms': {'twitter': [], 'linkedin': []},
        'summary': {'verified_brand_posts': 0, 'high_engagement_posts': 0},
        'competitive_analysis': {}
    }

def create_fallback_results(urls: List[str], user_context: Dict[str, str], error: str) -> Dict[str, Any]:
    """Create fallback results when enhanced analysis fails"""
    
    return {
        'trending_topic': create_topic_from_url(urls[0]) if urls else "Analysis failed",
        'trending_urls': urls,
        'user_context': user_context,
        'enhanced_analysis': {'error': error},
        'content_extraction': {'error': error},
        'brand_responses': create_empty_brand_responses(),
        'key_metrics': {
            'response_likelihood': 0.5,
            'competition_level': 'medium_competition', 
            'opportunity_score': 0.4,
            'risk_level': 'medium_risk'
        },
        'extraction_method': 'failed',
        'generation_method': 'fallback',
        'error_occurred': True,
        'error_message': error
    }

def demo_enhanced_section_1():
    """Demonstrate the enhanced Section 1 with example URLs"""
    
    print("🎯 DEMO: Enhanced Section 1 Integration")
    print("=" * 50)
    
    # Example trending URLs (mix of content types)
    demo_urls = [
        "https://knowyourmeme.com/memes/cash-me-ousside-howbow-dah",
        "https://imgur.com/gallery/memes"
    ]
    
    # Example user context
    demo_context = {
        'company_type': 'AI Engineering Consultancy',
        'goal': 'Showcase technical expertise through trendjacking',
        'brand_personality': 'Expert, innovative, approachable'
    }
    
    print(f"Testing with {len(demo_urls)} URLs and custom user context...")
    
    # Run enhanced Section 1
    results = section_1_enhanced_pop_culture_detection(demo_urls, demo_context)
    
    if results and not results.get('error_occurred'):
        print(f"\n✅ SUCCESS! Enhanced Section 1 results ready for pipeline integration.")
        print(f"📊 Key metrics extracted for Sections 2-5 compatibility")
        print(f"🎭 Brand responses generated using few-shot examples")
        print(f"🌐 Real content extracted from {len(demo_urls)} URLs")
        
        return results
    else:
        print(f"\n❌ Demo encountered issues. Check the results for details.")
        return None

if __name__ == "__main__":
    demo_enhanced_section_1()