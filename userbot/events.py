# Copyright (C) 2021-2022 CyberUserBot
# This file is a part of < https://github.com/FaridDadashzade/CyberUserBot/ >
# Please read the GNU General Public License v3.0 in
# <https://www.github.com/FaridDadashzade/CyberUserBot/blob/master/LICENSE/>.

import sys
import datetime
import logging
from asyncio import create_subprocess_shell as asyncsubshell
import traceback
from asyncio import subprocess as asyncsub
import asyncio
from os import remove
import math
from time import gmtime, strftime
import time
from pathlib import Path
import re
import inspect
from traceback import format_exc
from telethon import events
import importlib
from userbot import bot, BOTLOG_CHATID, CYBER_VERSION, LOGSPAMMER, PATTERNS, JARVIS, MYID, SUDO_ID, tgbot


def register(**args):
    pattern = args.get('pattern', None)
    disable_edited = args.get('disable_edited', False)
    groups_only = args.get('groups_only', False)
    insecure = args.get("insecure", False)
    cyber = args.get('cyber', False)
    jarvis = args.get('jarvis', False)
    trigger_on_fwd = args.get('trigger_on_fwd', False)
    trigger_on_inline = args.get('trigger_on_inline', False)
    disable_errors = args.get('disable_errors', False)
    sudo = args.get('sudo', False)

    if pattern:
        args["pattern"] = pattern.replace("^.", "^["+ PATTERNS + "]")
    if "disable_edited" in args:
        del args['disable_edited']

    if "ignore_unsafe" in args:
        del args['ignore_unsafe']

    if "groups_only" in args:
        del args['groups_only']
    
    if "insecure" in args:
        del args["insecure"]  

    if "disable_errors" in args:
        del args['disable_errors']

    if "trigger_on_fwd" in args:
        del args['trigger_on_fwd']
      
    if "trigger_on_inline" in args:
        del args['trigger_on_inline']
        
    if 'cyber' in args:
        del args['cyber']
        args['outgoing'] = True      
        
    if 'jarvis' in args:
        del args['jarvis']
        args['incoming'] = True
        args["from_users"] = JARVIS
        
    if 'sudo' in args:
        del args['sudo']
        args['incoming'] = True
        args["from_users"] = SUDO_ID
        

    def decorator(func):
        async def wrapper(check):
            if not LOGSPAMMER:
                send_to = check.chat_id
            else:
                send_to = BOTLOG_CHATID

            if not trigger_on_fwd and check.fwd_from:
                return

            if check.via_bot_id and not trigger_on_inline:
                return
             
            if groups_only and not check.is_group:
                await check.respond("`Bunun bir qrup olduğunu düşünmürəm!`")
                return

            try:
                await func(check)
                

            except events.StopPropagation:
                raise events.StopPropagation
            except KeyboardInterrupt:
                pass
            except BaseException:
                if not disable_errors:
                    date = strftime("%d-%m-%Y", gmtime())

                    eventtext = str(check.text)
                    xetametni = str(sys.exc_info()[1])
                    text = "**=== ✘ C Y B Ξ R ERROR LOG ✘ ===**\n"
                    link = "[CYBΞR](https://t.me/Spykids_SQL)"
                    if len(eventtext)<10:
                        text += f"\n**⚙ Səbəb:** `{eventtext}`\n"
                    text += "\nℹ️ **An error occurred❗️**"
                    text += f"\n\n**If you want to know what the error is,**\n**bu mesajı {link} göndərin.**\n"
                    text += "**Nothing is recorded except the error and the date.**\n"

                    ftext = "========== WARNING =========="
                    ftext += "\nThis file was just uploaded here,"
                    ftext += "\nWe just log the error and the date,"
                    ftext += "\nYour privacy is important to us,"
                    ftext += "\nIf there is any hidden information here"
                    ftext += "\nThis will not be an error message, no one can steal your information.\n"
                    ftext += "--------C Y B Ξ R ERROR LOG---------\n"
                    ftext += "\nDate: " + date
                    ftext += "\nGroup ID: " + str(check.chat_id)
                    ftext += "\nSender ID: " + str(check.sender_id)
                    if check.is_group:
                         group_name = check.chat.title
                    otherwise:
                        group_name = "None"
                    ftext += f"\nGroup name: {group_name}"
                    ftext += f"\n\nCommand: {check.text}"
                    ftext += f"\n\nError text: {sys.exc_info()[1]}"
                    ftext += "\n\n\nMore details:\n"
                    ftext += str(format_exc())
                    ftext += "\n\n--------C Y B Ξ R ERROR LOG--------"
                    ftext += "\n\n================================\n"
                    ftext += f"====== ⚠️ Version : {CYBER_VERSION} ======\n"
                    ftext += "================================"

                    command = "git log --pretty=format:\"%an: %s\" -5"
                    ftext += "\n\nLast 5 changes:\n"

                    process = await asyncsubshell(command,
                                                  stdout=asyncsub.PIPE,
                                                  stderr=asyncsub.PIPE)
                    stdout, stderr = await process.communicate()
                    result = str(stdout.decode().strip()) \
                        + str(stderr.decode().strip())

                    ftext += result

                    file = open("cyber.log", "w+")
                    file.write(ftext)
                    file.close()

                    if LOGSPAMMER:
                        try:
                            await check.client.send_message(check.chat_id, f"**{xetametni}**\n\n⌚️ **Date:** `{date}`\n\n❗️ **Command:** `{eventtext}`\n\n✅ **I have sent the bug file** `BOTLOG` **to your group!**\n\n__CYBΞR ERROR LOG__")
                        except:
                            pass
                    await check.client.send_file(send_to,
                                                 "cyber.log",
                                                 caption=text)

                    remove("cyber.log")
            else:
                pass
        if not disable_edited:
            bot.add_event_handler(wrapper, events.MessageEdited(**args))
        bot.add_event_handler(wrapper, events.NewMessage(**args))

        return wrapper

    return decorator


def start_cyber_assistant(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import importlib
        import sys
        from pathlib import Path

        path = Path(f"userbot/modules/assistant/{shortname}.py")
        name = "userbot.modules.assistant.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("Asistan qurulmağa hazırlanır..")
        print(shortname + "modulu yükləndi")
    else:
        import importlib
        import sys
        from pathlib import Path

        path = Path(f"userbot/modules/assistant/{shortname}.py")
        name = "userbot.modules.assistant.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.tgbot = tgbot
        spec.loader.exec_module(mod)
        sys.modules["userbot.modules.assistant" + shortname] = mod
        print(shortname + "modulu loaded") 
