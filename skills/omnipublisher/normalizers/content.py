class ContentNormalizer:
    """
    Adapts single input to platform-specific text and formatting rules.
    """
    def normalize(self, text, platform):
        if platform == "twitter":
            return self._to_twitter(text)
        elif platform == "instagram":
            return self._to_instagram(text)
        elif platform == "youtube":
            return self._to_youtube(text)
        elif platform == "telegram":
            return self._to_telegram(text)
        elif platform == "whatsapp":
            return self._to_whatsapp(text)
        return text

    def _to_twitter(self, text):
        # Max 280 chars, minimal hashtags
        return text[:277] + "..." if len(text) > 280 else text

    def _to_instagram(self, text):
        # Hashtag dense
        return f"{text}\n\n#reels #viral #content"

    def _to_youtube(self, text):
        # Title + Desc format
        title = text.split('\n')[0][:100]
        return {"title": title, "description": text}

    def _to_telegram(self, text):
        # Markdown supported
        return f"📢 **Update**\n\n{text}"

    def _to_whatsapp(self, text):
        # Plain text with bold markers
        return f"*Update*\n\n{text}"
