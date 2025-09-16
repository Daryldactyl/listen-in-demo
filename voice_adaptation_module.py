#!/usr/bin/env python3
"""
Voice Adaptation Module
Rewrites AI-generated LinkedIn posts in the company's authentic voice based on transcript analysis
"""

import dspy
import json
from datetime import datetime
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import re

load_dotenv()

# Configure DSPy
lm = dspy.LM('openai/google/gemini-2.5-flash', 
             api_key=os.getenv('OPENROUTER_API_KEY'), 
             api_base='https://openrouter.ai/api/v1')
dspy.configure(lm=lm)

class VoiceProfileExtractor(dspy.Signature):
    """Analyze transcript to extract the company's authentic communication patterns and voice characteristics."""
    
    transcript: str = dspy.InputField(desc="Full transcript of company conversations/presentations")
    company_context: str = dspy.InputField(desc="Brief description of what the company does")
    
    # Voice characteristics outputs
    communication_style: str = dspy.OutputField(desc="Overall communication style (direct, conversational, technical, etc.)")
    vocabulary_preferences: List[str] = dspy.OutputField(desc="Preferred technical terms, industry jargon, and key phrases they use")
    sentence_structure: str = dspy.OutputField(desc="Typical sentence patterns (short and punchy, complex technical, etc.)")
    personality_traits: List[str] = dspy.OutputField(desc="Personality traits evident in communication (confident, humble, innovative, etc.)")
    professional_tone_markers: List[str] = dspy.OutputField(desc="Elements that make their communication professional and credible")
    speaking_patterns: List[str] = dspy.OutputField(desc="Unique speaking patterns or phrases they frequently use")
    expertise_demonstration: str = dspy.OutputField(desc="How they naturally demonstrate expertise and credibility")
    engagement_approach: str = dspy.OutputField(desc="How they typically engage with their audience (questions, examples, stories, etc.)")
    voice_analysis_reasoning: str = dspy.OutputField(desc="Detailed analysis of their authentic voice characteristics")

class ProfessionalVoiceAdapter(dspy.Signature):
    """Rewrite AI-generated LinkedIn posts in the company's authentic voice while maintaining professionalism, trendjacking strategy, AND viral hook opening."""
    
    # Input content
    original_ai_post: str = dspy.InputField(desc="The original AI-generated LinkedIn post content")
    post_approach: str = dspy.InputField(desc="The approach of the original post (Professional Analogy, Educational, Conversational)")
    core_message: str = dspy.InputField(desc="The core business message that must be preserved")
    
    # Trendjacking context
    pop_culture_topic: str = dspy.InputField(desc="The trending pop culture topic being leveraged")
    trendjacking_strategy: str = dspy.InputField(desc="How the pop culture reference should be strategically used (wordplay, analogy, witty reference, etc.)")
    
    # CRITICAL: Viral hook preservation
    viral_hook: str = dspy.InputField(desc="The specific viral hook that MUST be preserved as the opening line - this hook should remain largely intact but can be adapted to match voice style")
    
    # Company voice profile
    voice_profile: str = dspy.InputField(desc="JSON string of the company's voice characteristics from transcript analysis")
    transcript_examples: str = dspy.InputField(desc="Specific examples from transcript showing their natural communication style")
    
    # Professional guidelines
    professional_requirements: str = dspy.InputField(desc="Requirements for maintaining professional LinkedIn tone while preserving trendjacking AND viral hook opening")
    
    # Rewritten content outputs
    voice_adapted_post: str = dspy.OutputField(desc="Complete LinkedIn post rewritten in the company's authentic voice with VIRAL HOOK PRESERVED as opening line and strategic trendjacking maintained")
    voice_changes_made: List[str] = dspy.OutputField(desc="Specific changes made to adapt the voice (vocabulary, tone, structure, etc.) while preserving viral hook")
    trendjacking_preserved: str = dspy.OutputField(desc="How the pop culture reference was strategically preserved (specific wordplay, analogy, or witty element used)")
    viral_hook_preserved: str = dspy.OutputField(desc="How the viral hook opening was preserved and adapted to match company voice while maintaining its attention-grabbing power")
    authenticity_score: float = dspy.OutputField(desc="How authentic the post sounds compared to their transcript voice (0-1)")
    professionalism_maintained: bool = dspy.OutputField(desc="Whether professional LinkedIn standards were maintained")
    adaptation_reasoning: str = dspy.OutputField(desc="Detailed explanation of voice adaptation choices, viral hook preservation, trendjacking maintenance, and professional adjustments")

