from django.utils.translation import override
    # TODO
    # 1. test global key interpolation
    # 1.2 test the XSS unsafe/safe behaviour for string interpolation
    # 2. test yaml language selection
    # 3. test exception is thrown when keys aren't unique
    # 4. test a default key gets HTML escaped

import unittest
from example_proj.text import tm

class TestStringExternalization(unittest.TestCase):
    def test_global_keys_available(self):
        # global keys are available as keys themselves
        self.assertEqual(tm("current_fiscal_year"), "2019-20")
        with override("fr"):
            self.assertEqual(tm("current_fiscal_year"), "2019-2020")

    def test_global_keys_available_for_insertion(self):
        # global keys are available to be inserted into other keys' strings
        self.assertEqual(tm("a_sentence"), "The current fiscal year is 2019-20.")
        with override("fr"):
            self.assertEqual(tm("a_sentence"), "L'exercise courrant est 2019-2020.")


    def test_unallowed_tags_in_entry(self):
        # unallowed tags in entry are stripped
        escaped_str = '&lt;script&gt;console.log("Hacked!");&lt;/script&gt;'
        unescaped_str = "<script>console.log(\"Hacked!\");</script>"

        self.assertEqual(tm("example_with_script_tag"), escaped_str) # default is to sanitize output
        self.assertEqual(tm("example_with_script_tag",sanitize_output=True), escaped_str)
        self.assertEqual(tm("example_with_script_tag",sanitize_output=False), unescaped_str)
    
    def test_unallowed_tags_in_input(self):
        escaped = "The input is &lt;script&gt;console.log('Hacked');&lt;/script&gt;"
        unescaped = "The input is <script>console.log('Hacked');</script>"
        args = dict(extra_keys={"input": "<script>console.log('Hacked');</script>"})
        self.assertEqual(tm("example_with_input",**args), escaped) # default is to sanitize input and output
        self.assertEqual(tm("example_with_input",**args, sanitize_output=False),escaped) # inputs are still sanitized by default
        self.assertEqual(tm("example_with_input",**args, sanitize_output=False, sanitize_input=False),unescaped) 


    def test_markdown(self):
        rendered_str =  '<p>I contain <strong>bolds</strong> and <em>italics</em></p>\n'
        self.assertEqual(tm("example_with_markdown"),rendered_str)


    def test_tm_inputs(self):
        # test that input that are themselves tm() objs dont cause errors (regression)
        firstname = tm("james")
        lastname = tm("bond")
        self.assertEqual(tm("txt_with_args",extra_keys={"firstname":firstname,"lastname":lastname}),"Hello James Bond")
