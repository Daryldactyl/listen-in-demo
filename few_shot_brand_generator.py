#!/usr/bin/env python3
"""
Few-Shot Brand Generator - Uses real brand posts as few-shot examples to generate new posts
Based on actual brand tactics and real post examples, not generic templates
"""

import dspy
from typing import Dict, List, Any
import random
from dataclasses import dataclass

class BrandPostGenerator(dspy.Signature):
    """Generate brand posts using few-shot examples from real campaigns"""
    
    # Brand context and examples
    brand_name: str = dspy.InputField(desc="Name of the brand")
    brand_tactics: str = dspy.InputField(desc="Brand's specific tactics (e.g., sassy_commentary, food_puns)")
    real_post_examples: str = dspy.InputField(desc="Real posts this brand has made on previous trends")
    
    # New trend information
    trending_topic: str = dspy.InputField(desc="New trending topic to create posts about")
    trend_context: str = dspy.InputField(desc="Context about why this trend is viral")
    
    # Output
    generated_post: str = dspy.OutputField(desc="New brand post in the style of the real examples")
    tactic_used: str = dspy.OutputField(desc="Which tactic from the brand's repertoire was used")
    reasoning: str = dspy.OutputField(desc="Why this post fits the brand's style and the trend")

@dataclass
class BrandProfile:
    name: str
    tactics: List[str]
    real_examples: List[str]
    post_style: str
    personality: str

