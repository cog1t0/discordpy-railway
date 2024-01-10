import discord
from discord.ext import commands
import openai  # OpenAIライブラリをインポート
from constant import TOKEN, OPENAI_API_KEY  # OPENAI_API_KEYもconstant.pyからインポート

extensions = (
)

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned,
            intents=discord.Intents.all(),
        )
        # OpenAIのAPIキーを設定
        openai.api_key = OPENAI_API_KEY

    async def setup_hook(self):
        for extension in extensions:
            await self.load_extension(f'extensions.{extension}')

    # メンションを受けた際の処理を追加
    async def on_message(self, message):
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "こんにちは。あなたは誰ですか？"},
            {"role": "assistant", "content": "私は AI アシスタントです。なにかお手伝いできることはありますか？"}
        ]
        if message.author.bot:  # ボット自体のメッセージは無視
            return
        if self.user.mentioned_in(message):  # Botへのメンションが含まれている場合
            content = message.content.replace(f'<@!{self.user.id}>', '')  # メンションを削除
            messages.append({"role": "user", "content": content.split('>')[1].lstrip()})
            # OpenAI APIを呼び出して応答を生成
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            await message.channel.send(completion.choices[0].message.content)  # 応答を送信

if __name__ == '__main__':
    MyBot().run(TOKEN)
