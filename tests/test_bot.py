"""
Unit tests for the Telegram bot handlers.

All Telegram API calls are mocked so no network access is required.
Run with:  pytest tests/ -v --cov=bot --cov-report=term-missing
"""

import random
import types as builtin_types
import unittest
from unittest.mock import MagicMock, mock_open, patch


# ---------------------------------------------------------------------------
# Helpers to build lightweight mock objects that look like pyTelegramBotAPI
# types without importing the real library.
# ---------------------------------------------------------------------------

def _make_chat(chat_type='private', chat_id=12345):
    chat = MagicMock()
    chat.id = chat_id
    chat.type = chat_type
    return chat


def _make_user(first_name='Alice', user_id=1):
    user = MagicMock()
    user.first_name = first_name
    user.id = user_id
    return user


def _make_message(text='', chat_type='private', chat_id=12345):
    msg = MagicMock()
    msg.chat = _make_chat(chat_type=chat_type, chat_id=chat_id)
    msg.from_user = _make_user()
    msg.text = text
    msg.message_id = 99
    return msg


def _make_call(data='good', chat_id=12345, message_id=99):
    call = MagicMock()
    call.data = data
    call.id = 'callback_id_1'
    call.message = _make_message(chat_id=chat_id)
    call.message.message_id = message_id
    return call


# ---------------------------------------------------------------------------
# Fixtures / module-level patching
# ---------------------------------------------------------------------------

# We patch config and telebot *before* importing bot so that bot.py can be
# imported without a real Telegram token or the pyTelegramBotAPI package.
import sys

_mock_config = MagicMock()
_mock_config.TOKEN = 'FAKE_TOKEN_FOR_TESTING'
sys.modules.setdefault('config', _mock_config)

_mock_telebot_module = MagicMock()
_mock_telebot_module.TeleBot.return_value = MagicMock()
sys.modules.setdefault('telebot', _mock_telebot_module)
sys.modules.setdefault('telebot.types', MagicMock())

import bot  # noqa: E402  (import after mocking)


# ---------------------------------------------------------------------------
# Tests: /start handler (welcome)
# ---------------------------------------------------------------------------

