from haystack import indexes
from readings.models import Note

class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    content = indexes.CharField(model_attr='content')
    created = indexes.DateTimeField(model_attr='created')
    reading = indexes.CharField(model_attr='reading')
    reading_slug = indexes.CharField(model_attr='reading')
    # reading_slug = indexes.CharField(model_attr='reading__slug')
    user = indexes.CharField(model_attr='user')

    def get_model(self):
        return Note

    def index_queryset(self):
        return self.get_model().objects.all()

    def prepare_content(self, obj):
        return obj.content.capitalize()

    def prepare_reading_slug(self, obj):
        return obj.reading.slug