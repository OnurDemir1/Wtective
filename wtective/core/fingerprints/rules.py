import re

R = re.compile
I = re.I

RULES = {

    # CMS
    'CMS': {
        'WordPress': {
            'headers': {'Link': R(r'api\.w\.org', I)},
            'cookies': [R(r'^wp-', I), R(r'^wordpress_')],
            'meta_generators': [R(r'WordPress', I)],
            'script_paths': [R(r'/wp-includes/', I), R(r'/wp-content/', I)],
            'html_comments': [R(r'Starter Template|flavor starter')],
            'url_paths': [R(r'/wp-json/', I)]
        },
        'Joomla': {
            'meta_generators': [R(r'Joomla', I)],
            'headers': {'X-Content-Encoded-By': R(r'Joomla', I)},
            'cookies': [R(r'^joomla_', I)],
            'script_paths': [R(r'/media/jui/', I)]
        },
        'Drupal': {
            'headers': {'X-Generator': R(r'Drupal', I), 'X-Drupal-Cache': R(r'.*')},
            'script_paths': [R(r'/sites/default/files/', I), R(r'/core/misc/drupal\.js', I)],
            'js_globals': ['Drupal']
        },
        'Ghost': {
            'meta_generators': [R(r'Ghost', I)],
            'headers': {'X-Ghost-Cache-Status': R(r'.*')}
        },
        'Squarespace': {
            'html_attrs': [R(r'data-squarespace-cacheversion')],
            'script_paths': [R(r'squarespace\.com', I)]
        },
        'Wix': {
            'meta_generators': [R(r'Wix\.com', I)],
            'script_paths': [R(r'static\.wixstatic\.com', I), R(r'parastorage\.com', I)],
            'headers': {'X-Wix-Request-Id': R(r'.*')}
        },
        'Webflow': {
            'meta_generators': [R(r'Webflow', I)],
            'script_paths': [R(r'assets\.website-files\.com', I), R(r'webflow\.js', I)],
            'html_attrs': [R(r'data-wf-site'), R(r'data-wf-page')]
        },
        'Typo3': {
            'meta_generators': [R(r'TYPO3', I)],
            'script_paths': [R(r'typo3temp/', I), R(r'typo3conf/', I)]
        },
        'Hugo': {
            'meta_generators': [R(r'Hugo', I)]
        },
        'Jekyll': {
            'meta_generators': [R(r'Jekyll', I)]
        },
        'Gatsby': {
            'js_globals': ['___gatsby'],
            'html_attrs': [R(r'id="___gatsby"')],
            'script_paths': [R(r'/page-data/', I)]
        },
        'Hexo': {
            'meta_generators': [R(r'Hexo', I)]
        },
        'Blogger': {
            'meta_generators': [R(r'blogger', I)],
            'script_paths': [R(r'blogger\.com', I), R(r'blogspot\.com', I)]
        },
        'Medium': {
            'script_paths': [R(r'medium\.com/_/', I)],
            'html_attrs': [R(r'data-is-published')]
        },
        'Contentful': {
            'js_globals': ['contentfulManagement'],
            'script_paths': [R(r'contentful\.com', I)]
        },
        'Strapi': {
            'headers': {'X-Powered-By': R(r'Strapi', I)}
        },
        'Craft CMS': {
            'meta_generators': [R(r'Craft CMS', I)],
            'headers': {'X-Powered-By': R(r'Craft CMS', I)}
        },
        'Prismic': {
            'script_paths': [R(r'prismic\.io', I)]
        },
        'Sanity': {
            'script_paths': [R(r'sanity\.io', I), R(r'cdn\.sanity\.io', I)]
        },
        'DatoCMS': {
            'script_paths': [R(r'datocms', I)]
        },
        'OpenCart': {
            'script_paths': [R(r'catalog/view/javascript/jquery/jquery', I), R(r'catalog/view/theme', I)],
            'url_paths': [R(r'route=product/', I), R(r'route=checkout/cart', I)]
        },
        'Simple Machines Forum': {
            'meta_generators': [R(r'Simple Machines Forum|SMF', I)],
            'script_paths': [R(r'/Themes/[^"\']+/scripts/', I), R(r'/Sources/', I), R(r'smf(?:_|\.)script', I)],
            'html_attrs': [R(r'index\.php\?action=', I), R(r'\bSMF\s+\d+\.\d+', I), R(r'Powered by SMF|Simple Machines', I)],
            'cookies': [R(r'^SMFCookie', I)]
        },
        'Concrete5': {
            'meta_generators': [R(r'concrete5', I)]
        },
        'SilverStripe': {
            'meta_generators': [R(r'SilverStripe', I)]
        },
        'Umbraco': {
            'headers': {'X-Umbraco-Version': R(r'.*')},
            'url_paths': [R(r'/umbraco/', I)]
        },
        'Kentico': {
            'meta_generators': [R(r'Kentico', I)]
        },
        'Sitecore': {
            'cookies': [R(r'SC_ANALYTICS_GLOBAL_COOKIE', I)],
            'html_attrs': [R(r'sc-part-of')]
        },
        'Adobe Experience Manager': {
            'url_paths': [R(r'/content/dam/', I), R(r'/etc\.clientlibs/', I)],
            'script_paths': [R(r'clientlib.*\.js', I)]
        },
        'HubSpot CMS': {
            'url_paths': [R(r'/hs-sites\.com/', I), R(r'/_hcms/', I)],
        },
        'Directus': {
            'headers': {'X-Powered-By': R(r'Directus', I)}
        },
        'Payload CMS': {
            'headers': {'X-Powered-By': R(r'Payload', I)},
            'url_paths': [R(r'/admin/collections/', I)]
        },
        'KeystoneJS': {
            'headers': {'X-Powered-By': R(r'KeystoneJS', I)}
        },
        'Cockpit CMS': {
            'script_paths': [R(r'cockpit', I)],
            'url_paths': [R(r'/cockpit/', I)]
        },
        'Storyblok': {
            'script_paths': [R(r'storyblok', I)]
        },
        'ButterCMS': {
            'script_paths': [R(r'buttercms', I)]
        },
        'Netlify CMS': {
            'script_paths': [R(r'netlify-cms', I), R(r'decap-cms', I)]
        },
        'VitePress': {
            'script_paths': [R(r'vitepress', I)],
            'html_attrs': [R(r'id="VPContent"')]
        },
        'Docusaurus': {
            'meta_generators': [R(r'Docusaurus', I)],
            'script_paths': [R(r'docusaurus', I)]
        },
        'MkDocs': {
            'meta_generators': [R(r'mkdocs', I)],
            'script_paths': [R(r'mkdocs', I)]
        },
        'Pelican': {
            'meta_generators': [R(r'Pelican', I)]
        },
        'Grav': {
            'meta_generators': [R(r'GravCMS', I)]
        },
        'Kirby': {
            'meta_generators': [R(r'Kirby', I)]
        },
        'Statamic': {
            'meta_generators': [R(r'Statamic', I)]
        },
        'Framer': {
            'meta_generators': [R(r'Framer', I)],
            'html_attrs': [R(r'data-framer-'), R(r'framer-search-index')],
            'script_paths': [R(r'framerusercontent\.com', I), R(r'framer\.com/m/', I)]
        },
        'Eleventy': {
            'meta_generators': [R(r'Eleventy', I)]
        },
        'Middleman': {
            'meta_generators': [R(r'Middleman', I)]
        },
        'Gridsome': {
            'js_globals': ['__GRIDSOME__'],
            'script_paths': [R(r'gridsome', I)]
        },
        'Bridgetown': {
            'meta_generators': [R(r'Bridgetown', I)]
        },
        'Neos CMS': {
            'meta_generators': [R(r'Neos', I)]
        },
        'ProcessWire': {
            'meta_generators': [R(r'ProcessWire', I)]
        },
        'Textpattern': {
            'meta_generators': [R(r'Textpattern', I)]
        },
        'ExpressionEngine': {
            'meta_generators': [R(r'ExpressionEngine', I)]
        },
        'Movable Type': {
            'meta_generators': [R(r'Movable Type', I)]
        },
        'b2evolution': {
            'meta_generators': [R(r'b2evolution', I)]
        },
        'MODX': {
            'headers': {'X-Powered-By': R(r'MODX', I)}
        },
        'Contao': {
            'meta_generators': [R(r'Contao', I)]
        },
        'Backdrop CMS': {
            'meta_generators': [R(r'Backdrop CMS', I)]
        },
        'Fork CMS': {
            'meta_generators': [R(r'Fork CMS', I)]
        },
        'Pimcore': {
            'headers': {'X-Powered-By': R(r'pimcore', I)}
        },
        'eZ Platform': {
            'headers': {'X-Powered-By': R(r'eZ', I)}
        },
        'Agility CMS': {
            'script_paths': [R(r'agilitycms', I)]
        },
        'Kontent.ai': {
            'script_paths': [R(r'kontent\.ai', I)]
        },
        'Magnolia': {
            'headers': {'X-Magnolia-Registration': R(r'.*')}
        },
        'Liferay': {
            'headers': {'Liferay-Portal': R(r'.*')},
            'script_paths': [R(r'liferay', I)]
        },
        'DNN': {
            'cookies': [R(r'\.DOTNETNUKE')],
            'html_attrs': [R(r'DnnModule')]
        },
        'Sitefinity': {
            'meta_generators': [R(r'Sitefinity', I)]
        },
        'Orchard CMS': {
            'meta_generators': [R(r'Orchard', I)]
        },
        'Episerver': {
            'headers': {'X-EPiServer-PageId': R(r'.*')}
        },
        'Optimizely CMS': {
            'headers': {'X-EPiServer-PageId': R(r'.*')},
            'script_paths': [R(r'episerver', I)]
        },
    },

    # E-commerce
    'E-commerce': {
        'Shopify': {
            'js_globals': ['Shopify'],
            'script_paths': [R(r'cdn\.shopify\.com', I), R(r'shopifycdn\.net', I), R(r'myshopify\.com', I)],
            'headers': {'X-ShopId': R(r'.*')},
            'cookies': [R(r'^_shopify', I), R(r'^cart_sig$'), R(r'^secure_customer_sig$')]
        },
        'Magento': {
            'cookies': [R(r'mage-cache', I), R(r'^form_key$', I), R(r'^private_content_version$', I)],
            'script_paths': [R(r'/static/version[a-f0-9]+/frontend/', I), R(r'mage/cookies', I), R(r'/skin/frontend/', I), R(r'/static/frontend/[A-Z]\w+/\w+/', I)],
            'js_globals': ['mage']
        },
        'WooCommerce': {
            'cookies': [R(r'woocommerce_', I), R(r'wp_woocommerce_session_', I)],
            'script_paths': [R(r'/plugins/woocommerce/', I), R(r'wc-cart-fragments', I), R(r'woocommerce', I)],
            'html_attrs': [R(r'wc-ajax=', I), R(r'woocommerce-cart', I), R(r'woocommerce-checkout', I)]
        },
        'BigCommerce': {
            'headers': {'X-BC-Store-Version': R(r'.*')},
            'script_paths': [R(r'bigcommerce\.com', I)]
        },
        'Salesforce Commerce Cloud': {
            'script_paths': [R(r'demandware\.static', I)],
            'url_paths': [R(r'/on/demandware', I)]
        },
        'Volusion': {
            'script_paths': [R(r'volusion\.com', I)]
        },
        'Ecwid': {
            'script_paths': [R(r'app\.ecwid\.com', I)],
            'js_globals': ['Ecwid']
        },
        'PrestaShop': {
            'meta_generators': [R(r'PrestaShop', I)],
            'script_paths': [R(r'/modules/(?:ps_|prestashop)', I)],
            'cookies': [R(r'PrestaShop-', I)]
        },
        'Squarespace Commerce': {
            'html_attrs': [R(r'data-squarespace-cacheversion')]
        },
        'Wix eCommerce': {
            'script_paths': [R(r'ecom\.wix\.com', I)]
        },
        'Tilda': {
            'script_paths': [R(r'tildacdn\.com', I)],
            'meta_generators': [R(r'Tilda', I)]
        },
        'Swell': {
            'script_paths': [R(r'swell\.is', I)]
        },
        'Medusa': {
            'headers': {'X-Powered-By': R(r'Medusa', I)}
        },
        'Saleor': {
            'script_paths': [R(r'saleor', I)]
        },
        'Spree Commerce': {
            'cookies': [R(r'^spree_', I)]
        },
        'nopCommerce': {
            'meta_generators': [R(r'nopCommerce', I)]
        },
        'Zen Cart': {
            'script_paths': [R(r'zen-cart', I)]
        },
        'osCommerce': {
            'url_paths': [R(r'product_info\.php', I)]
        },
        'CS-Cart': {
            'script_paths': [R(r'cs-cart', I)]
        },
        'X-Cart': {
            'script_paths': [R(r'xcart', I)]
        },
        'Gambio': {
            'meta_generators': [R(r'Gambio', I)]
        },
        'Oxid eShop': {
            'cookies': [R(r'^oxideshop', I)]
        },
        'Shopware': {
            'headers': {'sw-context-token': R(r'.*')},
            'script_paths': [R(r'shopware', I)]
        },
        'Sylius': {
            'cookies': [R(r'^sylius', I)]
        },
        'Reaction Commerce': {
            'script_paths': [R(r'reaction\.', I)]
        },
        'Snipcart': {
            'script_paths': [R(r'cdn\.snipcart\.com', I)],
            'js_globals': ['Snipcart']
        },
        'Paddle': {
            'script_paths': [R(r'cdn\.paddle\.com', I)]
        },
        'Gumroad': {
            'script_paths': [R(r'gumroad\.com', I)]
        },
        'Lemon Squeezy': {
            'script_paths': [R(r'lemonsqueezy\.com', I)]
        },
        'Commerce.js': {
            'script_paths': [R(r'commercejs', I)]
        },
        '3dcart': {
            'script_paths': [R(r'3dcart', I)]
        },
        'Wix Stores': {
            'script_paths': [R(r'wixstores', I)]
        },
    },

    # Databases (only match actual error signatures, not mentions)
    'Database': {
        'MySQL': {
            'html_attrs': [R(r'SQLSTATE\[HY000\]', I), R(r'MySQL server version for the right syntax', I), R(r'you have an error in your sql syntax', I)]
        },
        'MariaDB': {
            'html_attrs': [R(r'MariaDB server version', I)]
        },
        'PostgreSQL': {
            'html_attrs': [R(r'pg_query\(', I), R(r'pg_connect\(', I), R(r'unterminated quoted string at or near', I)]
        },
        'MongoDB': {
            'html_attrs': [R(r'MongoError', I), R(r'MongooseError', I)]
        },
        'Redis': {
            'html_attrs': [R(r'RedisException', I)]
        },
        'SQLite': {
            'html_attrs': [R(r'sqlite3?\.OperationalError', I), R(r'unable to open database file', I)]
        },
    },

    # Analytics & Marketing
    'Analytics': {
        'Google Analytics': {
            'js_globals': ['ga', 'gtag'],
            'script_paths': [R(r'google-analytics\.com', I), R(r'googletagmanager\.com/gtag', I)]
        },
        'Google Tag Manager': {
            'js_globals': ['dataLayer', 'google_tag_manager'],
            'script_paths': [R(r'googletagmanager\.com/gtm\.js', I)]
        },
        'Facebook Pixel': {
            'js_globals': ['fbq'],
            'script_paths': [R(r'connect\.facebook\.net.*fbevents', I)]
        },
        'Hotjar': {
            'js_globals': ['hj'],
            'script_paths': [R(r'static\.hotjar\.com', I)]
        },
        'Mixpanel': {
            'js_globals': ['mixpanel'],
            'script_paths': [R(r'cdn\.mxpnl\.com', I)]
        },
        'Segment': {
            'js_globals': ['analytics'],
            'script_paths': [R(r'cdn\.segment\.com', I)]
        },
        'Amplitude': {
            'js_globals': ['amplitude'],
            'script_paths': [R(r'cdn\.amplitude\.com', I)]
        },
        'Heap': {
            'js_globals': ['heap'],
            'script_paths': [R(r'cdn\.heapanalytics\.com', I)]
        },
        'Matomo': {
            'js_globals': ['_paq'],
            'script_paths': [R(r'matomo\.js', I), R(r'piwik\.js', I)]
        },
        'Plausible': {
            'script_paths': [R(r'plausible\.io', I)]
        },
        'Fathom': {
            'script_paths': [R(r'usefathom\.com', I), R(r'cdn\.usefathom\.com', I)]
        },
        'Clarity': {
            'script_paths': [R(r'clarity\.ms', I)]
        },
        'FullStory': {
            'js_globals': ['FS'],
            'script_paths': [R(r'fullstory\.com', I)]
        },
        'Lucky Orange': {
            'script_paths': [R(r'luckyorange\.com', I)]
        },
        'Crazy Egg': {
            'script_paths': [R(r'script\.crazyegg\.com', I)]
        },
        'VWO': {
            'script_paths': [R(r'dev\.visualwebsiteoptimizer\.com', I)]
        },
        'TikTok Pixel': {
            'script_paths': [R(r'analytics\.tiktok\.com', I)],
            'js_globals': ['ttq']
        },
        'LinkedIn Insight': {
            'script_paths': [R(r'snap\.licdn\.com', I)]
        },
        'Twitter Pixel': {
            'script_paths': [R(r'static\.ads-twitter\.com', I)],
            'js_globals': ['twq']
        },
        'Pinterest Tag': {
            'script_paths': [R(r'pintrk', I), R(r's\.pinimg\.com', I)],
            'js_globals': ['pintrk']
        },
        'Yandex Metrica': {
            'script_paths': [R(r'mc\.yandex\.ru', I)],
            'js_globals': ['ym']
        },
    },

    # Web Framework
    'Web Framework': {
        'React': {
            'js_globals': ['__REACT_DEVTOOLS_GLOBAL_HOOK__'],
            'html_attrs': [R(r'data-reactroot'), R(r'data-reactid')],
            'script_paths': [R(r'react-dom(?:\.production\.min)?\.js', I), R(r'[/@]react-dom@[\d.]+', I)]
        },
        'Next.js': {
            'js_globals': ['__NEXT_DATA__'],
            'script_paths': [R(r'/_next/static/', I)],
            'html_attrs': [R(r'id="__next"')]
        },
        'Vue.js': {
            'js_globals': ['__VUE__', '__vue__'],
            'html_attrs': [R(r'data-v-[a-f0-9]')],
            'storage_keys': ['vuex']
        },
        'Nuxt.js': {
            'js_globals': ['__NUXT__', '$nuxt'],
            'script_paths': [R(r'/_nuxt/', I)],
            'html_attrs': [R(r'id="__nuxt"')]
        },
        'Angular': {
            'html_attrs': [R(r'ng-version="'), R(r'_ngcontent-'), R(r'_nghost-')],
        },
        'AngularJS': {
            'html_attrs': [R(r'ng-controller'), R(r'ng-model')],
            'script_paths': [R(r'angular[\./@ -]1\.', I)]
        },
        'Svelte': {
            'css_classes': [R(r'\bsvelte-[a-z0-9]{5,}\b')],
            'script_paths': [R(r'svelte', I)]
        },
        'SvelteKit': {
            'script_paths': [R(r'/_app/immutable/', I)],
            'html_attrs': [R(r'data-sveltekit')]
        },
        'Remix': {
            'js_globals': ['__remixContext', '__remixRouteModules', '__remixManifest'],
            'html_attrs': [R(r'data-remix-run'), R(r'data-rmx-theme'), R(r'data-rmx-')],
            'script_paths': [R(r'/@remix-run/', I), R(r'/build/entry\.client-[a-zA-Z0-9]+\.js', I), R(r'/build/root-[a-zA-Z0-9]+\.js', I), R(r'/@remix-run/react', I)]
        },
        'Astro': {
            'html_attrs': [R(r'astro-island'), R(r'client:load'), R(r'client:idle'), R(r'client:visible')],
            'script_paths': [R(r'/_astro/', I)]
        },
        'Ember.js': {
            'js_globals': ['Ember', 'Em'],
            'html_attrs': [R(r'data-ember-action'), R(r'id="ember\d+"')],
            'css_classes': [R(r'\bember-view\b'), R(r'\bember-application\b')]
        },
        'Backbone.js': {
            'js_globals': ['Backbone']
        },
        'Alpine.js': {
            'html_attrs': [R(r'(?<![/\w-])x-data[\s="\'>/]'), R(r'(?<![/\w-])x-bind[=:@\s"\'>/]'), R(r'(?<![/\w-])x-on:[a-z]')]
        },
        'HTMX': {
            'html_attrs': [R(r'(?<!\w)hx-get[\s="\'>/]'), R(r'(?<!\w)hx-post[\s="\'>/]'), R(r'(?<!\w)hx-trigger[\s="\'>/]')],
            'script_paths': [R(r'htmx(\.min)?\.js', I)]
        },
        'Solid.js': {
            'js_globals': ['_$HY']
        },
        'Qwik': {
            'html_attrs': [R(r'q:container')],
            'script_paths': [R(r'qwikloader', I)]
        },
        'Preact': {
            'js_globals': ['__PREACT_DEVTOOLS__']
        },
        'Stimulus': {
            'html_attrs': [R(r'\bdata-controller="'), R(r'\bdata-stimulus')],
            'script_paths': [R(r'stimulus(\.min)?\.js', I), R(r'@hotwired/stimulus', I)]
        },
        'Turbo': {
            'html_attrs': [R(r'data-turbo')],
            'meta_generators': [R(r'turbo', I)]
        },
        'Laravel': {
            'cookies': [R(r'laravel_session', I)],
        },
        'Django': {
            'cookies': [R(r'^csrftoken$')],
            'html_attrs': [R(r'name="csrfmiddlewaretoken"')]
        },
        'Express': {
            'headers': {'X-Powered-By': R(r'^Express$', I)}
        },
        'Rails': {
            'headers': {'X-Powered-By': R(r'Phusion Passenger', I)},
            'meta_generators': [R(r'Ruby on Rails', I)]
        },
        'Spring': {
            'headers': {'X-Application-Context': R(r'.*')}
        },
        'Flask': {
            'headers': {'Server': R(r'Werkzeug', I)}
        },
        'FastAPI': {
            'headers': {'Server': R(r'uvicorn', I)}
        },
        'Blazor': {
            'script_paths': [R(r'_framework/blazor', I)],
            'js_globals': ['Blazor']
        },
        'Lit': {
            'js_globals': ['litElementVersions']
        },
        'Stencil': {
            'html_attrs': [R(r'data-stencil')],
            'script_paths': [R(r'stencil', I)]
        },
    },

    # JS Libraries
    'JS Library': {
        'jQuery': {
            'js_globals': ['jQuery'],
            'script_paths': [R(r'jquery[\.-]', I)]
        },
        'Lodash': {
            'script_paths': [R(r'lodash(\.min)?\.js', I)]
        },
        'core-js': {
            'script_paths': [R(r'core-js(?:@|/|-|\.)', I), R(r'/core-js/', I)]
        },
        'Axios': {
            'js_globals': ['axios']
        },
        'D3.js': {
            'script_paths': [R(r'/d3@\d', I), R(r'/d3\.v\d', I), R(r'cdn.*[/.]d3(\.min)?\.js', I)]
        },
        'Three.js': {
            'js_globals': ['THREE'],
            'script_paths': [R(r'three(\.min)?\.js', I)]
        },
        'GSAP': {
            'js_globals': ['gsap'],
            'script_paths': [R(r'gsap(\.min)?\.js', I)]
        },
        'Anime.js': {
            'js_globals': ['anime'],
            'script_paths': [R(r'anime(\.min)?\.js', I)]
        },
        'Chart.js': {
            'js_globals': ['Chart'],
            'script_paths': [R(r'chart(\.min)?\.js', I)]
        },
        'Socket.IO': {
            'js_globals': ['io'],
            'script_paths': [R(r'socket\.io(\.min)?\.js', I)]
        },
        'Leaflet': {
            'script_paths': [R(r'leaflet(\.min)?\.js', I)]
        },
        'Mapbox GL': {
            'js_globals': ['mapboxgl'],
            'script_paths': [R(r'mapbox-gl', I)]
        },
        'Swiper': {
            'js_globals': ['Swiper'],
            'script_paths': [R(r'swiper(\.min)?\.js', I)]
        },
        'Lottie': {
            'js_globals': ['lottie'],
            'script_paths': [R(r'lottie(\.min)?\.js', I)]
        },
        'Hammer.js': {
            'js_globals': ['Hammer'],
            'script_paths': [R(r'hammer(\.min)?\.js', I)]
        },
        'Highcharts': {
            'js_globals': ['Highcharts'],
            'script_paths': [R(r'highcharts(\.min)?\.js', I)]
        },
        'ApexCharts': {
            'js_globals': ['ApexCharts'],
            'script_paths': [R(r'apexcharts(\.min)?\.js', I)]
        },
        'Popper.js': {
            'js_globals': ['Popper'],
            'script_paths': [R(r'popper(\.min)?\.js', I)]
        },
        'Marked': {
            'js_globals': ['marked']
        },
        'Prism': {
            'js_globals': ['Prism'],
            'script_paths': [R(r'prism(\.min)?\.js', I)]
        },
        'Highlight.js': {
            'js_globals': ['hljs'],
            'script_paths': [R(r'highlight\.js[/@]', I), R(r'cdn.*hljs', I)]
        },
        'Tippy.js': {
            'js_globals': ['tippy'],
            'script_paths': [R(r'tippy(\.min)?\.js', I)]
        },
        'AOS': {
            'html_attrs': [R(r'data-aos')],
            'script_paths': [R(r'aos(\.min)?\.js', I)]
        },
        'ScrollReveal': {
            'js_globals': ['ScrollReveal']
        },
        'Intersection Observer Polyfill': {
            'script_paths': [R(r'intersection-observer', I)]
        },
        'PDF.js': {
            'js_globals': ['pdfjsLib'],
            'script_paths': [R(r'pdf(\.min)?\.js', I)]
        },
        'Video.js': {
            'js_globals': ['videojs'],
            'script_paths': [R(r'video\.js[/@]', I), R(r'vjs\.zencdn\.net', I), R(r'videojs[/@-]', I), R(r'/videojs/', I)]
        },
        'Plyr': {
            'js_globals': ['Plyr'],
            'script_paths': [R(r'plyr(\.min)?\.js', I)]
        },
        'Slick': {
            'script_paths': [R(r'slick(\.min)?\.js', I)],
            'css_classes': [R(r'\bslick-slide\b')]
        },
        'Owl Carousel': {
            'script_paths': [R(r'owl\.carousel', I)],
            'css_classes': [R(r'\bowl-carousel\b')]
        },
        'Flickity': {
            'js_globals': ['Flickity'],
            'css_classes': [R(r'\bflickity-slider\b')]
        },
        'Masonry': {
            'js_globals': ['Masonry']
        },
        'Isotope': {
            'js_globals': ['Isotope']
        },
        'Lazysizes': {
            'script_paths': [R(r'lazysizes(\.min)?\.js', I)],
            'css_classes': [R(r'\blazyload\b')]
        },
        'Fancybox': {
            'js_globals': ['Fancybox'],
            'script_paths': [R(r'fancybox', I)]
        },
        'PhotoSwipe': {
            'js_globals': ['PhotoSwipe']
        },
        'SweetAlert': {
            'js_globals': ['Swal', 'swal'],
            'script_paths': [R(r'sweetalert', I)]
        },
        'Toastr': {
            'js_globals': ['toastr'],
            'script_paths': [R(r'toastr(\.min)?\.js', I)]
        },
        'Turnstile': {
            'script_paths': [R(r'challenges\.cloudflare\.com/turnstile', I)]
        },
        'reCAPTCHA': {
            'script_paths': [R(r'google\.com/recaptcha', I)],
            'js_globals': ['grecaptcha']
        },
        'hCaptcha': {
            'script_paths': [R(r'hcaptcha\.com', I)],
            'js_globals': ['hcaptcha']
        },
    },

    # UI Framework
    'UI Framework': {
        'Tailwind CSS': {
            'css_classes': [R(r'\b(hover|focus|active|group-hover|dark|sm|md|lg|xl|2xl):[a-z].*\b(hover|focus|active|group-hover|dark|sm|md|lg|xl|2xl):[a-z].*\b(hover|focus|active|group-hover|dark|sm|md|lg|xl|2xl):[a-z]')],
            'script_paths': [R(r'tailwindcss', I), R(r'tailwind\.min\.css', I), R(r'tailwind\.css', I)]
        },
        'Bootstrap': {
            'css_classes': [R(r'\b(col-md-|col-lg-|col-sm-|container-fluid|navbar-brand)\b', I)],
            'script_paths': [R(r'(?<![\w.-])bootstrap(\.bundle)?(\.min)?\.js', I)]
        },
        'Bulma': {
            'css_classes': [R(r'\b(is-primary|is-link|is-info|is-success|is-warning|is-danger)\b')],
            'script_paths': [R(r'bulma(\.min)?\.css', I)]
        },
        'Foundation': {
            'css_classes': [R(r'\b(large-\d+\.columns|medium-\d+\.columns|small-\d+\.columns)\b')],
            'script_paths': [R(r'foundation(\.min)?\.js', I)],
            'html_attrs': [R(r'data-equalizer'), R(r'data-abide')]
        },
        'Materialize': {
            'css_classes': [R(r'\b(materialize|waves-effect|waves-light)\b', I)],
            'script_paths': [R(r'materialize(\.min)?\.js', I)]
        },
        'Semantic UI': {
            'css_classes': [R(r'\b(ui segment|ui container|ui grid)\b', I)],
            'script_paths': [R(r'semantic(\.min)?\.js', I)]
        },
        'Ant Design': {
            'css_classes': [R(r'\bant-', I)]
        },
        'Material UI': {
            'css_classes': [R(r'\bMui[A-Z]')],
            'html_attrs': [R(r'class="Mui')]
        },
        'Chakra UI': {
            'css_classes': [R(r'\bchakra-')]
        },
        'Radix UI': {
            'html_attrs': [R(r'data-radix')]
        },
        'shadcn/ui': {
            'html_attrs': [R(r'data-slot="(dialog|sheet|popover|tooltip|dropdown)')]
        },
        'DaisyUI': {
            'css_classes': [R(r'\b(?:data-theme|daisy-ui|daisyui)\b', I)],
            'script_paths': [R(r'daisyui', I)]
        },
        'Vuetify': {
            'css_classes': [R(r'\bv-application\b'), R(r'\bv-card\b')]
        },
        'Element UI': {
            'css_classes': [R(r'\bel-')]
        },
        'PrimeVue': {
            'css_classes': [R(r'\bp-component\b')]
        },
        'Quasar': {
            'css_classes': [R(r'\bq-page\b'), R(r'\bq-layout\b')]
        },
        'UIKit': {
            'css_classes': [R(r'\buk-')],
            'script_paths': [R(r'uikit(\.min)?\.js', I)]
        },
        'Elementor': {
            'css_classes': [R(r'\belementor-')],
            'script_paths': [R(r'elementor', I)]
        },
        'Mantine': {
            'css_classes': [R(r'\bmantine-')]
        },
    },

    # Programming Language
    'Programming Language': {
        'PHP': {
            'headers': {'X-Powered-By': R(r'PHP', I)},
            'cookies': [R(r'^PHPSESSID$')],
            'url_paths': [R(r'\.php(\?|$)', I)]
        },
        'ASP.NET': {
            'headers': {'X-Powered-By': R(r'ASP\.NET', I), 'X-AspNet-Version': R(r'.*'), 'X-AspNetMvc-Version': R(r'.*')},
            'cookies': [R(r'^ASP\.NET_SessionId$'), R(r'^__RequestVerificationToken$')],
            'url_paths': [R(r'\.aspx(\?|$)', I)]
        },
        'Java': {
            'cookies': [R(r'^JSESSIONID$')],
            'url_paths': [R(r'\.jsp(\?|$)', I)]
        },
        'Python': {
            'headers': {'Server': R(r'(gunicorn|uvicorn|Werkzeug)', I)}
        },
        'Ruby': {
            'headers': {'X-Powered-By': R(r'Phusion Passenger', I), 'Server': R(r'Passenger', I)}
        },
        'ColdFusion': {
            'url_paths': [R(r'\.cfm(\?|$)', I)],
            'cookies': [R(r'^CFID$'), R(r'^CFTOKEN$')]
        },
        'Perl': {
            'url_paths': [R(r'\.pl(\?|$)', I), R(r'cgi-bin/', I)]
        },
    },

    # Web Server
    'Web Server': {
        'Nginx': {
            'headers': {'Server': R(r'^nginx', I)}
        },
        'Apache': {
            'headers': {'Server': R(r'^Apache', I)}
        },
        'LiteSpeed': {
            'headers': {'Server': R(r'LiteSpeed', I)}
        },
        'IIS': {
            'headers': {'Server': R(r'Microsoft-IIS', I)}
        },
        'Caddy': {
            'headers': {'Server': R(r'Caddy', I)}
        },
        'OpenResty': {
            'headers': {'Server': R(r'openresty', I)}
        },
        'Varnish': {
            'headers': {'X-Varnish': R(r'.*')}
        },
        'Envoy': {
            'headers': {'Server': R(r'envoy', I)}
        },
        'Tengine': {
            'headers': {'Server': R(r'Tengine', I)}
        },
    },

    # PaaS / Hosting
    'PaaS/Hosting': {
        'Vercel': {
            'headers': {'x-vercel-id': R(r'.*'), 'server': R(r'Vercel', I)}
        },
        'Netlify': {
            'headers': {'x-nf-request-id': R(r'.*'), 'server': R(r'Netlify', I)}
        },
        'Heroku': {
            'headers': {'Via': R(r'vegur', I)}
        },
        'AWS': {
            'headers': {'Server': R(r'AmazonS3|Amazon', I), 'x-amz-request-id': R(r'.*')}
        },
        'Google Cloud': {
            'headers': {'Server': R(r'^GSE$', I), 'x-cloud-trace-context': R(r'.*')}
        },
        'Azure': {
            'headers': {'x-azure-ref': R(r'.*'), 'x-ms-request-id': R(r'.*')}
        },
        'DigitalOcean': {
            'headers': {'Server': R(r'digitalocean', I)}
        },
        'Render': {
            'headers': {'Server': R(r'Render', I)}
        },
        'Railway': {
            'headers': {'Server': R(r'railway', I)}
        },
        'Fly.io': {
            'headers': {'fly-request-id': R(r'.*')}
        },
        'Firebase Hosting': {
            'headers': {'x-served-by': R(r'firebase', I)}
        },
        'Surge.sh': {
            'headers': {'Server': R(r'surge', I)}
        },
        'Plesk': {
            'headers': {'X-Powered-By': R(r'Plesk', I)}
        },
        'cPanel': {
            'headers': {'Server': R(r'cPanel', I)},
            'url_paths': [R(r'cpanel', I)]
        },
    },

    # CDN
    'CDN': {
        'Fastly': {
            'headers': {'Via': R(r'Fastly', I), 'X-Served-By': R(r'cache-', I)}
        },
        'Akamai': {
            'headers': {'X-Akamai-Transformed': R(r'.*'), 'Server': R(r'AkamaiGHost', I)}
        },
        'KeyCDN': {
            'headers': {'Server': R(r'keycdn', I)}
        },
        'StackPath': {
            'headers': {'x-hw': R(r'.*')}
        },
        'Sucuri': {
            'headers': {'Server': R(r'Sucuri', I), 'X-Sucuri-ID': R(r'.*')}
        },
        'Incapsula': {
            'headers': {'X-CDN': R(r'Incapsula', I)}
        },
        'BunnyCDN': {
            'headers': {'Server': R(r'BunnyCDN', I), 'CDN-PullZone': R(r'.*')}
        },
    },

    # Security
    'Security': {
        'Cloudflare WAF': {
            'headers': {'cf-mitigated': R(r'.*'), 'cf-chl-bypass': R(r'.*')}
        },
        'AWS WAF': {
            'headers': {'x-amzn-waf-action': R(r'.*')}
        },
        'Akamai WAF': {
            'headers': {'X-Akamai-Session-Info': R(r'.*')}
        },
        'ModSecurity': {
            'headers': {'Server': R(r'mod_security', I)}
        },
        'Wordfence': {
            'headers': {'X-WF-Policy': R(r'.*')},
            'script_paths': [R(r'wordfence', I)]
        },
    },

    # Tag Manager
    'Tag Manager': {
        'Adobe Launch': {
            'script_paths': [R(r'assets\.adobedtm\.com', I)]
        },
        'Tealium': {
            'js_globals': ['utag'],
            'script_paths': [R(r'tags\.tiqcdn\.com', I)]
        },
    },

    # Chat / Support
    'Chat/Support': {
        'Intercom': {
            'js_globals': ['Intercom'],
            'script_paths': [R(r'widget\.intercom\.io', I)]
        },
        'Zendesk': {
            'js_globals': ['zE'],
            'script_paths': [R(r'static\.zdassets\.com', I)]
        },
        'Drift': {
            'js_globals': ['drift'],
            'script_paths': [R(r'js\.driftt\.com', I)]
        },
        'Crisp': {
            'js_globals': ['$crisp'],
            'script_paths': [R(r'client\.crisp\.chat', I)]
        },
        'LiveChat': {
            'js_globals': ['LiveChatWidget'],
            'script_paths': [R(r'cdn\.livechatinc\.com', I)]
        },
        'Tawk.to': {
            'js_globals': ['Tawk_API'],
            'script_paths': [R(r'embed\.tawk\.to', I)]
        },
        'Tidio': {
            'script_paths': [R(r'code\.tidio\.co', I)]
        },
        'HubSpot Chat': {
            'script_paths': [R(r'js\.usemessages\.com', I)]
        },
        'Freshdesk': {
            'script_paths': [R(r'wchat\.freshchat\.com', I)]
        },
    },

    # Payment / Billing
    'Payment': {
        'Stripe': {
            'js_globals': ['Stripe'],
            'script_paths': [R(r'js\.stripe\.com', I)]
        },
        'PayPal': {
            'script_paths': [R(r'paypal\.com/sdk', I), R(r'paypalobjects\.com', I)]
        },
        'Braintree': {
            'script_paths': [R(r'js\.braintreegateway\.com', I)]
        },
        'Square': {
            'script_paths': [R(r'squareup\.com', I), R(r'square\.site', I)]
        },
        'Klarna': {
            'script_paths': [R(r'klarna\.com', I)]
        },
        'Afterpay': {
            'script_paths': [R(r'afterpay\.com', I)]
        },
    },

    # A/B Testing
    'A/B Testing': {
        'Optimizely': {
            'script_paths': [R(r'cdn\.optimizely\.com', I)],
            'js_globals': ['optimizely']
        },
        'LaunchDarkly': {
            'script_paths': [R(r'launchdarkly', I)]
        },
        'Google Optimize': {
            'script_paths': [R(r'optimize\.google\.com', I)]
        },
    },

    # Email / CRM
    'Marketing': {
        'Mailchimp': {
            'script_paths': [R(r'chimpstatic\.com', I), R(r'list-manage\.com', I)]
        },
        'Klaviyo': {
            'js_globals': ['klaviyo'],
            'script_paths': [R(r'static\.klaviyo\.com', I)]
        },
        'Salesforce': {
            'script_paths': [R(r'force\.com', I)]
        },
        'ConvertKit': {
            'script_paths': [R(r'convertkit\.com', I)]
        },
        'ActiveCampaign': {
            'script_paths': [R(r'trackcmp\.net', I)]
        },
    },

    # Font
    'Font Service': {
        'Google Fonts': {
            'script_paths': [R(r'fonts\.googleapis\.com', I)]
        },
        'Adobe Fonts': {
            'script_paths': [R(r'use\.typekit\.net', I)]
        },
        'Font Awesome': {
            'script_paths': [R(r'fontawesome', I), R(r'font-awesome', I)],
            'css_classes': [R(r'\bfa-')]
        },
    },

    # State Management
    'State Management': {
        'Redux': {
            'js_globals': ['__REDUX_DEVTOOLS_EXTENSION__']
        },
        'MobX': {
            'js_globals': ['__mobxGlobals']
        },
        'Zustand': {
            'storage_keys': ['zustand']
        },
        'Pinia': {
            'storage_keys': ['pinia']
        },
    },

    # Build Tool
    'Build Tool': {
        'Webpack': {
            'js_globals': ['webpackJsonp', '__webpack_require__', 'webpackChunk']
        },
        'Vite': {
            'script_paths': [R(r'/@vite/', I), R(r'/@id/', I)],
            'html_attrs': [R(r'data-vite')],
            'html_comments': [R(r'vite', I)]
        },
        'Parcel': {
            'script_paths': [R(r'parcelRequire', I)]
        },
        'Turbopack': {
            'js_globals': ['TURBOPACK'],
            'script_paths': [R(r'turbopack', I)]
        },
        'Rspack': {
            'script_paths': [R(r'rspack', I)]
        },
    },

    # Monitoring
    'Monitoring': {
        'Sentry': {
            'js_globals': ['Sentry', '__SENTRY__'],
            'script_paths': [R(r'browser\.sentry-cdn\.com', I)]
        },
        'Datadog RUM': {
            'js_globals': ['DD_RUM'],
            'script_paths': [R(r'datadoghq\.com', I)]
        },
        'New Relic': {
            'js_globals': ['NREUM', 'newrelic'],
            'script_paths': [R(r'js-agent\.newrelic\.com', I)]
        },
        'LogRocket': {
            'js_globals': ['LogRocket'],
            'script_paths': [R(r'cdn\.logrocket\.io', I)]
        },
        'Bugsnag': {
            'js_globals': ['Bugsnag'],
            'script_paths': [R(r'd2wy8f7a9ursnm\.cloudfront\.net', I)]
        },
        'Rollbar': {
            'js_globals': ['Rollbar'],
            'script_paths': [R(r'rollbar\.com', I)]
        },
    },

    # Consent / Cookie
    'Cookie Consent': {
        'OneTrust': {
            'script_paths': [R(r'cdn\.cookielaw\.org', I)],
            'js_globals': ['OneTrust']
        },
        'CookieBot': {
            'script_paths': [R(r'consent\.cookiebot\.com', I)],
            'js_globals': ['Cookiebot']
        },
        'CookieYes': {
            'script_paths': [R(r'cdn-cookieyes\.com', I)]
        },
        'Osano': {
            'script_paths': [R(r'cmp\.osano\.com', I)]
        },
        'TrustArc': {
            'script_paths': [R(r'consent\.trustarc\.com', I)]
        },
    },

    # Misc
    'Miscellaneous': {
        'PWA': {
            'html_attrs': [R(r'href="[^"]*\.webmanifest"'), R(r'href="[^"]*manifest\.json"')],
        },
        'AMP': {
            'html_attrs': [R(r'<html amp'), R(r'<html ⚡')],
            'script_paths': [R(r'cdn\.ampproject\.org', I)]
        },
        'Tapatalk': {
            'script_paths': [R(r'tapatalk', I)],
            'html_attrs': [R(r'tapatalk', I), R(r'mobiquo', I)],
            'url_paths': [R(r'mobiquo(?:/|\.php)', I)]
        },
    },
}

from .extended import EXTENDED_RULES
for _cat, _techs in EXTENDED_RULES.items():
    if _cat not in RULES:
        RULES[_cat] = {}
    for _name, _conds in _techs.items():
        if _name not in RULES[_cat]:
            RULES[_cat][_name] = _conds
        else:
            for _k, _v in _conds.items():
                if _k in RULES[_cat][_name]:
                    if isinstance(RULES[_cat][_name][_k], list):
                        RULES[_cat][_name][_k].extend(_v)
                    elif isinstance(RULES[_cat][_name][_k], dict):
                        RULES[_cat][_name][_k].update(_v)
                else:
                    RULES[_cat][_name][_k] = _v

