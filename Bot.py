from CONFIG import *
from API import *

import requests

import botogram.objects.base
class InlineQuery(botogram.objects.base.BaseObject):
    required = {
        "id": str,
        "from": botogram.User,
        "query": str,
    }
    optional = {
        "location": botogram.Location,
        "offest": str,
    }
    replace_keys = {
        "from": "sender"
    }
botogram.Update.optional["inline_query"] = InlineQuery

import botogram
bot = botogram.create(TOKEN)

from pyshorteners import Shortener
google = Shortener('Google', api_key=GOOGLE_API_KEY)

@bot.before_processing
def start(chat, message):
    if message.text == "/users":
        return False

    add_user(message.sender.id)

    text = (
        "<b>Welcome!</b>"
        "\nWith this bot you can <b>short</b> any (valid) <b>URL</b> in the <b>web!</b>"
        "\nSimple use me <b>inline</b> in <b>any chat</b>!"
        "\n\n👤 <b>Developed by</b> @MarcoBuster"
        "\n👥 <b>Join in discussion group</b>: @MarcoBusterGroup"
        "\n🌐 <b>Source code</b>: <a href=\"github.com/MarcoBuster/ShortURLsBot\">GitHub, MIT license</a>"
    )
    bot.api.call("sendMessage", {
        "chat_id": chat.id, "text": text, "parse_mode": "HTML", "reply_markup":
            '{"inline_keyboard": ['
                '[{"text": "🚀 Try me!", "switch_inline_query": ""}]'
            ']}'
    })

    return True

