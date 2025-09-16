#!/usr/bin/env python3
"""
Enhanced Brand Detector V2 - Uses few-shot real examples instead of templates
Generates realistic brand posts using actual brand post examples as few-shot prompts
"""

import dspy
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from few_shot_brand_generator import FewShotBrandGenerator, BrandProfile

class EnhancedBrandDetectorV2:
    """Enhanced brand detector using few-shot examples from real brand posts"""
    
    def __init__(self):
        self.few_shot_generator = FewShotBrandGenerator()
        
        # Map trend types to response likelihood
        self.trend_response_likelihood = {
            'viral_content': 0.9,
            'real_time_event': 0.95,
            'cultural_moment': 0.8,
            'celebrity_fashion': 0.7,
            'meme_format': 0.85,
            'brand_controversy': 0.6,
            'platform_trend': 0.75,
            'seasonal_event': 0.8
        }
        
        # Engagement multipliers based on brand personality
        self.engagement_multipliers = {
            'Extremely enthusiastic, uses sour/sweet metaphors, very excitable': 2.0,  # SourPatchKids style
            'Witty roaster, competitive, never misses a chance for shade': 1.8,  # Wendy's style
            'Deadpan humor, snarky, uses minimal words for maximum impact': 1.6,  # MoonPie style
            'Weird, absurdist, late-night energy, embraces chaos': 1.5,  # Denny's style
            'Pop culture expert, observational, always ties to meat/food': 1.4,  # Arby's style
            'Trendy, relatable, always connects to coffee/drinks culture': 1.3,  # Starbucks style
            'Helpful but witty, always ties back to delivery/speed': 1.2,  # DoorDash style
            'Inspirational, athletic, focuses on achievement and perseverance': 1.1,  # Nike style
            'Warm, punny, family-friendly with bread/baking focus': 1.0,  # Panera style
            'Helpful, trendy, always suggests products, lifestyle-focused': 1.0   # Target style
        }
    
    def simulate_brand_responses(self, trending_topic: str, trend_context: str = None) -> Dict[str, Any]:
        """Simulate brand responses using few-shot generation"""
        
        # Determine trend category and response likelihood
        trend_category = self._categorize_trend(trending_topic)
        response_likelihood = self.trend_response_likelihood.get(trend_category, 0.7)
        
        # Generate enhanced context if not provided
        if not trend_context:
            trend_context = self._generate_trend_context(trending_topic, trend_category)
        
        # Determine how many brands would respond
        total_brands = len(self.few_shot_generator.brand_profiles)
        responding_brands_count = int(total_brands * response_likelihood)
        
        print(f"🎯 Generating responses from {responding_brands_count} brands using few-shot examples...")
        
        # Generate brand posts using few-shot examples
        try:
            brand_posts = self.few_shot_generator.generate_multiple_brand_posts(
                trending_topic=trending_topic,
                trend_context=trend_context,
                num_brands=responding_brands_count
            )
        except Exception as e:
            print(f"⚠️  DSPy generation failed: {e}")
            print("Using fallback simulation...")
            brand_posts = self._fallback_simulation(trending_topic, responding_brands_count)
        
        # Convert to platform-specific format and add engagement metrics
        twitter_posts = []
        linkedin_posts = []
        
        for post_data in brand_posts:
            # Create Twitter version
            twitter_post = self._create_twitter_post(post_data, trending_topic)
            twitter_posts.append(twitter_post)
            
            # Some brands also post on LinkedIn (30% chance)
            if random.random() < 0.3:
                linkedin_post = self._create_linkedin_post(post_data, trending_topic)
                linkedin_posts.append(linkedin_post)
        
        # Compile results
        results = {
            'trending_topic': trending_topic,
            'trend_context': trend_context,
            'trend_category': trend_category,
            'response_likelihood': response_likelihood,
            'total_responding_brands': len(brand_posts),
            'generation_method': 'few_shot_real_examples',
            'platforms': {
                'twitter': twitter_posts,
                'linkedin': linkedin_posts,
                'tiktok': []  # Could add TikTok later
            },
            'summary': {
                'total_posts_found': len(twitter_posts) + len(linkedin_posts),
                'verified_brand_posts': len(twitter_posts),
                'high_engagement_posts': len([p for p in twitter_posts if p.get('engagement_total', 0) > 5000]),
                'platforms_active': 2 if linkedin_posts else 1,
                'few_shot_success_rate': len([p for p in brand_posts if p.get('generation_method') == 'few_shot_dspy']) / len(brand_posts) if brand_posts else 0
            },
            'competitive_analysis': self._analyze_competitive_landscape(brand_posts),
            'few_shot_analysis': self.few_shot_generator.analyze_brand_response_patterns(brand_posts)
        }
        
        return results
    
    def _categorize_trend(self, trending_topic: str) -> str:
        """Categorize trending topic"""
        topic_lower = trending_topic.lower()
        
        if any(word in topic_lower for word in ['breaking', 'live', 'outage', 'emergency']):
            return 'real_time_event'
        elif any(word in topic_lower for word in ['viral', 'meme', 'challenge', 'trending']):
            return 'viral_content'
        elif any(word in topic_lower for word in ['celebrity', 'engagement', 'wedding', 'announcement']):
            return 'cultural_moment'
        elif any(word in topic_lower for word in ['fashion', 'outfit', 'style', 'hat']):
            return 'celebrity_fashion'
        elif any(word in topic_lower for word in ['meme format', 'template', 'little miss', 'red flag']):
            return 'meme_format'
        elif any(word in topic_lower for word in ['controversy', 'backlash', 'criticism']):
            return 'brand_controversy'
        elif any(word in topic_lower for word in ['tiktok', 'instagram', 'twitter', 'dance', 'audio']):
            return 'platform_trend'
        else:
            return 'viral_content'  # Default
    
    def _generate_trend_context(self, trending_topic: str, trend_category: str) -> str:
        """Generate context for the trend if not provided"""
        
        context_templates = {
            'viral_content': f"Viral phenomenon where {trending_topic.lower()} is spreading rapidly across social media platforms",
            'real_time_event': f"Breaking news event: {trending_topic} is happening now and capturing widespread attention",
            'cultural_moment': f"Cultural moment where {trending_topic.lower()} has captured public interest and conversation",
            'celebrity_fashion': f"Fashion/style moment where {trending_topic.lower()} has become a talking point",
            'meme_format': f"New meme format based on {trending_topic.lower()} that's perfect for brand participation",
            'brand_controversy': f"Controversial moment around {trending_topic.lower()} that brands are carefully navigating",
            'platform_trend': f"Platform-specific trend where {trending_topic.lower()} is gaining traction",
            'seasonal_event': f"Seasonal/planned event where {trending_topic.lower()} provides marketing opportunities"
        }
        
        return context_templates.get(trend_category, f"Trending topic: {trending_topic}")
    
    def _create_twitter_post(self, post_data: Dict, trending_topic: str) -> Dict[str, Any]:
        """Create Twitter post with realistic engagement"""
        
        brand = post_data['brand']
        personality = post_data.get('brand_personality', 'Standard brand personality')
        
        # Calculate engagement based on brand personality and post quality
        base_engagement = random.randint(500, 2000)
        personality_multiplier = self.engagement_multipliers.get(personality, 1.0)
        
        # Add randomness
        final_engagement = int(base_engagement * personality_multiplier * random.uniform(0.7, 1.5))
        
        # Distribute engagement
        likes = int(final_engagement * 0.6)
        retweets = int(final_engagement * 0.25)
        replies = int(final_engagement * 0.15)
        
        return {
            'platform': 'twitter',
            'username': brand.lower().replace(' ', '').replace("'", ''),
            'brand_name': brand,
            'content': post_data['post_content'],
            'trending_topic': trending_topic,
            'tactic_used': post_data['tactic_used'],
            'generation_reasoning': post_data.get('reasoning', ''),
            'brand_personality': personality,
            'real_examples_reference': post_data.get('real_examples_used', []),
            'timestamp': datetime.now().isoformat(),
            'is_brand_verified': True,
            'engagement': {
                'likes': likes,
                'retweets': retweets,
                'replies': replies
            },
            'engagement_total': final_engagement,
            'source': 'few_shot_brand_generation'
        }
    
    def _create_linkedin_post(self, post_data: Dict, trending_topic: str) -> Dict[str, Any]:
        """Create LinkedIn version (more professional)"""
        
        # Make content more professional for LinkedIn
        original_content = post_data['post_content']
        
        # Simple transformation for LinkedIn (in reality, would need more sophisticated conversion)
        professional_content = self._make_linkedin_appropriate(original_content, trending_topic)
        
        engagement_total = random.randint(50, 500)  # LinkedIn typically lower
        
        return {
            'platform': 'linkedin',
            'company': post_data['brand'],
            'content': professional_content,
            'trending_topic': trending_topic,
            'tactic_used': 'professional_commentary',
            'timestamp': datetime.now().isoformat(),
            'is_company_page': True,
            'engagement': {
                'likes': int(engagement_total * 0.7),
                'comments': int(engagement_total * 0.2),
                'shares': int(engagement_total * 0.1)
            },
            'engagement_total': engagement_total,
            'source': 'few_shot_brand_generation_linkedin'
        }
    
    def _make_linkedin_appropriate(self, content: str, trending_topic: str) -> str:
        """Convert casual content to LinkedIn-appropriate"""
        
        # Remove excessive caps and emojis for LinkedIn
        content = content.replace('!!!!!!', '.')
        
        # Add professional framing
        professional_versions = [
            f"The {trending_topic} conversation highlights the power of authentic engagement.",
            f"What {trending_topic} teaches us about brand storytelling and cultural moments.",
            f"Reflecting on how {trending_topic} demonstrates the importance of timely, relevant content.",
            f"The {trending_topic} phenomenon shows how brands can thoughtfully participate in cultural conversations."
        ]
        
        return random.choice(professional_versions)
    
    def _analyze_competitive_landscape(self, brand_posts: List[Dict]) -> Dict[str, Any]:
        """Analyze competitive landscape from generated posts"""
        
        if not brand_posts:
            return {'competition_level': 'none', 'analysis': 'No brand responses generated'}
        
        tactics_used = [post.get('tactic_used', 'unknown') for post in brand_posts]
        unique_tactics = list(set(tactics_used))
        
        # Competition level based on number of responses
        total_responses = len(brand_posts)
        if total_responses > 6:
            competition_level = 'high'
        elif total_responses > 3:
            competition_level = 'medium'
        else:
            competition_level = 'low'
        
        return {
            'competition_level': competition_level,
            'total_responses': total_responses,
            'unique_tactics': unique_tactics,
            'dominant_tactic': max(set(tactics_used), key=tactics_used.count) if tactics_used else None,
            'tactical_diversity': len(unique_tactics) / len(tactics_used) if tactics_used else 0
        }
    
    def _fallback_simulation(self, trending_topic: str, num_brands: int) -> List[Dict]:
        """Fallback when DSPy generation fails"""
        
        print("Using fallback simulation without DSPy...")
        
        # Select random brands and use their tactics
        selected_brands = random.sample(
            list(self.few_shot_generator.brand_profiles.keys()), 
            min(num_brands, len(self.few_shot_generator.brand_profiles))
        )
        
        fallback_posts = []
        for brand_name in selected_brands:
            profile = self.few_shot_generator.brand_profiles[brand_name]
            
            # Simple fallback content based on brand personality
            if 'sassy' in profile.personality.lower():
                content = f"Hot take: {trending_topic} hits different"
            elif 'punny' in profile.personality.lower():
                content = f"This {trending_topic} news has us feeling all kinds of ways"
            elif 'enthusiastic' in profile.personality.lower():
                content = f"OKAY BUT {trending_topic.upper()} THO!!!!"
            else:
                content = f"{brand_name} is here for this {trending_topic} energy"
            
            fallback_posts.append({
                'brand': brand_name,
                'post_content': content,
                'tactic_used': profile.tactics[0] if profile.tactics else 'general_participation',
                'reasoning': 'Fallback generation - DSPy unavailable',
                'brand_personality': profile.personality,
                'real_examples_used': profile.real_examples[:2],
                'generation_method': 'fallback'
            })
        
        return fallback_posts

