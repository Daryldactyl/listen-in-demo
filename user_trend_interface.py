#!/usr/bin/env python3
"""
User Trend Interface - Simple interface for users to input trend URLs and get analysis
"""

import json
from datetime import datetime
from typing import List, Dict, Any
from trend_content_analyzer import TrendContentAnalyzer, ContentType
from enhanced_content_extractor import EnhancedContentExtractor
from enhanced_brand_detector_v2 import EnhancedBrandDetectorV2

class UserTrendInterface:
    """Simple interface for trend analysis workflow"""
    
    def __init__(self):
        self.content_analyzer = TrendContentAnalyzer()
        self.content_extractor = EnhancedContentExtractor()
        self.brand_detector = EnhancedBrandDetectorV2()
        
    def analyze_user_trends(self, urls: List[str], user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main workflow for analyzing user-provided trend URLs"""
        
        print("🚀 TREND ANALYSIS WORKFLOW STARTING")
        print("=" * 60)
        print(f"📍 Analyzing {len(urls)} trend URLs")
        
        if user_context:
            print(f"👤 User Context: {user_context.get('company_type', 'Not specified')}")
            print(f"🎯 Goal: {user_context.get('goal', 'General trend analysis')}")
        
        workflow_results = {
            'input_data': {
                'urls': urls,
                'user_context': user_context,
                'timestamp': datetime.now().isoformat()
            },
            'analysis_steps': {},
            'final_recommendations': {}
        }
        
        # Step 1: Analyze URL content types
        print(f"\n🔍 STEP 1: CONTENT TYPE ANALYSIS")
        print("-" * 40)
        
        analyzed_trends = self.content_analyzer.analyze_trend_urls(urls)
        extraction_plan = self.content_analyzer.generate_extraction_plan(analyzed_trends)
        
        workflow_results['analysis_steps']['content_analysis'] = {
            'analyzed_trends': [self._trend_to_dict(t) for t in analyzed_trends],
            'extraction_plan': extraction_plan
        }
        
        self._print_content_analysis_summary(analyzed_trends, extraction_plan)
        
        # Step 2: Extract content from URLs
        print(f"\n📥 STEP 2: CONTENT EXTRACTION")
        print("-" * 40)
        
        # Create trend context from user context - prioritize user-provided trend context
        trend_context = ""
        if user_context:
            # Use explicit trend context if provided, otherwise create from company context
            if user_context.get('trend_context'):
                trend_context = user_context['trend_context']
                print(f"📝 Using provided trend context: {trend_context}")
            else:
                trend_context = f"{user_context.get('company_type', 'Business')} analyzing trends for {user_context.get('goal', 'marketing purposes')}"
        
        enhanced_extraction_results = self.content_extractor.extract_content_from_urls(urls, trend_context)
        
        # Transform enhanced results to match expected format
        extraction_results = self._transform_enhanced_results(enhanced_extraction_results)
        
        workflow_results['analysis_steps']['content_extraction'] = extraction_results
        
        self._print_extraction_summary(extraction_results)
        
        # Step 3: Simulate brand responses for high-opportunity trends
        print(f"\n🏢 STEP 3: BRAND RESPONSE SIMULATION")
        print("-" * 40)
        
        brand_simulation_results = self._simulate_brand_responses_for_trends(extraction_results)
        
        workflow_results['analysis_steps']['brand_simulation'] = brand_simulation_results
        
        self._print_brand_simulation_summary(brand_simulation_results)
        
        # Step 4: Generate final recommendations
        print(f"\n💡 STEP 4: STRATEGIC RECOMMENDATIONS")
        print("-" * 40)
        
        final_recommendations = self._generate_final_recommendations(
            extraction_results, 
            brand_simulation_results, 
            user_context
        )
        
        workflow_results['final_recommendations'] = final_recommendations
        
        self._print_final_recommendations(final_recommendations)
        
        # Save results
        self._save_workflow_results(workflow_results)
        
        print(f"\n🎉 WORKFLOW COMPLETE!")
        print(f"✅ {len([e for e in extraction_results['extracted_contents'] if e.success])} trends successfully analyzed")
        print(f"🎯 {len(final_recommendations['high_priority_trends'])} high-priority opportunities identified")
        print(f"💾 Results saved to workflow_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        return workflow_results
    
    def _trend_to_dict(self, trend) -> Dict[str, Any]:
        """Convert TrendContent object to dictionary"""
        return {
            'url': trend.url,
            'content_type': trend.content_type.value,
            'extraction_strategy': trend.extraction_strategy,
            'context_needed': trend.context_needed,
            'visual_analysis_required': trend.visual_analysis_required,
            'metadata': trend.metadata
        }
    
    def _print_content_analysis_summary(self, analyzed_trends, extraction_plan):
        """Print content analysis summary"""
        print(f"Content Type Breakdown:")
        for content_type, count in extraction_plan['content_type_breakdown'].items():
            icon = self._get_content_type_icon(content_type)
            print(f"  {icon} {content_type.replace('_', ' ').title()}: {count}")
        
        print(f"\n🎯 Analysis Requirements:")
        print(f"  📱 Visual Analysis Needed: {extraction_plan['visual_analysis_needed']}")
        print(f"  📝 Text-Only Content: {extraction_plan['text_only_content']}")
        print(f"  🔍 High Context Needs: {extraction_plan['high_context_needs']}")
        
        if extraction_plan['processing_recommendations']:
            print(f"\n💡 Processing Recommendations:")
            for rec in extraction_plan['processing_recommendations']:
                print(f"  • {rec}")
    
    def _get_content_type_icon(self, content_type: str) -> str:
        """Get emoji icon for content type"""
        icons = {
            'text_article': '📰',
            'social_post': '📱', 
            'image_meme': '🎭',
            'video_content': '🎥',
            'mixed_content': '🎪',
            'unknown': '❓'
        }
        return icons.get(content_type, '📄')
    
    def _print_extraction_summary(self, extraction_results):
        """Print extraction summary"""
        summary = extraction_results['extraction_summary']
        print(f"Extraction Results:")
        print(f"  ✅ Successful: {summary['successful_extractions']}")
        print(f"  ❌ Failed: {summary['failed_extractions']}")
        
        synthesis = extraction_results['trend_synthesis']
        if 'error' not in synthesis:
            print(f"\n📊 Trend Synthesis:")
            print(f"  🏷️ Trending Themes: {len(synthesis.get('trending_themes', []))}")
            print(f"  🚀 Viral Elements: {len(synthesis.get('viral_elements', []))}")
            print(f"  💼 Avg Brand Opportunity: {synthesis.get('average_brand_opportunity', 0):.2f}")
            print(f"  🎯 High Opportunity Content: {synthesis.get('high_opportunity_count', 0)}")
        
        opportunities = extraction_results['brand_opportunities']
        if opportunities:
            print(f"\n🎯 Top Brand Opportunities:")
            for i, opp in enumerate(opportunities[:3], 1):
                print(f"  {i}. Score: {opp['brand_score']:.2f} | {opp['content_type']}")
                print(f"     URL: {opp['url'][:50]}...")
                print(f"     Key Phrases: {', '.join(opp['key_phrases'][:3])}")
    
    def _simulate_brand_responses_for_trends(self, extraction_results) -> Dict[str, Any]:
        """Simulate brand responses for extracted trends"""
        
        # Get high-opportunity trends
        high_opp_trends = [
            content for content in extraction_results['extracted_contents']
            if content.success and (content.brand_opportunity_score or 0) > 0.6
        ]
        
        simulation_results = {
            'trends_simulated': len(high_opp_trends),
            'brand_responses': {},
            'competitive_landscape': {},
            'response_strategies': {}
        }
        
        for trend_content in high_opp_trends[:3]:  # Limit to top 3 for demo
            
            # Create intelligent trending topic from extracted content and key phrases
            trending_topic = self._create_intelligent_trend_context(trend_content)
            
            print(f"  🎭 Simulating brand responses for: {trending_topic}")
            print(f"      📋 Full Context: {trending_topic[:100]}...")  # Show more context
            
            # Simulate brand responses
            brand_responses = self.brand_detector.simulate_brand_responses(trending_topic)
            
            # Store results
            simulation_results['brand_responses'][trend_content.url] = brand_responses
            
            # Analyze competitive landscape
            competitive_analysis = self._analyze_competitive_landscape(brand_responses, trend_content)
            simulation_results['competitive_landscape'][trend_content.url] = competitive_analysis
            
            # Generate response strategy
            response_strategy = self._generate_response_strategy(brand_responses, trend_content)
            simulation_results['response_strategies'][trend_content.url] = response_strategy
        
        return simulation_results
    
    def _analyze_competitive_landscape(self, brand_responses, trend_content) -> Dict[str, Any]:
        """Analyze the competitive landscape for a trend"""
        
        twitter_posts = len(brand_responses['platforms']['twitter'])
        linkedin_posts = len(brand_responses['platforms']['linkedin'])
        total_posts = brand_responses['summary']['verified_brand_posts']
        
        # Calculate competition level
        if total_posts > 8:
            competition_level = "Very High"
            recommendation = "Focus on unique angle or skip this trend"
        elif total_posts > 5:
            competition_level = "High" 
            recommendation = "Need creative differentiation"
        elif total_posts > 2:
            competition_level = "Medium"
            recommendation = "Good opportunity with proper positioning"
        else:
            competition_level = "Low"
            recommendation = "Excellent first-mover opportunity"
        
        # Identify dominant tactics
        tactics_used = []
        for post in brand_responses['platforms']['twitter']:
            tactics_used.append(post.get('tactic_used', 'unknown'))
        
        dominant_tactics = list(set(tactics_used))
        
        return {
            'competition_level': competition_level,
            'total_competing_brands': total_posts,
            'platform_distribution': {
                'twitter': twitter_posts,
                'linkedin': linkedin_posts
            },
            'dominant_tactics': dominant_tactics,
            'strategic_recommendation': recommendation,
            'opportunity_window': 'narrow' if competition_level in ['High', 'Very High'] else 'good'
        }
    
    def _generate_response_strategy(self, brand_responses, trend_content) -> Dict[str, Any]:
        """Generate response strategy based on brand analysis and content"""
        
        # Identify gaps in competitor responses
        competitor_tactics = set()
        for post in brand_responses['platforms']['twitter']:
            competitor_tactics.add(post.get('tactic_used', 'unknown'))
        
        # Suggest differentiated approaches
        all_possible_tactics = [
            'educational_content', 'behind_scenes', 'customer_stories', 
            'product_demo', 'industry_insight', 'contrarian_take'
        ]
        
        unused_tactics = [tactic for tactic in all_possible_tactics if tactic not in competitor_tactics]
        
        # Determine optimal timing
        total_competitor_posts = brand_responses['summary']['verified_brand_posts']
        if total_competitor_posts < 3:
            timing_strategy = "Act quickly - first mover advantage available"
        elif total_competitor_posts < 6:
            timing_strategy = "Move fast with differentiated angle"
        else:
            timing_strategy = "Consider waiting for next trend cycle"
        
        # Content format recommendation
        if trend_content.content_type == 'image_meme':
            format_recommendation = "Visual meme adaptation or parody"
        elif trend_content.content_type == 'video_content':
            format_recommendation = "Video response or reaction content"
        else:
            format_recommendation = "Text-based thought leadership post"
        
        return {
            'primary_tactic': unused_tactics[0] if unused_tactics else 'contrarian_take',
            'alternative_tactics': unused_tactics[1:3] if len(unused_tactics) > 1 else [],
            'timing_strategy': timing_strategy,
            'content_format': format_recommendation,
            'differentiation_opportunity': len(unused_tactics) > 0,
            'risk_level': 'low' if total_competitor_posts < 5 else 'medium'
        }
    
    def _generate_final_recommendations(self, extraction_results, brand_simulation_results, user_context) -> Dict[str, Any]:
        """Generate final strategic recommendations"""
        
        # Get successful extractions
        successful_extractions = [e for e in extraction_results['extracted_contents'] if e.success]
        
        # Rank trends by opportunity score
        high_priority_trends = sorted(
            [e for e in successful_extractions if (e.brand_opportunity_score or 0) > 0.6],
            key=lambda x: x.brand_opportunity_score or 0,
            reverse=True
        )
        
        medium_priority_trends = sorted(
            [e for e in successful_extractions if 0.4 <= (e.brand_opportunity_score or 0) <= 0.6],
            key=lambda x: x.brand_opportunity_score or 0,
            reverse=True
        )
        
        # Generate action plan
        action_plan = []
        
        for i, trend in enumerate(high_priority_trends[:2], 1):
            url_key = trend.url
            competitive_info = brand_simulation_results['competitive_landscape'].get(url_key, {})
            strategy_info = brand_simulation_results['response_strategies'].get(url_key, {})
            
            action_item = {
                'priority': f'High Priority #{i}',
                'url': trend.url,
                'opportunity_score': trend.brand_opportunity_score,
                'content_type': trend.content_type,
                'recommended_action': strategy_info.get('primary_tactic', 'Immediate response'),
                'timing': strategy_info.get('timing_strategy', 'Act quickly'),
                'competition_level': competitive_info.get('competition_level', 'Unknown'),
                'risk_level': strategy_info.get('risk_level', 'medium'),
                'content_format': strategy_info.get('content_format', 'Social media post')
            }
            action_plan.append(action_item)
        
        # Overall strategy assessment
        total_high_priority = len(high_priority_trends)
        avg_opportunity = sum(e.brand_opportunity_score or 0 for e in successful_extractions) / len(successful_extractions) if successful_extractions else 0
        
        strategy_assessment = {
            'trend_landscape': 'favorable' if total_high_priority > 1 else 'challenging',
            'overall_opportunity': avg_opportunity,
            'recommended_approach': 'aggressive' if avg_opportunity > 0.6 else 'selective',
            'timing_urgency': 'high' if total_high_priority > 2 else 'medium'
        }
        
        return {
            'high_priority_trends': high_priority_trends,
            'medium_priority_trends': medium_priority_trends,
            'action_plan': action_plan,
            'strategy_assessment': strategy_assessment,
            'next_steps': [
                'Review high-priority trends and select top 1-2 for immediate action',
                'Develop content concepts using recommended tactics',
                'Monitor competitor responses and adjust strategy',
                'Execute content creation and publishing plan'
            ]
        }
    
    def _print_brand_simulation_summary(self, brand_simulation_results):
        """Print brand simulation summary"""
        print(f"Brand Response Simulation:")
        print(f"  🎭 Trends Simulated: {brand_simulation_results['trends_simulated']}")
        
        if brand_simulation_results['trends_simulated'] > 0:
            print(f"\n📊 Competitive Landscape Overview:")
            for url, competitive_info in list(brand_simulation_results['competitive_landscape'].items())[:2]:
                domain = url.split('/')[2] if len(url.split('/')) > 2 else url[:30]
                print(f"  🌐 {domain}:")
                print(f"    Competition: {competitive_info.get('competition_level', 'Unknown')}")
                print(f"    Competing Brands: {competitive_info.get('total_competing_brands', 0)}")
                print(f"    Recommendation: {competitive_info.get('strategic_recommendation', 'Analyze further')}")
    
    def _print_final_recommendations(self, recommendations):
        """Print final recommendations"""
        high_priority = recommendations['high_priority_trends']
        strategy = recommendations['strategy_assessment']
        
        print(f"Strategic Assessment:")
        print(f"  🎯 High Priority Opportunities: {len(high_priority)}")
        print(f"  📊 Overall Opportunity Score: {strategy['overall_opportunity']:.2f}")
        print(f"  🏃 Recommended Approach: {strategy['recommended_approach'].title()}")
        print(f"  ⏰ Timing Urgency: {strategy['timing_urgency'].title()}")
        
        if recommendations['action_plan']:
            print(f"\n🚀 Immediate Action Plan:")
            for action in recommendations['action_plan']:
                print(f"  {action['priority']}:")
                print(f"    • Opportunity Score: {action['opportunity_score']:.2f}")
                print(f"    • Recommended Action: {action['recommended_action']}")
                print(f"    • Timing: {action['timing']}")
                print(f"    • Risk Level: {action['risk_level'].title()}")
        
        print(f"\n📝 Next Steps:")
        for i, step in enumerate(recommendations['next_steps'], 1):
            print(f"  {i}. {step}")
    
    def _save_workflow_results(self, workflow_results):
        """Save workflow results to JSON file"""
        filename = f"workflow_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Convert any non-serializable objects
        serializable_results = self._make_serializable(workflow_results)
        
        with open(filename, 'w') as f:
            json.dump(serializable_results, f, indent=2, default=str)
        
        return filename
    
    def _make_serializable(self, obj):
        """Make object JSON serializable"""
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif isinstance(obj, dict):
            return {key: self._make_serializable(value) for key, value in obj.items()}
        else:
            return obj
    
    def _transform_enhanced_results(self, enhanced_results: List) -> Dict[str, Any]:
        """Transform enhanced extraction results to match expected interface format"""
        
        successful_extractions = len([r for r in enhanced_results if r.success])
        failed_extractions = len([r for r in enhanced_results if not r.success])
        
        # Extract content and calculate metrics
        all_text_content = []
        all_viral_elements = []
        brand_scores = []
        
        for result in enhanced_results:
            if result.success and result.text_content:
                all_text_content.append(result.text_content)
                brand_scores.append(result.brand_opportunity_score or 0.5)
                if result.viral_elements:
                    all_viral_elements.extend(result.viral_elements)
        
        # Calculate averages
        avg_brand_opportunity = sum(brand_scores) / len(brand_scores) if brand_scores else 0.5
        high_opportunity_count = len([score for score in brand_scores if score > 0.7])
        
        # Create trending themes from key phrases
        trending_themes = []
        for result in enhanced_results:
            if result.success and result.key_phrases:
                trending_themes.extend(result.key_phrases[:3])  # Top 3 from each
        
        # Remove duplicates and limit
        trending_themes = list(set(trending_themes))[:10]
        viral_elements_unique = list(set(all_viral_elements))[:10]
        
        return {
            'extraction_summary': {
                'successful_extractions': successful_extractions,
                'failed_extractions': failed_extractions,
                'total_urls': len(enhanced_results)
            },
            'trend_synthesis': {
                'trending_themes': trending_themes,
                'viral_elements': viral_elements_unique,
                'average_brand_opportunity': avg_brand_opportunity,
                'high_opportunity_count': high_opportunity_count
            },
            'brand_opportunities': [
                {
                    'url': result.url,
                    'content_type': result.content_type,
                    'brand_score': result.brand_opportunity_score or 0.5,
                    'key_phrases': result.key_phrases or [],
                    'viral_elements': result.viral_elements or [],
                    'has_screenshot': bool(result.screenshot_path),
                    'text_length': len(result.text_content) if result.text_content else 0
                }
                for result in enhanced_results if result.success
            ],
            'extracted_contents': enhanced_results  # Keep original enhanced results
        }
    
    def _create_intelligent_trend_context(self, trend_content) -> str:
        """Create intelligent trending topic context from extracted content and analysis"""
        
        # Start with key phrases if available (these come from DSPy analysis)
        context_parts = []
        
        if trend_content.key_phrases:
            # Use key phrases as the primary context
            key_context = ", ".join(trend_content.key_phrases[:4])  # Top 4 key phrases
            context_parts.append(key_context)
        
        # Add viral elements if available
        if trend_content.viral_elements:
            viral_context = ", ".join([ve.replace('content_', '').replace('_', ' ') for ve in trend_content.viral_elements[:2]])
            context_parts.append(f"viral elements: {viral_context}")
        
        # If we have rich content, try to extract the main topic from the text
        if trend_content.text_content and len(trend_content.text_content) > 200:
            # Look for title/headline patterns in the content
            lines = trend_content.text_content.split('\n')[:10]  # First 10 lines
            for line in lines:
                line = line.strip()
                # Look for title indicators
                if any(indicator in line.lower() for indicator in ['oreo', 'super bowl', 'blackout', 'dunk in the dark', 'viral', 'trending']):
                    if len(line) > 10 and len(line) < 150:  # Reasonable title length
                        context_parts.insert(0, line)  # Put title first
                        break
        
        # Create the final context
        if context_parts:
            trending_topic = " - ".join(context_parts)
            # Limit length but keep important context
            if len(trending_topic) > 200:
                trending_topic = trending_topic[:200] + "..."
        else:
            # Fallback to URL-based context
            trending_topic = f"Trending content from {trend_content.content_type}"
        
        return trending_topic

def run_user_workflow_demo():
    """Demonstration of the user workflow"""
    interface = UserTrendInterface()
    
    # Example user input
    example_urls = [
        "https://twitter.com/taylorswift/status/engagement-announcement",
        "https://www.instagram.com/p/viral-trend-post/",
        "https://imgur.com/gallery/trending-meme",
        "https://www.nytimes.com/2024/01/15/trending-news-story.html"
    ]
    
    user_context = {
        'company_type': 'AI Engineering Consultancy',
        'goal': 'Build thought leadership and attract enterprise clients',
        'brand_personality': 'Technical expertise with approachable communication',
        'target_audience': 'CTOs, engineering leaders, enterprise decision makers'
    }
    
    print("🎯 USER TREND WORKFLOW DEMONSTRATION")
    print("=" * 60)
    print("This demo shows how users can input trending URLs and get")
    print("comprehensive analysis for trendjacking opportunities.")
    print()
    
    results = interface.analyze_user_trends(example_urls, user_context)
    
    return results

if __name__ == "__main__":
    run_user_workflow_demo()