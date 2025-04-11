"""
Extended Tesla (TSLA) news data for testing the FundWise NLP system
This module provides a collection of Tesla-related news articles spanning
different time periods, sentiments, and topics for comprehensive testing.
"""
from datetime import datetime, timedelta

def get_tesla_articles():
    """Return a comprehensive collection of Tesla news articles"""
    
    # Calculate dates for relative timestamps
    today = datetime.now()
    yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    two_days_ago = (today - timedelta(days=2)).strftime('%Y-%m-%d')
    last_week = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    last_month = (today - timedelta(days=30)).strftime('%Y-%m-%d')
    
    return [
        # Recent positive news
        {
            'title': 'Tesla Reports Record Q2 Deliveries, Exceeding Analyst Expectations',
            'content': 'Tesla Inc. delivered 466,140 vehicles in the second quarter, beating Wall Street estimates of 445,000. The strong delivery numbers were driven by price cuts and tax incentives in key markets. Model Y remained the best-selling EV globally, with production constraints easing at both Shanghai and Berlin gigafactories. CEO Elon Musk stated that the company is on track to achieve its 1.8 million vehicle delivery target for the year.',
            'source': 'Bloomberg',
            'date': yesterday,
            'url': 'https://www.bloomberg.com/news/tesla-record-deliveries'
        },
        {
            'title': 'Tesla Supercharger Network Now Available to All EVs in North America',
            'content': 'Tesla has officially opened its Supercharger network to non-Tesla electric vehicles across North America, following successful pilot programs in Europe. The move comes after the adoption of the North American Charging Standard (NACS) by major automakers including Ford, GM, and Rivian. This expansion is expected to generate significant additional revenue through charging fees while strengthening Tesla\'s position in the EV infrastructure market. The company plans to add 10,000 new Supercharger stations globally by the end of next year.',
            'source': 'CNBC',
            'date': two_days_ago,
            'url': 'https://www.cnbc.com/tesla-supercharger-network-open'
        },
        {
            'title': 'Tesla Energy Division Posts Record Quarterly Growth',
            'content': 'Tesla\'s energy generation and storage division reported record revenue of $1.6 billion in Q2, up 74% year-over-year. Powerwall home battery installations doubled, while commercial Megapack deployments increased by 140%. During the earnings call, Elon Musk emphasized that Tesla Energy could eventually rival the automotive business in size, citing growing demand for renewable energy solutions worldwide. The company\'s energy storage products are now profitable on a standalone basis.',
            'source': 'Reuters',
            'date': yesterday,
            'url': 'https://www.reuters.com/tesla-energy-growth'
        },
        
        # Recent negative news
        {
            'title': 'Tesla Recalls 285,000 Vehicles in China Over Autopilot Safety Concerns',
            'content': 'Tesla is recalling approximately 285,000 Model 3 and Model Y vehicles in China due to safety risks associated with its Autopilot system. Chinese regulators identified issues where the driver assistance features could be activated accidentally, potentially leading to sudden acceleration. The recall will be conducted through an over-the-air software update, but has raised new questions about Tesla\'s testing procedures in its second-largest market. This marks the third major recall for Tesla in China this year.',
            'source': 'Wall Street Journal',
            'date': two_days_ago,
            'url': 'https://www.wsj.com/tesla-china-recall-autopilot'
        },
        {
            'title': 'Tesla Faces Production Delays for Cybertruck, Pushing Deliveries to Q4',
            'content': 'Tesla has confirmed that production ramp-up issues for the Cybertruck will delay mass deliveries until the fourth quarter of this year. The company cited challenges with the vehicle\'s unique exoskeleton design and new manufacturing techniques. Analysts have reduced their Cybertruck delivery estimates for the year from 75,000 to approximately 40,000 units. The delays have disappointed the more than 1.5 million reservation holders, some of whom have been waiting since the vehicle\'s announcement in 2019.',
            'source': 'Automotive News',
            'date': yesterday,
            'url': 'https://www.autonews.com/tesla-cybertruck-delays'
        },
        {
            'title': 'Tesla Stock Drops 8% Following Weaker-Than-Expected Profit Margins',
            'content': 'Tesla shares fell 8% after the company reported declining automotive gross margins for the third consecutive quarter. Despite strong delivery numbers, profit margins dropped to 18.2% from 25.1% a year earlier, primarily due to aggressive price cuts implemented to stimulate demand. CFO Zachary Kirkhorn warned that margins would remain under pressure as the company focuses on affordability and market share over short-term profitability. The company also faces increasing competition from Chinese manufacturers offering lower-priced electric vehicles.',
            'source': 'Financial Times',
            'date': two_days_ago,
            'url': 'https://www.ft.com/tesla-stock-margin-pressure'
        },
        
        # Older mixed news
        {
            'title': 'Tesla Launches New Model 3 Highland with Extended Range and Refreshed Interior',
            'content': 'Tesla has unveiled the refreshed Model 3, codenamed "Highland," featuring significant interior and exterior updates along with a range boost to 390 miles per charge. The redesign includes a streamlined dashboard, improved sound insulation, and new suspension components for a smoother ride. Industry observers note that this is the first major update to the Model 3 since its introduction in 2017. The Highland version will initially be available in China and Europe, with North American deliveries scheduled for early next quarter.',
            'source': 'Electrek',
            'date': last_week,
            'url': 'https://www.electrek.co/tesla-model3-highland'
        },
        {
            'title': 'Tesla\'s Full Self-Driving Beta Now Available to All North American Customers',
            'content': 'Tesla has removed the requirement for a minimum safety score to access its Full Self-Driving (FSD) Beta software, making it available to all customers in North America who purchased the FSD package. The version 11 update combines highway and city streets navigation into a single stack. While still requiring active driver supervision, early testers report significant improvements in the system\'s ability to navigate complex intersections and dense urban environments. Regulatory scrutiny remains a concern, with both NHTSA and the California DMV continuing their investigations into Tesla\'s autonomous driving claims.',
            'source': 'TechCrunch',
            'date': last_month,
            'url': 'https://www.techcrunch.com/tesla-fsd-beta-all-users'
        },
        {
            'title': 'Tesla Strikes Deal with BHP for Sustainable Nickel Supply',
            'content': 'Tesla has finalized a long-term agreement with mining giant BHP for the supply of nickel, a critical component in electric vehicle batteries. The deal includes environmental and Indigenous engagement requirements, with BHP committing to reduce carbon emissions in its mining operations. Tesla will receive nickel from BHP\'s operations in Western Australia, which are powered increasingly by renewable energy. This partnership aligns with Tesla\'s goal to secure sustainable battery materials as it scales production to meet growing global demand for electric vehicles.',
            'source': 'Mining Weekly',
            'date': last_month,
            'url': 'https://www.miningweekly.com/tesla-bhp-nickel-deal'
        },
        {
            'title': 'Elon Musk Announces Tesla AI Day, Promising Robotics and FSD Updates',
            'content': 'Tesla CEO Elon Musk has announced the date for the company\'s annual AI Day event, where he plans to showcase advances in the company\'s artificial intelligence and robotics programs. Expected highlights include updates on the humanoid robot project Optimus, improvements to the Full Self-Driving system, and details on Tesla\'s custom AI training computer Dojo. Musk teased that working prototypes of the Optimus robot would be demonstrated performing useful tasks. The event is positioned as both a technical showcase and a recruiting tool for AI and robotics talent.',
            'source': 'The Verge',
            'date': last_week,
            'url': 'https://www.theverge.com/tesla-ai-day-robotics'
        },
        {
            'title': 'Tesla Expands Solar Roof and Powerwall Installations to New Markets',
            'content': 'Tesla is expanding its energy products to five new international markets, offering its Solar Roof tiles and Powerwall home battery systems. The company has streamlined installation processes, reducing the average installation time by 40%. Tesla Energy has become increasingly important to the company\'s growth strategy, with Elon Musk previously stating that he expects the energy division to eventually grow faster than the automotive business. The expansion comes as many countries offer new incentives for residential solar and battery storage systems to reduce grid dependencies.',
            'source': 'CleanTechnica',
            'date': last_week,
            'url': 'https://www.cleantechnica.com/tesla-solar-expansion'
        }
    ] 