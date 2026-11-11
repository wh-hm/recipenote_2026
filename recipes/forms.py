from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory

from .models import Recipe, RecipeIngredient, RecipeStep


# ユーザー登録フォーム
class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True, label="メールアドレス")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    # def clean_email(self):
    #     email = self.cleaned_data["email"]

    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError(
    #             "このメールアドレスは既に登録されています。"
    #         )

    #     return email

    def clean_email(self):
        email = self.cleaned_data["email"].strip()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("このメールアドレスは既に登録されています。")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        return user


# レシピ登録・編集フォーム
# class RecipeForm(forms.ModelForm):

#     class Meta:
#         model = Recipe
#         fields = ["title", "reference_url", "image", "memo"]

#         labels = {
#             "title": "料理名",
#             "reference_url": "参考URL",
#             "image": "料理画像",
#             "memo": "メモ",
#         }

#         widgets = {
#             "memo": forms.Textarea(attrs={
#                 "rows": 5,
#                 "placeholder": "アレンジや次回作るときの注意点などを記入してください。",
#             }),
#             "image": forms.ClearableFileInput(attrs={
#                 "accept": ".jpg,.jpeg,.png,image/jpeg,image/png"
#             }),
#         }
#     def clean_title(self):
#         title = self.cleaned_data["title"]

#         if len(title) > 100:
#             raise forms.ValidationError(
#                 "料理名は100文字以内で入力してください。"
#             )


#         return title
# レシピ登録・編集フォーム
class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ["title", "reference_url", "image", "memo"]

        labels = {
            "title": "料理名",
            "reference_url": "参考URL",
            "image": "料理画像",
            "memo": "メモ",
        }

        widgets = {
            "memo": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "アレンジや次回作るときの注意点などを記入してください。",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={"accept": ".jpg,.jpeg,.png,image/jpeg,image/png"}
            ),
        }

    # 料理名の入力チェック
    def clean_title(self):
        title = self.cleaned_data["title"]

        if len(title) > 100:
            raise forms.ValidationError("料理名は100文字以内で入力してください。")

        return title

    # 参考URLの入力チェック
    def clean_reference_url(self):
        reference_url = self.cleaned_data["reference_url"]

        if reference_url and len(reference_url) > 200:
            raise forms.ValidationError("参考URLは200文字以内で入力してください。")

        return reference_url

    # メモの入力チェック
    def clean_memo(self):
        memo = self.cleaned_data["memo"]

        if memo and len(memo) > 200:
            raise forms.ValidationError("メモは200文字以内で入力してください。")

        return memo


# 材料フォーム
class IngredientForm(forms.ModelForm):

    class Meta:
        model = RecipeIngredient
        fields = ["name", "quantity"]

        labels = {
            "name": "材料名",
            "quantity": "分量",
        }


# 作り方フォーム
class StepForm(forms.ModelForm):

    class Meta:
        model = RecipeStep
        fields = ["instruction"]

        labels = {
            "instruction": "作り方",
        }


# 1つのレシピに複数の材料を登録する
IngredientFormSet = inlineformset_factory(
    Recipe, RecipeIngredient, form=IngredientForm, extra=0, can_delete=True
)


# 1つのレシピに複数の作り方を登録する
StepFormSet = inlineformset_factory(
    Recipe, RecipeStep, form=StepForm, extra=0, can_delete=True
)
