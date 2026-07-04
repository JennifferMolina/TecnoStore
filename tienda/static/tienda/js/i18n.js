(function(){
    const TRANSLATIONS = {
        es: {
            home: 'Inicio',
            catalog: 'Catálogo',
            profile: 'Perfil',
            login: 'Iniciar sesión',
            register: 'Registrarse',
            contact: 'Contacto',
            purchases: 'Mis compras',
            messages: 'Mensajes',
            logout: 'Salir',
            cart: 'Carrito',
            welcome_title: 'Bienvenida a TecnoStore',
            welcome_sub: 'Tecnología, accesorios y gaming seleccionados para una experiencia de compra rápida, segura y moderna.',
            hero_cta: 'Ir al catálogo',
            quick_catalog: 'Catálogo',
            quick_purchases: 'Mis compras',
            quick_profile: 'Perfil',
            quick_contact: 'Contacto',
            categories_title: 'Categorías',
            technology: 'Tecnología',
            accesorios: 'Accesorios',
            gaming: 'Gaming',
            cta_explore: 'Explora nuestros productos destacados',
            cta_view: 'Ver destacados',
            contact_title: 'Contacto',
            send_message: 'Enviar mensaje',
            name: 'Nombre',
            email: 'Correo electrónico',
            phone: 'Teléfono',
            subject: 'Asunto',
            message: 'Mensaje'
        },
        en: {
            home: 'Home',
            catalog: 'Catalog',
            profile: 'Profile',
            login: 'Log in',
            register: 'Register',
            contact: 'Contact',
            purchases: 'Purchases',
            messages: 'Messages',
            logout: 'Log out',
            cart: 'Cart',
            welcome_title: 'Welcome to TecnoStore',
            welcome_sub: 'Technology, accessories and gaming selected for a fast, secure shopping experience.',
            hero_cta: 'Go to catalog',
            quick_catalog: 'Catalog',
            quick_purchases: 'My purchases',
            quick_profile: 'Profile',
            quick_contact: 'Contact',
            categories_title: 'Categories',
            technology: 'Technology',
            accesorios: 'Accessories',
            gaming: 'Gaming',
            cta_explore: 'Explore our featured products',
            cta_view: 'View featured',
            contact_title: 'Contact',
            send_message: 'Send message',
            name: 'Name',
            email: 'Email',
            phone: 'Phone',
            subject: 'Subject',
            message: 'Message'
        }
    };

    function setFlagButton(lang){
        const btn = document.getElementById('lang-toggle');
        if(!btn) return;
        btn.textContent = (lang === 'en') ? '🇬🇧' : '🇪🇸';
        btn.setAttribute('aria-label', lang === 'en' ? 'Switch to English' : 'Cambiar a Español');
    }

    function translate(lang){
        const dict = TRANSLATIONS[lang] || TRANSLATIONS.es;

        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if(!key) return;
            const text = dict[key];
            if(text !== undefined){
                el.textContent = text;
            }
        });

        // placeholders
        document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
            const key = el.getAttribute('data-i18n-placeholder');
            const text = dict[key];
            if(text !== undefined){
                el.placeholder = text;
            }
        });

        // title attributes
        document.querySelectorAll('[data-i18n-title]').forEach(el => {
            const key = el.getAttribute('data-i18n-title');
            const text = dict[key];
            if(text !== undefined){
                el.title = text;
            }
        });

        // special case: cart label (keeps count)
        const cartLabel = document.getElementById('cart-label');
        if(cartLabel){
            const base = dict['cart'] || 'Carrito';
            cartLabel.textContent = base;
        }

        setFlagButton(lang);
    }

    function currentLang(){
        return localStorage.getItem('site_lang') || 'es';
    }

    function setLang(lang){
        localStorage.setItem('site_lang', lang);
        translate(lang);
    }

    document.addEventListener('DOMContentLoaded', function(){
        const lang = currentLang();
        translate(lang);

        const btn = document.getElementById('lang-toggle');
        if(btn){
            btn.addEventListener('click', function(e){
                const next = (currentLang() === 'es') ? 'en' : 'es';
                setLang(next);
            });
        }
    });
})();
