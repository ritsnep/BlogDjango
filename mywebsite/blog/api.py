import json
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from django.core.files.base import ContentFile
from django.contrib.auth.models import User

from .models import Post, Category, Tag

import requests


def _check_api_key(request):
    api_key = request.headers.get("X-API-Key") or request.META.get("HTTP_X_API_KEY")
    expected = getattr(settings, "API_SECRET_KEY", None)
    if not expected or api_key != expected:
        return False
    return True


def _json_error(message, status=400, extra=None):
    payload = {"error": message}
    if extra:
        payload.update(extra)
    return JsonResponse(payload, status=status)


def _parse_json_body(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}"), None
    except Exception:
        return None, _json_error("Invalid JSON body")


@csrf_exempt
def create_post_api(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"]) 

    if not _check_api_key(request):
        return _json_error("Unauthorized", status=401)

    data, err = _parse_json_body(request)
    if err:
        return err

    title = (data.get("title") or "").strip()
    intro = (data.get("intro") or "").strip()
    body = data.get("body") or ""
    category_slug = (data.get("category_slug") or "").strip()

    if not title:
        return _json_error("Missing required field: title")
    if not intro:
        return _json_error("Missing required field: intro")
    if not body:
        return _json_error("Missing required field: body")
    if not category_slug:
        return _json_error("Missing required field: category_slug")

    try:
        category = Category.objects.get(slug=category_slug)
    except Category.DoesNotExist:
        return _json_error("Invalid category_slug")

    status_value = (data.get("status") or Post.ACTIVE).lower()
    if status_value not in (Post.ACTIVE, Post.DRAFT):
        return _json_error("Invalid status. Must be 'active' or 'draft'")

    author_username = (data.get("author_username") or getattr(settings, "API_DEFAULT_AUTHOR_USERNAME", "")).strip()
    author = None
    if author_username:
        author = User.objects.filter(username=author_username).first()
        if not author:
            slug_user = slugify(author_username)
            if slug_user:
                author = User.objects.filter(username=slug_user).first()
                if not author:
                    author = User.objects.create_user(username=slug_user, password=None)
                    author.first_name = author_username
                    author.save()

    slug = (data.get("slug") or slugify(title))
    if not slug:
        slug = slugify(title) or "post"
    original_slug = slug
    count = 1
    while Post.objects.filter(slug=slug).exists():
        slug = f"{original_slug}-{count}"
        count += 1

    post = Post(
        category=category,
        author=author,
        title=title,
        slug=slug,
        intro=intro,
        body=body,
        status=status_value,
    )
    post.save()

    tags_value = data.get("tags")
    tag_objects = []
    if tags_value:
        if isinstance(tags_value, str):
            tags_iter = [t.strip() for t in tags_value.split(",")]
        elif isinstance(tags_value, list):
            tags_iter = tags_value
        else:
            tags_iter = []
        for t in tags_iter:
            name = (t or "").strip()
            if not name:
                continue
            t_slug = slugify(name)
            try:
                tag = Tag.objects.get(slug=t_slug)
            except Tag.DoesNotExist:
                display_name = name if name else t_slug.replace("-", " ").title()
                tag = Tag.objects.create(name=display_name, slug=t_slug)
            tag_objects.append(tag)
    if tag_objects:
        post.tags.set(tag_objects)

    image_url = (data.get("image_url") or "").strip()
    if image_url and not post.image:
        try:
            resp = requests.get(image_url, timeout=15)
            if resp.status_code == 200 and resp.content:
                filename = image_url.split("/")[-1]
                if "?" in filename:
                    filename = filename.split("?")[0]
                if not filename:
                    filename = "image_from_url.jpg"
                post.image.save(filename, ContentFile(resp.content), save=True)
        except Exception:
            pass

    absolute_url = request.build_absolute_uri(post.get_absolute_url())
    return JsonResponse(
        {
            "id": post.id,
            "slug": post.slug,
            "status": post.status,
            "category": post.category.slug,
            "author": post.author.username if post.author else None,
            "absolute_url": absolute_url,
        },
        status=201,
    )


@csrf_exempt
def list_categories_api(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"]) 

    if not _check_api_key(request):
        return _json_error("Unauthorized", status=401)

    items = [{"title": c.title, "slug": c.slug} for c in Category.objects.all()]
    return JsonResponse({"categories": items})


@csrf_exempt
def list_tags_api(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"]) 

    if not _check_api_key(request):
        return _json_error("Unauthorized", status=401)

    items = [{"name": t.name, "slug": t.slug} for t in Tag.objects.all()]
    return JsonResponse({"tags": items})


@csrf_exempt
def update_post_status_api(request, post_id):
    if request.method not in ("POST", "PATCH"):
        return HttpResponseNotAllowed(["POST", "PATCH"])

    if not _check_api_key(request):
        return _json_error("Unauthorized", status=401)

    data, err = _parse_json_body(request)
    if err:
        return err

    status_value = (data.get("status") or "").strip().lower()
    if status_value not in (Post.ACTIVE, Post.DRAFT):
        return _json_error("Invalid status. Must be 'active' or 'draft'")

    post = Post.objects.filter(id=post_id).first()
    if not post:
        return _json_error("Post not found", status=404)

    post.status = status_value
    post.save(update_fields=["status"])

    absolute_url = request.build_absolute_uri(post.get_absolute_url())
    return JsonResponse(
        {
            "id": post.id,
            "slug": post.slug,
            "status": post.status,
            "category": post.category.slug,
            "author": post.author.username if post.author else None,
            "absolute_url": absolute_url,
        },
        status=200,
    )


@csrf_exempt
def update_post_status_by_slug_api(request, slug):
    if request.method not in ("POST", "PATCH"):
        return HttpResponseNotAllowed(["POST", "PATCH"])

    if not _check_api_key(request):
        return _json_error("Unauthorized", status=401)

    data, err = _parse_json_body(request)
    if err:
        return err

    status_value = (data.get("status") or "").strip().lower()
    if status_value not in (Post.ACTIVE, Post.DRAFT):
        return _json_error("Invalid status. Must be 'active' or 'draft'")

    post = Post.objects.filter(slug=slug).first()
    if not post:
        return _json_error("Post not found", status=404)

    post.status = status_value
    post.save(update_fields=["status"])

    absolute_url = request.build_absolute_uri(post.get_absolute_url())
    return JsonResponse(
        {
            "id": post.id,
            "slug": post.slug,
            "status": post.status,
            "category": post.category.slug,
            "author": post.author.username if post.author else None,
            "absolute_url": absolute_url,
        },
        status=200,
    )
