# app/services/scraper.py

import requests
from bs4 import BeautifulSoup
import re
import logging
from urllib.parse import urlparse

class JobScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.logger = logging.getLogger(__name__)
    
    def extract_job_description(self, url):
        """Extract job description from various job posting sites"""
        try:
            domain = urlparse(url).netloc
            
            # LinkedIn
            if 'linkedin.com' in domain:
                return self._extract_from_linkedin(url)
            
            # Indeed
            elif 'indeed.com' in domain:
                return self._extract_from_indeed(url)
            
            # Glassdoor
            elif 'glassdoor.com' in domain:
                return self._extract_from_glassdoor(url)
            
            # ZipRecruiter
            elif 'ziprecruiter.com' in domain:
                return self._extract_from_ziprecruiter(url)
            
            # Monster
            elif 'monster.com' in domain:
                return self._extract_from_monster(url)
            
            # Default generic extraction
            else:
                return self._extract_generic(url)
                
        except Exception as e:
            self.logger.error(f"Error scraping job description: {str(e)}")
            raise ValueError(f"Failed to extract job description: {str(e)}")
    
    def _extract_from_linkedin(self, url):
        """Extract job description from LinkedIn"""
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # LinkedIn job descriptions are typically in a div with specific classes
        job_description = soup.find('div', {'class': 'description__text'})
        if not job_description:
            job_description = soup.find('div', {'class': 'show-more-less-html__markup'})
        
        if job_description:
            # Clean up the text
            return self._clean_text(job_description.get_text())
        else:
            raise ValueError("Could not find job description on LinkedIn page")
    
    def _extract_from_indeed(self, url):
        """Extract job description from Indeed"""
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Indeed job descriptions are typically in a div with id="jobDescriptionText"
        job_description = soup.find('div', {'id': 'jobDescriptionText'})
        
        if job_description:
            return self._clean_text(job_description.get_text())
        else:
            raise ValueError("Could not find job description on Indeed page")
    
    def _extract_from_glassdoor(self, url):
        """Extract job description from Glassdoor"""
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Glassdoor job descriptions are typically in a div with data-test="description"
        job_description = soup.find('div', {'data-test': 'description'})
        if not job_description:
            job_description = soup.find('div', {'class': 'jobDescriptionContent'})
        
        if job_description:
            return self._clean_text(job_description.get_text())
        else:
            raise ValueError("Could not find job description on Glassdoor page")
    
    def _extract_from_ziprecruiter(self, url):
        """Extract job description from ZipRecruiter"""
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # ZipRecruiter job descriptions are typically in a div with class="jobDescriptionSection"
        job_description = soup.find('div', {'class': 'jobDescriptionSection'})
        
        if job_description:
            return self._clean_text(job_description.get_text())
        else:
            raise ValueError("Could not find job description on ZipRecruiter page")
    
    def _extract_from_monster(self, url):
        """Extract job description from Monster"""
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Monster job descriptions are typically in a div with class="job-description"
        job_description = soup.find('div', {'class': 'job-description'})
        
        if job_description:
            return self._clean_text(job_description.get_text())
        else:
            raise ValueError("Could not find job description on Monster page")
    
    def _extract_generic(self, url):
        """Generic extraction for unsupported sites"""
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try common job description containers
        potential_containers = [
            soup.find('div', {'class': re.compile(r'job.*description', re.I)}),
            soup.find('div', {'class': re.compile(r'description', re.I)}),
            soup.find('div', {'id': re.compile(r'job.*description', re.I)}),
            soup.find('section', {'class': re.compile(r'description', re.I)}),
            soup.find('article')
        ]
        
        for container in potential_containers:
            if container:
                return self._clean_text(container.get_text())
        
        # If no specific container found, try to extract the main content
        main_content = soup.find('main')
        if main_content:
            return self._clean_text(main_content.get_text())
        
        # Last resort: extract body text and try to find job-related content
        body_text = soup.body.get_text()
        # Look for sections that might contain job details
        sections = re.split(r'\n{2,}', body_text)
        for section in sections:
            if any(keyword in section.lower() for keyword in ['job description', 'responsibilities', 'requirements', 'qualifications']):
                return self._clean_text(section)
        
        # If all else fails, return the whole body text
        return self._clean_text(body_text)
    
    def _clean_text(self, text):
        """Clean up extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove non-breaking spaces
        text = text.replace('\xa0', ' ')
        # Remove multiple newlines
        text = re.sub(r'\n{2,}', '\n', text)
        # Trim whitespace
        text = text.strip()
        return text