#!/usr/bin/env python3
"""
Iterative Post Refinement System
Allows users to iteratively refine generated posts with conversation history context
"""

import dspy
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
from dotenv import load_dotenv
from dspy_config import safe_configure_dspy, create_chain_of_thought

load_dotenv()

# Configure DSPy safely
safe_configure_dspy()

class PostRefinementAgent(dspy.Signature):
    """Refine a LinkedIn post based on user feedback while maintaining context from the entire generation pipeline."""
    
    # Core inputs
    current_post: str = dspy.InputField(desc="The current LinkedIn post that needs refinement")
    user_refinement_request: str = dspy.InputField(desc="Specific changes or improvements the user wants to make")
    
    # Pipeline context (full conversation history)
    pipeline_conversation_history: str = dspy.InputField(desc="Complete conversation history showing how this post was generated - includes trend analysis, viral hook generation, voice adaptation, etc.")
    
    # Original generation context
    trending_topic: str = dspy.InputField(desc="The trending topic being leveraged")
    business_topic: str = dspy.InputField(desc="The business topic being connected to the trend")
    viral_hook: str = dspy.InputField(desc="The original viral hook that was used")
    company_voice_profile: str = dspy.InputField(desc="The company's voice characteristics from transcript analysis")
    original_approach: str = dspy.InputField(desc="The original post approach (Question/Discussion, Personal Story, Industry Analysis)")
    
    # Constraints
    refinement_constraints: str = dspy.InputField(desc="Constraints that must be maintained (preserve viral hook, maintain professionalism, keep trendjacking, etc.)")
    
    # Outputs
    refined_post: str = dspy.OutputField(desc="The refined LinkedIn post incorporating user's requested changes while maintaining all original constraints and context")
    changes_made: List[str] = dspy.OutputField(desc="Specific changes made to address the user's refinement request")
    preserved_elements: List[str] = dspy.OutputField(desc="Key elements that were preserved from the original (viral hook, trendjacking, voice, etc.)")
    refinement_reasoning: str = dspy.OutputField(desc="Detailed explanation of how the refinement was approached and why specific choices were made")
    context_references_used: List[str] = dspy.OutputField(desc="Specific parts of the pipeline conversation history that were referenced to make informed refinements")

