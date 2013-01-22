from haystack import indexes
from readings.models import Reading

class ReadingIndex(indexes.SearchIndex, indexes.Indexable):
    # Every SearchIndex requires there to be one and only one field with
    # document=True. This indicates to both Haystack and the search engine
    # about which field is the primary field for searching within

    # The convention is to name this field text
    text = indexes.CharField(document=True, use_template=True)

    created = indexes.DateTimeField(model_attr='created')
    link = indexes.CharField(model_attr='link')
    image = indexes.CharField(model_attr='image')
    slug = indexes.CharField(model_attr='slug')
    title = indexes.CharField(model_attr='title')
    user = indexes.CharField(model_attr='user')
    views = indexes.IntegerField(model_attr='views')

    def get_model(self):
        return Reading

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()