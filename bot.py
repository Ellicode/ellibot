import os
import dotenv
import discord
from enum import Enum

dotenv.load_dotenv()

# This will load the permissions the bot has been granted in the previous configuration
intents = discord.Intents.default()
intents.message_content = True

class aclient(discord.Client):
  def __init__(self):
    super().__init__(intents = intents)
    self.synced = False # added to make sure that the command tree will be synced only once
    self.added = False

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced: #check if slash commands have been synced 
      await tree.sync(guild = discord.Object('1061280699379880077')) #guild specific: you can leave sync() blank to make it global. But it can take up to 24 hours, so test it in a specific guild.
      self.synced = True
    if not self.added:
      self.added = True
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="ellicode.com"))
    print(f"Say hi to {self.user}!")
    

client = aclient()
tree = discord.app_commands.CommandTree(client)

class ticket_view_2(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label='Close ticket', custom_id = "close_ticket_button", emoji = '✔️', style = discord.ButtonStyle.red)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user.name
        channel = interaction.channel
        await channel.delete()
        

class ticket_view(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label='Open ticket', custom_id = "open_ticket_button", emoji = '📬', style = discord.ButtonStyle.gray)
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user.name
        channel = interaction.channel
        thread = await channel.create_thread(name="ticket_" + user, type=discord.ChannelType.private_thread)
        tickembed = discord.Embed(
            color=discord.Color.blurple(),
            title="New ticket created",
            description="Thank you for reaching the staff. They will soon respond to you. You can now describe your problem."
        )
        server = interaction.message.guild
        role_id = '1061739063914279002'
        for role in server.roles:
            await interaction.channel.send(str(role.id)+ " / " + type(role.id))
            if role.id == role_id:
                break
            else:
                await interaction.response.send_message("Role doesn't exist")
                return
        for member in server.members:
            if role_id in member.roles:
                await thread.add_user(member)
        await thread.add_user(interaction.user)
        await thread.send(embed=tickembed,view=ticket_view_2())
        await interaction.response.send_message("A new ticket has been created successfully. Go to " + thread.mention,ephemeral=True)



panels = Enum(value='Panel', names=['TICKET', 'BLAH'])
@tree.command(description='Respond hello to you.', guild=discord.Object('1061280699379880077'))
async def panel(interaction: discord.Interaction, panel : panels):
    if interaction.user.guild_permissions.administrator:
        if panel.name == "TICKET" : 
            ticketembed = discord.Embed(
                title="Ticket",
                description="Click the button below to reach the support",
                color=discord.Color.blurple()
            )
            await interaction.channel.send(embed=ticketembed,view=ticket_view())
            await interaction.response.send_message("✅ Created panel", ephemeral=True)
    else:
        await interaction.response.send_message("⛔ Sorry, you don't have the required permissions to do this command.")


# add the token of your bot
client.run(os.getenv('TOKEN'))