from django.db import migrations
from django.utils.text import slugify


def _dedupe_slug(model, base_slug, slug_field="slug", extra_filter=None):
    slug = base_slug
    i = 1
    while True:
        qs = model.objects.all()
        if extra_filter:
            qs = qs.filter(**extra_filter)
        qs = qs.filter(**{slug_field: slug})
        if not qs.exists():
            return slug
        slug = f"{base_slug}-{i}"
        i += 1


def lowercase_slugs(apps, schema_editor):
    Category = apps.get_model("blog", "Category")
    Tag = apps.get_model("blog", "Tag")
    Post = apps.get_model("blog", "Post")

    for cat in Category.objects.all().iterator():
        base = slugify(cat.slug or cat.title)
        if not base:
            base = "category"
        desired = base
        if Category.objects.exclude(pk=cat.pk).filter(slug=desired).exists():
            desired = _dedupe_slug(Category, base, extra_filter=None)
        if cat.slug != desired:
            cat.slug = desired
            cat.save(update_fields=["slug"])

    for tag in Tag.objects.all().iterator():
        base = slugify(tag.slug or tag.name)
        if not base:
            base = "tag"
        desired = base
        if Tag.objects.exclude(pk=tag.pk).filter(slug=desired).exists():
            desired = _dedupe_slug(Tag, base, extra_filter=None)
        if tag.slug != desired:
            tag.slug = desired
            tag.save(update_fields=["slug"])

    for post in Post.objects.all().iterator():
        base = slugify(post.slug or post.title)
        if not base:
            base = "post"
        desired = base
        if Post.objects.exclude(pk=post.pk).filter(slug=desired).exists():
            desired = _dedupe_slug(Post, base, extra_filter=None)
        if post.slug != desired:
            post.slug = desired
            post.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0011_tag_post_tags"),
    ]

    operations = [
        migrations.RunPython(lowercase_slugs, reverse_code=migrations.RunPython.noop),
    ]
