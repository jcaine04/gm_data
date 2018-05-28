from data import get_session, Message

from wordcloud import WordCloud, STOPWORDS

def word_cloud_generator():
    session = get_session()
    messages = session.query(Message).filter_by(group_id='3009645').all()

    text = ' '.join([str(message.text) for message in messages])
    stopwords = set(STOPWORDS)

    # filter out some less interesting words
    additional_stopwords = ("None", 'https')
    for word in additional_stopwords:
        stopwords.add(word)

    wc = WordCloud(background_color='white', max_words=2000, stopwords=stopwords, width=1600, height=800,
                   normalize_plurals=False)
    wc.generate(text)
    wc.to_file('xavier_wc.png')

    # additional_stopwords = ("None", 'https', 'guy', 'Guy')
    # for word in additional_stopwords:
    #     stopwords.add(word)
    #
    # wc = WordCloud(background_color='white', max_words=2000, stopwords=stopwords, width=1600, height=800,
    #                normalize_plurals=False)
    # wc.generate(text)
    # wc.to_file('mcl_wc_filtered.png')


if __name__ == '__main__':
    word_cloud_generator()