import requests
import re
from bs4 import BeautifulSoup

class WebScraperService:
    """Service for extracting job descriptions from URLs."""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def extract_job_description_from_url(self, url):
        """Extract job description from a URL."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Different extraction strategies based on the URL
            if 'linkedin.com' in url:
                job_description = self._extract_linkedin_job(soup)
            elif 'indeed.com' in url:
                job_description = self._extract_indeed_job(soup)
            elif 'glassdoor.com' in url:
                job_description = self._extract_glassdoor_job(soup)
            else:
                job_description = self._extract_generic_job(soup)
                
            if not job_description or len(job_description.strip()) < 50:
                return "Could not extract a meaningful job description from the provided URL. Please try copying and pasting the text instead."
                
            return job_description
            
        except Exception as e:
            print(f"Error extracting job description: {e}")
            return f"Error extracting job description from URL. Please try copying and pasting the text instead. Error: {str(e)}"
    
    def _extract_linkedin_job(self, soup):
        """Extract job description from LinkedIn."""
        selectors = [
            'div.show-more-less-html__markup',
            'div.description__text',
            'div[class*="description"]',
            'section[class*="description"]'
        ]
        
        for selector in selectors:
            job_desc = soup.select_one(selector)
            if job_desc:
                return job_desc.get_text(separator='\n', strip=True)
        
        return None
    
    def _extract_indeed_job(self, soup):
        """Extract job description from Indeed."""
        selectors = [
            'div#jobDescriptionText',
            'div[data-testid="jobsearch-JobComponent-description"]',
            'div.jobsearch-jobDescriptionText'
        ]
        
        for selector in selectors:
            job_desc = soup.select_one(selector)
            if job_desc:
                return job_desc.get_text(separator='\n', strip=True)
        
        return None
    
    def _extract_glassdoor_job(self, soup):
        """Extract job description from Glassdoor."""
        selectors = [
            'div[data-test="job-description"]',
            'div.desc',
            'div.jobDescriptionContent'
        ]
        
        for selector in selectors:
            job_desc = soup.select_one(selector)
            if job_desc:
                return job_desc.get_text(separator='\n', strip=True)
        
        return None
    
    def _extract_generic_job(self, soup):
        """Generic extraction for other job sites."""
        selectors = [
            'div[class*="job-description" i]',
            'div[id*="job-description" i]',
            'section[class*="description" i]',
            'div[class*="description" i]',
            'div[class*="details" i]',
            'main',
            'article'
        ]
        
        for selector in selectors:
            container = soup.select_one(selector)
            if container:
                text = container.get_text(separator='\n', strip=True)
                if len(text) > 200:
                    return text
        
        # Last resort: get all paragraph text
        paragraphs = soup.find_all('p')
        if paragraphs:
            combined_text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50])
            if len(combined_text) > 200:
                return combined_text
            
        return None