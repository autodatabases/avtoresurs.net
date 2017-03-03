def get_i_board(queryset, lang, columns=2, payload=False):
    """ wee need to have ru_name, en_name and id fields in query sets objects """
    markup = []
    callbacks = []
    m_line = []
    cb_line = []
    for ind, button in enumerate(queryset):
        if lang == 'ru':
            m_line.append(button.ru_name)
        else:
            m_line.append(button.en_name)
        if not payload:
            cb_line.append("%s_%s" % (button.caption, button.id))
        else:
            cb_line.append("%s_%s|%s" % (button.caption, button.id, payload))
        if (ind + 1) % columns == 0:
            markup.append(sorted(m_line, reverse=False))
            callbacks.append(sorted(cb_line, reverse=False))
            m_line = []
            cb_line = []
    if cb_line not in callbacks:
        callbacks.append(cb_line)
    if m_line not in markup:
        markup.append(m_line)
    markup = sorted(markup, reverse=False)
    callbacks = sorted(callbacks, reverse=False)
    keyboard = kb.get_inline_keyboard(keyboard=markup, callbacks=callbacks)

    return keyboard