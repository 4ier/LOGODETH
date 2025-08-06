# LOGODETH Usage Examples 📚

This directory contains practical examples for using LOGODETH in different scenarios.

## 🐍 Python Examples

### Basic Usage

```python
import requests
import json
from pathlib import Path

def recognize_logo(image_path: str, api_url: str = "http://localhost:8000") -> dict:
    """
    Recognize a logo using LOGODETH API
    
    Args:
        image_path: Path to the image file
        api_url: Base URL of the API server
        
    Returns:
        Recognition result as dictionary
    """
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(f"{api_url}/api/v1/recognize", files=files)
    
    response.raise_for_status()
    return response.json()

# Example usage
if __name__ == "__main__":
    try:
        result = recognize_logo("sample_logo.jpg")
        print(f"Band: {result['band_name']}")
        print(f"Genre: {result['genre']}")
        print(f"Confidence: {result['confidence']:.1f}%")
        
        if result.get('_cache_metadata'):
            print("✨ Result was cached!")
            
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
    except FileNotFoundError:
        print("Image file not found")
```

### Batch Processing

```python
import asyncio
import aiohttp
from pathlib import Path
from typing import List, Dict

class LogoRecognitionClient:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        
    async def recognize_logo_async(
        self, 
        session: aiohttp.ClientSession, 
        image_path: Path
    ) -> Dict:
        """Async logo recognition"""
        try:
            with open(image_path, 'rb') as f:
                data = aiohttp.FormData()
                data.add_field('file', f, filename=image_path.name)
                
                async with session.post(
                    f"{self.api_url}/api/v1/recognize", 
                    data=data
                ) as response:
                    response.raise_for_status()
                    result = await response.json()
                    result['source_file'] = str(image_path)
                    return result
                    
        except Exception as e:
            return {
                'source_file': str(image_path),
                'error': str(e),
                'band_name': 'Error',
                'confidence': 0
            }
    
    async def batch_recognize(self, image_paths: List[Path]) -> List[Dict]:
        """Process multiple logos concurrently"""
        async with aiohttp.ClientSession() as session:
            tasks = [
                self.recognize_logo_async(session, path) 
                for path in image_paths
            ]
            return await asyncio.gather(*tasks)

# Example usage
async def main():
    client = LogoRecognitionClient()
    
    # Find all image files in a directory
    image_dir = Path("./logos")
    image_files = list(image_dir.glob("*.{jpg,jpeg,png,gif,webp}"))
    
    print(f"Processing {len(image_files)} logos...")
    results = await client.batch_recognize(image_files)
    
    # Print results
    for result in results:
        if 'error' not in result:
            print(f"✅ {result['source_file']}: {result['band_name']} ({result['confidence']:.1f}%)")
        else:
            print(f"❌ {result['source_file']}: {result['error']}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🌐 JavaScript/Web Examples

### Browser Upload

```html
<!DOCTYPE html>
<html>
<head>
    <title>Logo Recognition Example</title>
