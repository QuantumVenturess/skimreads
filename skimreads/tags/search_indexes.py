from haystack import indexes
from tags.models import Tag

class TagIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    created = indexes.DateTimeField(model_attr='created')
    name = indexes.CharField(model_attr='name')
    slug = indexes.CharField(model_attr='slug')
    user = indexes.CharField(model_attr='user')
    username = indexes.CharField(model_attr='user__username')

    def get_model(self):
        return Tag

    def index_queryset(self):
        return self.get_model().objects.all()

    def prepare_name(self, obj):
        return obj.name.capitalize()