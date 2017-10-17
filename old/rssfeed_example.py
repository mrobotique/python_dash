import feedparser as fp


url="https://weather.gc.ca/rss/battleboard/mb9_e.xml"
rss = fp.parse(url)

#print " Entries", len(rss.entries)

if (len(rss.entries)>0):
    print rss.entries[0]['title_detail']['value']
#    print rss.entries[0]['summary_detail']['value']
#    print rss.entries
