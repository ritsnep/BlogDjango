<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:sitemap="http://www.sitemaps.org/schemas/sitemap/0.9" exclude-result-prefixes="sitemap">
    <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
    <xsl:template match="/">
        <html lang="en">
            <head>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <title>Sitemap</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 900px;
                        margin: 0 auto;
                        padding: 2rem 1rem;
                        background: #f8f9fa;
                    }
                    .container {
                        background: #fff;
                        padding: 2rem;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    }
                    h1 {
                        font-size: 1.8rem;
                        margin: 0 0 1.5rem 0;
                        color: #2c3e50;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }
                    .count-badge {
                        background: #e0e0e0;
                        color: #555;
                        font-size: 0.8rem;
                        padding: 0.2rem 0.6rem;
                        border-radius: 1rem;
                        font-weight: normal;
                    }
                    
                    /* Tabs */
                    .tabs {
                        display: flex;
                        border-bottom: 2px solid #f0f0f0;
                        margin-bottom: 1.5rem;
                        overflow-x: auto;
                        gap: 1rem;
                    }
                    .tab-btn {
                        padding: 0.8rem 1rem;
                        border: none;
                        background: none;
                        cursor: pointer;
                        font-size: 0.95rem;
                        color: #666;
                        font-weight: 500;
                        position: relative;
                        white-space: nowrap;
                    }
                    .tab-btn:hover {
                        color: #333;
                    }
                    .tab-btn.active {
                        color: #1565c0;
                        font-weight: 600;
                    }
                    .tab-btn.active::after {
                        content: '';
                        position: absolute;
                        bottom: -2px;
                        left: 0;
                        width: 100%;
                        height: 2px;
                        background: #1565c0;
                    }

                    /* List */
                    ul {
                        list-style: none;
                        padding: 0;
                        margin: 0;
                    }
                    li {
                        padding: 0.8rem 0;
                        border-bottom: 1px solid #f0f0f0;
                        display: flex;
                        align-items: center;
                        gap: 1rem;
                        flex-wrap: wrap;
                        transition: opacity 0.3s ease;
                    }
                    li[style*="display: none"] {
                        opacity: 0;
                    }
                    li:hover {
                        background: #f9f9f9;
                        padding-left: 0.5rem;
                        transition: padding 0.2s;
                    }
                    
                    a {
                        text-decoration: none;
                        color: #2c3e50;
                        font-weight: 500;
                        word-break: break-all;
                        flex: 1;
                    }
                    a:hover {
                        color: #3498db;
                    }
                    .meta {
                        font-size: 0.8rem;
                        color: #999;
                        white-space: nowrap;
                        min-width: 80px;
                        text-align: right;
                    }
                    
                    /* Badges */
                    .badge {
                        display: inline-block;
                        padding: 0.2rem 0.6rem;
                        border-radius: 4px;
                        font-size: 0.7rem;
                        font-weight: 700;
                        text-transform: uppercase;
                        min-width: 65px;
                        text-align: center;
                    }
                    .badge.post { background: #e3f2fd; color: #1565c0; }
                    .badge.category { background: #fff3e0; color: #e65100; }
                    .badge.user { background: #f3e5f5; color: #7b1fa2; }
                    .badge.page { background: #e8f5e9; color: #2e7d32; }

                    /* Filtered State: Hide badges when a specific tab is active */
                    ul.filtered .badge {
                        display: none;
                    }

                    @media (max-width: 600px) {
                        .meta {
                            text-align: left;
                            width: 100%;
                            margin-top: 0.2rem;
                        }
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Sitemap <span class="count-badge"><xsl:value-of select="count(sitemap:urlset/sitemap:url)"/> URLs</span></h1>
                    
                    <div class="tabs">
                        <button class="tab-btn active" onclick="filterItems('all', this)">All</button>
                        <button class="tab-btn" onclick="filterItems('post', this)">Posts (<xsl:value-of select="count(sitemap:urlset/sitemap:url[sitemap:priority='0.9'])"/>)</button>
                        <button class="tab-btn" onclick="filterItems('category', this)">Categories (<xsl:value-of select="count(sitemap:urlset/sitemap:url[sitemap:priority='0.8'])"/>)</button>
                        <button class="tab-btn" onclick="filterItems('part', this)">Pages (<xsl:value-of select="count(sitemap:urlset/sitemap:url[sitemap:priority='0.6'])"/>)</button>
                        <button class="tab-btn" onclick="filterItems('user', this)">Authors (<xsl:value-of select="count(sitemap:urlset/sitemap:url[sitemap:priority='0.5'])"/>)</button>
                    </div>
                    
                    <ul id="sitemap-list">
                        <xsl:apply-templates select="sitemap:urlset/sitemap:url">
                            <xsl:sort select="sitemap:priority" order="descending"/>
                            <xsl:sort select="sitemap:lastmod" order="descending"/>
                        </xsl:apply-templates>
                    </ul>
                    
                    <footer style="margin-top: 3rem; font-size: 0.8rem; color: #999; text-align: center; border-top: 1px solid #eee; padding-top: 1rem;">
                        Generated by Django Sitemap
                    </footer>
                </div>

                <script>
                    function filterItems(type, btn) {
                        // Update active tab
                        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                        btn.classList.add('active');

                        const list = document.getElementById('sitemap-list');
                        
                        // Toggle 'filtered' class for CSS logic
                        if (type === 'all') {
                            list.classList.remove('filtered');
                        } else {
                            list.classList.add('filtered');
                        }

                        // Filter items
                        const items = list.querySelectorAll('li');
                        items.forEach(item => {
                            if (type === 'all' || item.dataset.type === type) {
                                item.style.display = 'flex';
                            } else {
                                item.style.display = 'none';
                            }
                        });
                    }
                </script>
            </body>
        </html>
    </xsl:template>
    
    <xsl:template match="sitemap:url">
        <xsl:variable name="url" select="sitemap:loc"/>
        <xsl:variable name="prio" select="sitemap:priority"/>
        
        <xsl:variable name="badgeType">
             <xsl:choose>
                 <xsl:when test="$prio = '0.9'">post</xsl:when>
                 <xsl:when test="$prio = '0.8'">category</xsl:when>
                 <xsl:when test="$prio = '0.6'">part</xsl:when>
                 <xsl:when test="$prio = '0.5'">user</xsl:when>
                 <xsl:otherwise>part</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        
        <xsl:variable name="displayText">
             <xsl:choose>
                 <xsl:when test="$prio = '0.9'">Post</xsl:when>
                 <xsl:when test="$prio = '0.8'">Category</xsl:when>
                 <xsl:when test="$prio = '0.6'">Page</xsl:when>
                 <xsl:when test="$prio = '0.5'">Author</xsl:when>
                 <xsl:otherwise>Page</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>

        <li data-type="{$badgeType}">
            <span class="badge {$badgeType}"><xsl:value-of select="$displayText"/></span>
            <a href="{$url}" target="_blank">
                <xsl:value-of select="$url"/>
            </a>
            <div class="meta">
                <xsl:if test="sitemap:lastmod">
                    <span><xsl:value-of select="substring(sitemap:lastmod, 1, 10)"/></span>
                </xsl:if>
                 <xsl:if test="not(sitemap:lastmod)">
                    <span>-</span>
                </xsl:if>
            </div>
        </li>
    </xsl:template>
</xsl:stylesheet>
