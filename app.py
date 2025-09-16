import streamlit as st
import sys
import os
import PyPDF2
import tempfile
import json
from pathlib import Path
from typing import List, Dict, Any
import time
import dspy

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import trendjacking modules with error handling
try:
    from notebook_integration import section_1_enhanced_pop_culture_detection as enhanced_section_1
    from voice_adaptation_module import VoiceAdaptationPipeline
    from concise_structure_generator import ConciseStructureGenerator
    from iterative_post_refiner import IterativePostRefiner, ConversationHistoryBuilder
    TRENDJACKING_AVAILABLE = True
except ImportError as e:
    st.error(f"Error importing trendjacking pipeline: {e}")
    TRENDJACKING_AVAILABLE = False

try:
    # Import transcript analysis
    from early_test import LinkedInTopicPipeline
    TRANSCRIPT_PIPELINE_AVAILABLE = True
except ImportError as e:
    st.warning(f"Transcript analysis not available: {e}")
    TRANSCRIPT_PIPELINE_AVAILABLE = False

st.set_page_config(
    page_title="Trendjacking Pipeline", 
    page_icon="🎭", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Custom styling for post cards */
    .post-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #333333;
    }
    
    .post-card h4 {
        color: #2c3e50;
        margin-bottom: 15px;
    }
    
    .post-card p {
        color: #555555;
        line-height: 1.6;
    }
    
    .post-card strong {
        color: #2c3e50;
    }
    
    .viral-post {
        border-left-color: #ff6b6b;
        background: #fff5f5;
        color: #333333;
    }
    
    .voice-post {
        border-left-color: #4ecdc4;
        background: #f0fffe;
        color: #333333;
    }
    
    .post-content {
        background: white;
        padding: 20px;
        border-radius: 8px;
        margin: 15px 0;
        color: #2c3e50 !important;
        border: 1px solid #e0e0e0;
        line-height: 1.8;
        font-size: 1.1em;
    }
    
    .topic-card {
        background: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin-bottom: 10px;
        color: #333333;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .metric-card h4, .metric-card p {
        color: white !important;
    }
    
    .trend-url {
        background: #e8f4f8;
        padding: 8px 12px;
        border-radius: 6px;
        border-left: 3px solid #00a8cc;
        margin: 5px 0;
        font-family: monospace;
        font-size: 0.9em;
        color: #2c3e50;
    }
    
    /* Fix any white text issues */
    .post-card div, .post-card span {
        color: #333333;
    }