</head>
<body>
    <div>
        <input type="file" id="logoFile" accept="image/*" />
        <button onclick="recognizeLogo()">Recognize Logo</button>
        <div id="results"></div>
    </div>

    <script>
        async function recognizeLogo() {
            const fileInput = document.getElementById('logoFile');
            const resultsDiv = document.getElementById('results');
            
            if (!fileInput.files[0]) {
                alert('Please select a file first');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            
            try {
                resultsDiv.innerHTML = 'Analyzing...';
                
                const response = await fetch('/api/v1/recognize', {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const result = await response.json();
                
                resultsDiv.innerHTML = `
                    <h3>Recognition Result</h3>
                    <p><strong>Band:</strong> ${result.band_name}</p>
                    <p><strong>Genre:</strong> ${result.genre}</p>
                    <p><strong>Confidence:</strong> ${result.confidence.toFixed(1)}%</p>
                    ${result.description ? `<p><strong>Description:</strong> ${result.description}</p>` : ''}
                    ${result._cache_metadata?.cached_at ? '<p>✨ <em>From cache</em></p>' : ''}
                `;
                
            } catch (error) {
                resultsDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
            }
        }
    </script>
</body>
</html>
```

### Node.js Example

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const path = require('path');

class LogoRecognitionAPI {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
        this.client = axios.create({
            baseURL: baseURL,
            timeout: 60000, // 60 seconds
        });
    }
    
    async recognizeLogo(imagePath, options = {}) {
        try {
            const form = new FormData();
            const imageStream = fs.createReadStream(imagePath);
            form.append('file', imageStream, path.basename(imagePath));
            
            // Add optional parameters
            if (options.providerPreference) {
                form.append('provider_preference', JSON.stringify(options.providerPreference));
            }
            if (options.forceRefresh) {
                form.append('force_refresh', 'true');
            }
            
            const response = await this.client.post('/api/v1/recognize', form, {
                headers: {
                    ...form.getHeaders(),
                    'Accept': 'application/json'
                }
            });
            
            return response.data;
            
        } catch (error) {
            if (error.response) {
                throw new Error(`API Error ${error.response.status}: ${error.response.data?.detail?.message || error.response.statusText}`);
            } else if (error.code === 'ENOTFOUND') {
                throw new Error('Cannot connect to API server. Is it running?');
            } else {
                throw error;
            }
        }
    }
    
    async getHealth() {
        try {
            const response = await this.client.get('/health');
            return response.data;
        } catch (error) {
            return { status: 'unhealthy', error: error.message };
        }
    }
}

// Example usage
async function main() {
    const api = new LogoRecognitionAPI();
    
    // Check API health
    const health = await api.getHealth();
    console.log('API Health:', health.status);
    
    if (health.status !== 'healthy') {
        console.error('API is not healthy, exiting');
        return;
    }
    
    try {
        // Recognize a logo
        const result = await api.recognizeLogo('./sample_logo.jpg', {
            providerPreference: ['openai', 'anthropic']
        });
        
        console.log('Recognition Result:');
        console.log(`Band: ${result.band_name}`);
        console.log(`Genre: ${result.genre}`);
        console.log(`Confidence: ${result.confidence.toFixed(1)}%`);
        
        if (result.description) {
            console.log(`Description: ${result.description}`);
        }
        
        if (result._cache_metadata?.cached_at) {
            console.log('✨ Result was retrieved from cache');
        }
        
    } catch (error) {
        console.error('Recognition failed:', error.message);
    }
}

main().catch(console.error);
```

## 🐚 Shell/Bash Examples

### Simple cURL Example

```bash
#!/bin/bash

# Basic logo recognition
recognize_logo() {
    local image_file="$1"
    local api_url="${2:-http://localhost:8000}"
    
    if [[ ! -f "$image_file" ]]; then
        echo "Error: File '$image_file' not found"
        return 1
    fi
    
    echo "Analyzing $image_file..."
    
    curl -s -X POST "$api_url/api/v1/recognize" \
        -F "file=@$image_file" \
        -H "Accept: application/json" | \
    jq -r '"Band: " + .band_name + " (" + (.confidence | tostring) + "%)"'
}

# Example usage
recognize_logo "sample_logo.jpg"
```

### Batch Processing Script

```bash
#!/bin/bash

API_URL="http://localhost:8000"
LOGO_DIR="./logos"
OUTPUT_FILE="recognition_results.json"

echo "Starting batch logo recognition..."
echo "[]" > "$OUTPUT_FILE"

# Check API health
health_status=$(curl -s "$API_URL/health" | jq -r '.status')
if [[ "$health_status" != "healthy" ]]; then
    echo "Error: API is not healthy (status: $health_status)"
    exit 1
fi

# Process each image file
for image_file in "$LOGO_DIR"/*.{jpg,jpeg,png,gif,webp}; do
    if [[ -f "$image_file" ]]; then
        echo "Processing: $(basename "$image_file")"
        
        # Make API request
        result=$(curl -s -X POST "$API_URL/api/v1/recognize" \
            -F "file=@$image_file" \
            -H "Accept: application/json")
        
        # Check if request was successful
        if echo "$result" | jq -e '.band_name' >/dev/null 2>&1; then
            # Add source file info and append to results
            enhanced_result=$(echo "$result" | jq --arg file "$(basename "$image_file")" '. + {source_file: $file}')
            
            # Append to results file
            jq --argjson new_result "$enhanced_result" '. += [$new_result]' "$OUTPUT_FILE" > temp.json && mv temp.json "$OUTPUT_FILE"
            
            # Print summary
            band_name=$(echo "$result" | jq -r '.band_name')
            confidence=$(echo "$result" | jq -r '.confidence')
            echo "  ✅ Result: $band_name ($confidence%)"
        else
            echo "  ❌ Failed to recognize logo"
            
            # Log error
            error_result=$(jq -n \
                --arg file "$(basename "$image_file")" \
                --arg error "Recognition failed" \
                '{source_file: $file, error: $error, band_name: "Error", confidence: 0}')
            
            jq --argjson error_result "$error_result" '. += [$error_result]' "$OUTPUT_FILE" > temp.json && mv temp.json "$OUTPUT_FILE"
        fi
        
        # Small delay to respect rate limits
        sleep 1
    fi
done

echo "Batch processing complete. Results saved to $OUTPUT_FILE"

# Print summary
total_files=$(jq 'length' "$OUTPUT_FILE")
successful_files=$(jq '[.[] | select(.error == null)] | length' "$OUTPUT_FILE")
echo "Summary: $successful_files/$total_files files processed successfully"
```

## 🧪 Testing Examples

### API Testing with pytest

```python
import pytest
import requests
from pathlib import Path
import tempfile
from PIL import Image
import io

@pytest.fixture
def api_url():
    """API base URL for testing"""
    return "http://localhost:8000"

@pytest.fixture
def sample_image():
    """Create a sample test image"""
    # Create a simple test image
    img = Image.new('RGB', (200, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

class TestLogoRecognitionAPI:
    
    def test_health_endpoint(self, api_url):
        """Test the health check endpoint"""
        response = requests.get(f"{api_url}/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "checks" in data
    
    def test_recognize_endpoint_success(self, api_url, sample_image):
        """Test successful logo recognition"""
        files = {'file': ('test.jpg', sample_image, 'image/jpeg')}
        
        response = requests.post(f"{api_url}/api/v1/recognize", files=files)
        assert response.status_code == 200
        
        data = response.json()
        assert "band_name" in data
        assert "confidence" in data
        assert "genre" in data
        assert isinstance(data["confidence"], (int, float))
        assert 0 <= data["confidence"] <= 100
    
    def test_recognize_endpoint_no_file(self, api_url):
        """Test recognition endpoint without file"""
        response = requests.post(f"{api_url}/api/v1/recognize")
        assert response.status_code == 422  # Validation error
    
    def test_recognize_endpoint_invalid_file(self, api_url):
        """Test recognition endpoint with invalid file"""
        files = {'file': ('test.txt', b'not an image', 'text/plain')}
        
        response = requests.post(f"{api_url}/api/v1/recognize", files=files)
        assert response.status_code == 400  # Bad request
    
    def test_rate_limiting(self, api_url, sample_image):
        """Test rate limiting functionality"""
        files = {'file': ('test.jpg', sample_image, 'image/jpeg')}
        
        # Make multiple rapid requests
        responses = []
        for _ in range(15):  # Exceed default rate limit
            sample_image.seek(0)  # Reset file pointer
            response = requests.post(f"{api_url}/api/v1/recognize", files=files)
            responses.append(response.status_code)
        
        # Should get some 429 (Too Many Requests) responses
        assert 429 in responses
```

## 📊 Performance Testing

### Load Testing with Artillery

```yaml
# artillery-config.yml
config:
  target: 'http://localhost:8000'
  phases:
    - duration: 60
      arrivalRate: 5
      name: "Warm up"
    - duration: 300
      arrivalRate: 10
      name: "Load test"
  processor: "./test-functions.js"

scenarios:
  - name: "Logo Recognition"
    weight: 100
    flow:
      - post:
          url: "/api/v1/recognize"
          beforeRequest: "setImageFile"
          capture:
            - json: "$.band_name"
              as: "bandName"
            - json: "$.confidence"
              as: "confidence"
      - think: 2
```

```javascript
// test-functions.js
const fs = require('fs');
const path = require('path');

function setImageFile(requestParams, context, ee, next) {
  // Load a test image file
  const imagePath = path.join(__dirname, 'test-logo.jpg');
  const imageBuffer = fs.readFileSync(imagePath);
  
  requestParams.formData = {
    file: {
      value: imageBuffer,
      options: {
        filename: 'test-logo.jpg',
        contentType: 'image/jpeg'
      }
    }
  };
  
  return next();
}

module.exports = {
  setImageFile
};
```

## 🔗 Integration Examples

### Discord Bot Integration

```python
import discord
from discord.ext import commands
import requests
import tempfile
import os

class LogoBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_url = "http://localhost:8000"
    
    @commands.command(name='recognize')
    async def recognize_logo(self, ctx):
        """Recognize a logo from an attached image"""
        
        if not ctx.message.attachments:
            await ctx.send("Please attach an image to recognize!")
            return
        
        attachment = ctx.message.attachments[0]
        
        # Check if it's an image
        if not any(attachment.filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
            await ctx.send("Please attach a valid image file!")
            return
        
        await ctx.send("🔍 Analyzing logo...")
        
        try:
            # Download the image to a temporary file
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
                await attachment.save(tmp_file.name)
                
                # Send to recognition API
                with open(tmp_file.name, 'rb') as f:
                    files = {'file': f}
                    response = requests.post(f"{self.api_url}/api/v1/recognize", files=files)
                
                # Clean up temp file
                os.unlink(tmp_file.name)
            
            if response.status_code == 200:
                result = response.json()
                
                embed = discord.Embed(
                    title="🎸 Logo Recognition Result",
                    color=0x8B0000  # Dark red
                )
                embed.add_field(name="Band", value=result['band_name'], inline=True)
                embed.add_field(name="Genre", value=result.get('genre', 'Unknown'), inline=True)
                embed.add_field(name="Confidence", value=f"{result['confidence']:.1f}%", inline=True)
                
                if result.get('description'):
                    embed.add_field(name="Description", value=result['description'], inline=False)
                
                if result.get('_cache_metadata', {}).get('cached_at'):
                    embed.set_footer(text="✨ Result retrieved from cache")
                
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"❌ Recognition failed: {response.status_code}")
                
        except Exception as e:
            await ctx.send(f"❌ Error: {str(e)}")

# Bot setup
bot = commands.Bot(command_prefix='!')
bot.add_cog(LogoBot(bot))

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Run the bot (requires DISCORD_TOKEN environment variable)
bot.run(os.getenv('DISCORD_TOKEN'))
```

This comprehensive examples collection shows how to integrate LOGODETH into various applications and workflows! 🚀