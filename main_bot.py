# pip install discord.py
# pip install "discord.py[voice]" yt-dlp PyNaCl

# Windows
# winget install Gyan.FFmpeg

# Linux
# sudo apt install -y ffmpeg

import discord, os, sys, yt_dlp, asyncio, random
from discord import app_commands
from discord.ext import commands
from datetime import datetime, time

# 인텐트(권한) 설정
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

# 뻘짓
def error(text):
    return "[+] 에러!\n" + text
def success(text):
    return "[+] 성공!\n" + text

# 서버 아이디
server_id = 1546128396524847106

# 토큰 불러오기
def get_token():
    file_name = "Token.txt" # 토큰 파일 이름
    dir = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(dir, file_name)
    if not os.path.exists(dir): # 파일 없을 때
        print(error(f"[+] Token 파일 읽기 실패!\n[+] \"{file_name}\" 파일을 생성해주세요!"))
        sys.exit(1) # 프로그램 종료

    with open(dir, "r", encoding="utf=8") as f:
        token = f.read().strip()
    print(success(f"[+] Token 파일을 찾았습니다!"))

    if not token: # 파일 비었을 때
        print(error(f"[+] Token 파일이 비어있습니다!"))
        sys.exit(1)

    return token

# 봇 객체 생성
BOT = commands.Bot(command_prefix="메구밍", intents=intents)

# yt-dlp, FFmpeg 기본 옵션
YDL_OPTIONS = {
    'format': 'm4a/bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0'
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -filter:a "volume=1.0"'
}

# '간고등어'
ijun = 1547935249885962381 # 고유 아이디 보려면 프로필 우클릭하고 맨 아래 "사용자 ID 복사하기"
def IsIjun(userid):
    if userid == ijun:
        return True
    else:
        return False

# 봇 이벤트
@BOT.event
async def on_ready():
    print(success(f"[+] 로그인: {BOT.user.name} (ID: {BOT.user.id})"))
    
    # 슬래시 커맨드 동기화
    try:
        guild = discord.Object(id=server_id)
        BOT.tree.copy_global_to(guild=guild)
        synced = await BOT.tree.sync(guild=guild)
        print(success(f"[+] 슬래시 커맨드 {len(synced)}개 동기화 완료"))
    except Exception as e:
        print(error(f"[+] 동기화 에러: {e}"))

# 도움!
DoUm = "# 명령어들\
        \n\n## 채팅\
        \n* **메구밍도움** or **/메구밍도움**\
        \n `미쳐버린 메구밍봇의 도움말을 출력한닷!`\
        \n\n## 노래관련\
        \n* **메구밍노동요사용법**\
        \n `여기에 '메구밍노동요' 시리즈의 사용법이 모두 적혀있닷!`\
        \n* **메구밍노동요**\
        \n `미쳐버린 메구밍의 폭☆렬☆송을 튼닷!`\
        \n* **메구밍노동요일시정지**\
        \n `노동요를 일시정지한닷!`\
        \n* **메구밍노동요다시재생**\
        \n `노동요를 다시 재생한닷!`\
        \n* **메구밍노동요퇴장**\
        \n `미쳐버린 메구밍를 퇴장시킨닷!`\
        \n\n## 주의할점\
        \n* **미쳐버린 메구밍봇의 모든 명령어는 앞에 `메구밍`를 붙여야 한닷!**\
        \n* **딱히없다. 그냥 잘 쓰면 된닷!**\
        \n* **사용법에 큰따옴표(\")가 포함돼 있으면 붙여랏!**"

NoreDoUm = "# 노동요 재생 방법!\
            \n`메구밍노동요` : *미쳐버린 메구밍의 노동요*를 재생한닷!\
            \n\n## 노동요 멈추고 다시 재생하는 방법\
            \n`메구밍노동요일시정지` : 메구밍의 폭☆렬☆송을 멈춘닷!\
            \n`메구밍노동요다시재생` : 메구밍의 폭☆렬☆송을 다시 재생한닷!\
            \n# 봇 퇴장시키는 방법!\
            \n`메구밍노동요퇴장` : 메구밍을 퇴장시킨닷!\
            \n\n## **주의할점**\
            \n* 방에 들어가있어야지 봇이 들어가서 재생시킨닷!"

# 슬래시 명령어

# 도움
@BOT.tree.command(name="메구밍도움", description="도와줘요 메구밍!")
async def helpSlash(interaction: discord.Interaction):
    await interaction.response.send_message(DoUm)

# 느낌표명령어

# 채팅
@BOT.command(name="도움", description="도와줘요 메구밍!")
async def help_Megumin(ctx):
    await ctx.reply(DoUm)

