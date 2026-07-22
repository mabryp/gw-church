#!/usr/bin/env python3
"""Regenerate both reading-plan embed documents on the shared template.
Content transcribed verbatim from the original embeds (raw/embeds/)."""
import html

ROOT = '/Users/mabryp/repositories/gateway_site_work'
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

MATTHEW = {
    'title': 'The Gospel of Matthew',
    'doc_title': 'Matthew Reading Plan — Gospel Reading Plan Year One',
    'subtitle': None,
    'pills': ['14 Weeks', 'April 6 – July 10, 2026', 'Monday–Friday Readings'],
    'footer': 'Gateway Church · Gospel Reading Plan · 2026 — Next up: The Gospel of Mark · Weeks 15–21',
    'weeks': [
        # (num, range, topic, dates, [5 passages], ot_refs, why, quiz_url)
        (1, 'Matthew 1–2', 'Birth & Early Life', 'Apr 6 – Apr 10',
         ['1:1–17', '1:18–25', '2:1–12', '2:13–18', '2:19–23'],
         '2 Sam 7:12–16 · Micah 5:2 · Hosea 11:1 · Jer 31:15 · Isa 7:14',
         'These passages form the backbone of Messianic expectation—promises of a Davidic King, a Bethlehem birth, and prophetic echoes in suffering. Matthew presents Jesus as their fulfillment.',
         'https://docs.google.com/forms/d/e/1FAIpQLSdZNN70c3JJGHEsHG7HHqKHs1hWxMt74FGsJGEIyhBAdX7PZA/viewform?usp=dialog'),
        (2, 'Matthew 3–4', 'Baptism & Temptation', 'Apr 13 – Apr 17',
         ['3:1–12', '3:13–17', '4:1–11', '4:12–17', '4:18–25'],
         'Isa 40:3 · Deut 8:3; 6:16; 6:13',
         'John fulfills Isaiah’s “voice in the wilderness.” Jesus’ temptations echo Israel’s wilderness testing—where Israel failed, Christ succeeds.',
         'https://docs.google.com/forms/d/e/1FAIpQLSdu0W5DFwt9dvCJ9TO4n6VehvGezfTr7ROyHeJuji_X5Lgr3g/viewform?usp=dialog'),
        (3, 'Matthew 5', 'Sermon on the Mount I', 'Apr 20 – Apr 24',
         ['5:1–12', '5:13–26', '5:27–37', '5:38–48', '5:17–20 (re-read)'],
         'Exodus 20 · Leviticus 19:18',
         'Jesus is not abolishing the Law—He is fulfilling and intensifying it. These passages show the original commandments He now interprets at the heart level.',
         'https://docs.google.com/forms/d/e/1FAIpQLSfDFlUdOg9AeA2yxQFkx8B52P-IswpzxA6xgvSP3f4gO7oyXw/viewform?usp=dialog'),
        (4, 'Matthew 6–7', 'Sermon on the Mount II', 'Apr 27 – May 1',
         ['6:1–18', '6:19–34', '7:1–12', '7:13–23', '7:24–29'],
         'Proverbs 3:5–6 · Psalm 1',
         'These wisdom texts reinforce Jesus’ teaching: true righteousness is not external—it is rooted in trust, obedience, and a transformed heart.',
         'https://docs.google.com/forms/d/e/1FAIpQLScARUPmtFN2nA-NMcFj6x-RHx8LxnNzAddAHt8oWBwgodTBmg/viewform?usp=sharing&ouid=115640525677031127885'),
        (5, 'Matthew 8–9', 'Miracles & Faith', 'May 4 – May 8',
         ['8:1–17', '8:18–34', '9:1–17', '9:18–31', '9:32–38'],
         'Isaiah 53:4',
         'Matthew connects Jesus’ healing ministry to the Suffering Servant, showing His miracles are signs of redemptive restoration—not random acts of power.',
         'https://docs.google.com/forms/d/e/1FAIpQLScGgEjsZ2myHPzYl96zDoEFQT1nSTVngoEEVK-fb1wGO4uRNg/viewform?usp=dialog'),
        (6, 'Matthew 10', 'The Twelve Sent Out', 'May 11 – May 15',
         ['10:1–15', '10:16–25', '10:26–33', '10:34–39', '10:40–42'],
         'Micah 7:6',
         'Jesus warns that allegiance to Him will divide even families—echoing prophetic warnings that faithfulness to God often brings conflict, not comfort.',
         'https://docs.google.com/forms/d/e/1FAIpQLSckhmU9hFqXArX40muyDVAWLlcML5XX4EMmW-CNQ1xSf74PnQ/viewform?usp=dialog'),
        (7, 'Matthew 11–12', 'Jesus & Opposition', 'May 18 – May 22',
         ['11:1–19', '11:20–30', '12:1–21', '12:22–37', '12:38–50'],
         'Isaiah 42:1–4 · Psalm 110:1',
         'Jesus is revealed as both the Gentle Servant and the Exalted Lord—a tension that explains why so many misunderstood Him.',
         'https://docs.google.com/forms/d/e/1FAIpQLSc9DUy2RWzDs0NMewoAJn3mZBrV8BcixNHk98Q2NTIrIfj_mA/viewform?usp=dialog'),
        (8, 'Matthew 13', 'Parables of the Kingdom', 'May 25 – May 29',
         ['13:1–23', '13:24–43', '13:44–52', '13:53–58', 'Review 13:1–52'],
         'Isaiah 6:9–10 · Psalm 78:2',
         'Parables both reveal and conceal truth—just as Isaiah foretold. They expose the condition of the heart, not just the content of the message.',
         'https://docs.google.com/forms/d/e/1FAIpQLSdXTtwHYgJQcvM6NMrPxt4pqF6TOSOv5iw05MZnha-thFF9Gg/viewform?usp=dialog'),
        (9, 'Matthew 14–15', 'Feeding & Faith', 'Jun 1 – Jun 5',
         ['14:1–21', '14:22–36', '15:1–20', '15:21–39', 'Review 14:33 & 15:28'],
         'Psalm 107:29 · Isaiah 29:13',
         'Jesus demonstrates authority over creation and exposes hollow religion—God desires true worship, not empty tradition.',
         ''),
        (10, 'Matthew 16–17', 'Peter’s Confession', 'Jun 8 – Jun 12',
         ['16:1–20', '16:21–28', '17:1–13', '17:14–23', '17:24–27'],
         'Daniel 7:13–14 · Psalm 2',
         'These texts define the Messiah as both Suffering Servant and Glorious King—the tension the disciples struggle to grasp.',
         ''),
        (11, 'Matthew 18–20', 'Kingdom Ethics', 'Jun 15 – Jun 19',
         ['18:1–20', '18:21–35', '19:1–15', '19:16–30', '20:1–34'],
         'Isaiah 53:10–12',
         'True greatness in the Kingdom comes through humility, sacrifice, and service—patterns fulfilled in Christ Himself.',
         'https://docs.google.com/forms/d/e/1FAIpQLSfW2R28nFNCasN1W-ibm9F-NwvolIJOdoefgPPUBEZmGLUzUw/viewform'),
        (12, 'Matthew 21–24:14', 'Jerusalem & Transition', 'Jun 22 – Jun 26',
         ['21:1–17', '21:18–46', '22:1–22', '22:23–46', '23:1–39 + 24:1–14'],
         'Zech 9:9 · Psalm 118:22–26 · Psalm 110:1',
         'Jesus enters as King, yet is rejected—fulfilling prophecy. The “rejected stone” becomes the cornerstone of God’s redemptive plan.',
         'https://docs.google.com/forms/d/e/1FAIpQLSeZT3E4jGJHFtQl69itCmS_jL_zRJ8Jcg7VrwYUFUm9uaJHYg/viewform'),
        (13, 'Matthew 24:15–26:35', 'Judgment & Preparation', 'Jun 29 – Jul 3',
         ['24:15–35', '24:36–51', '25:1–30', '25:31–46', '26:1–35'],
         'Daniel 7',
         'Jesus frames history in terms of final judgment and eternal kingship—echoing Daniel’s vision of the Son of Man reigning forever.',
         ''),
        (14, 'Matthew 26:36–28:20', 'The Cross & Resurrection', 'Jul 6 – Jul 10',
         ['26:36–75', '27:1–26', '27:27–44', '27:45–66', '28:1–20'],
         'Psalm 22 · Isaiah 53',
         'The clearest prophetic windows into the Cross—revealing that Jesus’ suffering was not accidental, but ordained, substitutionary, and redemptive.',
         ''),
    ],
}

