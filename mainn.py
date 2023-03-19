import asyncio
import aiohttp
from bs4 import BeautifulSoup

async def monitoring():
    async with aiohttp.ClientSession() as sess:
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Atom/13.0.0.44 Safari/537.36'}
        while True:
            a=await sess.get("https://ru.investing.com/crypto/ethereum/eth-usd",headers=header)
            a=BeautifulSoup(await a.text(),"lxml")
            eth=a.find("span",class_="text-2xl").text.replace(".","").replace(",",".")
            await asyncio.sleep(3600)
            a=await sess.get("https://ru.investing.com/crypto/ethereum/eth-usd",headers=header)
            a=BeautifulSoup(await a.text(),"lxml")
            eth1=a.find("span",class_="text-2xl").text.replace(".","").replace(",",".")
            if abs(float(eth1)-float(eth))/float(eth)*100>=1:
                print(f"ETH: old:{eth} new: {eth1}\nEdit: "+str(abs(float(eth1)-float(eth))/float(eth)*100)+"%")
asyncio.run(monitoring())