class VoiceAdaptationPipeline(dspy.Module):
    """Complete pipeline for adapting AI-generated posts to company's authentic voice."""
    
    def __init__(self):
        self.voice_extractor = dspy.ChainOfThought(VoiceProfileExtractor)
        self.voice_adapter = dspy.ChainOfThought(ProfessionalVoiceAdapter)
    
    def extract_company_voice(self, transcript: str, company_context: str = "") -> Dict[str, Any]:
        """Extract voice characteristics from company transcript."""
        
        print(f"🎭 === VOICE PROFILE EXTRACTION ===")
        print(f"📄 Transcript length: {len(transcript)} characters")
        print(f"🏢 Company context: {company_context[:100]}...")
        
        # Extract voice profile
        voice_profile = self.voice_extractor(
            transcript=transcript,
            company_context=company_context
        )
        
        print(f"✅ Voice Profile Extracted:")
        print(f"   🗣️ Communication Style: {voice_profile.communication_style}")
        print(f"   📝 Vocabulary: {len(voice_profile.vocabulary_preferences)} key terms")
        print(f"   🎯 Personality Traits: {len(voice_profile.personality_traits)} traits identified")
        print(f"   💼 Professional Markers: {len(voice_profile.professional_tone_markers)} markers")
        
        return {
            'communication_style': voice_profile.communication_style,
            'vocabulary_preferences': voice_profile.vocabulary_preferences,
            'sentence_structure': voice_profile.sentence_structure,
            'personality_traits': voice_profile.personality_traits,
            'professional_tone_markers': voice_profile.professional_tone_markers,
            'speaking_patterns': voice_profile.speaking_patterns,
            'expertise_demonstration': voice_profile.expertise_demonstration,
            'engagement_approach': voice_profile.engagement_approach,
            'analysis_reasoning': voice_profile.voice_analysis_reasoning
        }
    
    def adapt_posts_to_voice(self, 
                           linkedin_posts: List[Dict[str, str]], 
                           voice_profile: Dict[str, Any],
                           transcript: str,
                           core_business_message: str,
                           pop_culture_topic: str = "",
                           viral_hooks: List[str] = None) -> List[Dict[str, Any]]:
        """Adapt multiple LinkedIn posts to company's authentic voice."""
        
        print(f"\n✍️ === VOICE ADAPTATION ===")
        print(f"📝 Adapting {len(linkedin_posts)} LinkedIn posts to company voice")
        if viral_hooks:
            print(f"🎣 Preserving {len(viral_hooks)} viral hooks as opening lines")
        
        adapted_posts = []
        
        # Extract key transcript examples for voice reference
        transcript_examples = self._extract_transcript_examples(transcript)
        
        # Professional requirements for LinkedIn WITH trendjacking AND viral hooks
        professional_requirements = f"""
        - Maintain professional LinkedIn tone and credibility
        - PRESERVE the strategic trendjacking of '{pop_culture_topic}' - do NOT remove the pop culture reference
        - CRITICALLY IMPORTANT: PRESERVE the viral hook as the opening line - adapt its style to match voice but keep the core hook structure
        - Use the pop culture reference strategically (wordplay, clever analogy, witty connection) but keep it professional
        - Remove any overly casual language while keeping BOTH the viral hook AND trendjacking elements
        - Ensure industry-appropriate terminology and expertise demonstration  
        - Keep engaging but business-focused messaging with strategic pop culture hook
        - Preserve authentic voice while elevating professionalism AND maintaining trendjacking value AND viral hook impact
        - The viral hook should remain attention-grabbing but professional
        """
        
        # Define trendjacking strategy based on pop culture topic
        trendjacking_strategy = self._define_trendjacking_strategy(pop_culture_topic)
        
        for i, post in enumerate(linkedin_posts, 1):
            print(f"\n🔄 Adapting Post {i}: {post.get('approach', 'Unknown')} Approach")
            
            # Get viral hook for this post (or empty string if none provided)
            current_viral_hook = ""
            if viral_hooks and i <= len(viral_hooks):
                current_viral_hook = viral_hooks[i-1]  # i is 1-based, list is 0-based
                print(f"🎣 Viral Hook: {current_viral_hook[:60]}...")
            elif post.get('viral_hook'):  # Fallback: get from post itself
                current_viral_hook = post.get('viral_hook', '')
                print(f"🎣 Viral Hook (from post): {current_viral_hook[:60]}...")
            
            adapted_result = self.voice_adapter(
                original_ai_post=post['content'],
                post_approach=post.get('approach', 'Unknown'),
                core_message=core_business_message,
                pop_culture_topic=pop_culture_topic,
                trendjacking_strategy=trendjacking_strategy,
                viral_hook=current_viral_hook,  # Pass viral hook to preserve it
                voice_profile=json.dumps(voice_profile),
                transcript_examples=transcript_examples,
                professional_requirements=professional_requirements
            )
            
            print(f"   ✅ Adaptation complete")
            print(f"   🎯 Authenticity Score: {adapted_result.authenticity_score:.2f}")
            print(f"   💼 Professional Standards: {'✅' if adapted_result.professionalism_maintained else '❌'}")
            print(f"   🎭 Trendjacking Preserved: {adapted_result.trendjacking_preserved[:50]}...")
            if hasattr(adapted_result, 'viral_hook_preserved') and current_viral_hook:
                print(f"   🎣 Viral Hook Preserved: {adapted_result.viral_hook_preserved[:50]}...")
            print(f"   📝 Changes Made: {len(adapted_result.voice_changes_made)} adjustments")
            
            adapted_posts.append({
                'post_number': i,
                'original_approach': post.get('approach', 'Unknown'),
                'original_content': post['content'],
                'original_hashtags': post.get('hashtags', ''),
                'original_viral_hook': current_viral_hook,  # Track original viral hook
                'voice_adapted_content': adapted_result.voice_adapted_post,
                'voice_changes_made': adapted_result.voice_changes_made,
                'trendjacking_preserved': adapted_result.trendjacking_preserved,
                'viral_hook_preserved': getattr(adapted_result, 'viral_hook_preserved', ''),  # Track viral hook preservation
                'authenticity_score': adapted_result.authenticity_score,
                'professionalism_maintained': adapted_result.professionalism_maintained,
                'adaptation_reasoning': adapted_result.adaptation_reasoning
            })
        
        return adapted_posts
    
    def _extract_transcript_examples(self, transcript: str, max_examples: int = 5) -> str:
        """Extract representative examples from transcript for voice reference."""
        
        # Split transcript into sentences/segments
        sentences = re.split(r'[.!?]+', transcript)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]  # Filter short fragments
        
        # Select diverse examples (beginning, middle, end)
        if len(sentences) <= max_examples:
            selected = sentences
        else:
            step = len(sentences) // max_examples
            selected = [sentences[i * step] for i in range(max_examples)]
        
        examples = "\n".join([f"• {example}" for example in selected[:max_examples]])
        return f"Representative speaking examples:\n{examples}"
    
    def _define_trendjacking_strategy(self, pop_culture_topic: str) -> str:
        """Define the trendjacking strategy based on the pop culture topic."""
        
        topic_lower = pop_culture_topic.lower()
        
        # Define strategies for different types of pop culture topics
        if "engagement" in topic_lower or "taylor swift" in topic_lower:
            return "Use 'engagement' as a double meaning - both the romantic engagement and technical engagement/commitment to production AI systems. Maintain the clever wordplay while keeping it business-focused."
        
        elif "logo" in topic_lower or "rebrand" in topic_lower or "cracker barrel" in topic_lower:
            return "Use brand identity/change themes to discuss AI system evolution and transformation. Connect visual/brand changes to technical architecture changes."
        
        elif "controversy" in topic_lower or "backlash" in topic_lower:
            return "Use the concept of 'challenging decisions' or 'bold moves' to discuss making tough technical choices in AI implementation."
        
        elif "super bowl" in topic_lower or "sports" in topic_lower:
            return "Use sports metaphors like 'game-changing,' 'winning strategy,' 'championship-level performance' for AI systems."
        
        elif "movie" in topic_lower or "trailer" in topic_lower or "entertainment" in topic_lower:
            return "Use entertainment/storytelling concepts like 'plot development,' 'behind the scenes,' 'production value' for AI development."
        
        else:
            return f"Create strategic wordplay, clever analogy, or witty professional connection between '{pop_culture_topic}' and AI/technology concepts while maintaining business relevance."
    
    def run_complete_voice_adaptation(self, 
                                    linkedin_posts: List[Dict[str, str]], 
                                    transcript: str,
                                    company_context: str,
                                    core_business_message: str,
                                    pop_culture_topic: str = "") -> Dict[str, Any]:
        """Run complete voice adaptation pipeline."""
        
        print(f"🚀 === COMPLETE VOICE ADAPTATION PIPELINE ===")
        start_time = datetime.now()
        
        try:
            # Step 1: Extract company voice profile
            voice_profile = self.extract_company_voice(transcript, company_context)
            
            # Step 2: Adapt posts to authentic voice with trendjacking preservation
            adapted_posts = self.adapt_posts_to_voice(
                linkedin_posts, voice_profile, transcript, core_business_message, pop_culture_topic
            )
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Compile results
            results = {
                'timestamp': datetime.now().isoformat(),
                'processing_time_seconds': processing_time,
                'success': True,
                'input_summary': {
                    'posts_processed': len(linkedin_posts),
                    'transcript_length': len(transcript),
                    'company_context': company_context,
                    'core_business_message': core_business_message,
                    'pop_culture_topic': pop_culture_topic
                },
                'voice_profile': voice_profile,
                'adapted_posts': adapted_posts,
                'pipeline_summary': {
                    'average_authenticity_score': sum(p['authenticity_score'] for p in adapted_posts) / len(adapted_posts) if adapted_posts else 0,
                    'professionalism_maintained': all(p['professionalism_maintained'] for p in adapted_posts),
                    'total_voice_changes': sum(len(p['voice_changes_made']) for p in adapted_posts)
                }
            }
            
            print(f"\n🎉 === VOICE ADAPTATION COMPLETE ===")
            print(f"⏱️ Processing Time: {processing_time:.2f} seconds")
            print(f"📊 Average Authenticity Score: {results['pipeline_summary']['average_authenticity_score']:.2f}")
            print(f"💼 Professional Standards: {'✅ Maintained' if results['pipeline_summary']['professionalism_maintained'] else '❌ Issues Found'}")
            print(f"📝 Total Voice Adaptations: {results['pipeline_summary']['total_voice_changes']}")
            
            return results
            
        except Exception as e:
            print(f"\n❌ VOICE ADAPTATION FAILED")
            print(f"💥 Error: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return {
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': str(e),
                'input_summary': {
                    'posts_processed': len(linkedin_posts),
                    'transcript_length': len(transcript),
                    'company_context': company_context
                }
            }

