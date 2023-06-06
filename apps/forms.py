from django import forms

class VideoForm(forms.Form):
    name = forms.CharField(max_length=255)
    video_file = forms.FileField()
    
# class CustomUserCreationForm(UserCreationForm):
#     e_email = forms.EmailField(required=True, label="Emergency Email")

#     class Meta:
#         model = User
#         fields = UserCreationForm.Meta.fields + ("e_email",)