MARK = {
    'title': 'The Gospel of Mark',
    'doc_title': 'The Gospel of Mark Reading Plan',
    'subtitle': 'Follow Jesus through Mark’s fast-moving account of the Servant-King: acting with authority, showing compassion, suffering willingly, and triumphing over death.',
    'pills': ['7 Weeks', 'July 13 – August 28, 2026', 'Monday–Friday Readings'],
    'footer': 'Gateway Church · Gospel Reading Plan · 2026',
    'weeks': [
        # (num, range, topic, dates, [5 passages], ot_refs, summary, quiz_url)
        (15, 'Mark 1–2', 'The Servant Begins', 'July 13–17',
         ['Mark 1:1–20', 'Mark 1:21–45', 'Mark 2:1–17', 'Mark 2:18–28', 'Review Mark 2:10'],
         'Isaiah 40:3 · Psalm 2',
         'Mark introduces Jesus with urgency and action. The promised Messiah immediately begins proclaiming the Kingdom, demonstrating divine authority through teaching, healing, forgiving sins, and calling ordinary people to follow Him.',
         'https://docs.google.com/forms/d/e/1FAIpQLSdczQGEPYIHeiS684CpFBCeg3OtYioB4kD1ZE2tHfwsjjjdyA/viewform'),
        (16, 'Mark 3–4', 'The Servant Under Opposition', 'July 20–24',
         ['Mark 3:1–19', 'Mark 3:20–35', 'Mark 4:1–20', 'Mark 4:21–34', 'Mark 4:35–41'],
         'Isaiah 6 · Psalm 107:23–30',
         'As Jesus’ ministry expands, opposition also grows. His parables reveal the condition of the human heart, while His authority over nature confirms that even creation obeys the Servant-King.',
         'https://docs.google.com/forms/d/e/1FAIpQLSeT4y-AgRnDmH6gBz-KpMqFxToK-W5n0yqFWTvOQlOaz0PfIQ/viewform'),
        (17, 'Mark 5–6', 'The Compassionate Servant', 'July 27–31',
         ['Mark 5:1–20', 'Mark 5:21–43', 'Mark 6:1–29', 'Mark 6:30–44', 'Mark 6:45–56'],
         'Psalm 23 · Psalm 107',
         'Jesus displays remarkable compassion toward the desperate, the broken, and the outcast. His miracles reveal both His divine power and His deep concern for those who come to Him in faith.',
         'https://docs.google.com/forms/d/e/1FAIpQLSfcweGTbb97iCyXQYZMz-sGy8R22S3uzkb5yW1dv2CwNj64dA/viewform'),
        (18, 'Mark 7–8', 'The Revealed Servant', 'August 3–7',
         ['Mark 7:1–23', 'Mark 7:24–37', 'Mark 8:1–21', 'Mark 8:22–30', 'Mark 8:31–38'],
         'Isaiah 29:13 · Daniel 7:13–14',
         'Jesus exposes empty religion while progressively revealing His true identity. Peter’s confession marks a turning point as Jesus begins preparing His disciples for a suffering Messiah rather than a conquering political king.',
         'https://docs.google.com/forms/d/e/1FAIpQLScy6y6zdiMP_aG-0ZTkSxQgIA2Y6JYdye-0G8h65eOlPUzh7w/viewform'),
        (19, 'Mark 9–10', 'The Serving King', 'August 10–14',
         ['Mark 9:1–29', 'Mark 9:30–50', 'Mark 10:1–31', 'Mark 10:32–45', 'Mark 10:46–52'],
         'Isaiah 53',
         'Greatness in God’s Kingdom is measured by humility and service. Jesus teaches that the King Himself came not to be served, but to serve and to give His life as a ransom for many.',
         'https://docs.google.com/forms/d/e/1FAIpQLSfRsGCycQNO6Go9f8aas_c09SO_8wmz7FQjFBjnRHvbrWlxxA/viewform'),
        (20, 'Mark 11–16', 'The Suffering Servant Triumphs', 'August 17–21',
         ['Mark 11–12', 'Mark 13', 'Mark 14', 'Mark 15', 'Mark 16'],
         'Psalm 22 · Isaiah 53 · Daniel 7',
         'The Servant willingly lays down His life, accomplishing redemption through the cross. His resurrection vindicates every claim He made and proclaims His victory over sin, death, and the grave.',
         'https://docs.google.com/forms/d/e/1FAIpQLSfV_PScIevBUk4TJYhN3bPCSK7KHx_vzzWJVmohEA2FFSty9Q/viewform'),
        (21, 'Transition · Mark 10:45 & Luke 1:1–4', 'From Servant to Savior', 'August 24–28',
         ['Mark 10:45', 'Luke 1:1–2', 'Luke 1:3–4', 'Review Both Passages', 'Reflective Reading'],
         None,
         'Mark presents Jesus as the Servant who acts with authority, compassion, and sacrificial love. Luke now begins an orderly account, inviting us to understand with certainty who Jesus is and why His life changes everything.',
         'https://docs.google.com/forms/d/e/1FAIpQLSe_utf8OKAsEdcB3Jag5gKG6iTuxNQnwYhtzAceOssv8HyOUQ/viewform'),
    ],
}

