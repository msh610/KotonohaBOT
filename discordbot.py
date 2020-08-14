# インストールした discord.py を読み込む
import discord
import os
import sys
#import ffmpeg
from voiceroid import talkVOICEROID2
from voice_win import talkWin32
from voice_comtypes import talkComtypes
import mytoken

# 自分のBotのアクセストークンに置き換えてください
TOKEN = mytoken.TOKEN

# 接続に必要なオブジェクトを生成
client = discord.Client()

# 最大読み上げ時間
MAX_DURATION = 5

# 音声合成の種類
mode = "win32"

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('Success to login!')

async def join(message):
    """Botをボイスチャンネルに入室させます。"""
    voice_state = message.author.voice

    if (not voice_state) or (not voice_state.channel):
        #もし送信者がどこのチャンネルにも入っていないなら
        await message.channel.send("先にボイスチャンネルに入っている必要があります。")
        return

    channel = voice_state.channel #送信者のチャンネル

    await channel.connect()  #VoiceChannel.connect()を使用
    await message.channel.send(f'Join to {channel.name}')

async def leave(message):
    """Botをボイスチャンネルから切断します。"""
    voice_client = message.guild.voice_client

    if not voice_client:
        await message.channel.send("Botはこのサーバーのボイスチャンネルに参加していません。")
        return

    await voice_client.disconnect()
    await message.channel.send("Left from voice channel.")

async def talk(message):
    """Botが発言します。"""
    voice_client = message.guild.voice_client
    if not voice_client:
        return
    dirname = "tmpdata"
    os.makedirs(dirname, exist_ok=True)    
    voice_file = os.path.join(dirname, "voice.wav")
    global mode
    if mode == "win32":
        talkWin32(message.content, voice_file)
    #talkComtypes(message.content, voice_file)
    elif mode == "akane":
        talkVOICEROID2(message.content, voice_file)
    source = discord.FFmpegPCMAudio(voice_file, options=f"-t {MAX_DURATION}")
    voice_client.play(source)

async def help(message):
    """helpメッセージを表示します。"""
    help_message = [
        f"テキストチャンネルに投下されたチャットを読み上げます。(最大{MAX_DURATION}秒)",
        f"Usage：@KotonohaBOT [command]",
        "Command List",
        "\tjoin: メンションを送った人が滞在中のボイスチャンネルにBOTが入ります。",
        "\tleave: ボイスチャンネルにいるBOTが退出します。",
        "\tshut: BOTのプログラムを終了します。",
        "\takane: 読み手が琴葉茜になります",
        "\twin32: 読み手がMicrosoftのsayakaになります。",
        "\thelp: この文章が読める"
    ]
    await message.channel.send("\n".join(help_message))

async def shut(message):
    """Botをボイスチャンネルから切断し、ログアウトします。"""
    voice_client = message.guild.voice_client

    if voice_client:
        await voice_client.disconnect()

    await message.channel.send("Left from voice channel.")
    await message.channel.send(f"おやすみなさい！")
    await client.logout()


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    global mode
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    if client.user in message.mentions:  # 話しかけられたかの判定
        #print("recieve menthion " + message.content)
        if len(message.content.split()) < 2:
            await message.channel.send(f"\"@KotonohaBOT help\"でコマンド一覧が確認できます。")
            return
        command = message.content.split()[1]
        if command == ("join"):
            await join(message)  # ボイスチャンネル入室
        elif command == ("leave"):
            await leave(message)  # ボイスチャンネルから退出
        elif command == ("help"):
            await help(message)  # ヘルプメッセージを表示
        elif command == ("shut"):
            await shut(message)  # BOTを閉じる
        elif command == ("akane"):
            mode = "akane"
            await message.channel.send(f"読み手を琴葉茜に変更")
        elif command == ("win32"):
            mode = "win32"
            await message.channel.send(f"読み手をMicrosoft sayakaに変更")
        else:
            await message.channel.send(f"\"@KotonohaBOT help\"でコマンド一覧が確認できます。")
    else:
        await talk(message)

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN) 
