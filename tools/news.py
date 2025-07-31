"""
News API Tool for CLAIRE
Provides real-time AI policy and regulation news
"""

from langchain.tools import tool
import requests
import os
from datetime import datetime, timedelta
from typing import Optional
import logging

@tool
def get_ai_policy_news(
    query: str = "AI regulation policy", 
    days_back: int = 7,
    max_articles: int = 5
) -> str:
    """
    Get recent news articles about AI policy and regulation.
    
    Args:
        query: Search query for news (default: "AI regulation policy")
        days_back: How many days back to search (default: 7)
        max_articles: Maximum number of articles to return (default: 5)
    
    Returns:
        Formatted news articles with titles, sources, and summaries
    """
    try:
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            return "❌ News API key not configured. Please set NEWS_API_KEY environment variable."
        
        # Calculate date range
        from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        # NewsAPI endpoint
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "from": from_date,
            "sortBy": "relevancy",
            "pageSize": max_articles,
            "apiKey": api_key,
            "language": "en"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        articles = data.get("articles", [])
        
        if not articles:
            return f"No recent news found for '{query}' in the last {days_back} days."
        
        # Format results
        result = f"## 📰 AI Policy & Regulation News ({len(articles)} articles)\n\n"
        result += f"**Search:** {query} | **Period:** Last {days_back} days\n\n"
        
        for i, article in enumerate(articles, 1):
            title = article.get("title", "No title")
            source = article.get("source", {}).get("name", "Unknown source")
            description = article.get("description", "No description available")
            url = article.get("url", "")
            published_at = article.get("publishedAt", "")
            
            # Format date
            if published_at:
                try:
                    pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    formatted_date = pub_date.strftime("%Y-%m-%d %H:%M")
                except:
                    formatted_date = published_at
            else:
                formatted_date = "Unknown date"
            
            result += f"### {i}. {title}\n"
            result += f"**Source:** {source} | **Date:** {formatted_date}\n"
            result += f"**Summary:** {description}\n"
            if url:
                result += f"**Link:** {url}\n"
            result += "\n"
        
        result += "---\n"
        result += "💡 Stay informed about regulatory changes that may impact your AI systems."
        
        return result
        
    except requests.RequestException as e:
        logging.error(f"Error fetching news: {e}")
        return f"Error fetching news: {str(e)}"
    except Exception as e:
        logging.error(f"Error in get_ai_policy_news: {e}")
        return f"Error getting AI policy news: {str(e)}"

@tool
def get_general_news(
    category: str = "technology",
    country: str = "us",
    max_articles: int = 5
) -> str:
    """
    Get general news headlines by category.
    
    Args:
        category: News category (business, technology, science, health, general)
        country: Country code (us, gb, ca, au, etc.)
        max_articles: Maximum number of articles to return
    
    Returns:
        Formatted news headlines with sources
    """
    try:
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            return "❌ News API key not configured. Please set NEWS_API_KEY environment variable."
        
        # NewsAPI top headlines endpoint
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "category": category,
            "country": country,
            "pageSize": max_articles,
            "apiKey": api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        articles = data.get("articles", [])
        
        if not articles:
            return f"No current {category} headlines found for {country.upper()}."
        
        # Format results
        result = f"## 📺 {category.title()} Headlines ({len(articles)} articles)\n\n"
        
        for i, article in enumerate(articles, 1):
            title = article.get("title", "No title")
            source = article.get("source", {}).get("name", "Unknown source")
            description = article.get("description", "")
            published_at = article.get("publishedAt", "")
            
            # Format date
            if published_at:
                try:
                    pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    formatted_date = pub_date.strftime("%Y-%m-%d %H:%M")
                except:
                    formatted_date = published_at
            else:
                formatted_date = "Recent"
            
            result += f"### {i}. {title}\n"
            result += f"**Source:** {source} | **Date:** {formatted_date}\n"
            if description:
                result += f"**Summary:** {description}\n"
            result += "\n"
        
        return result
        
    except requests.RequestException as e:
        logging.error(f"Error fetching news: {e}")
        return f"Error fetching news: {str(e)}"
    except Exception as e:
        logging.error(f"Error in get_general_news: {e}")
        return f"Error getting general news: {str(e)}"
