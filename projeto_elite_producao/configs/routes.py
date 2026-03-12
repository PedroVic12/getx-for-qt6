ROUTES = [
    {"path": "/", "view_class": "HomeView", "module": "views.pages.home_view", "label": "Home"},
    {"path": "/pdf", "view_class": "Pdf_extractorView", "module": "views.pages.pdf_extractor_view", "label": "PDF Extractor"},
    {"path": "/settings", "view_class": "SettingsView", "module": "views.pages.settings_view", "label": "Settings"},
    {"path": "/help", "view_class": "HelpView", "module": "views.pages.help_view", "label": "Help"}
]