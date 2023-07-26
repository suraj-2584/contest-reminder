import nextcord,requests,datetime,asyncio
from nextcord.ext import commands
from nextcord import Embed, Color
intents=nextcord.Intents.default()
intents.message_content=True


bot= commands.Bot(command_prefix="!",intents=intents)
#/?username=suraj10&api_key=e6573c930785dcdecad6a7a18d3a48d5f1c9a31a
contests=[]

@commands.cooldown(1,5,commands.BucketType.user)
@bot.command(name="atcoder")
async def atcoderReply(ctx):
    found=False
    for obj in contests: 
        if obj["host"]=="atcoder.jp":
            await ctx.send(obj["href"])
            found=True
    if found==False: 
        await ctx.send("No atcoder contest for the next month :(")

@commands.cooldown(1,5,commands.BucketType.user)
@bot.command(name="codeforces")
async def codeforcesReply(ctx):
    found=False
    for obj in contests: 
        if obj["host"]=="codeforces.com":
            await ctx.send(obj["href"])
            found=True
    if found==False: 
        await ctx.send("No codeforces contest for the next month :(")

@commands.cooldown(1,5,commands.BucketType.user)
@bot.command(name="codechef")
async def codechefReply(ctx):
    found=False
    for obj in contests: 
        if obj["host"]=="codechef.com":
            await ctx.send(obj["href"])
            found=True
    if found==False: 
        await ctx.send("No codechef contest for the next month :(")

@commands.cooldown(1,5,commands.BucketType.user)
@bot.command(name="leetcode")
async def leetcodeReply(ctx):
    found=False
    for obj in contests: 
        if obj["host"]=="leetcode.com":
            await ctx.send(obj["href"])
            found=True
    if found==False: 
        await ctx.send("No leetcode contest for the next month :(")


@bot.event
async def on_ready(): 
    await fetchContests()
    await schedule_reminder()
    print(f"Logged in as: {bot.user.name}")

@bot.event
async def on_command_error(ctx,error): 
    if isinstance(error,commands.CommandOnCooldown): 
        em=Embed(title=f"Slow it down!",description=f"Try again in {error.retry_after:.2f}s",color=Color.red())
        await ctx.send(embed=em)

async def schedule_reminder(): 
    channel = bot.get_channel(1132900729221296188)
    now = datetime.datetime.now()
    for obj in contests:
        then =datetime.datetime.strptime(obj["start"],"%Y-%m-%dT%H:%M:%S")
        if then<now+datetime.timedelta(minutes=30):
            continue

        when = then-datetime.timedelta(minutes=30)
        wait_time=(when-datetime.datetime.now()).total_seconds()
        await asyncio.sleep(wait_time)
        await channel.send(f"Reminder! {obj['host']} contest starts in half an hour.\n{obj['href']}")


async def fetchContests(): 
    global contests
    response = requests.get("https://clist.by:443/api/v3/contest/?upcoming=true&username=suraj10&api_key=e6573c930785dcdecad6a7a18d3a48d5f1c9a31a")
    contests = response.json()["objects"]
    contests = sorted(contests,key=lambda obj: datetime.datetime.strptime(obj["start"],"%Y-%m-%dT%H:%M:%S"))
    #print(contests)


if __name__ == "__main__":
    bot.run("MTEzMjcyNTE1ODY3OTk0MTI5MA.Gh8toa.gjbMXE_mF3TXuHTQbsZaJry-PArJy7D7F4BENw")