def process_inline(bot, chains, update):
    update_id = update.inline_query.id
    sender = update.inline_query.sender
    query = update.inline_query.query

    add_user(sender.id)

    if query == "":
        bot.api.call("answerInlineQuery", {
                        "inline_query_id": update_id,
                        "cache_time": 300,
                        "results": '[{'+
                            '"type": "article",'+
                            '"id": "1",'+
                            '"title": "Welcome in Short URLs!",'+
                            '"thumb_url": "https://cdn2.iconfinder.com/data/icons/flat-icons-19/512/Sclssors.png",'+
                            '"description": "Simple write a link and I\'ll short it!",'+
                            '"input_message_content": {'+
                                '"message_text": "<b>Hello!</b>\nType in any chat <code>@ShortURLsBot URL</code> and <b>I\'ll short it!</b>",'+
                                '"parse_mode": "HTML"'+
                            '}, '+
                            '"reply_markup": {"inline_keyboard":'+
                                '[[{"text":"↩️ Retry", "switch_inline_query_current_chat": ""}]]'+
                            '}'+
                        '}]'
                })
        return

    url = query
    try:
        google = short('Google', url)
        tinyurl = short('Tinyurl', url)
        adfly = short('AdFly', url)
        isgd = short('Isgd', url)
        bitly = short('Bitly', url)
    except ValueError as e:
        bot.api.call("answerInlineQuery", {
                        "inline_query_id": update_id,
                        "cache_time": 300,
                        "results": '[{'+
                            '"type": "article",'+
                            '"id": "1",'+
                            '"title": "Invalid URL",'+
                            '"thumb_url": "http://icons.iconarchive.com/icons/paomedia/small-n-flat/1024/sign-error-icon.png",'+
                            '"description": "Please send a valid URL",'+
                            '"input_message_content": {'+
                                '"message_text": "<b>Invalid URL</b>\nType in any chat <code>@ShortURLsBot URL</code> and <b>I\'ll short it!</b>",'+
                                '"parse_mode": "HTML"'+
                            '}, '+
                            '"reply_markup": {"inline_keyboard":'+
                                '[[{"text":"↩️ Retry", "switch_inline_query_current_chat": ""}]]'+
                            '}'+
                        '}]'
                })
        return
    except requests.exceptions.ReadTimeout:
        bot.api.call("answerInlineQuery", {
                        "inline_query_id": update_id,
                        "cache_time": 0,
                        "results": '[{'+
                            '"type": "article",'+
                            '"id": "1",'+
                            '"title": "Timeout error",'+
                            '"thumb_url": "http://icons.iconarchive.com/icons/paomedia/small-n-flat/1024/sign-error-icon.png",'+
                            '"description": "Sorry, please try again later",'+
                            '"input_message_content": {'+
                                '"message_text": "<b>Timeout error</b>\nSorry, please try again later",'+
                                '"parse_mode": "HTML"'+
                            '}, '+
                            '"reply_markup": {"inline_keyboard":'+
                                '[[{"text":"↩️ Try again", "switch_inline_query_current_chat": ""}]]'+
                            '}'+
                        '}]'
                })
        return
    except:
        bot.api.call("answerInlineQuery", {
                        "inline_query_id": update_id,
                        "cache_time": 0,
                        "results": '[{'+
                            '"type": "article",'+
                            '"id": "1",'+
                            '"title": "Unknow",'+
                            '"thumb_url": "http://icons.iconarchive.com/icons/paomedia/small-n-flat/1024/sign-error-icon.png",'+
                            '"description": "Sorry, please try again later",'+
                            '"input_message_content": {'+
                                '"message_text": "<b>Unknow error</b>\nSorry, please try again later",'+
                                '"parse_mode": "HTML"'+
                            '}, '+
                            '"reply_markup": {"inline_keyboard":'+
                                '[[{"text":"↩️ Try again", "switch_inline_query_current_chat": ""}]]'+
                            '}'+
                        '}]'
                })
        return

    bot.api.call("answerInlineQuery", {
                    "inline_query_id": update_id,
                    "cache_time": 300,
                    "results": '[{'+
                        '"type": "article",'+
                        '"id": "1",'+
                        '"title": "Goo.gl",'+
                        '"thumb_url": "http://images.dailytech.com/nimage/G_is_For_Google_New_Logo_Thumb.png",'+
                        '"description": "'+google+'",'+
                        '"input_message_content": {'+
                            '"message_text": "<b>Shortened URL</b>: '+google+'",'+
                            '"parse_mode": "HTML"'+
                            '},'+
                        '"reply_markup": {"inline_keyboard":'+
                            '[[{"text": "🌐 Open URL", "url": "'+google+'"}]]'+
                        '}'+
                        '},'+
                        '{'+
                        '"type": "article",'+
                        '"id": "2",'+
                        '"title": "Tinyurl",'+
                        '"thumb_url": "http://blinklist.com/files/logos/tinyurl-logo.png",'+
                        '"description": "'+tinyurl+'",'+
                        '"input_message_content": {'+
                            '"message_text": "<b>Shortened URL</b>: '+tinyurl+'",'+
                            '"parse_mode": "HTML"'+
                            '},'+
                        '"reply_markup": {"inline_keyboard":'+
                            '[[{"text": "🌐 Open URL", "url": "'+tinyurl+'"}]]'+
                        '}'+
                        '},'+
                        '{'+
                        '"type": "article",'+
                        '"id": "3",'+
                        '"title": "AdfLy",'+
                        '"thumb_url": "https://az495088.vo.msecnd.net/app-logo/adfly_215.png",'+ # Wow, such URL, very secure
                        '"description": "'+adfly+'",'+
                        '"input_message_content": {'+
                            '"message_text": "<b>Shortened URL</b>: '+adfly+'",'+
                            '"parse_mode": "HTML"'+
                            '},'+
                        '"reply_markup": {"inline_keyboard":'+
                            '[[{"text": "🌐 Open URL", "url": "'+adfly+'"}]]'+
                        '}'+
                        '},'+
                        '{'+
                        '"type": "article",'+
                        '"id": "4",'+
                        '"title": "Isgd",'+
                        '"thumb_url": "https://is.gd/isgdlogo.jpg",'+
                        '"description": "'+isgd+'",'+
                        '"input_message_content": {'+
                            '"message_text": "<b>Shortened URL</b>: '+isgd+'",'+
                            '"parse_mode": "HTML"'+
                            '},'+
                        '"reply_markup": {"inline_keyboard":'+
                            '[[{"text": "🌐 Open URL", "url": "'+isgd+'"}]]'+
                        '}'+
                        '},'+
                        '{'+
                        '"type": "article",'+
                        '"id": "5",'+
                        '"title": "Bitly",'+
                        '"thumb_url": "http://www.dmuth.org/files/bitly-logo.jpg",'+
                        '"description": "'+bitly+'",'+
                        '"input_message_content": {'+
                            '"message_text": "<b>Shortened URL</b>: '+bitly+'",'+
                            '"parse_mode": "HTML"'+
                            '},'+
                        '"reply_markup": {"inline_keyboard":'+
                            '[[{"text": "🌐 Open URL", "url": "'+bitly+'"}]]'+
                        '}'+
                        '}'+
                    ']'
                })

bot.register_update_processor("inline_query", process_inline)

@bot.command("users")
def count(chat, message):
    if message.sender.id not in ADMINS:
        message.reply("<b>You aren't authorized to use this command</b>")
        return

    message.reply("<b>Users who started the bot</b>: {users}".format(users=count_users()))

if __name__ == "__main__":
    bot.run()
