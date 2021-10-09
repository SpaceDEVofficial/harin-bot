import io
import asyncio
from PycordPaginator import Paginator
import aiosqlite
import discord
from discord.ext import commands
import discordSuperUtils
class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ImageManager = discordSuperUtils.ImageManager()

    @commands.command(name="도움",aliases=["도움말","help"])
    async def help(self,ctx):
        main = discord.Embed(
            title="메인페이지",
            description="""
안녕하세요! 하린봇을 이용해주셔서 감사드립니다.

도움말 목차는 아래와 같아요!

< 목차 >
• 1페이지 - 메인페이지
• 2페이지 - 서버 관리 ⚖
• 3페이지 - 도구 🧰
• 4페이지 - 뮤직 🎶
• 5페이지 - 생일 🎉
• 6페이지 - 템플릿 🧩
""",
            colour=discord.Colour.random()
        )
        main.set_thumbnail(url=self.bot.user.avatar_url)
        main.set_image(url="https://media.discordapp.net/attachments/889514827905630290/896359450544308244/37cae031dc5a6c40.png")
        main.set_footer(text="1 / 6페이지",icon_url=ctx.author.avatar_url)

        manage = discord.Embed(
            title="서버 관리 ⚖",
            description="""
이곳에서 서버 관리 명령어를 확인해보세요!            
""",
            colour=discord.Colour.random()
        )
        manage.add_field(name="하린아 처벌 @유저",
                         value="```\n지정한 유저의 처벌기록을 보여드려요.\n```",
                         inline=False)
        manage.add_field(name="하린아 처벌 조회 @유저 처벌ID",
                         value="```\n지정한 유저의 처벌ID에 해당하는 기록을 보여드려요.\n```",
                         inline=False)
        manage.add_field(name="하린아 처벌 추가 @유저 (사유)",
                         value="```\n지정한 유저에게 경고를 부여해요. 사유는 선택사항이에요.\n```",
                         inline=False)
        manage.add_field(name="하린아 처벌 취소 @유저 처벌ID (사유)",
                         value="```\n지정한 유저에게 부여된 경고를 취소해요. 사유는 선택사항이에요.\n```",
                         inline=False)
        manage.add_field(name="하린아 뮤트 @유저 시간|0d0h0m0s (사유)",
                         value="```\n지정한 유저에게 뮤트를 설정한 시간동안 부여해요. 사유는 선택사항이에요.\n```",
                         inline=False)
        manage.add_field(name="하린아 언뮤트 @유저 (사유)",
                         value="```\n지정한 유저에게 부여된 뮤트를 취소해요. 사유는 선택사항이에요.\n```",
                         inline=False)
        manage.add_field(name="하린아 밴 @유저 시간|0d0h0m0s (사유)",
                         value="```\n지정한 유저를 밴하여 설정한 시간후에 언밴해요. 사유는 선택사항이에요.\n```",
                         inline=False)
        manage.add_field(name="하린아 언밴 @유저 (사유)",
                         value="```\n지정한 유저에게 부여된 뮤트를 취소해요. 사유는 선택사항이에요.\n```",
                         inline=False)
        manage.add_field(name="하린아 청소 갯수",
                         value="```\n지정한 갯수만큼 메세지를 지워요. 최대갯수는 99개에요.\n```",
                         inline=False)
        manage.set_footer(text="2 / 6페이지",icon_url=ctx.author.avatar_url)

        util = discord.Embed(
            title="도구 🧰",
            description="""
        이곳에서 도구 관련 명령어를 확인해보세요!            
        """,
            colour=discord.Colour.random()
        )
        util.add_field(
            name="하린아 [옵션 or 설정]",
            value="```\n여러 기능을 설정할 수 있는 명령어에요!\n```",
            inline=False
        )
        util.add_field(
            name="하린아 프사 (@유저)",
            value="```\n유저를 지정하거나 하지않으면 자신의 프로필 사진을 불러와요!\n```",
            inline=False
        )
        util.add_field(
            name="하린아 서버정보",
            value="```\n명령어를 실행한 서버의 정보를 불러와요!\n```",
            inline=False
        )
        util.add_field(
            name="하린아 봇정보",
            value="```\n제 정보를 보여드려요!\n```",
            inline=False
        )
        util.add_field(
            name="하린아 [랭크 or 레벨] (@user)",
            value="```\n지정한 유저 혹은 자신의 레벨카드를 보여드려요.\n```",
            inline=False
        )
        util.add_field(
            name="하린아 리더보드",
            value="```\n현재 길드의 레벨순위정보판을 보여드려요.\n```",
            inline=False
        )
        util.add_field(
            name="하린아 초대정보 (@user)",
            value="```\n지정한 유저 혹은 자신의 초대정보를 보여줘요.\n```",
            inline=False
        )
        util.set_footer(text="3 / 6페이지",icon_url=ctx.author.avatar_url)

        music = discord.Embed(
            title="뮤직 🎶",
            description="""
                이곳에서 노래 관련 명령어를 확인해보세요!            
                """,
            colour=discord.Colour.random()
        )
        music.add_field(
            name="하린아 들어와",
            value="```\n현재 접속한 음성채널에 접속해요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 재생 인자값",
            value="```\n입력한 인자값(제목 또는 링크)을 불러와 재생해요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 가사",
            value="```\n현재 재생중인 곡의 가사를 불러와요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 지금곡",
            value="```\n현재 재생중인 노래의 정보를 불러와요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 일시정지",
            value="```\n현재 재생중인 곡을 일시정지해요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 이어재생",
            value="```\n일시정지된 곡을 이어서 재생해요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 볼륨 (설정할볼륨)",
            value="```\n설정할 볼륨으로 볼륨을 조절해요. 입력하지 않으면 현재 볼륨을 보여줘요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 루프",
            value="```\n반복기능을 활성화하거나 비활성화해요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 큐루프",
            value="```\n큐반복기능을 활성화하거나 비활성화해요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 노래기록",
            value="```\n지금까지 재생됐던 노래기록을 불러와요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 정지",
            value="```\n현재 재생중인 곡을 완전히 정지해요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 스킵",
            value="```\n현재 재생중인 곡을 스킵하거나 요청해요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 큐",
            value="```\n현재 대기중인 큐목록을 보여줘요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 반복확인",
            value="```\n현재 설정된 반복상태를 보여줘요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 셔플",
            value="```\n셔플기능을 활성화하거나 비활성화해요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 자동재생",
            value="```\n자동재생기능을 활성화하거나 비활성화해요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 이전곡",
            value="```\n이전곡을 재생해요.\n```",
            inline=False
        )
        music.add_field(
            name="하린아 나가",
            value="```\n현재 접속한 음성채널에서 노래를 멈추고 나가요.\n```",
            inline=False
        )
        music.set_footer(text="4 / 6페이지",icon_url=ctx.author.avatar_url)

        birthday = discord.Embed(
            title="생일 🎉",
            description="""
                이곳에서 생일 관련 명령어를 확인해보세요!            
                """,
            colour=discord.Colour.random()
        )
        birthday.add_field(
            name="하린아 생일등록",
            value="```\n자신의 생일을 등록해요.\n```",
            inline=False
        )
        birthday.add_field(
            name="하린아 생일삭제",
            value="```\n등록된 자신의 생일을 삭제해요.\n```",
            inline=False
        )
        birthday.add_field(
            name="하린아 생일목록",
            value="```\n현재길드에 등록된 멤버들의 생일을 보여줘요.\n```",
            inline=False
        )
        birthday.set_footer(text="5 / 6페이지",icon_url=ctx.author.avatar_url)

        template = discord.Embed(
            title="템플릿 🧩",
            description="""
                        이곳에서 템플릿 관련 명령어를 확인해보세요!            
                        """,
            colour=discord.Colour.random()
        )
        template.add_field(
            name="하린아 템플릿사용 템플릿ID",
            value="```\n입력한 ID의 템플릿을 사용해요.어드민 권한이 있어야해요.\n```",
            inline=False
        )
        template.add_field(
            name="하린아 템플릿삭제 템플릿ID",
            value="```\n입력한 ID의 템플릿을 삭제해요.어드민 권한이 있어야해요.\n```",
            inline=False
        )
        template.add_field(
            name="하린아 템플릿목록",
            value="```\n저장된 템플릿 목록을 불러와요.\n```",
            inline=False
        )
        template.add_field(
            name="하린아 템플릿찾기 (템플릿ID)",
            value="```\n입력한 ID 혹은 현재길드의 템플릿을 불러와요.\n```",
            inline=False
        )
        template.add_field(
            name="하린아 템플릿등록",
            value="```\n현재 길드를 템플릿화해요.어드민 권한이 있어야해요.\n```",
            inline=False
        )
        template.set_footer(text="6 / 6페이지",icon_url=ctx.author.avatar_url)

        embeds = [main,manage,util,music,birthday,template]
        desc = {
            "메인 페이지": "목차가 있는 메인페이지",
            "서버 관리": "서버 관리 명령어가 있는 페이지.",
            "도구":"간편히 사용할 수 있는 명령어가 있는 페이지.",
            "뮤직":"노래 명령어가 있는 페이지.",
            "생일": "생일 명령어가 있는 페이지.",
            "템플릿":"템플릿 명령어가 있는 페이지."
        }
        e = Paginator(
            client=self.bot.components_manager,
            embeds=embeds,
            channel=ctx.channel,
            only=ctx.author,
            ctx=ctx,
            use_select=True,
            desc=desc)
        await e.start()

def setup(bot):
    bot.add_cog(general(bot))
