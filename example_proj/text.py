from django_string_externalization import WatchingTextMakerCreator

en_global_keys = {
    "current_fiscal_year": "2019-20",
}
fr_global_keys = {
    "current_fiscal_year": "2019-2020",
}

text_files = [
    "example_proj/text_one.text.yaml",
    "example_proj/text_two.text.yaml",
]

tm = WatchingTextMakerCreator(
    {"en": en_global_keys, "fr": fr_global_keys}, text_files
).get_tm_func()