INTRO = """  <section class="intro">
    <h2>How to Use This Plan</h2>
    <p>
      Read the assigned passage each weekday. Take time to notice what the text reveals about
      Jesus, how people respond to Him, and what faithful discipleship requires.
    </p>
  </section>"""

THREE_CS = """  <section class="three-cs">
    <h2>The Three C’s of Reading</h2>
    <p>As you read each day, consider whether the passage leaves you convicted, confused, or confirmed.</p>
    <div class="c-grid">
      <div class="c-card">
        <strong>Convicted</strong>
        What is God showing me that needs to change in my beliefs, attitudes, or actions?
      </div>
      <div class="c-card">
        <strong>Confused</strong>
        What do I not yet understand, and what question should I bring to further study?
      </div>
      <div class="c-card">
        <strong>Confirmed</strong>
        What truth about God, Christ, or faithful living has been strengthened in me?
      </div>
    </div>
  </section>"""

QUIZ_JS = """<script>
  // Activates a week's quiz button when a URL is present in data-quiz-url
  document.querySelectorAll('.week[data-quiz-url]').forEach(function (card) {
    var url = card.getAttribute('data-quiz-url').trim();
    if (url) {
      var btn = card.querySelector('.quiz-btn');
      if (btn) {
        btn.href = url;
        btn.classList.add('active');
      }
    }
  });
</script>"""