class TestWelcomeHandler(unittest.TestCase):
    """Tests for the /start command handler."""

    def setUp(self):
        bot.bot.reset_mock()

    def test_sends_sticker_on_start(self):
        """welcome() should open the sticker file and call send_sticker."""
        msg = _make_message()
        m = mock_open()
        with patch('builtins.open', m):
            bot.welcome(msg)

        m.assert_called_once_with('static/welcome.webp', 'rb')
        bot.bot.send_sticker.assert_called_once_with(msg.chat.id, m())

    def test_sends_welcome_message_on_start(self):
        """welcome() should call send_message with the user's first name."""
        msg = _make_message()
        msg.from_user.first_name = 'Bob'
        with patch('builtins.open', mock_open()):
            bot.welcome(msg)

        assert bot.bot.send_message.called
        call_kwargs = bot.bot.send_message.call_args
        sent_text = call_kwargs[0][1] if call_kwargs[0] else call_kwargs[1].get('text', '')
        assert 'Bob' in sent_text

    def test_welcome_message_uses_html_parse_mode(self):
        """welcome() should use parse_mode='html' for bold bot name."""
        msg = _make_message()
        with patch('builtins.open', mock_open()):
            bot.welcome(msg)

        _, kwargs = bot.bot.send_message.call_args
        assert kwargs.get('parse_mode') == 'html'

    def test_welcome_attaches_reply_keyboard(self):
        """welcome() should attach a ReplyKeyboardMarkup."""
        msg = _make_message()
        with patch('builtins.open', mock_open()):
            bot.welcome(msg)

        _, kwargs = bot.bot.send_message.call_args
        assert kwargs.get('reply_markup') is not None

    def test_welcome_missing_sticker_file_raises(self):
        """welcome() should propagate FileNotFoundError when sticker is absent."""
        msg = _make_message()
        with patch('builtins.open', side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                bot.welcome(msg)


# ---------------------------------------------------------------------------
# Tests: text handler (handle_text)
# ---------------------------------------------------------------------------

class TestHandleTextRandom(unittest.TestCase):
    """Tests for the random-number branch of handle_text."""

    def setUp(self):
        bot.bot.reset_mock()

    def test_random_number_sent_for_dice_button(self):
        """handle_text() should send a number string for the dice button."""
        msg = _make_message(text='🎲 Рандомное число')
        bot.handle_text(msg)

        bot.bot.send_message.assert_called_once()
        args, _ = bot.bot.send_message.call_args
        sent_value = int(args[1])          # must be convertible to int
        assert 0 <= sent_value <= 100

    def test_random_number_is_in_range(self):
        """Random output should always be 0–100 (100 samples)."""
        msg = _make_message(text='🎲 Рандомное число')
        for _ in range(100):
            bot.bot.reset_mock()
            bot.handle_text(msg)
            args, _ = bot.bot.send_message.call_args
            value = int(args[1])
            assert 0 <= value <= 100, f"Out-of-range value: {value}"

    def test_random_number_seeded(self):
        """With a fixed seed, random.randint should produce a deterministic result."""
        msg = _make_message(text='🎲 Рандомное число')
        with patch('random.randint', return_value=42):
            bot.handle_text(msg)
        args, _ = bot.bot.send_message.call_args
        assert args[1] == '42'

    def test_random_number_sent_to_correct_chat(self):
        """handle_text() should reply to the originating chat_id."""
        msg = _make_message(text='🎲 Рандомное число', chat_id=777)
        bot.handle_text(msg)
        args, _ = bot.bot.send_message.call_args
        assert args[0] == 777


class TestHandleTextHowAreYou(unittest.TestCase):
    """Tests for the 'how are you' branch of handle_text."""

    def setUp(self):
        bot.bot.reset_mock()

    def test_how_are_you_sends_message(self):
        """handle_text() should send a reply for the '😊 Как дела?' button."""
        msg = _make_message(text='😊 Как дела?')
        bot.handle_text(msg)
        bot.bot.send_message.assert_called_once()

    def test_how_are_you_attaches_inline_keyboard(self):
        """The 'how are you' reply should include an inline keyboard."""
        msg = _make_message(text='😊 Как дела?')
        bot.handle_text(msg)
        _, kwargs = bot.bot.send_message.call_args
        assert kwargs.get('reply_markup') is not None

    def test_how_are_you_correct_chat(self):
        """The reply should go to the same chat_id."""
        msg = _make_message(text='😊 Как дела?', chat_id=888)
        bot.handle_text(msg)
        args, _ = bot.bot.send_message.call_args
        assert args[0] == 888


class TestHandleTextUnknown(unittest.TestCase):
    """Tests for the fallback branch of handle_text."""

    def setUp(self):
        bot.bot.reset_mock()

    def test_unknown_text_sends_fallback_message(self):
        """handle_text() should send a 'I don't know' message for unrecognised input."""
        msg = _make_message(text='something completely unrecognised')
        bot.handle_text(msg)
        bot.bot.send_message.assert_called_once()
        args, _ = bot.bot.send_message.call_args
        assert '😢' in args[1]

    def test_empty_string_sends_fallback(self):
        """An empty string is not a known command and should get a fallback reply."""
        msg = _make_message(text='')
        bot.handle_text(msg)
        bot.bot.send_message.assert_called_once()

    def test_case_sensitive_matching(self):
        """Button text matching is case-sensitive; wrong case → fallback."""
        msg = _make_message(text='как дела?')  # lowercase variant
        bot.handle_text(msg)
        args, _ = bot.bot.send_message.call_args
        assert '😢' in args[1]


class TestHandleTextGroupChat(unittest.TestCase):
    """handle_text() must silently ignore non-private chats."""

    def setUp(self):
        bot.bot.reset_mock()

    def test_group_message_ignored(self):
        msg = _make_message(text='🎲 Рандомное число', chat_type='group')
        bot.handle_text(msg)
        bot.bot.send_message.assert_not_called()

    def test_supergroup_message_ignored(self):
        msg = _make_message(text='😊 Как дела?', chat_type='supergroup')
        bot.handle_text(msg)
        bot.bot.send_message.assert_not_called()

    def test_channel_message_ignored(self):
        msg = _make_message(text='hello', chat_type='channel')
        bot.handle_text(msg)
        bot.bot.send_message.assert_not_called()


# ---------------------------------------------------------------------------
# Tests: inline callback handler (callback_inline)
# ---------------------------------------------------------------------------

class TestCallbackInlineGood(unittest.TestCase):
    """Tests for callback_data='good'."""

    def setUp(self):
        bot.bot.reset_mock()

    def test_good_callback_sends_positive_reply(self):
        call = _make_call(data='good')
        bot.callback_inline(call)
        bot.bot.send_message.assert_called_once_with(
            call.message.chat.id, 'Вот и отличненько 😊'
        )

    def test_good_callback_removes_inline_keyboard(self):
        call = _make_call(data='good')
        bot.callback_inline(call)
        bot.bot.edit_message_text.assert_called_once()
        _, kwargs = bot.bot.edit_message_text.call_args
        assert kwargs.get('reply_markup') is None

    def test_good_callback_restores_original_question_text(self):
        call = _make_call(data='good')
        bot.callback_inline(call)
        _, kwargs = bot.bot.edit_message_text.call_args
        assert kwargs.get('text') == '😊 Как дела?'

    def test_good_callback_shows_alert(self):
        call = _make_call(data='good')
        bot.callback_inline(call)
        bot.bot.answer_callback_query.assert_called_once_with(
            callback_query_id=call.id,
            show_alert=False,
            text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11",
        )


class TestCallbackInlineBad(unittest.TestCase):
    """Tests for callback_data='bad'."""

    def setUp(self):
        bot.bot.reset_mock()

    def test_bad_callback_sends_empathetic_reply(self):
        call = _make_call(data='bad')
        bot.callback_inline(call)
        bot.bot.send_message.assert_called_once_with(
            call.message.chat.id, 'Бывает 😢'
        )

    def test_bad_callback_removes_inline_keyboard(self):
        call = _make_call(data='bad')
        bot.callback_inline(call)
        _, kwargs = bot.bot.edit_message_text.call_args
        assert kwargs.get('reply_markup') is None

    def test_bad_callback_shows_alert(self):
        call = _make_call(data='bad')
        bot.callback_inline(call)
        assert bot.bot.answer_callback_query.called


class TestCallbackInlineEdgeCases(unittest.TestCase):
    """Edge cases for the callback handler."""

    def setUp(self):
        bot.bot.reset_mock()

    def test_unknown_callback_data_no_send_message(self):
        """Unknown callback_data should not send any message (no branch matches)."""
        call = _make_call(data='unknown_action')
        bot.callback_inline(call)
        bot.bot.send_message.assert_not_called()

    def test_unknown_callback_still_edits_and_answers(self):
        """Even for unknown data, the keyboard should be removed and alert shown."""
        call = _make_call(data='unknown_action')
        bot.callback_inline(call)
        assert bot.bot.edit_message_text.called
        assert bot.bot.answer_callback_query.called

    def test_none_message_is_handled_gracefully(self):
        """callback_inline must not raise when call.message is None/falsy."""
        call = _make_call(data='good')
        call.message = None
        try:
            bot.callback_inline(call)
        except Exception as exc:
            self.fail(f"callback_inline raised {exc!r} for call.message=None")

    def test_exception_during_send_is_caught(self):
        """Exceptions from bot API calls must be swallowed (not re-raised)."""
        call = _make_call(data='good')
        bot.bot.send_message.side_effect = RuntimeError("network error")
        try:
            bot.callback_inline(call)
        except RuntimeError:
            self.fail("callback_inline should not propagate RuntimeError")

    def test_correct_message_id_used_for_edit(self):
        """edit_message_text must reference the original message_id."""
        call = _make_call(data='good', message_id=42)
        bot.callback_inline(call)
        _, kwargs = bot.bot.edit_message_text.call_args
        assert kwargs.get('message_id') == 42

    def test_correct_chat_id_used_for_edit(self):
        """edit_message_text must reference the correct chat_id."""
        call = _make_call(data='bad', chat_id=555)
        bot.callback_inline(call)
        _, kwargs = bot.bot.edit_message_text.call_args
        assert kwargs.get('chat_id') == 555


if __name__ == '__main__':
    unittest.main()