# 음성
# 메구밍노동요사용법
@BOT.command(name="노동요사용법", description="미쳐버린 메구밍의 폭☆렬☆송 사용법을 출력한다.")
async def HowtoUsePlayTheSong(ctx):
    await ctx.reply(NoreDoUm)

# 메구밍노동요
@BOT.command(name="노동요", description="폭☆렬 폭☆렬!")
async def Megumin(ctx):
    if not ctx.author.voice:
        await ctx.reply("음성 채널에 들어가랏!")
        return

    channel = ctx.author.voice.channel
    voice_client = ctx.voice_client

    # 봇이 음성채널에 없으면 입장
    try:
        ctx.voice_client.pause() # 먼저 재생중이던 노래 멈추고 입장
    except:
        pass
    if not voice_client:
        voice_client = await channel.connect()
    elif voice_client.channel != channel:
        await voice_client.move_to(channel)

    # 노동요를 튼다.
    MeguminSong_dir = os.path.dirname(os.path.abspath (__file__))
    MeguminSong_dir = os.path.join(MeguminSong_dir, "Megumin.mp3")

    if not os.path.exists(MeguminSong_dir):
        await ctx.reply("에러! 제작자에게 문의해랏!")
        return

    # 재생 중이면 중지 후 새로 재생
    if voice_client.is_playing():
        voice_client.stop()

    def play_loop(error=None):
        if error:
            print(f"[-] 재생 에러!\n{error}")
            return
        if voice_client and voice_client.is_connected():
            source = discord.FFmpegPCMAudio(MeguminSong_dir)
            voice_client.play(source, after=play_loop)

    play_loop()
    
    await ctx.reply(f"미쳐버린 메구밍의 [폭☆렬☆송](https://www.youtube.com/watch?v=a0L8DClsF0M)을 재생한닷!")

# 일시정지
@BOT.command(name="노동요일시정지", description="폭☆렬☆송을 정지시킨닷!")
async def pause(ctx):
    if not ctx.author.voice:
        await ctx.reply("음성 채널에 들어가랏!")
        return
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.reply("ザ・ワールド！時よ止まれ！")

Megumin_Desa = ["黒より黒く 闇より暗き漆黒に 我が深紅の混淆を望みたもう\n覚醒のとき来たれり、無謬の境界に落ちし理\n無行の歪みとなりて、現出せよ！",
                "天変地異の奔流よ、我が呼びかけに応じ、今ひとたびその咆哮を轟かせよ！\n",
                "紅き魔力は、万象の崩壊を導く光\n終焉の調べを奏でよ、森羅万象を覆す力をもって！",
                "紅蓮の炎に抱かれし、万物を灰燼と化す絶対の力\n万象を灰燼に帰す、究極の破壊を今ここに！",
                "深淵なる闇の底より、焦土を焦がす劫火を召喚せん\nすべてを無に帰す、灼熱の閃光となりて！",
                "暗黒の彼方より、虚無の彼方より、深淵の呼び声に応えよ...\n赤き波動は、森羅万象を滅ぼす業火なり\n我が求めに応じ、万物を呑み込む焔となれ！",
                "我が名に賭けて、我が深紅の炎に命ずる\n無窮の深淵より現れし、破滅の化身よ\n今ここに、我が力の証を示せ！",
                "光に覆われし漆黒よ、夜を纏いし爆炎よ\n紅魔の名のもとに、原初の崩壊を顕現せよ！\n終焉の王たる我が力、見よ！",
                "我は求む、我が身を焦がすほどの熱き力を\n紅魔随一の天才魔法使い、めぐみんの名のもとに！\n理を砕き、世界を赤く染め上げよ！",
                "偽りの平穏を打ち砕く、真紅の雷撃よ\n我が咆哮に応え、滅びの雨を降らせたまえ！"]

# 다시재생
@BOT.command(name="노동요다시재생", description="정지시킨 폭☆렬☆송을 다시 재생시킨닷!")
async def resume(ctx):
    if not ctx.author.voice:
        await ctx.reply("음성 채널에 들어가랏!")
        return
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        n = random.randint(0, len(Megumin_Desa) - 1)
        await ctx.reply(f"{random.choice(Megumin_Desa)}\n{n}\n# エクスプロージョン！")

# 퇴장
@BOT.command(name="노동요퇴장", description="광메봇을 퇴장시킨닷!")
async def leave(ctx):
    if not ctx.author.voice:
        await ctx.reply("음성 채널에 들어가랏!")
        return
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.reply("퇴장한닷!")
    else:
        await ctx.reply("퇴장 불가능하닷!")

TOKEN = get_token()
BOT.run(TOKEN)