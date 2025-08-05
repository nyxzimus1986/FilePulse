"""
Create test files to trigger FilePulse events and test memory limit
"""

import os
import time
import random
import string

def create_test_files(num_files=50, base_dir="test_files"):
    """Create test files to trigger filesystem events"""
    
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    print(f"Creating {num_files} test files in '{base_dir}' directory...")
    
    for i in range(num_files):
        # Generate random filename and content
        filename = f"test_file_{i:03d}_{''.join(random.choices(string.ascii_lowercase, k=5))}.txt"
        filepath = os.path.join(base_dir, filename)
        
        # Create file with some content
        content = f"Test file {i}\n" + "Sample content line\n" * random.randint(5, 20)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        # Small delay to spread out the events
        if i % 10 == 0:
            print(f"Created {i+1}/{num_files} files...")
            time.sleep(0.1)
    
    print(f"✅ Created {num_files} test files")
    print(f"📁 Location: {os.path.abspath(base_dir)}")
    print()
    print("Now modify some files to trigger more events:")
    
    # Modify some files
    for i in range(0, min(10, num_files), 2):
        filename = f"test_file_{i:03d}_{''.join(random.choices(string.ascii_lowercase, k=5))}.txt"
        filepath = os.path.join(base_dir, filename)
        
        if os.path.exists(filepath):
            with open(filepath, 'a') as f:
                f.write(f"\nModified at {time.strftime('%H:%M:%S')}\n")
    
    print("✅ Modified some test files")
    print()
    print("To clean up later, delete the 'test_files' directory")

if __name__ == '__main__':
    print("=" * 50)
    print("FILEPULSE TEST FILE GENERATOR")
    print("=" * 50)
    print()
    print("This will create test files to trigger filesystem events")
    print("and help test the memory limit functionality.")
    print()
    
    try:
        num_files = int(input("How many test files to create? (default 50): ") or "50")
    except ValueError:
        num_files = 50
    
    create_test_files(num_files)
    
    print()
    print("Now run the FilePulse GUI and monitor this directory!")
    print("Set a low memory limit to see the memory management in action.")
