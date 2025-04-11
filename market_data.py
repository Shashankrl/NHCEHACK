"""
Comprehensive Market Dataset for FundWise NLP Testing
This module provides a collection of financial news articles covering
multiple companies, sectors, and market trends for testing.
"""
from datetime import datetime, timedelta

def get_market_articles():
    """Return a comprehensive collection of market news articles"""
    
    # Calculate dates for relative timestamps
    today = datetime.now()
    yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    two_days_ago = (today - timedelta(days=2)).strftime('%Y-%m-%d')
    last_week = (today - timedelta(days=7)).strftime('%Y-%m-%d')
    last_month = (today - timedelta(days=30)).strftime('%Y-%m-%d')
    
    return [
        # APPLE (AAPL) News
        {
            'title': 'Apple\'s iPhone 16 Pre-orders Break Records in Key Markets',
            'content': 'Pre-orders for Apple\'s new iPhone 16 lineup have exceeded expectations, with sales tracking 15% higher than the iPhone 15 launch last year. The company\'s decision to emphasize AI capabilities with Apple Intelligence has resonated with consumers, particularly in premium models. Analysts have raised their shipment forecasts for the quarter and several have upgraded their price targets for AAPL. Supply chain sources indicate Apple has requested suppliers to increase production capacity to meet the stronger-than-expected demand.',
            'source': 'Bloomberg',
            'date': yesterday,
            'url': 'https://www.bloomberg.com/news/apple-iphone16-preorder-records'
        },
        {
            'title': 'Apple Faces European Antitrust Challenges Over App Store Policies',
            'content': 'European regulators have announced new investigations into Apple\'s compliance with the Digital Markets Act (DMA). The scrutiny focuses on the company\'s App Store commission structure and restrictions on developers directing users to alternative payment methods. The potential fines could reach up to 10% of Apple\'s global annual revenue if found in violation. This represents the latest chapter in the ongoing regulatory challenges faced by the tech giant in Europe, which has already been hit with over €1.8 billion in fines this year.',
            'source': 'Financial Times',
            'date': two_days_ago,
            'url': 'https://www.ft.com/apple-eu-antitrust-challenges'
        },
        
        # MICROSOFT (MSFT) News
        {
            'title': 'Microsoft Cloud Revenue Jumps 35% as AI Investments Pay Off',
            'content': 'Microsoft reported quarterly earnings that significantly exceeded analyst expectations, with cloud revenue growing 35% year-over-year. Azure\'s AI services were highlighted as the primary growth driver, accounting for 8 percentage points of Azure\'s growth. CEO Satya Nadella emphasized that Copilot and other AI offerings are seeing rapid enterprise adoption, with over 60% of Fortune 500 companies now using Microsoft\'s AI services. The company raised its full-year growth outlook for its cloud segment, sending shares up in after-hours trading.',
            'source': 'CNBC',
            'date': yesterday,
            'url': 'https://www.cnbc.com/microsoft-cloud-growth-ai'
        },
        {
            'title': 'Microsoft Expands Gaming Portfolio with New Studio Acquisitions',
            'content': 'Following its successful acquisition of Activision Blizzard, Microsoft has announced the purchase of two additional gaming studios to bolster its Game Pass subscription service. These strategic moves further strengthen Microsoft\'s gaming division, which reported a 22% revenue increase last quarter. Xbox Game Pass subscribers have now surpassed 30 million, according to the company\'s latest figures. The gaming subscription service has become an increasingly important part of Microsoft\'s consumer strategy as it competes with Sony\'s PlayStation platform.',
            'source': 'The Verge',
            'date': last_week,
            'url': 'https://www.theverge.com/microsoft-gaming-acquisitions'
        },
        
        # AMAZON (AMZN) News
        {
            'title': 'Amazon Web Services Unveils New AI Infrastructure Services',
            'content': 'Amazon Web Services (AWS) has introduced a new suite of AI infrastructure services designed to help companies build and deploy custom large language models. The offering includes specialized instances powered by NVIDIA\'s latest H200 GPUs and software tools for efficient model training. AWS CEO Adam Selipsky claimed the new services can reduce AI training costs by up to 40% compared to competing platforms. The announcement comes as AWS faces increasing competition from Microsoft Azure and Google Cloud in the rapidly growing AI infrastructure market.',
            'source': 'TechCrunch',
            'date': yesterday,
            'url': 'https://techcrunch.com/aws-ai-infrastructure'
        },
        {
            'title': 'Amazon Expands Same-Day Delivery Network with Mini-Fulfillment Centers',
            'content': 'Amazon is expanding its same-day delivery capabilities with dozens of new mini-fulfillment centers across North America. These smaller facilities, located closer to urban centers, enable delivery times as short as two hours for Prime members. The company reported that same-day deliveries have increased by 65% year-over-year as consumers increasingly expect faster shipping. The expansion represents part of Amazon\'s $20 billion investment in logistics infrastructure announced earlier this year to maintain its competitive edge against Walmart and other retailers.',
            'source': 'Reuters',
            'date': two_days_ago,
            'url': 'https://www.reuters.com/amazon-same-day-delivery'
        },
        
        # NVIDIA (NVDA) News
        {
            'title': 'NVIDIA Unveils Next-Generation Blackwell AI Chips with 2.5x Performance Gain',
            'content': 'NVIDIA has officially launched its next-generation Blackwell GPU architecture, delivering performance up to 2.5 times faster than its predecessor while using 25% less power. CEO Jensen Huang announced that the new chips are already in full production, with major cloud providers and AI companies receiving the first shipments. The company reported that demand continues to outstrip supply, with the global waitlist for its AI chips extending well into next year. Analysts project that the new chips could generate over $50 billion in revenue in the first year of availability.',
            'source': 'Wall Street Journal',
            'date': yesterday,
            'url': 'https://www.wsj.com/nvidia-blackwell-launch'
        },
        {
            'title': 'NVIDIA Partners with Leading Automakers for Autonomous Driving Platform',
            'content': 'NVIDIA has announced partnerships with five major global automakers to implement its DRIVE Thor autonomous vehicle computing platform. The system-on-chip combines autonomous driving capabilities with in-vehicle AI features and is scheduled for production in 2026 model year vehicles. This expansion of NVIDIA\'s automotive business represents a significant diversification beyond its core data center and gaming segments. The automotive division grew 125% year-over-year, though it still represents less than 5% of the company\'s total revenue.',
            'source': 'Automotive News',
            'date': last_week,
            'url': 'https://www.autonews.com/nvidia-automaker-partnerships'
        },
        
        # GOOGLE/ALPHABET (GOOGL) News
        {
            'title': 'Google Search Overhaul Integrates Gemini AI Across Core Products',
            'content': 'Google has launched its most significant search redesign in years, deeply integrating its Gemini AI model throughout the search experience. The update provides more conversational responses, multimodal understanding of images and text, and personalized search features. Early metrics show increased user engagement with the new AI features, though some advertisers have expressed concerns about the potential impact on traditional search ads. The company emphasized that the changes represent an evolution rather than a replacement of its core search functionality.',
            'source': 'The Information',
            'date': yesterday,
            'url': 'https://www.theinformation.com/google-search-gemini-integration'
        },
        {
            'title': 'Google Cloud Grows Market Share Against AWS and Azure',
            'content': 'Google Cloud Platform has reported its highest quarterly market share gain in three years, capturing 12.5% of the global cloud infrastructure market according to industry analysts. While still trailing Amazon Web Services and Microsoft Azure, Google\'s cloud division has now posted seven consecutive profitable quarters. The division\'s success has been attributed to its AI infrastructure offerings and vertical-specific solutions for industries like healthcare and financial services. Parent company Alphabet highlighted cloud as its fastest-growing segment in its latest earnings report.',
            'source': 'CNBC',
            'date': two_days_ago,
            'url': 'https://www.cnbc.com/google-cloud-market-share-gain'
        },
        
        # META (META) News
        {
            'title': 'Meta\'s AI Assistant Reaches 500 Million Monthly Users',
            'content': 'Meta announced that its AI assistant has reached 500 million monthly active users across Facebook, Instagram, WhatsApp, and Messenger. CEO Mark Zuckerberg highlighted that the assistant now handles over 1 billion queries daily, making it one of the most widely used AI products globally. The company also reported that its open-source Llama 3 model has been downloaded over 150 million times by developers and researchers. These milestones underscore Meta\'s successful pivot to AI after years of heavy investment in its metaverse vision.',
            'source': 'Wired',
            'date': yesterday,
            'url': 'https://www.wired.com/meta-ai-assistant-milestone'
        },
        {
            'title': 'Meta Faces Headwinds in European Ad Business Due to Privacy Regulations',
            'content': 'Meta is encountering challenges in its European advertising business due to increasingly strict privacy regulations and the rollout of Apple\'s App Tracking Transparency feature. Internal documents reveal that European ad revenue growth has slowed to single digits, compared to double-digit growth in North America and Asia. The company has been developing new privacy-preserving ad measurement tools, but advertisers report these alternatives provide less precise targeting capabilities. Analysts estimate the impact could reduce Meta\'s annual European revenue by approximately $2-3 billion.',
            'source': 'Bloomberg',
            'date': last_week,
            'url': 'https://www.bloomberg.com/meta-european-ad-challenges'
        },
        
        # Market Trends & Sector News
        {
            'title': 'Fed Signals Interest Rate Cuts as Inflation Eases',
            'content': 'The Federal Reserve has signaled a shift toward interest rate cuts after inflation data showed continued moderation. The central bank\'s latest meeting minutes revealed growing comfort among officials with the inflation trajectory. Market participants are now pricing in two quarter-point cuts by year-end. Bond yields fell on the news while stock indexes rose, particularly benefiting growth and technology sectors. Economists note that this potential loosening of monetary policy comes as the labor market shows signs of cooling without a dramatic rise in unemployment.',
            'source': 'Wall Street Journal',
            'date': yesterday,
            'url': 'https://www.wsj.com/fed-interest-rate-cuts-inflation'
        },
        {
            'title': 'Semiconductor Sector Faces Supply Chain Disruptions from Taiwan Tensions',
            'content': 'The global semiconductor industry is experiencing heightened supply chain concerns amid increased geopolitical tensions involving Taiwan. Several major chipmakers have accelerated contingency plans, including diversifying manufacturing locations and building resilience through inventory management. Analysts warn that prolonged disruptions could impact everything from smartphones to automobiles, potentially creating shortages similar to those experienced during the pandemic. Industry association SEMI has called for international cooperation to ensure semiconductor supply chain stability, which underpins approximately $7 trillion of global economic activity.',
            'source': 'Financial Times',
            'date': two_days_ago,
            'url': 'https://www.ft.com/semiconductor-taiwan-tensions'
        },
        {
            'title': 'AI Startup Funding Reaches Record High Despite Overall VC Slowdown',
            'content': 'Venture capital funding for artificial intelligence startups has reached an all-time quarterly high of $25.2 billion, despite an overall slowdown in the broader VC landscape. The funding surge has been concentrated in mature AI companies, with five mega-rounds of over $500 million each. Early-stage AI startups are facing more challenging fundraising conditions as investors become more selective. The divergence highlights the "barbell effect" in AI investing, with capital flowing primarily to industry leaders and very early proof-of-concept companies, while mid-stage startups face a more competitive environment.',
            'source': 'TechCrunch',
            'date': last_week,
            'url': 'https://www.techcrunch.com/ai-startup-funding-record'
        },
        {
            'title': 'Oil Prices Drop as OPEC+ Announces Production Increase',
            'content': 'Oil prices fell sharply after OPEC+ announced plans to gradually increase production starting next month. Brent crude dropped below $75 per barrel for the first time in three months on the news. The decision comes as global oil demand forecasts have been revised downward due to slowing economic growth in China and persistent inflation in Western economies. Energy sector stocks declined following the announcement, with major oil companies like Exxon Mobil, Chevron, and BP all trading lower. Analysts note that the production increase could create a supply surplus if demand continues to weaken.',
            'source': 'Reuters',
            'date': yesterday,
            'url': 'https://www.reuters.com/oil-prices-opec-production'
        }
    ] 