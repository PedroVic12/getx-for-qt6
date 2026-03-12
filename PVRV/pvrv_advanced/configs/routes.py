ROUTES = [
    {
        "path": "/myhomepagestatefull",
        "view": "views.pages.myhomepagestatefull_view.MyhomepagestatefullView",
        "label": "Myhomepagestatefull",
        "icon": ft.Icons.CHEVRON_RIGHT,
        "show_in_top": True,
        "show_in_bottom": False,
    },

    { "path": "/pdf_extractor", "view_class": "Pdf_extractorView", "module": "views.pages.pdf_extractor_view", "label": "Pdf_extractor" },
    { "path": "/help", "view_class": "HelpView", "module": "views.pages.help_view", "label": "Help" },
    { "path": "/settings", "view_class": "SettingsView", "module": "views.pages.settings_view", "label": "Settings" },
    {
        "path": "/",
        "view_class": "HomeView",
        "module": "views.pages.home_view",
        "label": "Home",
    },
]