</style>
""", unsafe_allow_html=True)

def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

def extract_text_from_docx(uploaded_file):
    """Extract text from uploaded DOCX file"""
    try:
        import docx
        doc = docx.Document(uploaded_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except ImportError:
        st.error("python-docx not installed. Install with: pip install python-docx")
        return None
    except Exception as e:
        st.error(f"Error reading DOCX: {e}")
        return None

def clean_transcript(text):
    """Basic transcript cleaning"""
    if not text:
        return ""
    
    import re
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

def extract_topics_from_transcript(transcript_text, promotional_goal):
    """Extract LinkedIn topics from transcript"""
    if not TRANSCRIPT_PIPELINE_AVAILABLE:
        # Create mock topics for demo
        return [
            {
                'topic': 'DSPy Framework Implementation',
                'explanation': 'Using structured prompting for production AI systems',
                'linkedin_angle': 'How DSPy transforms prototype AI into enterprise solutions',
                'confidence': 0.85,
                'aligns_with_goal': True
            },
            {
                'topic': 'AI Engineering Best Practices',
                'explanation': 'Building scalable AI systems with proper observability',
                'linkedin_angle': 'The engineering discipline behind successful AI deployment',
                'confidence': 0.78,
                'aligns_with_goal': True
            }
        ]
    
    try:
        with st.spinner("🤖 Analyzing transcript and extracting topics..."):
            pipeline = LinkedInTopicPipeline()
            result = pipeline(transcript_text, promotional_goal)
        
        if result and 'evaluated_topics' in result:
            aligned_topics = [
                topic for topic in result['evaluated_topics'] 
                if topic.get('aligns_with_goal', False)
            ]
            return aligned_topics
        else:
            st.error("Failed to extract topics")
            return []
            
    except Exception as e:
        st.error(f"Error during topic extraction: {str(e)}")
        return []

class ViralHookGenerator(dspy.Signature):
    """Generate 3 different viral hooks using these proven patterns from TikTok viral video analysis.
    
    Use these EXACT proven viral hook patterns as templates:
    1. "[Famous Person/Company] just made a HUGE mistake..."
    2. "What are some weird things people don't know about [topic]..."
    3. "This is the most interesting thing in the last decade..."
    4. "I don't think people understand [topic]..."
    5. "Am I the only one that didn't know [topic]..."
    6. "Everybody's looking for [fundamental human desire]..."
    7. "This is the secret to..."
    
    INSTRUCTIONS:
    - Pick 3 DIFFERENT patterns from the 7 above
    - Adapt each pattern to connect trending topic with business topic
    - Keep the hook structure but customize the content
    - Make them LinkedIn-appropriate but still attention-grabbing
    
    EXAMPLES of adaptation:
    - Pattern 1: "Netflix just made a HUGE mistake with their password sharing crackdown..."
    - Pattern 4: "I don't think people understand what the Super Bowl blackout teaches us about AI systems..."
    - Pattern 6: "Everybody's looking for reliable AI, but here's what the Oreo blackout moment shows us..."
    """
    
    trending_topic = dspy.InputField(desc="The trending topic to reference")
    business_topic = dspy.InputField(desc="The business topic to connect to")
    company_type = dspy.InputField(desc="Type of company for context")
    
    hook_1 = dspy.OutputField(desc="First viral hook using one of the 7 patterns above - adapt it to connect trending topic with business topic")
    hook_2 = dspy.OutputField(desc="Second viral hook using a DIFFERENT pattern from the 7 - must use a completely different pattern structure than hook 1")
    hook_3 = dspy.OutputField(desc="Third viral hook using yet ANOTHER different pattern from the 7 - must be unique pattern from hooks 1 and 2")

class PostApproachGenerator(dspy.Signature):
    """Generate 3 DRAMATICALLY different LinkedIn posts using the provided viral hooks.
    
    Use the viral hooks as opening lines and build completely different posts around them:
    
    POST 1: Question/Discussion Format
    - Start with hook_1, then develop into thought-provoking questions
    - Use conversational, engaging tone
    - End with questions to spark community discussion
    
    POST 2: Personal Story/Anecdote Format  
    - Start with hook_2, then share personal experience/observation
    - Use "I" statements and personal perspective after the hook
    - Tell a brief story connecting the hook to business insights
    
    POST 3: Industry Analysis/List Format
    - Start with hook_3, then provide analytical breakdown
    - Use bullet points or numbered insights after the hook
    - Professional, expert tone with actionable takeaways
    
    CRITICAL:
    - Each hook creates a completely different post style
    - Don't repeat similar structures across posts
    - Build meaningful content after each viral hook
    - Connect hooks to business insights naturally
    """
    
    trending_topic = dspy.InputField(desc="The trending topic or viral content")
    business_topic = dspy.InputField(desc="The business topic to connect with the trend")
    topic_explanation = dspy.InputField(desc="Explanation of the business topic")
    linkedin_angle = dspy.InputField(desc="The LinkedIn angle for the business topic")
    promotional_goal = dspy.InputField(desc="Company's promotional goal")
    brand_personality = dspy.InputField(desc="Company's brand personality traits")
    company_type = dspy.InputField(desc="Type of company")
    
    # Generated viral hooks as inputs
    hook_1 = dspy.InputField(desc="First viral hook to use as opening for post 1")
    hook_2 = dspy.InputField(desc="Second viral hook to use as opening for post 2") 
    hook_3 = dspy.InputField(desc="Third viral hook to use as opening for post 3")
    
    approach_1_name = dspy.OutputField(desc="Name: Question/Discussion approach")
    approach_1_content = dspy.OutputField(desc="Start with hook_1 as opening line, then develop into question format with 2-3 follow-up questions to spark discussion. Conversational tone.")
    approach_1_hashtags = dspy.OutputField(desc="3-5 relevant hashtags for question post")
    
    approach_2_name = dspy.OutputField(desc="Name: Personal Story approach")
    approach_2_content = dspy.OutputField(desc="Start with hook_2 as opening line, then share personal experience using 'I' statements, tell brief story connecting to business insight. Authentic tone.")
    approach_2_hashtags = dspy.OutputField(desc="3-5 relevant hashtags for personal post")
    
    approach_3_name = dspy.OutputField(desc="Name: Industry Analysis approach") 
    approach_3_content = dspy.OutputField(desc="Start with hook_3 as opening line, then provide analytical breakdown with bullet points or numbered list (3-5 points). Professional expert tone.")
    approach_3_hashtags = dspy.OutputField(desc="3-5 relevant hashtags for analysis post")

def generate_dynamic_post_approaches(trending_topic, business_topic, topic_explanation, 
                                   linkedin_angle, promotional_goal, brand_personality, company_type):
    """Generate 3 contextual post approaches using viral hooks + DSPy (two-stage approach)"""
    
    try:
        # STAGE 1: Generate 3 different viral hooks
        hook_generator = dspy.ChainOfThought(ViralHookGenerator)
        
        hooks_result = hook_generator(
            trending_topic=trending_topic,
            business_topic=business_topic,
            company_type=company_type
        )
        
        print(f"🎣 Generated viral hooks:")
        print(f"  Hook 1: {hooks_result.hook_1}")
        print(f"  Hook 2: {hooks_result.hook_2}")  
        print(f"  Hook 3: {hooks_result.hook_3}")
        
        # STAGE 2: Use hooks to generate diverse posts
        generator = dspy.ChainOfThought(PostApproachGenerator)
        
        result = generator(
            trending_topic=trending_topic,
            business_topic=business_topic,
            topic_explanation=topic_explanation,
            linkedin_angle=linkedin_angle,
            promotional_goal=promotional_goal,
            brand_personality=brand_personality,
            company_type=company_type,
            hook_1=hooks_result.hook_1,
            hook_2=hooks_result.hook_2,
            hook_3=hooks_result.hook_3
        )
        
        # Format the results
        approaches = [
            {
                'name': result.approach_1_name,
                'content': result.approach_1_content,
                'hashtags': result.approach_1_hashtags,
                'viral_hook': hooks_result.hook_1
            },
            {
                'name': result.approach_2_name,
                'content': result.approach_2_content,
                'hashtags': result.approach_2_hashtags,
                'viral_hook': hooks_result.hook_2
            },
            {
                'name': result.approach_3_name,
                'content': result.approach_3_content,
                'hashtags': result.approach_3_hashtags,
                'viral_hook': hooks_result.hook_3
            }
        ]
        
        return approaches
        
    except Exception as e:
        st.warning(f"⚠️ Dynamic approach generation failed: {e}")
        # Fallback to diverse examples
        return [
            {
                'name': 'Thought Leadership',
                'content': f"The recent buzz around {trending_topic} got me thinking about {business_topic}. {linkedin_angle} As leaders in {company_type.lower()}, how we approach this matters.",
                'hashtags': '#leadership #innovation #insights'
            },
            {
                'name': 'Personal Connection',
                'content': f"Seeing {trending_topic} everywhere reminds me why {business_topic} is so crucial right now. {topic_explanation[:100]}... What's your take?",
                'hashtags': '#perspective #discussion #business'
            },
            {
                'name': 'Industry Analysis',
                'content': f"While everyone's talking about {trending_topic}, let's discuss its connection to {business_topic}. {linkedin_angle} The implications for our industry are significant.",
                'hashtags': '#analysis #industry #trends'
            }
        ]

def extract_primary_trending_topic(pop_culture_results, user_context):
    """Extract the primary trending topic using user context and content analysis"""
    
    # Priority 1: Use user-provided trend context if available (most reliable)
    if user_context.get('trend_context'):
        user_trend_context = user_context['trend_context'].strip()
        if user_trend_context:
            # Use the user context as-is - they know best what the trend is about
            return user_trend_context
    
    # Priority 2: Extract from analyzed content using the intelligent context creation
    content_extraction = pop_culture_results.get('content_extraction', {})
    extracted_contents = content_extraction.get('extracted_contents', [])
    
    if extracted_contents:
        # Use the same intelligent context creation logic from the interface
        for content in extracted_contents:
            if hasattr(content, 'success') and content.success:
                # Use key phrases if available (from DSPy analysis)
                if hasattr(content, 'key_phrases') and content.key_phrases:
                    key_context = ", ".join(content.key_phrases[:4])
                    return key_context
                
                # Fallback to content analysis
                if hasattr(content, 'text_content') and content.text_content:
                    # Look for title/headline in first few lines
                    lines = content.text_content.split('\n')[:5]
                    for line in lines:
                        line = line.strip()
                        if len(line) > 10 and len(line) < 150:  # Reasonable title length
                            return line
    
    # Priority 3: Use the main trending topic from analysis
    main_topic = pop_culture_results.get('trending_topic', 'General trending topic')
    
    return main_topic

def display_topic_selection(topics):
    """Display topics with selection checkboxes"""
    if not topics:
        st.warning("No topics found. Try adjusting your promotional goal or uploading a different transcript.")
        return []
    
    st.subheader(f"📊 Found {len(topics)} Topics")
    st.markdown("Select the topics you want to enhance with trending content:")
    
    # Sort by confidence
    sorted_topics = sorted(topics, key=lambda x: x.get('confidence', 0), reverse=True)
    
    selected_topics = []
    
    for i, topic in enumerate(sorted_topics):
        topic_id = f"topic_{i}"
        
        # Create expandable topic card
        with st.expander(f"📝 {topic.get('topic', 'Unknown Topic')} (Confidence: {topic.get('confidence', 0):.2f})", expanded=i<2):
            
            # Checkbox for selection
            is_selected = st.checkbox(
                "Select this topic for trendjacking",
                key=f"select_{topic_id}",
                value=i<2  # Auto-select first 2 topics
            )
            
            # Topic details in columns
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write("**Explanation:**")
                st.write(topic.get('explanation', 'No explanation provided'))
                
                if topic.get('linkedin_angle'):
                    st.write("**LinkedIn Angle:**")
                    st.write(topic.get('linkedin_angle'))
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{topic.get('confidence', 0):.1%}</h4>
                    <p>Confidence</p>
                </div>
                """, unsafe_allow_html=True)
            
            if is_selected:
                selected_topics.append({
                    'id': topic_id,
                    'topic': topic.get('topic', 'Unknown'),
                    'explanation': topic.get('explanation', ''),
                    'linkedin_angle': topic.get('linkedin_angle', ''),
                    'confidence': topic.get('confidence', 0),
                    'full_data': topic
                })
    
    return selected_topics