def display_voice_adaptation_results(results: Dict[str, Any]):
    """Display voice adaptation results in a formatted way."""
    
    if not results['success']:
        print(f"❌ Voice adaptation failed: {results['error']}")
        return
    
    print(f"\n🎭 === COMPANY VOICE PROFILE ===")
    voice_profile = results['voice_profile']
    print(f"🗣️ Communication Style: {voice_profile['communication_style']}")
    print(f"📝 Key Vocabulary: {', '.join(voice_profile['vocabulary_preferences'][:5])}...")
    print(f"🏗️ Sentence Structure: {voice_profile['sentence_structure']}")
    print(f"🎯 Personality Traits: {', '.join(voice_profile['personality_traits'])}")
    print(f"💡 Expertise Demo: {voice_profile['expertise_demonstration']}")
    
    print(f"\n✍️ === VOICE-ADAPTED LINKEDIN POSTS ===")
    for post in results['adapted_posts']:
        print(f"\n--- Post {post['post_number']}: {post['original_approach']} ---")
        print(f"🎯 Authenticity Score: {post['authenticity_score']:.2f}")
        print(f"💼 Professional: {'✅' if post['professionalism_maintained'] else '❌'}")
        print(f"🎭 Trendjacking: {post['trendjacking_preserved']}")
        
        print(f"\n📝 VOICE-ADAPTED CONTENT:")
        print(post['voice_adapted_content'])
        
        print(f"\n🔄 VOICE CHANGES MADE:")
        for change in post['voice_changes_made'][:3]:  # Show first 3 changes
            print(f"   • {change}")
        if len(post['voice_changes_made']) > 3:
            print(f"   • ... and {len(post['voice_changes_made']) - 3} more changes")