class ConversationHistoryBuilder:
    """Builds comprehensive conversation history from pipeline generation steps."""
    
    def __init__(self):
        self.messages = []
    
    def add_pipeline_step(self, step_name: str, inputs: Dict[str, Any], outputs: Dict[str, Any], reasoning: str = ""):
        """Add a pipeline step to conversation history."""
        
        message = {
            'timestamp': datetime.now().isoformat(),
            'step': step_name,
            'inputs': inputs,
            'outputs': outputs,
            'reasoning': reasoning
        }
        self.messages.append(message)
    
    def add_trend_analysis(self, trending_urls: List[str], extracted_content: Dict[str, Any], primary_topic: str):
        """Add trend analysis step."""
        self.add_pipeline_step(
            step_name="Trend Analysis",
            inputs={'trending_urls': trending_urls},
            outputs={'extracted_content': extracted_content, 'primary_trending_topic': primary_topic},
            reasoning="Analyzed trending URLs and extracted primary trending topic for trendjacking focus"
        )
    
    def add_viral_hook_generation(self, trending_topic: str, business_topic: str, generated_hooks: Dict[str, str]):
        """Add viral hook generation step."""
        self.add_pipeline_step(
            step_name="Viral Hook Generation",
            inputs={'trending_topic': trending_topic, 'business_topic': business_topic},
            outputs={'hooks': generated_hooks},
            reasoning="Generated 3 viral hooks using proven TikTok patterns to create attention-grabbing openings"
        )
    
    def add_post_generation(self, approach: str, viral_hook: str, generated_content: str, hashtags: str):
        """Add initial post generation step."""
        self.add_pipeline_step(
            step_name="Post Generation",
            inputs={'approach': approach, 'viral_hook': viral_hook},
            outputs={'content': generated_content, 'hashtags': hashtags},
            reasoning=f"Generated {approach} style post using viral hook as opening line"
        )
    
    def add_voice_adaptation(self, original_post: str, voice_profile: Dict[str, Any], adapted_post: str, changes_made: List[str]):
        """Add voice adaptation step."""
        self.add_pipeline_step(
            step_name="Voice Adaptation",
            inputs={'original_post': original_post, 'voice_profile': voice_profile},
            outputs={'adapted_post': adapted_post, 'voice_changes': changes_made},
            reasoning="Adapted post to match company's authentic voice while preserving viral hook and trendjacking elements"
        )
    
    def add_user_refinement(self, refinement_request: str, previous_post: str, refined_post: str, changes_made: List[str]):
        """Add user refinement step."""
        self.add_pipeline_step(
            step_name="User Refinement",
            inputs={'user_request': refinement_request, 'previous_post': previous_post},
            outputs={'refined_post': refined_post, 'changes_made': changes_made},
            reasoning="Applied user-requested refinements while maintaining pipeline context and constraints"
        )
    
    def remove_refinement_steps(self):
        """Remove all 'User Refinement' steps from conversation history (for reset functionality)."""
        self.messages = [msg for msg in self.messages if msg['step'] != 'User Refinement']
    
    def get_conversation_history_text(self) -> str:
        """Convert conversation history to formatted text for DSPy input."""
        
        history_text = "COMPLETE PIPELINE CONVERSATION HISTORY:\n\n"
        
        for i, message in enumerate(self.messages, 1):
            history_text += f"=== STEP {i}: {message['step']} ===\n"
            history_text += f"Timestamp: {message['timestamp']}\n\n"
            
            history_text += "INPUTS:\n"
            for key, value in message['inputs'].items():
                try:
                    if isinstance(value, (dict, list)):
                        history_text += f"  {key}: {json.dumps(value, indent=2, default=str)}\n"
                    else:
                        history_text += f"  {key}: {str(value)[:200]}{'...' if len(str(value)) > 200 else ''}\n"
                except (TypeError, ValueError):
                    # Handle non-serializable objects
                    history_text += f"  {key}: {str(value)[:200]}{'...' if len(str(value)) > 200 else ''}\n"
            
            history_text += "\nOUTPUTS:\n"
            for key, value in message['outputs'].items():
                try:
                    if isinstance(value, (dict, list)):
                        history_text += f"  {key}: {json.dumps(value, indent=2, default=str)}\n"
                    else:
                        history_text += f"  {key}: {str(value)[:200]}{'...' if len(str(value)) > 200 else ''}\n"
                except (TypeError, ValueError):
                    # Handle non-serializable objects  
                    history_text += f"  {key}: {str(value)[:200]}{'...' if len(str(value)) > 200 else ''}\n"
            
            if message['reasoning']:
                history_text += f"\nREASONING: {message['reasoning']}\n"
            
            history_text += "\n" + "="*60 + "\n\n"
        
        return history_text
    
    def save_history(self, filename: str):
        """Save conversation history to JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump({
                    'messages': self.messages,
                    'saved_at': datetime.now().isoformat()
                }, f, indent=2, default=str)
        except (TypeError, ValueError) as e:
            print(f"Warning: Could not save conversation history to {filename}: {e}")
            # Fallback: save as string representation
            with open(filename.replace('.json', '.txt'), 'w') as f:
                f.write(self.get_conversation_history_text())

class IterativePostRefiner(dspy.Module):
    """Complete system for iterative post refinement with full pipeline context."""
    
    def __init__(self):
        self.refiner = create_chain_of_thought(PostRefinementAgent)
        self.conversation_history = ConversationHistoryBuilder()
    
    def initialize_post_context(self, 
                              trending_topic: str,
                              business_topic: str,
                              viral_hook: str,
                              original_approach: str,
                              voice_profile: Dict[str, Any],
                              final_post: str) -> Dict[str, Any]:
        """Initialize post refinement context with pipeline generation data."""
        
        return {
            'trending_topic': trending_topic,
            'business_topic': business_topic, 
            'viral_hook': viral_hook,
            'original_approach': original_approach,
            'voice_profile': voice_profile,
            'original_post': final_post,  # Preserve original for reset functionality
            'current_post': final_post,
            'refinement_history': [],
            'conversation_history': self.conversation_history
        }
    
    def refine_post(self,
                   post_context: Dict[str, Any],
                   user_refinement_request: str) -> Dict[str, Any]:
        """Refine a post based on user feedback with full pipeline context."""
        
        print(f"\n🔄 === ITERATIVE POST REFINEMENT ===")
        print(f"📝 User Request: {user_refinement_request[:100]}...")
        print(f"🎯 Current Post Length: {len(post_context['current_post'])} characters")
        
        # Build refinement constraints
        refinement_constraints = f"""
        CRITICAL CONSTRAINTS - MUST BE PRESERVED:
        1. Maintain the viral hook opening: "{post_context['viral_hook'][:50]}..."
        2. Preserve trendjacking connection to: {post_context['trending_topic']}
        3. Keep business connection to: {post_context['business_topic']}
        4. Maintain company voice characteristics from voice profile
        5. Keep professional LinkedIn tone and credibility
        6. Preserve the {post_context['original_approach']} approach structure
        
        REFINEMENT FLEXIBILITY:
        - Adjust wording, tone, emphasis within constraints
        - Reorganize content structure if requested
        - Add or modify details as requested
        - Change hashtags, formatting, or style elements
        """
        
        # Get conversation history
        conversation_history_text = post_context['conversation_history'].get_conversation_history_text()
        
        # Perform refinement
        refinement_result = self.refiner(
            current_post=post_context['current_post'],
            user_refinement_request=user_refinement_request,
            pipeline_conversation_history=conversation_history_text,
            trending_topic=post_context['trending_topic'],
            business_topic=post_context['business_topic'],
            viral_hook=post_context['viral_hook'],
            company_voice_profile=json.dumps(post_context['voice_profile']),
            original_approach=post_context['original_approach'],
            refinement_constraints=refinement_constraints
        )
        
        print(f"✅ Refinement Complete!")
        print(f"📊 Changes Made: {len(refinement_result.changes_made)}")
        print(f"🔒 Elements Preserved: {len(refinement_result.preserved_elements)}")
        print(f"🧠 Context References: {len(refinement_result.context_references_used)}")
        
        # Update conversation history
        post_context['conversation_history'].add_user_refinement(
            refinement_request=user_refinement_request,
            previous_post=post_context['current_post'],
            refined_post=refinement_result.refined_post,
            changes_made=refinement_result.changes_made
        )
        
        # Update post context
        post_context['current_post'] = refinement_result.refined_post
        post_context['refinement_history'].append({
            'request': user_refinement_request,
            'changes_made': refinement_result.changes_made,
            'preserved_elements': refinement_result.preserved_elements,
            'reasoning': refinement_result.refinement_reasoning,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'refined_post': refinement_result.refined_post,
            'changes_made': refinement_result.changes_made,
            'preserved_elements': refinement_result.preserved_elements,
            'refinement_reasoning': refinement_result.refinement_reasoning,
            'context_references_used': refinement_result.context_references_used,
            'updated_context': post_context
        }

def demo_iterative_refinement():
    """Demo the iterative post refinement system."""
    
    refiner = IterativePostRefiner()
    
    # Simulate pipeline context
    post_context = refiner.initialize_post_context(
        trending_topic="Super Bowl blackout",
        business_topic="Prompt Engineering", 
        viral_hook="Superbowl organizers just made a HUGE mistake during the blackout—here's what it teaches us about prompt engineering failures...",
        original_approach="Question/Discussion",
        voice_profile={'communication_style': 'technical expert', 'personality_traits': ['innovative', 'analytical']},
        final_post="Superbowl organizers just made a HUGE mistake during the blackout—here's what it teaches us about prompt engineering failures in AI systems. When systems fail under pressure, it's rarely the technology—it's the instructions we gave them. How are you stress-testing your AI prompts? #AI #PromptEngineering #SuperBowl"
    )
    
    # Test refinement
    refinement_result = refiner.refine_post(
        post_context=post_context,
        user_refinement_request="Make this more personal and include a specific example from my own experience with AI failures"
    )
    
    print(f"\n🎉 DEMO COMPLETE!")
    print(f"Original: {post_context['current_post'][:100]}...")
    print(f"Refined: {refinement_result['refined_post'][:100]}...")

if __name__ == "__main__":
    demo_iterative_refinement()