def run_trendjacking_pipeline(trending_urls, user_context, selected_topics, transcript):
    """Run the complete trendjacking pipeline"""
    
    if not TRENDJACKING_AVAILABLE:
        st.error("Trendjacking pipeline not available")
        return None
    
    # Configure DSPy with GPT-4.1 for the entire pipeline
    try:
        from dotenv import load_dotenv
        from dspy_config import safe_configure_dspy
        
        if safe_configure_dspy():
            # st.info("🤖 DSPy configured successfully")
            pass
        else:
            st.warning("⚠️ DSPy configuration failed - using fallback mode")
    except Exception as e:
        st.warning(f"⚠️ DSPy configuration failed: {e} - using fallback mode")
    
    results = {}
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Initialize conversation history tracker for iterative refinement
    conversation_history = ConversationHistoryBuilder()
    
    # STEP 1: RUN TREND ANALYSIS ONCE FOR ALL TOPICS
    st.markdown("### 🌟 Step 1: Analyzing Trending Content")
    status_text.text("🌟 Analyzing trending content...")
    
    try:
        trend_context_msg = f" (Context: {user_context.get('trend_context', 'No context')})" if user_context.get('trend_context') else ""
        st.markdown(f"**Trend Context**: {trend_context_msg}")
        
        pop_culture_results = enhanced_section_1(trending_urls, user_context)
        
        if pop_culture_results.get('error_occurred'):
            st.error(f"Trend analysis failed: {pop_culture_results.get('error_message', 'Unknown error')}")
            return None
        
        # Extract the PRIMARY trending topic based on user context and content analysis
        primary_trending_topic = extract_primary_trending_topic(pop_culture_results, user_context)
        st.success(f"✅ Primary trending topic identified: **{primary_trending_topic}**")
        
        # Add trend analysis to conversation history
        conversation_history.add_trend_analysis(
            trending_urls=trending_urls,
            extracted_content=pop_culture_results.get('content_extraction', {}),
            primary_topic=primary_trending_topic
        )
        
    except Exception as e:
        st.error(f"Error in trend analysis: {str(e)}")
        return None
    
    # STEP 2: EXTRACT VOICE PROFILE ONCE
    st.markdown("### 🗣️ Step 2: Analyzing Company Voice")
    status_text.text("🗣️ Extracting company voice profile...")
    
    try:
        voice_pipeline = VoiceAdaptationPipeline()
        company_context = f"{user_context['company_type']} - {user_context['goal']}"
        voice_profile = voice_pipeline.extract_company_voice(transcript, company_context)
        st.success("✅ Company voice profile extracted")
    except Exception as e:
        st.error(f"Error extracting voice profile: {str(e)}")
        return None
    
    # STEP 3: GENERATE POSTS FOR EACH TOPIC USING THE SAME TREND
    st.markdown("### 🎭 Step 3: Generating Content for Each Topic")
    
    total_steps = len(selected_topics) * 2  # 2 steps per topic now (generate + adapt)
    current_step = 0
    
    for topic_idx, topic_data in enumerate(selected_topics):
        topic_name = topic_data['topic']
        
        with st.container():
            st.markdown(f"### 🎭 Processing: {topic_name}")
            
            try:
                # Generate posts for this topic using the PRIMARY trending topic
                current_step += 1
                progress_bar.progress(current_step / total_steps)
                status_text.text(f"🎨 Generating contextual post approaches for {topic_name}...")
                
                # Generate dynamic post approaches using the PRIMARY trending topic
                st.write(f"🎨 Creating posts that connect **{topic_name}** with **{primary_trending_topic}**...")
                post_approaches = generate_dynamic_post_approaches(
                    trending_topic=primary_trending_topic,  # Use PRIMARY trend, not generic
                    business_topic=topic_name,
                    topic_explanation=topic_data['explanation'],
                    linkedin_angle=topic_data['linkedin_angle'],
                    promotional_goal=user_context['goal'],
                    brand_personality=user_context['brand_personality'],
                    company_type=user_context['company_type']
                )
                
                # Create enhanced posts using generated approaches (including viral hooks)
                enhanced_posts = []
                viral_hooks = []
                viral_hooks_dict = {}
                for i, approach in enumerate(post_approaches, 1):
                    enhanced_posts.append({
                        'post_number': i,
                        'approach': approach['name'],
                        'content': approach['content'],
                        'hashtags': approach['hashtags'],
                        'viral_hook': approach.get('viral_hook', '')  # Include viral hook
                    })
                    viral_hooks.append(approach.get('viral_hook', ''))
                    viral_hooks_dict[f'hook_{i}'] = approach.get('viral_hook', '')
                
                # Track viral hook generation in conversation history
                conversation_history.add_viral_hook_generation(
                    trending_topic=primary_trending_topic,
                    business_topic=topic_name,
                    generated_hooks=viral_hooks_dict
                )
                
                # Adapt posts to company voice using the PRIMARY trending topic
                current_step += 1  
                progress_bar.progress(current_step / total_steps)
                status_text.text(f"🗣️ Adapting posts to company voice for {topic_name}...")
                
                adapted_posts = voice_pipeline.adapt_posts_to_voice(
                    linkedin_posts=enhanced_posts,
                    voice_profile=voice_profile,
                    transcript=transcript,
                    core_business_message=topic_data['explanation'],
                    pop_culture_topic=primary_trending_topic,  # Use PRIMARY trend
                    viral_hooks=viral_hooks  # Pass viral hooks to preserve them
                )
                
                # Track voice adaptation in conversation history
                for i, (enhanced_post, adapted_post) in enumerate(zip(enhanced_posts, adapted_posts)):
                    conversation_history.add_voice_adaptation(
                        original_post=enhanced_post['content'],
                        voice_profile=voice_profile,
                        adapted_post=adapted_post['voice_adapted_content'],
                        changes_made=adapted_post.get('voice_changes_made', [])
                    )
                
                st.success(f"✅ Generated {len(post_approaches)} post approaches for {topic_name}")
                status_text.text(f"🎯 Creating viral posts for {topic_name}...")
                
                structure_generator = ConciseStructureGenerator()
                
                # Get brand examples
                brand_examples = []
                brand_responses = pop_culture_results.get('brand_responses', {})
                if brand_responses and brand_responses.get('platforms', {}).get('twitter'):
                    for post in brand_responses['platforms']['twitter'][:5]:
                        brand_examples.append({
                            'brand': post.get('username', 'Unknown'),
                            'content': post.get('content', ''),
                            'tactic': post.get('tactic_used', 'unknown'),
                            'engagement': post.get('engagement_total', 0)
                        })
                
                if not brand_examples:
                    # Fallback examples
                    brand_examples = [
                        {'brand': 'Nike', 'content': 'Just do it.', 'tactic': 'motivational', 'engagement': 1000},
                        {'brand': 'Wendys', 'content': 'Spicy take incoming.', 'tactic': 'sassy', 'engagement': 500}
                    ]
                
                company_voice_keywords = [
                    topic_name.split()[0] if topic_name.split() else 'innovation',
                    user_context['company_type'].split()[0] if user_context['company_type'].split() else 'business',
                    'expertise', 'leadership'
                ]
                
                structure_results = structure_generator.run_concise_generation(
                    business_topic=topic_name,
                    pop_culture_topic=primary_trending_topic,  # Use PRIMARY trend
                    company_voice_keywords=company_voice_keywords,
                    brand_examples=brand_examples
                )
                
                st.success(f"✅ Viral posts created for {topic_name}")
                
                # Store results (reuse shared pop_culture_results but update trending topic)
                shared_pop_culture_results = pop_culture_results.copy()
                shared_pop_culture_results['trending_topic'] = primary_trending_topic
                
                # Create post contexts for iterative refinement
                post_contexts = []
                refiner = IterativePostRefiner()
                for i, adapted_post in enumerate(adapted_posts):
                    post_context = refiner.initialize_post_context(
                        trending_topic=primary_trending_topic,
                        business_topic=topic_name,
                        viral_hook=adapted_post.get('original_viral_hook', ''),
                        original_approach=adapted_post.get('original_approach', ''),
                        voice_profile=voice_profile,
                        final_post=adapted_post['voice_adapted_content']
                    )
                    post_context['conversation_history'] = conversation_history
                    post_contexts.append(post_context)
                
                results[topic_name] = {
                    'topic_data': topic_data,
                    'pop_culture_results': shared_pop_culture_results,  # Shared results
                    'voice_profile': voice_profile,  # Shared voice profile
                    'voice_adapted_posts': adapted_posts,
                    'viral_posts': structure_results['concise_variations'],
                    'brand_examples': brand_examples,
                    'primary_trending_topic': primary_trending_topic,  # Track the primary topic used
                    'post_contexts': post_contexts,  # For iterative refinement
                    'conversation_history': conversation_history  # Full pipeline context
                }
                
            except Exception as e:
                st.error(f"Error processing {topic_name}: {str(e)}")
                continue
    
    progress_bar.progress(1.0)
    status_text.text("🎉 Pipeline complete!")
    
    return results

