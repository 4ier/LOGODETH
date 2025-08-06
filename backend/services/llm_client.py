"""
LLM client for multimodal AI services
"""
import json
from typing import Dict, Any
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from loguru import logger

from backend.config import get_settings


class LLMClient:
    """Client for multimodal LLM APIs"""
    
    def __init__(self):
        self.settings = get_settings()
        self.openai_client = AsyncOpenAI(api_key=self.settings.openai_api_key)
        
        if self.settings.anthropic_api_key:
            self.anthropic_client = AsyncAnthropic(api_key=self.settings.anthropic_api_key)
        else:
            self.anthropic_client = None
    
    async def recognize_with_openai(self, base64_image: str) -> Dict[str, Any]:
        """
        Recognize logo using OpenAI GPT-4 Vision
        
        Args:
            base64_image: Base64 encoded image
            
        Returns:
            Dict with recognition results
        """
        prompt = """You are an expert in metal music and band logos. Analyze this metal band logo and provide:

1. The band name (be as accurate as possible)
2. The music genre/subgenre (e.g., Black Metal, Death Metal, Doom Metal, etc.)
3. Your confidence level (0-100)
4. A brief description of the logo style

Respond in JSON format:
{
    "band_name": "Band Name",
    "genre": "Genre",
    "confidence": 85,
    "description": "Brief description of the logo"
}

If you cannot identify the band, still provide your best guess with low confidence."""

        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300,
                temperature=0.1
            )
            
            # Parse response
            content = response.choices[0].message.content
            logger.debug(f"OpenAI response: {content}")
            
            # Try to parse JSON
            try:
                # Find JSON in the response
                start = content.find('{')
                end = content.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = content[start:end]
                    return json.loads(json_str)
                else:
                    # Fallback parsing
                    return self._parse_text_response(content)
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON response, using fallback parser")
                return self._parse_text_response(content)
                
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def recognize_with_anthropic(self, base64_image: str) -> Dict[str, Any]:
        """
        Recognize logo using Anthropic Claude Vision
        
        Args:
            base64_image: Base64 encoded image
            
        Returns:
            Dict with recognition results
        """
        if not self.anthropic_client:
            raise Exception("Anthropic API key not configured")
        
        prompt = """You are an expert in metal music and band logos. Analyze this metal band logo and provide:

1. The band name (be as accurate as possible)
2. The music genre/subgenre (e.g., Black Metal, Death Metal, Doom Metal, etc.)
3. Your confidence level (0-100)
4. A brief description of the logo style

Respond in JSON format:
{
    "band_name": "Band Name",
    "genre": "Genre",
    "confidence": 85,
    "description": "Brief description of the logo"
}

If you cannot identify the band, still provide your best guess with low confidence."""

        try:
            response = await self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=300,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": base64_image
                                }
                            }
                        ]
                    }
                ]
            )
            
            # Parse response
            content = response.content[0].text
            logger.debug(f"Anthropic response: {content}")
            
            # Try to parse JSON
            try:
                # Find JSON in the response
                start = content.find('{')
                end = content.rfind('}') + 1
                if start >= 0 and end > start:
                    json_str = content[start:end]
                    return json.loads(json_str)
                else:
                    return self._parse_text_response(content)
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON response, using fallback parser")
                return self._parse_text_response(content)
                
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
    
    async def recognize_with_fallback(self, base64_image: str, provider_preference: list = None) -> Dict[str, Any]:
        """
        Try multiple providers with fallback mechanism
        
        Args:
            base64_image: Base64 encoded image
            provider_preference: List of providers to try in order ['openai', 'anthropic']
            
        Returns:
            Dict with recognition results
        """
        if not provider_preference:
            provider_preference = ['openai', 'anthropic'] if self.anthropic_client else ['openai']
        
        last_error = None
        
        for provider in provider_preference:
            try:
                if provider == 'openai':
                    logger.info("Attempting recognition with OpenAI GPT-4o")
                    return await self.recognize_with_openai(base64_image)
                elif provider == 'anthropic' and self.anthropic_client:
                    logger.info("Attempting recognition with Anthropic Claude")
                    return await self.recognize_with_anthropic(base64_image)
                else:
                    logger.warning(f"Provider {provider} not available, skipping")
                    continue
                    
            except Exception as e:
                logger.error(f"Provider {provider} failed: {e}")
                last_error = e
                continue
        
        # If all providers failed, raise the last error
        if last_error:
            raise last_error
        else:
            raise Exception("No available providers configured")
    
    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """
        Fallback parser for non-JSON responses
        
        Args:
            text: Raw text response
            
        Returns:
            Dict with parsed results
        """
        # Basic fallback parsing
        result = {
            "band_name": "Unknown",
            "genre": "Metal",
            "confidence": 50,
            "description": "Could not parse response properly"
        }
        
        # Try to extract band name
        lines = text.split('\n')
        for line in lines:
            if 'band' in line.lower() and ':' in line:
                result["band_name"] = line.split(':')[-1].strip()
            elif 'genre' in line.lower() and ':' in line:
                result["genre"] = line.split(':')[-1].strip()
            elif 'confidence' in line.lower() and ':' in line:
                try:
                    conf_str = line.split(':')[-1].strip()
                    # Extract number from string
                    conf_num = ''.join(filter(str.isdigit, conf_str))
                    if conf_num:
                        result["confidence"] = min(100, max(0, int(conf_num)))
                except:
                    pass
        
        return result
    
    async def get_provider_health(self) -> Dict[str, bool]:
        """
        Check health status of available providers
        
        Returns:
            Dict with provider health status
        """
        health = {}
        
        # Test OpenAI
        try:
            # Simple test call with minimal token usage
            await self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            health['openai'] = True
        except Exception as e:
            logger.warning(f"OpenAI health check failed: {e}")
            health['openai'] = False
        
        # Test Anthropic if available
        if self.anthropic_client:
            try:
                await self.anthropic_client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1,
                    messages=[{"role": "user", "content": "test"}]
                )
                health['anthropic'] = True
            except Exception as e:
                logger.warning(f"Anthropic health check failed: {e}")
                health['anthropic'] = False
        else:
            health['anthropic'] = False
        
        return health