# Test function using the sample transcript
def test_voice_adaptation():
    """Test voice adaptation with sample transcript and generated posts."""
    
    # Sample transcript from the debrief (represents company voice)
    sample_transcript = """
    Daryl Roberts - 00:08
    Yeah, yeah. But there's also a text grad part that we can take like just that structured prompt, like the input for 
    prompt and then that will change the prompt. So we can change the prompt level, actual like value in the JSON. But 
    then DSPY is adding information for the model to use. There's a few different levels of what's happening.
    
    Cameron Barre - 00:35
    All the stuff that DSPY is adding. Is it durable? If you were to turn off the service and restart it has the same access 
    to the same information to add.
    
    Daryl Roberts - 00:45
    Yeah. After it does its training and everything, it just outputs all the new information to a JSON and then the model 
    just pulls from that JSON. As long as that JSON, nothing happens to it. It's there even if it's not there, it'll just say 
    using default node or whatever. Yeah, it's pretty nuts. It's also doing bootstrap view shot at the top of it's looking at 
    all of the training data and choosing which examples give us the best outputs.
    
    Justin Obney - 01:45
    So this is all dope. What I, what I, what will be so awesome for me is ways that I can visualize and communicate this 
    to like people of say. Because when I think of like our push of saying there's all these other layers to like the 
    engineering pieces and I kind of see this world where the frst part is. It's like a simple visualization of the agent 
    aspect of it.
    """
    
    # Sample AI-generated LinkedIn posts (from our previous demo)
    ai_generated_posts = [
        {
            'post_number': 1,
            'approach': 'Professional Analogy',
            'content': "The internet is buzzing with Taylor Swift's engagement news, and it got us thinking about \"engagement\" in enterprise AI. Just like a successful relationship needs more than just good intentions to move from dating to marriage, AI projects need more than just a prototype to move from \"ChatGPT doesn't work for us\" to production.\n\nThat's where the DSPY framework comes in. It's the engagement ring for your AI, ensuring structured prompting, modular pipelines, and measurable results. No more fleeting flings with AI ideas; it's time for a committed, high-performing partnership.\n\n#DSPY #EnterpriseAI #AIEngagement #AIStrategy #ProductionAI",
            'hashtags': '#DSPY #EnterpriseAI #AIEngagement #AIStrategy #ProductionAI #TaylorSwift'
        },
        {
            'post_number': 2, 
            'approach': 'Educational',
            'content': "What can Taylor Swift's engagement teach us about AI implementation? It's all about moving from casual interest to serious commitment. Many companies \"date\" AI with prototypes, but struggle to \"marry\" it into their core operations.\n\nThe DSPY framework provides the structure for that commitment. It's not just about building an AI model; it's about building a robust, scalable, and measurable system that delivers real business value. Think of DSPY as the pre-nup for your AI project – ensuring clarity, performance, and long-term success. Stop swiping left on AI potential and start building a lasting relationship.\n\n#AIDevelopment #DSPYFramework #BusinessAI #AITransformation #TechTrends",
            'hashtags': '#AIDevelopment #DSPYFramework #BusinessAI #AITransformation #TechTrends #TaylorSwiftEngagement'
        },
        {
            'post_number': 3,
            'approach': 'Conversational', 
            'content': "The news of Taylor Swift's engagement has everyone talking about commitment. In the world of enterprise AI, \"commitment\" means moving beyond experimental prototypes to production-ready systems that actually deliver ROI.\n\nAre you ready to commit to your AI strategy? Many businesses are stuck in the \"dating\" phase with AI, experiencing frustration when prototypes don't scale. The DSPY framework is designed to help you make that leap to a truly engaged, high-performing AI future.\n\nWhat's your biggest challenge in getting AI projects from prototype to production? Share your thoughts below!\n\n#AIChallenges #EnterpriseSolutions #DSPY #FutureofAI #TechDiscussion",
            'hashtags': '#AIChallenges #EnterpriseSolutions #DSPY #FutureofAI #TechDiscussion #TaylorSwift'
        }
    ]
    
    company_context = "AI engineering consultancy specializing in DSPY framework implementation, helping enterprises move from AI prototypes to production systems"
    core_business_message = "DSPY framework transforms prototype AI into production-ready enterprise solutions with structured prompting and measurable results"
    
    print("🧪 === TESTING VOICE ADAPTATION PIPELINE ===")
    print("Converting AI-generated posts to authentic company voice...")
    print("=" * 70)
    
    # Initialize voice adaptation pipeline
    voice_pipeline = VoiceAdaptationPipeline()
    
    # Run complete voice adaptation with trendjacking preservation
    pop_culture_topic = "Taylor Swift engagement announcement"
    
    results = voice_pipeline.run_complete_voice_adaptation(
        linkedin_posts=ai_generated_posts,
        transcript=sample_transcript,
        company_context=company_context,
        core_business_message=core_business_message,
        pop_culture_topic=pop_culture_topic
    )
    
    # Display results
    display_voice_adaptation_results(results)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"voice_adapted_posts_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Voice adaptation results saved to: {filename}")
    
    return results

if __name__ == "__main__":
    print("🎭 === VOICE ADAPTATION MODULE ===")
    print("Rewriting AI-generated LinkedIn posts in company's authentic voice")
    print("=" * 80)
    
    test_voice_adaptation()