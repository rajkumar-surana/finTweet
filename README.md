# finTweet
financial smart analysis of popular tweets

Rough Idea:#System Prompt#

Hey my use case is that I want to give you my credentials for Twitter. You have to keep monitoring the posts or replies of all the people I follow. They will post images, text, videos, etc. You have to keep track of sectors/stocks/industry/commodity timeline of what different folks talked about related to that.

This way you keep adding and building to existing timelines of each sector and what each person talked about.


Any questions you have in building this system, you will ask without hesitating and you will make tech decisions as per best of your knowledge. You will use the ChatGPT API to process each post/reply, including images, and make notes in a DB, and create an interactive dashboard for the user to see the most hyped/talked about stock/sector/industry/macro/commodity on a daily, weekly, and monthly basis.

1. Use official Twitter documentation. I will see how to get keys, etc. Use GPT for direct analysis of the posts of people I follow. Use Vision GPT wherever necessary. We will only be consuming images and textual info for now, no video.
2. You can add new topics/categories as you see fit. Create your prompt accordingly and don't do duplication, so use RAG or whatever necessary to see if there is something existing.
3. Web-based dashboard sounds good.
4. Filters are nice to have on date range and author but everything would be based on topics they are the main thing.
5. add sort by mentions+/- that will tells us about the hype, so give bullish, bearish, contradictory tags as per sentiments overall on daily, weekly basis
6. it should update every hour use whatever storage you think would do better, as you may know each hour we take update from different topics and then we update our view on the basis of new info
7. use whatever gpt model you see would work best
