class CorrectYoutubeVideoUrl:
    """Проверяет, что video_url — это ссылка на YouTube"""
    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)
        if not value:  # пропускаем, если пусто — пусть required решает
            return attrs

        youtube_regex = r'https?://(?:www\.|m\.)?youtube\.com/'
        if not re.search(youtube_regex, value):
            raise serializers.ValidationError({
                self.field: "Ссылка должна быть на видео с YouTube."
            })
