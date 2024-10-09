.. py:currentmodule:: waifuim



Quick Examples
==============

Here are some examples to get started.


Basic Example
-------------
This example shows how to use the client to search for images.

.. code-block:: python

    import asyncio

    import waifuim


    async def main():
        client = waifuim.Client(token="token", identifier="TestApp")

        # will return a list of Image objects with the tags "waifu" and "maid".
        images = await client.search(included_tags=["waifu", "maid"], multiple=True)
        for image in images:
            print(image.url)

        await client.close()

    asyncio.run(main())



Discord Bot Example
-------------------

.. code-block:: python

    # This example requires the discord.py 2.0 library.

    import discord
    import waifuim
    from discord.ext import commands


    intents = discord.Intents.default()
    intents.messages = True


    bot = commands.Bot(command_prefix="!", intents=intents)

    waifuim_client = waifuim.Client(token="token", identifier="MyDiscordBot")

    @bot.command()
    async def waifu(ctx: commands.Context, *tags: str):
        image = await waifuim_client.search(included_tags=tags)

        embed = discord.Embed(
            title="Waifu",
            description=f"{image.tags[0].description}",
            color=discord.Colour.from_str(image.dominant_color)
        )

        embed.set_image(url=image.url)
        embed.set_footer(text=f"Image ID: {image.id}")

        await ctx.send(embed=embed)

    bot.run("token")
