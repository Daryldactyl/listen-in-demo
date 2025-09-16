import dspy
from dotenv import load_dotenv
import os
from typing import List, Dict

load_dotenv()

promotional_goal = """
Showcase AI Engineering Excellence: Position ourselves as the go-to experts for enterprise AI implementation with deep technical
capabilities in prompt optimization, agent training, and observability - demonstrating how we turn 'ChatGPT doesn't work for us' into
production-ready AI systems with measurable results.
"""

# Configure DSPY with OpenAI
lm = dspy.LM('openai/google/gemini-2.5-flash', api_key=os.getenv('OPENROUTER_API_KEY'), api_base='https://openrouter.ai/api/v1')
dspy.configure(lm=lm)

class TopicExtraction(dspy.Signature):
    """Extract potential LinkedIn post topics from a transcript that could support our promotional goals."""
    
    promotional_goal: str = dspy.InputField(desc="The promotional goal we want to achieve this quarter")
    transcript: str = dspy.InputField(desc="The transcript content to analyze for topics")
    topics: List[Dict[str, str]] = dspy.OutputField(desc="List of dictionaries where the topic is the key and the value is the explanation of why that topic is relevant to the promotional goal")
    evidence: Dict[str, list[str]] = dspy.OutputField(desc="List of evidence for each topic where the key is the topic and the value is a list of quotes/sections from the transcript that support the topic")

class TopicAlignment(dspy.Signature):
    """Evaluate if a topic with its explanation aligns with our promotional goal."""
    
    promotional_goal: str = dspy.InputField(desc="The promotional goal we want to achieve this quarter") 
    topic: str = dspy.InputField(desc="The topic name")
    explanation: str = dspy.InputField(desc="Explanation of the topic")
    transcript_evidence: str = dspy.InputField(desc="Relevant evidence from the transcript")
    
    aligns_with_goal: bool = dspy.OutputField(desc="Whether this topic supports our promotional goal")
    alignment_reason: str = dspy.OutputField(desc="Why this topic does or doesn't align with our goal")
    linkedin_angle: str = dspy.OutputField(desc="Specific angle for a LinkedIn post if aligned")
    confidence: float = dspy.OutputField(desc="Confidence score 0-1 for alignment assessment")

class LinkedInTopicPipeline(dspy.Module):
    """Pipeline to extract and validate LinkedIn post topics from transcripts."""
    
    def __init__(self):
        self.topic_extractor = dspy.ChainOfThought(TopicExtraction)
        self.topic_evaluator = dspy.ChainOfThought(TopicAlignment)
    
    def __call__(self, transcript: str, promotional_goal: str):
        print(f"\n📝 === TRANSCRIPT ANALYSIS PIPELINE ===")
        print(f"🎯 Promotional Goal: {promotional_goal[:100]}...")
        print(f"📄 Transcript length: {len(transcript)} characters")
        
        # Step 1: Extract potential topics with evidence
        print(f"\n🔄 Step 1: Extracting potential topics with evidence...")
        import time
        start_time = time.time()
        topics_result = self.topic_extractor(
            promotional_goal=promotional_goal,
            transcript=transcript
        )
        extraction_time = time.time() - start_time
        print(f"⏱️ Topic extraction completed in {extraction_time:.2f} seconds")
        print(f"✅ Extracted {len(topics_result.topics)} potential topics")
        
        # Step 2: Evaluate each topic for alignment using the extracted evidence
        print(f"\n🔄 Step 2: Evaluating topic alignment...")
        evaluated_topics = []
        
        for i, topic_data in enumerate(topics_result.topics, 1):
            # Get the first (and only) key-value pair from the dictionary
            topic_name = list(topic_data.keys())[0] if topic_data else ''
            topic_explanation = list(topic_data.values())[0] if topic_data else ''
            
            print(f"   📝 Evaluating topic {i}/{len(topics_result.topics)}: {topic_name}")
            
            # Get evidence for this topic from the evidence dictionary
            topic_evidence_list = topics_result.evidence.get(topic_name, [])
            # Join the evidence list into a single string for the evaluator
            topic_evidence = " ".join(topic_evidence_list)
            print(f"   📋 Evidence items: {len(topic_evidence_list)}")
            
            # Evaluate alignment
            evaluation_start_time = time.time()
            alignment_result = self.topic_evaluator(
                promotional_goal=promotional_goal,
                topic=topic_name,
                explanation=topic_explanation,
                transcript_evidence=topic_evidence
            )
            evaluation_time = time.time() - evaluation_start_time
            print(f"   ⏱️ Evaluation completed in {evaluation_time:.2f} seconds")
            
            print(f"   {'✅' if alignment_result.aligns_with_goal else '❌'} Alignment: {alignment_result.aligns_with_goal} (Confidence: {alignment_result.confidence:.2f})")
            
            evaluated_topics.append({
                'topic': topic_name,
                'explanation': topic_explanation,
                'aligns_with_goal': alignment_result.aligns_with_goal,
                'alignment_reason': alignment_result.alignment_reason,
                'linkedin_angle': alignment_result.linkedin_angle,
                'confidence': alignment_result.confidence,
                'reasoning': alignment_result.reasoning,
                'evidence_used': topic_evidence_list  # Keep as list for display
            })
        
        aligned_count = sum(1 for topic in evaluated_topics if topic['aligns_with_goal'])
        print(f"\n✅ Transcript analysis complete!")
        print(f"   📊 {aligned_count}/{len(evaluated_topics)} topics align with promotional goal")
        
        return {
            'extraction_reasoning': topics_result.reasoning,
            'evaluated_topics': evaluated_topics
        }

# Example usage
# Update the model configuration in early_test.py to match
lm = dspy.LM('openai/google/gemini-2.5-flash', api_key=os.getenv('OPENROUTER_API_KEY'), api_base='https://openrouter.ai/api/v1')
dspy.configure(lm=lm)

if __name__ == "__main__":
    # Sample transcript excerpt from the debrief
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
    
    # Initialize pipeline
    pipeline = LinkedInTopicPipeline()
    
    # Run the pipeline
    result = pipeline(sample_transcript, promotional_goal)
    
    print("=== EXTRACTION REASONING ===")
    print(result['extraction_reasoning'])
    print("\n=== EVALUATED TOPICS ===")
    
    for i, topic in enumerate(result['evaluated_topics']):
        print(f"\n--- Topic {i+1}: {topic['topic']} ---")
        print(f"Explanation: {topic['explanation']}")
        print(f"Aligns with Goal: {topic['aligns_with_goal']}")
        print(f"Confidence: {topic['confidence']}")
        print(f"LinkedIn Angle: {topic['linkedin_angle']}")
        print(f"Why: {topic['alignment_reason']}")