#!/usr/bin/env python3
"""
Compatibility module for handling fcntl issues on Windows and cloud platforms
"""

import os
import sys
import platform

# Check if we're on Windows or a platform without fcntl
IS_WINDOWS = platform.system() == 'Windows'
IS_CLOUD = os.environ.get('RENDER') or os.environ.get('HEROKU') or os.environ.get('VERCEL')

# Create a mock fcntl module if needed
if IS_WINDOWS or IS_CLOUD:
    try:
        import fcntl
    except ImportError:
        # Create a mock fcntl module
        import types
        
        class MockFcntl:
            """Mock fcntl module for platforms that don't support it"""
            
            LOCK_EX = 0x02
            LOCK_UN = 0x08
            
            def flock(self, fd, operation):
                """Mock flock function"""
                pass
            
            def fcntl(self, fd, operation, arg=0):
                """Mock fcntl function"""
                pass
        
        # Create the mock module
        fcntl = MockFcntl()
        
        # Add it to sys.modules so other modules can import it
        sys.modules['fcntl'] = fcntl
        
        print("⚠️  Using mock fcntl module for compatibility")

# Export the fcntl module (real or mock)
try:
    import fcntl
    FCNTL_AVAILABLE = True
except ImportError:
    FCNTL_AVAILABLE = False
    fcntl = None

def is_fcntl_available():
    """Check if fcntl is available"""
    return FCNTL_AVAILABLE

def get_fcntl_module():
    """Get the fcntl module (real or mock)"""
    return fcntl 