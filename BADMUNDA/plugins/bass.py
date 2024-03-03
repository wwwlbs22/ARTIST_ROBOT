from pyrogram import Client, filters
from pyrogram.types import Message
from pydub import AudioSegment
import os
import pydub
from BADMUNDA.bot_class import BAD


@BAD.on_message(filters.command("bass"))
async def bass_boost_command(client, message):
    try:
        # Check if there is a reply to the command
        if message.reply_to_message and message.reply_to_message.audio:
            original_audio = message.reply_to_message.audio
            file_id = original_audio.file_id

            # Download the audio file
            audio_path = await client.download_media(file_id)

            # Apply bass boost effect
            boosted_audio = apply_bass_boost(audio_path)

            # Send the boosted audio as a reply
            await message.reply_audio(audio=boosted_audio)

            # Clean up temporary files
            os.remove(audio_path)
            os.remove(boosted_audio)

        else:
            await message.reply_text("Please reply to an audio file with /bass to apply the bass boost effect.")
    except Exception as e:
        await message.reply_text(f"🚫")

def apply_bass_boost(audio_path):
    # Load audio file using pydub
    audio = AudioSegment.from_file(audio_path)

    # Apply bass boost effect (adjust the gain according to your preference)
    boosted_audio = audio.low_pass_filter(100).high_pass_filter(30).apply_gain(10)

    # Save the boosted audio as a temporary file
    boosted_audio_path = " ʙᴀss.mp3"
    boosted_audio.export(boosted_audio_path, format="mp3")

    return boosted_audio_path


@BAD.on_message(filters.command("loudly") & filters.reply)
async def download_and_enhance_audio(client, message):
    try:
        reply_message = message.reply_to_message

        if reply_message.audio:
            msg = await message.reply("processing")
            audio = await reply_message.download()
            audio_segment = pydub.AudioSegment.from_file(audio)
            await msg.edit("now adding loude audio and uploading...")
        
            louder_audio = audio_segment + 10
            
            louder_audio.export("chizuru.mp3", format="mp3")
            await msg.delete()
            await message.reply_audio("chizuru.mp3")
        else:
            await message.reply("The replied message is not an audio.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")




@BAD.on_message(filters.command("mono") & filters.reply)
async def split_stereo_and_send_audio(client, message):
    try:
        reply_message = message.reply_to_message

        if reply_message.audio:
            msg = await message.reply("processing")
            a = pydub.AudioSegment.from_file(await reply_message.download())
            b = a.split_to_mono()
            mono_audio = b[0]
            await msg.edit("now adding mono audio and uploading...")
            
            mono_audio.export("chizuru.mp3", format="mp3")
            await msg.delete()
            await message.reply_audio("chizuru.mp3")
        else:
            await message.reply("The replied message is not an audio.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
