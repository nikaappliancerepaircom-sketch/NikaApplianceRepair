#!/usr/bin/env python3
"""
BMAD V2 - TIER 3 CONTENT & UX TESTS
50 parameters: Content Quality (20) + Design & UX (30)
Target: 70% score
"""

import re
import json
from pathlib import Path

class Tier3Tester:
    """Test 50 medium-priority parameters - Content & UX"""

    def __init__(self, html_file, config_file):
        self.html_file = html_file
        self.config_file = config_file
        self.html_content = ""
        self.text_content = ""
        self.config = {}
        self.results = []
        self.score = 0
        self.total_tests = 50

    def load_config(self):
        with open(self.config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        return True

    def load_html(self):
        with open(self.html_file, 'r', encoding='utf-8') as f:
            self.html_content = f.read()

        # Extract text
        text = re.sub(r'<script[^>]*>.*?</script>', '', self.html_content, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        self.text_content = ' '.join(text.split())

        return True

    def test_all(self):
        """Run all 50 Tier 3 tests"""
        print("\n" + "=" * 60)
        print("TIER 3: CONTENT & UX (50 params)")
        print("=" * 60)

        # CONTENT QUALITY (46-65)
        self.test_paragraph_length()        # 46
        self.test_bullet_lists()            # 47
        self.test_sections_count()          # 48
        self.test_readability()             # 49
        self.test_semantic_keywords()       # 50
        self.test_question_headers()        # 51
        self.test_answer_format()           # 52
        self.test_table_of_contents()       # 53
        self.test_jump_links()              # 54
        self.test_related_content()         # 55
        self.test_authority_signals()       # 56
        self.test_pain_points()             # 57
        self.test_benefit_headers()         # 58
        self.test_active_voice()            # 59
        self.test_technical_explanations()  # 60
        self.test_faq_section()             # 61
        self.test_process_guides()          # 62
        self.test_comparison_tables()       # 63
        self.test_stats_data()              # 64
        self.test_expert_quotes()           # 65

        # DESIGN & UX (66-95)
        self.test_page_speed()              # 66
        self.test_lazy_loading()            # 67
        self.test_mobile_breakpoints()      # 68
        self.test_responsive_typography()   # 69
        self.test_color_contrast()          # 70
        self.test_font_size()               # 71
        self.test_whitespace()              # 72
        self.test_visual_hierarchy()        # 73
        self.test_click_targets()           # 74
        self.test_form_validation()         # 75
        self.test_error_messages()          # 76
        self.test_success_states()          # 77
        self.test_loading_indicators()      # 78
        self.test_hover_states()            # 79
        self.test_focus_indicators()        # 80
        self.test_skip_navigation()         # 81
        self.test_keyboard_accessible()     # 82
        self.test_screen_reader()           # 83
        self.test_touch_friendly()          # 84
        self.test_hamburger_menu()          # 85
        self.test_search_function()         # 86
        self.test_breadcrumb_visible()      # 87
        self.test_back_to_top()             # 88
        self.test_print_styles()            # 89
        self.test_favicon()                 # 90
        self.test_404_page()                # 91
        self.test_thank_you_page()          # 92
        self.test_privacy_policy()          # 93
        self.test_terms_link()              # 94
        self.test_cookie_notice()           # 95

        # Calculate score
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        self.score = (passed / self.total_tests) * 100

        self.print_summary()
        return self.score >= 70

    # CONTENT QUALITY TESTS (46-65)

    def test_paragraph_length(self):
        """46. Paragraphs ≤5 sentences"""
        paragraphs = re.findall(r'<p[^>]*>(.*?)</p>', self.html_content, re.DOTALL)
        if paragraphs:
            long_paragraphs = []
            for p in paragraphs:
                sentences = len(re.findall(r'[.!?]+', p))
                if sentences > 5:
                    long_paragraphs.append(sentences)

            if not long_paragraphs:
                self.results.append({'param': '46. Paragraph length', 'status': 'PASS'})
            else:
                self.results.append({'param': '46. Paragraph length', 'status': 'FAIL',
                                   'issue': f'{len(long_paragraphs)} paragraphs >5 sentences'})
        else:
            self.results.append({'param': '46. Paragraph length', 'status': 'WARN', 'issue': 'No <p> tags'})

    def test_bullet_lists(self):
        """47. Bullet lists: 3+"""
        lists = len(re.findall(r'<ul|<ol', self.html_content, re.IGNORECASE))
        if lists >= 3:
            self.results.append({'param': '47. Bullet lists', 'status': 'PASS', 'value': lists})
        else:
            self.results.append({'param': '47. Bullet lists', 'status': 'FAIL',
                               'issue': f'{lists} lists (need 3+)'})

    def test_sections_count(self):
        """48. Sections: 6-12"""
        sections = len(re.findall(r'<section', self.html_content, re.IGNORECASE))
        target_min = self.config['bmad_targets']['sections_min']
        target_max = self.config['bmad_targets']['sections_max']

        if target_min <= sections <= target_max:
            self.results.append({'param': '48. Section count', 'status': 'PASS', 'value': sections})
        else:
            self.results.append({'param': '48. Section count', 'status': 'FAIL',
                               'issue': f'{sections} sections (target: {target_min}-{target_max})'})

    def test_readability(self):
        """49. Readability score"""
        # Simple readability check: average words per sentence
        sentences = len(re.findall(r'[.!?]+', self.text_content))
        words = len(re.findall(r'\b\w+\b', self.text_content))

        if sentences > 0:
            avg_words = words / sentences
            # Good readability: 15-20 words per sentence
            if 15 <= avg_words <= 20:
                self.results.append({'param': '49. Readability', 'status': 'PASS',
                                   'value': f'{avg_words:.1f} words/sentence'})
            else:
                self.results.append({'param': '49. Readability', 'status': 'WARN',
                                   'issue': f'{avg_words:.1f} words/sentence (optimal: 15-20)'})
        else:
            self.results.append({'param': '49. Readability', 'status': 'WARN', 'issue': 'No sentences'})

    def test_semantic_keywords(self):
        """50. Semantic keywords: 5+"""
        semantic_kws = self.config['keywords']['semantic']
        found = sum(1 for kw in semantic_kws if kw.lower() in self.text_content.lower())

        if found >= 5:
            self.results.append({'param': '50. Semantic keywords', 'status': 'PASS', 'value': found})
        else:
            self.results.append({'param': '50. Semantic keywords', 'status': 'FAIL',
                               'issue': f'{found} keywords (need 5+)'})

    def test_question_headers(self):
        """51. Question headers (H2/H3)"""
        headers = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', self.html_content, re.IGNORECASE)
        questions = [h for h in headers if '?' in h]

        if len(questions) >= 2:
            self.results.append({'param': '51. Question headers', 'status': 'PASS', 'value': len(questions)})
        else:
            self.results.append({'param': '51. Question headers', 'status': 'WARN',
                               'issue': f'Only {len(questions)} question headers'})

    def test_answer_format(self):
        """52. Direct answer format"""
        # Check for answer indicators
        answer_patterns = ['the answer is', 'yes,', 'no,', 'it depends', 'typically', 'usually']
        found_answers = sum(1 for pattern in answer_patterns if pattern in self.text_content.lower())

        if found_answers >= 2:
            self.results.append({'param': '52. Answer format', 'status': 'PASS'})
        else:
            self.results.append({'param': '52. Answer format', 'status': 'WARN',
                               'issue': 'Few direct answer patterns'})

    def test_table_of_contents(self):
        """53. Table of contents"""
        toc_indicators = ['table of contents', 'toc', 'on this page', 'jump to']
        has_toc = any(indicator in self.html_content.lower() for indicator in toc_indicators)

        if has_toc:
            self.results.append({'param': '53. Table of contents', 'status': 'PASS'})
        else:
            self.results.append({'param': '53. Table of contents', 'status': 'WARN', 'issue': 'No TOC found'})

    def test_jump_links(self):
        """54. Jump links"""
        jump_links = len(re.findall(r'href=["\']#[^"\']+', self.html_content))

        if jump_links >= 3:
            self.results.append({'param': '54. Jump links', 'status': 'PASS', 'value': jump_links})
        else:
            self.results.append({'param': '54. Jump links', 'status': 'WARN',
                               'issue': f'Only {jump_links} jump links'})

    def test_related_content(self):
        """55. Related content links"""
        related_indicators = ['related', 'see also', 'you may also', 'similar']
        has_related = any(indicator in self.html_content.lower() for indicator in related_indicators)

        if has_related:
            self.results.append({'param': '55. Related content', 'status': 'PASS'})
        else:
            self.results.append({'param': '55. Related content', 'status': 'WARN', 'issue': 'No related links'})

    def test_authority_signals(self):
        """56. Authority signals: 4+"""
        authority_kws = ['licensed', 'certified', 'experienced', 'professional', 'expert', 'qualified']
        found = sum(1 for kw in authority_kws if kw in self.text_content.lower())

        if found >= 4:
            self.results.append({'param': '56. Authority signals', 'status': 'PASS', 'value': found})
        else:
            self.results.append({'param': '56. Authority signals', 'status': 'FAIL',
                               'issue': f'{found} signals (need 4+)'})

    def test_pain_points(self):
        """57. Pain point mentions: 3+"""
        pain_kws = ['problem', 'broken', 'not working', 'issue', 'trouble', 'emergency', 'failed']
        found = sum(1 for kw in pain_kws if kw in self.text_content.lower())

        if found >= 3:
            self.results.append({'param': '57. Pain points', 'status': 'PASS', 'value': found})
        else:
            self.results.append({'param': '57. Pain points', 'status': 'FAIL',
                               'issue': f'{found} mentions (need 3+)'})

    def test_benefit_headers(self):
        """58. Benefit-driven headers"""
        headers = re.findall(r'<h[2-3][^>]*>(.*?)</h[2-3]>', self.html_content, re.IGNORECASE)
        benefit_words = ['benefit', 'advantage', 'why', 'how', 'save', 'get', 'achieve', 'improve']

        benefit_headers = sum(1 for h in headers if any(word in h.lower() for word in benefit_words))

        if benefit_headers >= 2:
            self.results.append({'param': '58. Benefit headers', 'status': 'PASS', 'value': benefit_headers})
        else:
            self.results.append({'param': '58. Benefit headers', 'status': 'WARN',
                               'issue': f'Only {benefit_headers} benefit headers'})

    def test_active_voice(self):
        """59. Active voice: 80%+"""
        # Simple heuristic: count passive voice indicators
        passive_indicators = ['was ', 'were ', 'been ', 'being ', 'is being', 'are being']
        passive_count = sum(self.text_content.lower().count(ind) for ind in passive_indicators)

        words = len(re.findall(r'\b\w+\b', self.text_content))
        passive_ratio = (passive_count / words * 100) if words > 0 else 0

        # Want <20% passive (means >80% active)
        if passive_ratio < 20:
            self.results.append({'param': '59. Active voice', 'status': 'PASS',
                               'value': f'{100-passive_ratio:.0f}% active'})
        else:
            self.results.append({'param': '59. Active voice', 'status': 'WARN',
                               'issue': f'Too much passive voice ({passive_ratio:.0f}%)'})

    def test_technical_explanations(self):
        """60. Technical terms explained"""
        # Check for explanation patterns
        explain_patterns = ['this means', 'in other words', 'simply put', 'for example', 'i.e.', 'e.g.']
        found = sum(1 for pattern in explain_patterns if pattern in self.text_content.lower())

        if found >= 2:
            self.results.append({'param': '60. Technical explanations', 'status': 'PASS'})
        else:
            self.results.append({'param': '60. Technical explanations', 'status': 'WARN',
                               'issue': 'Few explanation patterns'})

    def test_faq_section(self):
        """61. FAQ section present"""
        if 'faq' in self.html_content.lower() or 'frequently asked' in self.html_content.lower():
            self.results.append({'param': '61. FAQ section', 'status': 'PASS'})
        else:
            self.results.append({'param': '61. FAQ section', 'status': 'WARN', 'issue': 'No FAQ section'})

    def test_process_guides(self):
        """62. Step-by-step guides"""
        step_indicators = ['step 1', 'step 2', 'first,', 'second,', 'third,', 'then,', 'finally']
        found = sum(1 for ind in step_indicators if ind in self.text_content.lower())

        if found >= 3:
            self.results.append({'param': '62. Process guides', 'status': 'PASS'})
        else:
            self.results.append({'param': '62. Process guides', 'status': 'WARN',
                               'issue': 'No step-by-step guide'})

    def test_comparison_tables(self):
        """63. Comparison tables"""
        tables = len(re.findall(r'<table', self.html_content, re.IGNORECASE))

        if tables >= 1:
            self.results.append({'param': '63. Comparison tables', 'status': 'PASS', 'value': tables})
        else:
            self.results.append({'param': '63. Comparison tables', 'status': 'WARN', 'issue': 'No tables'})

    def test_stats_data(self):
        """64. Stats/data points: 3+"""
        # Look for number patterns followed by units/descriptions
        stat_patterns = r'\d+%|\d+\+|\d+\s+(?:years|clients|customers|hours|days|reviews)'
        stats = len(re.findall(stat_patterns, self.text_content, re.IGNORECASE))

        if stats >= 3:
            self.results.append({'param': '64. Stats/data points', 'status': 'PASS', 'value': stats})
        else:
            self.results.append({'param': '64. Stats/data points', 'status': 'WARN',
                               'issue': f'Only {stats} stats'})

    def test_expert_quotes(self):
        """65. Expert quotes/certifications"""
        quote_indicators = ['certified', 'accredited', 'qualified', 'trained', 'expert', 'specialist']
        found = sum(1 for ind in quote_indicators if ind in self.text_content.lower())

        if found >= 2:
            self.results.append({'param': '65. Expert quotes', 'status': 'PASS'})
        else:
            self.results.append({'param': '65. Expert quotes', 'status': 'WARN',
                               'issue': 'Few expert indicators'})

    # DESIGN & UX TESTS (66-95)

    def test_page_speed(self):
        """66. Page speed indicators"""
        # Check for speed optimization signs
        has_minified = '.min.js' in self.html_content or '.min.css' in self.html_content
        has_async = 'async' in self.html_content or 'defer' in self.html_content

        if has_minified and has_async:
            self.results.append({'param': '66. Page speed', 'status': 'PASS'})
        else:
            issues = []
            if not has_minified: issues.append('no minification')
            if not has_async: issues.append('no async loading')
            self.results.append({'param': '66. Page speed', 'status': 'WARN',
                               'issue': ', '.join(issues)})

    def test_lazy_loading(self):
        """67. Lazy loading"""
        lazy = len(re.findall(r'loading=["\']lazy', self.html_content, re.IGNORECASE))
        images = len(re.findall(r'<img', self.html_content, re.IGNORECASE))

        if images > 0:
            ratio = lazy / images
            if ratio >= 0.5:
                self.results.append({'param': '67. Lazy loading', 'status': 'PASS',
                                   'value': f'{lazy}/{images} images'})
            else:
                self.results.append({'param': '67. Lazy loading', 'status': 'WARN',
                                   'issue': f'Only {lazy}/{images} images lazy'})
        else:
            self.results.append({'param': '67. Lazy loading', 'status': 'WARN', 'issue': 'No images'})

    def test_mobile_breakpoints(self):
        """68. Mobile breakpoints: 3+"""
        breakpoints = len(re.findall(r'@media.*?(?:max-width|min-width)', self.html_content, re.IGNORECASE))

        if breakpoints >= 3:
            self.results.append({'param': '68. Mobile breakpoints', 'status': 'PASS', 'value': breakpoints})
        else:
            self.results.append({'param': '68. Mobile breakpoints', 'status': 'FAIL',
                               'issue': f'Only {breakpoints} breakpoints'})

    def test_responsive_typography(self):
        """69. Responsive typography (clamp)"""
        clamp_usage = len(re.findall(r'clamp\s*\(', self.html_content, re.IGNORECASE))

        if clamp_usage >= 5:
            self.results.append({'param': '69. Responsive typography', 'status': 'PASS'})
        else:
            self.results.append({'param': '69. Responsive typography', 'status': 'WARN',
                               'issue': f'Only {clamp_usage} clamp() uses'})

    def test_color_contrast(self):
        """70. Color contrast (basic check)"""
        # Check for contrast-related CSS
        has_contrast = 'color:' in self.html_content and 'background' in self.html_content

        if has_contrast:
            self.results.append({'param': '70. Color contrast', 'status': 'PASS'})
        else:
            self.results.append({'param': '70. Color contrast', 'status': 'WARN', 'issue': 'Cannot verify'})

    def test_font_size(self):
        """71. Font size: 16px+ body"""
        # Check for font-size declarations
        font_sizes = re.findall(r'font-size:\s*(\d+)px', self.html_content)
        small_fonts = [int(size) for size in font_sizes if int(size) < 16]

        if not small_fonts or len(small_fonts) < 3:
            self.results.append({'param': '71. Font size', 'status': 'PASS'})
        else:
            self.results.append({'param': '71. Font size', 'status': 'WARN',
                               'issue': f'{len(small_fonts)} elements <16px'})

    def test_whitespace(self):
        """72. Whitespace optimization"""
        # Check for padding/margin declarations
        has_spacing = 'padding:' in self.html_content and 'margin:' in self.html_content

        if has_spacing:
            self.results.append({'param': '72. Whitespace', 'status': 'PASS'})
        else:
            self.results.append({'param': '72. Whitespace', 'status': 'WARN', 'issue': 'Limited spacing'})

    def test_visual_hierarchy(self):
        """73. Visual hierarchy (headings)"""
        h1 = len(re.findall(r'<h1', self.html_content, re.IGNORECASE))
        h2 = len(re.findall(r'<h2', self.html_content, re.IGNORECASE))
        h3 = len(re.findall(r'<h3', self.html_content, re.IGNORECASE))

        if h1 == 1 and h2 >= 3 and h3 >= 2:
            self.results.append({'param': '73. Visual hierarchy', 'status': 'PASS'})
        else:
            self.results.append({'param': '73. Visual hierarchy', 'status': 'WARN',
                               'issue': 'Heading structure unclear'})

    def test_click_targets(self):
        """74. Click targets: 44px+"""
        # Basic check for button/link sizing
        has_touch_friendly = 'min-width' in self.html_content or 'min-height' in self.html_content

        if has_touch_friendly:
            self.results.append({'param': '74. Click targets', 'status': 'PASS'})
        else:
            self.results.append({'param': '74. Click targets', 'status': 'WARN', 'issue': 'No size constraints'})

    def test_form_validation(self):
        """75. Form validation"""
        has_validation = 'required' in self.html_content or 'pattern=' in self.html_content

        if has_validation:
            self.results.append({'param': '75. Form validation', 'status': 'PASS'})
        else:
            self.results.append({'param': '75. Form validation', 'status': 'WARN', 'issue': 'No validation'})

    def test_error_messages(self):
        """76. Error messages"""
        error_indicators = ['error', 'invalid', 'required', 'please enter']
        has_errors = any(ind in self.html_content.lower() for ind in error_indicators)

        if has_errors:
            self.results.append({'param': '76. Error messages', 'status': 'PASS'})
        else:
            self.results.append({'param': '76. Error messages', 'status': 'WARN', 'issue': 'No error handling'})

    def test_success_states(self):
        """77. Success states"""
        success_indicators = ['success', 'thank you', 'submitted', 'received']
        has_success = any(ind in self.html_content.lower() for ind in success_indicators)

        if has_success:
            self.results.append({'param': '77. Success states', 'status': 'PASS'})
        else:
            self.results.append({'param': '77. Success states', 'status': 'WARN', 'issue': 'No success feedback'})

    def test_loading_indicators(self):
        """78. Loading indicators"""
        loading_indicators = ['loading', 'spinner', 'please wait']
        has_loading = any(ind in self.html_content.lower() for ind in loading_indicators)

        if has_loading:
            self.results.append({'param': '78. Loading indicators', 'status': 'PASS'})
        else:
            self.results.append({'param': '78. Loading indicators', 'status': 'WARN', 'issue': 'No loading feedback'})

    def test_hover_states(self):
        """79. Hover states"""
        has_hover = ':hover' in self.html_content

        if has_hover:
            self.results.append({'param': '79. Hover states', 'status': 'PASS'})
        else:
            self.results.append({'param': '79. Hover states', 'status': 'WARN', 'issue': 'No hover styles'})

    def test_focus_indicators(self):
        """80. Focus indicators"""
        has_focus = ':focus' in self.html_content or 'outline:' in self.html_content

        if has_focus:
            self.results.append({'param': '80. Focus indicators', 'status': 'PASS'})
        else:
            self.results.append({'param': '80. Focus indicators', 'status': 'WARN', 'issue': 'No focus styles'})

    def test_skip_navigation(self):
        """81. Skip navigation"""
        has_skip = 'skip' in self.html_content.lower() and 'navigation' in self.html_content.lower()

        if has_skip:
            self.results.append({'param': '81. Skip navigation', 'status': 'PASS'})
        else:
            self.results.append({'param': '81. Skip navigation', 'status': 'WARN', 'issue': 'No skip link'})

    def test_keyboard_accessible(self):
        """82. Keyboard accessible"""
        has_tabindex = 'tabindex' in self.html_content

        if has_tabindex:
            self.results.append({'param': '82. Keyboard accessible', 'status': 'PASS'})
        else:
            self.results.append({'param': '82. Keyboard accessible', 'status': 'WARN', 'issue': 'No tabindex'})

    def test_screen_reader(self):
        """83. Screen reader support"""
        has_aria = 'aria-' in self.html_content or 'role=' in self.html_content

        if has_aria:
            self.results.append({'param': '83. Screen reader support', 'status': 'PASS'})
        else:
            self.results.append({'param': '83. Screen reader support', 'status': 'WARN', 'issue': 'No ARIA'})

    def test_touch_friendly(self):
        """84. Touch-friendly"""
        has_touch = 'touch' in self.html_content or 'pointer' in self.html_content

        if has_touch:
            self.results.append({'param': '84. Touch-friendly', 'status': 'PASS'})
        else:
            self.results.append({'param': '84. Touch-friendly', 'status': 'WARN', 'issue': 'No touch events'})

    def test_hamburger_menu(self):
        """85. Hamburger menu"""
        has_hamburger = 'hamburger' in self.html_content.lower() or 'menu-toggle' in self.html_content.lower()

        if has_hamburger:
            self.results.append({'param': '85. Hamburger menu', 'status': 'PASS'})
        else:
            self.results.append({'param': '85. Hamburger menu', 'status': 'WARN', 'issue': 'No mobile menu'})

    def test_search_function(self):
        """86. Search function"""
        has_search = '<form' in self.html_content and 'search' in self.html_content.lower()

        if has_search:
            self.results.append({'param': '86. Search function', 'status': 'PASS'})
        else:
            self.results.append({'param': '86. Search function', 'status': 'WARN', 'issue': 'No search'})

    def test_breadcrumb_visible(self):
        """87. Breadcrumb visible"""
        has_breadcrumb = 'breadcrumb' in self.html_content.lower()

        if has_breadcrumb:
            self.results.append({'param': '87. Breadcrumb visible', 'status': 'PASS'})
        else:
            self.results.append({'param': '87. Breadcrumb visible', 'status': 'WARN', 'issue': 'No breadcrumb'})

    def test_back_to_top(self):
        """88. Back to top button"""
        has_back_to_top = 'back to top' in self.html_content.lower() or 'scroll-to-top' in self.html_content.lower()

        if has_back_to_top:
            self.results.append({'param': '88. Back to top', 'status': 'PASS'})
        else:
            self.results.append({'param': '88. Back to top', 'status': 'WARN', 'issue': 'No back to top'})

    def test_print_styles(self):
        """89. Print styles"""
        has_print = '@media print' in self.html_content or 'print.css' in self.html_content

        if has_print:
            self.results.append({'param': '89. Print styles', 'status': 'PASS'})
        else:
            self.results.append({'param': '89. Print styles', 'status': 'WARN', 'issue': 'No print styles'})

    def test_favicon(self):
        """90. Favicon"""
        has_favicon = 'favicon' in self.html_content or 'icon' in self.html_content

        if has_favicon:
            self.results.append({'param': '90. Favicon', 'status': 'PASS'})
        else:
            self.results.append({'param': '90. Favicon', 'status': 'WARN', 'issue': 'No favicon'})

    def test_404_page(self):
        """91. Custom 404 page"""
        # Check filename or 404 indicators
        is_404 = '404' in self.html_file or '404' in self.html_content

        if is_404:
            self.results.append({'param': '91. 404 page', 'status': 'PASS'})
        else:
            self.results.append({'param': '91. 404 page', 'status': 'WARN', 'issue': 'Cannot verify'})

    def test_thank_you_page(self):
        """92. Thank you page"""
        has_thank_you = 'thank you' in self.text_content.lower() or 'thanks' in self.text_content.lower()

        if has_thank_you:
            self.results.append({'param': '92. Thank you page', 'status': 'PASS'})
        else:
            self.results.append({'param': '92. Thank you page', 'status': 'WARN', 'issue': 'No thank you message'})

    def test_privacy_policy(self):
        """93. Privacy policy link"""
        has_privacy = 'privacy' in self.html_content.lower()

        if has_privacy:
            self.results.append({'param': '93. Privacy policy', 'status': 'PASS'})
        else:
            self.results.append({'param': '93. Privacy policy', 'status': 'WARN', 'issue': 'No privacy link'})

    def test_terms_link(self):
        """94. Terms link"""
        has_terms = 'terms' in self.html_content.lower() or 'conditions' in self.html_content.lower()

        if has_terms:
            self.results.append({'param': '94. Terms link', 'status': 'PASS'})
        else:
            self.results.append({'param': '94. Terms link', 'status': 'WARN', 'issue': 'No terms link'})

    def test_cookie_notice(self):
        """95. Cookie notice"""
        has_cookie = 'cookie' in self.html_content.lower()

        if has_cookie:
            self.results.append({'param': '95. Cookie notice', 'status': 'PASS'})
        else:
            self.results.append({'param': '95. Cookie notice', 'status': 'WARN', 'issue': 'No cookie notice'})

    def print_summary(self):
        """Print test summary"""
        print("\n" + "-" * 60)
        print("TEST RESULTS:")
        print("-" * 60)

        for result in self.results:
            if result['status'] == 'PASS':
                status_icon = "[PASS]"
                value = result.get('value', '')
                print(f"{status_icon} {result['param']} {value}")
            else:
                status_icon = "[FAIL]" if result['status'] == 'FAIL' else "[WARN]"
                print(f"{status_icon} {result['param']}")
                if result.get('issue'):
                    print(f"   >> {result['issue']}")

        print("\n" + "=" * 60)
        print(f"TIER 3 SCORE: {self.score:.1f}/100")
        print("=" * 60)

        if self.score >= 70:
            print("[SUCCESS] TIER 3 PASSED")
        else:
            print("[NEEDS WORK] TIER 3 below 70%")

        print("=" * 60)

    def get_fixes_needed(self):
        return [r for r in self.results if r['status'] in ['FAIL', 'WARN']]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tier3_content_ux.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    config_file = Path(__file__).parent.parent / "config" / "business-data.json"

    tester = Tier3Tester(html_file, config_file)

    if not tester.load_config():
        sys.exit(1)

    if not tester.load_html():
        sys.exit(1)

    passed = tester.test_all()

    sys.exit(0 if passed else 1)
