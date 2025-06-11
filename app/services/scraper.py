import requests
from bs4 import BeautifulSoup
import logging
import time
import os

class JobScraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

    def extract_job_description(self, url):
        """Extract job description from various job sites"""
        try:
            self.logger.info(f"Extracting job description from: {url}")
            
            # Add delay to be respectful
            time.sleep(1)
            
            if 'linkedin.com' in url:
                return self._extract_from_linkedin(url)
            elif 'indeed.com' in url:
                return self._extract_from_indeed(url)
            elif 'glassdoor.com' in url:
                return self._extract_from_glassdoor(url)
            else:
                return self._extract_generic(url)
                
        except Exception as e:
            self.logger.error(f"Error scraping job description: {str(e)}")
            # Try generic extraction as fallback
            try:
                self.logger.info("Trying generic extraction as fallback...")
                return self._extract_generic(url)
            except Exception as fallback_error:
                self.logger.error(f"Fallback extraction also failed: {str(fallback_error)}")
                raise ValueError(f"Failed to extract job description: {str(e)}")

    def _save_debug_html(self, html_content, site_name):
        """Save HTML for debugging"""
        debug_dir = "debug_html"
        if not os.path.exists(debug_dir):
            os.makedirs(debug_dir)
        
        filename = f"{debug_dir}/{site_name}_debug.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        self.logger.info(f"Debug HTML saved to {filename}")

    def _extract_from_indeed(self, url):
        """Extract job description from Indeed"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            # Save debug HTML
            self._save_debug_html(response.text, "indeed")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Updated Indeed selectors (they change frequently)
            selectors = [
                'div[data-testid="jobsearch-JobComponent-description"]',
                'div.jobsearch-jobDescriptionText',
                'div.jobsearch-JobComponent-description',
                'div#jobDescriptionText',
                'div.jobsearch-SerpJobCard-description',
                'div.job-snippet',
                'span[title]',
                'div.summary',
                # More generic selectors
                'div[class*="description"]',
                'div[class*="job"]',
                'div[id*="description"]',
                'div[id*="job"]'
            ]
            
            # Try each selector
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    text = ' '.join([self._clean_text(el.get_text()) for el in elements])
                    if len(text) > 100:  # Make sure we got substantial content
                        self.logger.info(f"Found content with selector: {selector}")
                        return text
            
            # If no specific selectors work, try to find the main content
            return self._extract_main_content(soup, "Indeed")
            
        except Exception as e:
            self.logger.error(f"Indeed extraction failed: {str(e)}")
            raise ValueError(f"Could not find job description on Indeed page: {str(e)}")

    def _extract_from_linkedin(self, url):
        """Extract job description from LinkedIn"""
        try:
            # LinkedIn requires more sophisticated headers
            linkedin_headers = {
                **self.headers,
                'Referer': 'https://www.linkedin.com/',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
            }
            
            response = requests.get(url, headers=linkedin_headers, timeout=15)
            response.raise_for_status()
            
            # Save debug HTML
            self._save_debug_html(response.text, "linkedin")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Updated LinkedIn selectors
            selectors = [
                'div.description__text',
                'div.show-more-less-html__markup',
                'div[data-test-id="job-description"]',
                'div.jobs-description__content',
                'div.jobs-box__html-content',
                'section.jobs-description',
                'div.jobs-description-content__text',
                'div.job-view-layout',
                'div.jobs-details__main-content',
                # More generic
                'div[class*="description"]',
                'div[class*="job"]'
            ]
            
            # Try each selector
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    text = ' '.join([self._clean_text(el.get_text()) for el in elements])
                    if len(text) > 100:
                        self.logger.info(f"Found content with selector: {selector}")
                        return text
            
            # If no specific selectors work, try to find the main content
            return self._extract_main_content(soup, "LinkedIn")
            
        except Exception as e:
            self.logger.error(f"LinkedIn extraction failed: {str(e)}")
            raise ValueError(f"Could not find job description on LinkedIn page: {str(e)}")

    def _extract_from_glassdoor(self, url):
        """Extract job description from Glassdoor"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            # Save debug HTML
            self._save_debug_html(response.text, "glassdoor")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            selectors = [
                'div.jobDescriptionContent',
                'div[data-test="jobDescription"]',
                'div.desc',
                'div.jobDescription',
                'section[data-test="description"]'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                if elements:
                    text = ' '.join([self._clean_text(el.get_text()) for el in elements])
                    if len(text) > 100:
                        return text
            
            return self._extract_main_content(soup, "Glassdoor")
            
        except Exception as e:
            self.logger.error(f"Glassdoor extraction failed: {str(e)}")
            raise ValueError(f"Could not find job description on Glassdoor page: {str(e)}")

    def _extract_generic(self, url):
        """Generic extraction for other job sites"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            # Save debug HTML
            self._save_debug_html(response.text, "generic")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            return self._extract_main_content(soup, "Generic")
            
        except Exception as e:
            self.logger.error(f"Generic extraction failed: {str(e)}")
            raise ValueError(f"Could not extract content from URL: {str(e)}")

    def _extract_main_content(self, soup, site_name):
        """Extract main content when specific selectors fail"""
        try:
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            # Try to find main content areas
            main_selectors = [
                'main',
                'article',
                'div[role="main"]',
                'div.main-content',
                'div.content',
                'div.container',
                'body'
            ]
            
            for selector in main_selectors:
                main_element = soup.select_one(selector)
                if main_element:
                    # Get all paragraphs and divs with substantial text
                    text_elements = main_element.find_all(['p', 'div', 'li', 'span'])
                    text_blocks = []
                    
                    for element in text_elements:
                        text = self._clean_text(element.get_text())
                        if len(text) > 50:  # Only substantial text blocks
                            text_blocks.append(text)
                    
                    if text_blocks:
                        content = '\n\n'.join(text_blocks)
                        if len(content) > 200:  # Make sure we got meaningful content
                            self.logger.info(f"Extracted content using main content strategy for {site_name}")
                            return content
            
            # Last resort - get all text
            all_text = soup.get_text()
            lines = [line.strip() for line in all_text.splitlines() if line.strip()]
            meaningful_lines = [line for line in lines if len(line) > 30]
            
            if meaningful_lines:
                content = '\n'.join(meaningful_lines)
                if len(content) > 200:
                    self.logger.info(f"Extracted content using last resort strategy for {site_name}")
                    return content
            
            raise ValueError(f"Could not extract meaningful content from {site_name} page")
            
        except Exception as e:
            raise ValueError(f"Main content extraction failed: {str(e)}")

    def _clean_text(self, text):
        """Clean extracted text"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = ' '.join(text.split())
        
        # Remove common unwanted phrases
        unwanted_phrases = [
            'Sign in',
            'Create account',
            'Apply now',
            'Save job',
            'Share',
            'Report job',
            'Cookie policy',
            'Privacy policy'
        ]
        
        for phrase in unwanted_phrases:
            text = text.replace(phrase, '')
        
        return text.strip()