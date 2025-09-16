#!/usr/bin/env python3
"""
Centralized DSPy Configuration
Thread-safe configuration for Streamlit Cloud deployment
"""

import dspy
import os
import threading
from dotenv import load_dotenv

load_dotenv()

# Thread-safe configuration tracking
_config_lock = threading.Lock()
_is_configured = False
_lm = None

def get_configured_lm():
    """Get a pre-configured DSPy language model. Thread-safe."""
    global _is_configured, _lm
    
    with _config_lock:
        if not _is_configured:
            try:
                api_key = os.getenv('OPENROUTER_API_KEY')
                if not api_key:
                    raise ValueError("OPENROUTER_API_KEY not found in environment")
                
                # Use GPT-4o for best quality
                _lm = dspy.LM(
                    'openai/gpt-4o', 
                    api_key=api_key, 
                    api_base='https://openrouter.ai/api/v1'
                )
                
                # Only configure if not already configured
                try:
                    dspy.configure(lm=_lm)
                    _is_configured = True
                    print("✅ DSPy configured successfully with GPT-4o")
                except Exception as e:
                    if "can only be changed by the thread that initially configured it" in str(e):
                        # DSPy is already configured, just use the existing config
                        print("✅ DSPy already configured, using existing configuration")
                        _is_configured = True
                    else:
                        raise e
                        
            except Exception as e:
                print(f"⚠️ DSPy configuration failed: {e} - using fallback mode")
                # Return None to indicate fallback mode
                return None
        
        return _lm

def safe_configure_dspy():
    """Safely configure DSPy, handling threading issues."""
    return get_configured_lm() is not None

def create_chain_of_thought(signature_class):
    """Create a ChainOfThought module with safe configuration."""
    try:
        lm = get_configured_lm()
        if lm is None:
            print("⚠️ Using fallback mode - limited functionality")
            return None
        return dspy.ChainOfThought(signature_class)
    except Exception as e:
        print(f"⚠️ Failed to create ChainOfThought: {e}")
        return None

# For backward compatibility - modules can still import this
def configure_dspy():
    """Legacy function for backward compatibility."""
    return safe_configure_dspy()