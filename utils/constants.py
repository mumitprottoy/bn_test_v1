DATE_STR_FORMAT_1 = "%B %d, %Y"
DATETIME_STR_FORMAT_1 = "%I : %M %p %a %d %b, %Y"
DEFAULT_CENTER_LOGO = 'https://logos.bowlersnetwork.com/pinsX.jpg'
PROFILE_PIC_SUPPORTED_FILES = ['jpg', 'jpeg', 'png', 'gif']
COVER_PHOTO_SUPPORTED_FILES = ['jpg', 'jpeg', 'png']
INTRO_VIDEO_SUPPORTED_FILES = [
    "mp4",   # H.264 + AAC codec required
    "webm",  # VP8/VP9 + Vorbis/Opus
    "ogg",   # Ogg Theora video
]
MEDIA_CONTENT_SUPPORTED_FILES = [
    # Image types supported in browsers
    ".jpg", ".jpeg",
    ".png",
    ".gif",
    ".webp",
    ".avif",
    ".svg",

    # Video types supported in HTML5 video tag
    ".mp4",   # H.264 + AAC codec required
    ".webm",  # VP8/VP9 + Vorbis/Opus
    ".ogg",   # Ogg Theora video
    "mkv",

    # (Optional) Audio types — if needed in posts
    # ".mp3", ".wav", ".ogg"
]

FILE_TYPE_EXT_MAP = {
    'photos': [".jpg", ".jpeg",
    ".png",
    ".webp",
    ".avif",
    ".svg",],
    'gifs': ['gif'],
    'videos': [".mp4",   # H.264 + AAC codec required
    ".webm",  # VP8/VP9 + Vorbis/Opus
    ".ogg",   # Ogg Theora video
    "mkv",]
}

def get_media_type(ext: str) -> str:
    for k in FILE_TYPE_EXT_MAP.keys():
        if ext in FILE_TYPE_EXT_MAP[k]:
            return k

POPULAR_SOCIALS = {
    "facebook": {
        "name": "Facebook",
        "logo": "https://logo.clearbit.com/facebook.com"
    },
    "instagram": {
        "name": "Instagram",
        "logo": "https://logo.clearbit.com/instagram.com"
    },
    "twitter": {
        "name": "Twitter",
        "logo": "https://logo.clearbit.com/twitter.com"
    },
    "linkedin": {
        "name": "LinkedIn",
        "logo": "https://logo.clearbit.com/linkedin.com"
    },
    "youtube": {
        "name": "YouTube",
        "logo": "https://logo.clearbit.com/youtube.com"
    },
    "tiktok": {
        "name": "TikTok",
        "logo": "https://logo.clearbit.com/tiktok.com"
    },
    "github": {
        "name": "GitHub",
        "logo": "https://logo.clearbit.com/github.com"
    },
    "reddit": {
        "name": "Reddit",
        "logo": "https://logo.clearbit.com/reddit.com"
    },
    "snapchat": {
        "name": "Snapchat",
        "logo": "https://logo.clearbit.com/snapchat.com"
    },
    "pinterest": {
        "name": "Pinterest",
        "logo": "https://logo.clearbit.com/pinterest.com"
    },
    "telegram": {
        "name": "Telegram",
        "logo": "https://logo.clearbit.com/telegram.org"
    },
    "whatsapp": {
        "name": "WhatsApp",
        "logo": "https://logo.clearbit.com/whatsapp.com"
    },
    "discord": {
        "name": "Discord",
        "logo": "https://logo.clearbit.com/discord.com"
    },
    "medium": {
        "name": "Medium",
        "logo": "https://logo.clearbit.com/medium.com"
    },
    "tumblr": {
        "name": "Tumblr",
        "logo": "https://logo.clearbit.com/tumblr.com"
    },
}
