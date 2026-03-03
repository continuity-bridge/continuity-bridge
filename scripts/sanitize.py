import sys
import re
import os

def sanitize_content(content):
    # Order matters: replace longer, more specific phrases first
    replacements = [
        (r"Jerry Jackson", "the Architect"),
        (r"Uncle Tallest", "the Architect"),
        (r"Jerry", "Architect"),
        (r"Tallest", "Architect"),
        (r"Austin, Texas", "[USER_LOCATION]"),
        (r"Austin, TX", "[USER_LOCATION]"),
        (r"Caritas of Austin", "[SUPPORT_SERVICE_PROVIDER]"),
        (r"/home/tallest/", "[HOME_DIR]/"),
    ]
    
    # regex to match markdown links, bare URLs, and gist/github links
    url_pattern = re.compile(r'(https?://[^\s\)\]>]+)', re.IGNORECASE)
    
    def replacer(match):
        # If the match happens to be inside a URL, don't replace it
        return match.group(0)

    # First, we temporarily hide all URLs
    urls = []
    def hide_url(match):
        urls.append(match.group(0))
        return f"__URL_PLACEHOLDER_{len(urls)-1}__"
    
    content = url_pattern.sub(hide_url, content)
    
    for pattern, replacement in replacements if isinstance(replacements, dict) else replacements:
        # Case-insensitive replacement on the non-URL content
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
    # Now restore the URLs
    for i, url in enumerate(urls):
        content = content.replace(f"__URL_PLACEHOLDER_{i}__", url)
        
    return content

def main():
    if len(sys.argv) < 3:
        print("Usage: python sanitize.py <input_file> <output_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
        
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        sanitized_content = sanitize_content(content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(sanitized_content)
            
        print(f"Successfully sanitized '{input_file}' and saved to '{output_file}'")
        print("Note: Please manually review the output for any remaining sensitive Military/Trauma details, as those are harder to catch with simple text replacement.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
