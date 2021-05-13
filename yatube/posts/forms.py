from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    """Form for adding a post."""
    class Meta:
        model = Post
        fields = ('group', 'text', 'image')
        help_texts = {
            'group': 'Выбирай с умом!',
            'text': 'Текст сам себя не напишет!',
            'image': 'Неплохо бы и картинку добавить!',
        }


class CommentForm(forms.ModelForm):
    """Form for adding a comment."""
    text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        exclude = ('post', 'author', 'created')
        help_texts = {'text': 'Без мата, а то сам понимаешь..'}