def test_enhanced_detector_v2():
    """Test the enhanced detector with few-shot examples"""
    
    print("🚀 ENHANCED BRAND DETECTOR V2 TEST")
    print("Using few-shot real examples instead of templates")
    print("=" * 60)
    
    detector = EnhancedBrandDetectorV2()
    
    # Test with Cash Me Outside
    trending_topic = "Cash Me Outside viral catchphrase from Dr. Phil becomes internet sensation"
    trend_context = "Viral meme where teen on Dr. Phil says 'Cash me outside, how bout dah' becomes massive internet catchphrase with millions of remixes"
    
    print(f"🔥 TRENDING TOPIC: {trending_topic}")
    print(f"📝 CONTEXT: {trend_context}")
    print()
    
    # Note: This requires DSPy configuration
    print("⚠️  Note: Few-shot generation requires DSPy to be configured")
    print("If DSPy isn't configured, will use fallback simulation")
    print()
    
    try:
        results = detector.simulate_brand_responses(trending_topic, trend_context)
        
        print(f"📊 SIMULATION RESULTS:")
        print(f"   Response Likelihood: {results['response_likelihood']:.1%}")
        print(f"   Brands Responding: {results['total_responding_brands']}")
        print(f"   Generation Method: {results['generation_method']}")
        print(f"   Few-Shot Success Rate: {results['summary']['few_shot_success_rate']:.1%}")
        
        print(f"\n🐦 TWITTER RESPONSES:")
        print("-" * 40)
        
        for i, post in enumerate(results['platforms']['twitter'][:5], 1):
            print(f"\n{i}. @{post['username']} ({post['brand_name']})")
            print(f"   📱 \"{post['content']}\"")
            print(f"   🎯 Tactic: {post['tactic_used']}")
            print(f"   🎭 Personality: {post['brand_personality']}")
            print(f"   📊 Engagement: {post['engagement_total']:,}")
            
            if post.get('real_examples_reference'):
                print(f"   📚 Real Examples Used:")
                for example in post['real_examples_reference'][:2]:
                    print(f"      • \"{example}\"")
        
        print(f"\n🔍 COMPETITIVE ANALYSIS:")
        comp_analysis = results['competitive_analysis']
        print(f"   Competition Level: {comp_analysis['competition_level']}")
        print(f"   Tactics Used: {', '.join(comp_analysis['unique_tactics'])}")
        print(f"   Tactical Diversity: {comp_analysis['tactical_diversity']:.2f}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("Make sure DSPy is properly configured for few-shot generation")

if __name__ == "__main__":
    test_enhanced_detector_v2()