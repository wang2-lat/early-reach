from models import Product, Platform


class ContentGenerator:
    def generate_content(self, product: Product, platform: Platform, tone: str) -> str:
        templates = {
            Platform.PRODUCT_HUNT: self._product_hunt_template,
            Platform.REDDIT: self._reddit_template,
            Platform.TWITTER: self._twitter_template,
            Platform.HACKER_NEWS: self._hacker_news_template,
            Platform.INDIE_HACKERS: self._indie_hackers_template,
        }
        
        return templates[platform](product, tone)
    
    def _product_hunt_template(self, product: Product, tone: str) -> str:
        if tone == "professional":
            return f"""🚀 Launching {product.name}

{product.description}

We've built this to solve a real problem we faced ourselves. Would love to hear your thoughts and feedback!

🔗 {product.url or 'Coming soon'}

What features would you like to see next?"""
        else:
            return f"""Hey Product Hunt! 👋

Just launched {product.name} - {product.description}

Built this because I was frustrated with [problem]. Hope it helps you too!

Try it out: {product.url or 'Link in bio'}

Early feedback super welcome! What do you think?"""
    
    def _reddit_template(self, product: Product, tone: str) -> str:
        return f"""I built {product.name} to help with [specific problem]

Hey everyone! I'm an indie developer and I've been working on {product.name}.

**What it does:** {product.description}

**Why I built it:** [Your story here - be genuine]

**Current status:** Early beta, looking for feedback

I'd love to hear your thoughts! What would make this more useful for you?

{product.url or '[Link]'}

Happy to answer any questions!"""
    
    def _twitter_template(self, product: Product, tone: str) -> str:
        return f"""🚀 Just launched {product.name}!

{product.description}

Perfect for [target audience]. Early access available now.

{product.url or 'Link in bio'}

Feedback welcome! 🙏

#IndieHacker #BuildInPublic"""
    
    def _hacker_news_template(self, product: Product, tone: str) -> str:
        return f"""Show HN: {product.name} – {product.description}

Hi HN,

I built {product.name} to address [problem]. {product.description}

Technical details:
- [Stack/approach]
- [Key features]
- [What makes it different]

Looking for feedback on:
1. Product-market fit
2. Technical approach
3. Feature priorities

{product.url or 'Demo available'}

Happy to answer questions!"""
    
    def _indie_hackers_template(self, product: Product, tone: str) -> str:
        return f"""Launched {product.name} - Here's what I learned

Hey IH community!

Just launched {product.name}: {product.description}

**The Journey:**
- Started [timeframe] ago
- Built solo/with [team size]
- Tech stack: [your stack]

**Current metrics:**
- [Users/revenue/engagement]

**Biggest challenge:** [Be honest]

**What's next:** [Roadmap]

{product.url or 'Link'}

Would love your feedback and advice on growth strategies!"""
