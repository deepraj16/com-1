from flask import Flask, render_template, request, flash
import pandas as pd
from df_preprocessing import df_of_comment
from simple_about_video import simple_info
from date_time import (
    plot_comments_per_day,
    plot_comments_by_weekday,
    plot_avg_comment_length_over_time,
    plot_weekly_comments,
    fig_to_base64
)
from nlp_info import (
    text_stats,
    sentmint_grph,
    sentmint_bar,
    mostcommn_word,
    make_word_cloud,
    make_bigram,
    make_emoji_graph,
    show_comments
)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

@app.route('/', methods=['GET', 'POST'])
def index():
    graphs = {}
    stats = None
    video_info = None
    result={}
    if request.method == 'POST':
        url = request.form['url'].strip()
        if not url:
            flash("Please enter a valid YouTube video URL.", "danger")
            return render_template('index.html')

        try:
            video_info = simple_info(url)
            df = df_of_comment(url)
            result = show_comments(df)

            graphs = {
                'per_day': fig_to_base64(plot_comments_per_day(df)),
                'by_weekday': fig_to_base64(plot_comments_by_weekday(df)),
                'avg_length': fig_to_base64(plot_avg_comment_length_over_time(df)),
                'weekly': fig_to_base64(plot_weekly_comments(df)),
                'sentmint_grph': fig_to_base64(sentmint_grph(df)),
                'sentmint_bar': fig_to_base64(sentmint_bar(df)),
                'most_common': fig_to_base64(mostcommn_word(df)),
                'wordcloud': fig_to_base64(make_word_cloud(df)),
                'bigram': fig_to_base64(make_bigram(df)),
                'emoji': fig_to_base64(make_emoji_graph(df))
            }

            stats = text_stats(df)

        except Exception as e:
            flash(f"Error: {str(e)}", "danger")

    return render_template(
        'index2.html',
        graphs=graphs,
        stats=stats,
        video_info=video_info
    )

if __name__ == '__main__':
    app.run(debug=True)
