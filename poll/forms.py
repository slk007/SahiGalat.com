from django.forms import ModelForm
from .models import Comment


class AddCommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['comment_text',]