def display_results_interface(results):
    """Display results with tabs for different post types"""
    
    if not results:
        st.warning("No results to display")
        return
    
    st.header("🎉 Trendjacking Results")
    
    # Create tabs for post types
    voice_tab, viral_tab, refine_tab = st.tabs(["🗣️ Voice-Adapted Posts", "🔥 Viral Posts", "✨ Iterative Refinement"])
    
    with voice_tab:
        topic_names = list(results.keys())
        st.subheader("🗣️ Voice-Adapted Posts")
        st.markdown("*Detailed posts that match your authentic company voice*")
        
        # Topic selector
        selected_topic = st.selectbox(
            "Select Topic:",
            topic_names,
            key="voice_topic_select"
        ) if len(topic_names) > 1 else topic_names[0]
        
        if selected_topic in results:
            topic_results = results[selected_topic]
            voice_posts = topic_results['voice_adapted_posts']
            voice_profile = topic_results['voice_profile']
            
            # Show voice profile
            with st.expander("🎙️ Your Company Voice Profile", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Communication Style:** {voice_profile.get('communication_style', 'Unknown')}")
                    st.write(f"**Personality Traits:** {', '.join(voice_profile.get('personality_traits', []))}")
                
                with col2:
                    if voice_profile.get('vocabulary_preferences'):
                        st.write(f"**Key Vocabulary:** {', '.join(voice_profile['vocabulary_preferences'][:6])}")
            
            # Display voice-adapted posts
            for post in voice_posts:
                authenticity_score = post.get('authenticity_score', 0)
                authenticity_color = "#4ecdc4" if authenticity_score > 0.7 else "#ffd93d" if authenticity_score > 0.5 else "#ff6b6b"
                
                st.markdown(f"""
                <div class="post-card voice-post">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <h4>📱 Post #{post.get('post_number', 'N/A')} - {post.get('original_approach', 'Unknown')} </h4>
                        <div style="color: {authenticity_color}; font-weight: bold; font-size: 1.1em;">
                            🎯 {authenticity_score:.1%} Authentic
                        </div>
                    </div>
                    <div class="post-content" style="border-left: 4px solid {authenticity_color};">
                        {post.get('voice_adapted_content', 'No content available').replace(chr(10), '<br>')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show voice changes
                # if post.get('voice_changes_made'):
                #     with st.expander(f"🔄 Voice Adaptations Made", expanded=False):
                #         for change in post['voice_changes_made']:
                #             st.write(f"• {change}")

    with viral_tab:
        st.subheader("🔥 Ultra-Concise Viral Posts")
        st.markdown("*Short, punchy posts designed for maximum viral potential*")
        
        # Topic selector
        topic_names = list(results.keys())
        selected_topic = st.selectbox(
            "Select Topic:",
            topic_names,
            key="viral_topic_select"
        ) if len(topic_names) > 1 else topic_names[0]
        
        if selected_topic in results:
            topic_results = results[selected_topic]
            viral_posts = topic_results['viral_posts']
            
            # Show trending topic context
            trending_topic = topic_results['pop_culture_results']['trending_topic']
            st.info(f"🎭 **Trending Topic**: {trending_topic}")
            
            # Display viral posts
            if 'variations' in viral_posts:
                for name, post_data in viral_posts['variations'].items():
                    word_status = "🎯" if post_data['word_count'] <= 7 else "✅" if post_data['word_count'] <= 10 else "⚠️"
                    
                    st.markdown(f"""
                    <div class="post-card viral-post">
                        <div style="font-size: 1.1em; font-weight: bold; margin: 15px 0;">
                            "{post_data['content']}"
                        </div>
                        <p><strong>| Style:</strong> {name.replace('_', ' ').title()}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Show hashtags
                hashtags = viral_posts.get('hashtags', [])
                if hashtags:
                    st.markdown(f"**💡 Suggested Hashtags:** {' '.join(f'#{tag}' for tag in hashtags)}")
                
                # Show reasoning
                if viral_posts.get('best_version_reasoning'):
                    with st.expander("🧠 Generation Strategy"):
                        st.write(viral_posts['best_version_reasoning'])

    with refine_tab:
        display_iterative_refinement_interface(results)
    
    # with analytics_tab:
    #     st.subheader("📊 Pipeline Analytics")
        
    #     # Overall metrics
    #     col1, col2, col3, col4 = st.columns(4)
        
    #     with col1:
    #         st.metric("Topics Processed", len(results))
        
    #     with col2:
    #         total_viral_posts = sum(len(r['viral_posts'].get('variations', {})) for r in results.values())
    #         st.metric("Viral Posts Generated", total_viral_posts)
        
    #     with col3:
    #         total_voice_posts = sum(len(r['voice_adapted_posts']) for r in results.values())
    #         st.metric("Voice Posts Generated", total_voice_posts)
        
    #     with col4:
    #         avg_authenticity = sum(
    #             sum(post.get('authenticity_score', 0) for post in r['voice_adapted_posts'])
    #             / len(r['voice_adapted_posts'])
    #             for r in results.values()
    #         ) / len(results) if results else 0
    #         st.metric("Avg. Authenticity", f"{avg_authenticity:.1%}")
        
    #     # Per-topic breakdown
    #     st.subheader("📋 Topic Breakdown")
    #     for topic_name, topic_results in results.items():
    #         with st.expander(f"📝 {topic_name}", expanded=False):
                
    #             col1, col2 = st.columns(2)
                
    #             with col1:
    #                 st.write("**Original Topic Data:**")
    #                 topic_data = topic_results['topic_data']
    #                 st.write(f"Confidence: {topic_data['confidence']:.1%}")
    #                 st.write(f"LinkedIn Angle: {topic_data['linkedin_angle']}")
                
    #             with col2:
    #                 st.write("**Generated Content:**")
    #                 viral_count = len(topic_results['viral_posts'].get('variations', {}))
    #                 voice_count = len(topic_results['voice_adapted_posts'])
    #                 st.write(f"Viral Posts: {viral_count}")
    #                 st.write(f"Voice Posts: {voice_count}")
                
    #             # Show trending topic used
    #             trending_topic = topic_results['pop_culture_results']['trending_topic']
    #             st.write(f"**🎭 Trending Topic Used:** {trending_topic}")

def display_iterative_refinement_interface(results):
    """Display the iterative post refinement interface with two-column layout."""
    
    st.subheader("✨ Iterative Post Refinement")
    st.markdown("*Refine your posts with conversation history context*")
    
    # Initialize session state for refined posts
    if 'refined_posts' not in st.session_state:
        st.session_state.refined_posts = {}
    
    # Topic and post selectors
    topic_names = list(results.keys())
    if not topic_names:
        st.warning("No topics available for refinement")
        return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        selected_topic = st.selectbox(
            "Select Topic:",
            topic_names,
            key="refine_topic_select"
        )
    
    with col2:
        if selected_topic in results:
            topic_results = results[selected_topic]
            post_contexts = topic_results.get('post_contexts', [])
            
            if post_contexts:
                selected_post_idx = st.selectbox(
                    "Select Post:",
                    range(len(post_contexts)),
                    format_func=lambda x: f"Post #{x+1} - {topic_results['voice_adapted_posts'][x].get('original_approach', 'Unknown')}",
                    key="refine_post_select"
                )
            else:
                st.warning("No posts available for refinement")
                return
    
    if selected_topic not in results or not post_contexts:
        return
        
    # Get current post context
    post_context = post_contexts[selected_post_idx]
    post_key = f"{selected_topic}_post_{selected_post_idx}"
    
    # Show trending topic context
    trending_topic = topic_results['primary_trending_topic']
    st.info(f"🎭 **Trending Topic**: {trending_topic}")
    
    # TWO-COLUMN LAYOUT: Post Display + Refinement Input
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown("### 📝 Current Post")
        
        # Show current post (refined or original)
        current_post = st.session_state.refined_posts.get(post_key, post_context.get('original_post', post_context['current_post']))
        
        # Display post with styling
        authenticity_score = topic_results['voice_adapted_posts'][selected_post_idx].get('authenticity_score', 0)
        authenticity_color = "#4ecdc4" if authenticity_score > 0.7 else "#ffd93d" if authenticity_score > 0.5 else "#ff6b6b"
        
        st.markdown(f"""
        <div style="border: 2px solid {authenticity_color}; border-radius: 10px; padding: 20px; background: #f8f9fa;">
            <div style="font-size: 1.1em; line-height: 1.6; color: #333;">
                {current_post.replace(chr(10), '<br>')}
            </div>
            <div style="margin-top: 15px; font-size: 0.9em; color: #666;">
                🎯 Authenticity: {authenticity_score:.1%} | 
                📊 Characters: {len(current_post)} | 
                🎭 Hook: {post_context['viral_hook'][:30]}...
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show refinement history if any
        if post_context.get('refinement_history'):
            with st.expander(f"📚 Refinement History ({len(post_context['refinement_history'])} changes)"):
                for i, refinement in enumerate(post_context['refinement_history'], 1):
                    st.write(f"**{i}.** {refinement['request']}")
                    st.write(f"*Changes made:* {', '.join(refinement['changes_made'][:3])}")
                    st.divider()
    
    with col_right:
        st.markdown("### 🛠️ Refinement Controls")
        
        # Initialize input clear flag
        input_key = f"refinement_input_{post_key}"
        clear_input_key = f"clear_input_{post_key}"
        
        # Check if we should clear the input
        if st.session_state.get(clear_input_key, False):
            if input_key in st.session_state:
                st.session_state[input_key] = ""
            st.session_state[clear_input_key] = False
        
        # Refinement input
        refinement_request = st.text_area(
            "What changes would you like to make?",
            placeholder="E.g., 'Make this more personal and add a specific example from my experience'",
            height=120,
            key=input_key
        )
        
        # Refinement button
        if st.button("🔄 Refine Post", key=f"refine_btn_{post_key}", type="primary"):
            if refinement_request.strip():
                # Show progress
                with st.spinner("🧠 Applying refinement with conversation history context..."):
                    try:
                        # Get the refiner
                        refiner = IterativePostRefiner()
                        refiner.conversation_history = post_context['conversation_history']
                        
                        # Perform refinement
                        refinement_result = refiner.refine_post(
                            post_context=post_context,
                            user_refinement_request=refinement_request
                        )
                        
                        # Update session state with refined post
                        st.session_state.refined_posts[post_key] = refinement_result['refined_post']
                        
                        # Update post context in results
                        results[selected_topic]['post_contexts'][selected_post_idx] = refinement_result['updated_context']
                        
                        # Clear the input field for next refinement
                        st.session_state[clear_input_key] = True
                        
                        st.success("✅ Post refined successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Refinement failed: {str(e)}")
            else:
                st.warning("Please enter a refinement request")
        
        # Reset button
        if st.button("🔄 Reset to Original", key=f"reset_btn_{post_key}"):
            # Reset the post to original
            if post_key in st.session_state.refined_posts:
                del st.session_state.refined_posts[post_key]
            
            # Clear the input field
            st.session_state[clear_input_key] = True
            
            # Reset the post context refinement history and current_post
            if selected_topic in results and 'post_contexts' in results[selected_topic]:
                original_context = results[selected_topic]['post_contexts'][selected_post_idx]
                if 'refinement_history' in original_context:
                    original_context['refinement_history'] = []
                # Reset current_post to original_post
                if 'original_post' in original_context:
                    original_context['current_post'] = original_context['original_post']
                # Remove refinement steps from conversation history
                if 'conversation_history' in original_context:
                    original_context['conversation_history'].remove_refinement_steps()
            
            st.success("✅ Reset to original post")
            st.rerun()
        
        # Show conversation history context
        with st.expander("🧠 Pipeline Context", expanded=False):
            st.write("**Original Generation Context:**")
            st.write(f"• Viral Hook: {post_context['viral_hook'][:100]}...")
            st.write(f"• Approach: {post_context['original_approach']}")
            st.write(f"• Business Topic: {post_context['business_topic']}")
            
            # Show conversation history summary
            history_text = post_context['conversation_history'].get_conversation_history_text()
            st.write(f"**Conversation History:** {len(history_text)} characters of context available")
            
            if st.button("📋 View Full Context", key=f"context_btn_{post_key}"):
                st.text_area("Full Pipeline Context", history_text, height=200, key=f"context_view_{post_key}")

def main():
    """Main Streamlit app"""
    
    # Header
    st.title("🎭 Trendjacking Pipeline")
    st.markdown("""
    Transform your business insights into **viral LinkedIn content** by connecting them with trending topics!
    
    **How it works:**
    1. 📄 Upload your transcript (PDF/DOCX)
    2. 🔗 Add trending URLs you want to leverage  
    3. 🏢 Set your company context
    4. 🤖 Let AI extract topics and create viral content
    5. 🎉 Get both viral-style posts AND voice-adapted posts
    """)
    
    # Sidebar for company context
    with st.sidebar:
        st.header("🏢 Company Context")
        
        company_type = st.text_input(
            "Company Type:",
            value="AI Engineering Consultancy",
            placeholder="e.g., Tech Startup, Consulting Firm"
        )
        
        goal = st.text_area(
            "Promotional Goal:",
            value="""Showcase AI Engineering Excellence: Position ourselves as the go-to experts for enterprise AI implementation with deep technical
    capabilities in prompt optimization, agent training, and observability - demonstrating how we turn 'ChatGPT doesn't work for us' into
    production-ready AI systems with measurable results.""",
            placeholder="What do you want to achieve?",
            height=200
        )
        
        brand_personality = st.text_input(
            "Brand Personality:",
            value="Expert, innovative, authentic",
            placeholder="e.g., Professional, Witty, Approachable"
        )
        
        user_context = {
            'company_type': company_type,
            'goal': goal,
            'brand_personality': brand_personality
        }
        
        st.markdown("---")
        st.markdown("**💡 Tips:**")
        st.markdown("• Set your promotional goal to help the AI understand what you want to achieve in your company's marketing")
        st.markdown("• Set your brand personality to help the AI understand your company's voice and tone.")
        st.markdown("• Use the 'Describe the trending topic' input to help the AI understand what this trend is about when analyzing multiple URLs")
        st.markdown("• Use specific trending URLs for best results")
    
    # Initialize session state
    if 'pipeline_results' not in st.session_state:
        st.session_state.pipeline_results = None
    if 'extracted_topics' not in st.session_state:
        st.session_state.extracted_topics = []
    
    # Main workflow
    st.header("🚀 Trendjacking Workflow")
    
    # Step 1: File Upload
    with st.expander("📄 Step 1: Upload Your Transcript", expanded=True):
        uploaded_file = st.file_uploader(
            "Choose a transcript file",
            type=['pdf', 'docx'],
            help="Upload a PDF or DOCX file with your business transcript"
        )
        
        transcript_text = ""
        if uploaded_file is not None:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            with st.spinner(f"📖 Reading {file_extension.upper()} file..."):
                if file_extension == 'pdf':
                    transcript_text = extract_text_from_pdf(uploaded_file)
                elif file_extension == 'docx':
                    transcript_text = extract_text_from_docx(uploaded_file)
                
                if transcript_text:
                    transcript_text = clean_transcript(transcript_text)
                    # st.success(f"✅ Successfully extracted {len(transcript_text)} characters")
                    
                    # Preview
                    with st.expander("📝 Preview Transcript"):
                        st.text_area("Preview:", transcript_text[:800] + "..." if len(transcript_text) > 800 else transcript_text, height=150, disabled=True)
    
    # Step 2: Trending URLs and Context
    if transcript_text:
        with st.expander("🔗 Step 2: Add Trending Content", expanded=True):
            
            # Trend context input
            st.markdown("### 🎯 Trending Topic Context")
            st.markdown("*Help the AI understand what this trend is about when analyzing multiple URLs*")
            
            trend_context = st.text_input(
                "Describe the trending topic:",
                value=st.session_state.get('trend_context', ''),
                placeholder="e.g., 'Taylor Swift and Travis Kelce engagement announcement', 'New iPhone price controversy', 'CEO resignation scandal'",
                help="Provide context about what the trend is so the AI can better interpret multiple URLs about the same topic",
                key='trend_context'
            )
            
            st.markdown("### 📎 Trending URLs")
            st.markdown("*Add URLs related to the trending topic above*")
            
            # Preset examples
            # col1, col2 = st.columns([1, 1])
            # with col1:
            #     if st.button("📋 Use Example URLs"):
            #         example_urls = "https://knowyourmeme.com/memes/cash-me-ousside-howbow-dah\nhttps://knowyourmeme.com/memes/distracted-boyfriend\nhttps://imgur.com/gallery/trending"
            #         example_context = "Viral internet memes gaining mainstream attention"
            #         st.session_state.url_input = example_urls
            #         st.session_state.trend_context = example_context
            #         st.rerun()
            
            # with col2:
            #     if st.button("🎭 Use Taylor Swift Example"):
            #         example_urls = "https://www.bbc.com/news/entertainment-celebrity\nhttps://www.instagram.com/taylorswift\nhttps://twitter.com/taylorswift13"
            #         example_context = "Taylor Swift and Travis Kelce engagement speculation"
            #         st.session_state.url_input = example_urls
            #         st.session_state.trend_context = example_context
            #         st.rerun()
            
            url_input = st.text_area(
                "URLs (one per line):",
                value=st.session_state.get('url_input', ''),
                placeholder="https://www.bbc.com/news/entertainment-celebrity\nhttps://www.instagram.com/taylorswift\nhttps://twitter.com/trending-topic",
                height=120,
                key='url_input'
            )
            
            trending_urls = [url.strip() for url in url_input.split('\n') if url.strip()]
            
            # if trending_urls and trend_context:
                # st.success(f"✅ {len(trending_urls)} URLs ready for analysis")
                # st.info(f"🎯 **Trend Context**: {trend_context}")
                
                # st.markdown("**📋 URLs to Analyze:**")
                # for i, url in enumerate(trending_urls, 1):
                #     st.markdown(f'<div class="trend-url">{i}. {url}</div>', unsafe_allow_html=True)
            # elif trending_urls and not trend_context:
            #     st.warning("⚠️ Please add trend context to help the AI understand these URLs")
            # elif trend_context and not trending_urls:
            #     st.warning("⚠️ Please add URLs related to your trending topic")
        
        # Step 3: Topic Extraction
        if trending_urls and trend_context and all(user_context.values()):
            with st.expander("📊 Step 3: Extract Topics", expanded=True):
                
                if st.button("🤖 Extract Topics from Transcript", type="primary"):
                    with st.spinner("Analyzing transcript..."):
                        topics = extract_topics_from_transcript(transcript_text, goal)
                        st.session_state.extracted_topics = topics
                        if topics:
                            st.success(f"✅ Found {len(topics)} aligned topics!")
                
                if st.session_state.extracted_topics:
                    selected_topics = display_topic_selection(st.session_state.extracted_topics)
                    
                    # Step 4: Run Pipeline
                    if selected_topics:
                        st.markdown("---")
                        
                        if st.button("🎭 Generate Trendjacking Content", type="primary", key="run_pipeline"):
                            st.header("🎬 Running Trendjacking Pipeline")
                            
                            # Pass trend context to the pipeline
                            enhanced_user_context = user_context.copy()
                            enhanced_user_context['trend_context'] = trend_context
                            
                            results = run_trendjacking_pipeline(
                                trending_urls, 
                                enhanced_user_context, 
                                selected_topics, 
                                transcript_text
                            )
                            
                            st.session_state.pipeline_results = results
                            
                            if results:
                                st.success("🎉 Pipeline completed successfully!")
                            else:
                                st.error("❌ Pipeline failed to complete")
    
    # Display Results
    if st.session_state.pipeline_results:
        st.markdown("---")
        display_results_interface(st.session_state.pipeline_results)

if __name__ == "__main__":
    main()