
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Recipe
from .forms import RegisterForm
from django.db import transaction
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from .forms import (
    RecipeForm,
    IngredientFormSet,
    StepFormSet
)


# ユーザー登録
def register_view(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "ユーザー登録が完了しました。")
            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "recipes/register.html", {
        "form": form
    })


# ログイン
def login_view(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            user = authenticate(
                request,
                username=user.username,
                password=password
            )

        if user is not None:
            login(request, user)
            return redirect("recipe_list")

        messages.error(
            request,
            "メールアドレスまたはパスワードが正しくありません。"
        )

    return render(request, "recipes/login.html")


# ログアウト
def logout_view(request):
    logout(request)
    return redirect("login")


# トップページ
def index_view(request):

    if request.user.is_authenticated:
        return redirect("recipe_list")

    return redirect("login")


# レシピ一覧
@login_required
def recipe_list_view(request):

    # 検索キーワードを取得
    query = request.GET.get("q", "").strip()

    # ログイン中のユーザーのレシピだけを取得
    recipes = Recipe.objects.filter(
        owner=request.user
    )

    # キーワードが入力されている場合
    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) |
            Q(ingredients__name__icontains=query)
        ).distinct()

    # 登録日の新しい順に並べる
    recipes = recipes.order_by("-created_at")

    return render(request, "recipes/recipe_list.html", {
        "recipes": recipes,
        "query": query,
    })


# レシピ詳細
@login_required
def recipe_detail_view(request, recipe_id):

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        owner=request.user
    )

    return render(request, "recipes/recipe_detail.html", {
        "recipe": recipe
    })


# レシピ登録
@login_required
def recipe_create_view(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        ingredient_formset = IngredientFormSet(
            request.POST,
            prefix="ingredients"
        )
        step_formset = StepFormSet(
            request.POST,
            prefix="steps"
        )

        if (
            form.is_valid()
            and ingredient_formset.is_valid()
            and step_formset.is_valid()
        ):
            with transaction.atomic():
                # レシピ本体を保存
                recipe = form.save(commit=False)
                recipe.owner = request.user
                recipe.save()

                # 材料を保存
                ingredient_formset.instance = recipe
                ingredients = ingredient_formset.save(commit=False)

                for index, ingredient in enumerate(ingredients):
                    ingredient.sort_order = index + 1
                    ingredient.save()

                for ingredient in ingredient_formset.deleted_objects:
                    ingredient.delete()

                ingredient_formset.save_m2m()

                # 作り方を保存
                step_formset.instance = recipe
                steps = step_formset.save(commit=False)

                for index, step in enumerate(steps):
                    step.step_number = index + 1
                    step.save()

                for step in step_formset.deleted_objects:
                    step.delete()

                step_formset.save_m2m()

            return redirect("recipe_detail", recipe_id=recipe.id)

    else:
        form = RecipeForm()
        ingredient_formset = IngredientFormSet(prefix="ingredients")
        step_formset = StepFormSet(prefix="steps")

    return render(
        request,
        "recipes/recipe_create.html",
        {
            "form": form,
            "ingredient_formset": ingredient_formset,
            "step_formset": step_formset,
        }
    )
# レシピ画像表示
@login_required
def recipe_image_view(request, recipe_id):

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        owner=request.user
    )

    if not recipe.image:
        raise Http404

    return FileResponse(
        recipe.image.open("rb")
    )
    

# レシピ編集
@login_required
def recipe_edit_view(request, recipe_id):

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        owner=request.user
    )

    if request.method == "POST":
        form = RecipeForm(
            request.POST,
            request.FILES,
            instance=recipe
        )

        ingredient_formset = IngredientFormSet(
            request.POST,
            instance=recipe,
            prefix="ingredients"
        )

        step_formset = StepFormSet(
            request.POST,
            instance=recipe,
            prefix="steps"
        )

        if (
            form.is_valid()
            and ingredient_formset.is_valid()
            and step_formset.is_valid()
        ):
            with transaction.atomic():

                # レシピ本体を更新
                form.save()

                # 材料を更新
                ingredients = ingredient_formset.save(
                    commit=False
                )

                for index, ingredient in enumerate(ingredients):
                    ingredient.sort_order = index + 1
                    ingredient.save()

                for ingredient in ingredient_formset.deleted_objects:
                    ingredient.delete()

                ingredient_formset.save_m2m()

                # 作り方を更新
                steps = step_formset.save(commit=False)

                for index, step in enumerate(steps):
                    step.step_number = index + 1
                    step.save()

                for step in step_formset.deleted_objects:
                    step.delete()

                step_formset.save_m2m()

            messages.success(request, "レシピを更新しました。")

            return redirect(
                "recipe_detail",
                recipe_id=recipe.id
            )

    else:
        form = RecipeForm(instance=recipe)

        ingredient_formset = IngredientFormSet(
            instance=recipe,
            prefix="ingredients"
        )

        step_formset = StepFormSet(
            instance=recipe,
            prefix="steps"
        )

    return render(
        request,
        "recipes/recipe_edit.html",
        {
            "recipe": recipe,
            "form": form,
            "ingredient_formset": ingredient_formset,
            "step_formset": step_formset,
        }
    )


# レシピ削除
@login_required
@require_POST
def recipe_delete_view(request, recipe_id):

    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        owner=request.user
    )

    recipe.delete()

    messages.success(request, "レシピを削除しました。")

    return redirect("recipe_list")