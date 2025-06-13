import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_symlinks():
    """Create symlinks to ensure files are accessible from both locations"""
    try:
        # Ensure output directories exist
        os.makedirs('output', exist_ok=True)
        os.makedirs('app/output', exist_ok=True)
        
        # Create symlinks between the directories
        # This ensures files are accessible from both locations
        
        # List all files in output directory
        if os.path.exists('output'):
            output_files = os.listdir('output')
            for file in output_files:
                source = os.path.join('output', file)
                target = os.path.join('app/output', file)
                
                # Create symlink if it doesn't exist
                if os.path.isfile(source) and not os.path.exists(target):
                    try:
                        os.symlink(os.path.abspath(source), target)
                        logger.info(f"Created symlink: {target} -> {source}")
                    except Exception as e:
                        logger.error(f"Error creating symlink {target}: {str(e)}")
        
        # List all files in app/output directory
        if os.path.exists('app/output'):
            app_output_files = os.listdir('app/output')
            for file in app_output_files:
                source = os.path.join('app/output', file)
                target = os.path.join('output', file)
                
                # Create symlink if it doesn't exist
                if os.path.isfile(source) and not os.path.exists(target):
                    try:
                        os.symlink(os.path.abspath(source), target)
                        logger.info(f"Created symlink: {target} -> {source}")
                    except Exception as e:
                        logger.error(f"Error creating symlink {target}: {str(e)}")
        
        logger.info("✅ Symlinks created successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating symlinks: {str(e)}")
        return False

def copy_files():
    """Copy files between output directories to ensure they're accessible"""
    try:
        # Ensure output directories exist
        os.makedirs('output', exist_ok=True)
        os.makedirs('app/output', exist_ok=True)
        
        # Copy files from output to app/output
        if os.path.exists('output'):
            output_files = os.listdir('output')
            for file in output_files:
                source = os.path.join('output', file)
                target = os.path.join('app/output', file)
                
                # Copy file if it doesn't exist in destination
                if os.path.isfile(source) and not os.path.exists(target):
                    try:
                        import shutil
                        shutil.copy2(source, target)
                        logger.info(f"Copied file: {source} -> {target}")
                    except Exception as e:
                        logger.error(f"Error copying file {source}: {str(e)}")
        
        # Copy files from app/output to output
        if os.path.exists('app/output'):
            app_output_files = os.listdir('app/output')
            for file in app_output_files:
                source = os.path.join('app/output', file)
                target = os.path.join('output', file)
                
                # Copy file if it doesn't exist in destination
                if os.path.isfile(source) and not os.path.exists(target):
                    try:
                        import shutil
                        shutil.copy2(source, target)
                        logger.info(f"Copied file: {source} -> {target}")
                    except Exception as e:
                        logger.error(f"Error copying file {source}: {str(e)}")
        
        logger.info("✅ Files copied successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error copying files: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔧 Applying direct fix for file access...")
    
    # Try to create symlinks first (more elegant solution)
    try:
        if create_symlinks():
            print("✅ Created symlinks between output directories")
        else:
            # Fall back to copying files
            if copy_files():
                print("✅ Copied files between output directories")
            else:
                print("❌ Failed to sync output directories")
    except:
        # If symlinks fail, try copying
        if copy_files():
            print("✅ Copied files between output directories")
        else:
            print("❌ Failed to sync output directories")
    
    print("🔄 Please restart your Flask application")