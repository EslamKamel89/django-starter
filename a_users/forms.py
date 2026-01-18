from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django import forms
from django.contrib.auth.models import User

from a_users.models import Profile

INPUT_STYLES = (
    "block w-full rounded-md border px-3 py-2 "
    "focus:ring-2 focus:ring-primary focus:border-primary"
)

PASSWORD_STYLES = INPUT_STYLES

SUBMIT_STYLES = (
    "w-full bg-primary text-white font-semibold py-2 rounded-md "
    "hover:bg-primary/90 transition"
)


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = "POST"
        self.helper.form_class = "space-y-4 max-w-lg mx-auto"
        self.helper.layout = Layout(
            Field(
                "image",
                css_class="hidden",
                **{"x-on:change": "previewAvatar(event)", "x-ref": "avatarInput"},
            ),
            Field("display_name", css_class=INPUT_STYLES, **{"x-model": "displayName"}),
            Field("info", css_class=INPUT_STYLES, rows=4),
            Submit("submit", "Save Profile", css_class=SUBMIT_STYLES),
        )

    class Meta:
        model = Profile
        fields = ("image", "display_name", "info")


class EmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