class FewShotBrandGenerator:
    """Generates brand posts using few-shot learning from real examples"""
    
    def __init__(self):
        # Initialize DSPy generator
        self.post_generator = dspy.ChainOfThought(BrandPostGenerator)
        
        # Real brand profiles with actual post examples
        self.brand_profiles = self._load_brand_profiles()
    
    def _load_brand_profiles(self) -> Dict[str, BrandProfile]:
        """Load brand profiles with real post examples"""
        
        profiles = {
            'DoorDash': BrandProfile(
                name='DoorDash',
                tactics=['discount_codes', 'number_references', 'delivery_puns', 'speed_claims'],
                real_examples=[
                    '13% off with code THIRTEEN',
                    'Special delivery for love stories', 
                    'We deliver happiness faster than Swift news',
                    'Delivering hot takes and cold drinks since day one'
                ],
                post_style='Punny, promotional, delivery-focused',
                personality='Helpful but witty, always ties back to delivery/speed'
            ),
            
            'Panera': BrandProfile(
                name='Panera',
                tactics=['food_puns', 'wordplay', 'product_integration', 'wholesome_messaging'],
                real_examples=[
                    'Its a loaf story, baby—just say yeast',
                    'Bread-y for love', 
                    'Sourdough and so in love',
                    'This news has us feeling all warm and toasty inside'
                ],
                post_style='Food puns, wholesome, bread-focused wordplay',
                personality='Warm, punny, family-friendly with bread/baking focus'
            ),
            
            'Starbucks': BrandProfile(
                name='Starbucks',
                tactics=['product_mentions', 'seasonal_tie_ins', 'casual_commentary', 'lifestyle_content'],
                real_examples=[
                    'Are we supposed to keep talking about PSL like nothing happened???',
                    'Love is brewing',
                    'This calls for a celebration drink',
                    'Nothing pairs better with good news than your favorite drink'
                ],
                post_style='Casual, lifestyle-focused, drink tie-ins',
                personality='Trendy, relatable, always connects to coffee/drinks culture'
            ),
            
            'SourPatchKids': BrandProfile(
                name='SourPatchKids',
                tactics=['emotional_reactions', 'caps_enthusiasm', 'personality_driven', 'sour_sweet_metaphors'],
                real_examples=[
                    'SUDDENLY I BELIEVE IN LOVE!!!!!!!!!!!!!!!',
                    'SWEET then SOUR then SWEET AGAIN',
                    'First they were sour, now theyre ENGAGED',
                    'This news has us going from sour to sweet REAL QUICK'
                ],
                post_style='High energy, caps, emotional reactions',
                personality='Extremely enthusiastic, uses sour/sweet metaphors, very excitable'
            ),
            
            'Wendys': BrandProfile(
                name='Wendys',
                tactics=['sassy_commentary', 'competitor_shade', 'viral_participation', 'roasting'],
                real_examples=[
                    'Our Twitter engagement rate > their engagement ring',
                    'Still serving hot takes and cold drinks',
                    'Spicy take: This is cute',
                    'At least someone has good taste'
                ],
                post_style='Sassy, confident, competitive shade',
                personality='Witty roaster, competitive, never misses a chance for shade'
            ),
            
            'Nike': BrandProfile(
                name='Nike',
                tactics=['motivational_tie_ins', 'just_do_it_variations', 'athlete_connections', 'inspirational_messaging'],
                real_examples=[
                    'Just Do It... together',
                    'Love wins. Always.',
                    'Champions on and off the field',
                    'Greatness comes in all forms'
                ],
                post_style='Motivational, inspiring, sports-focused',
                personality='Inspirational, athletic, focuses on achievement and perseverance'
            ),
            
            'Target': BrandProfile(
                name='Target',
                tactics=['product_suggestions', 'lifestyle_content', 'shopping_tie_ins', 'trendy_commentary'],
                real_examples=[
                    'Wedding planning essentials in aisle 12',
                    'Target run for engagement party supplies?',
                    'Love is our favorite trend',
                    'Adding this to our inspiration board'
                ],
                post_style='Shopping-focused, lifestyle, helpful suggestions',
                personality='Helpful, trendy, always suggests products, lifestyle-focused'
            ),
            
            'Arby\'s': BrandProfile(
                name='Arby\'s',
                tactics=['pop_culture_references', 'visual_puns', 'meat_puns', 'clever_observations'],
                real_examples=[
                    'Can we have our hat back?',
                    'We have the meats',
                    'Arby\'s: We Have The Meats... and the references',
                    'This looks familiar...'
                ],
                post_style='Pop culture savvy, visual references, meat-focused',
                personality='Pop culture expert, observational, always ties to meat/food'
            ),
            
            'MoonPie': BrandProfile(
                name='MoonPie',
                tactics=['snarky_observations', 'deadpan_humor', 'cosmic_references', 'simple_commentary'],
                real_examples=[
                    'lol ok',
                    'Looks like a MoonPie',
                    'We see you',
                    'Same energy'
                ],
                post_style='Deadpan, snarky, minimal words, cosmic references',
                personality='Deadpan humor, snarky, uses minimal words for maximum impact'
            ),
            
            'Denny\'s': BrandProfile(
                name='Denny\'s',
                tactics=['weird_humor', 'late_night_references', 'absurdist_content', 'meme_participation'],
                real_examples=[
                    'zoom in on the syrup',
                    '2am thoughts hit different',
                    'This is fine *pancakes on fire*',
                    'POV: You\'re a pancake at 3am'
                ],
                post_style='Weird, absurdist, late-night focused, meme-heavy',
                personality='Weird, absurdist, late-night energy, embraces chaos'
            )
        }
        
        return profiles
    
    def generate_brand_post(self, brand_name: str, trending_topic: str, trend_context: str = "") -> Dict[str, Any]:
        """Generate a brand post using few-shot examples"""
        
        if brand_name not in self.brand_profiles:
            # Fallback for unknown brands
            return self._generate_generic_post(brand_name, trending_topic)
        
        brand = self.brand_profiles[brand_name]
        
        # Format examples for few-shot
        examples_text = "\n".join([f"• {example}" for example in brand.real_examples])
        tactics_text = ", ".join(brand.tactics)
        
        # Generate new post using DSPy
        result = self.post_generator(
            brand_name=brand.name,
            brand_tactics=tactics_text,
            real_post_examples=examples_text,
            trending_topic=trending_topic,
            trend_context=trend_context if trend_context else f"Viral trending topic: {trending_topic}"
        )
        
        return {
            'brand': brand_name,
            'post_content': result.generated_post,
            'tactic_used': result.tactic_used,
            'reasoning': result.reasoning,
            'brand_personality': brand.personality,
            'real_examples_used': brand.real_examples,
            'generation_method': 'few_shot_dspy'
        }
    
    def generate_multiple_brand_posts(self, trending_topic: str, trend_context: str = "", num_brands: int = 6) -> List[Dict[str, Any]]:
        """Generate posts from multiple brands for a trending topic"""
        
        # Select brands to respond (mix of different personality types)
        selected_brands = random.sample(list(self.brand_profiles.keys()), min(num_brands, len(self.brand_profiles)))
        
        posts = []
        for brand_name in selected_brands:
            try:
                post = self.generate_brand_post(brand_name, trending_topic, trend_context)
                posts.append(post)
            except Exception as e:
                print(f"Failed to generate post for {brand_name}: {e}")
                continue
        
        return posts
    
    def _generate_generic_post(self, brand_name: str, trending_topic: str) -> Dict[str, Any]:
        """Fallback for brands not in our database"""
        
        generic_templates = [
            f"{brand_name} is here for this {trending_topic} energy",
            f"This {trending_topic} moment hits different",
            f"{brand_name} x {trending_topic} = 💯",
            f"Adding {trending_topic} to our inspiration board"
        ]
        
        return {
            'brand': brand_name,
            'post_content': random.choice(generic_templates),
            'tactic_used': 'generic_participation',
            'reasoning': 'Generic brand response - no specific examples available',
            'brand_personality': 'Unknown',
            'real_examples_used': [],
            'generation_method': 'generic_fallback'
        }
    
    def analyze_brand_response_patterns(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the patterns in generated brand responses"""
        
        tactics_used = [post['tactic_used'] for post in posts]
        unique_tactics = list(set(tactics_used))
        
        # Group posts by personality type
        personality_groups = {}
        for post in posts:
            personality = post['brand_personality']
            if personality not in personality_groups:
                personality_groups[personality] = []
            personality_groups[personality].append(post)
        
        return {
            'total_posts_generated': len(posts),
            'unique_tactics_used': unique_tactics,
            'personality_distribution': {k: len(v) for k, v in personality_groups.items()},
            'generation_success_rate': len([p for p in posts if p['generation_method'] == 'few_shot_dspy']) / len(posts),
            'sample_reasoning': posts[0]['reasoning'] if posts else None
        }

def test_few_shot_generation():
    """Test the few-shot brand post generation"""
    
    print("🎯 FEW-SHOT BRAND POST GENERATION TEST")
    print("=" * 60)
    
    generator = FewShotBrandGenerator()
    
    # Test with Cash Me Outside
    trending_topic = "Cash Me Outside viral catchphrase from Dr. Phil becomes internet sensation"
    trend_context = "Viral meme from Dr. Phil show where teen says 'Cash me outside, how bout dah' becomes internet catchphrase with millions of remixes and reactions"
    
    print(f"🔥 TRENDING TOPIC: {trending_topic}")
    print(f"📝 CONTEXT: {trend_context}")
    print()
    
    # Generate posts from multiple brands
    print("🏢 GENERATING BRAND POSTS USING FEW-SHOT EXAMPLES...")
    print("=" * 50)
    
    brand_posts = generator.generate_multiple_brand_posts(trending_topic, trend_context, num_brands=6)
    
    for i, post in enumerate(brand_posts, 1):
        print(f"\n{i}. 🎭 {post['brand'].upper()}")
        print("-" * 30)
        print(f"📱 POST: \"{post['post_content']}\"")
        print(f"🎯 TACTIC: {post['tactic_used']}")
        print(f"🧠 REASONING: {post['reasoning']}")
        print(f"🎪 PERSONALITY: {post['brand_personality']}")
        
        # Show the real examples that influenced this
        if post['real_examples_used']:
            print(f"📚 REAL EXAMPLES USED:")
            for example in post['real_examples_used'][:2]:  # Show top 2
                print(f"   • \"{example}\"")
    
    # Analysis
    analysis = generator.analyze_brand_response_patterns(brand_posts)
    
    print(f"\n📊 GENERATION ANALYSIS:")
    print("=" * 30)
    print(f"Total Posts: {analysis['total_posts_generated']}")
    print(f"Unique Tactics: {', '.join(analysis['unique_tactics_used'])}")
    print(f"Success Rate: {analysis['generation_success_rate']:.1%}")
    
    print(f"\n🎭 PERSONALITY DISTRIBUTION:")
    for personality, count in analysis['personality_distribution'].items():
        print(f"   • {personality}: {count} brands")

def test_specific_brand():
    """Test generation for a specific brand"""
    
    print(f"\n🔍 SPECIFIC BRAND TEST - WENDY'S")
    print("=" * 40)
    
    generator = FewShotBrandGenerator()
    
    # Test Wendy's specifically
    brand_profile = generator.brand_profiles['Wendys']
    print(f"Brand: {brand_profile.name}")
    print(f"Tactics: {', '.join(brand_profile.tactics)}")
    print(f"Personality: {brand_profile.personality}")
    print(f"\nReal Examples:")
    for example in brand_profile.real_examples:
        print(f"  • \"{example}\"")
    
    # Generate new post
    trending_topic = "New iPhone costs $2000, breaks price records"
    
    post = generator.generate_brand_post('Wendys', trending_topic)
    
    print(f"\n🆕 GENERATED POST:")
    print(f"Content: \"{post['post_content']}\"")
    print(f"Tactic: {post['tactic_used']}")
    print(f"Reasoning: {post['reasoning']}")

if __name__ == "__main__":
    # Set up DSPy configuration (you'll need this)
    print("⚠️  Note: This requires DSPy configuration with an LM")
    print("Configure with: dspy.configure(lm=your_language_model)")
    print()
    
    # Uncomment when you have DSPy configured:
    # test_few_shot_generation()
    # test_specific_brand()
    
    # For now, just show the system structure
    generator = FewShotBrandGenerator()
    print("🏢 LOADED BRAND PROFILES:")
    for name, profile in generator.brand_profiles.items():
        print(f"  • {name}: {len(profile.real_examples)} real examples")
    
    print(f"\nTotal brands with few-shot examples: {len(generator.brand_profiles)}")
    print("Ready to generate realistic posts using real brand examples! 🚀")