def esc(s):
    return html.escape(s, quote=False)

def week_html(num, rng, topic, dates, passages, ot, note, note_class, quiz):
    quiz_attr = f' data-quiz-url="{html.escape(quiz)}"' if quiz is not None else ''
    days = '\n'.join(
        f'          <div class="day"><strong>{d}</strong><span>{esc(p)}</span></div>'
        for d, p in zip(DAYS, passages))
    parts = [f"""    <article class="week"{quiz_attr}>
      <header class="week-header">
        <div class="week-number">Week <span>{num}</span></div>
        <div class="week-title">
          <h2>{esc(topic)}</h2>
          <p>{esc(rng)}</p>
        </div>
        <div class="date">{esc(dates)}</div>
      </header>
      <div class="week-body">
        <div class="readings">
{days}
        </div>"""]
    if ot:
        label = 'Old Testament Connection' + ('s' if '·' in ot or ';' in ot else '')
        ot_block = f"""        <div class="ot">
          <p class="ot-refs">{label}: {esc(ot)}</p>"""
        if note_class == 'ot-why':
            ot_block += f"""
          <p class="ot-why">{esc(note)}</p>"""
        ot_block += """
        </div>"""
        parts.append(ot_block)
    if note_class == 'summary':
        parts.append(f"""        <p class="summary">{esc(note)}</p>""")
    if quiz is not None:
        parts.append(f"""        <a class="quiz-btn" target="_blank" rel="noopener">Take the Week {num} Quiz</a>""")
    parts.append("""      </div>
    </article>""")
    return '\n'.join(parts)

def build(plan, note_class, has_quizzes):
    weeks = '\n\n'.join(
        week_html(num, rng, topic, dates, passages, ot, note, note_class,
                  quiz if has_quizzes else None)
        for (num, rng, topic, dates, passages, ot, note, quiz) in plan['weeks'])
    subtitle = f"""
    <p class="subtitle">
      {esc(plan['subtitle'])}
    </p>""" if plan['subtitle'] else ''
    pills = '\n      '.join(f'<span class="meta-pill">{esc(p)}</span>' for p in plan['pills'])
    script = ('\n' + QUIZ_JS) if has_quizzes else ''
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(plan['doc_title'])}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="reading-plan.css">
</head>
<body>
<main class="reading-plan">
  <section class="hero">
    <p class="eyebrow">Gospel Reading Plan · Year One</p>
    <h1>{esc(plan['title'])}</h1>{subtitle}
    <div class="meta-row">
      {pills}
    </div>
  </section>

  <button class="print-btn no-print" onclick="window.print()">Print / Save as PDF</button>

{INTRO}

  <section class="weeks">

{weeks}

  </section>

{THREE_CS}

  <p class="footer-note">{esc(plan['footer'])}</p>
</main>{script}
</body>
</html>
"""

with open(f'{ROOT}/site/embeds/matthew-reading-plan.html', 'w') as f:
    f.write(build(MATTHEW, 'ot-why', True))
with open(f'{ROOT}/site/embeds/mark-reading-plan.html', 'w') as f:
    f.write(build(MARK, 'summary', True))
print('wrote both plans')
