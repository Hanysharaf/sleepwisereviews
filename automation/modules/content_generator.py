"""
SleepWise Automation Agent - Content Generator
Generates content using Claude API.
"""

import anthropic
import logging
import json
import random
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime, timezone

import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import ANTHROPIC_API_KEY, CONTENT_CONFIG, INSTAGRAM_CONFIG

logger = logging.getLogger(__name__)


class ContentGenerator:
    """Generates content using Claude API."""

    def __init__(self, api_key: str = None):
        """
        Initialize the content generator.

        Args:
            api_key: Anthropic API key (defaults to env var)
        """
        self.api_key = api_key or ANTHROPIC_API_KEY
        self.client = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None
        self.model = CONTENT_CONFIG["model"]
        self.max_tokens = CONTENT_CONFIG["max_tokens"]

    def _generate(self, prompt: str, system_prompt: str = None,
                  max_tokens: int = None) -> dict:
        """
        Generate content using Claude API.

        Args:
            prompt: User prompt
            system_prompt: System instructions
            max_tokens: Max tokens to generate

        Returns:
            Generated content and metadata
        """
        if not self.client:
            logger.error("Claude API client not initialized - missing API key")
            return {"ok": False, "error": "API key not configured"}

        try:
            messages = [{"role": "user", "content": prompt}]

            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens or self.max_tokens,
                "messages": messages
            }

            if system_prompt:
                kwargs["system"] = system_prompt

            response = self.client.messages.create(**kwargs)

            content = response.content[0].text
            return {
                "ok": True,
                "content": content,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }

        except anthropic.APIError as e:
            logger.error(f"Claude API error: {e}")
            return {"ok": False, "error": str(e)}

    # ==========================================================================
    # Article Generation
    # ==========================================================================

    def generate_article(self, topic: str, content_type: str = "buying_guide",
                         target_length: int = None) -> dict:
        """
        Generate a full article for the website.

        Args:
            topic: Article topic
            content_type: Type of content (buying_guide, product_review, etc.)
            target_length: Target word count

        Returns:
            Generated article with metadata
        """
        target_length = target_length or CONTENT_CONFIG["article_length"]

        system_prompt = """You are an expert sleep health writer for SleepWise Reviews,
a website that helps people improve their sleep quality through product reviews and advice.

Write engaging, SEO-optimized articles that are:
- Informative and backed by sleep science
- Easy to read with clear formatting
- Helpful for readers making purchasing decisions
- Professional but friendly in tone

Always include practical tips and actionable advice."""

        content_type_instructions = {
            "buying_guide": "Write a comprehensive buying guide that helps readers choose the best product.",
            "product_review": "Write an honest, detailed product review covering pros, cons, and who it's best for.",
            "how_to": "Write a step-by-step guide with practical instructions.",
            "comparison": "Write a comparison article that objectively compares different options.",
            "tips_list": "Write a listicle with actionable tips and advice."
        }

        prompt = f"""Write a {target_length}-word article about: {topic}

Article type: {content_type_instructions.get(content_type, content_type_instructions["buying_guide"])}

Structure the article with:
1. An engaging introduction that hooks the reader
2. Clear H2 and H3 headings for easy scanning
3. Practical, actionable content
4. A conclusion with key takeaways

Format the output as JSON with these fields:
{{
    "title": "SEO-optimized article title",
    "meta_description": "155-character meta description for SEO",
    "keywords": ["keyword1", "keyword2", ...],
    "introduction": "Opening paragraph",
    "sections": [
        {{
            "heading": "Section H2 heading",
            "content": "Section content with paragraphs",
            "subsections": [
                {{
                    "heading": "H3 subheading",
                    "content": "Subsection content"
                }}
            ]
        }}
    ],
    "conclusion": "Concluding paragraph with takeaways",
    "faq": [
        {{
            "question": "Common question?",
            "answer": "Helpful answer"
        }}
    ]
}}"""

        result = self._generate(prompt, system_prompt, max_tokens=4096)

        if result.get("ok"):
            try:
                # Parse the JSON response
                content = result["content"]
                # Find JSON in the response
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    article_data = json.loads(content[json_start:json_end])
                    result["article"] = article_data
            except json.JSONDecodeError as e:
                logger.warning(f"Could not parse article JSON: {e}")
                result["article"] = {"raw_content": result["content"]}

        return result

    # ==========================================================================
    # Social Media Content
    # ==========================================================================

    def generate_instagram_caption(self, topic: str, article_excerpt: str = None,
                                   style: str = "informative") -> dict:
        """
        Generate an Instagram caption.

        Args:
            topic: Post topic
            article_excerpt: Optional excerpt from related article
            style: Caption style (informative, engaging, question, etc.)

        Returns:
            Caption with hashtags
        """
        system_prompt = """You are a social media expert for a sleep health brand.
Create engaging Instagram captions that:
- Start with a hook (emoji or question)
- Are easy to read (short sentences, line breaks)
- Include a call to action
- Feel authentic and helpful, not salesy"""

        prompt = f"""Write an Instagram caption about: {topic}

Style: {style}
{"Reference this content: " + article_excerpt if article_excerpt else ""}

Provide the response as JSON:
{{
    "caption": "The caption text with line breaks as \\n",
    "suggested_hashtags": ["hashtag1", "hashtag2", ...],
    "best_posting_time": "suggested time to post"
}}

Keep the caption under 2200 characters. Suggest 15-20 relevant hashtags."""

        result = self._generate(prompt, system_prompt, max_tokens=1024)

        if result.get("ok"):
            try:
                content = result["content"]
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    caption_data = json.loads(content[json_start:json_end])
                    result["caption_data"] = caption_data
            except json.JSONDecodeError as e:
                logger.warning(f"Could not parse caption JSON: {e}")
                result["caption_data"] = {"caption": result["content"]}

        return result

    def generate_pinterest_description(self, title: str, article_summary: str,
                                        keywords: List[str]) -> dict:
        """
        Generate a Pinterest pin description.

        Args:
            title: Pin title
            article_summary: Brief article summary
            keywords: Target keywords

        Returns:
            Optimized Pinterest description
        """
        system_prompt = """You are a Pinterest marketing expert.
Create pin descriptions that are keyword-rich and encourage clicks."""

        prompt = f"""Write a Pinterest pin description for:

Title: {title}
Summary: {article_summary}
Keywords: {', '.join(keywords)}

The description should:
- Be 100-300 characters
- Include 2-3 relevant keywords naturally
- Have a call to action
- Include 3-5 hashtags at the end

Return as JSON:
{{
    "description": "The pin description",
    "hashtags": ["hashtag1", "hashtag2"]
}}"""

        result = self._generate(prompt, system_prompt, max_tokens=256)

        if result.get("ok"):
            try:
                content = result["content"]
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    pin_data = json.loads(content[json_start:json_end])
                    result["pin_data"] = pin_data
            except json.JSONDecodeError:
                result["pin_data"] = {"description": result["content"]}

        return result

    # ==========================================================================
    # Content Ideas & Planning
    # ==========================================================================

    def generate_content_ideas(self, category: str = None, count: int = 5) -> dict:
        """
        Generate content ideas for the week.

        Args:
            category: Specific category to focus on
            count: Number of ideas to generate

        Returns:
            List of content ideas
        """
        topics = CONTENT_CONFIG["topics"]
        if category:
            focus = category
        else:
            focus = random.choice(topics)

        system_prompt = """You are a content strategist for a sleep health website.
Generate creative, SEO-friendly content ideas that will engage readers and rank well."""

        prompt = f"""Generate {count} unique content ideas related to: {focus}

For each idea, provide:
{{
    "ideas": [
        {{
            "title": "Article title",
            "content_type": "buying_guide/product_review/how_to/comparison/tips_list",
            "target_keywords": ["keyword1", "keyword2"],
            "estimated_search_volume": "high/medium/low",
            "brief": "2-3 sentence description of the article"
        }}
    ]
}}

Focus on topics that:
- People are actively searching for
- Can include affiliate product recommendations
- Provide genuine value to readers"""

        result = self._generate(prompt, system_prompt, max_tokens=1024)

        if result.get("ok"):
            try:
                content = result["content"]
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                if json_start >= 0 and json_end > json_start:
                    ideas_data = json.loads(content[json_start:json_end])
                    result["ideas"] = ideas_data.get("ideas", [])
            except json.JSONDecodeError:
                result["ideas"] = []

        return result

    def select_random_topic(self) -> str:
        """Select a random topic from configured topics."""
        return random.choice(CONTENT_CONFIG["topics"])

    def select_random_content_type(self) -> str:
        """Select a random content type."""
        return random.choice(CONTENT_CONFIG["content_types"])

    # ==========================================================================
    # Utility Methods
    # ==========================================================================

    def test_connection(self) -> bool:
        """Test the Claude API connection."""
        if not self.client:
            logger.error("Claude API client not initialized")
            return False

        result = self._generate("Say 'Connection successful' in exactly those words.",
                               max_tokens=20)
        if result.get("ok"):
            logger.info("Claude API connection successful")
            return True
        logger.error("Failed to connect to Claude API")
        return False

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Estimate API cost for token usage.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Estimated cost in USD
        """
        # Claude 3.5 Sonnet pricing (as of 2024)
        input_cost_per_1k = 0.003
        output_cost_per_1k = 0.015

        input_cost = (input_tokens / 1000) * input_cost_per_1k
        output_cost = (output_tokens / 1000) * output_cost_per_1k

        return round(input_cost + output_cost, 4)


# =============================================================================
# Standalone test
# =============================================================================
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generator = ContentGenerator()

    if generator.test_connection():
        print("✅ Claude API connection successful!")

        # Test content generation
        print("\nGenerating sample Instagram caption...")
        result = generator.generate_instagram_caption(
            topic="Benefits of weighted blankets for anxiety",
            style="engaging"
        )

        if result.get("ok"):
            caption_data = result.get("caption_data", {})
            print(f"\nCaption:\n{caption_data.get('caption', result['content'])}")
    else:
        print("❌ Failed to connect to Claude API")
