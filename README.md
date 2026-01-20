# Search Signal Room - Django Blog Platform

A modern, feature-rich blog platform built with Django, focused on digital marketing, SEO, and PPC content. This project provides a complete blogging solution with advanced features like RSS feeds, tag management, user profiles, and a premium responsive design.

![Django](https://img.shields.io/badge/Django-4.2.9-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### Content Management
- **Rich Text Editor**: Integrated CKEditor 5 with advanced formatting options
- **Post Management**: Create, edit, and manage blog posts with draft/publish workflow
- **Category System**: Organize posts by categories with dedicated category pages
- **Tag System**: Flexible tagging with ability to create new tags on-the-fly
- **Image Support**: Upload images or use external URLs for post thumbnails
- **Comment System**: User engagement through post comments
- **Post Status**: Active, Draft, and Trash status management

### User Features
- **User Authentication**: Secure signup, login, and logout functionality
- **Author Profiles**: Detailed author pages with bio, social links, and profile images
- **User Dashboard**: Personal dashboard for managing posts and profile
- **Role-based System**: Support for Authors, Editors, Writers, SEO Experts, and Admins
- **Profile Management**: Update bio, profile image, and social media links

### Content Discovery
- **Search Functionality**: Full-text search across titles, introductions, and body content
- **Trending Posts**: Posts ranked by comment count
- **Latest Articles**: Chronologically sorted recent posts
- **Related Posts**: Context-aware post recommendations
- **Category Filtering**: Browse posts by specific categories
- **Author Pages**: View all posts by a specific author

### SEO & Syndication
- **RSS/Atom Feeds**: Automatic feed generation for content syndication
- **XML Sitemap**: Dynamic sitemap generation for search engines
- **HTML Sitemap**: User-friendly sitemap page
- **SEO-friendly URLs**: Clean, readable URL structure
- **Meta Tags**: Proper meta descriptions and title tags
- **robots.txt**: Automated robots.txt generation

### Design & UX
- **Responsive Design**: Mobile-first, fully responsive layout
- **Modern UI**: Premium design with smooth animations and transitions
- **Reading Time**: Estimated reading time calculation
- **Social Sharing**: Share posts on social media platforms
- **Newsletter Integration**: Newsletter signup functionality
- **404 Page**: Custom error page

## 🚀 Technology Stack

- **Backend**: Django 4.2.9
- **Database**: SQLite (development), PostgreSQL/MySQL compatible
- **Rich Text Editor**: django-ckeditor-5
- **Image Processing**: Pillow
- **HTTP Requests**: requests library
- **Frontend**: HTML5, CSS3, JavaScript
- **Deployment**: PythonAnywhere compatible

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- Git

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/SunilThapa7/django_blog.git
cd django_blog
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv dev
dev\Scripts\activate

# Linux/Mac
python3 -m venv dev
source dev/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Settings

The project uses environment variables for configuration. Create a `.env` file in the root directory (optional):

```env
DJANGO_DEBUG=True
SECRET_KEY=your-secret-key-here
```

### 5. Database Setup

```bash
cd mywebsite
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Collect Static Files

```bash
python manage.py collectstatic
```

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## 📁 Project Structure

```
BlogDjango/
├── mywebsite/                  # Main project directory
│   ├── blog/                   # Blog application
│   │   ├── migrations/         # Database migrations
│   │   ├── templates/          # Blog templates
│   │   │   └── blog/
│   │   │       ├── all_articles.html
│   │   │       ├── author_detail.html
│   │   │       ├── category.html
│   │   │       ├── create_post.html
│   │   │       ├── detail.html
│   │   │       ├── my_posts.html
│   │   │       └── search.html
│   │   ├── admin.py            # Admin configuration
│   │   ├── context_processors.py  # Custom context processors
│   │   ├── feeds.py            # RSS/Atom feed configuration
│   │   ├── forms.py            # Blog forms
│   │   ├── models.py           # Blog models (Post, Category, Tag, Comment)
│   │   ├── urls.py             # Blog URL patterns
│   │   └── views.py            # Blog views
│   │
│   ├── core/                   # Core application
│   │   ├── migrations/         # Database migrations
│   │   ├── templates/          # Core templates
│   │   │   └── core/
│   │   │       ├── 404.html
│   │   │       ├── about.html
│   │   │       ├── frontpage.html
│   │   │       ├── login.html
│   │   │       ├── meet_the_team.html
│   │   │       ├── signup.html
│   │   │       └── sitemap.html
│   │   ├── admin.py            # Admin configuration
│   │   ├── forms.py            # User forms
│   │   ├── models.py           # User profile model
│   │   └── views.py            # Core views
│   │
│   ├── mywebsite/              # Project settings
│   │   ├── settings.py         # Django settings
│   │   ├── urls.py             # Main URL configuration
│   │   ├── wsgi.py             # WSGI configuration
│   │   └── sitemaps.py         # Sitemap configuration
│   │
│   ├── static/                 # Static files
│   │   └── sitemap.xsl         # Sitemap stylesheet
│   │
│   ├── media/                  # User-uploaded files
│   ├── db.sqlite3              # SQLite database
│   └── manage.py               # Django management script
│
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🎯 Usage

### Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin/` to:
- Manage posts, categories, and tags
- Moderate comments
- Manage user profiles and roles
- Configure site settings

### Creating Posts

1. **Via Admin Panel**: 
   - Login to admin panel
   - Navigate to Posts → Add Post
   - Fill in details and publish

2. **Via Frontend**:
   - Login to your account
   - Navigate to "Create Post"
   - Use the rich text editor to compose your article
   - Add tags, category, and featured image
   - Save as draft or publish immediately

### Managing Content

- **My Posts Dashboard**: Access at `/my-posts/` to manage your articles
- **Edit Posts**: Click edit on any of your posts
- **Trash/Restore**: Move posts to trash or restore them
- **Delete Permanently**: Remove posts from trash permanently
- **Manage Comments**: View and delete comments on your posts

### User Profiles

- Update your profile at the "My Posts" page
- Add profile image (upload or URL)
- Set bio and social media links
- Configure display name

## 🔌 API Endpoints

### Public Endpoints

- `/` - Homepage
- `/<category-slug>/` - Category page
- `/<category-slug>/<post-slug>/` - Post detail
- `/author/<username>/` - Author profile
- `/search/?query=<term>` - Search results
- `/all-latest/` - All latest articles
- `/all-trending/` - Trending articles
- `/feed/` - RSS feed
- `/feed/atom/` - Atom feed
- `/sitemap.xml` - XML sitemap
- `/sitemap/` - HTML sitemap

### Authenticated Endpoints

- `/create-post/` - Create new post
- `/post/<slug>/edit/` - Edit post
- `/my-posts/` - User dashboard
- `/my-posts/trash/<slug>/` - Move to trash
- `/my-posts/restore/<slug>/` - Restore post
- `/my-posts/delete/<slug>/` - Delete permanently

## 🎨 Customization

### Site Name

Update the site name in `mywebsite/settings.py`:

```python
SITE_NAME = "Your Site Name"
```

### Theme Colors

Modify CSS files in your templates to customize the color scheme.

### CKEditor Configuration

Customize the rich text editor in `mywebsite/settings.py` under `CKEDITOR_5_CONFIGS`.

## 🚢 Deployment

### PythonAnywhere Deployment

1. **Upload Code**:
   ```bash
   git clone https://github.com/SunilThapa7/django_blog.git
   ```

2. **Create Virtual Environment**:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 mysite-env
   pip install -r requirements.txt
   ```

3. **Configure Web App**:
   - Set source code directory
   - Set working directory
   - Configure WSGI file
   - Set virtualenv path

4. **Update Settings**:
   - Add domain to `ALLOWED_HOSTS`
   - Add domain to `CSRF_TRUSTED_ORIGINS`
   - Set `DEBUG = False` for production

5. **Static Files**:
   ```bash
   python manage.py collectstatic
   ```

6. **Database**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

7. **Reload Web App**

### Environment Variables

For production, set these environment variables:
- `DJANGO_DEBUG=False`
- `SECRET_KEY=<your-secret-key>`
- Database credentials (if using PostgreSQL/MySQL)

## 🔒 Security

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Use HTTPS in production
- Configure `ALLOWED_HOSTS` properly
- Keep dependencies updated
- Use environment variables for sensitive data

## 📊 Database Models

### Post Model
- `category` - ForeignKey to Category
- `author` - ForeignKey to User
- `title` - Post title
- `slug` - URL-friendly identifier
- `intro` - Short summary
- `body` - Rich text content
- `image` - Featured image
- `tags` - ManyToMany to Tag
- `status` - Active/Draft/Trash
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### Category Model
- `title` - Category name
- `slug` - URL-friendly identifier

### Tag Model
- `name` - Tag name
- `slug` - URL-friendly identifier

### Comment Model
- `post` - ForeignKey to Post
- `name` - Commenter name
- `email` - Commenter email
- `body` - Comment text
- `created_at` - Creation timestamp

### UserProfile Model
- `user` - OneToOne to User
- `role` - User role (Author/Editor/Writer/SEO Expert/Admin)
- `bio` - User biography
- `profile_image` - Profile picture
- `linkedin_url` - LinkedIn profile
- `twitter_url` - Twitter profile
- `website_url` - Personal website

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Sunil Thapa** - [SunilThapa7](https://github.com/SunilThapa7)

## 🙏 Acknowledgments

- Django framework and community
- CKEditor 5 for the rich text editor
- All contributors and users of this project

## 📧 Contact

For questions or support, please open an issue on GitHub or contact the maintainer.

## 🐛 Known Issues

- None currently reported

## 🗺️ Roadmap

- [ ] Add multi-language support
- [ ] Implement email notifications
- [ ] Add social media auto-posting
- [ ] Implement advanced analytics
- [ ] Add bookmark/favorite functionality
- [ ] Implement post series/collections

## 📚 Documentation

For more detailed documentation, please refer to:
- [Django Documentation](https://docs.djangoproject.com/)
- [CKEditor 5 Documentation](https://ckeditor.com/docs/ckeditor5/latest/)

---

