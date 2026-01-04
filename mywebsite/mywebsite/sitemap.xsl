<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:sitemap="http://www.sitemaps.org/schemas/sitemap/0.9" exclude-result-prefixes="sitemap">
    <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/">
        <html lang="en">
            <head>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <title>Sitemap</title>
                <link rel="stylesheet" href="https://unpkg.com/bulma@0.9.4/css/bulma.min.css"/>
                <link href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet" integrity="sha384-wvfXpqpZZVQGK6TAh5PVlGOfQNHSoD2xbE+QkPxCAFlNEevoEH3Sl0sibVcOQVnN" crossorigin="anonymous"/>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Nunito&amp;display=swap');
                    
                    * {
                        font-family: 'Nunito', sans-serif;
                    }
                    
                    body {
                        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                        min-height: 100vh;
                    }
                    
                    .sitemap-header {
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 4rem 1.5rem;
                        text-align: center;
                        margin-bottom: 3rem;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }
                    
                    .sitemap-header h1 {
                        font-size: 2.5rem;
                        margin-bottom: 0.5rem;
                        font-weight: 700;
                    }
                    
                    .sitemap-header p {
                        font-size: 1.1rem;
                        opacity: 0.95;
                        margin-bottom: 1.5rem;
                    }
                    
                    .sitemap-stats {
                        display: flex;
                        justify-content: center;
                        gap: 2rem;
                        flex-wrap: wrap;
                    }
                    
                    .stat-box {
                        background: rgba(255, 255, 255, 0.1);
                        padding: 1rem 1.5rem;
                        border-radius: 8px;
                        backdrop-filter: blur(10px);
                        min-width: 120px;
                    }
                    
                    .stat-box .number {
                        font-size: 2rem;
                        font-weight: 700;
                        display: block;
                    }
                    
                    .stat-box .label {
                        font-size: 0.85rem;
                        opacity: 0.9;
                        margin-top: 0.25rem;
                    }
                    
                    .sitemap-container {
                        max-width: 1000px;
                        margin: 0 auto;
                        padding: 0 1rem 3rem;
                    }
                    
                    .controls-section {
                        background: white;
                        padding: 1.5rem;
                        border-radius: 8px;
                        margin-bottom: 2rem;
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                        display: flex;
                        gap: 1rem;
                        flex-wrap: wrap;
                        align-items: center;
                    }
                    
                    .search-input {
                        flex: 1;
                        min-width: 200px;
                        padding: 0.75rem 1rem;
                        border: 2px solid #e0e0e0;
                        border-radius: 6px;
                        font-size: 1rem;
                        transition: border-color 0.3s;
                    }
                    
                    .search-input:focus {
                        outline: none;
                        border-color: #667eea;
                        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
                    }
                    
                    .filter-buttons {
                        display: flex;
                        gap: 0.5rem;
                    }
                    
                    .filter-btn {
                        padding: 0.6rem 1rem;
                        border: 2px solid #e0e0e0;
                        background: white;
                        border-radius: 6px;
                        cursor: pointer;
                        transition: all 0.3s;
                        font-weight: 500;
                        font-size: 0.9rem;
                    }
                    
                    .filter-btn:hover,
                    .filter-btn.active {
                        border-color: #667eea;
                        background: #667eea;
                        color: white;
                    }
                    
                    .urls-table {
                        background: white;
                        border-radius: 8px;
                        overflow: hidden;
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                    }
                    
                    .url-item {
                        border-bottom: 1px solid #e0e0e0;
                        padding: 1.25rem;
                        transition: all 0.3s ease;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        flex-wrap: wrap;
                        gap: 1rem;
                    }
                    
                    .url-item:last-child {
                        border-bottom: none;
                    }
                    
                    .url-item:hover {
                        background: #f9f9f9;
                        padding-left: 1.5rem;
                    }
                    
                    .url-content {
                        flex: 1;
                        min-width: 250px;
                    }
                    
                    .url-link {
                        color: #667eea;
                        text-decoration: none;
                        font-weight: 600;
                        word-break: break-all;
                        display: flex;
                        align-items: center;
                        gap: 0.5rem;
                        font-size: 1rem;
                    }
                    
                    .url-link:hover {
                        color: #764ba2;
                        text-decoration: underline;
                    }
                    
                    .url-meta {
                        display: flex;
                        gap: 2rem;
                        margin-top: 0.5rem;
                        font-size: 0.85rem;
                        color: #999;
                        flex-wrap: wrap;
                    }
                    
                    .meta-item {
                        display: flex;
                        align-items: center;
                        gap: 0.3rem;
                    }
                    
                    .url-badge {
                        background: #f0f0f0;
                        padding: 0.3rem 0.8rem;
                        border-radius: 20px;
                        font-size: 0.75rem;
                        font-weight: 600;
                        color: #666;
                        white-space: nowrap;
                    }
                    
                    .url-badge.category {
                        background: #e3f2fd;
                        color: #1976d2;
                    }
                    
                    .url-badge.post {
                        background: #f3e5f5;
                        color: #7b1fa2;
                    }
                    
                    .url-open-btn {
                        padding: 0.6rem 1.2rem;
                        background: #667eea;
                        color: white;
                        border: none;
                        border-radius: 6px;
                        cursor: pointer;
                        text-decoration: none;
                        font-weight: 600;
                        transition: all 0.3s;
                        font-size: 0.9rem;
                        white-space: nowrap;
                    }
                    
                    .url-open-btn:hover {
                        background: #764ba2;
                        transform: translateY(-2px);
                        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
                    }
                    
                    .empty-state {
                        text-align: center;
                        padding: 3rem;
                        color: #999;
                    }
                    
                    .empty-state-icon {
                        font-size: 4rem;
                        margin-bottom: 1rem;
                        opacity: 0.3;
                    }
                    
                    .pagination-info {
                        text-align: center;
                        padding: 1.5rem;
                        color: #666;
                        font-size: 0.95rem;
                    }
                    
                    .footer-info {
                        background: white;
                        padding: 2rem;
                        border-radius: 8px;
                        margin-top: 2rem;
                        text-align: center;
                        color: #666;
                        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                    }
                    
                    @media (max-width: 768px) {
                        .sitemap-header {
                            padding: 2rem 1rem;
                        }
                        
                        .sitemap-header h1 {
                            font-size: 1.8rem;
                        }
                        
                        .controls-section {
                            flex-direction: column;
                        }
                        
                        .search-input {
                            width: 100%;
                        }
                        
                        .filter-buttons {
                            width: 100%;
                            justify-content: center;
                        }
                        
                        .url-item {
                            flex-direction: column;
                            align-items: flex-start;
                        }
                        
                        .url-meta {
                            width: 100%;
                        }
                    }
                    
                    .hidden {
                        display: none !important;
                    }
                </style>
            </head>
            <body>
                <div class="sitemap-header">
                    <h1>🗺️ Website Sitemap</h1>
                    <p>Complete directory of all pages and content on our website</p>
                    <div class="sitemap-stats">
                        <div class="stat-box">
                            <span class="number" id="total-count">0</span>
                            <span class="label">Total URLs</span>
                        </div>
                        <div class="stat-box">
                            <span class="number" id="category-count">0</span>
                            <span class="label">Categories</span>
                        </div>
                        <div class="stat-box">
                            <span class="number" id="post-count">0</span>
                            <span class="label">Posts</span>
                        </div>
                    </div>
                </div>
                
                <div class="sitemap-container">
                    <div class="controls-section">
                        <input type="text" class="search-input" id="searchInput" placeholder="🔍 Search URLs..."/>
                        <div class="filter-buttons">
                            <button class="filter-btn active" onclick="filterUrls('all')">All</button>
                            <button class="filter-btn" onclick="filterUrls('category')">Categories</button>
                            <button class="filter-btn" onclick="filterUrls('post')">Posts</button>
                        </div>
                    </div>
                    
                    <div class="urls-table">
                        <xsl:apply-templates select="sitemap:urlset"/>
                    </div>
                    
                    <div class="footer-info">
                        <p>💡 This sitemap helps search engines discover and crawl all the content on our website.</p>
                        <p style="font-size: 0.85rem; margin-top: 1rem;">Last updated: <xsl:value-of select="substring(sitemap:urlset/sitemap:url[1]/sitemap:lastmod, 1, 10)"/></p>
                    </div>
                </div>
                
                <script>
                    function getUrlType(url) {
                        if (url.includes('/category/') || url.includes('category')) {
                            return 'category';
                        } else if (url.includes('/post/') || url.includes('article')) {
                            return 'post';
                        }
                        return 'other';
                    }
                    
                    function updateStats() {
                        const items = document.querySelectorAll('.url-item');
                        const categoryCount = Array.from(items).filter(item => item.dataset.type === 'category').length;
                        const postCount = Array.from(items).filter(item => item.dataset.type === 'post').length;
                        
                        document.getElementById('total-count').textContent = items.length;
                        document.getElementById('category-count').textContent = categoryCount;
                        document.getElementById('post-count').textContent = postCount;
                    }
                    
                    function filterUrls(type) {
                        const items = document.querySelectorAll('.url-item');
                        let visibleCount = 0;
                        
                        items.forEach(item => {
                            if (type === 'all' || item.dataset.type === type) {
                                item.classList.remove('hidden');
                                visibleCount++;
                            } else {
                                item.classList.add('hidden');
                            }
                        });
                        
                        document.querySelectorAll('.filter-btn').forEach(btn => {
                            btn.classList.remove('active');
                        });
                        event.target.classList.add('active');
                        
                        updateEmptyState();
                    }
                    
                    function searchUrls() {
                        const input = document.getElementById('searchInput').value.toLowerCase();
                        const items = document.querySelectorAll('.url-item');
                        let visibleCount = 0;
                        
                        items.forEach(item => {
                            const url = item.querySelector('.url-link').textContent.toLowerCase();
                            if (url.includes(input)) {
                                item.classList.remove('hidden');
                                visibleCount++;
                            } else {
                                item.classList.add('hidden');
                            }
                        });
                        
                        updateEmptyState();
                    }
                    
                    function updateEmptyState() {
                        const visibleItems = document.querySelectorAll('.url-item:not(.hidden)').length;
                        const table = document.querySelector('.urls-table');
                        let emptyState = document.querySelector('.empty-state');
                        
                        if (visibleItems === 0) {
                            if (!emptyState) {
                                emptyState = document.createElement('div');
                                emptyState.className = 'empty-state';
                                emptyState.innerHTML = '&lt;div class="empty-state-icon"&gt;🔍&lt;/div&gt;&lt;h3&gt;No URLs found&lt;/h3&gt;&lt;p&gt;Try adjusting your search or filter criteria.&lt;/p&gt;';
                                table.appendChild(emptyState);
                            }
                        } else if (emptyState) {
                            emptyState.remove();
                        }
                    }
                    
                    document.getElementById('searchInput').addEventListener('keyup', searchUrls);
                    
                    setTimeout(updateStats, 100);
                </script>
            </body>
        </html>
    </xsl:template>
    
    <xsl:template match="sitemap:urlset">
        <xsl:apply-templates select="sitemap:url"/>
    </xsl:template>
    
    <xsl:template match="sitemap:url">
        <xsl:variable name="url" select="sitemap:loc/text()"/>
        <xsl:variable name="type">
            <xsl:choose>
                <xsl:when test="contains($url, '/category/')">category</xsl:when>
                <xsl:when test="contains($url, '/post/')">post</xsl:when>
                <xsl:otherwise>other</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        
        <div class="url-item" data-type="{$type}">
            <div class="url-content">
                <a href="{$url}" class="url-link" target="_blank" rel="noopener noreferrer">
                    <xsl:choose>
                        <xsl:when test="$type = 'category'">
                            <i class="fa fa-folder-open"></i>
                        </xsl:when>
                        <xsl:when test="$type = 'post'">
                            <i class="fa fa-file-text-o"></i>
                        </xsl:when>
                        <xsl:otherwise>
                            <i class="fa fa-link"></i>
                        </xsl:otherwise>
                    </xsl:choose>
                    <xsl:value-of select="$url"/>
                </a>
                <div class="url-meta">
                    <span class="url-badge" style="margin-right: 0.5rem;">
                        <xsl:choose>
                            <xsl:when test="$type = 'category'">
                                <xsl:attribute name="class">url-badge category</xsl:attribute>
                                📂 Category
                            </xsl:when>
                            <xsl:when test="$type = 'post'">
                                <xsl:attribute name="class">url-badge post</xsl:attribute>
                                📰 Post
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="class">url-badge</xsl:attribute>
                                🔗 Page
                            </xsl:otherwise>
                        </xsl:choose>
                    </span>
                    <xsl:if test="sitemap:lastmod">
                        <span class="meta-item">
                            <i class="fa fa-calendar"></i>
                            Updated: <xsl:value-of select="substring(sitemap:lastmod, 1, 10)"/>
                        </span>
                    </xsl:if>
                    <xsl:if test="sitemap:changefreq">
                        <span class="meta-item">
                            <i class="fa fa-sync"></i>
                            <xsl:value-of select="sitemap:changefreq"/>
                        </span>
                    </xsl:if>
                </div>
            </div>
            <a href="{$url}" class="url-open-btn" target="_blank" rel="noopener noreferrer">
                Visit →
            </a>
        </div>
    </xsl:template>
</xsl:stylesheet>
